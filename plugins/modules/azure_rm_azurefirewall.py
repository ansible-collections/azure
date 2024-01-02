#!/usr/bin/python
#
# Copyright (c) 2019 Zim Kalinowski, (@zikalino), Jurijs Fadejevs (@needgithubid)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_azurefirewall
version_added: '0.1.2'
short_description: Manage Azure Firewall instance
description:
    - Create, update and delete instance of Azure Firewall.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - The name of the Azure Firewall.
        required: true
        type: str
    location:
        description:
            - Resource location.
        type: str
    application_rule_collections:
        description:
            - Collection of application rule collections used by Azure Firewall.
        type: list
        elements: dict
        suboptions:
            priority:
                description:
                    - Priority of the application rule collection resource.
                type: int
            action:
                description:
                    - The action type of a rule collection.
                choices:
                    - allow
                    - deny
                type: str
            rules:
                description:
                    - Collection of rules used by a application rule collection.
                type: list
                elements: raw
                suboptions:
                    name:
                        description:
                            - Name of the application rule.
                        type: str
                    description:
                        description:
                            - Description of the rule.
                        type: str
                    source_addresses:
                        description:
                            - List of source IP addresses for this rule.
                        type: list
                        elements: str
                    protocols:
                        description:
                            - Array of ApplicationRuleProtocols.
                        elements: dict
                        type: list
                        suboptions:
                            type:
                                description:
                                    - The type of the protocols.
                                type: str
                            port:
                                description:
                                    - The ports of the protocols.
                                type: str
                    target_fqdns:
                        description:
                            - List of FQDNs for this rule.
                        type: list
                        elements: raw
                    fqdn_tags:
                        description:
                            - List of FQDN Tags for this rule.
                        type: list
                        elements: raw
            name:
                description:
                    - Gets name of the resource that is unique within a resource group.
                    - This name can be used to access the resource.
                type: str
    nat_rule_collections:
        description:
            - Collection of NAT rule collections used by Azure Firewall.
        type: list
        elements: dict
        suboptions:
            priority:
                description:
                    - Priority of the NAT rule collection resource.
                type: int
            action:
                description:
                    - The action type of a NAT rule collection
                choices:
                    - snat
                    - dnat
                type: str
            rules:
                description:
                    - Collection of rules used by a NAT rule collection.
                type: list
                elements: dict
                suboptions:
                    name:
                        description:
                            - Name of the NAT rule.
                        type: str
                    description:
                        description:
                            - Description of the rule.
                        type: str
                    source_addresses:
                        description:
                            - List of source IP addresses for this rule.
                        type: list
                        elements: str
                    destination_addresses:
                        description:
                            - List of destination IP addresses for this rule.
                        type: list
                        elements: str
                    destination_ports:
                        description:
                            - List of destination ports.
                        type: list
                        elements: str
                    protocols:
                        description:
                            - Array of AzureFirewallNetworkRuleProtocols applicable to this NAT rule.
                        type: list
                        elements: raw
                    translated_address:
                        description:
                            - The translated address for this NAT rule.
                        type: str
                    translated_port:
                        description:
                            - The translated port for this NAT rule.
                        type: str
            name:
                description:
                    - Gets name of the resource that is unique within a resource group.
                    - This name can be used to access the resource.
                type: str
    network_rule_collections:
        description:
            - Collection of network rule collections used by Azure Firewall.
        type: list
        elements: dict
        suboptions:
            priority:
                description:
                    - Priority of the network rule collection resource.
                type: int
            action:
                description:
                    - The action type of a rule collection.
                type: str
                choices:
                    - allow
                    - deny
            rules:
                description:
                    - Collection of rules used by a network rule collection.
                type: list
                elements: dict
                suboptions:
                    name:
                        description:
                            - Name of the network rule.
                        type: str
                    description:
                        description:
                            - Description of the rule.
                        type: str
                    protocols:
                        description:
                            - Array of AzureFirewallNetworkRuleProtocols.
                        type: list
                        elements: raw
                    source_addresses:
                        description:
                            - List of source IP addresses for this rule.
                        type: list
                        elements: str
                    destination_addresses:
                        description:
                            - List of destination IP addresses.
                        type: list
                        elements: str
                    destination_ports:
                        description:
                            - List of destination ports.
                        type: list
                        elements: str
            name:
                description:
                    - Gets name of the resource that is unique within a resource group.
                    - This name can be used to access the resource.
                type: str
    ip_configurations:
        description:
            - IP configuration of the Azure Firewall resource.
        type: list
        elements: dict
        suboptions:
            subnet:
                description:
                    - Existing subnet.
                    - It can be a string containing subnet resource ID.
                    - It can be a dictionary containing I(name), I(virtual_network_name) and optionally I(resource_group) .
                type: raw
            public_ip_address:
                description:
                    - Existing public IP address.
                    - It can be a string containing resource ID.
                    - It can be a string containing a name in current resource group.
                    - It can be a dictionary containing I(name) and optionally I(resource_group).
                type: raw
            name:
                description:
                    - Name of the resource that is unique within a resource group.
                    - This name can be used to access the resource.
                type: str
    state:
        description:
            - Assert the state of the AzureFirewall.
            - Use C(present) to create or update an AzureFirewall and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Zim Kalinowski (@zikalino)
    - Jurijs Fadejevs (@needgithubid)

'''

EXAMPLES = '''
- name: Create Azure Firewall
  azure_rm_azurefirewall:
    resource_group: myResourceGroup
    name: myAzureFirewall
    tags:
      key1: value1
    application_rule_collections:
      - priority: 110
        action: deny
        rules:
          - name: rule1
            description: Deny inbound rule
            source_addresses:
              - 216.58.216.164
              - 10.0.0.0/24
            protocols:
              - type: https
                port: '443'
            target_fqdns:
              - www.test.com
        name: apprulecoll
    nat_rule_collections:
      - priority: 112
        action: dnat
        rules:
          - name: DNAT-HTTPS-traffic
            description: D-NAT all outbound web traffic for inspection
            source_addresses:
              - '*'
            destination_addresses:
              - 1.2.3.4
            destination_ports:
              - '443'
            protocols:
              - tcp
            translated_address: 1.2.3.5
            translated_port: '8443'
        name: natrulecoll
    network_rule_collections:
      - priority: 112
        action: deny
        rules:
          - name: L4-traffic
            description: Block traffic based on source IPs and ports
            protocols:
              - tcp
            source_addresses:
              - 192.168.1.1-192.168.1.12
              - 10.1.4.12-10.1.4.255
            destination_addresses:
              - '*'
            destination_ports:
              - 443-444
              - '8443'
        name: netrulecoll
    ip_configurations:
      - subnet: >-
          /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup
          /providers/Microsoft.Network/virtualNetworks/myVirtualNetwork
          /subnets/AzureFirewallSubnet
        public_ip_address: >-
          /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup
          /providers/Microsoft.Network/publicIPAddresses/
          myPublicIpAddress
        name: azureFirewallIpConfiguration
- name: Delete Azure Firewall
  azure_rm_azurefirewall:
    resource_group: myResourceGroup
    name: myAzureFirewall
    state: absent
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/azureFirewalls/myAzureFirewall
'''

import time
import json
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMAzureFirewalls(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
            ),
            application_rule_collections=dict(
                type='list',
                elements='dict',
                options=dict(
                    priority=dict(
                        type='int',
                    ),
                    action=dict(
                        type='str',
                        choices=['allow',
                                 'deny'],
                    ),
                    rules=dict(
                        type='list',
                        elements='raw',
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            description=dict(
                                type='str'
                            ),
                            source_addresses=dict(
                                type='list',
                                elements='str',
                            ),
                            protocols=dict(
                                type='list',
                                elements='dict',
                                options=dict(
                                    type=dict(
                                        type='str',
                                    ),
                                    port=dict(
                                        type='str'
                                    )
                                )
                            ),
                            target_fqdns=dict(
                                type='list',
                                elements='raw',
                            ),
                            fqdn_tags=dict(
                                type='list',
                                elements='raw',
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            nat_rule_collections=dict(
                type='list',
                elements='dict',
                options=dict(
                    priority=dict(
                        type='int',
                    ),
                    action=dict(
                        type='str',
                        choices=['snat',
                                 'dnat'],
                    ),
                    rules=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            description=dict(
                                type='str'
                            ),
                            source_addresses=dict(
                                type='list',
                                elements='str',
                            ),
                            destination_addresses=dict(
                                type='list',
                                elements='str',
                            ),
                            destination_ports=dict(
                                type='list',
                                elements='str',
                            ),
                            protocols=dict(
                                type='list',
                                elements='raw'
                            ),
                            translated_address=dict(
                                type='str',
                            ),
                            translated_port=dict(
                                type='str',
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            network_rule_collections=dict(
                type='list',
                elements='dict',
                options=dict(
                    priority=dict(
                        type='int',
                    ),
                    action=dict(
                        type='str',
                        choices=['allow',
                                 'deny'],
                    ),
                    rules=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            description=dict(
                                type='str'
                            ),
                            protocols=dict(
                                type='list',
                                elements='raw'
                            ),
                            source_addresses=dict(
                                type='list',
                                elements='str',
                            ),
                            destination_addresses=dict(
                                type='list',
                                elements='str',
                            ),
                            destination_ports=dict(
                                type='list',
                                elements='str',
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            ip_configurations=dict(
                type='list',
                elements='dict',
                options=dict(
                    subnet=dict(
                        type='raw',
                    ),
                    public_ip_address=dict(
                        type='raw',
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.body = {}
        self.body['properties'] = {}

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200, 201, 202]
        self.to_do = Actions.NoAction

        self.query_parameters = {}
        self.query_parameters['api-version'] = '2018-11-01'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(AzureRMAzureFirewalls, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == 'application_rule_collections':
                    self.body['properties']['applicationRuleCollections'] = []
                    for item in kwargs[key]:
                        app_rule = dict(properties={})
                        if item.get('priority') is not None:
                            app_rule['properties']['priority'] = item['priority']
                        if item.get('action') is not None:
                            app_rule['properties']['action'] = dict(type=item['action'])
                        if item.get('name') is not None:
                            app_rule['name'] = item['name']
                        if item.get('rules') is not None:
                            app_rule['properties']['rules'] = []
                            for value in item['rules']:
                                rule_value = {}
                                if value.get('name') is not None:
                                    rule_value['name'] = value['name']
                                if value.get('description') is not None:
                                    rule_value['description'] = value['description']
                                if value.get('source_addresses') is not None:
                                    rule_value['sourceAddresses'] = value.get('source_addresses')
                                if value.get('target_fqdns') is not None:
                                    rule_value['targetFqdns'] = value.get('target_fqdns')
                                if value.get('fqdn_tags') is not None:
                                    rule_value['fqdnTags'] = value.get('fqdn_tags')
                                if value.get('protocols') is not None:
                                    rule_value['protocols'] = []
                                    for pp in value['protocols']:
                                        pro = {}
                                        if pp.get('type') is not None:
                                            pro['protocolType'] = pp.get('type')
                                        if pp.get('port') is not None:
                                            pro['port'] = pp.get('port')
                                        rule_value['protocols'].append(pro)
                                app_rule['properties']['rules'].append(rule_value)
                        self.body['properties']['applicationRuleCollections'].append(app_rule)
                elif key == 'nat_rule_collections':
                    self.body['properties']['natRuleCollections'] = []
                    for item in kwargs[key]:
                        nat_rule = dict(properties={})
                        if item.get('priority') is not None:
                            nat_rule['properties']['priority'] = item['priority']
                        if item.get('action') is not None:
                            nat_rule['properties']['action'] = dict(type=item['action'])
                        if item.get('name') is not None:
                            nat_rule['name'] = item['name']
                        if item.get('rules') is not None:
                            nat_rule['properties']['rules'] = []
                            for value in item['rules']:
                                nat_value = {}
                                if value.get('name') is not None:
                                    nat_value['name'] = value.get('name')
                                if value.get('description') is not None:
                                    nat_value['description'] = value.get('description')
                                if value.get('source_addresses') is not None:
                                    nat_value['sourceAddresses'] = value.get('source_addresses')
                                if value.get('destination_addresses') is not None:
                                    nat_value['destinationAddresses'] = value.get('destination_addresses')
                                if value.get('destination_ports') is not None:
                                    nat_value['destinationPorts'] = value.get('destination_ports')
                                if value.get('protocols') is not None:
                                    nat_value['protocols'] = value.get('protocols')
                                if value.get('translated_address') is not None:
                                    nat_value['translatedAddress'] = value.get('translated_address')
                                if value.get('translated_port') is not None:
                                    nat_value['translatedPort'] = value.get('translated_port')
                                nat_rule['properties']['rules'].append(nat_value)
                        self.body['properties']['natRuleCollections'].append(nat_rule)
                elif key == 'network_rule_collections':
                    self.body['properties']['networkRuleCollections'] = []
                    for item in kwargs[key]:
                        network_rule = dict(properties={})
                        if item.get('priority') is not None:
                            network_rule['properties']['priority'] = item['priority']
                        if item.get('action') is not None:
                            network_rule['properties']['action'] = dict(type=item['action'])
                        if item.get('name') is not None:
                            network_rule['name'] = item['name']
                        if item.get('rules') is not None:
                            network_rule['properties']['rules'] = []
                            for value in item['rules']:
                                net_value = {}
                                if value.get('name') is not None:
                                    net_value['name'] = value.get('name')
                                if value.get('description') is not None:
                                    net_value['description'] = value.get('description')
                                if value.get('source_addresses') is not None:
                                    net_value['sourceAddresses'] = value.get('source_addresses')
                                if value.get('destination_addresses') is not None:
                                    net_value['destinationAddresses'] = value.get('destination_addresses')
                                if value.get('destination_ports') is not None:
                                    net_value['destinationPorts'] = value.get('destination_ports')
                                if value.get('protocols') is not None:
                                    net_value['protocols'] = value.get('protocols')
                                network_rule['properties']['rules'].append(net_value)
                        self.body['properties']['networkRuleCollections'].append(network_rule)
                elif key == 'ip_configurations':
                    self.body['properties']['ipConfigurations'] = []
                    for item in kwargs[key]:
                        ipconfig = dict(properties={})
                        if item.get('subnet') is not None:
                            ipconfig['properties']['subnet'] = {}
                            if isinstance(item['subnet'], str):
                                ipconfig['properties']['subnet']['id'] = item['subnet']
                            elif isinstance(item['subnet'], dict):
                                if item['subnet'].get('id') is not None:
                                    ipconfig['properties']['subnet']['id'] = item['subnet'].get('id')
                                elif (item['subnet'].get('resource_group') is not None and item['subnet'].get('name') is not None and
                                      item['subnet'].get('virtual_network_name') is not None):
                                    ipconfig['properties']['subnet']['id'] = ('/subscriptions/' +
                                                                              self.subscription_id +
                                                                              '/resourceGroups/' +
                                                                              item['subnet'].get('resource_group') +
                                                                              '/providers/Microsoft.Network/virtualNetworks/' +
                                                                              item['subnet'].get('virtual_network_name') +
                                                                              '/subnets/' +
                                                                              item['subnet'].get('name'))
                                elif item['subnet'].get('name') is not None and item['subnet'].get('virtual_network_name') is not None:
                                    ipconfig['properties']['subnet']['id'] = ('/subscriptions/' +
                                                                              self.subscription_id +
                                                                              '/resourceGroups/' +
                                                                              self.resource_group +
                                                                              '/providers/Microsoft.Network/virtualNetworks/' +
                                                                              item['subnet'].get('virtual_network_name') +
                                                                              '/subnets/' +
                                                                              item['subnet'].get('name'))
                                else:
                                    self.fail("The ip_configuration's subnet config error")
                            else:
                                self.fail("The ip_configuration's subnet config error")
                        if item.get('public_ip_address') is not None:
                            ipconfig['properties']['publicIPAddress'] = {}
                            if isinstance(item.get('public_ip_address'), str):
                                ipconfig['properties']['publicIPAddress']['id'] = item.get('public_ip_address')
                            elif isinstance(item.get('public_ip_address'), dict):
                                if item['public_ip_address'].get('id') is not None:
                                    ipconfig['properties']['publicIPAddress']['id'] = item['public_ip_address'].get('id')
                                elif item['public_ip_address'].get('resource_group') is not None and item['public_ip_address'].get('name') is not None:
                                    ipconfig['properties']['publicIPAddress']['id'] = ('/subscriptions/' +
                                                                                       self.subscription_id +
                                                                                       '/resourceGroups/' +
                                                                                       item['public_ip_address'].get('resource_group') +
                                                                                       '/providers/Microsoft.Network/publicIPAddresses/' +
                                                                                       item['public_ip_address'].get('name'))
                                elif item['public_ip_address'].get('name') is not None:
                                    ipconfig['properties']['publicIPAddress']['id'] = ('/subscriptions/' +
                                                                                       self.subscription_id +
                                                                                       '/resourceGroups/' +
                                                                                       self.resource_group +
                                                                                       '/providers/Microsoft.Network/publicIPAddresses/' +
                                                                                       item['public_ip_address'].get('name'))
                                else:
                                    self.fail("The ip_configuration's public ip address config error")
                            else:
                                self.fail("The ip_configuration's public ip address config error")

                        if item.get('name') is not None:
                            ipconfig['name'] = item['name']
                        self.body['properties']['ipConfigurations'].append(ipconfig)
                else:
                    self.body[key] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if 'location' not in self.body:
            self.body['location'] = resource_group.location

        self.url = ('/subscriptions' +
                    '/' + self.subscription_id +
                    '/resourceGroups' +
                    '/' + self.resource_group +
                    '/providers' +
                    '/Microsoft.Network' +
                    '/azureFirewalls' +
                    '/' + self.name)

        old_response = self.get_resource()

        if not old_response:
            self.log("AzureFirewall instance doesn't exist")

            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log('AzureFirewall instance already exists')

            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                update_tags, new_tags = self.update_tags(old_response.get('tags'))
                if update_tags:
                    self.to_do = Actions.Update
                    self.body['tags'] = new_tags

                if not self.default_compare({}, self.body, old_response, '', dict(compare=[])):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log('Need to Create / Update the AzureFirewall instance')

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_resource()

            # if not old_response:
            self.results['changed'] = True
            # else:
            #     self.results['changed'] = old_response.__ne__(response)
            self.log('Creation / Update done')
        elif self.to_do == Actions.Delete:
            self.log('AzureFirewall instance deleted')
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_resource()

            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_resource():
                time.sleep(20)
        else:
            self.log('AzureFirewall instance unchanged')
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]
            while response['properties']['provisioningState'] == 'Updating':
                time.sleep(30)
                response = self.get_resource()

        return self.results

    def create_update_resource(self):
        # self.log('Creating / Updating the AzureFirewall instance {0}'.format(self.))

        try:
            response = self.mgmt_client.query(self.url,
                                              'PUT',
                                              self.query_parameters,
                                              self.header_parameters,
                                              self.body,
                                              self.status_code,
                                              600,
                                              30)
        except Exception as exc:
            self.log('Error attempting to create the AzureFirewall instance.')
            self.fail('Error creating the AzureFirewall instance: {0}'.format(str(exc)))

        if hasattr(response, 'body'):
            response = json.loads(response.body())
        elif hasattr(response, 'context'):
            response = response.context['deserialized_data']
        else:
            self.fail("Create or Updating fail, no match message return, return info as {0}".format(response))

        return response

    def delete_resource(self):
        # self.log('Deleting the AzureFirewall instance {0}'.format(self.))
        try:
            response = self.mgmt_client.query(self.url,
                                              'DELETE',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
        except Exception as e:
            self.log('Error attempting to delete the AzureFirewall instance.')
            self.fail('Error deleting the AzureFirewall instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        # self.log('Checking if the AzureFirewall instance {0} is present'.format(self.))
        found = False
        try:
            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            response = json.loads(response.body())
            found = True
            self.log("Response : {0}".format(response))
            # self.log("AzureFirewall instance : {0} found".format(response.name))
        except Exception as e:
            self.log('Did not find the AzureFirewall instance.')
        if found is True:
            return response

        return False


def main():
    AzureRMAzureFirewalls()


if __name__ == '__main__':
    main()
