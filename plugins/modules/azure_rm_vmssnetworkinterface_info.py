#!/usr/bin/python
#
# Copyright (c) 2023 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_vmssnetworkinterface_info

version_added: "1.15.0"

short_description: Get information about network interface in virtul machine scale

description:
    - Get information about network interface in virtual machine scale set.

options:
    name:
        description:
            - The name of the network interface.
            - If configure I(name), you must set the parameters I(vm_index).
        type: str
    vmss_name:
        description:
            - The name of the virtual machine scale set.
        type: str
        required: True
    vm_index:
        description:
            - The virtual machine index, such as I(vm_index=0).
        type: str
    resource_group:
        description:
            - Name of the resource group.
        type: str
        required: True

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Get information by the network name
  azure_rm_vmssnetworkinterface_info:
    resource_group: myResourceGroup
    name: nic001
    vmss_name: testVMSS
    vm_index: 0

- name: Get all network interface information in virtual machine scale set
  azure_rm_vmssnetworkinterface_info:
    resource_group: myResourceGroup
    vmss_name: testVMSS

- name: Get all network interface information in the same virtual machine index.
  azure_rm_vmssnetworkinterface_info:
    resource_group: myResourceGroup
    vmss_name: testVMSS
    vm_index: 1
'''

RETURN = '''
vmss_networkinterfaces:
    description:
        - List of network interface dicts. Each dict contains parameters can be passed to M(azure.azcollection.azure_rm_vmssnetworkinterface) module.
    type: complex
    returned: always
    contains:
        id:
            description:
                - Id of the network interface.
            returned: always
            type: str
            sample: "/subscriptions/xxx-xxx/resourceGroups/RG/providers/Microsoft.Compute/virtualMachineScaleSets/fredvmss/virtualMachines/1/networkInterfaces/nic01"
        resource_group:
            description:
                - Name of a resource group where the network interface exists.
            returned: always
            type: str
            sample: RG
        name:
            description:
                - Name of the network interface.
            type: str
            returned: always
            sample: nic01
        location:
            description:
                - Azure location.
            type: str
            returned: always
            sample: eastus
        virtual_network:
            description:
                - An existing virtual network with which the network interface will be associated.
                - It is a dict which contains I(name) and I(resource_group) of the virtual network.
            type: dict
            returned: always
            sample: {"name": "vnet01", "resource_group": "RG"}
        subnet:
            description:
                - Name of an existing subnet within the specified virtual network.
            type: str
            returned: always
            sample: default
        tags:
            description:
                - Tags of the network interface.
            type: dict
            returned: always
            sample: {"key1": "value1"}
        ip_configurations:
            description:
                - List of IP configurations, if contains multiple configurations.
            type: complex
            returned: always
            contains:
                name:
                    description:
                        - Name of the IP configuration.
                    type: str
                    returned: always
                    sample: defaultIpConfiguration
                private_ip_address:
                    description:
                        - Private IP address for the IP configuration.
                    type: str
                    returned: always
                    sample: 10.3.0.5
                private_ip_allocation_method:
                    description:
                        - Private IP allocation method.
                    returned: always
                    type: str
                    sample: Dynamic
                public_ip_address:
                    description:
                        - Name of the public IP address. None for disable IP address.
                    returned: always
                    type: str
                    sample: null
                public_ip_allocation_method:
                    description:
                        - Public IP allocation method.
                    returned: always
                    type: str
                    sample: null
                load_balancer_backend_address_pools:
                    description:
                        - List of existing load-balancer backend address pools associated with the network interface.
                    returned: always
                    type: str
                    sample: null
                application_gateway_backend_address_pools:
                    description:
                        - List of existing application gateway backend address pools associated with the network interface.
                    returned: always
                    type: str
                    sample: null
                primary:
                    description:
                        - Whether the IP configuration is the primary one in the list.
                    returned: always
                    type: bool
                    sample: True
                application_security_groups:
                    description:
                        - List of Application security groups.
                    returned: always
                    type: str
                    sample: /subscriptions/<subsid>/resourceGroups/<rg>/providers/Microsoft.Network/applicationSecurityGroups/myASG
        enable_accelerated_networking:
            description:
                - Specifies whether the network interface should be created with the accelerated networking feature or not.
            type: bool
            returned: always
            sample: True
        create_with_security_group:
            description:
                - Specifies whether a default security group should be be created with the NIC. Only applies when creating a new NIC.
            type: bool
            returned: always
            sample: True
        security_group:
            description:
                - A security group resource ID with which to associate the network interface.
            type: str
            returned: always
            sample: /subscriptions/xxx-xxx/resourceGroups/RG/providers/Microsoft.Network/networkSecurityGroups/nic01
        enable_ip_forwarding:
            description:
                - Whether to enable IP forwarding
            type: bool
            returned: always
            sample: True
        dns_servers:
            description:
                - Which DNS servers should the NIC lookup.
                - List of IP addresses.
            type: list
            returned: always
            sample: []
        mac_address:
            description:
                - The MAC address of the network interface.
            type: str
            returned: always
            sample: 00-0D-3A-17-EC-36
        provisioning_state:
            description:
                - The provisioning state of the network interface.
            type: str
            returned: always
            sample: Succeeded
        dns_settings:
            description:
                - The DNS settings in network interface.
            type: complex
            returned: always
            contains:
                dns_servers:
                    description:
                        - List of DNS servers IP addresses.
                    returned: always
                    type: list
                    sample: []
                applied_dns_servers:
                    description:
                        - If the VM that uses this NIC is part of an Availability Set, then this list will have the union of all DNS servers
                          from all NICs that are part of the Availability Set. This property is what is configured on each of those VMs.
                    returned: always
                    type: list
                    sample: []
                internal_dns_name_label:
                    description:
                        - Relative DNS name for this NIC used for internal communications between VMs in the same virtual network.
                    returned: always
                    type: str
                    sample: null
                internal_fqdn:
                    description:
                        - Fully qualified DNS name supporting internal communications between VMs in the same virtual network.
                    returned: always
                    type: str
                    sample: null
'''  # NOQA
try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, azure_id_to_dict


AZURE_OBJECT_CLASS = 'VMSSNetworkInterface'


def nic_to_dict(nic):
    ip_configurations = [
        dict(
            name=config.name,
            private_ip_address=config.private_ip_address,
            private_ip_allocation_method=config.private_ip_allocation_method,
            primary=config.primary if config.primary else False,
            load_balancer_backend_address_pools=([item.id for item in config.load_balancer_backend_address_pools]
                                                 if config.load_balancer_backend_address_pools else None),
            application_gateway_backend_address_pools=([item.id for item in config.application_gateway_backend_address_pools]
                                                       if config.application_gateway_backend_address_pools else None),
            public_ip_address=config.public_ip_address.id if config.public_ip_address else None,
            public_ip_allocation_method=config.public_ip_address.public_ip_allocation_method if config.public_ip_address else None,
            application_security_groups=([asg.id for asg in config.application_security_groups]
                                         if config.application_security_groups else None)
        ) for config in nic.ip_configurations
    ]
    config = nic.ip_configurations[0] if len(nic.ip_configurations) > 0 else None
    subnet_dict = azure_id_to_dict(config.subnet.id) if config and config.subnet else None
    subnet = subnet_dict.get('subnets') if subnet_dict else None
    virtual_network = dict(
        resource_group=subnet_dict.get('resourceGroups'),
        name=subnet_dict.get('virtualNetworks')) if subnet_dict else None
    return dict(
        id=nic.id,
        resource_group=azure_id_to_dict(nic.id).get('resourceGroups'),
        name=nic.name,
        subnet=subnet,
        virtual_network=virtual_network,
        location=nic.location,
        tags=nic.tags,
        security_group=nic.network_security_group.id if nic.network_security_group else None,
        dns_settings=dict(
            dns_servers=nic.dns_settings.dns_servers,
            applied_dns_servers=nic.dns_settings.applied_dns_servers,
            internal_dns_name_label=nic.dns_settings.internal_dns_name_label,
            internal_fqdn=nic.dns_settings.internal_fqdn
        ),
        ip_configurations=ip_configurations,
        mac_address=nic.mac_address,
        enable_ip_forwarding=nic.enable_ip_forwarding,
        provisioning_state=nic.provisioning_state,
        enable_accelerated_networking=nic.enable_accelerated_networking,
        dns_servers=nic.dns_settings.dns_servers,
    )


class AzureRMVMSSNetworkInterfaceInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str', required=True),
            vmss_name=dict(type='str', required=True),
            vm_index=dict(type='str'),
        )

        self.results = dict(
            changed=False,
        )

        self.name = None
        self.resource_group = None
        self.vmss_name = None
        self.vm_index = None

        super(AzureRMVMSSNetworkInterfaceInfo, self).__init__(self.module_arg_spec,
                                                              supports_check_mode=True,
                                                              supports_tags=False,
                                                              facts_module=True
                                                              )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        results = []
        if self.name is not None:
            if self.vm_index is not None:
                results = self.get_item()
            else:
                self.fail("Parameter error: vm_index required when filtering by name.")
        elif self.vm_index is not None:
            results = self.list_vm_index()
        else:
            results = self.list_vmss()

        self.results['vmss_networkinterfaces'] = self.to_dict_list(results)
        return self.results

    def get_item(self):
        res = None
        self.log("Get the specified network interface in a virtual machine scale set.")
        try:
            res = self.network_client.network_interfaces.get_virtual_machine_scale_set_network_interface(resource_group_name=self.resource_group,
                                                                                                         virtual_machine_scale_set_name=self.vmss_name,
                                                                                                         virtualmachine_index=self.vm_index,
                                                                                                         network_interface_name=self.name)
        except ResourceNotFoundError:
            pass

        return [res] if res is not None else []

    def list_vm_index(self):
        try:
            res = self.network_client.network_interfaces.list_virtual_machine_scale_set_vm_network_interfaces(resource_group_name=self.resource_group,
                                                                                                              virtual_machine_scale_set_name=self.vmss_name,
                                                                                                              virtualmachine_index=self.vm_index)
            return list(res)
        except Exception as exc:
            self.fail("Error listing by resource group {0} - {1}".format(self.resource_group, str(exc)))

    def list_vmss(self):
        self.log('List all')
        try:
            response = self.network_client.network_interfaces.list_virtual_machine_scale_set_network_interfaces(resource_group_name=self.resource_group,
                                                                                                                virtual_machine_scale_set_name=self.vmss_name)
            return list(response)
        except Exception as exc:
            self.fail("Error listing all - {0}".format(str(exc)))

    def to_dict_list(self, raws):
        return [nic_to_dict(item) for item in raws] if raws else []


def main():
    AzureRMVMSSNetworkInterfaceInfo()


if __name__ == '__main__':
    main()
