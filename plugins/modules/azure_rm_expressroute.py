#!/usr/bin/python
#
# Copyright (c) 2021 Praveen Ghuge (@praveenghuge), Karl Dasan (@ikarldasan), Sakar Mehra (@sakar97)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_expressroute
version_added: "1.7.0"
short_description: Manage Express Route Circuits
description:
    - Create, update and delete instance of Express Route.
options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: true
        type: str
    name:
        description:
            - Unique name of the app service plan to create or update.
        required: true
        type: str
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
        type: str
    service_provider_properties:
        type: dict
        description:
            - The service Provider properties
        suboptions:
            peering_location:
                description:
                    - The peering location
                type: str
            bandwidth_in_mbps:
                description:
                    - The bandwidth of the circuit when the circuit is provisioned on an ExpressRoutePort resource.
                type: str
            service_provider_name:
                description:
                    - Name of service provider
                type: str
    sku:
        description:
            - The name of the SKU.
            - Please see L(https://azure.microsoft.com/en-in/pricing/details/expressroute/,)
            - Required sku when I(state=present).
        type: dict
        suboptions:
            tier:
                description:
                    - The tier of the SKU
                type: str
                required: true
                choices:
                    - standard
                    - premium
            family:
                description:
                    - the family of the SKU
                type: str
                required: true
                choices:
                    - metereddata
                    - unlimiteddata
    global_reach_enabled:
        description:
            - Flag denoting global reach status.
        type: bool
    authorizations:
        description:
            - The list of authorizations.
        type: list
        elements: dict
        suboptions:
            name:
                description: Name of the authorization.
                required: true
                type: str
    allow_classic_operations:
        description:
            - Support for classic operations.
        type: bool
    state:
        description:
            - Assert the state of the express route.
            - Use C(present) to create or update an express route and C(absent) to delete it.
        type: str
        default: present
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Praveen Ghuge (@praveenghuge)
    - Karl Dasan (@ikarldasan)
    - Sakar Mehra (@sakar97)
'''
EXAMPLES = '''
- name: "Create Express route"
  azure_rm_expressroute:
    resource_group: rg
    location: eastus
    name: exp
    allow_classic_operations: true
    global_reach_enabled: false
    tags:
       - a: b
    authorizations:
       - name: authorization_test
    service_provider_properties:
      service_provider_name: Aryaka Networks
      peering_location: Seattle
      bandwidth_in_mbps: '200'
    sku:
      tier: premium
      family: metereddata

- name: Delete Express route
  azure_rm_expressroute:
    resource_group: rg
    name: exp
    state: absent

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
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureExpressRoute(AzureRMModuleBase):

    def __init__(self):
        # define user inputs from playbook

        self.service_provider_properties_spec = dict(
            service_provider_name=dict(type='str'),
            peering_location=dict(type='str'),
            bandwidth_in_mbps=dict(type='str')
        )

        self.sku_spec = dict(
            tier=dict(type='str', choices=[
                      'standard', 'premium'], required=True),
            family=dict(type='str', choices=[
                        'unlimiteddata', 'metereddata'], required=True)
        )

        self.authorizations_spec = dict(
            name=dict(type='str', required=True)
        )

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            sku=dict(type='dict', options=self.sku_spec),
            allow_classic_operations=dict(type='bool'),
            authorizations=dict(type='list', options=self.authorizations_spec, elements='dict'),
            state=dict(choices=['present', 'absent'],
                       default='present', type='str'),
            service_provider_properties=dict(
                type='dict', options=self.service_provider_properties_spec),
            global_reach_enabled=dict(type='bool'),
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.allow_classic_operations = None
        self.authorizations = None
        self.service_provider_properties = None
        self.global_reach_enabled = None
        self.sku = None
        self.tags = None
        self.state = None
        self.results = dict(
            changed=False,
            state=dict()
        )

        super(AzureExpressRoute, self).__init__(self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        self.results['check_mode'] = self.check_mode

        # retrieve resource group to make sure it exists
        resource_group = self.get_resource_group(self.resource_group)

        results = dict()
        changed = False

        try:
            self.log('Fetching Express Route Circuits {0}'.format(self.name))
            express_route_circuit = self.network_client.express_route_circuits.get(
                self.resource_group, self.name)

            results = express_route_to_dict(express_route_circuit)

            # don't change anything if creating an existing zone, but change if deleting it
            if self.state == 'present':
                changed = False

                update_tags, results['tags'] = self.update_tags(
                    results['tags'])
                if update_tags:
                    changed = True

            elif self.state == 'absent':
                changed = True

        except CloudError:
            # the express route does not exist so create it
            if self.state == 'present':
                changed = True
            else:
                # you can't delete what is not there
                changed = False

        self.results['changed'] = changed
        self.results['state'] = results

        # return the results if your only gathering information
        if self.check_mode:
            return self.results

        if changed:
            if self.state == "present":
                self.results['state'] = self.create_or_update_express_route(
                    self.module.params)
            elif self.state == "absent":
                # delete express route
                self.delete_expressroute()
                self.results['state']['status'] = 'Deleted'

        return self.results

    def create_or_update_express_route(self, params):
        '''
        Create or update Express route.
        :return: create or update Express route instance state dictionary
        '''
        self.log("create or update Express Route {0}".format(self.name))
        try:
            params["sku"]["name"] = params.get("sku").get("tier") + "_" + params.get("sku").get("family")
            poller = self.network_client.express_route_circuits.create_or_update(
                resource_group_name=params.get("resource_group"),
                circuit_name=params.get("name"),
                parameters=params)
            result = self.get_poller_result(poller)
            self.log("Response : {0}".format(result))
        except CloudError as ex:
            self.fail("Failed to create express route {0} in resource group {1}: {2}".format(
                self.name, self.resource_group, str(ex)))
        return express_route_to_dict(result)

    def delete_expressroute(self):
        '''
        Deletes specified express route circuit
        :return True
        '''
        self.log("Deleting the express route {0}".format(self.name))
        try:
            poller = self.network_client.express_route_circuits.delete(
                self.resource_group, self.name)
            result = self.get_poller_result(poller)
        except CloudError as e:
            self.log('Error attempting to delete express route.')
            self.fail(
                "Error deleting the express route : {0}".format(str(e)))
        return result


def express_route_to_dict(item):
    # turn express route object into a dictionary (serialization)
    express_route = item.as_dict()
    result = dict(
        additional_properties=express_route.get('additional_properties', {}),
        id=express_route.get('id', None),
        name=express_route.get('name', None),
        type=express_route.get('type', None),
        location=express_route.get('location', '').replace(' ', '').lower(),
        tags=express_route.get('tags', None),
        allow_classic_operations=express_route.get(
            'allow_classic_operations', None),
        circuit_provisioning_state=express_route.get(
            'circuit_provisioning_state', None),
        service_provider_provisioning_state=express_route.get(
            'service_provider_provisioning_state', None),
        authorizations=express_route.get('authorizations', []),
        peerings=express_route.get('peerings', []),
        service_key=express_route.get('service_key', None),
        service_provider_notes=express_route.get(
            'service_provider_notes', None),
        express_route_port=express_route.get('express_route_port', None),
        bandwidth_in_gbps=express_route.get('bandwidth_in_gbps', None),
        stag=express_route.get('stag', None),
        provisioning_state=express_route.get('provisioning_state', None),
        gateway_manager_etag=express_route.get('gateway_manager_etag', ''),
        global_reach_enabled=express_route.get('global_reach_enabled', '')
    )
    return result


def main():
    AzureExpressRoute()


if __name__ == '__main__':
    main()
