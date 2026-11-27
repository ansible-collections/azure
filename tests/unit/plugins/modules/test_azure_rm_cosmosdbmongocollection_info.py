from types import SimpleNamespace
from unittest.mock import MagicMock

from azure.core.exceptions import ResourceNotFoundError

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_cosmosdbmongocollection_info import AzureRMCosmosDBMongoCollectionInfo


def module(resources=None, not_found=False):
    obj = AzureRMCosmosDBMongoCollectionInfo.__new__(AzureRMCosmosDBMongoCollectionInfo)
    obj.module_arg_spec = dict.fromkeys(('resource_group', 'account_name', 'database_name', 'name', 'retrieve_throughput'))
    obj.results = dict(changed=False, collections=[])
    client = MagicMock()
    if not_found:
        client.get_mongo_db_collection.side_effect = ResourceNotFoundError('missing')
    else:
        client.list_mongo_db_collections.return_value = resources or []
    obj._cosmosdb_client = SimpleNamespace(mongo_db_resources=client)
    obj.module = SimpleNamespace(debug=MagicMock())

    def fail(message):
        raise ValueError(message)
    obj.fail = MagicMock(side_effect=fail)
    return obj, client


def params(**overrides):
    values = dict(resource_group='rg', account_name='account', database_name='db', name=None,
                  retrieve_throughput=False)
    values.update(overrides)
    return values


def test_mongo_collection_info_list_and_throughput():
    collection = SimpleNamespace(as_dict=lambda: {'name': 'events', 'resource': {'id': 'events'}})
    obj, client = module([collection])
    throughput = SimpleNamespace(as_dict=lambda: {'resource': {'throughput': 400}})
    client.get_mongo_db_collection_throughput.return_value = throughput
    result = obj.exec_module(**params(retrieve_throughput=True))
    assert result['collections'][0]['name'] == 'events'
    assert result['collections'][0]['throughput']['resource']['throughput'] == 400
    client.list_mongo_db_collections.assert_called_once_with('rg', 'account', 'db')


def test_mongo_collection_info_missing_name_is_empty():
    obj = module(not_found=True)[0]
    assert obj.exec_module(**params(name='missing'))['collections'] == []
