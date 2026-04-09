#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_oracleautonomousdatabase_info
version_added: "3.17.0"
short_description: Get Oracle Autonomous Database facts
description:
    - Get facts of Oracle Autonomous Database on Azure.

options:
    resource_group:
        description:
            - The name of the resource group.
            - Required when I(name) is specified.
        type: str
    name:
        description:
            - The name of the Oracle Autonomous Database resource.
            - If specified, only the specific database will be returned.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Get a specific Oracle Autonomous Database
  azure.azcollection.azure_rm_oracle_autonomous_database_info:
    resource_group: myResourceGroup
    name: myAutonomousDb

- name: List Oracle Autonomous Databases in a resource group
  azure.azcollection.azure_rm_oracle_autonomous_database_info:
    resource_group: myResourceGroup

- name: List all Oracle Autonomous Databases in a subscription
  azure.azcollection.azure_rm_oracle_autonomous_database_info:

- name: List Oracle Autonomous Databases filtered by tags
  azure.azcollection.azure_rm_oracle_autonomous_database_info:
    resource_group: myResourceGroup
    tags:
      - environment:dev
'''

RETURN = '''
databases:
    description:
        - A list of Oracle Autonomous Database facts.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxx/resourceGroups/myRG/providers/Oracle.Database/autonomousDatabases/myDB"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: myAutonomousDb
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: eastus
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: {"environment": "dev"}
        display_name:
            description:
                - The user-friendly name for the Autonomous Database.
            returned: always
            type: str
            sample: myAutonomousDb
        db_workload:
            description:
                - The Autonomous Database workload type.
            returned: always
            type: str
            sample: OLTP
        compute_model:
            description:
                - The compute model of the Autonomous Database.
            returned: always
            type: str
            sample: ECPU
        compute_count:
            description:
                - The compute amount (CPUs) available to the database.
            returned: always
            type: float
            sample: 2.0
        data_storage_size_in_tbs:
            description:
                - The quantity of data in the database, in terabytes.
            returned: always
            type: int
            sample: 1
        character_set:
            description:
                - The character set for the autonomous database.
            returned: always
            type: str
            sample: AL32UTF8
        ncharacter_set:
            description:
                - The national character set for the Autonomous Database.
            returned: always
            type: str
            sample: AL16UTF16
        db_version:
            description:
                - A valid Oracle Database version for Autonomous Database.
            returned: always
            type: str
            sample: 19c
        license_model:
            description:
                - The Oracle license model.
            returned: always
            type: str
            sample: LicenseIncluded
        lifecycle_state:
            description:
                - The current lifecycle state of the Autonomous Database.
            returned: always
            type: str
            sample: Available
        provisioning_state:
            description:
                - Azure resource provisioning state.
            returned: always
            type: str
            sample: Succeeded
        is_auto_scaling_enabled:
            description:
                - Whether auto scaling is enabled for CPU.
            returned: always
            type: bool
            sample: true
        is_auto_scaling_for_storage_enabled:
            description:
                - Whether auto scaling is enabled for storage.
            returned: always
            type: bool
            sample: true
        is_mtls_connection_required:
            description:
                - Whether mTLS connections are required.
            returned: always
            type: bool
            sample: true
        subnet_id:
            description:
                - Client subnet ID.
            returned: always
            type: str
        vnet_id:
            description:
                - VNET ID for network connectivity.
            returned: always
            type: str
        connection_strings:
            description:
                - Connection strings for the Autonomous Database.
            returned: always
            type: dict
        connection_urls:
            description:
                - Connection URLs for APEX and SQL Developer Web.
            returned: always
            type: dict
'''

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import HttpResponseError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMOracleAutonomousDatabaseInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
            ),
            name=dict(
                type='str'
            ),
            tags=dict(
                type='list',
                elements='str'
            )
        )
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.name = None
        self.tags = None
        super(AzureRMOracleAutonomousDatabaseInfo, self).__init__(
            self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.resource_group is not None and self.name is not None:
            self.results['databases'] = self.get()
        elif self.resource_group is not None:
            self.results['databases'] = self.list_by_resource_group()
        else:
            self.results['databases'] = self.list_by_subscription()

        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.oracle_database_client.autonomous_databases.get(
                resource_group_name=self.resource_group,
                autonomousdatabasename=self.name
            )
            self.log("Response : {0}".format(response))
        except HttpResponseError as e:
            self.log('Could not get facts for Oracle Autonomous Database. Exception as {0}'.format(e))

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.oracle_database_client.autonomous_databases.list_by_resource_group(
                resource_group_name=self.resource_group
            )
            self.log("Response : {0}".format(response))
        except HttpResponseError as e:
            self.log('Could not get facts for Oracle Autonomous Databases. Exception as {0}'.format(e))

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))
        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.oracle_database_client.autonomous_databases.list_by_subscription()
            self.log("Response : {0}".format(response))
        except HttpResponseError as e:
            self.log('Could not get facts for Oracle Autonomous Databases. Exception as {0}'.format(e))

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))
        return results

    def format_item(self, item):
        """Format the SDK response into a module return dictionary."""
        props = item.properties if item.properties else {}
        result = dict(
            id=item.id,
            name=item.name,
            type=item.type,
            location=item.location,
            tags=item.tags,
            resource_group=self.parse_resource_to_dict(item.id).get('resource_group'),
            display_name=getattr(props, 'display_name', None),
            db_workload=getattr(props, 'db_workload', None),
            compute_model=getattr(props, 'compute_model', None),
            compute_count=getattr(props, 'compute_count', None),
            cpu_core_count=getattr(props, 'cpu_core_count', None),
            data_storage_size_in_tbs=getattr(props, 'data_storage_size_in_tbs', None),
            data_storage_size_in_gbs=getattr(props, 'data_storage_size_in_gbs', None),
            character_set=getattr(props, 'character_set', None),
            ncharacter_set=getattr(props, 'ncharacter_set', None),
            db_version=getattr(props, 'db_version', None),
            license_model=getattr(props, 'license_model', None),
            database_edition=getattr(props, 'database_edition', None),
            lifecycle_state=getattr(props, 'lifecycle_state', None),
            lifecycle_details=getattr(props, 'lifecycle_details', None),
            provisioning_state=getattr(props, 'provisioning_state', None),
            is_auto_scaling_enabled=getattr(props, 'is_auto_scaling_enabled', None),
            is_auto_scaling_for_storage_enabled=getattr(props, 'is_auto_scaling_for_storage_enabled', None),
            is_mtls_connection_required=getattr(props, 'is_mtls_connection_required', None),
            is_local_data_guard_enabled=getattr(props, 'is_local_data_guard_enabled', None),
            is_remote_data_guard_enabled=getattr(props, 'is_remote_data_guard_enabled', None),
            subnet_id=getattr(props, 'subnet_id', None),
            vnet_id=getattr(props, 'vnet_id', None),
            private_endpoint=getattr(props, 'private_endpoint', None),
            private_endpoint_ip=getattr(props, 'private_endpoint_ip', None),
            private_endpoint_label=getattr(props, 'private_endpoint_label', None),
            autonomous_database_id=getattr(props, 'autonomous_database_id', None),
            backup_retention_period_in_days=getattr(props, 'backup_retention_period_in_days', None),
            open_mode=getattr(props, 'open_mode', None),
            permission_level=getattr(props, 'permission_level', None),
            role=getattr(props, 'role', None),
            ocid=getattr(props, 'ocid', None),
            oci_url=getattr(props, 'oci_url', None),
            connection_strings=self._format_connection_strings(props),
            connection_urls=self._format_connection_urls(props),
            time_created=str(getattr(props, 'time_created', None)) if getattr(props, 'time_created', None) else None,
        )
        return result

    def _format_connection_strings(self, props):
        """Format connection strings from properties."""
        cs = getattr(props, 'connection_strings', None)
        if cs is None:
            return None
        return dict(
            all_connection_strings=getattr(cs, 'all_connection_strings', None),
            dedicated=getattr(cs, 'dedicated', None),
            high=getattr(cs, 'high', None),
            low=getattr(cs, 'low', None),
            medium=getattr(cs, 'medium', None),
        )

    def _format_connection_urls(self, props):
        """Format connection URLs from properties."""
        cu = getattr(props, 'connection_urls', None)
        if cu is None:
            return None
        return dict(
            apex_url=getattr(cu, 'apex_url', None),
            database_transforms_url=getattr(cu, 'database_transforms_url', None),
            graph_studio_url=getattr(cu, 'graph_studio_url', None),
            machine_learning_notebook_url=getattr(cu, 'machine_learning_notebook_url', None),
            mongo_db_url=getattr(cu, 'mongo_db_url', None),
            ords_url=getattr(cu, 'ords_url', None),
            sql_dev_web_url=getattr(cu, 'sql_dev_web_url', None),
        )


def main():
    """Main execution"""
    AzureRMOracleAutonomousDatabaseInfo()


if __name__ == '__main__':
    main()
