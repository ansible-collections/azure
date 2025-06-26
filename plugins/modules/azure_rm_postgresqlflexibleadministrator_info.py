#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexibleadministrator_info
version_added: "3.6.0"
short_description: Get Azure PostgreSQL Flexible Administrator facts
description:
    - Get facts of PostgreSQL Flexible Administrator.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource.
            - You can obtain this value from the Azure Resource Manager API or the portal.
        type: str
        required: True
    server_name:
        description:
            - The name of the post gresql server.
        type: str
        required: True
    object_id:
        description:
            - Guid of the objectId for the administrator.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: List instance of PostgreSQL Flexible Administrator by server name
  azure_rm_postgresqlflexibleadministrator_info:
    resource_group: myResourceGroup
    server_name: server_name

- name: Get instances of PostgreSQL Flexible Administrator
  azure_rm_postgresqlflexibleadministrator_info:
    resource_group: myResourceGroup
    server_name: server_name
    object_id: a2cf7b83-174b-4371-acce-f2381f373641
'''

RETURN = '''
admistrator:
    description:
        - A list of dictionaries containing facts for PostgreSQL Flexible Administrator.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID of the postgresql flexible admistrator.
            returned: always
            type: str
            sample: "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.DBforPostgreSQL/flexibleServers/postgresql03/administrators/xxx-xxx"
        principal_name:
            description:
                - Active Directory administrator principal name.
            returned: always
            type: str
            sample: fred-sun
        principal_type:
            description:
                - The principal type used to represent the type of Active Directory Administrator.
            returned: always
            type: str
            sample: User
        object_id:
            description:
                - The Object ID of Azure Directory Administrator.
            returned: always
            type: str
            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        type:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: Microsoft.DBforPostgreSQL/flexibleServers/administrators
        tenant_id:
            description:
                - The tenant ID of Active Directory Administrator.
            returned: always
            type: str
            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxx
        resource_group:
            description:
                - The resource group name.
            returned: always
            type: str
            sample: testRG
        server_name:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: postgresql03
'''


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPostgreSqlFlexibleAdministratorInfo(AzureRMModuleBase):
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
            object_id=dict(
                type='str'
            ),
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.object_id = None
        self.server_name = None
        super(AzureRMPostgreSqlFlexibleAdministratorInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.object_id:
            self.results['administrators'] = self.get()
        else:
            self.results['administrators'] = self.list_all()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.administrators.get(resource_group_name=self.resource_group,
                                                                          server_name=self.server_name,
                                                                          object_id=self.object_id)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError:
            self.log('Could not get administrator facts for PostgreSQL Flexible Server.')

        if response:
            results.append(self.format_item(response))

        return results

    def list_all(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.administrators.list_by_server(resource_group_name=self.resource_group,
                                                                                     server_name=self.server_name)
            self.log("Response : {0}".format(response))
        except Exception as ec:
            self.log('Could not list administrators facts for PostgreSQL Flexible Servers.')

        if response:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        return dict(
            resource_group=self.resource_group,
            server_name=self.server_name,
            object_id=item.object_id,
            id=item.id,
            principal_name=item.principal_name,
            principal_type=item.principal_type,
            tenant_id=item.tenant_id,
            type=item.type
        )


def main():
    AzureRMPostgreSqlFlexibleAdministratorInfo()


if __name__ == '__main__':
    main()
