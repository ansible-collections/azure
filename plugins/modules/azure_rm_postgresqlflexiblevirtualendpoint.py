#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexiblevirtualendpoint
version_added: "3.6.0"
short_description: Manage PostgreSQL Flexible virtualendpoint instance
description:
    - Create or delete instance of PostgreSQL Flexible virtualendpoint.

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
    virtual_endpoint_name:
        description:
            - The name of the post gresql flexible virtual endpoint.
        required: True
        type: str
    members:
        description:
            - List of virtual endpoints for a server.
            - The names are the same with I(server_name).
        type: list
        elements: str
    endpoint_type:
        description:
            - The endpoint type for the virtual endpoint.
        type: str
        choices:
            - ReadWrite
    state:
        description:
            - Assert the state of the PostgreSQL Flexible virtualendpoint. Use C(present) to create or update a virtualendpoint and C(absent) to delete it.
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
- name: Create (or update) PostgreSQL Flexible virtualendpoint
  azure_rm_postgresqlflexiblevirtualendpoint:
    resource_group: myResourceGroup
    server_name: testserver
    name: db1
    charset: UTF8
    collation: en_US.utf8

- name: Delete PostgreSQL Flexible virtualendpoint
  azure_rm_postgresqlflexiblevirtualendpoint:
    resource_group: myResourceGroup
    server_name: testserver
    virtual_endpoint_name: vendpoint01
'''

RETURN = '''
virtual_endpoint:
    description:
        - A list of dictionaries containing facts for PostgreSQL Flexible virtual endpoint.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID of the postgresql flexible virtual endpoints.
            returned: always
            type: str
            sample: "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.DBforPostgreSQL/flexibleServers/postsql01/virtualendpoints/vendpoint"
        virtual_endpoint_name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: vendpoint
        endpoint_type:
            description:
                - The endpoint type for the virtual endpoint.
            returned: always
            type: str
            sample: ReadWrite
        resource_group:
            description:
                - The resoure group name.
            returned: always
            type: str
            sample: myResourceGroup
        members:
            description:
                - List of members for a virtual endpoint.
            returned: always
            type: list
            sample: ['postsqlrpfx01']
        server_name:
            description:
                - The Post gresql flexibeserver name.
            returned: always
            type: str
            sample: postsql01
        virtual_endpoints:
            description:
                - List of virtual endpoints for a server.
            returned: always
            type: list
            sample: ["vendpoint.writer.postgres.database.azure.com", "vendpoint.reader.postgres.database.azure.com"]
        type:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: Microsoft.DBforPostgreSQL/flexibleServers/virtualendpoints
'''


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPostgreSqlFlexibleVirtualEndpoint(AzureRMModuleBase):
    """Configuration class for an Azure RM PostgreSQL Flexible virtualendpoint resource"""

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
            virtual_endpoint_name=dict(
                type='str',
                required=True
            ),
            endpoint_type=dict(
                type='str',
                choices=['ReadWrite']
            ),
            members=dict(
                type='list',
                elements='str',
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.virtual_endpoint_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.state = None

        super(AzureRMPostgreSqlFlexibleVirtualEndpoint, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        old_response = self.get_postgresqlflexiblevirtualendpoint()

        if not old_response:
            self.log("PostgreSQL Flexible virtualendpoint instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                changed = True
                if not self.check_mode:
                    response = self.create_postgresqlflexiblevirtualendpoint(self.parameters)
        else:
            self.log("PostgreSQL Flexible virtualendpoint instance already exists")
            if self.state == 'absent':
                changed = True
                if not self.check_mode:
                    response = self.delete_postgresqlflexiblevirtualendpoint()
            else:
                if self.check_mode:
                    changed = True
                response = old_response

        self.results['virtualendpoint'] = response
        self.results['changed'] = changed
        return self.results

    def create_postgresqlflexiblevirtualendpoint(self, body):
        '''
        Creates PostgreSQL Flexible virtualendpoint with the specified configuration.

        :return: deserialized PostgreSQL Flexible virtualendpoint instance state dictionary
        '''
        self.log("Creating the PostgreSQL Flexible virtualendpoint instance {0}".format(self.virtual_endpoint_name))

        try:
            response = self.postgresql_flexible_client.virtual_endpoints.begin_create(resource_group_name=self.resource_group,
                                                                                      server_name=self.server_name,
                                                                                      virtual_endpoint_name=self.virtual_endpoint_name,
                                                                                      parameters=body)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

        except Exception as exc:
            self.log('Error attempting to create the PostgreSQL Flexible virtualendpoint instance.')
            self.fail("Error creating the PostgreSQL Flexible virtualendpoint instance: {0}".format(str(exc)))
        return self.format_item(response)

    def delete_postgresqlflexiblevirtualendpoint(self):
        '''
        Deletes specified PostgreSQL Flexible virtualendpoint instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the PostgreSQL Flexible virtualendpoint instance {0}".format(self.virtual_endpoint_name))
        try:
            self.postgresql_flexible_client.virtual_endpoints.begin_delete(resource_group_name=self.resource_group,
                                                                           server_name=self.server_name,
                                                                           virtual_endpoint_name=self.virtual_endpoint_name)
        except Exception as ec:
            self.log('Error attempting to delete the PostgreSQL Flexible virtualendpoint instance.')
            self.fail("Error deleting the PostgreSQL Flexible virtualendpoint instance: {0}".format(str(ec)))

    def get_postgresqlflexiblevirtualendpoint(self):
        '''
        Gets the properties of the specified PostgreSQL Flexible virtualendpoint.

        :return: deserialized PostgreSQL Flexible virtualendpoint instance state dictionary
        '''
        self.log("Checking if the PostgreSQL Flexible virtualendpoint instance {0} is present".format(self.virtual_endpoint_name))
        found = False
        try:
            response = self.postgresql_flexible_client.virtual_endpoints.get(resource_group_name=self.resource_group,
                                                                             server_name=self.server_name,
                                                                             virtual_endpoint_name=self.virtual_endpoint_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("PostgreSQL Flexible virtualendpoint instance : {0} found".format(response.name))
        except ResourceNotFoundError as e:
            self.log('Did not find the PostgreSQL Flexible virtualendpoint instance. Exception as {0}'.format(e))
        if found is True:
            return self.format_item(response)

        return None

    def format_item(self, item):
        return dict(
            resource_group=self.resource_group,
            server_name=self.server_name,
            id=item.id,
            endpoint_type=item.endpoint_type,
            members=item.members,
            virtual_endpoint_name=item.name,
            type=item.type,
            virtual_endpoints=item.virtual_endpoints
        )


def main():
    """Main execution"""
    AzureRMPostgreSqlFlexibleVirtualEndpoint()


if __name__ == '__main__':
    main()
