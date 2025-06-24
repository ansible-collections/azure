#!/usr/bin/python
#
# Copyright (c) 2016 Matt Davis, <mdavis@ansible.com>
#                    Chris Houseknecht, <house@redhat.com>

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_networkinterface_info

version_added: "0.1.2"

short_description: Get network interface facts

description:
    - Get facts for a specific network interface or all network interfaces within a resource group.

options:
    name:
        description:
            - Only show results for a specific network interface.
        type: str
    resource_group:
        description:
            - Name of the resource group containing the network interface(s). Required when searching by name.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Chris Houseknecht (@chouseknecht)
    - Matt Davis (@nitzmahone)

'''

EXAMPLES = '''
- name: Get facts for one network interface
  azure_rm_networkinterface_info:
    resource_group: myResourceGroup
    name: nic001

- name: Get network interfaces within a resource group
  azure_rm_networkinterface_info:
    resource_group: myResourceGroup

- name: Get network interfaces by tag
  azure_rm_networkinterface_info:
    resource_group: myResourceGroup
    tags:
      - testing
      - foo:bar
'''

RETURN = '''
networkinterfaces:
    description:
        - List of network interface dicts. Each dict contains parameters can be passed to M(azure.azcollection.azure_rm_networkinterface) module.
    type: complex
    returned: always
    contains:
        id:
            description:
                - Id of the network interface.
            type: str
            returned: always
            sample: "/subscriptions/xxxx-xxxxx/resourceGroups/testRG/providers/Microsoft.Network/networkInterfaces/nic01"
        resource_group:
            description:
                - Name of a resource group where the network interface exists.
            type: str
            returned: always
            sample: testRG
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
            type: complex
            returned: always
            contains:
                name:
                    description:
                        - The name of the virtual network relate network interface.
                    type: str
                    returned: always
                    sample: vnetnic01
                resource_gorup:
                    description:
                        - Resource groups name that exist on the virtual network.
                    type: str
                    returned: always
                    sample: testRG
                subscription_id:
                    description:
                        - Virtual network Subscription ID.
                    type: str
                    returned: always
                    sample: xxxxxxx-xxxxxxxxxxxxx
                subnet_id:
                    description:
                        - The subnet's ID.
                    type: str
                    returned: always
                    sample: "/subscriptions/xxx-xxxx/resourceGroups/testRG/providers/Microsoft.Network/virtualNetworks/nic01/subnets/sub01"
        subnet:
            description:
                - Name of an existing subnet within the specified virtual network.
            type: str
            returned: always
            sample: sub01
        tags:
            description:
                - Tags of the network interface.
            type: dict
            returned: always
            sample: {key1: value1, key2: value2}
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
                    sample: default
                private_ip_address:
                    description:
                        - Private IP address for the IP configuration.
                    type: str
                    returned: always
                    sample: 10.10.0.4
                private_ip_allocation_method:
                    description:
                        - Private IP allocation method.
                    type: str
                    returned: always
                    sample: Dynamic
                public_ip_address:
                    description:
                        - Name of the public IP address. None for disable IP address.
                    type: str
                    returned: always
                    sample: null
                public_ip_allocation_method:
                    description:
                        - Public IP allocation method.
                    type: str
                    returned: always
                    sample: null
                load_balancer_backend_address_pools:
                    description:
                        - List of existing load-balancer backend address pools associated with the network interface.
                    type: list
                    returned: always
                    sample: null
                application_gateway_backend_address_pools:
                    description:
                        - List of existing application gateway backend address pools associated with the network interface.
                    version_added: "1.10.0"
                    type: list
                    returned: always
                    sample: null
                primary:
                    description:
                        - Whether the IP configuration is the primary one in the list.
                    type: bool
                    returned: always
                    sample: true
                application_security_groups:
                    description:
                        - List of Application security groups.
                    type: list
                    returned: always
                    sample: ['/subscriptions/<subsid>/resourceGroups/<rg>/providers/Microsoft.Network/applicationSecurityGroups/myASG']
        enable_accelerated_networking:
            description:
                - Specifies whether the network interface should be created with the accelerated networking feature or not.
            type: bool
            returned: always
            sample: false
        create_with_security_group:
            description:
                - Specifies whether a default security group should be be created with the NIC. Only applies when creating a new NIC.
            type: bool
            returned: always
            sample: false
        security_group:
            description:
                - A security group resource ID with which to associate the network interface.
            type: str
            returned: always
            sample: null
        enable_ip_forwarding:
            description:
                - Whether to enable IP forwarding
            type: bool
            returned: always
            sample: false
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
            sample: null
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
                    type: list
                    returned: always
                    sample: []
                applied_dns_servers:
                    description:
                        - If the VM that uses this NIC is part of an Availability Set, then this list will have the union of all DNS servers
                          from all NICs that are part of the Availability Set. This property is what is configured on each of those VMs.
                    type: list
                    returned: always
                    sample: []
                internal_dns_name_label:
                    description:
                        - Relative DNS name for this NIC used for internal communications between VMs in the same virtual network.
                    type: str
                    returned: always
                    sample: null
                internal_fqdn:
                    description:
                        - Fully qualified DNS name supporting internal communications between VMs in the same virtual network.
                    type: str
                    returned: always
                    sample: null
'''  # NOQA
try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, azure_id_to_dict


AZURE_OBJECT_CLASS = 'NetworkInterface'


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
        subnet_id=config.subnet.id if config and config.subnet else None,
        subscription_id=subnet_dict.get('subscriptions'),
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


class AzureRMNetworkInterfaceInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.results = dict(
            changed=False,
        )

        self.name = None
        self.resource_group = None
        self.tags = None

        super(AzureRMNetworkInterfaceInfo, self).__init__(self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=False,
                                                          facts_module=True
                                                          )

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name and not self.resource_group:
            self.fail("Parameter error: resource group required when filtering by name.")

        results = []

        if self.name:
            results = self.get_item()
        elif self.resource_group:
            results = self.list_resource_group()
        else:
            results = self.list_all()

        self.results['networkinterfaces'] = self.to_dict_list(results)
        return self.results

    def get_item(self):
        self.log('Get properties for {0}'.format(self.name))
        item = None
        try:
            item = self.network_client.network_interfaces.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            pass

        return [item] if item and self.has_tags(item.tags, self.tags) else []

    def list_resource_group(self):
        self.log('List for resource group')
        try:
            response = self.network_client.network_interfaces.list(self.resource_group)
            return [item for item in response if self.has_tags(item.tags, self.tags)]
        except ResourceNotFoundError as exc:
            self.fail("Error listing by resource group {0} - {1}".format(self.resource_group, str(exc)))

    def list_all(self):
        self.log('List all')
        try:
            response = self.network_client.network_interfaces.list_all()
            return [item for item in response if self.has_tags(item.tags, self.tags)]
        except ResourceNotFoundError as exc:
            self.fail("Error listing all - {0}".format(str(exc)))

    def to_dict_list(self, raws):
        return [nic_to_dict(item) for item in raws] if raws else []


def main():
    AzureRMNetworkInterfaceInfo()


if __name__ == '__main__':
    main()
