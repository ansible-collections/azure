#!/usr/bin/python
#
# Copyright (c) 2018
# Gustavo Muniz do Carmo <gustavo@esign.com.br>
# Zim Kalinowski <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_virtualmachine_info

version_added: "0.1.2"

short_description: Get virtual machine facts

description:
    - Get facts for one or all virtual machines in a resource group.

options:
    resource_group:
        description:
            - Name of the resource group containing the virtual machines (required when filtering by vm name).
        type: str
    name:
        description:
            - Name of the virtual machine.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Gustavo Muniz do Carmo (@gustavomcarmo)
    - Zim Kalinowski (@zikalino)

'''

EXAMPLES = '''
- name: Get facts for all virtual machines of a resource group
  azure_rm_virtualmachine_info:
    resource_group: myResourceGroup

- name: Get facts by name
  azure_rm_virtualmachine_info:
    resource_group: myResourceGroup
    name: myVm

- name: Get facts by tags
  azure_rm_virtualmachine_info:
    resource_group: myResourceGroup
    tags:
      - testing
      - foo:bar
'''

RETURN = '''
vms:
    description:
        - List of virtual machines.
    returned: always
    type: complex
    contains:
        additional_capabilities:
            description:
                - Enables or disables a capability on the virtual machine.
            type: dict
            returned: always
            sample: {ultra_ssd_enabled: False}
        admin_username:
            description:
                - Administrator user name.
            returned: always
            type: str
            sample: admin
        boot_diagnostics:
            description:
                - Information about the boot diagnostics settings.
            returned: always
            type: complex
            contains:
                enabled:
                    description:
                        - Indicates if boot diagnostics are enabled.
                    returned: always
                    type: bool
                    sample: true
                storage_uri:
                    description:
                        - Indicates the storage account used by boot diagnostics.
                    returned: always
                    type: str
                    sample: https://mystorageaccountname.blob.core.windows.net/
                console_screenshot_uri:
                    description:
                        - Contains a URI to grab a console screenshot.
                        - Only present if enabled.
                    returned: always
                    type: str
                    sample: https://mystorageaccountname.blob.core.windows.net/bootdiagnostics-myvm01-a4db09a6-ab7f-4d80-9da8-fbceaef9288a/
                            myVm.a4db09a6-ab7f-4d80-9da8-fbceaef9288a.screenshot.bmp
                serial_console_log_uri:
                    description:
                        - Contains a URI to grab the serial console log.
                        - Only present if enabled.
                    returned: always
                    type: str
                    sample: https://mystorageaccountname.blob.core.windows.net/bootdiagnostics-myvm01-a4db09a6-ab7f-4d80-9da8-fbceaef9288a/
                            myVm.a4db09a6-ab7f-4d80-9da8-fbceaef9288a.serialconsole.log
        data_disks:
            description:
                - List of attached data disks.
            returned: always
            type: complex
            contains:
                caching:
                    description:
                        - Type of data disk caching.
                    returned: always
                    type: str
                    sample: ReadOnly
                disk_size_gb:
                    description:
                        - The initial disk size in GB for blank data disks.
                    returned: always
                    type: int
                    sample: 64
                lun:
                    description:
                        - The logical unit number for data disk.
                    returned: always
                    type: int
                    sample: 0
                managed_disk_type:
                    description:
                        - Managed data disk type.
                    returned: always
                    type: str
                    sample: Standard_LRS
                managed_disk_id:
                    description:
                        - Managed data disk ID.
                    returned: always
                    type: str
                    sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/Microsoft.Compute/disks/diskName
                write_accelerator_enabled:
                    description:
                        - Specifies whether writeAccelerator should be enabled or disabled on the disk.
                    type: bool
                    returned: always
                    sample: False
        user_data:
            description:
                - UserData for the VM, which must be base-64 encoded.
            type: str
            returned: always
            sample: None
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Compute/virtualMachines/myVm
        image:
            description:
                - Image specification.
            returned: always
            type: complex
            contains:
                offer:
                    description:
                        - The offer of the platform image or marketplace image used to create the virtual machine.
                    type: str
                    returned: when created from marketplace image
                    sample: RHEL
                publisher:
                    description:
                        - Publisher name.
                    type: str
                    returned: when created from marketplace image
                    sample: RedHat
                sku:
                    description:
                        - SKU name.
                    type: str
                    returned: when created from marketplace image
                    sample: 7-RAW
                version:
                    description:
                        - Image version.
                    type: str
                    returned: when created from marketplace image
                    sample: 7.5.2018050901
                id:
                    description:
                        - Custom image resource ID.
                    type: str
                    returned: when created from custom image
                    sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Compute/images/myImage
                community_gallery_image_id:
                    description:
                        - The community gallery image unique id for vm deployment.
                    type: str
                    returned: when created from community gallery image
                    sample: "/CommunityGalleries/yellowbrick-fc7e81f1-87dd-4989-9ca8-03743762e873/Images/Ubuntu-5.15.0-1035-azure_22.04"
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: japaneast
        maintenance_redeploy_status:
            description:
                - If maintenance is scheduled for this server set to something like example, otherwise empty dict
            returned: always
            type: dict
            sample: { "is_customer_initiated_maintenance_allowed": true, "last_operation_result_code": "None", "maintenance_window_end_time":
                    "2025-06-18T23:59:00.000Z", "maintenance_window_start_time": "2025-06-12T00:00:00.000Z", "pre_maintenance_window_end_time":
                    "2025-06-11T23:30:00.000Z", "pre_maintenance_window_start_time": "2025-01-30T00:00:00.000Z" }
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: myVm
        network_interface_names:
            description:
                - List of attached network interfaces.
            returned: always
            type: list
            sample: [
                "myNetworkInterface"
            ]
        proximityPlacementGroup:
            description:
                - The name or ID of the proximity placement group the VM should be associated with.
            type: dict
            returned: always
            sample: { "id": "/subscriptions/xxx/resourceGroups/xxx/providers/Microsoft.Compute/proximityPlacementGroups/testid13"}
        CapacityReservation:
            description:
                - The name or ID of the capacity reservation group to be associated with.
            type: dict
            returned: always
            sample: { }
        os_disk_caching:
            description:
                - Type of OS disk caching.
            returned: always
            type: str
            sample: ReadOnly
        os_type:
            description:
                - Base type of operating system.
            returned: always
            type: str
            sample: Linux
        resource_group:
            description:
                - Resource group.
            returned: always
            type: str
            sample: myResourceGroup
        state:
            description:
                - State of the resource.
            returned: always
            type: str
            sample: present
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: { "key1":"value1" }
        vm_agent_version:
            description:
                - Version of the Azure VM Agent (waagent) running inside the VM.
            returned: always
            type: str
            sample: '2.9.1.1'
        vm_size:
            description:
                - Virtual machine size.
            returned: always
            type: str
            sample: Standard_D4
        zones:
            description:
                - A list of Availability Zones for your VM.
            type: list
            sample: [1]
        power_state:
            description:
                - Power state of the virtual machine.
            returned: always
            type: str
            sample: running
        display_status:
            description:
                - The short localizable label for the status.
            returned: always
            type: str
            sample: "VM running"
        provisioning_state:
            description:
                - The provisioning state, which only appears in the response.
            returned: always
            type: str
            sample: running
        identity:
            description:
                - The identity of the virtual machine.
            type: dict
            returned: always
            sample: {
                    "principal_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                    "tenant_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                    "type": "SystemAssigned, UserAssigned",
                    "user_assigned_identities": {
                        "/subscriptions/xxx/resourceGroups/testRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test": {
                            "client_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                            "principal_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                        }
                    }
        }
        security_profile:
            description:
                - Specifies the Security related profile settings for the virtual machine.
            type: complex
            returned: when-used
            contains:
                encryption_at_host:
                    description:
                        - This property can be used by user in the request to enable or disable the Host Encryption for the virtual machine.
                        - This will enable the encryption for all the disks including Resource/Temp disk at host itself.
                    type: bool
                    returned: when-enabled
                    sample: True
                security_type:
                    description:
                        - Specifies the SecurityType of the virtual machine.
                        - It is set as TrustedLaunch to enable UefiSettings.
                    type: str
                    returned: when-enabled
                    sample: TrustedLaunch
                uefi_settings:
                    description:
                        - Specifies the security settings like secure boot and vTPM used while creating the virtual machine.
                    type: complex
                    returned: when-enabled
                    contains:
                        secure_boot_enabled:
                            description:
                                - Specifies whether secure boot should be enabled on the virtual machine.
                            type: bool
                            returned: when-enabled
                            sample: True
                        v_tpm_enabled:
                            description:
                                - Specifies whether vTPM should be enabled on the virtual machine.
                            type: bool
                            returned: when-enabled
                            sample: True
'''

try:
    from azure.mgmt.core.tools import parse_resource_id
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.six.moves.urllib.parse import urlparse
import re


AZURE_OBJECT_CLASS = 'VirtualMachine'

AZURE_ENUM_MODULES = ['azure.mgmt.compute.models']


class AzureRMVirtualMachineInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.results = dict(
            changed=False,
            vms=[]
        )

        self.resource_group = None
        self.name = None
        self.tags = None

        super(AzureRMVirtualMachineInfo, self).__init__(self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=False,
                                                        facts_module=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name and not self.resource_group:
            self.fail("Parameter error: resource group required when filtering by name.")
        if self.name:
            self.results['vms'] = self.get_item()
        elif self.resource_group:
            self.results['vms'] = self.list_items_by_resourcegroup()
        else:
            self.results['vms'] = self.list_all_items()

        return self.results

    def get_item(self):
        self.log('Get properties for {0}'.format(self.name))
        item = None
        result = []

        item = self.get_vm(self.resource_group, self.name)

        if item and self.has_tags(item.get('tags'), self.tags):
            result = [item]

        return result

    def list_items_by_resourcegroup(self):
        self.log('List all items')
        try:
            items = self.compute_client.virtual_machines.list(self.resource_group)
        except ResourceNotFoundError as exc:
            self.fail("Failed to list all items - {0}".format(str(exc)))

        results = []
        for item in items:
            if self.has_tags(item.tags, self.tags):
                results.append(self.get_vm(self.resource_group, item.name))
        return results

    def list_all_items(self):
        self.log('List all items')
        try:
            items = self.compute_client.virtual_machines.list_all()
        except ResourceNotFoundError as exc:
            self.fail("Failed to list all items - {0}".format(str(exc)))

        results = []
        for item in items:
            if self.has_tags(item.tags, self.tags):
                results.append(self.get_vm(parse_resource_id(item.id).get('resource_group'), item.name))
        return results

    def get_vm(self, resource_group, name):
        '''
        Get the VM with expanded instanceView

        :return: VirtualMachine object
        '''
        try:
            vm = self.compute_client.virtual_machines.get(resource_group, name, expand='instanceview')
            return self.serialize_vm(vm)
        except ResourceNotFoundError as exc:
            self.fail("Error getting virtual machine {0} - {1}".format(self.name, str(exc)))

    def serialize_vm(self, vm):
        '''
        Convert a VirtualMachine object to dict.

        :param vm: VirtualMachine object
        :return: dict
        '''

        result = self.serialize_obj(vm, AZURE_OBJECT_CLASS, enum_modules=AZURE_ENUM_MODULES)
        resource_group = parse_resource_id(result['id']).get('resource_group')
        instance = None
        power_state = None
        display_status = None

        try:
            instance = self.compute_client.virtual_machines.instance_view(resource_group, vm.name)
            instance = self.serialize_obj(instance, AZURE_OBJECT_CLASS, enum_modules=AZURE_ENUM_MODULES)
        except Exception as exc:
            self.fail("Error getting virtual machine {0} instance view - {1}".format(vm.name, str(exc)))

        for index in range(len(instance['statuses'])):
            code = instance['statuses'][index]['code'].split('/')
            if code[0] == 'PowerState':
                power_state = code[1]
                display_status = instance['statuses'][index]['display_status']
            elif code[0] == 'OSState' and code[1] == 'generalized':
                display_status = instance['statuses'][index]['display_status']
                power_state = 'generalized'
                break
            elif code[0] == 'ProvisioningState' and code[1] == 'failed':
                display_status = instance['statuses'][index]['display_status']
                power_state = ''
                break

        new_result = {}

        if instance.get('maintenance_redeploy_status') is not None:
            new_result['maintenance_redeploy_status'] = instance['maintenance_redeploy_status']
        else:
            new_result['maintenance_redeploy_status'] = dict()

        if instance.get('vm_agent') is not None:
            new_result['vm_agent_version'] = instance['vm_agent'].get('vm_agent_version')
        else:
            new_result['vm_agent_version'] = 'Unknown'

        if vm.security_profile is not None:
            new_result['security_profile'] = dict()
            if vm.security_profile.encryption_at_host is not None:
                new_result['security_profile']['encryption_at_host'] = vm.security_profile.encryption_at_host
            if vm.security_profile.security_type is not None:
                new_result['security_profile']['security_type'] = vm.security_profile.security_type
            if vm.security_profile.uefi_settings is not None:
                new_result['security_profile']['uefi_settings'] = dict()
                if vm.security_profile.uefi_settings.secure_boot_enabled is not None:
                    new_result['security_profile']['uefi_settings']['secure_boot_enabled'] = vm.security_profile.uefi_settings.secure_boot_enabled
                if vm.security_profile.uefi_settings.v_tpm_enabled is not None:
                    new_result['security_profile']['uefi_settings']['v_tpm_enabled'] = vm.security_profile.uefi_settings.v_tpm_enabled

        new_result['power_state'] = power_state
        new_result['display_status'] = display_status
        new_result['provisioning_state'] = vm.provisioning_state
        new_result['id'] = vm.id
        new_result['resource_group'] = resource_group
        new_result['name'] = vm.name
        new_result['state'] = 'present'
        new_result['location'] = vm.location
        new_result['vm_size'] = result['hardware_profile']['vm_size']
        new_result['user_data'] = result.get('user_data', None)

        new_result['proximityPlacementGroup'] = result.get('proximity_placement_group')
        new_result['zones'] = result.get('zones', None)
        new_result['additional_capabilities'] = result.get('additional_capabilities')
        new_result['identity'] = result.get('identity')
        new_result['capacity_reservation'] = dict()
        if result.get('capacity_reservation') is not None:
            new_result['capacity_reservation']['capacity_reservation_group'] = result.get('capacity_reservation', {}).get('capacity_reservation_group')
        os_profile = result.get('os_profile')
        if os_profile is not None:
            new_result['admin_username'] = os_profile.get('admin_username')
        image = result['storage_profile'].get('image_reference')
        if image is not None:
            if image.get('publisher', None) is not None:
                new_result['image'] = {
                    'publisher': image['publisher'],
                    'sku': image['sku'],
                    'offer': image['offer'],
                    'version': image['version']
                }
            elif image.get('community_gallery_image_id') is not None:
                new_result['image'] = {
                    'community_gallery_image_id': image.get('community_gallery_image_id')
                }
            else:
                new_result['image'] = {
                    'id': image.get('id', None)
                }

        new_result['boot_diagnostics'] = {
            'enabled': 'diagnostics_profile' in result and
                       'boot_diagnostics' in result['diagnostics_profile'] and
                       result['diagnostics_profile']['boot_diagnostics']['enabled'] or False,
            'storage_uri': 'diagnostics_profile' in result and
                           'boot_diagnostics' in result['diagnostics_profile'] and
                           result['diagnostics_profile']['boot_diagnostics'].get('storageUri', None)
        }
        if new_result['boot_diagnostics']['enabled']:
            new_result['boot_diagnostics']['console_screenshot_uri'] = result['instance_view']['boot_diagnostics'].get('console_screenshot_blob_uri')
            new_result['boot_diagnostics']['serial_console_log_uri'] = result['instance_view']['boot_diagnostics'].get('serial_console_log_blob_uri')

        vhd = result['storage_profile']['os_disk'].get('vhd')
        if vhd is not None:
            url = urlparse(vhd['uri'])
            new_result['storage_account_name'] = url.netloc.split('.')[0]
            new_result['storage_container_name'] = url.path.split('/')[1]
            new_result['storage_blob_name'] = url.path.split('/')[-1]

        new_result['os_disk'] = result['storage_profile']['os_disk']
        new_result['os_disk_caching'] = result['storage_profile']['os_disk']['caching']
        new_result['os_type'] = result['storage_profile']['os_disk']['os_type']
        new_result['data_disks'] = []
        disks = result['storage_profile']['data_disks']
        for disk_index in range(len(disks)):
            new_result['data_disks'].append({
                'lun': disks[disk_index].get('lun'),
                'name': disks[disk_index].get('name'),
                'disk_size_gb': disks[disk_index].get('disk_size_gb'),
                'managed_disk_type': disks[disk_index].get('managed_disk', {}).get('storage_account_type'),
                'managed_disk_id': disks[disk_index].get('managed_disk', {}).get('id'),
                'caching': disks[disk_index].get('caching'),
                'write_accelerator_enabled': disks[disk_index].get('write_accelerator_enabled', False)
            })

        new_result['network_interface_names'] = []
        nics = result['network_profile']['network_interfaces']
        for nic_index in range(len(nics)):
            new_result['network_interface_names'].append(re.sub('.*networkInterfaces/', '', nics[nic_index]['id']))

        new_result['tags'] = vm.tags
        return new_result


def main():
    AzureRMVirtualMachineInfo()


if __name__ == '__main__':
    main()
