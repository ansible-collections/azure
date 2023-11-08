#!/usr/bin/python
#
# Copyright (c) 2020 XiuxiSun, (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_virtualhub_info
version_added: '1.10.0'
short_description: Get VirtualHub info
description:
    - Get info of VirtualHub.
options:
    resource_group:
        description:
            - The resource group name of the VirtualHub.
        type: str
    name:
        description:
            - The name of the VirtualHub.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Fred-Sun (@Fred-Sun)
    - Haiyuan Zhang (@haiyuazhang)

'''

EXAMPLES = '''
- name: Get virtual hub info by name
  azure_rm_virtualhub_info:
    resource_group: myResourceGroup
    name: virtualHub

- name: Get virtual hub info by resource group
  azure_rm_virtualhub_info:
    resource_group: myResourceGroup

- name: Get birtual hub info by sub
  azure_rm_virtualhub_info:
'''

RETURN = '''
virtual_hubs:
    description:
        - A list of dict results where the key is the name of the VirtualHub and the values are the facts for that VirtualHub.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualHubs/fredhub
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: fredhub
        type:
            description:
                - Resource type.
            returned: always
            type: str
            sample: Microsoft.Network/virtualHubs
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: eastus
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: {"key1":"value1"}
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: 4462b9db-6569-49be-8d00-000178b29e90
        virtual_wan:
            description:
                - The VirtualWAN to which the VirtualHub belongs.
            returned: always
            type: complex
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: /subscriptions/xxx-xxx/resourceGroups/v-xisuRG/providers/Microsoft.Network/virtualWans/virtualwanfred01
        vpn_gateway:
            description:
                - The VpnGateway associated with this VirtualHub.
            returned: always
            type: complex
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: null
        p2_s_vpn_gateway:
            description:
                - The P2SVpnGateway associated with this VirtualHub.
            returned: always
            type: complex
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: null
        express_route_gateway:
            description:
                - The expressRouteGateway associated with this VirtualHub.
            returned: always
            type: complex
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: null
        azure_firewall:
            description:
                - The azureFirewall associated with this VirtualHub.
            returned: always
            type: complex
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: null
        security_partner_provider:
            description:
                - The securityPartnerProvider associated with this VirtualHub.
            returned: always
            type: complex
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: null
        address_prefix:
            description:
                - Address-prefix for this VirtualHub.
            returned: always
            type: str
            sample: 10.0.0.0/24
        route_table:
            description:
                - The routeTable associated with this virtual hub.
            returned: always
            type: complex
            contains:
                routes:
                    description:
                        - List of all routes.
                    returned: always
                    type: list
                    contains:
                        address_prefixes:
                            description:
                                - List of all addressPrefixes.
                            returned: always
                            type: list
                            sample: null
                        next_hop_ip_address:
                            description:
                                - NextHop ip address.
                            returned: always
                            type: str
                            sample: null
        provisioning_state:
            description:
                - The provisioning state of the virtual hub resource.
            returned: always
            type: str
            sample: Succeeded
        security_provider_name:
            description:
                - The Security Provider name.
            returned: always
            type: str
            sample: null
        virtual_hub_route_table_v2_s:
            description:
                - List of all virtual hub route table v2s associated with this VirtualHub.
            returned: always
            type: complex
            contains:
                name:
                    description:
                        - The name of the resource that is unique within a resource group.
                        - This name can be used to access the resource.
                    returned: always
                    type: str
                    sample: null
                routes:
                    description:
                        - List of all routes.
                    returned: always
                    type: complex
                    contains:
                        destination_type:
                            description:
                                - The type of destinations.
                            returned: always
                            type: str
                            sample: null
                        destinations:
                            description:
                                - List of all destinations.
                            returned: always
                            type: list
                            sample: null
                        next_hop_type:
                            description:
                                - The type of next hops.
                            returned: always
                            type: str
                            sample: null
                        next_hops:
                            description:
                                - NextHops ip address.
                            returned: always
                            type: list
                            sample: null
                attached_connections:
                    description:
                        - List of all connections attached to this route table v2.
                    returned: always
                    type: list
                    sample: null
        sku:
            description:
                - The sku of this VirtualHub.
            returned: always
            type: str
            sample: Standard
        routing_state:
            description:
                - The routing state.
            returned: always
            type: str
            sample: null
        bgp_connections:
            description:
                - List of references to Bgp Connections.
            returned: always
            type: list
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: null
        ip_configurations:
            description:
                - List of references to IpConfigurations.
            returned: always
            type: list
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: null
        virtual_router_asn:
            description:
                - VirtualRouter ASN.
            returned: always
            type: int
            sample: null
        virtual_router_ips:
            description:
                - VirtualRouter IPs.
            returned: always
            type: list
            sample: null
        enable_virtual_router_route_propogation:
            description:
                - Flag to control route propogation for VirtualRouter hub.
            returned: always
            type: bool
            sample: null
        value:
            description:
                - List of VirtualHubs.
            returned: always
            type: complex
            contains:
                virtual_wan:
                    description:
                        - The VirtualWAN to which the VirtualHub belongs.
                    returned: always
                    type: complex
                    contains:
                        id:
                            description:
                                - Resource ID.
                            returned: always
                            type: str
                            sample: null
                vpn_gateway:
                    description:
                        - The VpnGateway associated with this VirtualHub.
                    returned: always
                    type: complex
                    contains:
                        id:
                            description:
                                - Resource ID.
                            returned: always
                            type: str
                            sample: null
                p2_s_vpn_gateway:
                    description:
                        - The P2SVpnGateway associated with this VirtualHub.
                    returned: always
                    type: complex
                    contains:
                        id:
                            description:
                                - Resource ID.
                            returned: always
                            type: str
                            sample: null
                express_route_gateway:
                    description:
                        - The expressRouteGateway associated with this VirtualHub.
                    returned: always
                    type: complex
                    contains:
                        id:
                            description:
                                - Resource ID.
                            returned: always
                            type: str
                            sample: null
                azure_firewall:
                    description:
                        - The azureFirewall associated with this VirtualHub.
                    returned: always
                    type: complex
                    contains:
                        id:
                            description:
                                - Resource ID.
                            returned: always
                            type: str
                            sample: null
                security_partner_provider:
                    description:
                        - The securityPartnerProvider associated with this VirtualHub.
                    returned: always
                    type: complex
                    contains:
                        id:
                            description:
                                - Resource ID.
                            returned: always
                            type: str
                            sample: null
                address_prefix:
                    description:
                        - Address-prefix for this VirtualHub.
                    returned: always
                    type: str
                    sample: null
                route_table:
                    description:
                        - The routeTable associated with this virtual hub.
                    returned: always
                    type: complex
                    contains:
                        routes:
                            description:
                                - List of all routes.
                            returned: always
                            type: list
                            contains:
                                address_prefixes:
                                    description:
                                        - List of all addressPrefixes.
                                    returned: always
                                    type: list
                                    sample: null
                                next_hop_ip_address:
                                    description:
                                        - NextHop ip address.
                                    returned: always
                                    type: str
                                    sample: null
                security_provider_name:
                    description:
                        - The Security Provider name.
                    returned: always
                    type: str
                    sample: null
                virtual_hub_route_table_v2_s:
                    description:
                        - List of all virtual hub route table v2s associated with this VirtualHub.
                    returned: always
                    type: complex
                    contains:
                        name:
                            description:
                                - The name of the resource that is unique within a resource group.
                                - This name can be used to access the resource.
                            returned: always
                            type: str
                            sample: null
                        routes:
                            description:
                                - List of all routes.
                            returned: always
                            type: list
                            contains:
                                destination_type:
                                    description:
                                        - The type of destinations.
                                    returned: always
                                    type: str
                                    sample: null
                                destinations:
                                    description:
                                        - List of all destinations.
                                    returned: always
                                    type: list
                                    sample: null
                                next_hop_type:
                                    description:
                                        - The type of next hops.
                                    returned: always
                                    type: str
                                    sample: null
                                next_hops:
                                    description:
                                        - NextHops ip address.
                                    returned: always
                                    type: list
                                    sample: null
                        attached_connections:
                            description:
                                - List of all connections attached to this route table v2.
                            returned: always
                            type: list
                            sample: null
                sku:
                    description:
                        - The sku of this VirtualHub.
                    returned: always
                    type: str
                    sample: null
                bgp_connections:
                    description:
                        - List of references to Bgp Connections.
                    returned: always
                    type: list
                    contains:
                        id:
                            description:
                                - Resource ID.
                            returned: always
                            type: str
                            sample: null
                ip_configurations:
                    description:
                        - List of references to IpConfigurations.
                    returned: always
                    type: list
                    contains:
                        id:
                            description:
                                - Resource ID.
                            returned: always
                            type: str
                            sample: null
                virtual_router_asn:
                    description:
                        - VirtualRouter ASN.
                    returned: always
                    type: int
                    sample: null
                virtual_router_ips:
                    description:
                        - VirtualRouter IPs.
                    returned: always
                    type: list
                    sample: null
                enable_virtual_router_route_propogation:
                    description:
                        - Flag to control route propogation for VirtualRouter hub.
                    returned: always
                    type: bool
                    sample: null
        next_link:
            description:
                - URL to get the next set of operation list results if there are any.
            returned: always
            type: str
            sample: null

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase
try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVirtualHubInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            name=dict(
                type='str'
            )
        )

        self.resource_group = None
        self.name = None

        self.results = dict(changed=False)
        self.state = None
        self.status_code = [200]

        super(AzureRMVirtualHubInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if (self.resource_group is not None and self.name is not None):
            self.results['virtual_hubs'] = self.format_item(self.get())
        elif (self.resource_group is not None):
            self.results['virtual_hubs'] = self.format_item(self.list_by_resource_group())
        else:
            self.results['virtual_hubs'] = self.format_item(self.list())
        return self.results

    def get(self):
        response = None

        try:
            response = self.network_client.virtual_hubs.get(resource_group_name=self.resource_group,
                                                            virtual_hub_name=self.name)
        except ResourceNotFoundError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list_by_resource_group(self):
        response = None

        try:
            response = self.network_client.virtual_hubs.list_by_resource_group(resource_group_name=self.resource_group)
        except ResourceNotFoundError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list(self):
        response = None

        try:
            response = self.network_client.virtual_hubs.list()
        except ResourceNotFoundError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def format_item(self, item):
        if item is None:
            return None
        elif hasattr(item, 'as_dict'):
            return [item.as_dict()]
        else:
            result = []
            items = list(item)
            for tmp in items:
                result.append(tmp.as_dict())
            return result


def main():
    AzureRMVirtualHubInfo()


if __name__ == '__main__':
    main()
