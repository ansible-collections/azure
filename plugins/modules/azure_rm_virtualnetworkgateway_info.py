#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_virtualnetworkgateway_info

version_added: "3.5.0"

short_description: Get or list Azure virtual network gateways

description:
    - Get or list the Azure virtual network gateways.

options:
    resource_group:
        description:
            - Name of a resource group where VPN Gateway exists or will be created.
        required: true
        type: str
    name:
        description:
            - Name of VPN Gateway.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags.
            - Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get the virtual network gateway facts
  azure_rm_virtualnetworkgateway_info:
    resource_group: myResourceGroup
    name: myVirtualNetworkGateway

- name: List virtual network gateway and filter by tags
  azure_rm_virtualnetworkgateway_info:
    resource_group: myResourceGroup
    tags:
      - key1
'''

RETURN = '''
virtual_network_gatways:
    description:
        - List the facts of the virtual network gateways.
    type: complex
    returned: always
    contains:
        bgp_settings:
            description:
                - Virtual network gateway's BGP speaker settings.
            type: dict
            returned: always
            sample: {'asn':65515, 'bgp_peering_address':'10.0.2.254', 'peer_weight':0}
        enable_bgp:
            description:
                -  Whether BGP is enabled for this virtual network gateway or not.
            type: bool
            returned: always
            sample: false
        etag:
            description:
                -  A unique read-only string that changes whenever the resource is updated.
            type: str
            returned: always
            sample: 28a83384-dda9-435b-ba0c-4914c4fce18a
        id:
            description:
                - Resource ID.
            type: str
            returned: always
            sample: "/subscriptions/xxxx-xxxx/resourceGroups/testRG/providers/Microsoft.Network/virtualNetworkGateways/vng"
        gateway_type:
            description:
                - The type of this virtual network gateway.
            type: str
            returned: always
            sample: Vpn
        ip_configurations:
            description:
                - IP configurations for virtual network gateway.
            type: list
            returned: always
            sample: [
                    {
                        "etag": "28a83384-dda9-435b-ba0c-4914c4fce18a",
                        "id": "/subscriptions/xxxx-xxxx/resourceGroups/testRG/providers/Microsoft.Network/virtualNetworkGateways/vng/ipConfigurations/default",
                        "name": "default",
                        "private_ip_allocation_method": "Dynamic",
                        "provisioning_state": "Succeeded",
                        "public_ip_address": {
                            "id": "/subscriptions/xxxx-xxxx/resourceGroups/testRG/providers/Microsoft.Network/publicIPAddresses/testPublicIP"
                        },
                        "subnet": {
                            "id": "/subscriptions/xxxx-xxxxx/resourceGroups/testRG/providers/Microsoft.Network/virtualNetworks/vnet/subnets/GatewaySubnet"
                        }
                    }
                ]
        location:
            description:
                - Resource location.
            type: str
            returned: always
            sample: eastus
        name:
            description:
                - Resoure name.
            type: str
            returned: always
            sample: vng
        provisioning_state:
            description:
                - The provisioning state of the virtual network gateway resource.
            type: str
            returned: always
            sample: Succeeded
        resource_group:
            description:
                - Resource group name.
            type: str
            returned: always
            sample: testRG
        sku:
            description:
                - The reference to the VirtualNetworkGatewaySku resource which represents the SKU selected for Virtual network gateway.
            type: dict
            returned: always
            sample: {'name':'VpnGw1', 'tier':'VpnGw1'}
        tags:
            description:
                - Resource tags.
            type: dict
            returned: always
            sample: {'common':'xyz'}
        vpn_gateway_generation:
            description:
                - The generation for this VirtualNetworkGateway.
                - Must be None if gatewayType is not VPN.
            type: str
            returned: always
            sample: Generation1
        vpn_type:
            description:
                - The type of this virtual network gateway.
            type: str
            returned: always
            sample: RouteBaseg
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMVirtualNetworkGatewayInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.resource_group = None
        self.name = None
        self.tags = None

        self.results = dict(
            changed=False,
            virtual_network_gatways=[]
        )

        super(AzureRMVirtualNetworkGatewayInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                               supports_tags=False,
                                                               facts_module=True,
                                                               supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results['virtual_network_gatways'] = self.get_item()
        else:
            self.results['virtual_network_gatways'] = self.list_item()

        return self.results

    def get_item(self):
        try:
            response = self.network_client.virtual_network_gateways.get(self.resource_group, self.name)
            if self.has_tags(response.tags, self.tags):
                return [self.vgw_to_dict(response)]
        except ResourceNotFoundError as ec:
            self.log("The virtual network gatway {0} not exist, exception as {1}".format(self.name, ec))
            return []

    def list_item(self):
        results = []
        try:
            response = self.network_client.virtual_network_gateways.list(self.resource_group)
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.vgw_to_dict(item))
        except Exception as ec:
            self.log("List virtual network gatway catch exception as {0}".format(ec))
        return results

    def vgw_to_dict(self, vgw):
        results = dict(
            resource_group=self.resource_group,
            id=vgw.id,
            name=vgw.name,
            location=vgw.location,
            gateway_type=vgw.gateway_type,
            vpn_type=vgw.vpn_type,
            vpn_gateway_generation=vgw.vpn_gateway_generation,
            enable_bgp=vgw.enable_bgp,
            tags=vgw.tags,
            provisioning_state=vgw.provisioning_state,
            sku=dict(
                name=vgw.sku.name,
                tier=vgw.sku.tier
            ),
            bgp_settings=dict(
                asn=vgw.bgp_settings.asn,
                bgp_peering_address=vgw.bgp_settings.bgp_peering_address,
                peer_weight=vgw.bgp_settings.peer_weight
            ) if vgw.bgp_settings else None,
            etag=vgw.etag,
            ip_configurations=[item.as_dict() for item in vgw.ip_configurations] if vgw.ip_configurations else None
        )
        return results


def main():
    AzureRMVirtualNetworkGatewayInfo()


if __name__ == '__main__':
    main()
