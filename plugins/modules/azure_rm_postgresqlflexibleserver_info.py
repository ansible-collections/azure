#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexibleserver_info
version_added: "2.2.0"
short_description: Get Azure PostgreSQL Flexible Server facts
description:
    - Get facts of PostgreSQL Flexible Server.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        type: str
    name:
        description:
            - The name of the server.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Get instance of PostgreSQL Flexible Server
  azure_rm_postgresqlflexibleserver_info:
    resource_group: myResourceGroup
    name: server_name

- name: List instances of PostgreSQL Flexible Server
  azure_rm_postgresqlflexibleserver_info:
    resource_group: myResourceGroup
    tags:
      - key
'''

RETURN = '''
servers:
    description:
        - A list of dictionaries containing facts for PostgreSQL Flexible servers.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID of the postgresql flexible server.
            returned: always
            type: str
            sample: "/subscriptions/xxx/resourceGroups/myResourceGroup/providers/Microsoft.DBforPostgreSQL/flexibleservers/postgresql3"
        resource_group:
            description:
                - Resource group name.
            returned: always
            type: str
            sample: myResourceGroup
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: postgreabdud1223
        location:
            description:
                - The location the resource resides in.
            returned: always
            type: str
            sample: eastus
        sku:
            description:
                - The SKU of the server.
            returned: always
            type: complex
            contains:
                name:
                    description:
                        - The name of the SKU.
                    returned: always
                    type: str
                    sample: Standard_B1ms
                tier:
                    description:
                        - The tier of the particular SKU.
                    returned: always
                    type: str
                    sample: Burstable
        storage:
            description:
                - The maximum storage allowed for a server.
            returned: always
            type: complex
            contains:
                storage_size_gb:
                    description:
                        - Max storage allowed for a server.
                    type: int
                    returned: always
                    sample: 128
        administrator_login:
            description:
                - The administrator's login name of a server.
            returned: always
            type: str
            sample: azureuser
        version:
            description:
                - Flexible Server version.
            returned: always
            type: str
            sample: "12"
        fully_qualified_domain_name:
            description:
                - The fully qualified domain name of the flexible server.
            returned: always
            type: str
            sample: postflexiblefredpgsqlflexible.postgres.database.azure.com
        availability_zone:
            description:
                - availability zone information of the server.
            type: str
            returned: always
            sample: 1
        backup:
            description:
                - Backup properties of a server.
            type: complex
            returned: always
            contains:
                backup_retention_days:
                    description:
                        - Backup retention days for the server.
                    type: int
                    returned: always
                    sample: 7
                geo_redundant_backup:
                    description:
                        - A value indicating whether Geo-Redundant backup is enabled on the server.
                    type: str
                    returned: always
                    sample: Disabled
        high_availability:
            description:
                - High availability properties of a server.
            type: complex
            returned: always
            contains:
                mode:
                    description:
                        - The HA mode for the server.
                    returned: always
                    sample: Disabled
                    type: str
                standby_availability_zone:
                    description:
                        - availability zone information of the standby.
                    type: str
                    returned: always
                    sample: null
        maintenance_window:
            description:
                - Maintenance window properties of a server.
            type: complex
            returned: always
            contains:
                custom_window:
                    description:
                        - Indicates whether custom window is enabled or disabled.
                    returned: always
                    sample: Enabled
                    type: str
                day_of_week:
                    description:
                        - Day of week for maintenance window.
                    returned: always
                    sample: 0
                    type: int
                start_hour:
                    description:
                        - Start hour for maintenance window.
                    type: int
                    returned: always
                    sample: 8
                start_minute:
                    description:
                        - Start minute for maintenance window.
                    type: int
                    returned: always
                    sample: 0
        network:
            description:
                - Network properties of a server.
            type: complex
            returned: always
            contains:
                delegated_subnet_resource_id:
                    description:
                        - Delegated subnet arm resource id.
                    type: str
                    returned: always
                    sample: null
                private_dns_zone_arm_resource_id:
                    description:
                        - Private dns zone arm resource id.
                    type: str
                    returned: always
                    sample: null
                public_network_access:
                    description:
                        - Public network access is enabled or not.
                    type: str
                    returned: always
                    sample: Enabled
        point_in_time_utc:
            description:
                - Restore point creation time (ISO8601 format).
            type: str
            sample: null
            returned: always
        source_server_resource_id:
            description:
                - The source server resource ID to restore from.
            type: str
            returned: always
            sample: null
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
        tags:
            description:
                - Tags assigned to the resource. Dictionary of string:string pairs.
            type: dict
            returned: always
            sample: { tag1: abc }
        auth_config:
            description:
                - AuthConfig properties of a server.
            type: dict
            returned: always
            sample: {"active_directory_auth": "Disabled", "password_auth": "Enabled", "tenant_id": null}
'''


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    import azure.mgmt.rdbms.postgresql_flexibleservers.models as PostgreSQLFlexibleModels
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPostgreSqlFlexibleServersInfo(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
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
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.name = None
        self.tags = None
        super(AzureRMPostgreSqlFlexibleServersInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.resource_group is not None and self.name is not None:
            self.results['servers'] = self.get()
        elif self.resource_group is not None:
            self.results['servers'] = self.list_by_resource_group()
        else:
            self.results['servers'] = self.list_all()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.servers.get(resource_group_name=self.resource_group,
                                                                   server_name=self.name)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError:
            self.log('Could not get facts for PostgreSQL Flexible Server.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.servers.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except Exception:
            self.log('Could not get facts for PostgreSQL Flexible Servers.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_all(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.servers.list()
            self.log("Response : {0}".format(response))
        except Exception:
            self.log('Could not get facts for PostgreSQL Flexible Servers.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        result = dict(
            id=item.id,
            resource_group=self.resource_group,
            name=item.name,
            sku=dict(),
            location=item.location,
            tags=item.tags,
            system_data=dict(),
            administrator_login=item.administrator_login,
            version=item.version,
            minor_version=item.minor_version,
            fully_qualified_domain_name=item.fully_qualified_domain_name,
            storage=dict(),
            backup=dict(),
            network=dict(),
            high_availability=dict(),
            maintenance_window=dict(),
            source_server_resource_id=item.source_server_resource_id,
            point_in_time_utc=item.point_in_time_utc,
            availability_zone=item.availability_zone,
            auth_config=dict()
        )
        if item.sku is not None:
            result['sku']['name'] = item.sku.name
            result['sku']['tier'] = item.sku.tier
        if item.system_data is not None:
            result['system_data']['created_by'] = item.system_data.created_by
            result['system_data']['created_by_type'] = item.system_data.created_by_type
            result['system_data']['created_at'] = item.system_data.created_at
            result['system_data']['last_modified_by'] = item.system_data.last_modified_by
            result['system_data']['last_modified_by_type'] = item.system_data.last_modified_by_type
            result['system_data']['last_modified_at'] = item.system_data.last_modified_at
        if item.storage is not None:
            result['storage']['storage_size_gb'] = item.storage.storage_size_gb
        if item.backup is not None:
            result['backup']['backup_retention_days'] = item.backup.backup_retention_days
            result['backup']['geo_redundant_backup'] = item.backup.geo_redundant_backup
        if item.network is not None:
            result['network']['public_network_access'] = item.network.public_network_access
            result['network']['delegated_subnet_resource_id'] = item.network.delegated_subnet_resource_id
            result['network']['private_dns_zone_arm_resource_id'] = item.network.private_dns_zone_arm_resource_id
        if item.high_availability is not None:
            result['high_availability']['mode'] = item.high_availability.mode
            result['high_availability']['standby_availability_zone'] = item.high_availability.standby_availability_zone
        if item.maintenance_window is not None:
            result['maintenance_window']['custom_window'] = item.maintenance_window.custom_window
            result['maintenance_window']['start_minute'] = item.maintenance_window.start_minute
            result['maintenance_window']['start_hour'] = item.maintenance_window.start_hour
            result['maintenance_window']['day_of_week'] = item.maintenance_window.day_of_week
        if item.identity is not None:
            result['identity'] = item.identity.as_dict()
        else:
            result['identity'] = PostgreSQLFlexibleModels.UserAssignedIdentity(type='None').as_dict()
        if item.auth_config:
            result['auth_config']['active_directory_auth'] = item.auth_config.active_directory_auth
            result['auth_config']['password_auth'] = item.auth_config.password_auth
            result['auth_config']['tenant_id'] = item.auth_config.tenant_id

        return result


def main():
    AzureRMPostgreSqlFlexibleServersInfo()


if __name__ == '__main__':
    main()
