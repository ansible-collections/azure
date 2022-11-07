#!/usr/bin/python
#
# Copyright (c) 2017 Bruno Medina Bolanos Cacho <bruno.medina@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_manageddisk

version_added: "0.1.2"

short_description: Manage Azure Manage Disks

description:
    - Create, update and delete an Azure Managed Disk.

notes:
    - This module was called M(azure.azcollection.azure_rm_managed_disk) before Ansible 2.8. The usage did not change.

options:
    resource_group:
        description:
            - Name of a resource group where the managed disk exists or will be created.
        required: true
    name:
        description:
            - Name of the managed disk.
        required: true
    state:
        description:
            - Assert the state of the managed disk. Use C(present) to create or update a managed disk and C(absent) to delete a managed disk.
        default: present
        choices:
            - absent
            - present
    location:
        description:
            - Valid Azure location. Defaults to location of the resource group.
    storage_account_type:
        description:
            - Type of storage for the managed disk.
            - If not specified, the disk is created as C(Standard_LRS).
            - C(Standard_LRS) is for Standard HDD.
            - C(StandardSSD_LRS) (added in 2.8) is for Standard SSD.
            - C(StandardSSD_ZRS) is for Standard SSD Zone-redundant.
            - C(Premium_LRS) is for Premium SSD.
            - C(Premium_ZRS) is for Premium SSD Zone-redundant.
            - C(UltraSSD_LRS) (added in 2.8) is for Ultra SSD, which is only available on select instance types.
            - See U(https://docs.microsoft.com/en-us/azure/virtual-machines/windows/disks-types) for more information about disk types.
        choices:
            - Standard_LRS
            - StandardSSD_LRS
            - StandardSSD_ZRS
            - Premium_LRS
            - Premium_ZRS
            - UltraSSD_LRS
    create_option:
        description:
            - C(import) from a VHD file in I(source_uri) and C(copy) from previous managed disk I(source_uri).
        choices:
            - empty
            - import
            - copy
    storage_account_id:
        description:
            - The full path to the storage account the image is to be imported from.
            - Required when I(create_option=import).
        type: str
    source_uri:
        description:
            - URI to a valid VHD file to be used or the resource ID of the managed disk to copy.
        aliases:
            - source_resource_uri
    os_type:
        description:
            - Type of Operating System.
            - Used when I(create_option=copy) or I(create_option=import) and the source is an OS disk.
            - If omitted during creation, no value is set.
            - If omitted during an update, no change is made.
            - Once set, this value cannot be cleared.
        choices:
            - linux
            - windows
    disk_size_gb:
        description:
            - Size in GB of the managed disk to be created.
            - If I(create_option=copy) then the value must be greater than or equal to the source's size.
    managed_by:
        description:
            - Name of an existing virtual machine with which the disk is or will be associated, this VM should be in the same resource group.
            - To detach a disk from a vm, explicitly set to ''.
            - If this option is unset, the value will not be changed.
    managed_by_extended:
        description:
            - List of name and resource group of the VMs that have the disk attached.
            - I(max_shares) should be set to a value greater than one for disks to allow attaching them to multiple VMs.
        type: list
        elements: dict
        suboptions:
            resource_group:
                description:
                    - The resource group of the attache VM.
                type: str
            name:
                description:
                    - The name of the attache VM.
                type: str
    max_shares:
        description:
            - The maximum number of VMs that can attach to the disk at the same time.
            - Value greater than one indicates a disk that can be mounted on multiple VMs at the same time.
        type: int
    attach_caching:
        description:
            - Disk caching policy controlled by VM. Will be used when attached to the VM defined by C(managed_by).
            - If this option is different from the current caching policy, the managed disk will be deattached and attached with current caching option again.
        choices:
            - ''
            - read_only
            - read_write
    zone:
        description:
            - The Azure managed disk's zone.
            - Allowed values are C(1), C(2), C(3) and C(' ').
        choices:
            - 1
            - 2
            - 3
            - ''
    lun:
        description:
            - The logical unit number for data disk.
            - This value is used to identify data disks within the VM and therefore must be unique for each data disk attached to a VM.
        type: int

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Bruno Medina (@brusMX)
'''

EXAMPLES = '''
    - name: Create managed disk
      azure_rm_manageddisk:
        name: mymanageddisk
        location: eastus
        resource_group: myResourceGroup
        disk_size_gb: 4

    - name: Create managed operating system disk from page blob
      azure_rm_manageddisk:
        name: mymanageddisk
        location: eastus2
        resource_group: myResourceGroup
        create_option: import
        source_uri: https://storageaccountname.blob.core.windows.net/containername/blob-name.vhd
        storage_account_id: /subscriptions/<uuid>/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/storageaccountname
        os_type: windows
        storage_account_type: Premium_LRS

    - name: Mount the managed disk to VM
      azure_rm_manageddisk:
        name: mymanageddisk
        location: eastus
        resource_group: myResourceGroup
        disk_size_gb: 4
        managed_by: testvm001
        attach_caching: read_only

    - name: Mount the managed disk to multiple VMs
      azure_rm_manageddisk:
        resource_group: myResourceGroup
        name: freddisk04
        max_shares: 4
        disk_size_gb: 1024
        storage_account_type: Premium_LRS
        managed_by_extended:
          - resource_group: myResourceGroup01
            name: testVM01
          - resource_group: myResourceGroup02
            name: testVM02
        zone: 1

    - name: Unmount the managed disk to VM
      azure_rm_manageddisk:
        name: mymanageddisk
        location: eastus
        resource_group: myResourceGroup
        managed_by: ''
        disk_size_gb: 4

    - name: Delete managed disk
      azure_rm_manageddisk:
        name: mymanageddisk
        location: eastus
        resource_group: myResourceGroup
        state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the managed disk.
    returned: always
    type: complex
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
        storage_account_id:
            description:
                - The full path to the storage account the image is to be imported from
            type: str
            sample: /subscriptions/<uuid>/resourceGroups/<resource group name>/providers/Microsoft.Storage/storageAccounts/<storage account name>
        source_uri:
            description:
                - URI to a valid VHD file to be used or the resource ID of the managed disk to copy.
            type: str
        os_type:
            description:
                - Type of Operating System.
            type: str
            sample: linux
        disk_size_gb:
            description:
                - Size in GB of the managed disk to be created.
            type: str
        managed_by:
            description:
                - Name of an existing virtual machine with which the disk is or will be associated, this VM should be in the same resource group.
            type: str
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
changed:
    description:
        - Whether or not the resource has changed.
    returned: always
    type: bool
'''

import re


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
try:
    from concurrent.futures import ThreadPoolExecutor
    import multiprocessing
    from msrestazure.tools import parse_resource_id
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


managed_by_extended_spec = dict(
    resource_group=dict(type='str'),
    name=dict(type='str')
)


# duplicated in azure_rm_manageddisk_facts
def managed_disk_to_dict(managed_disk):
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
        zone=managed_disk.zones[0] if managed_disk.zones and len(managed_disk.zones) > 0 else ''
    )


class AzureRMManagedDisk(AzureRMModuleBase):
    """Configuration class for an Azure RM Managed Disk resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            location=dict(
                type='str'
            ),
            storage_account_type=dict(
                type='str',
                choices=['Standard_LRS', 'StandardSSD_LRS', 'StandardSSD_ZRS', 'Premium_LRS', 'Premium_ZRS', 'UltraSSD_LRS']
            ),
            create_option=dict(
                type='str',
                choices=['empty', 'import', 'copy']
            ),
            storage_account_id=dict(
                type='str'
            ),
            source_uri=dict(
                type='str',
                aliases=['source_resource_uri']
            ),
            os_type=dict(
                type='str',
                choices=['linux', 'windows']
            ),
            disk_size_gb=dict(
                type='int'
            ),
            managed_by=dict(
                type='str'
            ),
            zone=dict(
                type='str',
                choices=['', '1', '2', '3']
            ),
            attach_caching=dict(
                type='str',
                choices=['', 'read_only', 'read_write']
            ),
            lun=dict(
                type='int'
            ),
            max_shares=dict(
                type='int'
            ),
            managed_by_extended=dict(
                type='list',
                elements='dict',
                options=managed_by_extended_spec
            )
        )
        required_if = [
            ('create_option', 'import', ['source_uri', 'storage_account_id']),
            ('create_option', 'copy', ['source_uri']),
            ('create_option', 'empty', ['disk_size_gb'])
        ]
        self.results = dict(
            changed=False,
            state=dict())

        self.resource_group = None
        self.name = None
        self.location = None
        self.storage_account_type = None
        self.create_option = None
        self.storage_account_id = None
        self.source_uri = None
        self.os_type = None
        self.disk_size_gb = None
        self.tags = None
        self.zone = None
        self.managed_by = None
        self.attach_caching = None
        self.lun = None
        self.max_shares = None
        self.managed_by_extended = None

        mutually_exclusive = [['managed_by_extended', 'managed_by']]

        super(AzureRMManagedDisk, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            required_if=required_if,
            supports_check_mode=True,
            mutually_exclusive=mutually_exclusive,
            supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        result = None
        changed = False

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        disk_instance = self.get_managed_disk()
        if disk_instance is not None:
            if self.create_option is None:
                self.create_option = disk_instance.get('create_option')
            if self.source_uri is None:
                self.source_uri = disk_instance.get('source_uri')
            if self.disk_size_gb is None:
                self.disk_size_gb = disk_instance.get('disk_size_gb')
            if self.os_type is None:
                self.os_type = disk_instance.get('os_type')
            if self.zone is None:
                self.zone = disk_instance.get('zone')
        result = disk_instance

        # need create or update
        if self.state == 'present':
            parameter = self.generate_managed_disk_property()
            if not disk_instance or self.is_different(disk_instance, parameter):
                changed = True
                if not self.check_mode:
                    result = self.create_or_update_managed_disk(parameter)
                else:
                    result = True

        # Mount the disk to multiple VM
        if self.managed_by_extended:
            if not self.check_mode:
                cpu_count = multiprocessing.cpu_count()
                executor = ThreadPoolExecutor(max_workers=cpu_count)
                task_result = []
                for vm_item in self.managed_by_extended:
                    vm_name_id = self.compute_client.virtual_machines.get(vm_item['resource_group'], vm_item['name'])
                    if result['managed_by_extended'] is None or vm_name_id.id not in result['managed_by_extended']:
                        changed = True
                        feature = executor.submit(self.attach, vm_item['resource_group'], vm_item['name'], result)
                        task_result.append({'task': feature, 'vm_name': vm_item['name'], 'resource_group': vm_item['resource_group']})
                fail_attach_VM = []
                for task_item in task_result:
                    if task_item['task'].result() is not None:
                        task_item['error_msg'] = task_item['task'].result()
                        task_item.pop('task')
                        fail_attach_VM.append(task_item)
                if len(fail_attach_VM) > 0:
                    self.fail("Disk mount failure, VM and Error message information: {0}".format(fail_attach_VM))

                result = self.get_managed_disk()

        # unmount from the old virtual machine and mount to the new virtual machine
        if self.managed_by or self.managed_by == '':
            vm_name = parse_resource_id(disk_instance.get('managed_by', '')).get('name') if disk_instance else None
            vm_name = vm_name or ''
            if self.managed_by != vm_name or self.is_attach_caching_option_different(vm_name, result):
                changed = True
                if not self.check_mode:
                    if vm_name:
                        self.detach(self.resource_group, vm_name, result)
                    if self.managed_by:
                        self.attach(self.resource_group, self.managed_by, result)
                    result = self.get_managed_disk()

        if self.state == 'absent' and disk_instance:
            changed = True
            if not self.check_mode:
                self.delete_managed_disk()
            result = True

        self.results['changed'] = changed
        self.results['state'] = result
        return self.results

    def attach(self, resource_group, vm_name, disk):
        vm = self._get_vm(resource_group, vm_name)
        # find the lun
        if self.lun:
            lun = self.lun
        else:
            luns = ([d.lun for d in vm.storage_profile.data_disks]
                    if vm.storage_profile.data_disks else [])
            lun = 0
            while True:
                if lun not in luns:
                    break
                lun = lun + 1
            for item in vm.storage_profile.data_disks:
                if item.name == self.name:
                    lun = item.lun

        # prepare the data disk
        params = self.compute_models.ManagedDiskParameters(id=disk.get('id'), storage_account_type=disk.get('storage_account_type'))
        caching_options = self.compute_models.CachingTypes[self.attach_caching] if self.attach_caching and self.attach_caching != '' else None
        # pylint: disable=missing-kwoa
        data_disk = self.compute_models.DataDisk(lun=lun,
                                                 create_option=self.compute_models.DiskCreateOptionTypes.attach,
                                                 managed_disk=params,
                                                 caching=caching_options)
        vm.storage_profile.data_disks.append(data_disk)
        return self._update_vm(resource_group, vm_name, vm)

    def detach(self, resource_group, vm_name, disk):
        vm = self._get_vm(resource_group, vm_name)
        leftovers = [d for d in vm.storage_profile.data_disks if d.name.lower() != disk.get('name').lower()]
        if len(vm.storage_profile.data_disks) == len(leftovers):
            self.fail("No disk with the name '{0}' was found".format(disk.get('name')))
        vm.storage_profile.data_disks = leftovers
        self._update_vm(resource_group, vm_name, vm)

    def _update_vm(self, resource_group, name, params):
        try:
            poller = self.compute_client.virtual_machines.begin_create_or_update(resource_group, name, params)
            self.get_poller_result(poller)
        except Exception as exc:
            if self.managed_by_extended:
                return exc
            else:
                self.fail("Error updating virtual machine {0} - {1}".format(name, str(exc)))

    def _get_vm(self, resource_group, name):
        try:
            return self.compute_client.virtual_machines.get(resource_group, name, expand='instanceview')
        except Exception as exc:
            self.fail("Error getting virtual machine {0} - {1}".format(name, str(exc)))

    def generate_managed_disk_property(self):
        # TODO: Add support for EncryptionSettings, DiskIOPSReadWrite, DiskMBpsReadWrite
        disk_params = {}
        creation_data = {}
        disk_params['location'] = self.location
        disk_params['tags'] = self.tags
        if self.zone:
            disk_params['zones'] = [self.zone]
        if self.storage_account_type:
            storage_account_type = self.compute_models.DiskSku(name=self.storage_account_type)
            disk_params['sku'] = storage_account_type
        disk_params['disk_size_gb'] = self.disk_size_gb
        creation_data['create_option'] = self.compute_models.DiskCreateOption.empty
        if self.create_option == 'import':
            creation_data['create_option'] = self.compute_models.DiskCreateOption.import_enum
            creation_data['source_uri'] = self.source_uri
            creation_data['source_account_id'] = self.storage_account_id
        elif self.create_option == 'copy':
            creation_data['create_option'] = self.compute_models.DiskCreateOption.copy
            creation_data['source_resource_id'] = self.source_uri
        if self.os_type:
            disk_params['os_type'] = self.compute_models.OperatingSystemTypes(self.os_type.capitalize())
        else:
            disk_params['os_type'] = None
        if self.max_shares:
            disk_params['max_shares'] = self.max_shares
        disk_params['creation_data'] = creation_data
        return disk_params

    def create_or_update_managed_disk(self, parameter):
        try:
            poller = self.compute_client.disks.begin_create_or_update(self.resource_group,
                                                                      self.name,
                                                                      parameter)
            aux = self.get_poller_result(poller)
            return managed_disk_to_dict(aux)
        except Exception as e:
            self.fail("Error creating the managed disk: {0}".format(str(e)))

    # This method accounts for the difference in structure between the
    # Azure retrieved disk and the parameters for the new disk to be created.
    def is_different(self, found_disk, new_disk):
        resp = False
        if new_disk.get('disk_size_gb'):
            if not found_disk['disk_size_gb'] == new_disk['disk_size_gb']:
                resp = True
        if new_disk.get('os_type'):
            if found_disk['os_type'] is None or not self.compute_models.OperatingSystemTypes(found_disk['os_type'].capitalize()) == new_disk['os_type']:
                resp = True
        if new_disk.get('sku'):
            if not found_disk['storage_account_type'] == new_disk['sku'].name:
                resp = True
        # Check how to implement tags
        if new_disk.get('tags') is not None:
            if not found_disk['tags'] == new_disk['tags']:
                resp = True
        if self.zone is not None:
            if not found_disk['zone'] == self.zone:
                resp = True
        if self.max_shares is not None:
            if not found_disk['max_shares'] == self.max_shares:
                resp = True
        return resp

    def delete_managed_disk(self):
        try:
            poller = self.compute_client.disks.begin_delete(self.resource_group,
                                                            self.name)
            return self.get_poller_result(poller)
        except Exception as e:
            self.fail("Error deleting the managed disk: {0}".format(str(e)))

    def get_managed_disk(self):
        try:
            resp = self.compute_client.disks.get(
                self.resource_group,
                self.name)
            return managed_disk_to_dict(resp)
        except ResourceNotFoundError:
            self.log('Did not find managed disk')

    def is_attach_caching_option_different(self, vm_name, disk):
        resp = False
        if vm_name:
            vm = self._get_vm(self.resource_group, vm_name)
            correspondence = next((d for d in vm.storage_profile.data_disks if d.name.lower() == disk.get('name').lower()), None)
            caching_options = self.compute_models.CachingTypes[self.attach_caching] if self.attach_caching and self.attach_caching != '' else None
            if correspondence and correspondence.caching != caching_options:
                resp = True
                if correspondence.caching == 'none' and (self.attach_caching == '' or self.attach_caching is None):
                    resp = False
        return resp


def main():
    """Main execution"""
    AzureRMManagedDisk()


if __name__ == '__main__':
    main()
