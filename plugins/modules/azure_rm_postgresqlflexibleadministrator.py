#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexibleadministrator
version_added: "3.6.0"
short_description: Manage PostgreSQL Flexible Administrator instance
description:
    - Add or Delete instance of PostgreSQL Flexible Administrator.
    - Require the postflexible server Enable Microsoft Entra authenticate.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
        type: str
    server_name:
        description:
            - The name of the post gresql flexible server.
        required: True
        type: str
    object_id:
        description:
            - The Object ID of Azure Directory Administrator.
        required: True
        type: str
    principal_name:
        description:
            - Active Directory administrator principal name.
        type: str
    principal_type:
        description:
            - The principal type used to represent the type of Active Directory Administrator.
        type: str
        choices:
            - Unknown
            - User
            - Group
            - ServicePrincipal
    tenant_id:
        description:
            - The tenant ID of Active Directory Administrator.
        type: str
    state:
        description:
            - Assert the state of the PostgreSQL Flexible administrator.
            - Use C(present) to create or update a administrator and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Create (or update) PostgreSQL Flexible Administrator
  azure_rm_postgresqlflexibleadministrator:
    resource_group: myResourceGroup
    server_name: testserver
    object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    principal_type: User
    principal_name: fred-sun
    tenant_id: yyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy

- name: Delete PostgreSQL Flexible Administrator
  azure_rm_postgresqlflexibleadministrator:
    resource_group: myResourceGroup
    server_name: testserver
    object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    state: absent
'''

RETURN = '''
administrator:
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
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPostgreSqlFlexibleAdministrator(AzureRMModuleBase):
    """Configuration class for an Azure RM PostgreSQL Flexible Administrator resource"""

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
            object_id=dict(
                type='str',
                required=True
            ),
            principal_type=dict(
                type='str',
                choices=['Unknown', 'User', 'Group', 'ServicePrincipal']
            ),
            principal_name=dict(
                type='str'
            ),
            tenant_id=dict(
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
        self.object_id = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.state = None

        super(AzureRMPostgreSqlFlexibleAdministrator, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                     supports_check_mode=True,
                                                                     supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            else:
                self.parameters[key] = kwargs[key]

        old_response = None
        response = None
        changed = False

        old_response = self.get_postgresqlflexibleadministrator()

        if not old_response:
            self.log("PostgreSQL Flexible Administrator instance doesn't exist")
            if self.state == 'absent':
                self.log("The PostgreSQL Flexible Administrator with object {0} no exist".format(self.object_id))
            else:
                changed = True
                if not self.check_mode:
                    response = self.add_postgresqlflexibleadministrator(self.parameters)
        else:
            self.log("PostgreSQL Flexible Administrator instance with object {0} already exists".format(self.object_id))
            if self.state == 'absent':
                changed = True
                if not self.check_mode:
                    response = self.delete_postgresqlflexibleadministrator()
            else:
                if self.check_mode:
                    changed = True
                    self.fail("PostgreSQL Flexible Administrator instance with object {0} already exists".format(self.object_id))
                response = old_response

        self.results['administrator'] = response
        self.results['changed'] = changed
        return self.results

    def add_postgresqlflexibleadministrator(self, body):
        '''
        Add PostgreSQL Flexible Administrator with the specified configuration.

        :return: deserialized PostgreSQL Flexible Administrator instance state dictionary
        '''
        self.log("Adding the PostgreSQL Flexible Administrator instance {0}".format(self.object_id))

        try:
            response = self.postgresql_flexible_client.administrators.begin_create(resource_group_name=self.resource_group,
                                                                                   server_name=self.server_name,
                                                                                   object_id=self.object_id,
                                                                                   parameters=body)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except Exception as exc:
            self.log('Error attempting to add the PostgreSQL Flexible Administrator instance.')
            self.fail("Error add the PostgreSQL Flexible Administrator instance: {0}".format(str(exc)))
        return self.format_item(response)

    def delete_postgresqlflexibleadministrator(self):
        '''
        Deletes specified PostgreSQL Flexible Administrator instance in the specified server name and resource group.

        :return: True
        '''
        self.log("Deleting the PostgreSQL Flexible Administrator instance {0}".format(self.object_id))
        try:
            self.postgresql_flexible_client.administrators.begin_delete(resource_group_name=self.resource_group,
                                                                        server_name=self.server_name,
                                                                        object_id=self.object_id)
        except Exception as ec:
            self.log('Error attempting to delete the PostgreSQL Flexible Administrator instance.')
            self.fail("Error deleting the PostgreSQL Flexible Administrator instance: {0}".format(str(ec)))

    def get_postgresqlflexibleadministrator(self):
        '''
        Gets the properties of the specified PostgreSQL Flexible Administrator.

        :return: deserialized PostgreSQL Flexible Administrator instance state dictionary
        '''
        self.log("Checking if the PostgreSQL Flexible Administrator instance {0} is present".format(self.object_id))
        found = False
        try:
            response = self.postgresql_flexible_client.administrators.get(resource_group_name=self.resource_group,
                                                                          server_name=self.server_name,
                                                                          object_id=self.object_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("PostgreSQL Flexible Administrator instance : {0} found".format(response.name))
        except ResourceNotFoundError as e:
            self.log('Did not find the PostgreSQL Flexible Administrator instance. Exception as {0}'.format(e))
        if found is True:
            return self.format_item(response)

        return None

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
    """Main execution"""
    AzureRMPostgreSqlFlexibleAdministrator()


if __name__ == '__main__':
    main()
