#!/usr/bin/python
#
# Copyright (c) 2020 Fred-Sun, (@Fred-Sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_privateendpoint_info

version_added: "1.8.0"

short_description: Get private endpoints info

description:
    - Get facts for private endpoints.

options:
    name:
        description:
            - Name of resource group.
        type: str
    resource_group:
        description:
            - Limit results by resource group.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
    - name: Get facts for one private endpoint
      azure_rm_privateendpoint_info:
        resource_group: myResourceGroup
        name: testprivateendpoint

    - name: Get all private endpoint under the resource group
      azure_rm_privateendpoint_info:
        resource_group: myResourceGroup

    - name: Get all private endpoint under subscription
      azure_rm_virtualnetwork_info:
        tags:
          - key1:value1
'''

RETURN = '''
state:
    description:
        - List of private endpoint dict with same format as M(azure.azcollection.azure_rm_privateendpoint) module paramter.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID of the private endpoint.
            sample: /subscriptions/xxx-xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/privateEndpoints/testprivateendpoint
            returned: always
            type: str
        etag:
            description:
                -  A unique read-only string that changes whenever the resource is updated.
            sample: 'W/\"20803842-7d51-46b2-a790-ded8971b4d8a'
            returned: always
            type: str
        network_interfaces:
            description:
                - List ID of the network interfaces.
            returned: always
            type: list
            sample:  ["/subscriptions/xxx-xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/networkInterfaces/fredprivateendpoint002.nic"]
        location:
            description:
                - Valid Azure location.
            returned: always
            type: str
            sample: eastus
        tags:
            description:
                - Tags assigned to the resource. Dictionary of string:string pairs.
            returned: always
            type: dict
            sample: { "tag1": "abc" }
        provisioning_state:
            description:
                - Provisioning state of the resource.
            returned: always
            sample: Succeeded
            type: str
        name:
            description:
                - Name of the private endpoint.
            returned: always
            type: str
            sample: estprivateendpoint
        subnets_id:
            description:
                - Subnets associated with the virtual network.
            returned: always
            type: str
            sample: "/subscriptions/xxx-xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/fredtestRG-vnet/subnets/default"
        private_link_service_connections:
            description:
                - The resource id of the private endpoint to connect.
            returned: always
            type: list
            sample: ["/subscriptions/xxx/resourceGroups/myRG/providers/Microsoft.Network/privateEndpoints/point/privateLinkServiceConnections/point",]
        type:
            description:
                - Resource type.
            returned: always
            type: str
            sample: Microsoft.Network/privateEndpoints
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMPrivateEndpointInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.results = dict(
            changed=False,
            privateendpoints=[]
        )

        self.name = None
        self.resource_group = None
        self.tags = None
        self.results = dict(
            changed=False
        )

        super(AzureRMPrivateEndpointInfo, self).__init__(self.module_arg_spec,
                                                         supports_check_mode=True,
                                                         supports_tags=False,
                                                         facts_module=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results['privateendpoints'] = self.get_item()
        elif self.resource_group is not None:
            self.results['privateendpoints'] = self.list_resource_group()
        else:
            self.results['privateendpoints'] = self.list_items()

        return self.results

    def get_item(self):
        self.log('Get properties for {0}'.format(self.name))
        item = None
        results = []

        try:
            item = self.network_client.private_endpoints.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')
        format_item = self.privateendpoints_to_dict(item)

        if format_item and self.has_tags(format_item['tags'], self.tags):
            results = [format_item]
        return results

    def list_resource_group(self):
        self.log('List items for resource group')
        try:
            response = self.network_client.private_endpoints.list(self.resource_group)
        except ResourceNotFoundError as exc:
            self.fail("Failed to list for resource group {0} - {1}".format(self.resource_group, str(exc)))

        results = []
        for item in response:
            format_item = self.privateendpoints_to_dict(item)
            if self.has_tags(format_item['tags'], self.tags):
                results.append(format_item)
        return results

    def list_items(self):
        self.log('List all for items')
        try:
            response = self.network_client.private_endpoints.list_by_subscription()
        except ResourceNotFoundError as exc:
            self.fail("Failed to list all items - {0}".format(str(exc)))

        results = []
        for item in response:
            format_item = self.privateendpoints_to_dict(item)
            if self.has_tags(format_item['tags'], self.tags):
                results.append(format_item)
        return results

    def privateendpoints_to_dict(self, privateendpoint):
        if privateendpoint is None:
            return None
        results = dict(
            id=privateendpoint.id,
            name=privateendpoint.name,
            location=privateendpoint.location,
            tags=privateendpoint.tags,
            provisioning_state=privateendpoint.provisioning_state,
            type=privateendpoint.type,
            etag=privateendpoint.etag,
            subnet_id=privateendpoint.subnet.id
        )
        if privateendpoint.network_interfaces and len(privateendpoint.network_interfaces) > 0:
            results['network_interfaces'] = []
            for interface in privateendpoint.network_interfaces:
                results['network_interfaces'].append(interface.id)
        if privateendpoint.private_link_service_connections and len(privateendpoint.private_link_service_connections) > 0:
            results['private_link_service_connections'] = []
            for connections in privateendpoint.private_link_service_connections:
                results['private_link_service_connections'].append(connections.id)
        if privateendpoint.manual_private_link_service_connections and len(privateendpoint.manual_private_link_service_connections) > 0:
            results['manual_private_link_service_connections'] = []
            for connections in privateendpoint.manual_private_link_service_connections:
                results['manual_private_link_service_connections'].append(connections.id)
        return results


def main():
    AzureRMPrivateEndpointInfo()


if __name__ == '__main__':
    main()
