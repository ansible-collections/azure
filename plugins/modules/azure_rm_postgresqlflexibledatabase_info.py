#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexibledatabase_info
version_added: "2.2.0"
short_description: Get Azure PostgreSQL Flexible Database facts
description:
    - Get facts of PostgreSQL Flexible Database.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        type: str
        required: True
    server_name:
        description:
            - The name of the post gresql server.
        type: str
        required: True
    name:
        description:
            - The name of the post gresql database.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: List instance of PostgreSQL Flexible Database by server name
  azure_rm_postgresqlflexibledatabase_info:
    resource_group: myResourceGroup
    server_name: server_name

- name: Get instances of PostgreSQL Flexible Database
  azure_rm_postgresqlflexibledatabase_info:
    resource_group: myResourceGroup
    server_name: server_name
    name: database_name
'''

RETURN = '''
database:
    description:
        - A list of dictionaries containing facts for PostgreSQL Flexible Database.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID of the postgresql flexible database.
            returned: always
            type: str
            sample: "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.DBforPostgreSQL/flexibleServers/postfle9/databases/freddatabase"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: freddatabase
        charset:
            description:
                - The charset of the database.
            returned: always
            type: str
            sample: UTF-8
        collation:
            description:
                - The collation of the database.
            returned: always
            type: str
            sample: en_US.utf8
        type:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: Microsoft.DBforPostgreSQL/flexibleServers/databases
        system_data:
            description:
                - The system metadata relating to this resource.
            type: complex
            returned: always
            contains:
                created_by:
                    description:
                        - The identity that created the resource.
                    type: str
                    returned: always
                    sample: null
                created_by_type:
                    description:
                        - The type of identity that created the resource.
                    returned: always
                    type: str
                    sample: null
                created_at:
                    description:
                        - The timestamp of resource creation (UTC).
                    returned: always
                    sample: null
                    type: str
                last_modified_by:
                    description:
                        - The identity that last modified the resource.
                    type: str
                    returned: always
                    sample: null
                last_modified_by_type:
                    description:
                        - The type of identity that last modified the resource.
                    returned: always
                    sample: null
                    type: str
                last_modified_at:
                    description:
                        - The timestamp of resource last modification (UTC).
                    returned: always
                    sample: null
                    type: str
'''


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPostgreSqlFlexibleDatabaseInfo(AzureRMModuleBase):
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
            ),
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.name = None
        self.server_name = None
        super(AzureRMPostgreSqlFlexibleDatabaseInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results['databases'] = self.get()
        else:
            self.results['databases'] = self.list_all()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.databases.get(resource_group_name=self.resource_group,
                                                                     server_name=self.server_name,
                                                                     database_name=self.name)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError:
            self.log('Could not get facts for PostgreSQL Flexible Server.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_all(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.databases.list_by_server(resource_group_name=self.resource_group,
                                                                                server_name=self.server_name)
            self.log("Response : {0}".format(response))
        except Exception as ec:
            self.log('Could not get facts for PostgreSQL Flexible Servers.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        result = dict(
            id=item.id,
            name=item.name,
            system_data=dict(),
            type=item.type,
            charset=item.charset,
            collation=item.collation
        )
        if item.system_data is not None:
            result['system_data']['created_by'] = item.system_data.created_by
            result['system_data']['created_by_type'] = item.system_data.created_by_type
            result['system_data']['created_at'] = item.system_data.created_at
            result['system_data']['last_modified_by'] = item.system_data.last_modified_by
            result['system_data']['last_modified_by_type'] = item.system_data.last_modified_by_type
            result['system_data']['last_modified_at'] = item.system_data.last_modified_at

        return result


def main():
    AzureRMPostgreSqlFlexibleDatabaseInfo()


if __name__ == '__main__':
    main()
