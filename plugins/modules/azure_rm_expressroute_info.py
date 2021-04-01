#!/usr/bin/python
#
# Copyright (c) 2020 Sakar Mehra (@sakar97), Praveen Ghuge (@praveenghuge), Karl Dasan (@karldas30)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_expressroute_info
short_description: Get Azure Express Route facts
description:
    - Get facts of Azure Express Route.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    express_route_name:
        description:
            - The name of the express route.
        required: True


extends_documentation_fragment:
- azure.azcollection.azure


author:
    - Praveen Ghuge (@praveenghuge)
    - Karl Dasan (@ikarldas30)
    - Sakar Mehra (@sakar97)

'''


EXAMPLES = '''
  - name: Get facts of specific expressroute
    community.azure.azure_rm_expressroute_info:
      resource_group: myResourceGroup
      express_route_name: myExpressRoute

'''

RETURN = '''
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

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
            express_route_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.express_route_name = None

        super(AzureExpressRouteInfo, self).__init__(self.module_arg_spec, supports_tags=False)


    def exec_module(self, **kwargs):
        is_old_facts = self.module._name == 'azure_expressroute_facts'
        if is_old_facts:
            self.module.deprecate("The 'azure_expressroute_facts' module has been renamed to 'azure_expressroute_info'",
                                  version='3.0.0', collection_name='community.azure')  # was 2.13

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results['subnets'] = self.get()
        else:
            self.results['subnets'] = self.list()

        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.network_client.express_route_circuits.get(resource_group_name=self.resource_group,
                                                       circuit_name=self.express_route_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.fail('Could not get facts for Subnet.')

        if response is not None:
            results.append(self.format_response(response))

        return results

def main():
    AzureExpressRouteInfo()


if __name__ == '__main__':
    main()
