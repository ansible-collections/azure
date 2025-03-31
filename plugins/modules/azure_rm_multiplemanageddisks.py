#!/usr/bin/python
#
# Copyright (c) 2022 Aubin Bikouo (@abikouo)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_multiplemanageddisks

version_added: "1.14.0"

short_description: Manage Multiple Azure Manage Disks

description:
    - Create, update and delete one or more Azure Managed Disk.
    - This module can be used also to attach/detach disks to/from one or more virtual machines.

options:
    state:
        description:
            - Assert the state of the managed disks.
            - Use C(present) to create or update managed disks and/or attach/detach managed disks to a list of
              VMs depending on the value specified in I(managed_by_extended).
            - Use C(absent) to detach/delete managed disks depending on the value specified in I(managed_by_extended).
        default: present
        type: str
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
                type: str
            name:
                description:
                    - Name of the managed disk.
                required: true
                type: str
            location:
                description:
                    - Valid Azure location. Defaults to location of the resource group.
                type: str
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
                type: str
            create_option:
                description:
                    - C(import) from a VHD file in I(source_uri) and C(copy) from previous managed disk I(source_uri).
                type: str
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
                    - Required when I(create_option=import) or I(create_option=copy).
                aliases:
                    - source_resource_uri
                type: str
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
                    - Linux
                    - Windows
                type: str
            disk_size_gb:
                description:
                    - Size in GB of the managed disk to be created.
                    - Required when I(create_option=empty).
                    - If I(create_option=copy) then the value must be greater than or equal to the source's size.
                type: int
            max_shares:
                description:
                    - The maximum number of VMs that can attach to the disk at the same time.
                    - Value greater than one indicates a disk that can be mounted on multiple VMs at the same time.
                type: int
            attach_caching:
                description:
                    - Disk caching policy controlled by VM. Will be used when attached to the VM defined by C(managed_by).
                    - If this option is different from the current caching policy, the managed disk will be deattached
                      and attached with current caching option again.
                choices:
                    - ''
                    - read_only
                    - read_write
                type: str
            zone:
                description:
                    - The Azure managed disk's zone.
                    - Allowed values are C(1), C(2), C(3) and C('').
                choices:
                    - '1'
                    - '2'
                    - '3'
                    - ''
                type: str
            lun:
                description:
                    - The logical unit number for data disk.
                    - This value is used to identify data disks within the VM and therefore must be unique for each data disk attached to a VM.
                type: int
    managed_by_extended:
        description:
            - List of name and resource group of the VMs to managed disks.
            - When I(state=present), the disks will be attached to the list of VMs specified.
            - When I(state=present), use I([]) to detach disks from all the VMs.
            - When I(state=absent) and this parameter is defined, the disks will be detached from the list of VMs.
            - When I(state=absent) and this parameter is not defined, the disks will be deleted.
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
- name: Create managed operating system disks from page blob and attach them to a list of VMs
  azure_rm_multiplemanageddisks:
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

- name: Detach disks from the VMs specified in the list
  azure_rm_multiplemanageddisks:
    state: absent
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
        name: TestVM1
      - resource_group: myResourceGroupTest
        name: TestVM2

- name: Detach managed disks from all VMs without deletion
  azure_rm_multiplemanageddisks:
    state: present
    managed_disks:
      - name: mymanageddisk1
        location: eastus2
        resource_group: myResourceGroup
      - name: mymanageddisk2
        location: eastus2
        resource_group: myResourceGroup
    managed_by_extended: []

- name: Detach managed disks from all VMs and delete them
  azure_rm_multiplemanageddisks:
    state: absent
    managed_disks:
      - name: mymanageddisk1
        location: eastus2
        resource_group: myResourceGroup
      - name: mymanageddisk2
        location: eastus2
        resource_group: myResourceGroup
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
    from azure.core.exceptions import ResourceNotFoundError, AzureError
    from azure.mgmt.core.tools import parse_resource_id
    import time
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


class AzureRMMultipleManagedDisk(AzureRMModuleBase):
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
                choices=['linux', 'windows', 'Linux', 'Windows']
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
            ),
            managed_by_extended=dict(
                type='list',
                elements='dict',
                options=managed_by_extended_spec,
            ),
        )
        self.results = dict(
            changed=False,
            state=list())

        super(AzureRMMultipleManagedDisk, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_tags=True)

    def validate_disks_parameter(self):
        errors = []
        create_option_reqs = [
            ('import', ['source_uri', 'storage_account_id']),
            ('copy', ['source_uri']),
            ('empty', ['disk_size_gb'])
        ]
        for disk in self.managed_disks:
            create_option = disk.get("create_option")
            for req in create_option_reqs:
                if create_option == req[0] and any((disk.get(opt) is None for opt in req[1])):
                    errors.append("managed disk {0}/{1} has create_option set to {2} but not all required parameters ({3}) are set.".format(
                                  disk.get("resource_group"), disk.get("name"), req[0], ",".join(req[1])))
        if errors:
            self.fail(msg="Some required options are missing from managed disks configuration.", errors=errors)

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
            storage = self.multi_disk_models.DiskSku(name=storage_account_type)
            disk_params['sku'] = storage
        disk_params['disk_size_gb'] = disk_size_gb
        creation_data['create_option'] = self.multi_disk_models.DiskCreateOption.empty
        if create_option == 'import':
            creation_data['create_option'] = self.multi_disk_models.DiskCreateOption.import_enum
            creation_data['source_uri'] = source_uri
            creation_data['storage_account_id'] = storage_account_id
        elif create_option == 'copy':
            creation_data['create_option'] = self.multi_disk_models.DiskCreateOption.copy
            creation_data['source_resource_id'] = source_uri
        if os_type:
            disk_params['os_type'] = self.multi_disk_models.OperatingSystemTypes(os_type.capitalize())
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

        state = kwargs.get("state")
        self.managed_disks = kwargs.get("managed_disks")
        self.managed_by_extended = kwargs.get("managed_by_extended")

        self.validate_disks_parameter()

        managed_vm_id = []
        if self.managed_by_extended:
            managed_vm_id = [self._get_vm(vm['resource_group'], vm['name']) for vm in self.managed_by_extended]

        if state == "present":
            return self.create_or_attach_disks(managed_vm_id)
        elif state == "absent":
            return self.detach_or_delete_disks(managed_vm_id)

    def compute_disks_result(self, disk_instances):
        result = []
        for params, disk in disk_instances:
            disk_id = parse_resource_id(disk.get("id"))
            result.append(self.get_managed_disk(resource_group=disk_id.get("resource_group"), name=disk_id.get("resource_name")))
        return result

    def create_or_attach_disks(self, managed_vm_id):
        changed, disk_instances, disks_to_create = False, [], []
        for disk in self.managed_disks:
            parameter, disk_instance = self.get_disk_instance(disk)
            # create or update disk
            disk_info_to_compare = dict(zone=disk.get("zone"), max_shares=disk.get("max_shares"), found_disk=disk_instance, new_disk=parameter)
            if disk_instance is None or self.is_different(**disk_info_to_compare):
                disks_to_create.append((disk, parameter))
            else:
                disk_instances.append((disk, disk_instance))

        if len(disks_to_create) > 0:
            changed = True
            result = self.create_or_update_disks(disks_to_create)
            disk_instances += result

        if self.managed_by_extended is not None and len(self.managed_by_extended) > 0:
            # Attach the disk to multiple VM
            attach_config = []
            for vm in managed_vm_id:
                time.sleep(5)
                disks = [(d, i) for d, i in disk_instances if not self._is_disk_attached_to_vm(vm.id, i)]
                if len(disks) > 0:
                    attach_config.append(self.create_attachment_configuration(vm, disks))

            if len(attach_config) > 0:
                changed = True
                self.update_virtual_machines(attach_config)

        elif self.managed_by_extended == []:
            # Detach disks from all VMs attaching them
            changed = self.detach_disks_from_all_vms(disk_instances) or changed

        return dict(changed=changed, state=self.compute_disks_result(disk_instances))

    def detach_or_delete_disks(self, managed_vm_id):
        changed, disk_instances = False, []
        for disk in self.managed_disks:
            params, disk_instance = self.get_disk_instance(disk)
            if disk_instance is not None:
                disk_instances.append((disk, disk_instance))

        result = []
        if self.managed_by_extended is not None and len(self.managed_by_extended) > 0:
            # Detach the disk from list of VMs
            disks_names = [d.get("name").lower() for p, d in disk_instances]
            attach_config = []
            for vm in managed_vm_id:
                disks = [d for p, d in disk_instances if self._is_disk_attached_to_vm(vm.id, d)]
                if len(disks) > 0:
                    attach_config.append(self.create_detachment_configuration(vm, disks_names))

            if len(attach_config) > 0:
                changed = True
                self.update_virtual_machines(attach_config)
            result = self.compute_disks_result(disk_instances)

        elif self.managed_by_extended is None:
            # Detach disks from all VMs attaching them
            changed = self.detach_disks_from_all_vms(disk_instances)

            # Delete existing disks
            if len(disk_instances) > 0:
                disks_ids = [disk.get("id") for param, disk in disk_instances]
                changed = True
                self.delete_disks(disks_ids)

        return dict(changed=changed, state=result)

    def detach_disks_from_all_vms(self, disk_instances):
        changed = False
        # Detach disk to all VMs attaching it
        unique_vm_id = []
        for param, disk_instance in disk_instances:
            managed_by_vm = disk_instance.get("managed_by")
            managed_by_extended_vms = disk_instance.get("managed_by_extended") or []
            if managed_by_vm is not None and managed_by_vm not in unique_vm_id:
                unique_vm_id.append(managed_by_vm)
            for vm_id in managed_by_extended_vms:
                if vm_id not in unique_vm_id:
                    unique_vm_id.append(vm_id)
        if unique_vm_id:
            disks_names = [instance.get("name").lower() for d, instance in disk_instances]
            changed = True
            attach_config = []
            for vm_id in unique_vm_id:
                vm_name_id = parse_resource_id(vm_id)
                vm_instance = self._get_vm(vm_name_id['resource_group'], vm_name_id['resource_name'])
                attach_config.append(self.create_detachment_configuration(vm_instance, disks_names))

            if len(attach_config) > 0:
                changed = True
                self.update_virtual_machines(attach_config)
        return changed

    def _is_disk_attached_to_vm(self, vm_id, item):
        managed_by = item['managed_by']
        managed_by_extended = item['managed_by_extended']
        if managed_by is not None and vm_id == managed_by:
            return True
        if managed_by_extended is not None and vm_id in managed_by_extended:
            return True
        return False

    def create_attachment_configuration(self, vm, disks):
        vm_id = parse_resource_id(vm.id)

        # attach all disks to the virtual machine
        for managed_disk, disk_instance in disks:
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
            params = self.multi_disk_models.ManagedDiskParameters(id=disk_instance.get('id'), storage_account_type=disk_instance.get('storage_account_type'))
            attach_caching = managed_disk.get("attach_caching")
            caching_options = self.multi_disk_models.CachingTypes[attach_caching] if attach_caching and attach_caching != '' else None

            # pylint: disable=missing-kwoa
            data_disk = self.multi_disk_models.DataDisk(lun=lun,
                                                        create_option=self.compute_models.DiskCreateOptionTypes.attach,
                                                        managed_disk=params,
                                                        caching=caching_options)
            vm.storage_profile.data_disks.append(data_disk)
        return vm_id["resource_group"], vm_id["resource_name"], vm

    def create_detachment_configuration(self, vm_instance, disks_names):
        vm_data = parse_resource_id(vm_instance.id)
        leftovers = [d for d in vm_instance.storage_profile.data_disks if d.name.lower() not in disks_names]
        if len(vm_instance.storage_profile.data_disks) == len(leftovers):
            self.fail("None of the following disks '{0}' are attached to the VM '{1}/{2}'.".format(
                disks_names, vm_data["resource_group"], vm_data["resource_name"]
            ))
        vm_instance.storage_profile.data_disks = leftovers
        return vm_data["resource_group"], vm_data["resource_name"], vm_instance

    def _get_vm(self, resource_group, name):
        try:
            return self.compute_client.virtual_machines.get(resource_group, name, expand='instanceview')
        except Exception as exc:
            self.fail("Error getting virtual machine {0}/{1} - {2}".format(resource_group, name, str(exc)))

    def create_or_update_disks(self, disks_to_create):
        pollers = []
        for disk_info, disk in disks_to_create:
            resource_group = disk_info.get("resource_group")
            name = disk_info.get("name")
            try:
                poller = self.multi_disk_client.disks.begin_create_or_update(resource_group, name, disk)
                pollers.append(poller)
            except Exception as e:
                self.fail("Error creating the managed disk {0}/{1}: {2}".format(resource_group, name, str(e)))
        disks_instances = self.get_multiple_pollers_results(pollers)
        result = []
        for i, instance in enumerate(disks_instances):
            result.append((disks_to_create[i][0], managed_disk_to_dict(instance)))
        return result

    # This method accounts for the difference in structure between the
    # Azure retrieved disk and the parameters for the new disk to be created.
    def is_different(self, zone, max_shares, found_disk, new_disk):
        resp = False
        if new_disk.get('disk_size_gb'):
            if not found_disk['disk_size_gb'] == new_disk['disk_size_gb']:
                resp = True
        if new_disk.get('os_type'):
            if found_disk['os_type'] is None or not self.multi_disk_models.OperatingSystemTypes(found_disk['os_type'].capitalize()) == new_disk['os_type']:
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

    def delete_disks(self, ids):
        pollers = []
        for disk_id in ids:
            try:
                disk = parse_resource_id(disk_id)
                resource_group, name = disk.get("resource_group"), disk.get("resource_name")
                poller = self.multi_disk_client.disks.begin_delete(resource_group, name)
                pollers.append(poller)
            except Exception as e:
                self.fail("Error deleting the managed disk {0}/{1}: {2}".format(resource_group, name, str(e)))
        return self.get_multiple_pollers_results(pollers)

    def update_virtual_machines(self, config):
        pollers = []
        for resource_group, name, params in config:
            try:
                poller = self.compute_client.virtual_machines.begin_create_or_update(resource_group, name, params)
                pollers.append(poller)
            except AzureError as exc:
                self.fail("Error updating virtual machine (attaching/detaching disks) {0}/{1} - {2}".format(resource_group, name, exc.message))
        return self.get_multiple_pollers_results(pollers)

    def get_managed_disk(self, resource_group, name):
        try:
            resp = self.multi_disk_client.disks.get(resource_group, name)
            return managed_disk_to_dict(resp)
        except ResourceNotFoundError:
            self.log("Did not find managed disk {0}/{1}".format(resource_group, name))


def main():
    """Main execution"""
    AzureRMMultipleManagedDisk()


if __name__ == '__main__':
    main()
