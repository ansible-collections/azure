#!/usr/bin/python
#
# Copyright (c) 2017 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_sqlserver
version_added: "0.1.2"
short_description: Manage SQL Server instance
description:
    - Create, update and delete instance of SQL Server.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    name:
        description:
            - The name of the server.
        required: True
    location:
        description:
            - Resource location.
    admin_username:
        description:
            - Username of the SQL administrator account for server. Once created it cannot be changed.
    admin_password:
        description:
            - Password of the SQL administrator account for server (required for server creation).
    version:
        description:
            - The version of the server. For example C(12.0).
    identity:
        description:
            - The identity type. Set this to C(SystemAssigned) in order to automatically create and assign an Azure Active Directory principal for the resource.
            - Possible values include C(SystemAssigned).
    minimal_tls_version:
        description:
            - Require clients to use a specified TLS version.
        type: str
        choices:
            - '1.0'
            - '1.1'
            - '1.2'
        version_added: "1.11.0"
    public_network_access:
        description:
            - Whether or not public endpoint access is allowed for the server.
        type: str
        choices:
            - Enabled
            - Disabled
        version_added: "1.11.0"
    restrict_outbound_network_access:
        description:
            - Whether or not to restrict outbound network access for this server.
        type: str
        choices:
            - Enabled
            - Disabled
        version_added: "1.11.0"
    change_admin_password:
        description:
            - Whether or not the c(admin_password) should be updated for an existing server. If true, the password is the only value which will be updated.
        type: bool
        default: false
        version_added: "1.11.0"
    administrators:
        description:
            - The Azure Active Directory identity of the server.
        type: dict
        suboptions:
            administrator_type:
                description:
                    - Type of the Azure AD administrator.
                type: str
                default: ActiveDirectory
            principal_type:
                description:
                    - Principal Type of the Azure AD administrator.
                type: str
                choices:
                    - User
                    - Group
                    - Application
            login:
                description:
                    - Login name of the Azure AD administrator.
                type: str
            sid:
                description:
                    - SID (object ID) of the Azure AD administrator.
                type: str
            tenant_id:
                description:
                    - Tenant ID of the Azure AD administrator.
                type: str
            azure_ad_only_authentication:
                description:
                    - Azure AD only authentication enabled.
                type: bool
        version_added: "1.11.0"
    state:
        description:
            - State of the SQL server. Use C(present) to create or update a server and use C(absent) to delete a server.
        default: present
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Zim Kalinowski (@zikalino)

'''

EXAMPLES = '''
- name: Create (or update) SQL Server
  azure_rm_sqlserver:
    resource_group: myResourceGroup
    name: server_name
    location: westus
    admin_username: mylogin
    admin_password: Testpasswordxyz12!

- name: Change SQL Server admin password
  azure_rm_sqlserver:
    resource_group: myResourceGroup
    name: server_name
    location: westus
    admin_password: NewPasswordx123!
    change_admin_password: true

- name: Create SQL Server with Azure Active Directory admin
  azure_rm_sqlserver:
    resource_group: myResourceGroup
    name: server_name
    location: westus
    admin_username: mylogin
    admin_password: Testpasswordxyz12!
    administrators:
      principal_type: Group
      login: MySqlAdminGroup
      sid: "{{ MySqlAdminGroup.object_id }}"
      tenant_id: "{{ my_tenant_id }}"
      azure_ad_only_authentication: false
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Sql/servers/sqlcrudtest-4645
version:
    description:
        - The version of the server.
    returned: always
    type: str
    sample: 12.0
state:
    description:
        - The state of the server.
    returned: always
    type: str
    sample: state
fully_qualified_domain_name:
    description:
        - The fully qualified domain name of the server.
    returned: always
    type: str
    sample: sqlcrudtest-4645.database.windows.net
'''

import time
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


administrators_spec = dict(
    administrator_type=dict(type='str', default='ActiveDirectory'),
    principal_type=dict(type='str', choices=['User', 'Group', 'Application']),
    login=dict(type='str'),
    sid=dict(type='str'),
    tenant_id=dict(type='str'),
    azure_ad_only_authentication=dict(type='bool'),
)


class AzureRMSqlServer(AzureRMModuleBaseExt):
    """Configuration class for an Azure RM SQL Server resource"""

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
                type='str'
            ),
            admin_username=dict(
                type='str'
            ),
            admin_password=dict(
                type='str',
                no_log=True
            ),
            version=dict(
                type='str'
            ),
            identity=dict(
                type='str'
            ),
            minimal_tls_version=dict(
                type="str",
                choices=["1.0", "1.1", "1.2"]
            ),
            public_network_access=dict(
                type="str",
                choices=["Enabled", "Disabled"]
            ),
            restrict_outbound_network_access=dict(
                type="str",
                choices=["Enabled", "Disabled"]
            ),
            change_admin_password=dict(
                type="bool",
                default=False,
                no_log=False,
            ),
            administrators=dict(
                type='dict',
                options=administrators_spec,
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.parameters = dict()
        self.tags = None

        self.results = dict(changed=False)
        self.state = None
        self.to_do = Actions.NoAction
        self.change_admin_password = False

        super(AzureRMSqlServer, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "admin_username":
                    self.parameters.update({"administrator_login": kwargs[key]})
                elif key == "admin_password":
                    self.parameters.update({"administrator_login_password": kwargs[key]})
                elif key == "identity":
                    self.parameters.update({"identity": {"type": kwargs[key]}})
                else:
                    self.parameters[key] = kwargs[key]

        old_response = None
        response = None

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_sqlserver()

        if not old_response:
            self.log("SQL Server instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("SQL Server instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if SQL Server instance has to be deleted or may be updated")
                update_tags, newtags = self.update_tags(old_response.get('tags', dict()))
                if update_tags:
                    self.tags = newtags
                admin_pass = self.parameters.pop('administrator_login_password', None)  # remove for comparison as value not returned in old_response
                if self.change_admin_password:
                    self.parameters.update(old_response)  # use all existing config
                    self.parameters.update({"administrator_login_password": admin_pass})
                self.results['compare'] = []
                if not self.idempotency_check(old_response, self.parameters):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the SQL Server instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            self.parameters['tags'] = self.tags
            response = self.create_update_sqlserver()
            response.pop('administrator_login_password', None)

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = True if self.change_admin_password else old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("SQL Server instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_sqlserver()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_sqlserver():
                time.sleep(20)
        else:
            self.log("SQL Server instance unchanged")
            self.results['changed'] = False
            response = old_response

        if response:
            self.results.update(self.format_results(response))

        return self.results

    def create_update_sqlserver(self):
        '''
        Creates or updates SQL Server with the specified configuration.

        :return: deserialized SQL Server instance state dictionary
        '''
        self.log("Creating / Updating the SQL Server instance {0}".format(self.name))

        try:
            response = self.sql_client.servers.begin_create_or_update(resource_group_name=self.resource_group,
                                                                      server_name=self.name,
                                                                      parameters=self.parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except Exception as exc:
            self.log('Error attempting to create the SQL Server instance.')
            self.fail("Error creating the SQL Server instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_sqlserver(self):
        '''
        Deletes specified SQL Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the SQL Server instance {0}".format(self.name))
        try:
            response = self.sql_client.servers.begin_delete(resource_group_name=self.resource_group,
                                                            server_name=self.name)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as e:
            self.log('Error attempting to delete the SQL Server instance.')
            self.fail("Error deleting the SQL Server instance: {0}".format(str(e)))

        return True

    def get_sqlserver(self):
        '''
        Gets the properties of the specified SQL Server.

        :return: deserialized SQL Server instance state dictionary
        '''
        self.log("Checking if the SQL Server instance {0} is present".format(self.name))
        found = False
        try:
            response = self.sql_client.servers.get(resource_group_name=self.resource_group,
                                                   server_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("SQL Server instance : {0} found".format(response.name))
        except ResourceNotFoundError:
            self.log('Did not find the SQL Server instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_results(self, response):
        return {
            "id": response.get("id"),
            "version": response.get("version"),
            "state": response.get("state"),
            "fully_qualified_domain_name": response.get("fully_qualified_domain_name"),
        }


def main():
    """Main execution"""
    AzureRMSqlServer()


if __name__ == '__main__':
    main()
