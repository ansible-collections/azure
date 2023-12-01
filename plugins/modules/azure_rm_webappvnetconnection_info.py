#!/usr/bin/python
#
# Copyright (c) 2021 Ross Bender (@l3ender)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_webappvnetconnection_info

version_added: "1.8.0"

short_description: Get Azure web app virtual network connection facts

description:
    - Get facts for a web app's virtual network connection.

options:
    name:
        description:
            - Name of the web app.
        required: true
        type: str
    resource_group:
        description:
            - Resource group of the web app.
        required: true
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Ross Bender (@l3ender)
'''

EXAMPLES = '''
- name: Get web app virtual network connection
  azure_rm_webappvnetconnection_info:
    name: "MyWebapp"
    resource_group: "MyResourceGroup"
'''

RETURN = '''
connection:
    description:
        - The web app's virtual network connection.
    returned: always
    type: complex
    contains:
        id:
            description:
                - ID of the web app virtual network connection.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Web/sites/myWebApp/virtualNetworkConnections/yyy-yyy_subnet
        name:
            description:
                - Name of the web app virtual network connection.
            returned: always
            type: str
            sample: yyy-yyy_subnet
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
            sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/myVnet/subnets/mySubnet
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMWebAppVnetConnectionInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
        )

        self.results = dict(
            changed=False,
            connection=dict(),
        )

        self.name = None
        self.resource_group = None

        super(AzureRMWebAppVnetConnectionInfo, self).__init__(self.module_arg_spec,
                                                              supports_check_mode=True,
                                                              supports_tags=False,
                                                              facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        vnet = self.get_vnet_connection()

        if vnet:
            self.results['connection'] = self.set_results(vnet)

        return self.results

    def get_vnet_connection(self):
        connections = self.list_vnet_connections()
        for connection in connections:
            if connection.is_swift:
                return connection

        return None

    def list_vnet_connections(self):
        try:
            return self.web_client.web_apps.list_vnet_connections(resource_group_name=self.resource_group, name=self.name)
        except Exception as exc:
            self.fail("Error getting webapp vnet connections {0} (rg={1}) - {2}".format(self.name, self.resource_group, str(exc)))

    def set_results(self, vnet):
        vnet_dict = vnet.as_dict()

        output = dict()
        output['id'] = vnet_dict['id']
        output['name'] = vnet_dict['name']
        subnet_id = vnet_dict['vnet_resource_id']
        output['vnet_resource_id'] = subnet_id
        subnet_detail = self.get_subnet_detail(subnet_id)
        output['vnet_resource_group'] = subnet_detail['resource_group']
        output['vnet_name'] = subnet_detail['vnet_name']
        output['subnet_name'] = subnet_detail['subnet_name']

        return output


def main():
    AzureRMWebAppVnetConnectionInfo()


if __name__ == '__main__':
    main()
