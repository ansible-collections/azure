#!/usr/bin/python
#
# Copyright (c) 2020 Praveen Ghuge (@praveenghuge), Karl Dasan (@ikarldasan), Sakar Mehra (@sakar97)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_expressroute_info
short_description: Get Azure Express Route
description:
    - Get facts of Azure Express Route.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the express route.
        required: True


extends_documentation_fragment:
- azure.azcollection.azure


author:
    - Praveen Ghuge (@praveenghuge)
    - Karl Dasan (@ikarldasan)
    - Sakar Mehra (@sakar97)

'''


EXAMPLES = '''
  - name: Get facts of specific expressroute
    community.azure.azure_rm_expressroute_info:
      resource_group: myResourceGroup
      name: myExpressRoute

'''

RETURN = '''
'''


try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass

class AzureExpressRouteInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False)
        self.resource_group = None
        self.name = None
        self.tags = None

        super(AzureExpressRouteInfo, self).__init__(
            self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            results = self.get()
        elif self.resource_group:
            # all the express route listed in that specific resource group
            results = self.list_resource_group()
        print("dsdsdss", results)
        # print("wwew"+ 123)
        self.results['expressroute'] = [
            self.express_route_to_dict(x) for x in results]
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.network_client.express_route_circuits.get(
                self.resource_group, self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.fail('Could not get info for express route. {0}').format(str(e))

        if response and self.has_tags(response.tags, self.tags):
            results = [response]
        return results

    def list_resource_group(self):
        self.log('List items for resource group')
        try:
            response = self.network_client.express_route_circuits.list(
                self.resource_group)

        except CloudError as exc:
            self.fail(
                "Failed to list for resource group {0} - {1}".format(self.resource_group, str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def express_route_to_dict(self, item):
        # turn express route object into a dictionary (serialization)
        express_route = item.as_dict()
        result = dict(
            additional_properties=express_route.get('additional_properties', {}),
            id=express_route.get('id', None),
            name=express_route.get('name', None),
            type=express_route.get('type', None),
            location=express_route.get('location', '').replace(' ', '').lower(),
            tags=express_route.get('tags', None),
            allow_classic_operations=express_route.get('allow_classic_operations', None),
            circuit_provisioning_state=express_route.get(
                'circuit_provisioning_state', None),
            service_provider_provisioning_state=express_route.get(
                'service_provider_provisioning_state', None),
            authorizations=express_route.get('authorizations', []),
            peerings=express_route.get('peerings', []),
            service_key=express_route.get('service_key', None),
            service_provider_notes=express_route.get('service_provider_notes', None),
            express_route_port=express_route.get('express_route_port', None),
            bandwidth_in_gbps=express_route.get('bandwidth_in_gbps', None),
            stag=express_route.get('stag', None),
            provisioning_state=express_route.get('provisioning_state', None),
            gateway_manager_etag=express_route.get('gateway_manager_etag', ''),
            global_reach_enabled=express_route.get('global_reach_enabled', '')
        )
        return result


def main():
    AzureExpressRouteInfo()


if __name__ == '__main__':
    main()
