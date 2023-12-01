#!/usr/bin/python
#
# Copyright (c) 2020 Praveen Ghuge (@praveenghuge), Karl Dasan (@ikarldasan), Sakar Mehra (@sakar97)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_expressroute_info
version_added: "1.7.0"
short_description: Get Azure Express Route
description:
    - Get facts of Azure Express Route.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
        type: str
    name:
        description:
            - The name of the express route.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

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
    tags:
      - key:value
'''

RETURN = '''
state:
    description:
        - Current state of the express route.
    returned: always
    type: dict

    sample: {
            "additional_properties": {},
            "allow_classic_operations": true,
            "authorizations": [
                {
                    "authorization_key": "d83e18b5-0200-4e0b-9cdb-6fdf95b00267",
                    "authorization_use_status": "Available",
                    "etag": "W/'09572845-c667-410c-b664-ed8e39242c13'",
                    "id": "/subscriptions/subs_id/resourceGroups/rg/providers/Microsoft.Network/expressRouteCircuits/exp/authorizations/az",
                    "name": "authorization_test",
                    "provisioning_state": "Succeeded",
                    "type": "Microsoft.Network/expressRouteCircuits/authorizations"
                }
            ],
            "bandwidth_in_gbps": null,
            "circuit_provisioning_state": "Enabled",
            "express_route_port": null,
            "gateway_manager_etag": "",
            "global_reach_enabled": false,
            "id": "/subscriptions/subs_id/resourceGroups/rg/providers/Microsoft.Network/expressRouteCircuits/exp",
            "location": "eastus",
            "name": "exp",
            "peerings": [],
            "provisioning_state": "Succeeded",
            "service_key": "e1956383-63b6-4709-8baa-3615bbf5d22b",
            "service_provider_notes": null,
            "service_provider_provisioning_state": "NotProvisioned",
            "stag": 27,
            "status": "Deleted",
            "tags": {
                "a": "b"
            },
            "type": "Microsoft.Network/expressRouteCircuits"
        }
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
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
            ),
            tags=dict(
                type='list',
                elements='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False)
        self.resource_group = None
        self.name = None
        self.tags = None

        super(AzureExpressRouteInfo, self).__init__(
            self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            results = self.get()
        elif self.resource_group:
            # all the express route listed in that specific resource group
            results = self.list_resource_group()

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
        except ResourceNotFoundError as e:
            self.fail('Could not get info for express route. {0}').format(str(e))

        if response and self.has_tags(response.tags, self.tags):
            results = [response]
        return results

    def list_resource_group(self):
        self.log('List items for resource group')
        try:
            response = self.network_client.express_route_circuits.list(
                self.resource_group)

        except ResourceNotFoundError as exc:
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
