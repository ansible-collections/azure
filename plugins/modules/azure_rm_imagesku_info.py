#!/usr/bin/python
#
# Copyright (c) 2024
# Hen Yaish <hyaish@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_imagesku_info

version_added: "2.4.0"

short_description: Get compute-related Image SKUs list

description:
    - Get details for compute-related resource Image SKUs.

options:
    location:
        description:
            - A region supported by current subscription.
        type: str
    offer:
        description:
            - The `Offer` refers to the specific product line of the operating system or software.
            - The offer usually includes multiple versions or configurations of the product.
        type: str
    publisher:
        description:
            - The `Publisher` is the entity that provides the OS image. It could be Microsoft, Canonical (for Ubuntu), Red Hat, etc.
            - It is a mandatory field that identifies the provider of the image.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Hen Yaish (@hyaish)

'''

EXAMPLES = '''
- name: Gather Resource Group info
  azure.azcollection.azure_rm_resourcegroup_info:
    name: "{{ resource_group }}"
  register: rg_info

- name: List available Image SKUs for 0001-com-ubuntu-server-focal
  azure.azcollection.azure_rm_imagesku_info:
    location: westus
    offer: 0001-com-ubuntu-server-focal
    publisher: Canonical
  register: available_image_skus_results
'''

RETURN = '''
available_skus:
    description:
        - List of Azure image SKUs for provisioning virtual machines.
    returned: always
    type: complex
    contains:
        name:
            description:
                - The specific SKU name or version.
            returned: always
            type: str
            sample: "20_04-lts"
        id:
            description:
                - The full Azure resource ID for the SKU.
            returned: always
            type: str
            sample: "0001-com-ubuntu-server-focal/Skus/20_04-lts"
        location:
            description:
                - The Azure region where the SKU is available.
            returned: always
            type: str
            sample: "westus"
        automatic_os_upgrade_supported:
            description:
                - Whether automatic OS upgrades are supported for this SKU.
            returned: always
            type: bool
            sample: false
        restrictions:
            description:
                - Restrictions that may apply to the use of this image SKU, such as region limitations or feature incompatibility.
            returned: always
            type: complex
            contains:
                type:
                    description:
                        - The type of restriction, which could include location-based restrictions or hardware compatibility issues.
                    type: str
                    returned: always
                    sample: "location"
                restriction_values:
                    description:
                        - A list of restricted locations, regions, or zones where the image SKU cannot be used.
                    type: list
                    returned: always
                    sample: ["eastus", "westeurope"]
                values:
                    description:
                        - A list of restricted locations, regions, or zones where the image SKU cannot be used.
                        - This return value has been deprecated and will be removed in a release after
                          2027-05-01. Use C(restriction_values) instead.
                    type: list
                    returned: always
                    sample: ["eastus", "westeurope"]
                reason_code:
                    description:
                        - The reason for the restriction, such as quota limitations or specific hardware requirements.
                    type: str
                    sample: "NotSupported"
                restriction_info:
                    description:
                        - Additional information about the restrictions, such as unsupported regions or features.
                    returned: always
                    type: complex
                    contains:
                        locations:
                            description:
                                - Locations where this SKU is restricted or unavailable.
                            type: list
                            sample: ["eastus"]
                        zones:
                            description:
                                - Availability zones within the region where this SKU is restricted.
                            type: list
                            sample: ["1", "2"]
'''


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
try:
    from azure.mgmt.compute import ComputeManagementClient
    from azure.core.exceptions import HttpResponseError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMImageskuInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            location=dict(type='str'),
            publisher=dict(type='str'),
            offer=dict(type='str'),
        )

        self.results = dict(
            available_skus=[],
            count=0
        )
        self.location = None
        self.publisher = None
        self.offer = None
        super(AzureRMImageskuInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        available_skus = self.list_skus()
        self.results['available_skus'] = available_skus
        self.results['count'] = len(available_skus)
        self.module.deprecate(
            "The 'values' return key in 'restrictions' is deprecated. Use 'restriction_values' instead.",
            date="2027-05-01",
            collection_name="azure.azcollection",
        )
        return self.results

    def list_skus(self):
        try:
            compute_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                      base_url=self._cloud_environment.endpoints.resource_manager,
                                                      api_version='2021-07-01')
            skus_result = compute_client.virtual_machine_images.list_skus(location=self.location,
                                                                          publisher_name=self.publisher,
                                                                          offer=self.offer)
            available_skus = []

            for sku_info in skus_result:
                sku_dict = sku_info.as_dict()
                for restriction in sku_dict.get('restrictions', []):
                    if 'values' in restriction:
                        restriction['restriction_values'] = restriction['values']
                available_skus.append(sku_dict)
            return available_skus

        except HttpResponseError as e:
            # Handle exceptions
            raise e


def _match_location(loc, locations):
    return next((x for x in locations if x.lower() == loc.lower()), None)


def _is_sku_available(sku_info, zone):
    """
    The SKU is unavailable in the following cases:
    1. regional restriction and the region is restricted
    2. parameter "zone" is input which indicates only showing skus with availability zones.
       Meanwhile, zonal restriction and all zones are restricted
    """
    is_available = True
    is_restrict_zone = False
    is_restrict_location = False
    if not sku_info.restrictions:
        return is_available
    for restriction in sku_info.restrictions:
        if restriction.reason_code == 'NotAvailableForSubscription':
            if restriction.type == 'Zone' and not (
                    set(sku_info.location_info[0].zones or []) - set(restriction.restriction_info.zones or [])):
                is_restrict_zone = True
            if restriction.type == 'Location' and (
                    sku_info.location_info[0].location in (restriction.restriction_info.locations or [])):
                is_restrict_location = True
            if is_restrict_location or (is_restrict_zone and zone):
                is_available = False
                break
    return is_available


def main():
    AzureRMImageskuInfo()


if __name__ == '__main__':
    main()
