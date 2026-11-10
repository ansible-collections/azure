#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_cosmosdbmongocollection_info
version_added: "4.3.0"
short_description: Get Cosmos DB MongoDB collection facts
description:
    - Get one MongoDB collection or list collections in an existing Cosmos DB MongoDB database.
    - Optionally retrieve dedicated throughput for each returned collection.
options:
    resource_group:
        description: Resource group containing the Cosmos DB account.
        type: str
        required: true
    account_name:
        description: Cosmos DB account name configured for MongoDB.
        type: str
        required: true
    database_name:
        description: Existing MongoDB database name.
        type: str
        required: true
    name:
        description: Return only this collection. When omitted, list database collections.
        type: str
    retrieve_throughput:
        description: Retrieve the dedicated throughput settings for each collection.
        type: bool
        default: false
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get one collection with throughput
  azure.azcollection.azure_rm_cosmosdbmongocollection_info:
    resource_group: analytics
    account_name: mongo-account
    database_name: events
    name: records
    retrieve_throughput: true

- name: List collections in a MongoDB database
  azure.azcollection.azure_rm_cosmosdbmongocollection_info:
    resource_group: analytics
    account_name: mongo-account
    database_name: events
'''

RETURN = '''
collections:
    description: List of MongoDB collections and, optionally, dedicated throughput settings.
    returned: always
    type: list
    elements: dict
    sample: [{"name": "records", "resource": {"id": "records", "shard_key": {"tenantId": "Hash"}}}]
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMCosmosDBMongoCollectionInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            account_name=dict(type='str', required=True),
            database_name=dict(type='str', required=True),
            name=dict(type='str'),
            retrieve_throughput=dict(type='bool', default=False),
        )
        self.results = dict(changed=False, collections=[])
        super(AzureRMCosmosDBMongoCollectionInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True,
            supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.client = self.cosmosdb_client.mongo_db_resources
        args = (self.resource_group, self.account_name, self.database_name)
        if self.name:
            try:
                resources = [self.client.get_mongo_db_collection(*args, self.name)]
            except ResourceNotFoundError:
                resources = []
            except Exception as exc:
                self.fail('Error retrieving MongoDB collection {0}: {1}'.format(self.name, exc))
        else:
            try:
                resources = list(self.client.list_mongo_db_collections(*args))
            except Exception as exc:
                self.fail('Error listing MongoDB collections in database {0}: {1}'.format(self.database_name, exc))
        self.results['collections'] = [self._format(resource, args) for resource in resources]
        return self.results

    def _format(self, resource, args):
        result = resource.as_dict()
        if self.retrieve_throughput:
            try:
                result['throughput'] = self.client.get_mongo_db_collection_throughput(
                    *(args + (result['name'],))).as_dict()
            except ResourceNotFoundError:
                result['throughput'] = None
            except Exception as exc:
                self.fail('Error retrieving throughput for collection {0}: {1}'.format(result.get('name'), exc))
        return result


def main():
    AzureRMCosmosDBMongoCollectionInfo()


if __name__ == '__main__':
    main()
