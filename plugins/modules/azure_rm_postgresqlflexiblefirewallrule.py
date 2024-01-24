#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexiblefirewallrule
version_added: "2.2.0"
short_description: Manage PostgreSQL flexible firewall rule instance
description:
    - Create, update and delete instance of PostgreSQL flexible firewall rule.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
        type: str
    server_name:
        description:
            - The name of the server.
        required: True
        type: str
    name:
        description:
            - The name of the PostgreSQL flexible firewall rule.
        required: True
        type: str
    start_ip_address:
        description:
            - The start IP address of the PostgreSQL flexible firewall rule. Must be IPv4 format.
        type: str
    end_ip_address:
        description:
            - The end IP address of the PostgreSQL flexible firewall rule. Must be IPv4 format.
        type: str
    state:
        description:
            - Assert the state of the PostgreSQL flexible firewall rule.
            - Use C(present) to create or update a PostgreSQL flexible firewall rule and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Create (or update) PostgreSQL flexible firewall rule
  azure_rm_postgresqlflexiblefirewallrule:
    resource_group: myResourceGroup
    server_name: testserver
    name: rule1
    start_ip_address: 10.0.0.16
    end_ip_address: 10.0.0.18
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
    from azure.core.polling import LROPoller
    import logging
    logging.basicConfig(filename='log.log', level=logging.INFO)
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPostgreSqlFlexibleFirewallRules(AzureRMModuleBase):
    """Configuration class for an Azure RM PostgreSQL flexible firewall rule resource"""

    def __init__(self):
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
                type='str',
                required=True
            ),
            start_ip_address=dict(
                type='str'
            ),
            end_ip_address=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.name = None
        self.start_ip_address = None
        self.end_ip_address = None

        self.results = dict(changed=False)
        self.state = None
        self.parameters = dict()

        super(AzureRMPostgreSqlFlexibleFirewallRules, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                     supports_check_mode=True,
                                                                     supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
                if key in ['start_ip_address', 'end_ip_address']:
                    self.parameters[key] = kwargs[key]

        old_response = None
        response = None
        changed = False

        old_response = self.get_firewallrule()

        if old_response is None:
            self.log("PostgreSQL flexible firewall rule instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                changed = True
                if not self.check_mode:
                    response = self.create_update_firewallrule(self.parameters)
        else:
            self.log("PostgreSQL flexible firewall rule instance already exists")
            if self.state == 'absent':
                changed = True
                if self.check_mode:
                    response = old_response
                else:
                    response = self.delete_firewallrule()
            else:
                self.log("Need to check if PostgreSQL flexible firewall rule instance has to be deleted or may be updated")
                if (self.start_ip_address is not None) and (self.start_ip_address != old_response['start_ip_address']):
                    changed = True
                else:
                    self.parameters['start_ip_address'] = old_response['start_ip_address']
                if (self.end_ip_address is not None) and (self.end_ip_address != old_response['end_ip_address']):
                    changed = True
                else:
                    self.parameters['end_ip_address'] = old_response['end_ip_address']
                if changed:
                    if not self.check_mode:
                        response = self.create_update_firewallrule(self.parameters)
                    else:
                        response = old_response
                else:
                    response = old_response
        self.results['firewall_rule'] = response
        self.results['changed'] = changed

        return self.results

    def create_update_firewallrule(self, body):
        '''
        Creates or updates PostgreSQL flexible firewall rule with the specified configuration.

        :return: deserialized PostgreSQL flexible firewall rule instance state dictionary
        '''
        self.log("Creating / Updating the PostgreSQL flexible firewall rule instance {0}".format(self.name))

        try:
            response = self.postgresql_flexible_client.firewall_rules.begin_create_or_update(resource_group_name=self.resource_group,
                                                                                             server_name=self.server_name,
                                                                                             firewall_rule_name=self.name,
                                                                                             parameters=body)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except Exception as exc:
            self.log('Error attempting to create the PostgreSQL flexible firewall rule instance.')
            self.fail("Error creating the PostgreSQL flexible firewall rule instance: {0}".format(str(exc)))
        return self.format_item(response)

    def delete_firewallrule(self):
        '''
        Deletes specified PostgreSQL flexible firewall rule instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the PostgreSQL flexible firewall rule instance {0}".format(self.name))
        try:
            self.postgresql_flexible_client.firewall_rules.begin_delete(resource_group_name=self.resource_group,
                                                                        server_name=self.server_name,
                                                                        firewall_rule_name=self.name)
        except Exception as e:
            self.log('Error attempting to delete the PostgreSQL flexible firewall rule instance.')
            self.fail("Error deleting the PostgreSQL flexible firewall rule instance: {0}".format(str(e)))

        return True

    def get_firewallrule(self):
        '''
        Gets the properties of the specified PostgreSQL flexible firewall rule.

        :return: deserialized PostgreSQL flexible firewall rule instance state dictionary
        '''
        self.log("Checking if the PostgreSQL flexible firewall rule instance {0} is present".format(self.name))
        try:
            response = self.postgresql_flexible_client.firewall_rules.get(resource_group_name=self.resource_group,
                                                                          server_name=self.server_name,
                                                                          firewall_rule_name=self.name)
            self.log("Response : {0}".format(response))
            self.log("PostgreSQL flexible firewall rule instance : {0} found".format(response.name))
        except ResourceNotFoundError as e:
            self.log('Did not find the PostgreSQL flexible firewall rule instance. Exception as {0}'.format(str(e)))
            return None
        return self.format_item(response)

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
    """Main execution"""
    AzureRMPostgreSqlFlexibleFirewallRules()


if __name__ == '__main__':
    main()
