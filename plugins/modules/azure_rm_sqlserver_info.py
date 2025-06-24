#!/usr/bin/python
#
# Copyright (c) 2017 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_sqlserver_info
version_added: "0.1.2"
short_description: Get SQL Server facts
description:
    - Get facts of SQL Server.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        type: str
        required: True
    server_name:
        description:
            - The name of the server.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Zim Kalinowski (@zikalino)

'''

EXAMPLES = '''
- name: Get instance of SQL Server
  azure_rm_sqlserver_info:
    resource_group: myResourceGroup
    server_name: server_name

- name: List instances of SQL Server
  azure_rm_sqlserver_info:
    resource_group: myResourceGroup
'''

RETURN = '''
servers:
    description:
        - A list of dict results where the key is the name of the SQL Server and the values are the facts for that SQL Server.
    returned: always
    type: complex
    contains:
        sqlserver_name:
            description:
                - The key is the name of the server that the values relate to.
            type: complex
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Sql/servers/sqlcrudtest-4645
                name:
                    description:
                        - Resource name.
                    returned: always
                    type: str
                    sample: sqlcrudtest-4645
                type:
                    description:
                        - Resource type.
                    returned: always
                    type: str
                    sample: Microsoft.Sql/servers
                location:
                    description:
                        - Resource location.
                    returned: always
                    type: str
                    sample: japaneast
                kind:
                    description:
                        - Kind of sql server. This is metadata used for the Azure portal experience.
                    returned: always
                    type: str
                    sample: v12.0
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
                    sample: Ready
                fully_qualified_domain_name:
                    description:
                        - The fully qualified domain name of the server.
                    returned: always
                    type: str
                    sample: fully_qualified_domain_name
                minimal_tls_version:
                    description:
                        - The version TLS clients at which must connect.
                    returned: always
                    type: str
                    sample: 1.2
                    version_added: "1.11.0"
                public_network_access:
                    description:
                        - Whether or not public endpoint access is allowed for the server.
                    returned: always
                    type: str
                    sample: Enabled
                    version_added: "1.11.0"
                restrict_outbound_network_access:
                    description:
                        - Whether or not outbound network access is allowed for this server.
                    returned: always
                    type: str
                    sample: Enabled
                    version_added: "1.11.0"
                admin_username:
                    description:
                        - Username of the SQL administrator account for server.
                    returned: always
                    type: str
                    sample: sqladmin
                    version_added: "1.11.0"
                administrators:
                    description:
                        - The Azure Active Directory identity of the server.
                    returned: always
                    type: dict
                    version_added: "1.11.0"
                    contains:
                        administrator_type:
                            description:
                                - Type of the Azure AD administrator.
                            type: str
                            sample: ActiveDirectory
                        azure_ad_only_authentication:
                            description:
                                - Azure AD only authentication enabled.
                            type: bool
                            sample: False
                        login:
                            description:
                                - Login name of the Azure AD administrator.
                            type: str
                            sample: MyAzureAdGroup
                        principal_type:
                            description:
                                - Principal Type of the Azure AD administrator.
                            type: str
                            sample: Group
                        sid:
                            description:
                                - SID (object ID) of the Azure AD administrator.
                            type: str
                            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                        tenant_id:
                            description:
                                - Tenant ID of the Azure AD administrator.
                            type: str
                            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                identity:
                    description:
                        - Identity for the Server.
                    type: complex
                    returned: when available
                    contains:
                        type:
                            description:
                                - Type of the managed identity
                            returned: always
                            sample: UserAssigned
                            type: str
                        user_assigned_identities:
                            description:
                                - User Assigned Managed Identities and its options
                            returned: always
                            type: complex
                            contains:
                                id:
                                    description:
                                        - Dict of the user assigned identities IDs associated to the Resource
                                    returned: always
                                    type: dict
                                    elements: dict
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSqlServerInfo(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
        )
        self.resource_group = None
        self.server_name = None
        super(AzureRMSqlServerInfo, self).__init__(self.module_arg_spec, supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if (self.resource_group is not None and
                self.server_name is not None):
            self.results['servers'] = self.get()
        elif (self.resource_group is not None):
            self.results['servers'] = self.list_by_resource_group()
        return self.results

    def get(self):
        '''
        Gets facts of the specified SQL Server.

        :return: deserialized SQL Serverinstance state dictionary
        '''
        response = None
        results = {}
        try:
            response = self.sql_client.servers.get(resource_group_name=self.resource_group,
                                                   server_name=self.server_name)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError:
            self.log('Could not get facts for Servers.')

        if response is not None:
            results[response.name] = self.format_results(response.as_dict())

        return results

    def list_by_resource_group(self):
        '''
        Gets facts of the specified SQL Server.

        :return: deserialized SQL Serverinstance state dictionary
        '''
        response = None
        results = {}
        try:
            response = self.sql_client.servers.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError:
            self.log('Could not get facts for Servers.')

        if response is not None:
            for item in response:
                results[item.name] = self.format_results(item.as_dict())

        return results

    def format_results(self, response):
        administrators = response.get("administrators")
        return {
            "id": response.get("id"),
            "name": response.get("name"),
            "type": response.get("type"),
            "location": response.get("location"),
            "kind": response.get("kind"),
            "version": response.get("version"),
            "state": response.get("state"),
            "tags": response.get("tags", {}),
            "fully_qualified_domain_name": response.get("fully_qualified_domain_name"),
            "minimal_tls_version": response.get("minimal_tls_version"),
            "public_network_access": response.get("public_network_access"),
            "restrict_outbound_network_access": response.get("restrict_outbound_network_access"),
            "admin_username": response.get("administrator_login"),
            "administrators": None if not administrators else {
                "administrator_type": administrators.get("administrator_type"),
                "azure_ad_only_authentication": administrators.get("azure_ad_only_authentication"),
                "login": administrators.get("login"),
                "principal_type": administrators.get("principal_type"),
                "sid": administrators.get("sid"),
                "tenant_id": administrators.get("tenant_id"),
            },
            "identity": response.get("identity"),
        }


def main():
    AzureRMSqlServerInfo()


if __name__ == '__main__':
    main()
