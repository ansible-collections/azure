from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.cosmosdb import models

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_cosmosdbsqlcontainer import AzureRMCosmosDBSqlContainer


def module(existing=None, throughput=None, check_mode=False):
    obj = AzureRMCosmosDBSqlContainer.__new__(AzureRMCosmosDBSqlContainer)
    obj.module_arg_spec = dict.fromkeys(('resource_group', 'account_name', 'database_name', 'name',
                                         'partition_key_paths', 'indexing_mode', 'throughput',
                                         'automatic', 'autoscale_max_throughput', 'state'))
    obj.results = dict(changed=False)
    client = MagicMock()
    if existing is None:
        client.get_sql_container.side_effect = ResourceNotFoundError('missing')
    else:
        client.get_sql_container.return_value = existing
    if throughput is not None:
        client.get_sql_container_throughput.return_value.resource = throughput
    obj._cosmosdb_client = SimpleNamespace(sql_resources=client)
    obj.module = SimpleNamespace(debug=MagicMock())
    obj.check_mode = check_mode
    obj.get_poller_result = MagicMock(side_effect=lambda poller: poller.result())

    def fail(message):
        raise ValueError(message)
    obj.fail = MagicMock(side_effect=fail)
    return obj, client


def params(**overrides):
    values = dict(resource_group='rg', account_name='account', database_name='db', name='container',
                  partition_key_paths=None, indexing_mode=None, automatic=None, throughput=None,
                  autoscale_max_throughput=None, state='present')
    values.update(overrides)
    return values


def existing_container():
    return models.SqlContainerGetResults(resource=models.SqlContainerGetPropertiesResource(
        id='container', partition_key=models.ContainerPartitionKey(paths=['/tenant'], kind='Hash'),
        indexing_policy=models.IndexingPolicy(indexing_mode='consistent', automatic=True), default_ttl=3600))


def test_creation_requires_partition_key():
    obj, client = module()
    with pytest.raises(ValueError, match='partition_key_paths is required'):
        obj.exec_module(**params())
    client.begin_create_update_sql_container.assert_not_called()


def test_hierarchical_partition_key_uses_multihash():
    obj, client = module()
    client.begin_create_update_sql_container.return_value.result.return_value = existing_container()
    obj.exec_module(**params(partition_key_paths=['/tenant', '/user']))
    body = client.begin_create_update_sql_container.call_args.kwargs['create_update_sql_container_parameters']
    assert body.resource.partition_key.kind == 'MultiHash'
    assert body.resource.partition_key.paths == ['/tenant', '/user']
    assert body.resource.partition_key.version == 2


def test_reject_more_than_three_partition_key_paths():
    obj, client = module()
    with pytest.raises(ValueError, match='at most three paths'):
        obj.exec_module(**params(partition_key_paths=['/a', '/b', '/c', '/d']))
    client.begin_create_update_sql_container.assert_not_called()


def test_unchanged_partition_key_is_idempotent():
    obj, client = module(existing_container())
    result = obj.exec_module(**params(partition_key_paths=['/tenant']))
    assert not result['changed']
    client.begin_create_update_sql_container.assert_not_called()


def test_index_update_preserves_existing_properties():
    old = existing_container()
    obj, client = module(old)
    client.begin_create_update_sql_container.return_value.result.return_value = old
    result = obj.exec_module(**params(indexing_mode='none'))
    body = client.begin_create_update_sql_container.call_args.kwargs['create_update_sql_container_parameters']
    assert result['changed']
    assert body.resource.indexing_policy.indexing_mode == 'none'
    assert body.resource.indexing_policy.automatic is False
    assert body.resource.indexing_policy.included_paths is None
    assert body.resource.indexing_policy.excluded_paths is None
    assert body.resource.default_ttl == 3600
    assert old.resource.indexing_policy.indexing_mode == 'consistent'


def test_index_idempotent_and_check_mode():
    obj, client = module(existing_container(), check_mode=True)
    assert not obj.exec_module(**params(indexing_mode='consistent'))['changed']
    assert obj.exec_module(**params(indexing_mode='none'))['changed']
    client.begin_create_update_sql_container.assert_not_called()


@pytest.mark.parametrize('configured,desired', [(400, 800), (4000, 6000)])
def test_throughput_updates_without_container_put(configured, desired):
    autoscale = configured > 1000
    resource = models.ThroughputSettingsResource(
        throughput=None if autoscale else configured,
        autoscale_settings=models.AutoscaleSettingsResource(max_throughput=configured) if autoscale else None)
    obj, client = module(existing_container(), resource)
    values = {'autoscale_max_throughput' if autoscale else 'throughput': desired}
    result = obj.exec_module(**params(**values))
    assert result['changed']
    client.begin_create_update_sql_container.assert_not_called()
    client.begin_update_sql_container_throughput.assert_called_once()


def test_reject_partition_key_change_before_mutation():
    obj, client = module(existing_container())
    with pytest.raises(ValueError, match='cannot be changed'):
        obj.exec_module(**params(partition_key_paths=['/other']))
    client.begin_create_update_sql_container.assert_not_called()


def test_absent_check_mode_does_not_delete():
    obj, client = module(existing_container(), check_mode=True)
    assert obj.exec_module(**params(state='absent'))['changed']
    client.begin_delete_sql_container.assert_not_called()
