#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexiblefirewallrule_info
version_added: "2.2.0"
short_description: Get Azure PostgreSQL Flexible Firewall Rule facts
description:
    - Get facts of Azure PostgreSQL Flexible Firewall Rule.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
        type: str
    server_name:
        description:
            - The name of the server.
        required: True
        type: str
    name:
        description:
            - The name of the server firewall rule.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Get instance of PostgreSQL Flexible Firewall Rule
  azure_rm_postgresqlflexiblefirewallrule_info:
    resource_group: myResourceGroup
    server_name: server_name
    name: firewall_rule_name

- name: List instances of PostgreSQL Flexible Firewall Rule
  azure_rm_postgresqlflexiblefirewallrule_info:
    resource_group: myResourceGroup
    server_name: server_name
'''

RETURN = '''
rules:
    description:
        - A list of dictionaries containing facts for PostgreSQL Flexible Firewall Rule.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.DBforPostgreSQL/flexibleServers/flexibled9b/firewallRules/firewalld9b"
        server_name:
            description:
                - The name of the server.
            returned: always
            type: str
            sample: testserver
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: rule1
        start_ip_address:
            description:
                - The start IP address of the PostgreSQL firewall rule.
            returned: always
            type: str
            sample: 10.0.0.16
        end_ip_address:
            description:
                - The end IP address of the PostgreSQL firewall rule.
            returned: always
            type: str
            sample: 10.0.0.18
'''

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPostgreSQLFlexibleFirewallRulesInfo(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.server_name = None
        self.name = None
        super(AzureRMPostgreSQLFlexibleFirewallRulesInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results['firewall_rules'] = self.get()
        else:
            self.results['firewall_rules'] = self.list_by_server()
        return self.results

    def get(self):
        response = None
        try:
            response = self.postgresql_flexible_client.firewall_rules.get(resource_group_name=self.resource_group,
                                                                          server_name=self.server_name,
                                                                          firewall_rule_name=self.name)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError as e:
            self.log('Could not get facts for FirewallRules. Exception as {0}'.format(str(e)))
            return []

        return [self.format_item(response)]

    def list_by_server(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.firewall_rules.list_by_server(resource_group_name=self.resource_group,
                                                                                     server_name=self.server_name)
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.log('Could not get facts for FirewallRules. Exception as {0}'.format(str(e)))
            return []

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d['id'],
            'server_name': self.server_name,
            'name': d['name'],
            'start_ip_address': d['start_ip_address'],
            'end_ip_address': d['end_ip_address']
        }
        return d


def main():
    AzureRMPostgreSQLFlexibleFirewallRulesInfo()


if __name__ == '__main__':
    main()
