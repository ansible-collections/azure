#!/usr/bin/python
#
# Copyright (c) 2020 XiuxiSun, (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_virtualhub
version_added: '1.10.0'
short_description: Manage Azure VirtualHub instance
description:
    - Create, update and delete instance of Azure VirtualHub.
options:
    resource_group:
        description:
            - The resource group name of the VirtualHub.
        required: true
        type: str
    location:
        description:
            - The location of the VirtualHub.
        type: str
    name:
        description:
            - The name of the VirtualHub.
        required: true
        type: str
    virtual_wan:
        description:
            - The VirtualWAN to which the VirtualHub belongs.
        type: dict
        suboptions:
            id:
                description:
                    - Resource ID.
                type: str
    vpn_gateway:
        description:
            - The VpnGateway associated with this VirtualHub.
        type: dict
        suboptions:
            id:
                description:
                    - Resource ID.
                type: str
    p2_s_vpn_gateway:
        description:
            - The P2SVpnGateway associated with this VirtualHub.
        type: dict
        suboptions:
            id:
                description:
                    - Resource ID.
                type: str
    express_route_gateway:
        description:
            - The expressRouteGateway associated with this VirtualHub.
        type: dict
        suboptions:
            id:
                description:
                    - Resource ID.
                type: str
    azure_firewall:
        description:
            - The azureFirewall associated with this VirtualHub.
        type: dict
        suboptions:
            id:
                description:
                    - Resource ID.
                type: str
    security_partner_provider:
        description:
            - The securityPartnerProvider associated with this VirtualHub.
        type: dict
        suboptions:
            id:
                description:
                    - Resource ID.
                type: str
    address_prefix:
        description:
            - Address-prefix for this VirtualHub.
        type: str
    route_table:
        description:
            - The routeTable associated with this virtual hub.
        type: dict
        suboptions:
            routes:
                description:
                    - List of all routes.
                elements: dict
                type: list
                suboptions:
                    address_prefixes:
                        description:
                            - List of all addressPrefixes.
                        type: list
                        elements: str
                    next_hop_ip_address:
                        description:
                            - NextHop ip address.
                        type: str
    security_provider_name:
        description:
            - The Security Provider name.
        type: str
    virtual_hub_route_table_v2_s:
        description:
            - List of all virtual hub route table v2s associated with this VirtualHub.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of the resource that is unique within a resource group.
                    - This name can be used to access the resource.
                type: str
            routes:
                description:
                    - List of all routes.
                type: list
                elements: dict
                suboptions:
                    destination_type:
                        description:
                            - The type of destinations.
                        type: str
                    destinations:
                        description:
                            - List of all destinations.
                        type: list
                        elements: str
                    next_hop_type:
                        description:
                            - The type of next hops.
                        type: str
                    next_hops:
                        description:
                            - NextHops ip address.
                        type: list
                        elements: str
            attached_connections:
                description:
                    - List of all connections attached to this route table v2.
                elements: str
                type: list
    sku:
        description:
            - The sku of this VirtualHub.
        type: str
    bgp_connections:
        description:
            - List of references to Bgp Connections.
        type: list
        elements: dict
        suboptions:
            id:
                description:
                    - Resource ID.
                type: str
    ip_configurations:
        description:
            - List of references to IpConfigurations.
        type: list
        elements: dict
        suboptions:
            id:
                description:
                    - Resource ID.
                type: str
    virtual_router_asn:
        description:
            - VirtualRouter ASN.
        type: int
    virtual_router_ips:
        description:
            - VirtualRouter IPs.
        type: list
        elements: str
    enable_virtual_router_route_propogation:
        description:
            - Flag to control route propogation for VirtualRouter hub.
        type: bool
    state:
        description:
            - Assert the state of the VirtualHub.
            - Use C(present) to create or update an VirtualHub and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Fred-Sun (@Fred-Sun)
    - Haiyuan Zhang (@haiyuazhang)

'''

EXAMPLES = '''
    - name: Create a VirtualHub
      azure_rm_virtualhub:
        resource_group: myResourceGroup
        name: my_virtual_hub_name
        address_prefix: 10.2.0.0/24
        sku: Standard
        location: eastus
        enable_virtual_router_route_propogation: false
        virtual_wan:
          id: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualWans/fredwan

    - name: Delete VirtualHub
      azure_rm_virtualhub:
        resource_group: myResourceGroup
        name: my_virtual_hub_name
        location: eastus
        state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the virtual hub.
    type: complex
    returned: always
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualHubs/my_virtual_hub_name
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: my_virtual_hub_name
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
            sample: { 'key1': 'value1' }
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: cf8c0b06-d339-4155-95fd-2a363945cce4
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
                    sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualWans/fredwan
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
            type: dict
            sample: null
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
            sample: 10.2.0.0/24
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
        routing_state:
            description:
                - The routing state.
            returned: always
            type: str
            sample: Standard
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

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
try:
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMVirtualHub(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
            ),
            name=dict(
                type='str',
                required=True
            ),
            virtual_wan=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str',
                    )
                )
            ),
            vpn_gateway=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str',
                    )
                )
            ),
            p2_s_vpn_gateway=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str',
                    )
                )
            ),
            express_route_gateway=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str',
                    )
                )
            ),
            azure_firewall=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str',
                    )
                )
            ),
            security_partner_provider=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str',
                    )
                )
            ),
            address_prefix=dict(
                type='str',
            ),
            route_table=dict(
                type='dict',
                options=dict(
                    routes=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            address_prefixes=dict(
                                type='list',
                                elements='str'
                            ),
                            next_hop_ip_address=dict(
                                type='str',
                            )
                        )
                    )
                )
            ),
            security_provider_name=dict(
                type='str',
            ),
            virtual_hub_route_table_v2_s=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(
                        type='str',
                    ),
                    routes=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            destination_type=dict(
                                type='str',
                            ),
                            destinations=dict(
                                type='list',
                                elements='str'
                            ),
                            next_hop_type=dict(
                                type='str',
                            ),
                            next_hops=dict(
                                type='list',
                                elements='str'
                            )
                        )
                    ),
                    attached_connections=dict(
                        type='list',
                        elements='str'
                    )
                )
            ),
            sku=dict(
                type='str',
            ),
            bgp_connections=dict(
                type='list',
                elements='dict',
                options=dict(
                    id=dict(
                        type='str',
                    )
                )
            ),
            ip_configurations=dict(
                type='list',
                elements='dict',
                options=dict(
                    id=dict(
                        type='str',
                    )
                )
            ),
            virtual_router_asn=dict(
                type='int',
            ),
            virtual_router_ips=dict(
                type='list',
                elements='str'
            ),
            enable_virtual_router_route_propogation=dict(
                type='bool',
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.body = {}

        self.results = dict(changed=False)
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualHub, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_parameters(self.module_arg_spec, self.body, 0)

        resource_group = self.get_resource_group(self.resource_group)
        if self.location is None:
            # Set default location
            self.location = resource_group.location
        self.body['location'] = self.location

        old_response = None
        response = None

        old_response = self.get_resource()

        if not old_response:
            if self.state == 'present':
                self.to_do = Actions.Create
        else:
            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                modifiers = {}
                self.create_compare_modifiers(self.module_arg_spec, '', modifiers)
                self.results['modifiers'] = modifiers
                self.results['compare'] = []
                if not self.default_compare(modifiers, self.body, old_response, '', self.results):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.create_update_resource()
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            self.delete_resource()
        else:
            self.results['changed'] = False
            response = old_response

        if response is not None:
            self.results['state'] = response

        return self.results

    def create_update_resource(self):
        try:
            response = self.network_client.virtual_hubs.begin_create_or_update(resource_group_name=self.resource_group,
                                                                               virtual_hub_name=self.name,
                                                                               virtual_hub_parameters=self.body)
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.log('Error attempting to create the VirtualHub instance.')
            self.fail('Error creating the VirtualHub instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.network_client.virtual_hubs.begin_delete(resource_group_name=self.resource_group,
                                                                     virtual_hub_name=self.name)
        except Exception as e:
            self.log('Error attempting to delete the VirtualHub instance.')
            self.fail('Error deleting the VirtualHub instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.network_client.virtual_hubs.get(resource_group_name=self.resource_group,
                                                            virtual_hub_name=self.name)
        except ResourceNotFoundError as e:
            return False
        return response.as_dict()


def main():
    AzureRMVirtualHub()


if __name__ == '__main__':
    main()
