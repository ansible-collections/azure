#!/usr/bin/python
#
# Copyright (c) 2019 Liu Qingyi, (@smile37773)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_azurefirewall_info
version_added: '0.1.2'
short_description: Get AzureFirewall info
description:
    - Get info of AzureFirewall.
options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
    name:
        description:
            - Resource name.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Liu Qingyi (@smile37773)

'''

EXAMPLES = '''
- name: List all Azure Firewalls for a given subscription
  azure_rm_azurefirewall_info:
- name: List all Azure Firewalls for a given resource group
  azure_rm_azurefirewall_info:
    resource_group: myResourceGroup
- name: Get Azure Firewall
  azure_rm_azurefirewall_info:
    resource_group: myResourceGroup
    name: myAzureFirewall
'''

RETURN = '''
firewalls:
    description:
        - A list of dict results where the key is the name of the AzureFirewall and the values are the facts for that AzureFirewall.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/
                     myResourceGroup/providers/Microsoft.Network/azureFirewalls/myAzureFirewall"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: "myAzureFirewall"
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: "eastus"
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: { "tag": "value" }
        etag:
            description:
                - Gets a unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        application_rule_collections:
            description:
                - Collection of application rule collections used by Azure Firewall.
            type: list
            returned: always
            sample: [
                {
                    "etag": "25b7fca4-c909-4913-8799-6cdb7da2e298",
                    "id": "/subscriptions/xxx-xxx1/resourceGroups/myResourceGroup/providers/
                           Microsoft.Network/azureFirewalls/myFirewall/applicationRuleCollections/apprulecoll",
                    "name": "apprulecoll",
                    "properties": {
                        "action": {
                            "type": "Deny"
                        },
                        "priority": 110,
                        "provisioningState": "Failed",
                        "rules": [
                            {
                                "actions": [],
                                "description": "Deny inbound rule",
                                "direction": "Inbound",
                                "fqdnTags": [],
                                "name": "rule1",
                                "priority": 0,
                                "protocols": [
                                    {
                                        "port": 443,
                                        "protocolType": "Https"
                                    }
                                ],
                                "sourceAddresses": [
                                    "216.58.216.164",
                                    "10.0.0.0/25"
                                ],
                                "sourceIpGroups": [],
                                "targetFqdns": [
                                    "www.test.com"
                                ]
                            }
                        ]
                    },
                    "type": "Microsoft.Network/azureFirewalls/applicationRuleCollections"
                }
            ]
        nat_rule_collections:
            description:
                - Collection of NAT rule collections used by Azure Firewall.
            type: list
            returned: always
            sample: [
                {
                    "etag": '3759e8b1-cdf7-44f4-a643-3a75e2b67877',
                    "id": "/subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/
                           azureFirewalls/myFirewall/natRuleCollections/natrulecoll",
                    "name": "natrulecoll",
                    "properties": {
                        "action": {
                            "type": "Dnat"
                        },
                        "priority": 112,
                        "provisioningState": "Failed",
                        "rules": [
                            {
                                "description": "D-NAT all outbound web traffic for inspection",
                                "destinationAddresses": [
                                    "20.169.156.124"
                                ],
                                "destinationPorts": [
                                    "443"
                                ],
                                "name": "DNAT-HTTPS-traffic",
                                "protocols": [
                                    "TCP"
                                ],
                                "sourceAddresses": [
                                    "*"
                                ],
                                "translatedAddress": "1.2.3.5",
                                "translatedPort": "8443"
                            }
                        ]
                    },
                    "type": "Microsoft.Network/azureFirewalls/natRuleCollections"
                }
            ]
        network_rule_collections:
            description:
                - Collection of network rule collections used by Azure Firewall.
            type: list
            returned: always
            sample: [
                {
                    "etag": "3759e8b1-cdf7-44f4-a643-3a75e2b67877",
                    "id": "/subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/
                           azureFirewalls/myFirewall/networkRuleCollections/netrulecoll",
                    "name": "netrulecoll",
                    "properties": {
                        "action": {
                            "type": "Deny"
                        },
                        "priority": 112,
                        "provisioningState": "Failed",
                        "rules": [
                            {
                                "description": "Block traffic based on source IPs and ports",
                                "destinationAddresses": [
                                    "*"
                                ],
                                "destinationPorts": [
                                    "443-444",
                                    "8443"
                                ],
                                "name": "L4-traffic",
                                "protocols": [
                                    "TCP"
                                ],
                                "sourceAddresses": [
                                    "192.168.1.1-192.168.1.12",
                                    "10.1.4.12-10.1.4.255"
                                ]
                            },
                            {
                                "description": "Block traffic based on source IPs and ports to amazon",
                                "destinationAddresses": [],
                                "destinationPorts": [
                                    "443-444",
                                    "8443"
                                ],
                                "name": "L4-traffic-with_FQDN",
                                "protocols": [
                                    "TCP"
                                ],
                                "sourceAddresses": [
                                    "10.2.4.12-10.2.4.255"
                                ]
                            }
                        ]
                    },
                    "type": "Microsoft.Network/azureFirewalls/networkRuleCollections"
                }
            ]
        ip_configurations:
            description:
                - IP configuration of the Azure Firewall resource.
            type: list
            returned: always
            sample: [
                {
                    "etag": "3759e8b1-cdf7-44f4-a643-3a75e2b67877",
                    "id": "/subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/azureFirewalls/myFirewall/i
                           azureFirewallIpConfigurations/azureFirewallIpConfiguration",
                    "name": "azureFirewallIpConfiguration",
                    "properties": {
                        "privateIPAllocationMethod": "Dynamic",
                        "provisioningState": "Succeeded",
                        "publicIPAddress": {
                            "id": "/subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/publicIPAddresses/myPublicIpAddress"
                        },
                        "subnet": {
                            "id": "/subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/
                                   virtualNetworks/myVirtualNetwork/subnets/AzureFirewallSubnet"
                        }
                    },
                    "type": "Microsoft.Network/azureFirewalls/azureFirewallIpConfigurations"
                }
            ]
        provisioning_state:
            description:
                - The current state of the gallery.
            type: str
            sample: "Succeeded"

'''

import json
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient


class AzureRMAzureFirewallsInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            name=dict(
                type='str'
            )
        )

        self.resource_group = None
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        self.query_parameters = {}
        self.query_parameters['api-version'] = '2024-01-01'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        self.mgmt_client = None
        super(AzureRMAzureFirewallsInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and self.name is not None):
            self.results['firewalls'] = self.get()
        elif (self.resource_group is not None):
            self.results['firewalls'] = self.list()
        else:
            self.results['firewalls'] = self.listall()
        return self.results

    def get(self):
        response = None
        results = {}
        # prepare url
        self.url = ('/subscriptions' +
                    '/{{ subscription_id }}' +
                    '/resourceGroups' +
                    '/{{ resource_group }}' +
                    '/providers' +
                    '/Microsoft.Network' +
                    '/azureFirewalls' +
                    '/{{ azure_firewall_name }}')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)
        self.url = self.url.replace('{{ resource_group }}', self.resource_group)
        self.url = self.url.replace('{{ azure_firewall_name }}', self.name)

        try:
            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            results = json.loads(response.body())
            # self.log('Response : {0}'.format(response))
        except Exception as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return self.format_item(results)

    def list(self):
        response = None
        results = {}
        # prepare url
        self.url = ('/subscriptions' +
                    '/{{ subscription_id }}' +
                    '/resourceGroups' +
                    '/{{ resource_group }}' +
                    '/providers' +
                    '/Microsoft.Network' +
                    '/azureFirewalls')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)
        self.url = self.url.replace('{{ resource_group }}', self.resource_group)

        try:
            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            results = json.loads(response.body())
            # self.log('Response : {0}'.format(response))
        except Exception as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return [self.format_item(x) for x in results['value']] if results['value'] else []

    def listall(self):
        response = None
        results = {}
        # prepare url
        self.url = ('/subscriptions' +
                    '/{{ subscription_id }}' +
                    '/providers' +
                    '/Microsoft.Network' +
                    '/azureFirewalls')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)

        try:
            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            results = json.loads(response.body())
            # self.log('Response : {0}'.format(response))
        except Exception as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return [self.format_item(x) for x in results['value']] if results['value'] else []

    def format_item(self, item):
        if item is None or item == {}:
            return {}
        d = {
            'id': item.get('id'),
            'name': item.get('name'),
            'location': item.get('location'),
            'etag': item.get('etag'),
            'tags': item.get('tags'),
            'nat_rule_collections': dict(),
            'network_rule_collections': dict(),
            'ip_configurations': dict(),
        }
        if isinstance(item.get('properties'), dict):
            d['nat_rule_collections'] = item.get('properties').get('natRuleCollections')
            d['network_rule_collections'] = item.get('properties').get('networkRuleCollections')
            d['application_rule_collections'] = item.get('properties').get('applicationRuleCollections')
            d['ip_configurations'] = item.get('properties').get('ipConfigurations')
            d['provisioning_state'] = item.get('properties').get('provisioningState')
        return d


def main():
    AzureRMAzureFirewallsInfo()


if __name__ == '__main__':
    main()
