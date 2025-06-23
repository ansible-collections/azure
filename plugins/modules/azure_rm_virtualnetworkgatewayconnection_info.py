#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_virtualnetworkgatewayconnection_info

version_added: "2.7.0"

short_description: Gets or list the specified virtual network gateway connection

description:
    - Gets or list the specified virtual network gateway connection.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: true
    name:
        description:
            - The name of the virtual network gateway connection.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Gets the specified local network gateway connection by name
  azure_rm_virtualnetworkgatewayconnection_info:
    resource_group: "{{ resource_group }}"
    name: "{{ local_networkgateway_name }}"

- name: Gets all the virtual network gateway connection in a resource group
  azure_rm_virtualnetworkgatewayconnection_info:
    resource_group: "{{ resource_group }}"

- name: Gets all the virtual network gateway connection in a resource group and filter by tags
  azure_rm_virtualnetworkgatewayconnection_info:
    resource_group: "{{ resource_group }}"
    tags:
      - foo
'''

RETURN = '''
state:
    description:
        - Current state of the Azure Virtual Network Gateway Connection resource.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource ID.
            type: str
            returned: always
            sample: "/subscriptions/xxx-xxx/resourceGroups/rg/providers/Microsoft.Network/connections/fredvnet"
        authorization_key:
            description:
                - The authorizationKey.
            type: str
            returned: always
            sample: "308201E806092A864886F*************B9FADDAC2D"
        connection_mode:
            description:
                - The connection mode for this connection.
            type: str
            returned: always
            sample: Default
        connection_protocol:
            description:
                - Connection protocol used for this connection.
            type: str
            returned: always
            sample: IKEv2
        connection_type:
            description:
                - Gateway connection type.
            type: str
            returned: always
            sample: Vnet2Vnet
        dpd_timeout_seconds:
            description:
                - The dead peer detection timeout of this connection in seconds.
            type: int
            returned: always
            sample: 45
        enable_bgp:
            description:
                - EnableBgp flag.
            type: bool
            returned: always
            sample: false
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            type: str
            returned: always
            sample: 58b6f0c2-7d7c-4666-a62e-6416b4e00c83
        express_route_gateway_bypass:
            description:
                - Bypass ExpressRoute Gateway for data forwarding.
            type: bool
            returned: always
            sample: false
        ipsec_policies:
            description:
                - The IPSec Policies to be considered by this connection.
            type: list
            returned: always
            sample: []
        location:
            description:
                - The resource location.
            type: str
            returned: always
            sample: eastus
        name:
            description:
                - The resource name.
            type: str
            returned: always
            sample: fredvnetconnection
        provisioning_state:
            description:
                - The provisioning state of the virtual network gateway connection resource.
            type: str
            returned: always
            sample: Succeeded
        resource_group:
            description:
                - The resource group of the virtual network gateway connection.
            type: str
            returned: always
            sample: rg
        routing_weight:
            description:
                - The routing weight.
            type: int
            returned: always
            sample: 0
        shared_key:
            description:
                - The IPSec shared key.
            type: str
            returned: always
            sample: null
        tags:
            description:
                - The resource tags.
            type: dict
            returned: always
            sample: {'key1': 'value1'}
        traffic_selector_policies:
            description:
                - The Traffic Selector Policies to be considered by this connection.
            type: list
            returned: always
            sample: []
        use_local_azure_ip_address:
            description:
                - Use private local Azure IP for the connection.
            type: bool
            returned: always
            sample: false
        use_policy_based_traffic_selectors:
            description:
                - Enable policy-based traffic selectors.
            type: bool
            returned: always
            sample: false
        local_network_gateway2:
            description:
                - The reference to local network gateway resource.
            type: complex
            returned: when-used
            contains:
                id:
                    description:
                        - The ID of the local network gateway resource.
                    type: str
                    returned: always
                    sample: /subscriptions/xxx-xxx/resourceGroups/rg/providers/Microsoft.Network/localNetworkGateways/rpfx001
        virtual_network_gateway1:
            description:
                - The reference to virtual network gateway resource.
            type: complex
            returned: always
            contains:
                id:
                    description:
                        - The ID of the virtul network gateway resource.
                    type: str
                    returned: always
                    sample: /subscriptions/xxx-xxx/resourceGroups/rg/providers/Microsoft.Network/virtualNetworkGateways/fredvng
        virtual_network_gateway2:
            description:
                - The reference to virtual network gateway resource.
            type: complex
            returned: always
            contains:
                id:
                    description:
                        - The ID of the virtul network gateway resource.
                    type: str
                    returned: always
                    sample: /subscriptions/xxx-xxx/resourceGroups/rg/providers/Microsoft.Network/virtualNetworkGateways/fredvng02

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import HttpResponseError
except Exception:
    # handled in azure_rm_common
    pass


class AzureRMVirutalNetworkGatewayConnectionInfo(AzureRMModuleBase):
    """Gets or list the specified virtual network gateway connection facts"""

    def __init__(self):

        self.module_args = dict(
            name=dict(type='str'),
            resource_group=dict(type='str', required=True),
            tags=dict(type='list', elements='str'),
        )

        self.name = None
        self.tags = None
        self.resource_group = None

        self.results = dict(
            changed=False,
            state=[],
        )

        super(AzureRMVirutalNetworkGatewayConnectionInfo, self).__init__(derived_arg_spec=self.module_args,
                                                                         supports_check_mode=True,
                                                                         supports_tags=False,
                                                                         facts_module=True)

    def exec_module(self, **kwargs):

        for key in self.module_args:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results['state'] = self.get_network_gateway_connection()
        else:
            self.results['state'] = self.list_network_gateway_connection()

        return self.results

    def get_network_gateway_connection(self):
        """Gets the specified local network gateway connection in a resource group"""
        response = None

        try:
            response = self.network_client.virtual_network_gateway_connections.get(self.resource_group, self.name)
        except HttpResponseError as ec:
            self.log("Gets the specified local network gateway connection in a resource group Failed, Exception as {0}".format(ec))
        if response and self.has_tags(response.tags, self.tags):
            return [self.format_response(response)]
        else:
            return []

    def list_network_gateway_connection(self):
        """Gets all the virtual network gateway connection in a resource group"""
        response = None

        try:
            response = self.network_client.virtual_network_gateway_connections.list(self.resource_group)
        except HttpResponseError as ec:
            self.log("Gets all the virtual network gateway connection in a resource group Failed, Exception as {0}".format(ec))

        if response:
            results = []
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))
            return results
        else:
            return []

    def format_response(self, vngwconn):

        result = dict(
            resource_group=self.resource_group,
            authorization_key=vngwconn.authorization_key,
            connection_mode=vngwconn.connection_mode,
            connection_protocol=vngwconn.connection_protocol,
            connection_type=vngwconn.connection_type,
            dpd_timeout_seconds=vngwconn.dpd_timeout_seconds,
            etag=vngwconn.etag,
            enable_bgp=vngwconn.enable_bgp,
            express_route_gateway_bypass=vngwconn.express_route_gateway_bypass,
            id=vngwconn.id,
            ipsec_policies=vngwconn.ipsec_policies,
            location=vngwconn.location,
            name=vngwconn.name,
            provisioning_state=vngwconn.provisioning_state,
            routing_weight=vngwconn.routing_weight,
            tags=vngwconn.tags,
            traffic_selector_policies=vngwconn.traffic_selector_policies,
            shared_key=vngwconn.shared_key,
            use_local_azure_ip_address=vngwconn.use_local_azure_ip_address,
            use_policy_based_traffic_selectors=vngwconn.use_policy_based_traffic_selectors,
            virtual_network_gateway1=None,
            virtual_network_gateway2=None,
            local_network_gateway2=None
        )
        if vngwconn.local_network_gateway2:
            result['local_network_gateway2'] = dict(id=vngwconn.local_network_gateway2.id)
        if vngwconn.virtual_network_gateway1:
            result['virtual_network_gateway1'] = dict(id=vngwconn.virtual_network_gateway1.id)
        if vngwconn.virtual_network_gateway2:
            result['virtual_network_gateway2'] = dict(id=vngwconn.virtual_network_gateway2.id)

        return result


def main():
    """Main module execution code path"""

    AzureRMVirutalNetworkGatewayConnectionInfo()


if __name__ == '__main__':
    main()
