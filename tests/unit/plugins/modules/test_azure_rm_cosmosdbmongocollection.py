from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.cosmosdb import models

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_cosmosdbmongocollection import AzureRMCosmosDBMongoCollection


def module(existing=None, check_mode=False):
    obj = AzureRMCosmosDBMongoCollection.__new__(AzureRMCosmosDBMongoCollection)
    obj.module_arg_spec = dict.fromkeys(('resource_group', 'account_name', 'database_name', 'name', 'shard_key',
                                         'indexes', 'throughput', 'autoscale_max_throughput', 'state'))
    obj.results = dict(changed=False)
    client = MagicMock()
    if existing is None:
        client.get_mongo_db_collection.side_effect = ResourceNotFoundError('missing')
    else:
        client.get_mongo_db_collection.return_value = existing
    obj._cosmosdb_client = SimpleNamespace(mongo_db_resources=client)
    obj.module = SimpleNamespace(debug=MagicMock())
    obj.check_mode = check_mode
    obj.get_poller_result = MagicMock(side_effect=lambda poller: poller.result())

    def fail(message):
        raise ValueError(message)
    obj.fail = MagicMock(side_effect=fail)
    return obj, client


def params(**overrides):
    values = dict(resource_group='rg', account_name='account', database_name='db', name='collection',
                  shard_key=None, indexes=None, throughput=None, autoscale_max_throughput=None, state='present')
    values.update(overrides)
    return values


def existing_collection():
    return models.MongoDBCollectionGetResults(resource=models.MongoDBCollectionGetPropertiesResource(
        id='collection', shard_key={'tenant': 'Hash'}, indexes=[models.MongoIndex(
            key=models.MongoIndexKeys(keys=['_id']))]))


def test_create_mongo_collection_with_indexes_and_throughput():
    obj, client = module()
    client.begin_create_update_mongo_db_collection.return_value.result.return_value = existing_collection()
    arguments = params(shard_key={'tenant': 'Hash'}, indexes=[{'keys': ['_id'], 'unique': True}],
                       throughput=400)
    result = obj.exec_module(**arguments)
    assert result['changed']
    call = client.begin_create_update_mongo_db_collection.call_args.kwargs
    assert call['create_update_mongo_db_collection_parameters'].resource.shard_key == {'tenant': 'Hash'}
    assert call['create_update_mongo_db_collection_parameters'].options.throughput == 400


def test_creation_requires_shard_key():
    obj, client = module()
    with pytest.raises(ValueError, match='shard_key is required'):
        obj.exec_module(**params())
    client.begin_create_update_mongo_db_collection.assert_not_called()


def test_index_update_and_shard_key_immutability():
    obj, client = module(existing_collection(), check_mode=True)
    assert obj.exec_module(**params(indexes=[{'keys': ['tenant'], 'unique': False}]))['changed']
    client.begin_create_update_mongo_db_collection.assert_not_called()


def test_default_id_index_is_idempotent_when_api_omits_unique_option():
    obj, client = module(existing_collection())
    result = obj.exec_module(**params(indexes=[{'keys': ['_id'], 'unique': True}]))
    assert not result['changed']
    client.begin_create_update_mongo_db_collection.assert_not_called()
    obj, client = module(existing_collection())
    with pytest.raises(ValueError, match='shard_key cannot be changed'):
        obj.exec_module(**params(shard_key={'other': 'Hash'}))
    client.begin_create_update_mongo_db_collection.assert_not_called()


def test_reordered_indexes_are_idempotent():
    collection = models.MongoDBCollectionGetResults(resource=models.MongoDBCollectionGetPropertiesResource(
        id='collection', shard_key={'tenant': 'Hash'}, indexes=[
            models.MongoIndex(key=models.MongoIndexKeys(keys=['_id']),
                              options=models.MongoIndexOptions(unique=True)),
            models.MongoIndex(key=models.MongoIndexKeys(keys=['tenant'])),
        ]))
    obj, client = module(collection)
    result = obj.exec_module(**params(indexes=[{'keys': ['tenant']}, {'keys': ['_id'], 'unique': True}]))
    assert not result['changed']
    client.begin_create_update_mongo_db_collection.assert_not_called()


def test_ttl_and_plain_indexes_compare_safely():
    collection = models.MongoDBCollectionGetResults(resource=models.MongoDBCollectionGetPropertiesResource(
        id='collection', shard_key={'tenant': 'Hash'}, indexes=[
            models.MongoIndex(key=models.MongoIndexKeys(keys=['_id']),
                              options=models.MongoIndexOptions(unique=True)),
            models.MongoIndex(key=models.MongoIndexKeys(keys=['created']),
                              options=models.MongoIndexOptions(expire_after_seconds=3600)),
        ]))
    obj, client = module(collection)
    result = obj.exec_module(**params(indexes=[{'keys': ['created'], 'expire_after_seconds': 3600},
                                               {'keys': ['_id'], 'unique': True}]))
    assert not result['changed']
    client.begin_create_update_mongo_db_collection.assert_not_called()


@pytest.mark.parametrize('current,desired', [(400, 800), (4000, 6000)])
def test_scale_manual_and_autoscale_throughput(current, desired):
    autoscale = current > 1000
    resource = models.ThroughputSettingsResource(
        throughput=None if autoscale else current,
        autoscale_settings=models.AutoscaleSettingsResource(max_throughput=current) if autoscale else None)
    obj, client = module(existing_collection())
    client.get_mongo_db_collection_throughput.return_value.resource = resource
    setting = {'autoscale_max_throughput': desired} if autoscale else {'throughput': desired}
    assert obj.exec_module(**params(**setting))['changed']
    client.begin_update_mongo_db_collection_throughput.assert_called_once()
    client.begin_create_update_mongo_db_collection.assert_not_called()
