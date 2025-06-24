#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2017, Sertac Ozercan <seozerca@microsoft.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_virtualmachinescaleset_info

version_added: "0.1.2"

short_description: Get Virtual Machine Scale Set facts

description:
    - Get facts for a virtual machine scale set.
    - Note that this module was called M(azure.azcollection.azure_rm_virtualmachine_scaleset_facts) before Ansible 2.8. The usage did not change.

options:
    name:
        description:
            - Limit results to a specific virtual machine scale set.
        type: str
    resource_group:
        description:
            - The resource group to search for the desired virtual machine scale set.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str
    format:
        description:
            - Format of the data returned.
            - If C(raw) is selected information will be returned in raw format from Azure Python SDK.
            - If C(curated) is selected the structure will be identical to input parameters of M(azure.azcollection.azure_rm_virtualmachinescaleset) module.
            - In Ansible 2.5 and lower facts are always returned in raw format.
            - Please note that this option will be deprecated in 2.10 when curated format will become the only supported format.
        default: 'raw'
        type: str
        choices:
            - 'curated'
            - 'raw'

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Sertac Ozercan (@sozercan)
'''

EXAMPLES = '''
- name: Get facts for a virtual machine scale set
  azure_rm_virtualmachinescaleset_info:
    resource_group: myResourceGroup
    name: testvmss001
    format: curated

- name: Get facts for all virtual networks
  azure_rm_virtualmachinescaleset_info:
    resource_group: myResourceGroup

- name: Get facts by tags
  azure_rm_virtualmachinescaleset_info:
    resource_group: myResourceGroup
    tags:
      - testing
'''

RETURN = '''
vmss:
    description:
        - List of virtual machine scale sets.
    returned: always
    type: list
    sample: [{
        "constrained_maximum_capacity": false,
        "etag": "3",
        "id": "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG02/providers/Microsoft.Compute/virtualMachineScaleSets/testVMSStestvmss",
        "location": "eastus",
        "name": "testVMSStestvmss",
        "orchestration_mode": "Flexible",
        "platform_fault_domain_count": 1,
        "provisioning_state": "Succeeded",
        "single_placement_group": false,
        "sku": {
            "capacity": 1,
            "name": "Standard_A1_v2",
            "tier": "Standard"
        },
        "tags": {
            "key2": "value2",
            "key3": "value3"
        },
        "time_created": "2025-04-22T08:03:29.427822Z",
        "type": "Microsoft.Compute/virtualMachineScaleSets",
        "unique_id": "da4393f5-6060-4a0e-8ae5-7616316402b8",
        "upgrade_policy": {
            "mode": "Manual"
        },
        "virtual_machine_profile": {
            "network_profile": {
                "network_api_version": "2020-11-01",
                "network_interface_configurations": [
                    {
                        "auxiliary_mode": "None",
                        "auxiliary_sku": "None",
                        "delete_option": "Delete",
                        "disable_tcp_state_tracking": false,
                        "dns_settings": {
                            "dns_servers": []
                        },
                        "enable_ip_forwarding": false,
                        "ip_configurations": [
                            {
                                "application_gateway_backend_address_pools": [],
                                "application_security_groups": [
                                    {
                                        "id": "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG02/providers/Microsoft.Network/applicationSecurityGroups/apptestvmss02"
                                    },
                                    {
                                        "id": "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG02/providers/Microsoft.Network/applicationSecurityGroups/apptestvmss"
                                    }
                                ],
                                "load_balancer_backend_address_pools": [],
                                "name": "default",
                                "primary": true,
                                "private_ip_address_version": "IPv4",
                                "public_ip_address_configuration": {
                                    "idle_timeout_in_minutes": 4,
                                    "ip_tags": [],
                                    "name": "instancepublicip",
                                    "public_ip_address_version": "IPv4"
                                },
                                "subnet": {
                                    "id": "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG02/providers/Microsoft.Network/virtualNetworks/VMSStestVnet/subnets/VMSStestSubnet"
                                }
                            }
                        ],
                        "name": "testVMSStestvmss",
                        "primary": true
                    }
                ]
            },
            "os_profile": {
                "admin_username": "testuser",
                "allow_extension_operations": true,
                "computer_name_prefix": "testVMSStestvmss",
                "linux_configuration": {
                    "disable_password_authentication": true,
                    "patch_settings": {
                        "assessment_mode": "ImageDefault",
                        "patch_mode": "ImageDefault"
                    },
                    "provision_vm_agent": true,
                    "ssh": {
                        "public_keys": [
                            {
                                "key_data": "ssh-rsa xxxxxxxxxx xx.yy@qq.com",
                                "path": "/home/testuser/.ssh/authorized_keys"
                            }
                        ]
                    }
                },
                "require_guest_provision_signal": true,
                "secrets": []
            },
            "storage_profile": {
                "data_disks": [
                    {
                        "caching": "ReadWrite",
                        "create_option": "Empty",
                        "delete_option": "Delete",
                        "disk_size_gb": 64,
                        "lun": 0,
                        "managed_disk": {
                            "storage_account_type": "Standard_LRS"
                        }
                    }
                ],
                "image_reference": {
                    "offer": "0001-com-ubuntu-server-focal",
                    "publisher": "Canonical",
                    "sku": "20_04-lts",
                    "version": "20.04.202504030"
                },
                "os_disk": {
                    "caching": "ReadWrite",
                    "create_option": "FromImage",
                    "delete_option": "Delete",
                    "disk_size_gb": 30,
                    "managed_disk": {
                        "storage_account_type": "Standard_LRS"
                    },
                    "os_type": "Linux"
                }
            },
            "time_created": "2025-04-22T08:53:17.201851Z"
        }
    }]
'''  # NOQA

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
import re

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'VirtualMachineScaleSet'

AZURE_ENUM_MODULES = ['azure.mgmt.compute.models']


class AzureRMVirtualMachineScaleSetInfo(AzureRMModuleBase):
    """Utility class to get virtual machine scale set facts"""

    def __init__(self):

        self.module_args = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            tags=dict(type='list', elements='str'),
            format=dict(
                type='str',
                choices=['curated',
                         'raw'],
                default='raw'
            )
        )

        self.results = dict(
            changed=False,
        )

        self.name = None
        self.resource_group = None
        self.format = None
        self.tags = None

        super(AzureRMVirtualMachineScaleSetInfo, self).__init__(
            derived_arg_spec=self.module_args,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):

        for key in self.module_args:
            setattr(self, key, kwargs[key])

        if self.name and not self.resource_group:
            self.fail("Parameter error: resource group required when filtering by name.")

        if self.name:
            result = self.get_item()
        else:
            result = self.list_items()

        if self.format == 'curated':
            for index in range(len(result)):
                vmss = result[index]
                subnet_name = None
                load_balancer_name = None
                virtual_network_name = None
                ssh_password_enabled = False

                try:
                    subnet_id = (vmss['virtual_machine_profile']['network_profile']['network_interface_configurations'][0]
                                 ['ipConfigurations'][0]['subnet']['id'])
                    subnet_name = re.sub('.*subnets\\/', '', subnet_id)
                except Exception:
                    self.log('Could not extract subnet name')

                try:
                    backend_address_pool_id = (vmss['virtual_machine_profile']['network_profile']['network_interface_configurations'][0]
                                               ['ip_configurations'][0]['load_balancer_backend_address_pools'][0]['id'])
                    load_balancer_name = re.sub('\\/backendAddressPools.*', '', re.sub('.*loadBalancers\\/', '', backend_address_pool_id))
                    virtual_network_name = re.sub('.*virtualNetworks\\/', '', re.sub('\\/subnets.*', '', subnet_id))
                except Exception:
                    self.log('Could not extract load balancer / virtual network name')

                try:
                    ssh_password_enabled = (not vmss['virtual_machine_profile']['os_profile']
                                                    ['linux_configuration']['disable_password_authentication'])
                except Exception:
                    self.log('Could not extract SSH password enabled')

                data_disks = vmss['virtual_machine_profile']['storage_profile'].get('data_disks', [])

                for disk_index in range(len(data_disks)):
                    old_disk = data_disks[disk_index]
                    new_disk = {
                        'lun': old_disk['lun'],
                        'disk_size_gb': old_disk['disk_size_gb'],
                        'managed_disk_type': old_disk['managed_disk']['storage_account_type'],
                        'caching': old_disk['caching']
                    }
                    data_disks[disk_index] = new_disk

                updated = {
                    'id': vmss['id'],
                    'resource_group': self.resource_group,
                    'name': vmss['name'],
                    'state': 'present',
                    'location': vmss['location'],
                    'vm_size': vmss['sku']['name'],
                    'capacity': vmss['sku']['capacity'],
                    'tier': vmss['sku']['tier'],
                    'upgrade_policy': vmss.get('upgrade_policy'),
                    'orchestrationMode': vmss.get('orchestration_mode'),
                    'platformFaultDomainCount': vmss.get('platform_fault_domain_count'),
                    'admin_username': vmss['virtual_machine_profile']['os_profile']['admin_username'],
                    'admin_password': vmss['virtual_machine_profile']['os_profile'].get('admin_password'),
                    'ssh_password_enabled': ssh_password_enabled,
                    'image': vmss['virtual_machine_profile']['storage_profile']['image_reference'],
                    'os_disk_caching': vmss['virtual_machine_profile']['storage_profile']['os_disk']['caching'],
                    'os_type': 'Linux' if (vmss['virtual_machine_profile']['os_profile'].get('linux_configuration') is not None) else 'Windows',
                    'overprovision': vmss.get('overprovision'),
                    'managed_disk_type': vmss['virtual_machine_profile']['storage_profile']['os_disk']['managed_disk']['storage_account_type'],
                    'data_disks': data_disks,
                    'virtual_network_name': virtual_network_name,
                    'subnet_name': subnet_name,
                    'load_balancer': load_balancer_name,
                    'identity': vmss.get('identity', None),
                    'tags': vmss.get('tags')
                }

                result[index] = updated

        self.results['vmss'] = result

        return self.results

    def get_item(self):
        """Get a single virtual machine scale set"""

        self.log('Get properties for {0}'.format(self.name))

        item = None
        results = []

        try:
            item = self.compute_client.virtual_machine_scale_sets.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            pass

        if item and self.has_tags(item.tags, self.tags):
            results = [self.serialize_obj(item, AZURE_OBJECT_CLASS, enum_modules=AZURE_ENUM_MODULES)]

        return results

    def list_items(self):
        """Get all virtual machine scale sets"""

        self.log('List all virtual machine scale sets')

        try:
            response = self.compute_client.virtual_machine_scale_sets.list(self.resource_group)
        except ResourceNotFoundError as exc:
            self.fail('Failed to list all items - {0}'.format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(self.serialize_obj(item, AZURE_OBJECT_CLASS, enum_modules=AZURE_ENUM_MODULES))

        return results


def main():
    """Main module execution code path"""

    AzureRMVirtualMachineScaleSetInfo()


if __name__ == '__main__':
    main()
