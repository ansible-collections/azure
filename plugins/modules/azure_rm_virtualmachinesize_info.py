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
        memoryInMB:
            description:
                - The amount of memory, in MB, supported by the virtual machine size
            type: int
            sample: 2048
        numberOfCores:
            description:
                - The number of cores supported by the virtual machine size
            type: int
            sample: 1
        maxDataDiskCount:
            description:
                - The maximum number of data disks that can be attached to the virtual machine size
            type: int
            sample: 2
        osDiskSizeInMB:
            description:
                - The OS disk size, in MB, allowed by the virtual machine size
            type: int
            sample: 1047552
        resourceDiskSizeInMB:
            description:
                - The resource disk size, in MB, allowed by the virtual machine size
            type: int
            sample: 10240
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

AZURE_OBJECT_CLASS = 'VirtualMachineSize'

AZURE_ENUM_MODULES = ['azure.mgmt.compute.models']


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
            items = self.compute_client.virtual_machine_sizes.list(location=self.location)
        except ResourceNotFoundError as exc:
            self.fail("Failed to list items - {0}".format(str(exc)))
        return [self.serialize_size(item) for item in items if self.name is None or self.name == item.name]

    def serialize_size(self, size):
        '''
        Convert a VirtualMachineSize object to dict.

        :param size: VirtualMachineSize object
        :return: dict
        '''

        return self.serialize_obj(size, AZURE_OBJECT_CLASS, enum_modules=AZURE_ENUM_MODULES)


def main():
    AzureRMVirtualMachineSizeInfo()


if __name__ == '__main__':
    main()
