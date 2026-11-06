from types import SimpleNamespace
from unittest.mock import MagicMock

from azure.core.exceptions import ResourceNotFoundError

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_cosmosdbmongocollection_info import AzureRMCosmosDBMongoCollectionInfo
from ansible_collections.azure.azcollection.plugins.modules.azure_rm_cosmosdbsqlcontainer_info import AzureRMCosmosDBSqlContainerInfo


def module(cls, api, resources=None, not_found=False):
    obj = cls.__new__(cls)
    obj.module_arg_spec = dict.fromkeys(('resource_group', 'account_name', 'database_name', 'name', 'retrieve_throughput'))
    obj.results = dict(changed=False, **{'containers' if api == 'sql_resources' else 'collections': []})
    client = MagicMock()
    if not_found:
        get_name = 'get_sql_container' if api == 'sql_resources' else 'get_mongo_db_collection'
        getattr(client, get_name).side_effect = ResourceNotFoundError('missing')
    else:
        list_name = 'list_sql_containers' if api == 'sql_resources' else 'list_mongo_db_collections'
        getattr(client, list_name).return_value = resources or []
    obj.get_mgmt_svc_client = MagicMock(return_value=SimpleNamespace(**{api: client}))
    obj.azure_auth = SimpleNamespace(_cloud_environment=SimpleNamespace(
        endpoints=SimpleNamespace(resource_manager='https://management.azure.com')))
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


def test_sql_container_info_list_and_throughput():
    container = SimpleNamespace(as_dict=lambda: {'name': 'events', 'resource': {'id': 'events'}})
    obj, client = module(AzureRMCosmosDBSqlContainerInfo, 'sql_resources', [container])
    throughput = SimpleNamespace(as_dict=lambda: {'resource': {'throughput': 800}})
    client.get_sql_container_throughput.return_value = throughput
    result = obj.exec_module(**params(retrieve_throughput=True))
    assert result['containers'][0]['name'] == 'events'
    assert result['containers'][0]['throughput']['resource']['throughput'] == 800
    client.list_sql_containers.assert_called_once_with('rg', 'account', 'db')


def test_sql_container_info_missing_name_is_empty():
    obj = module(AzureRMCosmosDBSqlContainerInfo, 'sql_resources', not_found=True)[0]
    assert obj.exec_module(**params(name='missing'))['containers'] == []


def test_mongo_collection_info_list_and_throughput():
    collection = SimpleNamespace(as_dict=lambda: {'name': 'events', 'resource': {'id': 'events'}})
    obj, client = module(AzureRMCosmosDBMongoCollectionInfo, 'mongo_db_resources', [collection])
    throughput = SimpleNamespace(as_dict=lambda: {'resource': {'throughput': 400}})
    client.get_mongo_db_collection_throughput.return_value = throughput
    result = obj.exec_module(**params(retrieve_throughput=True))
    assert result['collections'][0]['name'] == 'events'
    assert result['collections'][0]['throughput']['resource']['throughput'] == 400
    client.list_mongo_db_collections.assert_called_once_with('rg', 'account', 'db')


def test_mongo_collection_info_missing_name_is_empty():
    obj = module(AzureRMCosmosDBMongoCollectionInfo, 'mongo_db_resources', not_found=True)[0]
    assert obj.exec_module(**params(name='missing'))['collections'] == []
