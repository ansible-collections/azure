#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexiblemigration_info
version_added: "3.7.0"
short_description: Get or list Azure PostgreSQL Flexible Migration facts
description:
    - Get or list facts of PostgreSQL Flexible Migration.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        type: str
        required: True
    target_db_server_name:
        description:
            - The name of the target postgresql flexible server.
        type: str
        required: True
    migration_name:
        description:
            - The name of the post gresql flexible migration.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: List instance of PostgreSQL Flexible Migration by server name
  azure_rm_postgresqlflexiblemigration_info:
    resource_group: myResourceGroup
    target_db_server_name: server_name

- name: Get instances of PostgreSQL Flexible Migration
  azure_rm_postgresqlflexiblemigration_info:
    resource_group: myResourceGroup
    target_db_server_name: server_name
    migration_name: migration_name
'''

RETURN = '''
migrations:
    description:
        - A list of dictionaries containing facts for PostgreSQL Flexible Migration.
    returned: always
    type: list
    sample: [
            {
                "current_status": {
                    "current_sub_state_details": {
                        "current_sub_state": "ValidationInProgress",
                        "db_details": {}
                    },
                    "state": "InProgress"
                },
                "dbs_to_migrate": [
                    "ticketdb",
                    "timedb",
                    "inventorydb"
                ],
                "id": "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG03/providers/Microsoft.DBforPostgreSQL/flexibleServers/postflexiblefredtest02/migrations/testmigration",
                "location": "East US",
                "migrate_roles": "False",
                "migration_id": "47214695-22af-4424-b67d-3bb1e8fee8b3",
                "migration_mode": "Online",
                "migration_option": "ValidateAndMigrate",
                "migration_window_start_time_in_utc": "2025-07-09T08:04:44.360622Z",
                "name": "testmigration",
                "overwrite_dbs_in_target": "True",
                "setup_logical_replication_on_source_db_if_needed": "False",
                "source_db_server_resource_id": "20.121.44.182:22@azureuser",
                "source_type": "OnPremises",
                "ssl_mode": "Prefer",
                "target_db_server_metadata": {
                    "location": "East US",
                    "sku": {
                        "name": "Standard_B1ms",
                        "tier": "Burstable"
                    },
                    "storage_mb": 131072,
                    "version": "12"
                },
                "target_db_server_resource_id": "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG03/providers/Microsoft.DBforPostgreSQL/flexibleServers/postflexiblefredtest02",
                "type": "Microsoft.DBforPostgreSQL/flexibleServers/migrations"
            }
        ]
'''


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPostgreSqlFlexibleMigrationInfo(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
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
            ),
            migration_subscription_id=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.migration_name = None
        self.target_db_server_name = None
        self.migration_subscription_id = None

        super(AzureRMPostgreSqlFlexibleMigrationInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if not self.migration_subscription_id:
            self.migration_subscription_id = self.subscription_id

        if self.migration_name is not None:
            self.results['migrations'] = self.get()
        else:
            self.results['migrations'] = self.list_all()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.migrations.get(subscription_id=self.migration_subscription_id,
                                                                      resource_group_name=self.resource_group,
                                                                      target_db_server_name=self.target_db_server_name,
                                                                      migration_name=self.migration_name)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError:
            self.log('Could not get migration facts for PostgreSQL Flexible Server.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_all(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.migrations.list_by_target_server(subscription_id=self.migration_subscription_id,
                                                                                        resource_group_name=self.resource_group,
                                                                                        target_db_server_name=self.target_db_server_name)
            self.log("Response : {0}".format(response))
        except Exception:
            self.log('Could not list migration facts for PostgreSQL Flexible Server.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        return item.as_dict()


def main():
    AzureRMPostgreSqlFlexibleMigrationInfo()


if __name__ == '__main__':
    main()
