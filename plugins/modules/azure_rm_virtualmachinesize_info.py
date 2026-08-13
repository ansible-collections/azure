#!/usr/bin/python
#
# Copyright (c) 2021
# Maxence Ardouin <max@23.tf>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_virtualmachinesize_info

version_added: "1.8.0"

short_description: Get facts for virtual machine sizes

description:
    - Get available virtual machine size profiles for a location

options:
    location:
        description:
            - Location for which to list the available virtual machine size profiles
        required: true
        type: str
    name:
        description:
            - Name of a size to get information about
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Maxence Ardouin (@nbr23)

'''

EXAMPLES = '''
- name: Get all virtual machine size info in eastus
  azure_rm_virtualmachinesize_info:
    location: eastus

- name: Get virtual machine size info for eastus for Standard_A1_v2
  azure_rm_virtualmachinesize_info:
    location: eastus
    name: Standard_A1_v2
'''

RETURN = '''
sizes:
    description:
        - List of virtual machine Resource SKU profiles available for the location.
    returned: always
    type: complex
    contains:
        resource_type:
            description:
                - The type of resource the SKU applies to.
            type: str
            sample: virtualMachines
        name:
            description:
                - The name of the SKU.
            type: str
            sample: Standard_A1_v2
        tier:
            description:
                - The tier of the SKU.
            type: str
            sample: Standard
        size:
            description:
                - The size of the SKU.
            type: str
            sample: A1_v2
        family:
            description:
                - The family of the SKU.
            type: str
            sample: standardAv2Family
        locations:
            description:
                - The locations where the SKU is available.
            type: list
            elements: str
            sample: ["eastus"]
        location_info:
            description:
                - Location and availability zone information for the SKU.
            type: list
            elements: dict
        capabilities:
            description:
                - The capability name and value pairs reported by Azure.
            type: list
            elements: dict
            contains:
                name:
                    description:
                        - The capability name.
                    type: str
                    sample: MaxWriteAcceleratorDisksAllowed
                value:
                    description:
                        - The capability value.
                    type: str
                    sample: "4"
        restrictions:
            description:
                - The restrictions that apply to the SKU.
            type: list
            elements: dict
'''

try:
    from azure.core.exceptions import HttpResponseError
    from azure.mgmt.compute import ComputeManagementClient
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

RESOURCE_SKU_API_VERSION = '2021-07-01'
HYBRID_RESOURCE_SKU_API_VERSION = '2017-09-01'


class AzureRMVirtualMachineSizeInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            location=dict(type='str', required=True),
            name=dict(type='str')
        )

        self.results = dict(
            changed=False,
            sizes=[]
        )

        self.location = None
        self.name = None

        super(AzureRMVirtualMachineSizeInfo, self).__init__(self.module_arg_spec,
                                                            supports_check_mode=True,
                                                            supports_tags=False,
                                                            facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.results['sizes'] = self.list_items_by_location()
        return self.results

    def list_items_by_location(self):
        self.log('List items by location')
        try:
            is_hybrid_profile = self.api_profile == '2019-03-01-hybrid'
            compute_client = self.get_mgmt_svc_client(
                ComputeManagementClient,
                base_url=self._cloud_environment.endpoints.resource_manager,
                api_version=HYBRID_RESOURCE_SKU_API_VERSION if is_hybrid_profile else RESOURCE_SKU_API_VERSION
            )
            if is_hybrid_profile:
                items = compute_client.resource_skus.list()
            else:
                items = compute_client.resource_skus.list(filter="location eq '{0}'".format(self.location))
            return [
                self.serialize_size(item)
                for item in items
                if item.resource_type == 'virtualMachines'
                and (not is_hybrid_profile or _match_location(self.location, item.locations or []))
                and _is_sku_available(item, self.location)
                and (self.name is None or self.name == item.name)
            ]
        except HttpResponseError as exc:
            self.fail("Failed to list items - {0}".format(str(exc)))

    def serialize_size(self, size):
        '''
        Convert a ResourceSku object to a virtual machine size dict.

        :param size: ResourceSku object
        :return: dict
        '''

        return self.serialize_obj(size, 'ResourceSku')


def _match_location(location, locations):
    return next((item for item in locations if item.lower() == location.lower()), None)


def _is_sku_available(sku_info, location):
    if not sku_info.restrictions:
        return True
    for restriction in sku_info.restrictions:
        if restriction.reason_code != 'NotAvailableForSubscription':
            continue
        if restriction.type == 'Location':
            restricted_locations = getattr(restriction.restriction_info, 'locations', None) or []
            if _match_location(location, restricted_locations):
                return False
    return True


def main():
    AzureRMVirtualMachineSizeInfo()


if __name__ == '__main__':
    main()
