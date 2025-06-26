#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_postgresqlflexiblevirtualendpoint_info
version_added: "3.6.0"
short_description: Get or list Azure PostgreSQL Flexible Virtual Endpoints facts
description:
    - Get or list facts of PostgreSQL Flexible Virtual Endpoints.

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
    virtual_endpoint_name:
        description:
            - The name of the post gresql virtual endpoint.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: List instance of PostgreSQL Flexible Virtual Endpoints by server name
  azure_rm_postgresqlflexiblevirtualendpoint_info:
    resource_group: myResourceGroup
    server_name: server_name

- name: Get instances of PostgreSQL Flexible Virtual Endpoints
  azure_rm_postgresqlflexiblevirtualendpoint_info:
    resource_group: myResourceGroup
    server_name: server_name
    virutal_endpoint_name: vendpoint
'''

RETURN = '''
virtual_endpoints:
    description:
        - A list of dictionaries containing facts for PostgreSQL Flexible Virtual Endpoints.
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
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPostgreSqlFlexibleVirtualEndpointInfo(AzureRMModuleBase):
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
            virtual_endpoint_name=dict(
                type='str'
            ),
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.virtual_endpoint_name = None
        self.server_name = None
        super(AzureRMPostgreSqlFlexibleVirtualEndpointInfo, self).__init__(self.module_arg_spec,
                                                                           supports_check_mode=True,
                                                                           supports_tags=False,
                                                                           facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.virtual_endpoint_name:
            self.results['virtual_endpoints'] = self.get()
        else:
            self.results['virtual_endpoints'] = self.list_all()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.virtual_endpoints.get(resource_group_name=self.resource_group,
                                                                             server_name=self.server_name,
                                                                             virtual_endpoint_name=self.virtual_endpoint_name)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError:
            self.log('Could not get virtual endpoint facts for PostgreSQL Flexible Server.')

        if response:
            results.append(self.format_item(response))

        return results

    def list_all(self):
        response = None
        results = []
        try:
            response = self.postgresql_flexible_client.virtual_endpoints.list_by_server(resource_group_name=self.resource_group,
                                                                                        server_name=self.server_name)
            self.log("Response : {0}".format(response))
        except Exception as ec:
            self.log('Could not list virtual endpoints facts for PostgreSQL Flexible Servers.')

        if response:
            for item in response:
                results.append(self.format_item(item))

        return results

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
    AzureRMPostgreSqlFlexibleVirtualEndpointInfo()


if __name__ == '__main__':
    main()
