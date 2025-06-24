#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_virtualnetworkgatewayconnection

version_added: "2.7.0"

short_description: Manage Azure Virtual Network Gateway Connection in a resource group

description:
    - Create, update or delete Azure Virtual Network Gateway Connection in a resource group

options:
    resource_group:
        description:
            - The network gateway connection's resource group.
        type: str
        required: true
    name:
        description:
            - The name of the network gateway connection.
        type: str
        required: true
    location:
        description:
            - The location of the network gateway connection.
        type: str
    local_network_gateway2:
        description:
            - The reference to local network gateway resource.
        type: str
    virtual_network_gateway1:
        description:
            - The reference to virtual network gateway resource.
        type: str
    virtual_network_gateway2:
        description:
            - The reference to virtual network gateway resource.
        type: str
    authorization_key:
        description:
            - The authorizationKey.
        type: str
    connection_type:
        description:
            - Gateway connection type.
        type: str
        choices:
            - IPsec
            - Vnet2Vnet
            - ExpressRoute
            - VPNClient
    connection_protocol:
        description:
            - Connection protocol used for this connection.
        choices:
            - IKEv2
            - IKEv1
        type: str
    routing_weight:
        description:
            - The routing weight.
        type: int
    dpd_timeout_seconds:
        description:
            - The dead peer detection timeout of this connection in seconds.
        type: int
    shared_key:
        description:
            - The IPSec shared key.
        type: str
    enable_bgp:
        description:
            - EnableBgp flag.
        type: bool
    use_local_azure_ip_address:
        description:
            - Use private local Azure IP for the connection.
        type: bool
    use_policy_based_traffic_selectors:
        description:
            - Enable policy-based traffic selectors.
        type: bool
    express_route_gateway_bypass:
        description:
            - Bypass ExpressRoute Gateway for data forwarding.
        type: bool
    state:
        description:
            - Use C(present) to create or update a virtual network gateway connection.
            - Use C(absent) to delete the virtual network gateway connection.
        type: str
        default: present
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Create a new virtual network gateway connection
  azure_rm_virtualnetworkgatewayconnection:
    resource_group: "{{ resource_group }}"
    name: "new{{ rpfx }}"
    virtual_network_gateway1: "{{ virtual_network_gateway1 }}"
    virtual_network_gateway2: "{{ virtual_network_gateway2 }}"
    local_network_gateway2: "{{ local_network_gateway2 }}"
    authorization_key: Password@0329
    connection_type: Vnet2Vnet
    connection_protocol: IKEv2
    routing_weight: 1
    dpd_timeout_seconds: 60
    enable_bgp: false
    use_local_azure_ip_address: false
    use_policy_based_traffic_selectors: false
    express_route_gateway_bypass: false
    tags:
      key1: value1

- name: Delete network gateway connection
  virtualnetworkgatewayconnection:
    resource_group: "{{ resource_group }}"
    name: "localgateway-name"
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the Azure Local Network Gateway resource.
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
            sample: "308201E806092A864********************78B9FADDAC2D"
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
            returned: when-used
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
    from azure.core.polling import LROPoller
except Exception:
    # handled in azure_rm_common
    pass


class AzureRMVirutalNetworkGatewayConnection(AzureRMModuleBase):
    """Utility class to get Azure Kubernetes Service Credentials facts"""

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            virtual_network_gateway1=dict(type='str', required=False),
            virtual_network_gateway2=dict(type='str'),
            local_network_gateway2=dict(type='str'),
            authorization_key=dict(type='str', no_log=True),
            connection_type=dict(type='str', choices=["IPsec", "Vnet2Vnet", "ExpressRoute", "VPNClient"]),
            connection_protocol=dict(type='str', choices=["IKEv2", "IKEv1"]),
            routing_weight=dict(type='int'),
            dpd_timeout_seconds=dict(type='int'),
            shared_key=dict(type='str', no_log=True),
            enable_bgp=dict(type='bool'),
            use_local_azure_ip_address=dict(type='bool'),
            use_policy_based_traffic_selectors=dict(type='bool'),
            express_route_gateway_bypass=dict(type='bool'),
        )

        self.name = None
        self.resource_group = None
        self.location = None
        self.state = None
        self.virtual_network_gateway1 = None
        self.virtual_network_gateway2 = None
        self.local_network_gateway2 = None
        self.authorization_key = None
        self.connection_type = None
        self.connection_protocol = None
        self.routing_weight = None
        self.dpd_timeout_seconds = None
        self.shared_key = None
        self.enable_bgp = None
        self.use_local_azure_ip_address = None
        self.use_policy_based_traffic_selectors = None
        self.express_route_gateway_bypass = None

        required_if = [('connection_type', 'IPsec', ['name', 'local_network_gateway2']),
                       ('connection_type', 'Vnet2Vnet', ['name', 'virtual_network_gateway2'])]

        self.results = dict(
            changed=False,
            state=dict(),
        )

        super(AzureRMVirutalNetworkGatewayConnection, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                     supports_check_mode=True,
                                                                     supports_tags=True,
                                                                     required_if=required_if,
                                                                     facts_module=False)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec) + ['tags']:
            setattr(self, key, kwargs[key])

        if not self.location:
            # Set default location
            resource_group = self.get_resource_group(self.resource_group)
            self.location = resource_group.location

        old_response = self.get_local_network_gateway()
        changed = False
        update_tags = False
        response = None

        if self.state == 'present':
            if old_response is not None:
                if self.dpd_timeout_seconds and (self.dpd_timeout_seconds != old_response['dpd_timeout_seconds']):
                    changed = True
                elif bool(self.use_local_azure_ip_address) != bool(old_response['use_local_azure_ip_address']):
                    changed = True
                elif bool(self.enable_bgp) != bool(old_response['enable_bgp']):
                    changed = True
                elif bool(self.use_policy_based_traffic_selectors) != bool(old_response['use_policy_based_traffic_selectors']):
                    changed = True
                elif self.routing_weight and (self.routing_weight != old_response['routing_weight']):
                    changed = True
                elif bool(self.express_route_gateway_bypass) != bool(old_response['express_route_gateway_bypass']):
                    changed = True
            else:
                changed = True

            if changed:
                if not self.check_mode:
                    response = self.create_or_update_network_gateway_connection()
            if old_response is not None:
                update_tags, new_tags = self.update_tags(old_response.get('tags'))
                if update_tags:
                    if not self.check_mode:
                        response = self.update_vngwc_tags(new_tags)
                    changed = True
        else:
            if not self.check_mode:
                if old_response is not None:
                    self.delete_local_network_gateway()
                    changed = True
                    response = None
            else:
                changed = True

        if response is None:
            response = old_response
        self.results['state'] = response
        self.results['changed'] = changed
        return self.results

    def get_local_network_gateway(self):
        """Gets the specified network gateway connection in a resource group"""
        response = None
        try:
            response = self.network_client.virtual_network_gateway_connections.get(self.resource_group, self.name)
        except HttpResponseError as ec:
            self.log("Gets the specified network gateway connection in a resource group Failed, Exception as {0}".format(ec))
            return None
        return self.format_response(response)

    def create_or_update_network_gateway_connection(self):
        """Create or Update network gateway connection"""
        response = None
        try:
            body = dict(location=self.location,
                        virtual_network_gateway1=dict(id=self.virtual_network_gateway1) if self.virtual_network_gateway1 else None,
                        virtual_network_gateway2=dict(id=self.virtual_network_gateway2) if self.virtual_network_gateway2 else None,
                        local_network_gateway2=dict(id=self.local_network_gateway2) if self.local_network_gateway2 else None,
                        authorization_key=self.authorization_key,
                        connection_type=self.connection_type,
                        connection_protocol=self.connection_protocol,
                        routing_weight=self.routing_weight,
                        dpd_timeout_seconds=self.dpd_timeout_seconds,
                        shared_key=self.shared_key,
                        enable_bgp=self.enable_bgp,
                        use_local_azure_ip_address=self.use_local_azure_ip_address,
                        use_policy_based_traffic_selector=self.use_policy_based_traffic_selectors,
                        express_route_gateway_bypass=self.express_route_gateway_bypass,
                        tags=self.tags)
        except Exception as ec:
            pass
        try:
            response = self.network_client.virtual_network_gateway_connections.begin_create_or_update(self.resource_group, self.name, body)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except HttpResponseError as ec:
            self.fail("Create or Updated a network gateway connection in a resource group Failed, Exception as {0}".format(ec))

        return self.format_response(response)

    def update_vngwc_tags(self, tags):
        """Updates a network gateway connection tags"""
        response = None
        try:
            response = self.network_client.virtual_network_gateway_connections.begin_update_tags(self.resource_group, self.name, dict(tags=tags))
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except HttpResponseError as ec:
            self.fail("Update a network gateway connection tags Failed, Exception as {0}".format(ec))
        return self.format_response(response)

    def delete_local_network_gateway(self):
        """Deletes the specified network gateway connection"""
        try:
            poller = self.network_client.virtual_network_gateway_connections.begin_delete(self.resource_group, self.name)
            self.get_poller_result(poller)
        except HttpResponseError as ec:
            self.fail("Deletes the specified network gateway connection Failed, Exception as {0}".format(ec))
        return None

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
            virtual_network_gateway2=None,
            local_network_gateway2=None,
            virtual_network_gateway1=None,
        )
        if vngwconn.local_network_gateway2:
            result['local_network_gateway2'] = dict(id=vngwconn.local_network_gateway2.id)
        if vngwconn.virtual_network_gateway2:
            result['virtual_network_gateway2'] = dict(id=vngwconn.virtual_network_gateway2.id)
        if vngwconn.virtual_network_gateway1:
            result['virtual_network_gateway1'] = dict(id=vngwconn.virtual_network_gateway1.id)
        return result


def main():
    """Main module execution code path"""

    AzureRMVirutalNetworkGatewayConnection()


if __name__ == '__main__':
    main()
