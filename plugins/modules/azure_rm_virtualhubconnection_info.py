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
module: azure_rm_virtualhubconnection_info
version_added: '1.14.0'
short_description: Get VirtualHub info
description:
    - Get info of VirtualHub.
options:
    resource_group:
        description:
            - The resource group name of the VirtualHub.
        type: str
        required: True
    virtual_hub_name:
        description:
            - The resource name of the VirtualHub.
        type: str
        required: True
    name:
        description:
            - The name of the VirtualHub connection.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Fred-Sun (@Fred-Sun)
    - Xu Zhang (@xuzhang3)

'''

EXAMPLES = '''
- name: Get virtual hub connection info by name
  azure_rm_virtualhubconnection_info:
    resource_group: myResourceGroup
    virtual_hub_name: virtualHub
    name: vhubname

- name: Get virtual hub connection info by resource group
  azure_rm_virtualhubconnection_info:
    resource_group: myResourceGroup
    virtual_hub_name: virtualHub
'''

RETURN = '''
virtual_hub_connection:
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
            sample: "/subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Network/virtualHubs/vhub/hubVirtualNetworkConnections/MyConnection"
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
                            sample: [{id: '/subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Network/virtualHubs/testhub/hubRouteTables/rt_name'}]
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

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase
try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVirtualHubConnectionInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            virtual_hub_name=dict(
                type='str',
                required=True
            )
        )

        self.resource_group = None
        self.name = None
        self.virtual_hub_name = None

        self.results = dict(changed=False)
        self.state = None
        self.status_code = [200]

        super(AzureRMVirtualHubConnectionInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results['virtual_hub_connection'] = self.format_item(self.get())
        else:
            self.results['virtual_hub_connection'] = self.format_item(self.list())
        return self.results

    def get(self):
        response = None

        try:
            response = self.network_client.hub_virtual_network_connections.get(resource_group_name=self.resource_group,
                                                                               virtual_hub_name=self.virtual_hub_name,
                                                                               connection_name=self.name)
        except ResourceNotFoundError:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list(self):
        response = None

        try:
            response = self.network_client.hub_virtual_network_connections.list(resource_group_name=self.resource_group,
                                                                                virtual_hub_name=self.virtual_hub_name)
        except Exception:
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
    AzureRMVirtualHubConnectionInfo()


if __name__ == '__main__':
    main()
