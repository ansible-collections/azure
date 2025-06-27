#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexibleserver
version_added: "2.2.0"
short_description: Manage PostgreSQL Flexible Server instance
description:
    - Create, update and delete instance of PostgreSQL Flexible Server.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource.
            - You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
        type: str
    name:
        description:
            - The name of the flexible server.
        required: True
        type: str
    sku:
        description:
            - The SKU (pricing tier) of the server.
        type: dict
        suboptions:
            name:
                description:
                    - The name of the sku, typically, tier + family + cores, such as Standard_D4s_v3.
                type: str
                required: True
            tier:
                description:
                    - The tier of the particular
                type: str
                choices:
                    - Burstable
                    - GeneralPurpose
                    - MemoryOptimized
                required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
        type: str
    storage:
        description:
            - Storage properties of a server.
        type: dict
        suboptions:
            storage_size_gb:
                description:
                    - The storage size for the server.
                type: int
    administrator_login:
        description:
            - The administrator's login name of a server.
            - Can only be specified when the server is being created (and is required for creation).
        type: str
    administrator_login_password:
        description:
            - The administrator login password (required for server creation).
        type: str
    version:
        description:
            - PostgreSQL Server version.
        type: str
        choices:
            - '11'
            - '12'
            - '13'
            - '14'
            - '15'
            - '16'
            - '17'
    fully_qualified_domain_name:
        description:
            - The fully qualified domain name of a server.
        type: str
    backup:
        description:
            - Backup properties of a server.
        type: dict
        suboptions:
            backup_retention_days:
                description:
                    - Backup retention days for the server.
                type: int
            geo_redundant_backup:
                description:
                    - A value indicating whether Geo-Redundant backup is enabled on the server.
                type: str
                choices:
                    - Enabled
                    - Disabled
    network:
        description:
            - Network properties of a server.
        type: dict
        suboptions:
            delegated_subnet_resource_id:
                description:
                    - Delegated subnet arm resource id.
                type: str
            private_dns_zone_arm_resource_id:
                description:
                    - Private dns zone arm resource id.
                type: str
            public_network_access:
                description:
                    - Public network access is enabled or not.
                type: str
                choices:
                    - Enabled
                    - Disabled
    high_availability:
        description:
            - High availability properties of a server.
        type: dict
        suboptions:
            mode:
                description:
                    - The HA mode for the server.
                type: str
                choices:
                    - Disabled
                    - ZoneRedundant
                    - SameZone
            standby_availability_zone:
                description:
                    - Availability zone information of the standby.
                type: str
    maintenance_window:
        description:
            - Maintenance window properties of a server.
        type: dict
        suboptions:
            custom_window:
                description:
                    - Indicates whether custom window is enabled or disabled.
                type: str
            start_hour:
                description:
                    - Start hour for maintenance window.
                type: int
            start_minute:
                description:
                    - Start minute for maintenance window.
                type: int
            day_of_week:
                description:
                    - Day of week for maintenance window.
                type: int
    point_in_time_utc:
        description:
            - Restore point creation time (ISO8601 format), specifying the time to restore from.
            - It's required when I(create_mode=PointInTimeRestore).
        type: str
    availability_zone:
        description:
            - Availability zone information of the server
        type: str
    create_mode:
        description:
            - The mode to create a new PostgreSQL server.
        type: str
        choices:
            - Default
            - Create
            - Update
            - PointInTimeRestore
    source_server_resource_id:
        description:
            - The source server resource ID to restore from.
            - It's required when I(create_mode=PointInTimeRestore)
        type: str
    state:
        description:
            - Assert the state of the PostgreSQL Flexible server.
            - Use C(present) to create or update a server and C(absent) to delete it.
        default: present
        type: str
        choices:
            - present
            - absent
    is_restart:
        description:
            - Whether to restart the Post gresql server.
        type: bool
        default: False
    is_stop:
        description:
            - Whether to stop the Post gresql server.
        type: bool
        default: False
    is_start:
        description:
            - Whether to start the Post gresql server.
        type: bool
        default: False
    auth_config:
        description:
            - AuthConfig properties of a server.
        type: dict
        version_added: '3.6.0'
        suboptions:
            active_directory_auth:
                description:
                    - If C(Enabled), Azure Active Directory authentication is enabled.
                type: str
                choices:
                    - Enabled
                    - Disabled
            password_auth:
                description:
                    - If C(Enabled), Password authentication is enabled.
                type: str
                choices:
                    - Enabled
                    - Disabled
            tenant_id:
                description:
                    - Tenant id of the server.
                type: str
    identity:
        description:
            - Identity for the Server.
        type: dict
        version_added: '2.4.0'
        suboptions:
            type:
                description:
                    - Type of the managed identity
                required: false
                choices:
                    - UserAssigned
                    - None
                    - SystemAssigned
                default: None
                type: str
            user_assigned_identities:
                description:
                    - User Assigned Managed Identities and its options
                required: false
                type: dict
                default: {}
                suboptions:
                    id:
                        description:
                            - List of the user assigned identities IDs associated to the VM
                        required: false
                        type: list
                        elements: str
                        default: []
                    append:
                        description:
                            - If the list of identities has to be appended to current identities (true) or if it has to replace current identities (false)
                        required: false
                        type: bool
                        default: True


extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Create (or update) PostgreSQL Flexible Server
  azure_rm_postgresqlflexibleserver:
    resource_group: myResourceGroup
    name: testserver
    sku:
      name: Standard_B1ms
      tier: Burstable
    administrator_login: azureuser
    administrator_login_password: "{{ password }}"
    version: 12
    storage:
      storage_size_gb: 128
    fully_qualified_domain_name: st-private-dns-zone.postgres.database.azure.com
    backup:
      backup_retention_days: 7
      geo_redundant_backup: Disabled
    maintenance_window:
      custom_window: Enabled
      start_hour: 8
      start_minute: 0
      day_of_week: 0
    point_in_time_utc: 2023-05-31T00:28:17.7279547+00:00
    availability_zone: 1
    create_mode: Default

- name: Delete PostgreSQL Flexible Server
  azure_rm_postgresqlflexibleserver:
    resource_group: myResourceGroup
    name: testserver
    state: absent
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
                        - ax storage allowed for a server.
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
            choices:
                - '11'
                - '12'
                - '13'
        fully_qualified_domain_name:
            description:
                - The fully qualified domain name of the flexible server.
            returned: always
            type: str
            sample: postflexiblefredpgsqlflexible.postgres.database.azure.com
        availability_zone:
            description:
                - Availability zone information of the server.
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
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
    import azure.mgmt.rdbms.postgresql_flexibleservers.models as PostgreSQLFlexibleModels
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


sku_spec = dict(
    name=dict(type='str', required=True),
    tier=dict(type='str', required=True, choices=["Burstable", "GeneralPurpose", "MemoryOptimized"])
)


maintenance_window_spec = dict(
    custom_window=dict(type='str'),
    start_hour=dict(type='int'),
    start_minute=dict(type='int'),
    day_of_week=dict(type='int'),
)


high_availability_spec = dict(
    mode=dict(type='str', choices=["Disabled", "ZoneRedundant", "SameZone"]),
    standby_availability_zone=dict(type='str')
)


network_spec = dict(
    delegated_subnet_resource_id=dict(type='str'),
    private_dns_zone_arm_resource_id=dict(type='str'),
    public_network_access=dict(type='str', choices=["Enabled", "Disabled"])
)


backup_spec = dict(
    backup_retention_days=dict(type='int'),
    geo_redundant_backup=dict(type='str', choices=["Enabled", "Disabled"]),
)


storage_spec = dict(
    storage_size_gb=dict(type='int')
)


user_assigned_identities_spec = dict(
    id=dict(type='list', default=[], elements='str'),
    append=dict(type='bool', default=True)
)


managed_identity_spec = dict(
    type=dict(type='str', choices=['UserAssigned', 'None', 'SystemAssigned'], default='None'),
    user_assigned_identities=dict(type='dict', options=user_assigned_identities_spec, default={}),
)


class AzureRMPostgreSqlFlexibleServers(AzureRMModuleBaseExt):
    """Configuration class for an Azure RM PostgreSQL Flexible Server resource"""

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
            sku=dict(
                type='dict',
                options=sku_spec
            ),
            location=dict(
                type='str'
            ),
            administrator_login=dict(
                type='str'
            ),
            administrator_login_password=dict(
                type='str',
                no_log=True
            ),
            version=dict(
                type='str',
                choices=['11', '12', '13', '14', '15', '16', '17']
            ),
            fully_qualified_domain_name=dict(
                type='str',
            ),
            storage=dict(
                type='dict',
                options=storage_spec
            ),
            backup=dict(
                type='dict',
                options=backup_spec
            ),
            network=dict(
                type='dict',
                options=network_spec
            ),
            high_availability=dict(
                type='dict',
                options=high_availability_spec
            ),
            maintenance_window=dict(
                type='dict',
                options=maintenance_window_spec
            ),
            point_in_time_utc=dict(
                type='str'
            ),
            availability_zone=dict(
                type='str'
            ),
            create_mode=dict(
                type='str',
                choices=['Default', 'Create', 'Update', 'PointInTimeRestore']
            ),
            is_start=dict(
                type='bool',
                default=False,
            ),
            is_restart=dict(
                type='bool',
                default=False
            ),
            is_stop=dict(
                type='bool',
                default=False
            ),
            source_server_resource_id=dict(
                type='str'
            ),
            identity=dict(type='dict', options=managed_identity_spec),
            auth_config=dict(
                type='dict',
                options=dict(
                    active_directory_auth=dict(type='str', choices=['Enabled', 'Disabled']),
                    password_auth=dict(type='str', choices=['Enabled', 'Disabled']),
                    tenant_id=dict(type='str')
                )
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
        self.update_parameters = dict()
        self.tags = None
        self.is_start = None
        self.is_stop = None
        self.is_restart = None
        self.identity = None
        self.auth_config = None

        self.results = dict(changed=False)
        self.state = None

        self._managed_identity = None

        super(AzureRMPostgreSqlFlexibleServers, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                               supports_check_mode=True,
                                                               supports_tags=True)

    @property
    def managed_identity(self):
        if not self._managed_identity:
            self._managed_identity = {"identity": PostgreSQLFlexibleModels.UserAssignedIdentity,
                                      "user_assigned": PostgreSQLFlexibleModels.UserIdentity
                                      }
        return self._managed_identity

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]
                for key in ['location', 'sku', 'administrator_login_password', 'storage', 'backup',
                            'high_availability', 'maintenance_window', 'create_mode', 'auth_config']:
                    self.update_parameters[key] = kwargs[key]

        old_response = None
        response = None
        changed = False

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location
            self.update_parameters["location"] = resource_group.location

        old_response = self.get_postgresqlflexibleserver()

        if not old_response:
            self.log("PostgreSQL Flexible Server instance doesn't exist")
            if self.state == 'present':
                if not self.check_mode:
                    if self.identity:
                        update_identity, new_identity = self.update_managed_identity(new_identity=self.identity)
                        if update_identity:
                            self.parameters['identity'] = new_identity
                    response = self.create_postgresqlflexibleserver(self.parameters)
                    if self.is_stop:
                        self.stop_postgresqlflexibleserver()
                    elif self.is_start:
                        self.start_postgresqlflexibleserver()
                    elif self.is_restart:
                        self.restart_postgresqlflexibleserver()
                changed = True
            else:
                self.log("PostgreSQL Flexible Server instance doesn't exist, Don't need to delete")
        else:
            self.log("PostgreSQL Flexible Server instance already exists")
            if self.state == 'present':
                update_flag = False
                if self.update_parameters.get('sku') is not None:
                    for key in self.update_parameters['sku'].keys():
                        if self.update_parameters['sku'][key] is not None and self.update_parameters['sku'][key] != old_response['sku'].get(key):
                            update_flag = True
                        else:
                            self.update_parameters['sku'][key] = old_response['sku'].get(key)

                if self.update_parameters.get('storage') is not None and self.update_parameters['storage'] != old_response['storage']:
                    update_flag = True
                else:
                    self.update_parameters['storage'] = old_response['storage']

                if self.update_parameters.get('backup') is not None:
                    for key in self.update_parameters['backup'].keys():
                        if self.update_parameters['backup'][key] is not None and self.update_parameters['backup'][key] != old_response['backup'].get(key):
                            update_flag = True
                        else:
                            self.update_parameters['backup'][key] = old_response['backup'].get(key)

                if self.update_parameters.get('high_availability') is not None:
                    for key in self.update_parameters['high_availability'].keys():
                        if (self.update_parameters['high_availability'][key] is not None) and\
                                (self.update_parameters['high_availability'][key] != old_response['high_availability'].get(key)):
                            update_flag = True
                        else:
                            self.update_parameters['high_availability'][key] = old_response['high_availability'].get(key)

                if self.update_parameters.get('maintenance_window') is not None:
                    for key in self.update_parameters['maintenance_window'].keys():
                        if (self.update_parameters['maintenance_window'][key] is not None) and\
                                (self.update_parameters['maintenance_window'][key] != old_response['maintenance_window'].get(key)):
                            update_flag = True
                        else:
                            self.update_parameters['maintenance_window'][key] = old_response['maintenance_window'].get(key)

                if self.identity:
                    update_identity, new_identity = self.update_managed_identity(new_identity=self.identity,
                                                                                 curr_identity=old_response.get('identity', {}))
                    if update_identity:
                        self.update_parameters['identity'] = new_identity
                        update_flag = True

                update_tags, new_tags = self.update_tags(old_response['tags'])
                self.update_parameters['tags'] = new_tags
                if update_tags:
                    update_flag = True

                if self.auth_config is not None and not self.default_compare({}, self.auth_config, old_response['auth_config'], '', dict(compare=[])):
                    update_flag = True
                else:
                    self.auth_config = old_response['auth_config']

                if update_flag:
                    changed = True
                    if not self.check_mode:
                        response = self.update_postgresqlflexibleserver(self.update_parameters)
                    else:
                        response = old_response
                    if self.is_stop:
                        self.stop_postgresqlflexibleserver()
                        changed = True
                    elif self.is_start:
                        self.start_postgresqlflexibleserver()
                        changed = True
                    elif self.is_restart:
                        self.restart_postgresqlflexibleserver()
                        changed = True
                else:
                    if not self.check_mode:
                        if self.is_stop:
                            self.stop_postgresqlflexibleserver()
                            changed = True
                        elif self.is_start:
                            self.start_postgresqlflexibleserver()
                            changed = True
                        elif self.is_restart:
                            self.restart_postgresqlflexibleserver()
                            changed = True
                    response = old_response
            else:
                self.log("PostgreSQL Flexible Server instance already exist, will be deleted")
                changed = True
                if not self.check_mode:
                    response = self.delete_postgresqlflexibleserver()

        self.results['changed'] = changed
        self.results['state'] = response

        return self.results

    def update_postgresqlflexibleserver(self, body):
        '''
        Updates PostgreSQL Flexible Server with the specified configuration.
        :return: deserialized PostgreSQL Flexible Server instance state dictionary
        '''
        self.log("Updating the PostgreSQL Flexible Server instance {0}".format(self.name))
        try:
            # structure of parameters for update must be changed
            response = self.postgresql_flexible_client.servers.begin_update(resource_group_name=self.resource_group,
                                                                            server_name=self.name,
                                                                            parameters=body)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except Exception as exc:
            self.log('Error attempting to create the PostgreSQL Flexible Server instance.')
            self.fail("Error updating the PostgreSQL Flexible Server instance: {0}".format(str(exc)))
        return self.format_item(response)

    def create_postgresqlflexibleserver(self, body):
        '''
        Creates PostgreSQL Flexible Server with the specified configuration.
        :return: deserialized PostgreSQL Flexible Server instance state dictionary
        '''
        self.log("Creating the PostgreSQL Flexible Server instance {0}".format(self.name))
        try:
            response = self.postgresql_flexible_client.servers.begin_create(resource_group_name=self.resource_group,
                                                                            server_name=self.name,
                                                                            parameters=body)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except Exception as exc:
            self.log('Error attempting to create the PostgreSQL Flexible Server instance.')
            self.fail("Error creating the PostgreSQL Flexible Server instance: {0}".format(str(exc)))
        return self.format_item(response)

    def delete_postgresqlflexibleserver(self):
        '''
        Deletes specified PostgreSQL Flexible Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the PostgreSQL Flexible Server instance {0}".format(self.name))
        try:
            self.postgresql_flexible_client.servers.begin_delete(resource_group_name=self.resource_group,
                                                                 server_name=self.name)
        except Exception as e:
            self.log('Error attempting to delete the PostgreSQL Flexible Server instance.')
            self.fail("Error deleting the PostgreSQL Flexible Server instance: {0}".format(str(e)))

    def stop_postgresqlflexibleserver(self):
        '''
        Stop PostgreSQL Flexible Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Stop the PostgreSQL Flexible Server instance {0}".format(self.name))
        try:
            self.postgresql_flexible_client.servers.begin_stop(resource_group_name=self.resource_group,
                                                               server_name=self.name)
        except Exception as e:
            self.log('Error attempting to stop the PostgreSQL Flexible Server instance.')
            self.fail("Error stop the PostgreSQL Flexible Server instance: {0}".format(str(e)))

    def start_postgresqlflexibleserver(self):
        '''
        Start PostgreSQL Flexible Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Starting the PostgreSQL Flexible Server instance {0}".format(self.name))
        try:
            self.postgresql_flexible_client.servers.begin_start(resource_group_name=self.resource_group,
                                                                server_name=self.name)
        except Exception as e:
            self.log('Error attempting to start the PostgreSQL Flexible Server instance.')
            self.fail("Error starting the PostgreSQL Flexible Server instance: {0}".format(str(e)))

    def restart_postgresqlflexibleserver(self):
        '''
        Restart PostgreSQL Flexible Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Restarting the PostgreSQL Flexible Server instance {0}".format(self.name))
        try:
            self.postgresql_flexible_client.servers.begin_restart(resource_group_name=self.resource_group,
                                                                  server_name=self.name)
        except Exception as e:
            self.log('Error attempting to restart the PostgreSQL Flexible Server instance.')
            self.fail("Error restarting the PostgreSQL Flexible Server instance: {0}".format(str(e)))

    def get_postgresqlflexibleserver(self):
        '''
        Gets the properties of the specified PostgreSQL Flexible Server.

        :return: deserialized PostgreSQL Flexible Server instance state dictionary
        '''
        self.log("Checking if the PostgreSQL Flexible Server instance {0} is present".format(self.name))
        try:
            response = self.postgresql_flexible_client.servers.get(resource_group_name=self.resource_group,
                                                                   server_name=self.name)
            self.log("Response : {0}".format(response))
            self.log("PostgreSQL Flexible Server instance : {0} found".format(response.name))
        except ResourceNotFoundError as e:
            self.log('Did not find the PostgreSQL Flexible Server instance. Exception as {0}'.format(str(e)))
            return None

        return self.format_item(response)

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
        if item.auth_config is not None:
            result['auth_config']['active_directory_auth'] = item.auth_config.active_directory_auth
            result['auth_config']['password_auth'] = item.auth_config.password_auth
            result['auth_config']['tenant_id'] = item.auth_config.tenant_id
        else:
            result['auth_config'] = None

        return result


def main():
    """Main execution"""
    AzureRMPostgreSqlFlexibleServers()


if __name__ == '__main__':
    main()
