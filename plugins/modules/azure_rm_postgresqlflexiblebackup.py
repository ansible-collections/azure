#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexibledBackup
version_added: "2.2.0"
short_description: Manage PostgreSQL Flexible Backup instance
description:
    - Create, update and delete instance of PostgreSQL Flexible Backup.

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
            - The name of the backup.
        required: True
        type: str
    charset:
        description:
            - The charset of the backup.
        type: str
    collation:
        description:
            - The collation of the backup.
        type: str
    state:
        description:
            - Assert the state of the PostgreSQL Flexible backup. Use C(present) to create or update a backup and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Create (or update) PostgreSQL Flexible Backup
  azure_rm_postgresqlflexibledBackup:
    resource_group: myResourceGroup
    server_name: testserver
    name: db1
    charset: UTF8
    collation: en_US.utf8

- name: Delete PostgreSQL Flexible Backup
  azure_rm_postgresqlflexibledBackup:
    resource_group: myResourceGroup
    server_name: testserver
    name: db1
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
                - Resource ID of the postgresql flexible backup.
            returned: always
            type: str
            sample: "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.DBforPostgreSQL/flexibleServers/postfle9/backups/fredbackup"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: fredbackup
        charset:
            description:
                - The charset of the backup.
            returned: always
            type: str
            sample: UTF-8
        collation:
            description:
                - The collation of the backup.
            returned: always
            type: str
            sample: en_US.utf8
        type:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: Microsoft.DBforPostgreSQL/flexibleServers/backups
'''


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPostgreSqlFlexibleBackup(AzureRMModuleBase):
    """Configuration class for an Azure RM PostgreSQL Flexible Backup resource"""

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
            name=dict(
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.state = None

        super(AzureRMPostgreSqlFlexibleBackup, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        old_response = self.get_postgresqlflexiblebackup()

        if not old_response:
            self.log("PostgreSQL Flexible Backup instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                changed = True
                if not self.check_mode:
                    response = self.create_update_postgresqlflexiblebackup(self.parameters)
        else:
            self.log("PostgreSQL Flexible Backup instance already exists")
            if self.state == 'absent':
                changed = True
                if not self.check_mode:
                    response = self.delete_postgresqlflexiblebackup()
            else:
                if not self.default_compare({}, self.parameters, old_response, '', dict(compare=[])):
                    changed = True
                    if not self.check_mode:
                        self.fail("The Post Gresql Flexible backup not support to update")
                else:
                    response = old_response

        self.results['backup'] = response
        self.results['changed'] = changed
        return self.results

    def create_update_postgresqlflexiblebackup(self, body):
        '''
        Creates or updates PostgreSQL Flexible Backup with the specified configuration.

        :return: deserialized PostgreSQL Flexible Backup instance state dictionary
        '''
        self.log("Creating / Updating the PostgreSQL Flexible Backup instance {0}".format(self.name))

        try:
            response = self.postgresql_flexible_client.backups.begin_create(resource_group_name=self.resource_group,
                                                                            server_name=self.server_name,
                                                                            name=self.name)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except Exception as exc:
            self.log('Error attempting to create the PostgreSQL Flexible Backup instance.')
            self.fail("Error creating the PostgreSQL Flexible Backup instance: {0}".format(str(exc)))
        return self.format_item(response)

    def delete_postgresqlflexiblebackup(self):
        '''
        Deletes specified PostgreSQL Flexible Backup instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the PostgreSQL Flexible Backup instance {0}".format(self.name))
        try:
            self.postgresql_flexible_client.backups.begin_delete(resource_group_name=self.resource_group,
                                                                 server_name=self.server_name,
                                                                 name=self.name)
        except Exception as ec:
            self.log('Error attempting to delete the PostgreSQL Flexible Backup instance.')
            self.fail("Error deleting the PostgreSQL Flexible Backup instance: {0}".format(str(ec)))

    def get_postgresqlflexiblebackup(self):
        '''
        Gets the properties of the specified PostgreSQL Flexible Backup.

        :return: deserialized PostgreSQL Flexible Backup instance state dictionary
        '''
        self.log("Checking if the PostgreSQL Flexible Backup instance {0} is present".format(self.name))
        found = False
        try:
            response = self.postgresql_flexible_client.backups.get(resource_group_name=self.resource_group,
                                                                   server_name=self.server_name,
                                                                   name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("PostgreSQL Flexible Backup instance : {0} found".format(response.name))
        except ResourceNotFoundError as e:
            self.log('Did not find the PostgreSQL Flexible Backup instance. Exception as {0}'.format(e))
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
    AzureRMPostgreSqlFlexibleBackup()


if __name__ == '__main__':
    main()
