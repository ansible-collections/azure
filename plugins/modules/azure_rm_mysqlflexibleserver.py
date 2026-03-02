#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_mysqlflexibleserver
version_added: "2.7.0"
short_description: Manage MySQL Flexible Server instance
description:
    - Create, update and delete instance of MySQL Flexible Server.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
        type: str
    name:
        description:
            - The name of the server.
        required: True
        type: str
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
        type: str
    sku:
        description:
            - The SKU (pricing tier) of the server.
        type: dict
        suboptions:
            name:
                description:
                    - The name of the sku, e.g. Standard_D32s_v3.
                type: str
                required: true
            tier:
                description:
                    - The tier of the particular SKU,
                type: str
                choices:
                    - Burstable
                    - GeneralPurpose
                    - MemoryOptimized
                required: true
    storage:
        description:
            - Storage Profile properties of a server.
        type: dict
        suboptions:
            storage_size_gb:
                description:
                    - Max storage size allowed for a server.
                type: int
            iops:
                description:
                    - Storage IOPS for a server.
                type: int
            auto_grow:
                description:
                    - Enable Storage Auto Grow or not.
                type: str
                choices:
                    - Disabled
                    - Enabled
    version:
        description:
            - Server version.
        type: str
        choices:
            - '5.7'
            - '8.0.21'
    administrator_login:
        description:
            - The administrator's login name of a server.
            - Can only be specified when the server is being created (and is required for creation).
        type: str
    administrator_login_password:
        description:
            - The password of the administrator login.
        type: str
    availability_zone:
        description:
            - Availability Zone information of the server.
        type: str
    restore_point_in_time:
        description:
            - Restore point creation time (ISO8601 format), specifying the time to restore from.
            - Required when C(source_server_resource_id) is specified.
        type: str
    source_server_resource_id:
        description:
            - The source MySQL server id.
            - Required when C(restore_point_in_time) is specified.
        type: str
    backup:
        description:
            - Backup related properties of a server.
        type: dict
        suboptions:
            geo_redundant_backup:
                description:
                    - Whether or not geo redundant backup is enabled.
                type: str
                choices:
                    - Enabled
                    - Disabled
            backup_retention_days:
                description:
                    - Backup retention days for the server.
                type: int
    network:
        description:
            - Network related properties of a server.
        type: dict
        suboptions:
            delegated_subnet_resource_id:
                description:
                    - Delegated subnet resource id used to setup vnet for a server.
                type: str
            private_dns_zone_resource_id:
                description:
                    - Private DNS zone resource id.
                type: str
    high_availability:
        description:
            - High availability related properties of a server.
        type: dict
        suboptions:
            mode:
                description:
                    - High availability mode for a server.
                type: str
                choices:
                    - Disabled
                    - ZoneRedundant
                    - SameZone
            standby_availability_zone:
                description:
                    - Vailability zone of the standby server.
                type: str
    status:
        description:
            Set the server state.
        type: str
        choices:
            - restart
            - start
            - stop
            - failover
    state:
        description:
            - Assert the state of the MySQL Flexible Server. Use C(present) to create or update a server and C(absent) to delete it.
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
- name: Create mysql flexible server
  azure_rm_mysqlflexibleserver:
    resource_group: "{{ resource_group }}"
    name: postflexible{{ rpfx }}
    sku:
      name: Standard_D2ds_v4
      tier: GeneralPurpose
    administrator_login: azureuser
    administrator_login_password: Fred@0329
    location: northeurope
    version: 5.7
    storage:
      storage_size_gb: 128
      iops: 500
      auto_grow: Enabled
    high_availability:
      mode: ZoneRedundant
      standby_availability_zone: 3
    backup:
      backup_retention_days: 7
      geo_redundant_backup: Disabled
    availability_zone: 1

- name: Restore MySQL flexible server from a point-in-time backup
  azure_rm_mysqlflexibleserver:
    resource_group: "{{ resource_group }}"
    name: postflexible-restore{{ rpfx }}
    source_server_resource_id: "{{ mysql_flexible_server_id }}"
    restore_point_in_time: "2026-02-26T02:27:14Z"
'''

RETURN = '''
servers:
    description:
        - The facts of the flexible servers.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxxx-xxxx/resourceGroups/testRG/providers/Microsoft.DBforMySQL/flexibleServers/server01
        resource_group:
            description:
                - Resource group name.
            returned: always
            type: str
            sample: testRG
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: server01
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
                    sample: Standard_D32s_v3
                tier:
                    description:
                        - The tier of the particular SKU.
                    returned: always
                    type: str
                    sample: GeneralPurpose
        storage:
            description:
                - Storage related properties of a server.
            type: complex
            returned: always
            contains:
                storage_size_gb:
                    description:
                        - Max storage size allowed for a server.
                    returned: always
                    type: int
                    sample: 128000
                iops:
                    description:
                        - Storage IOPS for a server.
                    returned: always
                    type: int
                    sample: 684
                auto_grow:
                    description:
                        - Enable Storage Auto Grow or not.
                    returned: always
                    type: str
                    sample: Disabled
        availability_zone:
            description:
                - Availability Zone information of the server.
            returned: always
            type: str
            sample: 1
        administrator_login_password:
            description:
                - The administrator's login name of a server.
            returned: always
            type: str
            sample: serveradmin
        backup:
            description:
                - Backup related properties of a server.
            type: complex
            contains:
                backup_retention_days:
                    description:
                        - Backup retention days for the server.
                    type: int
                    returned: always
                    sample: 7
                geo_redundant_backup:
                    description:
                        - Whether or not geo redundant backup is enabled.
                    type: str
                    returned: always
                    sample: Disabled
        version:
            description:
                - Server version.
            returned: always
            type: str
            sample: "5.7"
        status:
            description:
                - Set server state.
            type: str
            choices:
                - restart
                - start
                - stop
                - failover
        state:
            description:
                - A state of a server that is visible to user.
            returned: always
            type: str
            sample: Ready
        fully_qualified_domain_name:
            description:
                - The fully qualified domain name of a server.
            returned: always
            type: str
            sample: myabdud1223.mys.database.azure.com
        high_availability:
            description:
                - High availability related properties of a server.
            type: complex
            returned: always
            contains:
                mode:
                    description:
                        - High availability mode for a server.
                    type: str
                    sample: Disabled
                    returned: always
                standby_availability_zone:
                    description:
                        - Availability zone of the standby server.
                    type: str
                    sample: Availability zone of the standby server.
                    returned: always
        network:
            description:
                - Network related properties of a server.
            type: complex
            returned: always
            contains:
                delegated_subnet_resource_id:
                    description:
                        - Delegated subnet resource id used to setup vnet for a server.
                    type: str
                    sample: null
                    returned: always
                private_dns_zone_resource_id:
                    description:
                        - Private DNS zone resource id.
                    type: str
                    sample: null
                    returned: always
        restore_point_in_time:
            description:
                - Restore point creation time (ISO8601 format), specifying the time to restore from.
            type: str
            returned: always
            sample: null
        source_server_resource_id:
            description:
                - The source MySQL server id.
            type: str
            returned: always
            sample: null
        tags:
            description:
                - Tags assigned to the resource. Dictionary of string:string pairs.
            type: dict
            returned: always
            sample: { tag1: abc }
        type:
            description:
                - The type of the resource.
            type: str
            returned: always
            sample: Microsoft.DBforMySQL/flexibleServers
'''


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass

storage_spec = dict(
    storage_size_gb=dict(
        type='int'
    ),
    iops=dict(
        type='int'
    ),
    auto_grow=dict(
        type='str',
        choices=['Disabled', 'Enabled']
    )
)


high_availability_spec = dict(
    mode=dict(type='str', choices=["Disabled", "ZoneRedundant", "SameZone"]),
    standby_availability_zone=dict(type='str')
)


sku_spec = dict(
    name=dict(type='str', required=True),
    tier=dict(type='str', required=True, choices=["Burstable", "GeneralPurpose", "MemoryOptimized"])
)


backup_spec = dict(
    backup_retention_days=dict(type='int'),
    geo_redundant_backup=dict(type='str', choices=["Enabled", "Disabled"])
)


network_spec = dict(
    delegated_subnet_resource_id=dict(type='str'),
    private_dns_zone_resource_id=dict(type='str'),
)


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMMySqlFlexibleServers(AzureRMModuleBaseExt):
    """Configuration class for an Azure RM MySQL Flexible Server resource"""

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
            version=dict(
                type='str',
                choices=['5.7', '8.0.21']
            ),
            administrator_login=dict(
                type='str'
            ),
            administrator_login_password=dict(
                type='str',
                no_log=True
            ),
            availability_zone=dict(
                type='str'
            ),
            restore_point_in_time=dict(
                type='str'
            ),
            source_server_resource_id=dict(
                type='str'
            ),
            backup=dict(
                type='dict',
                options=backup_spec
            ),
            network=dict(
                type='dict',
                options=network_spec
            ),
            storage=dict(
                type='dict',
                options=storage_spec
            ),
            high_availability=dict(
                type='dict',
                options=high_availability_spec
            ),
            status=dict(
                type='str',
                choices=['restart', 'start', 'stop', 'failover']
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
        self.status = None
        self.tags = None

        self.results = dict(changed=False)
        self.state = None
        self.to_do = Actions.NoAction

        required_together = [['restore_point_in_time', 'source_server_resource_id']]

        super(AzureRMMySqlFlexibleServers, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          required_together=required_together,
                                                          supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "sku":
                    self.parameters["sku"] = kwargs[key]
                    self.update_parameters["sku"] = kwargs[key]
                elif key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "storage":
                    self.parameters["storage"] = kwargs[key]
                    self.update_parameters["storage"] = kwargs[key]
                elif key == "version":
                    self.parameters["version"] = kwargs[key]
                elif key == "administrator_login":
                    self.parameters["administrator_login"] = kwargs[key]
                elif key == "administrator_login_password":
                    self.parameters["administrator_login_password"] = kwargs[key]
                elif key == 'availability_zone':
                    self.parameters['availability_zone'] = kwargs[key]
                elif key == 'source_server_resource_id':
                    self.parameters['source_server_resource_id'] = kwargs[key]
                elif key == 'restore_point_in_time':
                    self.parameters['restore_point_in_time'] = kwargs[key]
                elif key == 'backup':
                    self.parameters['backup'] = kwargs[key]
                    self.update_parameters['backup'] = kwargs[key]
                elif key == 'high_availability':
                    self.parameters['high_availability'] = kwargs[key]
                    self.update_parameters['high_availability'] = kwargs[key]
                elif key == 'network':
                    self.parameters['network'] = kwargs[key]

        self.parameters['tags'] = self.tags

        # If this is a PointInTimeRestore, set create_mode to PointInTimeRestore
        if self.parameters.get('source_server_resource_id') and self.parameters.get('restore_point_in_time'):
            self.parameters['create_mode'] = 'PointInTimeRestore'

        old_response = None
        response = None
        changed = False

        resource_group = self.get_resource_group(self.resource_group)
        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_mysqlserver()

        if not old_response:
            if self.state == 'absent':
                self.log("The mysql flexible server didn't exist")
            else:
                changed = True
                self.to_do = Actions.Create
        else:
            self.log("MySQL Flexible Server instance already exists")
            if self.state == 'absent':
                changed = True
                self.to_do = Actions.Delete
            else:
                self.log("Whether the MySQL Flexible Server instance need update")
                update_tags, self.update_parameters['tags'] = self.update_tags(old_response.get('tags'))
                if update_tags:
                    changed = True
                    self.to_do = Actions.Update

                for item in ['sku', 'network', 'storage', 'backup', 'high_availability']:
                    if not self.default_compare({}, self.update_parameters.get(item), old_response[item], '', dict(compare=[])):
                        changed = True
                        self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the MySQL Flexible Server instance")

            if not self.check_mode:
                response = self.create_update_mysqlserver()
                self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("MySQL Flexible Server instance deleted")
            if not self.check_mode:
                self.delete_mysqlserver()
        if self.status is not None:
            if self.status == 'start':
                self.start_mysqlserver()
                changed = True
            elif self.status == 'restart':
                self.restart_mysqlserver()
                changed = True
            elif self.status == 'stop':
                self.stop_mysqlserver()
                changed = True
            elif self.status == 'failover':
                self.failover_mysqlserver()
                changed = True
            else:
                pass
        self.results['changed'] = changed
        self.results['state'] = self.get_mysqlserver()
        return self.results

    def failover_mysqlserver(self):
        '''
        Manual failover MySQL Flexible Server.
        '''
        self.log("Failover MySQL Flexible Server instance {0}".format(self.name))

        try:
            response = self.mysql_flexible_client.servers.begin_failover(resource_group_name=self.resource_group,
                                                                         server_name=self.name)
        except Exception as exc:
            self.fail("Error failover mysql flexible server {0} - {1}".format(self.name, str(exc)))
        return True

    def stop_mysqlserver(self):
        '''
        Stop MySQL Flexible Server.
        '''
        self.log("Stop MySQL Flexible Server instance {0}".format(self.name))

        try:
            response = self.mysql_flexible_client.servers.begin_stop(resource_group_name=self.resource_group,
                                                                     server_name=self.name)
        except Exception as exc:
            self.fail("Error stop mysql flexible server {0} - {1}".format(self.name, str(exc)))
        return True

    def start_mysqlserver(self):
        '''
        Start MySQL Flexible Server.
        '''
        self.log("Start MySQL Flexible Server instance {0}".format(self.name))

        try:
            response = self.mysql_flexible_client.servers.begin_start(resource_group_name=self.resource_group,
                                                                      server_name=self.name)
        except Exception as exc:
            self.fail("Error starting mysql flexible server {0} - {1}".format(self.name, str(exc)))
        return True

    def restart_mysqlserver(self):
        '''
        Restart MySQL Flexible Server.
        '''
        self.log("Restart MySQL Flexible Server instance {0}".format(self.name))

        try:
            response = self.mysql_flexible_client.servers.begin_restart(resource_group_name=self.resource_group,
                                                                        server_name=self.name,
                                                                        parameters=dict(restart_with_failover='Enabled',
                                                                                        max_failover_seconds=20))
        except Exception as exc:
            self.fail("Error restarting mysql flexible server {0} - {1}".format(self.name, str(exc)))
        return True

    def create_update_mysqlserver(self):
        '''
        Creates or updates MySQL Flexible Server with the specified configuration.

        :return: deserialized MySQL Flexible Server instance state dictionary
        '''
        self.log("Creating / Updating the MySQL Flexible Server instance {0}".format(self.name))

        try:
            self.parameters['tags'] = self.tags
            if self.to_do == Actions.Create:
                response = self.mysql_flexible_client.servers.begin_create(resource_group_name=self.resource_group,
                                                                           server_name=self.name,
                                                                           parameters=self.parameters)
            else:
                # structure of parameters for update must be changed
                response = self.mysql_flexible_client.servers.begin_update(resource_group_name=self.resource_group,
                                                                           server_name=self.name,
                                                                           parameters=self.update_parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except Exception as exc:
            self.log('Error attempting to create the MySQL Flexible Server instance.')
            self.fail("Error creating the MySQL Flexible Server instance: {0}".format(str(exc)))
        return self.format_item(response)

    def delete_mysqlserver(self):
        '''
        Deletes specified MySQL Flexible Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the MySQL Flexible Server instance {0}".format(self.name))
        try:
            response = self.mysql_flexible_client.servers.begin_delete(resource_group_name=self.resource_group,
                                                                       server_name=self.name)
        except Exception as e:
            self.log('Error attempting to delete the MySQL Flexible Server instance.')
            self.fail("Error deleting the MySQL Flexible Server instance: {0}".format(str(e)))

        return True

    def get_mysqlserver(self):
        '''
        Gets the properties of the specified MySQL Flexible Server.

        :return: deserialized MySQL Flexible Server instance state dictionary
        '''
        self.log("Checking if the MySQL Flexible Server instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mysql_flexible_client.servers.get(resource_group_name=self.resource_group,
                                                              server_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("MySQL Flexible Server instance : {0} found".format(response.name))
        except ResourceNotFoundError as e:
            self.log('Did not find the MySQL Flexible Server instance.')
        if found is True:
            return self.format_item(response)

        return False

    def format_item(self, item):
        results = dict(
            resource_group=self.parse_resource_to_dict(item.id).get('resource_group'),
            id=item.id,
            name=item.name,
            type=item.type,
            tags=item.tags,
            location=item.location,
            sku=dict(),
            administrator_login=item.administrator_login,
            version=item.version,
            availability_zone=item.availability_zone,
            source_server_resource_id=item.source_server_resource_id,
            restore_point_in_time=item.restore_point_in_time,
            state=item.state,
            fully_qualified_domain_name=item.fully_qualified_domain_name,
            storage=dict(),
            backup=dict(),
            high_availability=dict(),
            network=dict(),
        )
        if item.sku not in [None, 'None']:
            results['sku']['name'] = item.sku.name
            results['sku']['tier'] = item.sku.tier
        else:
            results['sku'] = None
        if item.storage not in [None, 'None']:
            results['storage']['storage_size_gb'] = item.storage.storage_size_gb
            results['storage']['iops'] = item.storage.iops
            results['storage']['auto_grow'] = item.storage.auto_grow
        else:
            results['storage'] = None
        if item.high_availability not in [None, 'None']:
            results['high_availability']['standby_availability_zone'] = item.high_availability.standby_availability_zone
            results['high_availability']['mode'] = item.high_availability.mode
        else:
            results['high_availability'] = None
        if item.backup not in [None, 'None']:
            results['backup']['backup_retention_days'] = item.backup.backup_retention_days
            results['backup']['geo_redundant_backup'] = item.backup.geo_redundant_backup
        else:
            results['backup'] = None
        if item.network not in [None, 'None']:
            results['network']['delegated_subnet_resource_id'] = item.network.delegated_subnet_resource_id
            results['network']['private_dns_zone_resource_id'] = item.network.private_dns_zone_resource_id
        else:
            results['network'] = None
        return results


def main():
    """Main execution"""
    AzureRMMySqlFlexibleServers()


if __name__ == '__main__':
    main()
