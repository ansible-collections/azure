import json
from types import SimpleNamespace
from unittest.mock import MagicMock

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_synapseworkspace import AzureRMSynapseWorkspace


def module(current=None, check_mode=False):
    obj = AzureRMSynapseWorkspace.__new__(AzureRMSynapseWorkspace)
    obj.module_arg_spec = dict.fromkeys(('resource_group', 'name', 'location', 'storage_account_url', 'filesystem',
                                         'sql_admin_login', 'sql_admin_password', 'managed_resource_group_name',
                                         'public_network_access', 'tags', 'force_password_update', 'state'))
    obj._resource_client = MagicMock()
    response = SimpleNamespace(status_code=200 if current else 404, body=lambda: json.dumps(current or {}).encode())
    obj._resource_client.query.return_value = response
    obj.azure_auth = SimpleNamespace(
        _cloud_environment=SimpleNamespace(endpoints=SimpleNamespace(resource_manager='https://management.azure.com')),
        subscription_id='sub')
    obj.module = SimpleNamespace(debug=MagicMock(), params={'tags': {'env': 'test'}, 'append_tags': True})
    obj.check_mode = check_mode

    def fail(message):
        raise ValueError(message)
    obj.fail = MagicMock(side_effect=fail)
    return obj


def params(**overrides):
    values = dict(resource_group='rg', name='workspace', location='eastus',
                  storage_account_url='https://lake.dfs.core.windows.net', filesystem='synapse',
                  sql_admin_login='admin', sql_admin_password='password',
                  managed_resource_group_name='synapse-managed', public_network_access='Enabled',
                  tags={'env': 'test'}, force_password_update=False, state='present')
    values.update(overrides)
    return values


def test_create_workspace_redacts_sql_password():
    obj = module()
    result = obj.exec_module(**params())
    body = json.loads(obj._resource_client.query.call_args_list[1].args[4])
    assert result['changed']
    assert body['properties']['sqlAdministratorLoginPassword'] == 'password'
    assert 'sqlAdministratorLoginPassword' not in result['workspace']['properties']
    assert 'password' not in json.dumps(result)


def test_workspace_check_mode():
    obj = module(check_mode=True)
    result = obj.exec_module(**params())
    assert result['changed']
    assert obj._resource_client.query.call_count == 1
    assert 'sqlAdministratorLoginPassword' not in result['workspace']['properties']


def test_existing_workspace_idempotency_and_password_rotation():
    obj = module()
    obj.exec_module(**params())
    desired = json.loads(obj._resource_client.query.call_args_list[1].args[4])
    desired['properties'].pop('sqlAdministratorLoginPassword')
    obj = module(current=desired)
    assert not obj.exec_module(**params())['changed']
    obj = module(current=desired)
    assert obj.exec_module(**params(force_password_update=True))['changed']
    assert obj._resource_client.query.call_args_list[-1].args[1] == 'PUT'


def test_delete_check_mode():
    obj = module(current={'name': 'workspace'}, check_mode=True)
    assert obj.exec_module(**params(state='absent'))['changed']
    assert obj._resource_client.query.call_count == 1
