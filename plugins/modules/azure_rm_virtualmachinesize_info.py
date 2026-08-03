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
        - List of virtual machine size profiles available for the location.
    returned: always
    type: complex
    contains:
        name:
            description:
                - The name of the virtual machine size
            type: str
            sample: Standard_A1_v2
        memory_in_mb:
            description:
                - The amount of memory, in MB, supported by the virtual machine size
            type: int
            sample: 2048
        number_of_cores:
            description:
                - The number of cores supported by the virtual machine size
            type: int
            sample: 1
        max_data_disk_count:
            description:
                - The maximum number of data disks that can be attached to the virtual machine size
            type: int
            sample: 2
        max_write_accelerator_enabled_disk_count:
            description:
                - The maximum number of disks that can have Write Accelerator enabled.
                - Returns C(0) when Write Accelerator is not supported by the virtual machine size.
            type: int
            sample: 4
        os_disk_size_in_mb:
            description:
                - The OS disk size, in MB, allowed by the virtual machine size
            type: int
            sample: 1047552
        resource_disk_size_in_mb:
            description:
                - The resource disk size, in MB, allowed by the virtual machine size
            type: int
            sample: 10240
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

        capabilities = dict((capability.name, capability.value) for capability in size.capabilities or [])

        def _as_int(key, default=None):
            raw = capabilities.get(key)
            if raw is None:
                return default
            try:
                return int(raw)
            except (TypeError, ValueError):
                return default

        memory_gb = capabilities.get('MemoryGB')
        try:
            memory_in_mb = int(float(memory_gb) * 1024) if memory_gb is not None else None
        except (TypeError, ValueError):
            memory_in_mb = None

        return dict(
            name=size.name,
            number_of_cores=_as_int('vCPUs'),
            os_disk_size_in_mb=_as_int('OSVhdSizeMB'),
            resource_disk_size_in_mb=_as_int('MaxResourceVolumeMB'),
            memory_in_mb=memory_in_mb,
            max_data_disk_count=_as_int('MaxDataDiskCount'),
            # MaxWriteAcceleratorDisksAllowed: Azure Resource SKUs API uses 0 to indicate
            # "not supported" for this capability, so default missing values to 0.
            max_write_accelerator_enabled_disk_count=_as_int('MaxWriteAcceleratorDisksAllowed', default=0),
        )


def _match_location(location, locations):
    return next((item for item in locations if item.lower() == location.lower()), None)


def main():
    AzureRMVirtualMachineSizeInfo()


if __name__ == '__main__':
    main()
