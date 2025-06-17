#!/usr/bin/python
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
            etag=vgw.etag
        )
        return results


def main():
    AzureRMVirtualNetworkGatewayInfo()


if __name__ == '__main__':
    main()
