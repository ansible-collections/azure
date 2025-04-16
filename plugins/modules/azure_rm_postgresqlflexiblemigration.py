#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexibledmigration
version_added: "2.2.0"
short_description: Manage PostgreSQL Flexible migration instance
description:
    - Create, update and delete instance of PostgreSQL Flexible migration.

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
            - The name of the migration.
        required: True
        type: str
    charset:
        description:
            - The charset of the migration.
        type: str
    collation:
        description:
            - The collation of the migration.
        type: str
    state:
        description:
            - Assert the state of the PostgreSQL Flexible migration. Use C(present) to create or update a migration and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Create (or update) PostgreSQL Flexible migration
  azure_rm_postgresqlflexibledmigration:
    resource_group: myResourceGroup
    server_name: testserver
    name: db1
    charset: UTF8
    collation: en_US.utf8

- name: Delete PostgreSQL Flexible migration
  azure_rm_postgresqlflexibledmigration:
    resource_group: myResourceGroup
    server_name: testserver
    name: db1
'''

RETURN = '''
migration:
    description:
        - A list of dictionaries containing facts for PostgreSQL Flexible migration.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID of the postgresql flexible migration.
            returned: always
            type: str
            sample: "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.DBforPostgreSQL/flexibleServers/postfle9/migrations/fredmigration"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: fredmigration
        charset:
            description:
                - The charset of the migration.
            returned: always
            type: str
            sample: UTF-8
        collation:
            description:
                - The collation of the migration.
            returned: always
            type: str
            sample: en_US.utf8
        type:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: Microsoft.DBforPostgreSQL/flexibleServers/migrations
'''


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPostgreSqlFlexiblemigration(AzureRMModuleBase):
    """Configuration class for an Azure RM PostgreSQL Flexible migration resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            target_db_server_name=dict(
                type='str',
                required=True
            ),
            migration_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            migration_instance_resource_id=dict(
                type='str'
            ),
            migration_mode=dict(
                type='str',
                choices=['Offline', 'Online']
            ),
            migration_option=dict(
                type='str',
                choices=['Validate', 'Migrate', 'ValidateAndMigrate']
            ),
            source_type=dict(
                type='str',
                choices=["OnPremises", "AWS", "GCP", "AzureVM", "PostgreSQLSingleServer", "AWS_RDS", "AWS_AURORA", "AWS_EC2",
                         "GCP_CloudSQL", "GCP_AlloyDB", "GCP_Compute", "EDB", "EDB_Oracle_Server", "EDB_PostgreSQL", "PostgreSQLFlexibleServer",
                         "PostgreSQLCosmosDB", "Huawei_RDS", "Huawei_Compute", "Heroku_PostgreSQL", "Crunchy_PostgreSQL", "ApsaraDB_RDS",
                         "Digital_Ocean_Droplets", "Digital_Ocean_PostgreSQL", and "Supabase_PostgreSQL"]
            ),
            ssl_mode=dict(
                type='str',
                choices=['VerifyFull', 'Prefer', 'Require', 'VerifyCA'],
                default='VerifyFull'
            ),
            source_db_server_resource_id=dict(
                type='str'
            ),
            source_db_server_fully_qualified_domain_name=dict(
                type='str'
            ),
            secret_parameters=dict(
                type='dict',
                options=dict(
                    source_server_username=dict(type='str'),
                    target_server_username=dict(type='str'),
                    admin_credentials=dict(
                        type='dict',
                        required=True,
                        options=dict(
                            source_server_password=dict(type='str', required=True),
                            target_server_password=dict(type='str', required=True)
                        )
                    )
                )
            ),
            target_db_server_fully_qualified_domain_name=dict(
                type='str'
            ),
            dbs_to_migrate=dict(
                type='list',
                elements='str'
            ),
            setup_logical_replication_on_source_db_if_needed=dict(
                type='str'
                choices=['True', 'False']
            ),
            overwrite_dbs_in_target=dict(
                type='str',
                choices=['True', 'False']
            ),
            migration_window_start_time_in_utc=dict(
                type='str',
            ),
            migration_window_end_time_in_utc=dict(
                type='str'
            ),
            migrate_roles=dict(
                type='str',
                choices=['True', 'False']
            ),
            start_data_migration=dict(
                type='str',
                choices=['True', 'False']
            ),
            trigger_cutover=dict(
                type='str',
                choices=['True', 'False']
            ),
            dbs_to_trigger_cutover_on=dict(
                type='list',
                elements='str',
            ),
            cancel=dict(
                type='str',
                choices=['True', 'False']
            ),
            dbs_to_cancel_migration_on=dict(
                type='list',
                elements='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.migration_name = None
        self.target_db_server_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.state = None

        super(AzureRMPostgreSqlFlexiblemigration, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                 supports_check_mode=True,
                                                                 supports_tags=True)

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

        old_response = self.get_postgresqlflexiblemigration()

        if not old_response:
            self.log("PostgreSQL Flexible migration instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                changed = True
                if not self.check_mode:
                    response = self.create_postgresqlflexiblemigration(self.parameters)
        else:
            self.log("PostgreSQL Flexible migration instance already exists")
            if self.state == 'absent':
                changed = True
                if not self.check_mode:
                    response = self.delete_postgresqlflexiblemigration()
            else:
                if not self.default_compare({}, self.parameters, old_response, '', dict(compare=[])):
                    changed = True
                    if not self.check_mode:
                        response = self.update_postgresqlflexiblemigration(self.parameters)
                else:
                    response = old_response

        self.results['migration'] = response
        self.results['changed'] = changed
        return self.results

    def create_postgresqlflexiblemigration(self, body):
        '''
        Creates PostgreSQL Flexible migration with the specified configuration.

        :return: deserialized PostgreSQL Flexible migration instance state dictionary
        '''
        self.log("Creating the PostgreSQL Flexible migration instance {0}".format(self.name))

        try:
            response = self.postgresql_flexible_client.migrations.create(subscription_id=self.subscription_id,
                                                                         resource_group_name=self.resource_group,
                                                                         target_db_server_name=self.target_db_server_name,
                                                                         migration_name=self.migration_name, )
                                                                         parameters=body)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except Exception as exc:
            self.log('Error attempting to create the PostgreSQL Flexible migration instance.')
            self.fail("Error creating the PostgreSQL Flexible migration instance: {0}".format(str(exc)))
        return self.format_item(response)

    def update_postgresqlflexiblemigration(self, body):
        '''
        Updates PostgreSQL Flexible migration with the specified configuration.

        :return: deserialized PostgreSQL Flexible migration instance state dictionary
        '''
        self.log("Updating the PostgreSQL Flexible migration instance {0}".format(self.name))

        try:
            response = self.postgresql_flexible_client.migrations.update(subscription_id=self.subscription_id,
                                                                         resource_group_name=self.resource_group,
                                                                         target_db_server_name=self.target_db_server_name,
                                                                         migration_name=self.migration_name, )
                                                                         parameters=body)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except Exception as exc:
            self.log('Error attempting to create the PostgreSQL Flexible migration instance.')
            self.fail("Error updating the PostgreSQL Flexible migration instance: {0}".format(str(exc)))
        return self.format_item(response)

    def delete_postgresqlflexiblemigration(self):
        '''
        Deletes specified PostgreSQL Flexible migration instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the PostgreSQL Flexible migration instance {0}".format(self.name))
        try:
            self.postgresql_flexible_client.migrations.begin_delete(subscription_id=self.subscription_id,,
                                                                    resource_group_name=self.resource_group,
                                                                    target_db_server_name=self.target_db_server_name,
                                                                    migration_name=self.migration_name, )
        except Exception as ec:
            self.log('Error attempting to delete the PostgreSQL Flexible migration instance.')
            self.fail("Error deleting the PostgreSQL Flexible migration instance: {0}".format(str(ec)))

    def get_postgresqlflexiblemigration(self):
        '''
        Gets the properties of the specified PostgreSQL Flexible migration.

        :return: deserialized PostgreSQL Flexible migration instance state dictionary
        '''
        self.log("Checking if the PostgreSQL Flexible migration instance {0} is present".format(self.name))
        found = False
        try:
            response = self.postgresql_flexible_client.migrations.get(subscription_id=self.subscription_id,
                                                                      resource_group_name=self.resource_group,
                                                                      target_db_server_name=self.target_db_server_name,
                                                                      migration_name=self.migration_name)

            found = True
            self.log("Response : {0}".format(response))
            self.log("PostgreSQL Flexible migration instance : {0} found".format(response.name))
        except ResourceNotFoundError as e:
            self.log('Did not find the PostgreSQL Flexible migration instance. Exception as {0}'.format(e))
        if found is True:
            return self.format_item(response)

        return None

    def format_item(self, item):
        return item.as_dict()
        result = dict(
            id=item.id,
            name=item.name,
            type=item.type,
            charset=item.charset,
            collation=item.collation
        )
        return result


def main():
    """Main execution"""
    AzureRMPostgreSqlFlexibleMgration()


if __name__ == '__main__':
    main()
