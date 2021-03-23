#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Paul Aiton <@paultaiton>
# Copyright: (c) 2016, Bruno Medina Bolanos Cacho <bruno.medina@microsoft.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: azure_rm_manageddisk_info

version_added: "0.1.2"

short_description: Get managed disk facts

description:
    - Get facts for a specific managed disk or all managed disks.

notes:
    - This module was called M(azure_rm_managed_disk_facts) before Ansible 2.8. The usage did not change.

options:
    name:
        description:
            - Limit results to a specific managed disk.
        type: str
    resource_group:
        description:
            - Limit results to a specific resource group.
            - Required if I(name) is set
        type: str
    tags:
        description:
            - Limit results by providing a list of tags.
            - Format tags as 'key' or 'key:value'.
        type: list
    managed_by:
        description:
            - Limit results to disks managed by the given VM fqid.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Bruno Medina (@brusMX)
    - Paul Aiton (@paultaiton)
'''

EXAMPLES = r'''
- name: Get facts for one managed disk
  azure_rm_manageddisk_info:
    name: Testing
    resource_group: myResourceGroup

- name: Get facts for all managed disks
  azure_rm_manageddisk_info:

- name: Get facts for all managed disks managed by a specific vm
  azure_rm_manageddisk_info:
    managed_by: '/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/rgName/Microsoft.Compute/virtualMachines/vmName'

- name: Get facts by tags
  azure_rm_manageddisk_info:
    tags:
    - testing
'''

RETURN = r'''
azure_managed_disk:
    description:
        - List of managed disk dicts.
    returned: always
    type: list
    contains:
        id:
            description:
                - Resource id.
            type: str
        name:
            description:
                - Name of the managed disk.
            type: str
        location:
            description:
                - Valid Azure location.
            type: str
        storage_account_type:
            description:
                - Type of storage for the managed disk.
                - See U(https://docs.microsoft.com/en-us/azure/virtual-machines/windows/disks-types) for more information about this type.
            type: str
            sample: Standard_LRS
        create_option:
            description:
                - Create option of the disk.
            type: str
            sample: copy
        source_uri:
            description:
                - URI to a valid VHD file to be used or the resource ID of the managed disk to copy.
            type: str
        os_type:
            description:
                - Type of Operating System.
            choices:
                - linux
                - windows
            type: str
        disk_size_gb:
            description:
                - Size in GB of the managed disk to be created.
            type: str
        managed_by:
            description:
                - Name of an existing virtual machine with which the disk is or will be associated, this VM should be in the same resource group.
            type: str
        tags:
            description:
                - Tags to assign to the managed disk.
            type: dict
            sample: { "tag": "value" }
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
except Exception:
    # handled in azure_rm_common
    pass


class AzureRMManagedDiskInfo(AzureRMModuleBase):
    """Utility class to get managed disk facts"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            tags=dict(type='list'),
            managed_by=dict(type='str')
        )

        self.results = dict(
            ansible_info=dict(
                azure_managed_disk=[]
            )
        )

        self.resource_group = None
        self.name = None
        self.tags = None
        self.managed_by = None

        super(AzureRMManagedDiskInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     facts_module=True,
                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name and not self.resource_group:
            self.fail('Parameter Error: name requires that resource_group also be set.')

        if self.name:
            self.results['ansible_info']['azure_managed_disk'] = self.get_disk()
        elif self.resource_group:
            self.results['ansible_info']['azure_managed_disk'] = self.list_disks_by_resource_group()
        else:
            self.results['ansible_info']['azure_managed_disk'] = self.list_disks()

        return self.results

    def get_disk(self):
        """Get a single managed disk"""
        results = []

        try:
            results = [self.compute_client.disks.get(self.resource_group,
                                                     self.name)]
            if self.managed_by:
                results = [disk for disk in results if disk.managed_by == self.managed_by]
            if self.tags:
                results = [disk for disk in results if self.has_tags(disk.tags, self.tags)]
            results = [self.managed_disk_to_dict(disk) for disk in results]
        except CloudError:
            self.log('Could not find disk {0} in resource group {1}'.format(self.name, self.resource_group))

        return results

    def list_disks(self):
        """Get all managed disks"""
        results = []

        try:
            results = self.compute_client.disks.list()
            if self.managed_by:
                results = [disk for disk in results if disk.managed_by == self.managed_by]
            if self.tags:
                results = [disk for disk in results if self.has_tags(disk.tags, self.tags)]
            results = [self.managed_disk_to_dict(disk) for disk in results]
        except CloudError as exc:
            self.fail('Failed to list all items - {0}'.format(str(exc)))

        return results

    def list_disks_by_resource_group(self):
        """Get managed disks in a resource group"""
        results = []

        try:
            results = self.compute_client.disks.list_by_resource_group(resource_group_name=self.resource_group)
            if self.managed_by:
                results = [disk for disk in results if disk.managed_by == self.managed_by]
            if self.tags:
                results = [disk for disk in results if self.has_tags(disk.tags, self.tags)]
            results = [self.managed_disk_to_dict(disk) for disk in results]
        except CloudError as exc:
            self.fail('Failed to list items by resource group - {0}'.format(str(exc)))

        return results

    def managed_disk_to_dict(self, managed_disk):
        create_data = managed_disk.creation_data
        return dict(
            id=managed_disk.id,
            name=managed_disk.name,
            location=managed_disk.location,
            tags=managed_disk.tags,
            create_option=create_data.create_option.lower(),
            source_uri=create_data.source_uri or create_data.source_resource_id,
            disk_size_gb=managed_disk.disk_size_gb,
            os_type=managed_disk.os_type.lower() if managed_disk.os_type else None,
            storage_account_type=managed_disk.sku.name if managed_disk.sku else None,
            managed_by=managed_disk.managed_by,
            zone=managed_disk.zones[0] if managed_disk.zones and len(managed_disk.zones) > 0 else ''
        )


def main():
    """Main module execution code path"""
    AzureRMManagedDiskInfo()


if __name__ == '__main__':
    main()
