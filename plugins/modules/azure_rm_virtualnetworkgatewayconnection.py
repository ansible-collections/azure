#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_virtualnetworkgatewayconnection
version_added: "1.14.0"
short_description: Manage Azure Virtual Network Gateway Connections
description: Create, update or delete a virtual network gateway connection.
author:
  - Nilashish Chakraborty (@NilashishC)
options:
  resource_group:
    description: Name of a resource group where the virtual network gateway connection exists or will be created.
    type: str
    required: true
  name:
    description: Name of virtual network gateway connection.
    type: str
    required: true
  state:
    description: State of the virtual network gateway connection. Use C(present) to create or update and C(absent) to delete it.
    type: str
    default: present
    choices: ["absent", "present"]
  location:
    description: Valid Azure location. Defaults to location of the resource group.
    type: str
  virtual_network_gateway1:
    description: The name of the virtual network gateway resource.
    type: str
  virtual_network_gateway2:
    description: The name of the second virtual network gateway resource.
    type: str
  local_network_gateway:
    description: The name of the local network gateway resource.
    type: str
  authorization_key:
    description: The authorization key.
    type: str
  connection_type:
    description: The gateway connection type.
    type: str
    choices: ["IPsec", "Vnet2Vnet", "ExpressRoute", "VPNClient"]
  connection_protocol:
    description: Connection protocol used for this connection.
    type: str
    choices: ["IKEv2", "IKEv1"]
  routing_weight:
    description: The routing weight.
    type: int
  dpd_timeout_seconds:
    description: The dead peer detection timeout of this connection in seconds.
    type: int
  shared_key:
    description: The IPSec shared key.
    type: str
  enable_bgp:
    description: EnableBgp flag.
    type: bool
  use_local_azure_ip_address:
    description: Use private local Azure IP for the connection.
    type: bool
  use_policy_based_traffic_selectors:
    description: Enable policy-based traffic selectors.
    type: bool
  express_route_gateway_bypass:
    description: Bypass ExpressRoute Gateway for data forwarding.
    type: bool
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
'''

EXAMPLES = '''
    - name: Create Virtual Network Gateway Connection
      azure.azcollection.azure_rm_virtualnetworkgatewayconnection:
        name: Test-VN-GW-Conn
        location: West US 3
        resource_group: VPN-RG
        virtual_network_gateway1: VPN-VNG
        local_network_gateway: Local-NW-GW
        connection_type: IPsec
        connection_protocol: IKEv2
        shared_key: SuperSecretKey
        state: present

    - name: Delete Virtual Network Gateway Connections
      azure.azcollection.azure_rm_virtualnetworkgatewayconnection:
        name: Test-VN-GW-Conn
        location: West US 3
        resource_group: VPN-RG
        state: absent
'''

RETURN = '''
id:
    description:
        - Virual Network Gateway connection resource ID.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/connections/MyVNGWConnection"
'''
try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


def vngwconn_to_dict(vngwconn):
    results = dict(
        id=vngwconn.id,
        name=vngwconn.name,
        location=vngwconn.location,
        etag=vngwconn.etag,
        tags=vngwconn.tags,
        virtual_network_gateway1=vngwconn.virtual_network_gateway1,
        virtual_network_gateway2=vngwconn.virtual_network_gateway2,
        local_network_gateway=vngwconn.local_network_gateway2,
        authorization_key=vngwconn.authorization_key,
        connection_type=vngwconn.connection_type,
        connection_protocol=vngwconn.connection_protocol,
        routing_weight=vngwconn.routing_weight,
        dpd_timeout_seconds=vngwconn.dpd_timeout_seconds,
        shared_key=vngwconn.shared_key,
        enable_bgp=vngwconn.enable_bgp,
        use_local_azure_ip_address=vngwconn.use_local_azure_ip_address,
        use_policy_based_traffic_selectors=vngwconn.use_policy_based_traffic_selectors,
        express_route_gateway_bypass=vngwconn.express_route_gateway_bypass,
        provisioning_state=vngwconn.provisioning_state,
    )
    return results


class AzureRMVirutalNetworkGatewayConnection(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            virtual_network_gateway1=dict(type='str', required=False),
            virtual_network_gateway2=dict(type='str'),
            local_network_gateway=dict(type='str'),
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

        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None

        self.results = dict(
            changed=False,
            state=dict()
        )

        super(AzureRMVirutalNetworkGatewayConnection, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True
        )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False
        results = dict()
        vngwconn = None

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        resource_group = self.get_resource_group(self.resource_group)

        # get virtual network gateway connection if it exists
        try:
            vngwconn = self.network_client.virtual_network_gateway_connections.get(self.resource_group, self.name)
            if self.state == 'absent':
                self.log("CHANGED: Virtual Network Gateway Connection exists but requested state is 'absent'")
                changed = True
        except ResourceNotFoundError:
            if self.state == 'present':
                self.log("CHANGED: Virtual Network Gateway Connection {0} does not exist but requested state is 'present'".format(self.name))
                changed = True

        if vngwconn:
            results = vngwconn_to_dict(vngwconn)
            if self.state == 'present':
                update_tags, results['tags'] = self.update_tags(results['tags'])
                if update_tags:
                    changed = True
                elif self.dpd_timeout_seconds and (self.dpd_timeout_seconds != results['dpd_timeout_seconds']):
                    changed = True
                elif self.use_local_azure_ip_address and (self.use_local_azure_ip_address != results['use_local_azure_ip_address']):
                    changed = True
                elif self.enable_bgp and (self.enable_bgp != results['enable_bgp']):
                    changed = True
                elif self.use_policy_based_traffic_selectors and (self.use_policy_based_traffic_selectors != results['use_policy_based_traffic_selectors']):
                    changed = True

        self.results['changed'] = changed
        self.results['id'] = results.get('id')

        if self.check_mode:
            return self.results

        if changed:
            if self.state == "present":
                # get virtual network gateway1 object
                vn_gateway_1 = self.get_vn_gateway(self.virtual_network_gateway1)
                # get virtual network gateway object
                vn_gateway_2 = self.get_vn_gateway(self.virtual_network_gateway2)
                # get local network gateway object
                local_nw_gateway = self.get_local_nw_gateway(self.local_network_gateway)

                vngwconn = self.network_models.VirtualNetworkGatewayConnection(
                    location=self.location,
                    virtual_network_gateway1=vn_gateway_1,
                    virtual_network_gateway2=vn_gateway_2,
                    local_network_gateway2=local_nw_gateway,
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
                )
                if self.tags:
                    vngwconn.tags = self.tags
                results = self.create_or_update_vngwconn(vngwconn)

            else:
                results = self.delete_vngwconn()

        if self.state == 'present':
            self.results['id'] = results['id']
        return self.results

    def get_vn_gateway(self, virtual_network_gateway):
        vn_gw = None
        try:
            if virtual_network_gateway:
                vn_gw = self.network_client.virtual_network_gateways.get(self.resource_group, virtual_network_gateway)
            return vn_gw
        except ResourceNotFoundError:
            self.fail("Virtual Network Gateway - {0} in Resource Group - {1} does not exist!".format(virtual_network_gateway, self.resource_group))

    def get_local_nw_gateway(self, local_network_gateway):
        ln_gw = None
        try:
            if local_network_gateway:
                ln_gw = self.network_client.local_network_gateways.get(self.resource_group, local_network_gateway)
            return ln_gw
        except ResourceNotFoundError:
            self.fail("Local Network Gateway - {0} in Resource Group - {1} does not exist!".format(local_network_gateway, self.resource_group))

    def create_or_update_vngwconn(self, vngwconn):
        try:
            poller = self.network_client.virtual_network_gateway_connections.begin_create_or_update(self.resource_group, self.name, vngwconn)
            new_vngwconn = self.get_poller_result(poller)
            return vngwconn_to_dict(new_vngwconn)
        except Exception as exc:
            self.fail("Error creating or updating virtual network gateway connection {0} - {1}".format(self.name, str(exc)))

    def delete_vngwconn(self):
        try:
            poller = self.network_client.virtual_network_gateway_connections.begin_delete(self.resource_group, self.name)
            self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error deleting virtual network gateway connection {0} - {1}".format(self.name, str(exc)))
        return True


def main():
    AzureRMVirutalNetworkGatewayConnection()


if __name__ == '__main__':
    main()
