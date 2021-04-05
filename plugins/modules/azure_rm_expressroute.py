#!/usr/bin/python
#
# Copyright (c) 2020 Sakar Mehra (@sakar97), Praveen Ghuge (@praveenghuge), Karl Dasan (@karldas30)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
__metaclass__ = type
DOCUMENTATION = '''
---
module: azure_rm_expressroute
version_added: "0.1.2"
short_description: Manage Express Route Circuits
description:
    - Create, update and delete instance of Express Route.
options:
    resource_groups:
        description:
            - Name of the resource group to which the resource belongs.
    name:
        description:
            - Unique name of the app service plan to create or update.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    provider:
        description:
            - The service Provider Name
    peering_location:
        description:
            - The peering location
    bandwith:
        description:
            - The BandwidthInMbps
    sku:
        description:
            - The name of the SKU.
            - Please see (https://azure.microsoft.com/en-in/pricing/details/expressroute/)
        default: Standard
        choices:
            - Standard
            - Premium
    billing model:
        description:
            - The tier of the SKU
        default: Metered
        choices:
            - Metered
            - Unlimited
    state:
      description:
          - Assert the state of the express route.
          - Use C(present) to create or update an express route and C(absent) to delete it.
      default: present
      choices:
          - absent
          - present
extends_documentation_fragment:
- azure.azcollection.azure
author:
    - Praveen Ghuge (@praveenghuge)
    - Karl Dasan (@ikarldas30)
    - Sakar Mehra (@sakar97)
'''
EXAMPLES = '''
    - name: Create a express route
      azure_rm_expressroute:
        resource_group: myResourceGroup
        name: myAppPlan
        location: eastus
        provider: Airtel
        peering_location: Chennai2
        bandwith: 10
        sku: Standard
        billing_model: Metered
'''
try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureExpressRoute(AzureRMModuleBase):
    def __init__(self):
        # define user inputs from playbook
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            provider=dict(type='str'),
            peering_location=dict(type='str'),
            bandwith=dict(type='str'),
            sku=dict(choices=["Standard", "Premium"],
                     default='Standard', type='str'),
            billing_model=dict(
                choices=['Metered', 'Unlimited'], default='Metered', type='str'),
            state=dict(choices=['present', 'absent'],
                       default='present', type='str')
        )
        self.resource_group = None
        self.name = None
        self.location = None
        self.provider = None
        self.peering_location = None
        self.bandwith = None
        self.sku = None
        self.billing_model = None
        self.tags = None
        self.state = None
        self.results = dict(
            changed=False,
            state=dict()
        )
        super(AzureExpressRoute, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        self.results['check_mode'] = self.check_mode

        # retrieve resource group to make sure it exists
        self.get_resource_group(self.resource_group)

        results = dict()
        changed = False
        try:
            self.log('Fetching Express Route Circuits {0}'.format(self.name))
            express_route_circuit = self.network_client.express_route_circuits.get(self.resource_group, self.name)
            
            results = express_route_to_dict(express_route_circuit)

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

            params = dict(
                location=self.location,
                sku=self.sku,
                billing_model=self.billing_model,
                peering_location=self.peering_location,
                provider=self.provider,
                bandwith=self.bandwith
            )
            if self.state == "present":
                self.create_or_update_express_route(params)
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
            params = {
            "sku": {
                "name": "Standard_MeteredData",
                "tier": "Standard",
                "family": "MeteredData"
            },
            "location": "eastus",
            # "authorizations": [],
            # "peerings": [],
            # "allow_classic_operations": False,
            "service_provider_properties": {
                "service_provider_name": "Airtel",
                "peering_location": "Chennai2",
                "bandwidth_in_mbps": "50"
            }
            }
            response = self.network_client.express_route_circuits.create_or_update(self.resource_group, self.name, params)
            print("-----000000---------", response)                                                                                         
            self.log("Response : {0}".format(response))
        except CloudError as ex:
            self.fail("Failed to create express route {0} in resource group {1}: {2}".format(
                self.name, self.resource_group, str(ex)))
        return True

    def delete_expressroute(self):
        '''
        Deletes specified express route circuit
        :return True
        '''
        self.log("Deleting the express route {0}".format(self.name))
        try:
            poller = self.network_client.express_route_circuits.delete(self.resource_group, self.name)
            result = self.get_poller_result(poller)
        except CloudError as e:
            self.log('Error attempting to delete express route.')
            self.fail(
                "Error deleting the express route : {0}".format(str(e)))
        return result


def express_route_to_dict(item):
    # turn express route object into a dictionary (serialization)
    d = item.as_dict()
    result = dict(
        additional_properties=d.get('additional_properties', {}),
        id=d.get('id', None),
        name=d.get('name', None),
        type=d.get('type', None),
        location=d.get('location', '').replace(' ', '').lower(),
        tags=d.get('tags', None),
        # 'sku': <azure.mgmt.network.v2019_06_01.models._models_py3.ExpressRouteCircuitSku object at 0x7feb0dd91c40>,
        # 'sku': d['sku']['tier'].lower(),
        allow_classic_operations=d.get('allow_classic_operations', None),
        circuit_provisioning_state=d.get('circuit_provisioning_state', None),
        service_provider_provisioning_state=d.get('service_provider_provisioning_state', None),
        authorizations=d.get('authorizations', []),
        peerings=d.get('peerings', []),
        service_key=d.get('service_key', None),
        service_provider_notes=d.get('service_provider_notes', None),
        # 'service_provider_properties': <azure.mgmt.network.v2019_06_01.models._models_py3.ExpressRouteCircuitServiceProviderProperties object at 0x7feb0dd91c70>,
        express_route_port=d.get('express_route_port', None),
        bandwidth_in_gbps=d.get('bandwidth_in_gbps', None),
        stag=d.get('stag', None),
        provisioning_state=d.get('provisioning_state', None),
        gateway_manager_etag=d.get('gateway_manager_etag', ''),
        global_reach_enabled=d.get('global_reach_enabled', '')
    )
    return result

def main():
    AzureExpressRoute()


if __name__ == '__main__':
    main()
