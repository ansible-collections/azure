#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_mysqlflexibleconfiguration
version_added: "2.7.0"
short_description: Manage Configuration instance
description:
    - Update or delete instance of Flexible Configuration.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource.
        required: True
        type: str
    server_name:
        description:
            - The name of the server.
        required: True
        type: str
    name:
        description:
            - The name of the server configuration.
        required: True
        type: str
    value:
        description:
            - The value server configurations.
        type: str
    source:
        description:
            - Source of the configuration.
        type: str
        choices:
            - system-default
            - user-override
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Update SQL Server setting
  azure_rm_mysqlflexibleconfiguration:
    resource_group: myResourceGroup
    server_name: myServer
    name: event_scheduler
    value:
      - name: testvalue
        value: "ON"
        source: system-default
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/xx-xx/resourceGroups/myRG/providers/Microsoft.DBforMySQL/flexibleservers/myServer/configurations/event_scheduler"
server_name:
    description:
        - The MySQL flexible server name.
    type: str
    returned: always
    sample: testmysqlserver
name:
    description:
        - Setting name.
    returned: always
    type: str
    sample: deadlock_timeout
value:
    description:
        - Setting value.
    returned: always
    type: raw
    sample: 1000
source:
    description:
        - Source of the configuration.
    returned: always
    type: str
    sample: system-default
'''

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Update = range(2)


class AzureRMMySqlFlexibleConfiguration(AzureRMModuleBase):

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
            value=dict(type='str'),
            source=dict(type='str', choices=['system-default', 'user-override']),
        )

        self.resource_group = None
        self.server_name = None
        self.name = None
        self.value = None
        self.source = None

        self.results = dict(changed=False)
        self.to_do = Actions.NoAction

        super(AzureRMMySqlFlexibleConfiguration, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                supports_check_mode=True,
                                                                supports_tags=False)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        old_response = self.get_configuration()

        if not old_response:
            self.fail("The MySQL configuration not exist, We can't make any changes")
        else:
            self.log("Need to check if Configuration instance has to be deleted or may be updated")
            if self.value is not None and self.value != old_response['value'] or self.source is not None and self.source != old_response['source']:
                self.to_do = Actions.Update

        if self.to_do == Actions.Update:
            self.log("Need to Update the Configuration instance")
            if not self.check_mode:
                response = self.update_configuration()
                self.results['changed'] = True
                self.log("Update done")
        response = self.get_configuration()

        if response:
            self.results["id"] = response["id"]
            self.results['resource_group'] = self.resource_group
            self.results['server_name'] = self.server_name
            self.results['name'] = self.name
            self.results['source'] = response['source']
            self.results['value'] = response['value']

        return self.results

    def update_configuration(self):
        self.log("Updating the Configuration instance {0}".format(self.name))

        try:
            response = self.mysql_flexible_client.configurations.begin_update(resource_group_name=self.resource_group,
                                                                              server_name=self.server_name,
                                                                              configuration_name=self.name,
                                                                              parameters={'value': self.value, 'source': self.source})
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except Exception as exc:
            self.log('Error attempting to create the Configuration instance.')
            self.fail("Error creating the Configuration instance: {0}".format(str(exc)))
        return response.as_dict()

    def get_configuration(self):
        self.log("Checking if the Configuration instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mysql_flexible_client.configurations.get(resource_group_name=self.resource_group,
                                                                     server_name=self.server_name,
                                                                     configuration_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Configuration instance : {0} found".format(response.name))
        except ResourceNotFoundError as e:
            self.log('Did not find the Configuration instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMMySqlFlexibleConfiguration()


if __name__ == '__main__':
    main()
