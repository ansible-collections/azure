#!/usr/bin/python
#
# Copyright (c) 2026 zunyangc (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexibleconfiguration
version_added: "3.18.0"
short_description: Manage Azure PostgreSQL Flexible Configuration
description:
    - Update or reset Azure PostgreSQL Flexible Server Configuration setting.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource.
        required: true
        type: str
    server_name:
        description:
            - The name of the server.
        required: true
        type: str
    name:
        description:
            - Setting name.
        required: true
        type: str
    value:
        description:
            - Setting value.
        type: str
    state:
        description:
            - Assert the state of the PostgreSQL Flexible setting.
            - Use C(present) to update setting, or C(absent) to reset to default value.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - zunyangc (@zunyangc)

'''

EXAMPLES = '''
- name: Update PostgreSQL Flexible Server setting
  azure_rm_postgresqlflexibleconfiguration:
    resource_group: myResourceGroup
    server_name: myServer
    name: deadlock_timeout
    value: 2000

- name: Reset PostgreSQL Flexible Server setting to default
  azure_rm_postgresqlflexibleconfiguration:
    resource_group: myResourceGroup
    server_name: myServer
    name: deadlock_timeout
    state: absent
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.DBforPostgreSQL/flexibleServers/myServer/configurations/deadlock_timeout"
'''

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.mgmt.rdbms.postgresql_flexibleservers.models import Configuration
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMPostgreSqlFlexibleConfigurations(AzureRMModuleBase):

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
            value=dict(
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
        self.value = None

        self.results = dict(changed=False)
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMPostgreSqlFlexibleConfigurations, self).__init__(derived_arg_spec=self.module_arg_spec,
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
            self.log("Configuration instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Configuration instance already exists")
            if self.state == 'absent':
                if str(old_response.get('value')) != str(old_response.get('default_value')):
                    self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Configuration instance has to be updated")
                if self.value is not None and str(self.value) != str(old_response.get('value')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Configuration instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_configuration()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Configuration instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_configuration(old_response.get('default_value'))
        else:
            self.log("Configuration instance unchanged")
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]

        return self.results

    def create_update_configuration(self):
        '''
        Apply the requested value to the PostgreSQL Flexible Server configuration
        setting using ``source='user-override'`` and return the resulting resource as a dict.
        '''
        self.log("Creating / Updating the Configuration instance {0}".format(self.name))

        try:
            response = self.postgresql_flexible_client.configurations.begin_update(resource_group_name=self.resource_group,
                                                                                   server_name=self.server_name,
                                                                                   configuration_name=self.name,
                                                                                   parameters=Configuration(
                                                                                       value=self.value,
                                                                                       source='user-override'
                                                                                   ))
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except Exception as exc:
            self.log('Error attempting to create the Configuration instance.')
            self.fail("Error creating the Configuration instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_configuration(self, default_value):
        '''
        Reset the PostgreSQL Flexible Server configuration setting back to its
        ``default_value``.
        '''
        self.log("Resetting the Configuration instance {0} to default value {1}".format(self.name, default_value))
        try:
            response = self.postgresql_flexible_client.configurations.begin_update(resource_group_name=self.resource_group,
                                                                                   server_name=self.server_name,
                                                                                   configuration_name=self.name,
                                                                                   parameters=Configuration(
                                                                                       value=default_value,
                                                                                       source='user-override'
                                                                                   ))
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except Exception as e:
            self.log('Error attempting to reset the Configuration instance.')
            self.fail("Error resetting the Configuration instance: {0}".format(str(e)))

        return True

    def get_configuration(self):
        '''
        Fetch the current configuration setting from Azure.

        :return: dict representation of the configuration if found, otherwise ``False``.
        '''
        self.log("Checking if the Configuration instance {0} is present".format(self.name))
        found = False
        try:
            response = self.postgresql_flexible_client.configurations.get(resource_group_name=self.resource_group,
                                                                          server_name=self.server_name,
                                                                          configuration_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Configuration instance : {0} found".format(response.name))
        except ResourceNotFoundError as e:
            self.log('Did not find the Configuration instance. Exception: {0}'.format(e))
        if found is True:
            return response.as_dict()

        return False


def main():
    AzureRMPostgreSqlFlexibleConfigurations()


if __name__ == '__main__':
    main()
