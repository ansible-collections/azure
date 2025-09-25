#!/usr/bin/python
#
# Copyright (c) 2019 Zim Kalinowski, (@zikalino)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_subnet_info
version_added: "0.1.2"
short_description: Get Azure Subnet facts
description:
    - Get facts of Azure Subnet.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
        type: str
    virtual_network_name:
        description:
            - The name of the virtual network.
        required: True
        type: str
    name:
        description:
            - The name of the subnet.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zim Kalinowski (@zikalino)

'''

EXAMPLES = '''
- name: Get facts of specific subnet
  azure_rm_subnet_info:
    resource_group: myResourceGroup
    virtual_network_name: myVirtualNetwork
    name: mySubnet

- name: List facts for all subnets in virtual network
  azure_rm_subnet_info:
    resource_group: myResourceGroup
    virtual_network_name: myVirtualNetwork
    name: mySubnet
'''

RETURN = '''
subnets:
    description:
        - A list of dictionaries containing facts for subnet.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Subnet resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/my
                     VirtualNetwork/subnets/mySubnet"
        resource_group:
            description:
                - Name of resource group.
            returned: always
            type: str
            sample: myResourceGroup
        virtual_network_name:
            description:
                - Name of the containing virtual network.
            returned: always
            type: str
            sample: myVirtualNetwork
        name:
            description:
                - Name of the subnet.
            returned: always
            type: str
            sample: mySubnet
        address_prefix_cidr:
            description:
                - CIDR defining the IPv4 address space of the subnet.
            returned: always
            type: str
            sample: "10.1.0.0/16"
        address_prefixes_cidr:
            description:
                - CIDR defining the IPv4 and IPv6 address space of the subnet.
            returned: always
            type: list
            sample: ["10.2.0.0/24", "fdda:e69b:1587:495e::/64"]
        route_table:
            description:
                - Associated route table ID.
            returned: always
            type: str
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/routeTables/myRouteTable
        private_endpoint_network_policies:
            description:
                - C(Enabled) or C(Disabled) apply network policies on private endpoints in the subnet.
            returned: always
            type: str
            sample: Enabled
        private_link_service_network_policies:
            description:
                - C(Enabled) or C(Disabled) apply network policies on private link service in the subnet.
            returned: always
            type: str
            sample: Disabled
        security_group:
            description:
                - Associated security group ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/networkSecurityGr
                     oups/myNsg"
        service_endpoints:
            description:
                - List of service endpoints.
            type: list
            returned: when available
            contains:
                service:
                    description:
                        - The type of the endpoint service.
                    returned: always
                    type: str
                    sample: Microsoft.Sql
                locations:
                    description:
                        - A list of location names.
                    type: list
                    returned: always
                    sample: [ 'eastus', 'westus' ]
                provisioning_state:
                    description:
                        - Provisioning state.
                    returned: always
                    type: str
                    sample: Succeeded
        delegations:
            description:
                - Associated delegation of subnets
            returned: always
            type: list
            contains:
                name:
                    description:
                        - name of delegation
                    returned: when delegation is present
                    type: str
                    sample: "delegationname"
                serviceName:
                    description:
                        - service associated to delegation
                    returned: when delegation is present
                    type: str
                    sample: "Microsoft.ContainerInstance/containerGroups"
                actions:
                    description:
                        - list of actions associated with service of delegation
                    returned : when delegation is present
                    type: list
                    sample: ["Microsoft.Network/virtualNetworks/subnets/action"]
                provisioning_state:
                    description:
                        - Provisioning state of delegation.
                    returned: when delegation is present
                    type: str
                    sample: Succeeded
        provisioning_state:
            description:
                - Provisioning state.
            returned: always
            type: str
            sample: Succeeded
        nat_gateway:
            description:
                - ID of the associated NAT Gateway.
            returned: when available
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/natGateways/myGw"
        sharing_scope:
            description:
                - Set this property to Tenant to allow sharing subnet with other  subscriptions in your AAD tenant.
            type: str
            returned: always
            sample: None
        service_endpoint_policies:
            description:
                - An array of service endpoint policies.
            type: list
            returned: always
            sample: ["/subscriptions/xxx-xxx/resourceGroups/TestRG/providers/Microsoft.Network/serviceEndpointPolicies/testpolicy"]
        default_outbound_access:
            description:
                - Set this property to false to disable default outbound connectivity for all VMs in the subnet.
            type: bool
            returned: always
            sample: false
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSubnetInfo(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            virtual_network_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.virtual_network_name = None
        self.name = None
        super(AzureRMSubnetInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results['subnets'] = self.get()
        else:
            self.results['subnets'] = self.list()

        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.network_client.subnets.get(resource_group_name=self.resource_group,
                                                       virtual_network_name=self.virtual_network_name,
                                                       subnet_name=self.name)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError as e:
            self.fail('Could not get facts for Subnet.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list(self):
        response = None
        results = []
        try:
            response = self.network_client.subnets.list(resource_group_name=self.resource_group,
                                                        virtual_network_name=self.virtual_network_name)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError as e:
            self.fail('Could not get facts for Subnet.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'virtual_network_name': self.parse_resource_to_dict(d.get('id')).get('name'),
            'name': d.get('name'),
            'id': d.get('id'),
            'address_prefix_cidr': d.get('address_prefix'),
            'address_prefixes_cidr': d.get('address_prefixes'),
            'route_table': d.get('route_table', {}).get('id'),
            'security_group': d.get('network_security_group', {}).get('id'),
            'provisioning_state': d.get('provisioning_state'),
            'service_endpoints': d.get('service_endpoints'),
            'private_endpoint_network_policies': d.get('private_endpoint_network_policies'),
            'private_link_service_network_policies': d.get('private_link_service_network_policies'),
            'delegations': d.get('delegations'),
            'nat_gateway': d.get('nat_gateway', {}).get('id'),
            'sharing_scope': d.get('sharing_scope'),
            'default_outbound_access': d.get('default_outbound_access'),
            'service_endpoint_policies': [item['id'] for item in d['service_endpoint_policies']] if d.get('service_endpoint_policies') else []
        }

        return d


def main():
    AzureRMSubnetInfo()


if __name__ == '__main__':
    main()
