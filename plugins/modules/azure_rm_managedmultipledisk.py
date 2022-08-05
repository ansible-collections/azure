#!/usr/bin/python
#
# Copyright (c) 2022 Aubin Bikouo (@abikouo)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_managedmultipledisk

version_added: "1.14.0"

short_description: Manage Multiple Azure Manage Disks

description:
    - Create, update and delete one or more Azure Managed Disk.

options:
    state:
        description:
            - Assert the state of the managed disks. Use C(present) to create or update managed disks and C(absent) to delete a managed disks.
        default: present
        choices:
            - absent
            - present
    managed_disks:
        description:
            - List of managed disks to create, update, or delete.
        type: list
        elements: dict
        suboptions:
            resource_group:
                description:
                    - Name of a resource group where the managed disk exists or will be created.
                required: true
            name:
                description:
                    - Name of the managed disk.
                required: true
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
    managed_by_extended:
        description:
            - List of name and resource group of the VMs that have the disk attached.
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

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Aubin Bikouo (@abikouo)
'''

EXAMPLES = '''
    - name: Create managed operating system disks from page blob
      azure_rm_manageddisk:
        managed_disks:
            - name: mymanageddisk1
              location: eastus2
              resource_group: myResourceGroup
              create_option: import
              source_uri: https://storageaccountname.blob.core.windows.net/containername/blob-name.vhd
              storage_account_id: /subscriptions/<uuid>/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/storageaccountname
              os_type: windows
              storage_account_type: Premium_LRS
            - name: mymanageddisk2
              location: eastus2
              resource_group: myResourceGroup
              create_option: import
              source_uri: https://storageaccountname.blob.core.windows.net/containername/blob-name.vhd
              storage_account_id: /subscriptions/<uuid>/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/storageaccountname
              os_type: windows
              storage_account_type: Premium_LRS
        managed_by_extended:
            - resource_group: myResourceGroupTest
              name: TestVM
'''

RETURN = '''
state:
    description:
        - Current state of the managed disks.
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
'''


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


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


class AzureRMManagedMultipleDisk(AzureRMModuleBase):
    """Configuration class for an Azure RM Managed Disk resource"""

    def __init__(self):
        
        managed_by_extended_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str')
        )
        managed_disks_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
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
        )

        self.module_arg_spec = dict(
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            managed_disks=dict(
                type='list',
                elements='dict',
                options=managed_disks_spec,
                aliases=['managed_by']
            ),
            managed_by_extended=dict(
                type='list',
                elements='dict',
                options=managed_by_extended_spec,
                aliases=['managed_by']
            ),
        )
        # TODO: add this check for suboptions
        # required_if = [
        #     ('create_option', 'import', ['source_uri', 'storage_account_id']),
        #     ('create_option', 'copy', ['source_uri']),
        #     ('create_option', 'empty', ['disk_size_gb'])
        # ]
        self.results = dict(
            changed=False,
            state=list())

        super(AzureRMManagedMultipleDisk, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            # required_if=required_if,
            supports_check_mode=True,
            # mutually_exclusive=mutually_exclusive,
            supports_tags=True)

    def generate_disk_parameters(self, location, tags, zone=None, 
                                storage_account_type=None, disk_size_gb=None, create_option=None,
                                source_uri=None, storage_account_id=None, os_type=None, max_shares=None, **kwargs):
        disk_params = {}
        creation_data = {}
        disk_params['location'] = location
        disk_params['tags'] = tags
        if zone:
            disk_params['zones'] = [zone]
        if storage_account_type:
            storage = self.compute_models.DiskSku(name=storage_account_type)
            disk_params['sku'] = storage
        disk_params['disk_size_gb'] = disk_size_gb
        creation_data['create_option'] = self.compute_models.DiskCreateOption.empty
        if create_option == 'import':
            creation_data['create_option'] = self.compute_models.DiskCreateOption.import_enum
            creation_data['source_uri'] = source_uri
            creation_data['source_account_id'] = storage_account_id
        elif create_option == 'copy':
            creation_data['create_option'] = self.compute_models.DiskCreateOption.copy
            creation_data['source_resource_id'] = source_uri
        if os_type:
            disk_params['os_type'] = self.compute_models.OperatingSystemTypes(os_type.capitalize())
        else:
            disk_params['os_type'] = None
        if max_shares:
            disk_params['max_shares'] = max_shares
        disk_params['creation_data'] = creation_data
        return disk_params


    def get_disk_instance(self, managed_disk):

        resource_group = self.get_resource_group(managed_disk.get("resource_group"))
        managed_disk["location"] = managed_disk.get("location") or resource_group.location
        disk_instance = self.get_managed_disk(resource_group=managed_disk.get("resource_group"), name=managed_disk.get("name"))
        if disk_instance is not None:
            for key in ("create_option", 'source_uri', 'disk_size_gb', 'os_type', 'zone'):
                if managed_disk.get(key) is None:
                    managed_disk[key] = disk_instance.get(key)
        
        parameter = self.generate_disk_parameters(tags=self.tags, **managed_disk)

        return parameter, disk_instance

    def exec_module(self, **kwargs):
        """Main module execution method"""
        self.tags = kwargs.get("tags")

        result = list()
        changed = False
        state = kwargs.get("state")

        for disk in kwargs.get("managed_disks"):
            parameter, disk_instance = self.get_disk_instance(disk)

            # Create disk
            if state == 'present':
                if disk_instance is None or self.is_different(zone=disk.get("zone"), max_shares=disk.get("max_shares"), found_disk=disk_instance, new_disk=parameter):
                    changed = True
                    if not self.check_mode:
                        tmp = self.create_or_update_managed_disk(resource_group=disk.get("resource_group"), name=disk.get("name"), disk_params=parameter)
                        result.append((disk, tmp))
                    else:
                        result = True
                elif not self.check_mode:
                    result.append((disk, disk_instance))
                else:
                    result = True

            elif state == 'absent' and disk_instance:
                changed = True
                if not self.check_mode:
                    self.delete_managed_disk(resource_group=disk.get("resource_group"), name=disk.get("name"), disk_instance=disk_instance)
                result = True

        # Mount the disk to multiple VM
        if state == "present":
            if not self.check_mode:
                for vm_item in kwargs.get("managed_by_extended"):
                    try:
                        vm_name_id = self.compute_client.virtual_machines.get(vm_item['resource_group'], vm_item['name'])
                    except Exception as exc:
                        self.fail("Fail to get virtual machine {0}/{1}: {2}".format(vm_item['resource_group'], vm_item['name'], str(exc)))

                    def _is_disk_not_attached(vm_id, item):
                        managed_by = item['managed_by_extended']
                        return managed_by is None or vm_id not in managed_by
                    # self.module.exit_json(test=[i for p, i in result])
                    disks = [(p, i) for p, i in result if _is_disk_not_attached(vm_name_id.id, i)]
                    if len(disks) > 0:
                        changed = True
                        self.attach(vm_item['resource_group'], vm_item['name'], disks)

                result = [self.get_managed_disk(resource_group=params.get("resource_group"), name=params.get("name")) for params, disk_instance in result]

        return dict(changed=changed, state=result)

    def attach(self, resource_group, vm_name, disks):
        vm = self._get_vm(resource_group, vm_name)

        # attach all disks to the virtual machine
        for managed_disk, result in disks:
            lun = managed_disk.get("lun")
            if lun is None:
                luns = ([d.lun for d in vm.storage_profile.data_disks] if vm.storage_profile.data_disks else [])
                lun = 0
                while True:
                    if lun not in luns:
                        break
                    lun = lun + 1
                for item in vm.storage_profile.data_disks:
                    if item.name == managed_disk.get("name"):
                        lun = item.lun

            # prepare the data disk
            params = self.compute_models.ManagedDiskParameters(id=result.get('id'), storage_account_type=result.get('storage_account_type'))
            attach_caching = managed_disk.get("attach_caching")
            caching_options = self.compute_models.CachingTypes[attach_caching] if attach_caching and attach_caching != '' else None

            # pylint: disable=missing-kwoa
            data_disk = self.compute_models.DataDisk(lun=lun,
                                                    create_option=self.compute_models.DiskCreateOptionTypes.attach,
                                                    managed_disk=params,
                                                    caching=caching_options)
            vm.storage_profile.data_disks.append(data_disk)
        return self._update_vm(resource_group, vm_name, vm)

    def detach(self, resource_group, vm_name, disk_name):
        vm = self._get_vm(resource_group, vm_name)
        leftovers = [d for d in vm.storage_profile.data_disks if d.name.lower() != disk_name.lower()]
        if len(vm.storage_profile.data_disks) == len(leftovers):
            self.fail("No disk with the name '{0}' was found".format(disk_name))
        vm.storage_profile.data_disks = leftovers
        self._update_vm(resource_group, vm_name, vm)

    def _update_vm(self, resource_group, name, params):
        try:
            poller = self.compute_client.virtual_machines.begin_create_or_update(resource_group, name, params)
            self.get_poller_result(poller)
        except Exception as exc:
            return exc

    def _get_vm(self, resource_group, name):
        try:
            return self.compute_client.virtual_machines.get(resource_group, name, expand='instanceview')
        except Exception as exc:
            self.fail("Error getting virtual machine {0} - {1}".format(name, str(exc)))

    def create_or_update_managed_disk(self, resource_group, name, disk_params):
        try:
            poller = self.compute_client.disks.begin_create_or_update(resource_group, name, disk_params)
            aux = self.get_poller_result(poller)
            return managed_disk_to_dict(aux)
        except Exception as e:
            self.fail("Error creating the managed disk {0}/{1}: {2}".format(resource_group, name, str(e)))

    # This method accounts for the difference in structure between the
    # Azure retrieved disk and the parameters for the new disk to be created.
    def is_different(self, zone, max_shares, found_disk, new_disk):
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
        if zone is not None:
            if not found_disk['zone'] == zone:
                resp = True
        if max_shares is not None:
            if not found_disk['max_shares'] == max_shares:
                resp = True
        return resp

    def delete_managed_disk(self, resource_group, name, disk_instance):
        try:
            def _parse_vm_id(d):
                arr = d.split("/")
                rg, name = None, None
                for i, v in enumerate(arr):
                    if v == "resourceGroups":
                        rg = arr[i+1]
                    elif v == "virtualMachines":
                        name = arr[i+1]
                    print(i)
                return rg, name

            if disk_instance.get("managed_by") is not None:
                vm_resource_group, vm_name = _parse_vm_id(disk_instance.get("managed_by"))
                self.detach(vm_resource_group, vm_name, name)
                
            poller = self.compute_client.disks.begin_delete(resource_group, name)
            return self.get_poller_result(poller)
        except Exception as e:
            self.fail("Error deleting the managed disk {0}/{1}: {2}".format(resource_group, name, str(e)))

    def get_managed_disk(self, resource_group, name):
        try:
            resp = self.compute_client.disks.get(resource_group, name)
            return managed_disk_to_dict(resp)
        except ResourceNotFoundError:
            self.log("Did not find managed disk {0}/{1}".format(resource_group, name))


def main():
    """Main execution"""
    AzureRMManagedMultipleDisk()


if __name__ == '__main__':
    main()
