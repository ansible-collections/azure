#!/usr/bin/python
#
# Copyright (c) 2024
# Nir Argaman <nargaman@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_vmsku_info

version_added: "2.4.0"

short_description: Get compute-related SKUs list

description:
    - Get details for compute-related resource SKUs.

options:
    location:
        description:
            - A region supported by current subscription.
        type: str
    resource_type:
        description:
            - Resource types e.g. "availabilitySets", "snapshots", "disks", etc.
        type: str
    size:
        description:
            - Size name, partial name is accepted.
        type: str
    zone:
        description:
            - Show skus supporting availability zones.
        type: bool
        default: False

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Nir Argaman (@nirarg)

'''

EXAMPLES = '''
- name: Gather Resource Group info
  azure.azcollection.azure_rm_resourcegroup_info:
    name: "{{ resource_group }}"
  register: rg_info

- name: List available VM SKUs
  azure.azcollection.azure_rm_vmsku_info:
    location: "{{ rg_info.resourcegroups.0.location }}"
    resource_type: "virtualMachines"
    size: "standard_B1"
    zone: true
  register: available_skus_result
'''

RETURN = '''
available_skus:
    description:
        - List of compute-related resource SKUs.
    returned: always
    type: complex
    contains:
        resource_type:
            description:
                - The type of resource the SKU applies to.
            returned: always
            type: str
            sample: "virtual_machine"
        name:
            description:
                - The name of SKU.
            returned: always
            type: str
            sample: "Standard_B1s"
        tier:
            description:
                - Specifies the tier of virtual machines in a scale set.
            returned: always
            type: str
            sample: "Standard"
        size:
            description:
            - The Size of the SKU.
            returned: always
            type: str
            sample: "B1s"
        family:
            description:
            - The Family of this particular SKU.
            returned: always
            type: str
            sample: "standardBSFamily"
        locations:
            description:
            - The set of locations that the SKU is available.
            returned: always
            type: list
            sample: ["eastus"]
        location_info:
            description:
                - A list of locations and availability zones in those locations where the SKU is available.
            returned: always
            type: complex
            contains:
                location:
                    description:
                        - Location of the SKU.
                    type: str
                    returned: always
                    sample: "eastus"
                zones:
                    description:
                        - List of availability zones where the SKU is supported.
                    type: list
                    returned: always
                    sample: ["1", "2", "3"]
                zone_details:
                    description:
                        - Details of capabilities available to a SKU in specific zones.
                    returned: always
                    type: complex
                    contains:
                        capabilities:
                            description:
                                - A list of capabilities that are available for the SKU in the specified list of zones.
                            type: complex
                            returned: always
                            contains:
                                name:
                                    description:
                                        - An invariant to describe the feature.
                                    type: str
                                    returned: always
                                    sample: "ultrassdavailable"
                                value:
                                    description:
                                        - An invariant if the feature is measured by quantity.
                                    type: str
                                    returned: always
                                    sample: "True"
        capabilities:
            description:
                - A name value pair to describe the capability.
            returned: always
            type: complex
            contains:
                name:
                    description:
                        - An invariant to describe the feature.
                    type: str
                    returned: always
                    sample: "ultrassdavailable"
                value:
                    description:
                        - An invariant if the feature is measured by quantity.
                    type: str
                    returned: always
                    sample: "True"
        restrictions:
            description:
                - The restrictions because of which SKU cannot be used. This is empty if there are no restrictions.
            returned: always
            type: complex
            contains:
                type:
                    description:
                        - The type of restrictions.
                    type: str
                    returned: always
                    sample: "location"
                restriction_values:
                    description:
                        - The value of restrictions. If the restriction type is set to location.
                          This would be different locations where the SKU is restricted.
                    type: list
                    returned: always
                    sample: ["eastus"]
                values:
                    description:
                        - The value of restrictions. If the restriction type is set to location.
                          This would be different locations where the SKU is restricted.
                        - This return value has been deprecated and will be removed in a release after
                          2027-05-01. Use C(restriction_values) instead.
                    type: list
                    returned: always
                    sample: ["eastus"]
                restriction_info:
                    description:
                        - The information about the restriction where the SKU cannot be used.
                    returned: always
                    type: complex
                    contains:
                        locations:
                            description:
                                - Locations where the SKU is restricted.
                            type: list
                            sample: ["location"]
                        zones:
                            description:
                                - List of availability zones where the SKU is restricted.
                            type: list
                            sample: ["1", "2"]
                reason_code:
                    description:
                        - The reason for restriction.
                    type: str
                    sample: "QuotaId"
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.mgmt.compute import ComputeManagementClient
    from azure.core.exceptions import HttpResponseError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVmskuInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            location=dict(type='str'),
            resource_type=dict(type='str'),
            size=dict(type='str'),
            zone=dict(type='bool', default=False)
        )

        self.results = dict(
            available_skus=[],
            count=0
        )
        self.location = None
        self.resource_type = None
        self.size = None
        self.zone = False

        super(AzureRMVmskuInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def list_skus(self):
        try:
            compute_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                      base_url=self._cloud_environment.endpoints.resource_manager,
                                                      api_version='2021-07-01')
            skus_result = compute_client.resource_skus.list()
            available_skus = []
            for sku_info in skus_result:
                if self.location and not _match_location(self.location, sku_info.locations):
                    continue
                if not _is_sku_available(sku_info, self.zone):
                    continue
                if self.resource_type and not sku_info.resource_type.lower() == self.resource_type.lower():
                    continue
                if self.size and not (sku_info.resource_type == 'virtualMachines' and self.size.lower() in sku_info.name.lower()):
                    continue
                if self.zone and not (sku_info.location_info and sku_info.location_info[0].zones):
                    continue
                sku_dict = sku_info.as_dict()
                for restriction in sku_dict.get('restrictions', []):
                    if 'values' in restriction:
                        restriction['restriction_values'] = restriction['values']
                available_skus.append(sku_dict)
            return available_skus
        except HttpResponseError as e:
            # Handle exceptions
            raise e

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
    AzureRMVmskuInfo()


if __name__ == '__main__':
    main()
