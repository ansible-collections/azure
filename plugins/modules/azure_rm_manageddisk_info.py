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
    - This module was called M(azure.azcollection.azure_rm_managed_disk_facts) before Ansible 2.8. The usage did not change.

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
        elements: str
    managed_by:
        description:
            - Limit results to disks managed by the given VM fqid.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

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
            sample: "/subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/testVM"
        max_shares:
            description:
                - The maximum number of VMs that can attach to the disk at the same time.
                - Value greater than one indicates a disk that can be mounted on multiple VMs at the same time.
            type: int
            sample: 3
        managed_by_extended:
            description:
                - List ID of an existing virtual machine with which the disk is or will be associated.
            type: list
            sample: ["/subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/testVM"]
        tags:
            description:
                - Tags to assign to the managed disk.
            type: dict
            sample: { "tag": "value" }
        tier:
            description:
                - Performance tier assigned to the managed disk.
                - See U(https://learn.microsoft.com/en-us/azure/virtual-machines/disks-change-performance) for more information about disk performance tiers.
            type: str
            sample: "P30"
        time_created:
            description:
                - The time the disk was created.
            type: str
            sample: "2018-01-01T11:08:15.338648900:00"
        disk_iops_read_write:
            description:
                - The number of IOPS allowed for this disk.
                - Only settable for I(storage_account_type=UltraSSD_LRS) disks.
                - One operation can transfer between 4k and 256k bytes.
            type: int
            returned: always
            sample: 200
        disk_m_bps_read_write:
            description:
                - The bandwidth allowed for this disk.
                - Only settable for I(storage_account_type=UltraSSD_LRS) disks.
                - One operation can transfer between 4k and 256k bytes.
            type: int
            returned: always
            sample: 30
        disk_iops_read_only:
            description:
                - The total throughput (MBps) that will be allowed across all VMs mounting the shared disk as ReadOnly.
                - One operation can transfer between 4k and 256k bytes.
            type: int
            returned: always
            sample: 200
        disk_m_bps_read_only:
            description:
                - The total throughput (MBps) that will be allowed across all VMs mounting the shared disk as ReadOnly.
                - MBps means millions of bytes per second - MB here uses the ISO notation, of powers of 10.
            type: int
            returned: always
            sample: 30
        network_access_policy:
            description:
                - Policy for accessing the disk via network.
            type: str
            returned: always
            sample: AllowAll
        public_network_access:
            description:
                - Policy for controlling export on the disk.
            type: str
            returned: always
            sample: Enabled
        disk_access_id:
            description:
                - ARM ID of the DiskAccess resource for using private endpoints on disks.
            type: str
            returned: always
            sample: '/subscriptions/*********/resourceGroups/myRG/providers/Microsoft.Compute/diskAccesses/diskacc'
        performance_plus:
            description:
                - The flag of the performance target of the disk deployed.
            type: bool
            returned: always
            sample: False
        upload_size_bytes:
            description:
                - This is the size of the contents of the upload including the VHD footer.
            type: int
            returned: always
            sample: None
        gallery_image_reference:
            description:
                - The Gallery Image info.
            type: dict
            returned: always
            sample: None
        image_reference:
            description:
                - Disk source information for PIR or user images or Gallery Image.
            type: dict
            returned: always
            sample: None
        logical_sector_size:
            description:
                - Logical sector size in bytes for Ultra disks.
            type: int
            returned: always
            sample: None
        last_ownership_update_time:
            description:
                - The UTC time when the ownership state of the disk was last changed.
                - The time the disk was last attached or detached from a VM or the time when the VM to which the disk was attached was deallocated or started.
            returned: always
            type: str
            sample: "2025-06-27T01:55:10.239311+00:00"
        source_resource_id:
            description:
                - This is the ARM id of the source snapshot or disk.
            type: str
            returned: always
            sample: None
        security_profile:
            description:
                - The security related information for the resource.
            type: complex
            contains:
                security_type:
                    description:
                        - Specifies the SecurityType of the VM.
                    type: str
                    returned: when-used
                    sample: TrustedLaunch
                secure_vm_disk_encryption_set_id:
                    description:
                        -  ResourceId of the disk encryption set associated to Confidential VM supported disk encrypted with customer managed key.
                    type: str
                    returned: when-used
                    sample: None

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # handled in azure_rm_common
    pass


class AzureRMManagedDiskInfo(AzureRMModuleBase):
    """Utility class to get managed disk facts"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            tags=dict(type='list', elements='str'),
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
                                                     supports_tags=False)

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
            results = [self.disk_client.disks.get(self.resource_group,
                                                  self.name)]
            if self.managed_by:
                results = [disk for disk in results if disk.managed_by == self.managed_by]
            if self.tags:
                results = [disk for disk in results if self.has_tags(disk.tags, self.tags)]
            results = [self.managed_disk_to_dict(disk) for disk in results]
        except ResourceNotFoundError:
            self.log('Could not find disk {0} in resource group {1}'.format(self.name, self.resource_group))

        return results

    def list_disks(self):
        """Get all managed disks"""
        results = []

        try:
            results = self.disk_client.disks.list()
            if self.managed_by:
                results = [disk for disk in results if disk.managed_by == self.managed_by]
            if self.tags:
                results = [disk for disk in results if self.has_tags(disk.tags, self.tags)]
            results = [self.managed_disk_to_dict(disk) for disk in results]
        except ResourceNotFoundError as exc:
            self.fail('Failed to list all items - {0}'.format(str(exc)))

        return results

    def list_disks_by_resource_group(self):
        """Get managed disks in a resource group"""
        results = []

        try:
            results = self.disk_client.disks.list_by_resource_group(resource_group_name=self.resource_group)
            if self.managed_by:
                results = [disk for disk in results if disk.managed_by == self.managed_by]
            if self.tags:
                results = [disk for disk in results if self.has_tags(disk.tags, self.tags)]
            results = [self.managed_disk_to_dict(disk) for disk in results]
        except ResourceNotFoundError as exc:
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
            max_shares=managed_disk.max_shares,
            managed_by_extended=managed_disk.managed_by_extended,
            zone=managed_disk.zones[0] if managed_disk.zones and len(managed_disk.zones) > 0 else '',
            time_created=managed_disk.time_created.isoformat() if managed_disk.time_created else None,
            disk_iops_read_write=managed_disk.disk_iops_read_write,
            disk_m_bps_read_write=managed_disk.disk_m_bps_read_write,
            disk_iops_read_only=managed_disk.disk_iops_read_only,
            disk_m_bps_read_only=managed_disk.disk_m_bps_read_only,
            tier=managed_disk.tier,
            network_access_policy=managed_disk.network_access_policy,
            public_network_access=managed_disk.public_network_access,
            disk_access_id=managed_disk.disk_access_id,
            source_resource_id=create_data.source_resource_id,
            storage_account_id=create_data.storage_account_id,
            upload_size_bytes=create_data.upload_size_bytes,
            logical_sector_size=create_data.logical_sector_size,
            performance_plus=create_data.performance_plus,
            last_ownership_update_time=managed_disk.last_ownership_update_time,
            gallery_image_reference=dict(
                id=create_data.gallery_image_reference.id,
                shared_gallery_image_id=create_data.gallery_image_reference.shared_gallery_image_id,
                community_gallery_image_id=create_data.gallery_image_reference.community_gallery_image_id
            ) if create_data.gallery_image_reference is not None else None,
            image_reference=dict(
                id=create_data.image_reference.id,
                shared_gallery_image_id=create_data.image_reference.shared_gallery_image_id,
                community_gallery_image_id=create_data.image_reference.community_gallery_image_id
            ) if create_data.image_reference is not None else None,
            security_profile=dict(
                security_type=managed_disk.security_profile.security_type,
                secure_vm_disk_encryption_set_id=managed_disk.security_profile.secure_vm_disk_encryption_set_id
            ) if managed_disk.security_profile is not None else None
        )


def main():
    """Main module execution code path"""
    AzureRMManagedDiskInfo()


if __name__ == '__main__':
    main()
