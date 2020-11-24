#!/usr/bin/python
#
# Copyright (c) 2020 GuopengLin, (@t-glin)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_route_info
version_added: '2.0.0'
short_description: Get Route info
description:
    - Get info of Route.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    route_table_name:
        description:
            - The name of the route table.
        required: true
        type: str
    name:
        description:
            - The name of the route.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - GuopengLin (@t-glin)
    - Fred-Sun (@Fred-Sun)
    - Haiyuan Zhang (@haiyuazhang)

'''

EXAMPLES = '''
    - name: Get route
      azure_rm_route_info:
        resource_group: myResourceGroup
        name: routename
        route_table_name: routetabename


    - name: List routes
      azure_rm_route_info:
        resource_group: myResourceGroup
        route_table_name: routetabename

'''

RETURN = '''
routes:
    description:
        - A list of dict results where the key is the name of the Route and the values are the facts for that Route.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/routeTables/table01/routes/route01
        name:
            description:
                - The name of the resource that is unique within a resource group.
                - This name can be used to access the resource.
            returned: always
            type: str
            sample: route01
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: fda240c5-6f42-4eb0-8f05-b1599dc722fe
        address_prefix:
            description:
                - The destination CIDR to which the route applies.
            returned: always
            type: str
            sample: 10.0.0.0/25
        next_hop_type:
            description:
                - The type of Azure hop the packet should be sent to.
            returned: always
            type: str
            sample: VirtualAppliance
        next_hop_ip_address:
            description:
                - The IP address packets should be forwarded to.
                - Next hop values are only allowed in routes where the next hop type is VirtualAppliance.
            returned: always
            type: str
            sample: 10.0.0.0
        provisioning_state:
            description:
                - The provisioning state of the route resource.
            returned: always
            type: str
            sample: Succeeded

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase
try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRouteInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            route_table_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            )
        )

        self.resource_group = None
        self.route_table_name = None
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        self.mgmt_client = None
        super(AzureRMRouteInfo, self).__init__(self.module_arg_spec, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2020-04-01')

        if (self.resource_group is not None and self.route_table_name is not None and self.name is not None):
            self.results['routes'] = self.format_item(self.get())
        elif (self.resource_group is not None and
              self.route_table_name is not None):
            self.results['routes'] = self.format_item(self.list())
        return self.results

    def get(self):
        response = None

        try:
            response = self.mgmt_client.routes.get(resource_group_name=self.resource_group,
                                                   route_table_name=self.route_table_name,
                                                   route_name=self.name)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list(self):
        response = None

        try:
            response = self.mgmt_client.routes.list(resource_group_name=self.resource_group,
                                                    route_table_name=self.route_table_name)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def format_item(self, item):
        if hasattr(item, 'as_dict'):
            return [item.as_dict()]
        else:
            result = []
            items = list(item)
            for tmp in items:
                result.append(tmp.as_dict())
            return result


def main():
    AzureRMRouteInfo()


if __name__ == '__main__':
    main()
