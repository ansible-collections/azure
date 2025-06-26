#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexiblebackup_info
version_added: "3.6.0"
short_description: Get Azure PostgreSQL Flexible Backup facts
description:
    - Get or list facts of PostgreSQL Flexible Backup.

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
    backup_name:
        description:
            - The name of the post gresql backup.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: List instance of PostgreSQL Flexible Backup by server name
  azure_rm_postgresqlflexiblebackup_info:
    resource_group: myResourceGroup
    server_name: server_name

- name: Get instances of PostgreSQL Flexible Backup
  azure_rm_postgresqlflexiblebackup_info:
    resource_group: myResourceGroup
    server_name: server_name
    name: backup_name
'''

RETURN = '''
backup:
    description:
        - A list of dictionaries containing facts for PostgreSQL Flexible Backup.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource ID for the resource.
            returned: always
            type: str
            sample: "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.DBforPostgreSQL/flexibleServers/posttest/backups/fredbackup"
        backup_name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: fredbackup
        server_name:
            description:
                - The post gresql flexible server name.
            returned: always
            type: str
            sample: posttest
        resource_group:
            description:
                - Name of the resource group.
            returned: always
            type: str
            sample: testRG
        type:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: Microsoft.DBforPostgreSQL/flexibleServers/backups
        completed_time:
            description:
                - Backup completed time (ISO8601 format).
            type: str
            returned: always
            sample: "2025-04-17T08:11:58.756273+00:00"
        backup_type:
            description:
                - Backup type.
            type: str
            returned: always
            sample: Full
        source:
            description:
                - Backup source.
            type: str
            returned: always
            sample: Automatic
'''


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPostgreSqlFlexibleBackupInfo(AzureRMModuleBase):
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
            backup_name=dict(
                type='str'
            ),
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.backup_name = None
        self.server_name = None
        super(AzureRMPostgreSqlFlexibleBackupInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.backup_name:
            self.results['backups'] = self.get()
        else:
            self.results['backups'] = self.list_all()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.backups.get(resource_group_name=self.resource_group,
                                                                   server_name=self.server_name,
                                                                   backup_name=self.backup_name)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError:
            self.log('Could not get backup facts for PostgreSQL Flexible Server.')

        if response:
            results.append(self.format_item(response))

        return results

    def list_all(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.backups.list_by_server(resource_group_name=self.resource_group,
                                                                              server_name=self.server_name)
            self.log("Response : {0}".format(response))
        except Exception as ec:
            self.log('Could not list backups facts for PostgreSQL Flexible Servers.')

        if response:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        return dict(
            resource_group=self.resource_group,
            server_name=self.server_name,
            backup_type=item.backup_type,
            completed_time=item.completed_time,
            id=item.id,
            name=item.name,
            source=item.source,
            type=item.type
        )


def main():
    AzureRMPostgreSqlFlexibleBackupInfo()


if __name__ == '__main__':
    main()
