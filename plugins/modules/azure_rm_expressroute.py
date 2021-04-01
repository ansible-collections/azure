#!/usr/bin/python
#
# Copyright (c) 2020 Sakar Mehra (@sakar97), Praveen Ghuge (@praveenghuge), Karl Dasan (@karldas30)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

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
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            provider=dict(type='str', required=True),
            peering_location=dict(type='str', required=True),
            bandwith=dict(type='str', required=True),
            sku=dict(choices=["Standard", "Premium"], default='Standard', type='str'),
            billing_model=dict(choices=['Metered', 'Unlimited'], default='Metered', type='str'),
            state=dict(choices=['present', 'absent'], default='present', type='str')
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.provider = None
        self.peering_location = None
        self.bandwith =None
        self.sku = None
        self.billing_model = None
        self.tags = None

        self.results = dict(changed=False)

        super(AzureExpressRoute, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                  supports_check_mode=False,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        is_old_facts = self.module._name == 'azure_rm_expressroute_facts'
        if is_old_facts:
            self.module.deprecate("The 'azure_rm_expressroute_facts' module has been renamed to 'azure_rm_expressroute'",
                                  version='3.0.0', collection_name='community.azure')  # was 2.13

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results['subnets'] = self.get()
        else:
            self.results['subnets'] = self.list()

        return self.results

    def create_or_update_express_route(self, params):
        '''
        Create or update Express route.

        :return: create or update Express route instance state dictionary
        '''
        self.log("create or update Express Route {0}".format(self.name))
        try:
            response = self.network_client.express_route_circuits.begin_create_or_update(resource_group_name=self.resource_group,
                                                                           circuit_name=self.name, parameters=params)
            self.log("Response : {0}".format(response))

        return 
        except CloudError as ex:
            self.fail("Failed to create express route {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

    def delete_expressroute(self):
        '''
        Deletes specified express route circuit
        
        :return True
        '''
        self.log("Deleting the express route {0}".format(self.name))
        try:
            response = self.network_client.express_route_circuits.delete(resource_group_name=self.resource_group,
                                                                name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete express route.')
            self.fail(
                "Error deleting the express route : {0}".format(str(e)))

        return True

def main():
    AzureExpressRoute()


if __name__ == '__main__':
    main()