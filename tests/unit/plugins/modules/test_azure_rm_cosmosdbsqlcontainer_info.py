from types import SimpleNamespace
from unittest.mock import MagicMock

from azure.core.exceptions import ResourceNotFoundError

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_cosmosdbsqlcontainer_info import AzureRMCosmosDBSqlContainerInfo


def module(resources=None, not_found=False):
    obj = AzureRMCosmosDBSqlContainerInfo.__new__(AzureRMCosmosDBSqlContainerInfo)
    obj.module_arg_spec = dict.fromkeys(('resource_group', 'account_name', 'database_name', 'name', 'retrieve_throughput'))
    obj.results = dict(changed=False, containers=[])
    client = MagicMock()
    if not_found:
        client.get_sql_container.side_effect = ResourceNotFoundError('missing')
    else:
        client.list_sql_containers.return_value = resources or []
    obj._cosmosdb_client = SimpleNamespace(sql_resources=client)
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
    obj, client = module([container])
    throughput = SimpleNamespace(as_dict=lambda: {'resource': {'throughput': 800}})
    client.get_sql_container_throughput.return_value = throughput
    result = obj.exec_module(**params(retrieve_throughput=True))
    assert result['containers'][0]['name'] == 'events'
    assert result['containers'][0]['throughput']['resource']['throughput'] == 800
    client.list_sql_containers.assert_called_once_with('rg', 'account', 'db')


def test_sql_container_info_missing_name_is_empty():
    obj = module(not_found=True)[0]
    assert obj.exec_module(**params(name='missing'))['containers'] == []
