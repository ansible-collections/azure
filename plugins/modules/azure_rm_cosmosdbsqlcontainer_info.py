#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_cosmosdbsqlcontainer_info
version_added: "4.3.0"
short_description: Get Cosmos DB SQL container facts
description:
    - Get one SQL container or list the containers in an existing Cosmos DB SQL database.
    - Optionally retrieve dedicated throughput for each returned container.
options:
    resource_group:
        description: Resource group containing the Cosmos DB account.
        type: str
        required: true
    account_name:
        description: Cosmos DB account name.
        type: str
        required: true
    database_name:
        description: Existing SQL database name.
        type: str
        required: true
    name:
        description: Return only this container. When omitted, list the database's containers.
        type: str
    retrieve_throughput:
        description: Retrieve the dedicated throughput settings for each container.
        type: bool
        default: false
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get one container with its dedicated throughput
  azure.azcollection.azure_rm_cosmosdbsqlcontainer_info:
    resource_group: analytics
    account_name: example-account
    database_name: events
    name: records
    retrieve_throughput: true

- name: List containers in a database
  azure.azcollection.azure_rm_cosmosdbsqlcontainer_info:
    resource_group: analytics
    account_name: example-account
    database_name: events
'''

RETURN = '''
containers:
    description: List of SQL containers and, optionally, dedicated throughput settings.
    returned: always
    type: list
    elements: dict
    sample: [{"name": "records", "resource": {"id": "records", "indexing_policy": {"indexing_mode": "consistent"}}}]
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMCosmosDBSqlContainerInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            account_name=dict(type='str', required=True),
            database_name=dict(type='str', required=True),
            name=dict(type='str'),
            retrieve_throughput=dict(type='bool', default=False),
        )
        self.results = dict(changed=False, containers=[])
        super(AzureRMCosmosDBSqlContainerInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True,
            supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.client = self.cosmosdb_client.sql_resources
        args = (self.resource_group, self.account_name, self.database_name)
        if self.name:
            try:
                resources = [self.client.get_sql_container(*args, self.name)]
            except ResourceNotFoundError:
                resources = []
            except Exception as exc:
                self.fail('Error retrieving SQL container {0}: {1}'.format(self.name, exc))
        else:
            try:
                resources = list(self.client.list_sql_containers(*args))
            except Exception as exc:
                self.fail('Error listing SQL containers in database {0}: {1}'.format(self.database_name, exc))
        self.results['containers'] = [self._format(resource, args) for resource in resources]
        return self.results

    def _format(self, resource, args):
        result = resource.as_dict()
        if self.retrieve_throughput:
            try:
                result['throughput'] = self.client.get_sql_container_throughput(
                    *(args + (result['name'],))).as_dict()
            except ResourceNotFoundError:
                result['throughput'] = None
            except Exception as exc:
                self.fail('Error retrieving throughput for container {0}: {1}'.format(result.get('name'), exc))
        return result


def main():
    AzureRMCosmosDBSqlContainerInfo()


if __name__ == '__main__':
    main()
