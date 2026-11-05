#!/usr/bin/python
#
# Copyright (c) 2026
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_cosmosdbmongocollection
version_added: "4.3.0"
short_description: Manage a Cosmos DB MongoDB collection
description:
    - Create, update, or delete a MongoDB collection in an existing Cosmos DB database.
    - Reconcile shard keys and secondary indexes, and scale dedicated manual or autoscale throughput.
options:
    resource_group:
        description: Resource group containing the Cosmos DB account.
        required: true
        type: str
    account_name:
        description: Cosmos DB account name configured for MongoDB.
        required: true
        type: str
    database_name:
        description: Existing MongoDB database name.
        required: true
        type: str
    name:
        description: Collection name.
        required: true
        type: str
    shard_key:
        description:
            - Mapping of shard-key field names to their shard-key kind.
            - Required when creating a collection; immutable after creation.
        type: dict
    indexes:
        description: MongoDB indexes to set on the collection. Omit to preserve existing indexes.
        type: list
        elements: dict
        suboptions:
            keys:
                description: Index key paths, for example C(_id) or C(tenantId).
                type: list
                elements: str
                required: true
            unique:
                description: Whether the index enforces uniqueness.
                type: bool
            expire_after_seconds:
                description: TTL expiration for a TTL index.
                type: int
    throughput:
        description: Dedicated manual throughput in request units per second.
        type: int
    autoscale_max_throughput:
        description: Maximum dedicated autoscale throughput in request units per second.
        type: int
    state:
        description: Desired state of the collection.
        type: str
        choices: [present, absent]
        default: present
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - OpenAI (@openai)
'''

EXAMPLES = '''
- name: Create a sharded collection with an index
  azure.azcollection.azure_rm_cosmosdbmongocollection:
    resource_group: analytics
    account_name: mongo-account
    database_name: events
    name: records
    shard_key:
      tenantId: Hash
    indexes:
      - keys: [_id]
        unique: true
      - keys: [tenantId, timestamp]
    autoscale_max_throughput: 4000
'''

RETURN = '''
collection:
    description: MongoDB collection definition returned by the Azure management API.
    returned: when I(state=present) and not in check mode
    type: dict
    sample: {"name": "records", "resource": {"id": "records", "shardKey": {"tenantId": "Hash"}}}
'''

import copy

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.mgmt.cosmosdb import CosmosDBManagementClient
    from azure.mgmt.cosmosdb import models
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMCosmosDBMongoCollection(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            account_name=dict(type='str', required=True),
            database_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            shard_key=dict(type='dict', no_log=False),
            indexes=dict(type='list', elements='dict', options=dict(
                keys=dict(type='list', elements='str', required=True, no_log=False),
                unique=dict(type='bool'),
                expire_after_seconds=dict(type='int'),
            )),
            throughput=dict(type='int'),
            autoscale_max_throughput=dict(type='int'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )
        super(AzureRMCosmosDBMongoCollection, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=False,
            mutually_exclusive=[('throughput', 'autoscale_max_throughput')])

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.client = self.get_mgmt_svc_client(
            CosmosDBManagementClient, base_url=self._cloud_environment.endpoints.resource_manager).mongo_db_resources
        args = (self.resource_group, self.account_name, self.database_name, self.name)
        try:
            existing = self.client.get_mongo_db_collection(*args)
        except ResourceNotFoundError:
            existing = None
        except Exception as exc:
            self.fail('Error retrieving MongoDB collection {0}: {1}'.format(self.name, exc))

        if self.state == 'absent':
            if existing and not self.check_mode:
                try:
                    self.get_poller_result(self.client.begin_delete_mongo_db_collection(*args))
                except Exception as exc:
                    self.fail('Error deleting MongoDB collection {0}: {1}'.format(self.name, exc))
            return dict(changed=existing is not None)

        if existing is None and not self.shard_key:
            self.fail('shard_key is required when creating a collection')
        if existing and self.shard_key is not None and self.shard_key != existing.resource.shard_key:
            self.fail('shard_key cannot be changed on an existing collection')
        if self.throughput is not None and self.throughput <= 0:
            self.fail('throughput must be positive')
        if self.autoscale_max_throughput is not None and self.autoscale_max_throughput <= 0:
            self.fail('autoscale_max_throughput must be positive')
        throughput_changed = self._throughput_needs_update(args, existing)
        resource = copy.deepcopy(existing.resource) if existing else models.MongoDBCollectionResource(
            id=self.name, shard_key=self.shard_key)
        if self.indexes is not None:
            resource.indexes = [models.MongoIndex(
                key=models.MongoIndexKeys(keys=index['keys']),
                options=models.MongoIndexOptions(
                    unique=index.get('unique'), expire_after_seconds=index.get('expire_after_seconds')))
                for index in self.indexes]
        old = existing.resource.as_dict() if existing else None
        new = resource.as_dict()
        if existing:
            for key in ('_rid', '_ts', '_etag'):
                old.pop(key, None)
                new.pop(key, None)
        resource_changed = existing is None or old != new
        if self.check_mode:
            return dict(changed=resource_changed or throughput_changed)
        try:
            if resource_changed:
                options = None
                if existing is None and (self.throughput is not None or self.autoscale_max_throughput is not None):
                    options = models.CreateUpdateOptions(
                        throughput=self.throughput,
                        autoscale_settings=models.AutoscaleSettings(max_throughput=self.autoscale_max_throughput)
                        if self.autoscale_max_throughput is not None else None)
                existing = self.get_poller_result(self.client.begin_create_update_mongo_db_collection(
                    *args, create_update_mongo_db_collection_parameters=models.MongoDBCollectionCreateUpdateParameters(
                        resource=resource, options=options)))
            if throughput_changed:
                value = models.ThroughputSettingsResource(
                    throughput=self.throughput,
                    autoscale_settings=models.AutoscaleSettingsResource(max_throughput=self.autoscale_max_throughput)
                    if self.autoscale_max_throughput is not None else None)
                self.get_poller_result(self.client.begin_update_mongo_db_collection_throughput(
                    *args, update_throughput_parameters=models.ThroughputSettingsUpdateParameters(resource=value)))
        except Exception as exc:
            self.fail('Error updating MongoDB collection {0}: {1}'.format(self.name, exc))
        return dict(changed=resource_changed or throughput_changed,
                    collection=existing.as_dict() if existing is not None else {})

    def _throughput_needs_update(self, args, existing):
        desired = self.throughput if self.throughput is not None else self.autoscale_max_throughput
        if desired is None or existing is None:
            return False
        if desired <= 0:
            self.fail('throughput values must be positive')
        try:
            current = self.client.get_mongo_db_collection_throughput(*args).resource
        except ResourceNotFoundError:
            self.fail('Collection has no dedicated throughput; shared throughput cannot be updated here')
        except Exception as exc:
            self.fail('Error retrieving collection throughput: {0}'.format(exc))
        autoscale = current.autoscale_settings
        if (autoscale is not None) != (self.autoscale_max_throughput is not None):
            self.fail('Changing throughput mode is not supported; migrate collection throughput first')
        return desired != (autoscale.max_throughput if autoscale else current.throughput)


def main():
    AzureRMCosmosDBMongoCollection()


if __name__ == '__main__':
    main()
