#!/usr/bin/python
#
# Copyright (c) 2021 Ross Bender (@l3ender)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_webapp_vnetintegration_info

version_added: "1.9.0"

short_description: Get Azure web app virtual network integration facts

description:
    - Get facts for a web app's virtual network integration.

options:
    name:
        description:
            - Name of the web app.
    resource_group:
        description:
            - Resource group of the web app.

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Ross Bender (@l3ender)
'''

EXAMPLES = '''
    - name: Get web app virtual network integrations
      azure_rm_webapp_vnetintegration_info:
        name: "MyWebapp"
        resource_group: "MyResourceGroup"
'''

RETURN = '''
integrations:
    description:
        - List of the web app's virtual network integrations.
    returned: always
    type: complex
    contains:
        id:
            description:
                - ID of the web app virtual network integration.
            returned: always
            type: str
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Web/sites/myWebApp/virtualNetworkConnections/yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy_subnet
        name:
            description:
                - Name of the web app virtual network integration.
            returned: always
            type: str
            sample: yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy_subnet
        subnet_name:
            description:
               - Name of the subnet connected to the web app.
            returned: always
            type: str
            sample: mySubnet
        vnet_name:
            description:
               - Name of the virtual network connected to the web app.
            returned: always
            type: str
            sample: myVnet
        vnet_resource_group:
            description:
               - Name of the resource group the virtual network is in.
            returned: always
            type: str
            sample: myResourceGroup
        vnet_resource_id:
            description:
               - ID of the virtual network/subnet connected to the web app.
            returned: always
            type: str
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/myVnet/subnets/mySubnet
'''
try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from azure.common import AzureMissingResourceHttpError, AzureHttpError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
try:
    import xmltodict
except Exception:
    pass

AZURE_OBJECT_CLASS = 'WebApp'


class AzureRMWebAppVnetIntegrationInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
        )

        self.results = dict(
            changed=False,
            integrations=[],
        )

        self.name = None
        self.resource_group = None

        super(AzureRMWebAppVnetIntegrationInfo, self).__init__(self.module_arg_spec,
                                                supports_tags=False,
                                                facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        try:
            vnets = self.web_client.web_apps.list_vnet_connections(resource_group_name=self.resource_group, name=self.name)

            self.results['integrations'] = [self.set_results(vnet) for vnet in vnets]
        except CloudError:
            pass

        return self.results

    def set_results(self, vnet):
        vnet_dict = vnet.as_dict()

        output = dict()
        output['id'] = vnet_dict['id']
        output['name'] = vnet_dict['name']
        output['vnet_resource_id'] = vnet_dict['vnet_resource_id']
        output['vnet_resource_group'] = vnet_dict['vnet_resource_id'].split('resourceGroups/')[1].split('/')[0]
        vnet_detail = vnet_dict['vnet_resource_id'].split('/Microsoft.Network/virtualNetworks/')[1].split('/subnets/')
        output['vnet_name'] = vnet_detail[0]
        output['subnet_name'] = vnet_detail[1]

        return output


def main():
    AzureRMWebAppVnetIntegrationInfo()


if __name__ == '__main__':
    main()
