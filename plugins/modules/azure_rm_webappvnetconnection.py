#!/usr/bin/python
#
# Copyright (c) 2021 Ross Bender (@l3ender)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_webappvnetconnection
version_added: "1.8.0"
short_description: Manage web app virtual network connection
description:
    - Add, remove, or update the virtual network connection for a web app.
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
    state:
        description:
            - State of the virtual network connection. Use C(present) to create or update and C(absent) to delete.
        type: str
        default: present
        choices:
            - absent
            - present
    vnet_name:
        description:
            - Name of the virtual network. Required if adding or updating.
        type: str
    subnet:
        description:
            - Name of the virtual network's subnet. Required if adding or updating.
        type: str
    vnet_resource_group:
        description:
            - Name of the resource group for the virtual network. Defaults to main C(resource_group) value.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Ross Bender (@l3ender)
'''

EXAMPLES = '''
    - name: Configure web app with virtual network
      azure.azcollection.azure_rm_webappvnetconnection:
        name: "MyWebapp"
        resource_group: "MyResourceGroup"
        vnet_name: "MyVnetName"
        subnet: "MySubnetName"

    - name: Configure web app with virtual network in different resource group
      azure.azcollection.azure_rm_webappvnetconnection:
        name: "MyWebapp"
        resource_group: "MyResourceGroup"
        vnet_name: "MyVnetName"
        subnet: "MySubnetName"
        vnet_resource_group: "MyOtherResourceGroup"

    - name: Delete web app virtual network
      azure.azcollection.azure_rm_webappvnetconnection:
        name: "MyWebapp"
        resource_group: "MyResourceGroup"
        state: "absent"
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

try:
    from azure.mgmt.web.models import SwiftVirtualNetwork
except Exception:
    # This is handled in azure_rm_common
    pass


class AzureRMWebAppVnetConnection(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            vnet_name=dict(type='str'),
            subnet=dict(type='str'),
            vnet_resource_group=dict(type='str'),
        )

        self.results = dict(
            changed=False,
            connection=dict(),
        )

        self.state = None
        self.name = None
        self.resource_group = None
        self.vnet_name = None
        self.subnet = None
        self.vnet_resource_group = None

        super(AzureRMWebAppVnetConnection, self).__init__(self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        changed = False
        vnet = self.get_vnet_connection()
        if vnet:
            self.results['connection'] = self.set_results(vnet)

        if self.state == 'absent' and vnet:
            changed = True
            if not self.check_mode:
                self.log('Deleting vnet connection for webapp {0}'.format(self.name))
                self.delete_vnet_connection()
                self.results['connection'] = dict()
        elif self.state == 'present':
            self.vnet_resource_group = self.vnet_resource_group or self.resource_group

            if not vnet:
                self.log('Adding vnet connection for webapp {0}'.format(self.name))
                changed = True
            else:
                subnet_detail = self.get_subnet_detail(vnet.vnet_resource_id)
                if (subnet_detail['resource_group'] != self.vnet_resource_group
                        or subnet_detail['vnet_name'] != self.vnet_name
                        or subnet_detail['subnet_name'] != self.subnet):
                    self.log('Detected change in vnet connection for webapp {0}'.format(self.name))
                    changed = True

            if changed:
                if not self.check_mode:
                    self.log('Updating vnet connection for webapp {0}'.format(self.name))
                    subnet = self.get_subnet()
                    param = SwiftVirtualNetwork(subnet_resource_id=subnet.id)
                    self.create_or_update_vnet_connection(param)
                    vnet = self.get_vnet_connection()
                    self.results['connection'] = self.set_results(vnet)

        self.results['changed'] = changed
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

    def delete_vnet_connection(self):
        try:
            return self.web_client.web_apps.delete_swift_virtual_network(resource_group_name=self.resource_group, name=self.name)
        except Exception as exc:
            self.fail("Error deleting webapp vnet connection {0} (rg={1}) - {3}".format(self.name, self.resource_group, str(exc)))

    def create_or_update_vnet_connection(self, vnet):
        try:
            return self.web_client.web_apps.create_or_update_swift_virtual_network_connection(
                resource_group_name=self.resource_group, name=self.name, connection_envelope=vnet)
        except Exception as exc:
            self.fail("Error creating/updating webapp vnet connection {0} (vnet={1}, rg={2}) - {3}".format(
                self.name, self.vnet_name, self.resource_group, str(exc)))

    def get_subnet(self):
        try:
            return self.network_client.subnets.get(resource_group_name=self.vnet_resource_group, virtual_network_name=self.vnet_name, subnet_name=self.subnet)
        except Exception as exc:
            self.fail("Error getting subnet {0} in vnet={1} (rg={2}) - {3}".format(self.subnet, self.vnet_name, self.vnet_resource_group, str(exc)))

    def set_results(self, vnet):
        vnet_dict = vnet.as_dict()

        output = dict()
        output['id'] = vnet_dict['id']
        output['name'] = vnet_dict['name']
        subnet_id = vnet_dict.get('subnet_resource_id', vnet_dict.get('vnet_resource_id'))
        output['vnet_resource_id'] = subnet_id
        subnet_detail = self.get_subnet_detail(subnet_id)
        output['vnet_resource_group'] = subnet_detail['resource_group']
        output['vnet_name'] = subnet_detail['vnet_name']
        output['subnet_name'] = subnet_detail['subnet_name']

        return output


def main():
    AzureRMWebAppVnetConnection()


if __name__ == '__main__':
    main()
