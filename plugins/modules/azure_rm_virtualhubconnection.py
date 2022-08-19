#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3)
#                    XiuxiSun, (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_virtualhubconnection
version_added: '1.14.0'
short_description: Manage Azure VirtualHub instance
description:
    - Create, update and delete instance of Azure VirtualHub.
options:
    resource_group:
        description:
            - The resource group name of the VirtualHub.
        required: true
        type: str
    name:
        description:
            - The name of the VirtualHub connection.
        required: true
        type: str
    vhub_name:
        description:
            - The VirtualHub name.
        type: str
        required: True
    enable_internet_security:
        description:
            - Enable internet security.
        type: bool
    allow_remote_vnet_to_use_hub_vnet_gateways:
        description:
            - Allow RemoteVnet to use Virtual Hub's gateways.
        type: bool
    allow_hub_to_remote_vnet_transit:
        description:
            - VirtualHub to RemoteVnet transit to enabled or not.
        type: bool
    remote_virtual_network:
        description:
            - ID of the remote VNet to connect to.
        type: dict
        suboptions:
            id:
                description:
                    - The remote virtual network ID.
                type: str
    routing_configuration:
        description:
            - The Routing Configuration indicating the associated and propagated route tables on this connection.
        type: dict
        suboptions:
            propagated_route_tables:
                description:
                    - The list of RouteTables to advertise the routes to.
                type: dict
                suboptions:
                    labels:
                        description:
                            - The list of labels.
                        type: list
                        elements: str
                    ids:
                        description:
                            -The list of resource ids of all the virtual hub RouteTables.
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description:
                                    - The ID of the RouteTables.
                                type: str
            vnet_routes:
                description:
                    - List of routes that control routing from VirtualHub into a virtual network connection.
                type: dict
                suboptions:
                    static_routes:
                        description:
                            - List of all Static Routes.
                        type: list
                        elements: dict
                        suboptions:
                            name:
                                description:
                                    - The name of the StaticRoute that is unique within a VnetRoute.
                                type: str
                            address_prefixes:
                                description:
                                    - List of all address prefixes.
                                type: list
                                elements: str
                            next_hop_ip_address:
                                description:
                                    - The ip address of the next hop.
                                type: str
    state:
        description:
            - Assert the state of the VirtualHub connection.
            - Use C(present) to create or update an VirtualHub connection and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Fred-Sun (@Fred-Sun)
    - Xu Zhang (@xuzhang3)

'''

EXAMPLES = '''
- name: Create virtual hub connection
  azure_rm_virtualhubconnection:
    resource_group: myRG
    vhub_name: testhub
    name: Myconnection
    enable_internet_security: false
    allow_remote_vnet_to_use_hub_vnet_gateways: true
    allow_hub_to_remote_vnet_transit: true
    remote_virtual_network:
      id: /subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/testvnet
    routing_configuration:
      propagated_route_tables:
        labels:
          - labels1
          - labels3
        ids:
          - id: /subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Network/virtualHubs/testhub01/hubRouteTables/testtable
      vnet_routes:
        static_routes:
          - name: route1
            address_prefixes:
              - 10.1.0.0/16
              - 10.2.0.0/16
            next_hop_ip_address: 10.0.0.68
          - name: route2
            address_prefixes:
              - 10.4.0.0/16
            next_hop_ip_address: 10.0.0.65

- name: Delete virtual hub connection
  azure_rm_virtualhubconnection:
    resource_group: myRG
    vhub_name: testhub
    name: Myconnection
    state: absent

'''

RETURN = '''
state:
    description:
        - A list of dict results for the virtual hub connection info.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Network/virtualHubs/vhub/hubVirtualNetworkConnections/MyConnection
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: MyConnection
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: 31102041-49e7-4cac-8573-aac1e1a16793
        remote_virtual_network:
            description:
                - Name of ID of the remote VNet to connect to.
            returned: always
            type: complex
            contains:
                id:
                    description:
                        - The ID of the remote VNet to connect to.
                    returned: always
                    type: str
                    sample: /subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/testvnet
        routing_configuration:
            description:
                - The routing configuration information
            returned: always
            type: complex
            contains:
                associated_route_table:
                    description:
                        - The resource ID of route table associated with this routing configuration.
                    type: complex
                    returned: always
                    contains:
                        id:
                            description:
                                - The ID of the routetable.
                            type: str
                            returned: always
                            sample: /subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Network/virtualHubs/testhub/hubRouteTables/rt_name
                propagated_route_tables:
                    description:
                        - Space-separated list of resource id of propagated route tables.
                    type: complex
                    returned: always
                    contains:
                        ids:
                            description:
                                - The list resource ID of propagated route tables.
                            type: list
                            returned: always
                            sample: [{ id: '/subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Network/virtualHubs/testhub/hubRouteTables/rt_name'}]
                        labels:
                            description:
                                - Space-separated list of labels for propagated route tables.
                            type: list
                            returned: always
                            sample: ['labels1', 'labels2']
                vnet_routes:
                    description:
                        - The name of the Static Route that is unique within a Vnet Route.
                    returned: always
                    type: complex
                    contains:
                        static_routes:
                            description:
                                - The name of the Static Route.
                            type: list
                            returned: always
                            contains:
                                address_prefixes:
                                    description:
                                        - Space-separated list of all address prefixes.
                                    type: list
                                    returned: always
                                    sample: ["10.1.0.0/16", "10.2.0.0/16"]
                                name:
                                    description:
                                        - The name of static router.
                                    type: str
                                    returned: always
                                    sample: route1
                                next_hop_ip_address:
                                    description:
                                        - The next hop ip address.
                                    type: str
                                    returned: always
                                    sample: 10.0.0.65
        provisioning_state:
            description:
                - The provisioning state of the virtual hub connection resource.
            returned: always
            type: str
            sample: Succeeded
        allow_hub_to_remote_vnet_transit:
            description:
                - Enable hub to remote VNet transit.
            returned: always
            type: bool
            sample: true
        allow_remote_vnet_to_use_hub_vnet_gateways:
            description:
                - Allow remote VNet to use hub's VNet gateways.
            returned: always
            type: bool
            sample: true
        enable_internet_security:
            description:
                - Enable internet security and default is enabled.
            type: bool
            returned: always
            sample: true
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


static_routes_spec = dict(
    name=dict(type='str'),
    address_prefixes=dict(type='list', elements='str'),
    next_hop_ip_address=dict(type='str')
)


class AzureRMVirtualHubConnection(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            vhub_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            enable_internet_security=dict(
                type='bool'
            ),
            allow_remote_vnet_to_use_hub_vnet_gateways=dict(
                type='bool'
            ),
            allow_hub_to_remote_vnet_transit=dict(
                type='bool'
            ),
            remote_virtual_network=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str',
                    )
                )
            ),
            routing_configuration=dict(
                type='dict',
                options=dict(
                    propagated_route_tables=dict(
                        type='dict',
                        options=dict(
                            labels=dict(
                                type='list',
                                elements='str'
                            ),
                            ids=dict(
                                type='list',
                                elements='dict',
                                options=dict(
                                    id=dict(
                                        type='str',
                                    )
                                )
                            )
                        )
                    ),
                    vnet_routes=dict(
                        type='dict',
                        options=dict(
                            static_routes=dict(
                                type='list',
                                elements='dict',
                                options=static_routes_spec
                            )
                        )
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.vhub_name = None
        self.name = None
        self.body = {}

        self.results = dict(changed=False)
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualHubConnection, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_parameters(self.module_arg_spec, self.body, 0)

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
                if self.body.get('enable_internet_security') is not None:
                    if bool(self.body['enable_internet_security']) != bool(old_response['enable_internet_security']):
                        self.to_do = Actions.Update
                else:
                    self.body['enable_internet_security'] = old_response['enable_internet_security']
                if self.body.get('allow_remote_vnet_to_use_hub_vnet_gateways') is not None:
                    if bool(self.body['allow_remote_vnet_to_use_hub_vnet_gateways']) != bool(old_response['allow_remote_vnet_to_use_hub_vnet_gateways']):
                        self.to_do = Actions.Update
                else:
                    self.body['allow_remote_vnet_to_use_hub_vnet_gateways'] = old_response['allow_remote_vnet_to_use_hub_vnet_gateways']
                if self.body.get('allow_hub_to_remote_vnet_transit') is not None:
                    if bool(self.body['allow_hub_to_remote_vnet_transit']) != bool(old_response['allow_hub_to_remote_vnet_transit']):
                        self.to_do = Actions.Update
                else:
                    self.body['allow_hub_to_remote_vnet_transit'] = old_response['allow_hub_to_remote_vnet_transit']

                if self.body.get('routing_configuration') is not None:
                    modifiers = {}
                    self.create_compare_modifiers(self.module_arg_spec, '', modifiers)
                    self.results['modifiers'] = modifiers
                    self.results['compare'] = []
                    if not self.default_compare(modifiers, self.body['routing_configuration'], old_response['routing_configuration'], '', self.results):
                        self.to_do = Actions.Update
                    else:
                        self.body['routing_configuration'] = old_response['routing_configuration']
                else:
                    self.body['routing_configuration'] = old_response['routing_configuration']

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
            response = self.network_client.hub_virtual_network_connections.begin_create_or_update(resource_group_name=self.resource_group,
                                                                                                  virtual_hub_name=self.vhub_name,
                                                                                                  connection_name=self.name,
                                                                                                  hub_virtual_network_connection_parameters=self.body)
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.log('Error attempting to create the VirtualHub instance.')
            self.fail('Error creating the VirtualHub instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.network_client.hub_virtual_network_connections.begin_delete(resource_group_name=self.resource_group,
                                                                                        virtual_hub_name=self.vhub_name,
                                                                                        connection_name=self.name)
        except Exception as e:
            self.log('Error attempting to delete the VirtualHub connection instance.')
            self.fail('Error deleting the VirtualHub connection instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.network_client.hub_virtual_network_connections.get(resource_group_name=self.resource_group,
                                                                               virtual_hub_name=self.vhub_name,
                                                                               connection_name=self.name)
        except ResourceNotFoundError as e:
            return False
        return response.as_dict()


def main():
    AzureRMVirtualHubConnection()


if __name__ == '__main__':
    main()
