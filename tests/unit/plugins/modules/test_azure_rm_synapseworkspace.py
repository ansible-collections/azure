from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.synapse import models

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_synapseworkspace import AzureRMSynapseWorkspace


def module(existing=None, check_mode=False, tags=None):
    obj = AzureRMSynapseWorkspace.__new__(AzureRMSynapseWorkspace)
    obj.module_arg_spec = dict.fromkeys(('resource_group', 'name', 'location', 'storage_account_url', 'filesystem',
                                         'sql_admin_login', 'sql_admin_password', 'managed_resource_group_name',
                                         'public_network_access', 'tags', 'force_password_update', 'state'))
    obj.results = dict(changed=False)
    client = MagicMock()
    if existing is None:
        client.workspaces.get.side_effect = ResourceNotFoundError('missing')
    else:
        client.workspaces.get.return_value = existing
    obj._synapse_client = client
    obj.module = SimpleNamespace(debug=MagicMock(), params={'tags': tags, 'append_tags': True})
    obj.check_mode = check_mode

    def fail(message):
        raise ValueError(message)
    obj.fail = MagicMock(side_effect=fail)
    return obj, client


def params(**overrides):
    values = dict(resource_group='rg', name='workspace', location='eastus',
                  storage_account_url='https://lake.dfs.core.windows.net', filesystem='synapse',
                  sql_admin_login='admin', sql_admin_password='password',
                  managed_resource_group_name='synapse-managed', public_network_access='Enabled',
                  tags={'env': 'test'}, force_password_update=False, state='present')
    values.update(overrides)
    return values


def existing_workspace():
    return models.Workspace(
        location='eastus', tags={'env': 'test'},
        default_data_lake_storage=models.DataLakeStorageAccountDetails(
            account_url='https://lake.dfs.core.windows.net', filesystem='synapse'),
        sql_administrator_login='admin', managed_resource_group_name='synapse-managed',
        public_network_access='Enabled')


def test_create_workspace_waits_for_lro_and_redacts_sql_password():
    obj, client = module(tags={'env': 'test'})
    created = existing_workspace()
    created.provisioning_state = 'Succeeded'
    created.sql_administrator_login_password = 'password'
    client.workspaces.begin_create_or_update.return_value.result.return_value = created
    result = obj.exec_module(**params())
    body = client.workspaces.begin_create_or_update.call_args.args[2]
    assert result['changed']
    assert result['workspace']['provisioning_state'] == 'Succeeded'
    assert body.sql_administrator_login_password == 'password'
    assert 'sql_administrator_login_password' not in result['workspace']
    assert 'password' not in str(result)


def test_workspace_check_mode():
    obj, client = module(check_mode=True)
    result = obj.exec_module(**params())
    assert result['changed']
    client.workspaces.begin_create_or_update.assert_not_called()
    assert 'sql_administrator_login_password' not in result['workspace']


def test_existing_workspace_idempotency_and_password_rotation():
    obj, client = module(existing_workspace(), tags={'env': 'test'})
    assert not obj.exec_module(**params())['changed']
    client.workspaces.begin_create_or_update.assert_not_called()

    obj, client = module(existing_workspace(), tags={'env': 'test'})
    assert obj.exec_module(**params(force_password_update=True))['changed']
    body = client.workspaces.begin_create_or_update.call_args.args[2]
    assert body.sql_administrator_login_password == 'password'


def test_existing_workspace_update_carries_forward_settings():
    obj, client = module(existing_workspace(), tags={'env': 'prod'})
    result = obj.exec_module(**params(tags={'env': 'prod'}))
    assert result['changed']
    body = client.workspaces.begin_create_or_update.call_args.args[2]
    assert body.tags == {'env': 'prod'}
    assert body.default_data_lake_storage.account_url == 'https://lake.dfs.core.windows.net'
    assert body.sql_administrator_login == 'admin'
    assert body.sql_administrator_login_password is None


def test_create_requires_full_specification():
    obj, client = module()
    with pytest.raises(ValueError, match='are required when creating'):
        obj.exec_module(**params(location=None))
    client.workspaces.begin_create_or_update.assert_not_called()


def test_reject_location_change():
    obj, client = module(existing_workspace(), tags={'env': 'test'})
    with pytest.raises(ValueError, match='immutable'):
        obj.exec_module(**params(location='westus'))
    client.workspaces.begin_create_or_update.assert_not_called()


def test_delete_uses_lro_poller():
    obj, client = module(existing_workspace())
    assert obj.exec_module(**params(state='absent'))['changed']
    client.workspaces.begin_delete.assert_called_once_with('rg', 'workspace')


def test_delete_check_mode():
    obj, client = module(existing_workspace(), check_mode=True)
    assert obj.exec_module(**params(state='absent'))['changed']
    client.workspaces.begin_delete.assert_not_called()
