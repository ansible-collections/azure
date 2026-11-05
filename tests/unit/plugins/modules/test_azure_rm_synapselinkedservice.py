import json
from types import SimpleNamespace
from unittest.mock import MagicMock

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_synapselinkedservice import AzureRMSynapseLinkedService


def module(current=None, check_mode=False):
    obj = AzureRMSynapseLinkedService.__new__(AzureRMSynapseLinkedService)
    obj.module_arg_spec = dict.fromkeys(('resource_group', 'workspace_name', 'name', 'server', 'database',
                                         'user_name', 'password', 'integration_runtime',
                                         'force_password_update', 'state'))
    current_response = SimpleNamespace(status_code=200 if current else 404,
                                       body=lambda: json.dumps(current or {}).encode())
    obj._resource_client = MagicMock()
    obj._resource_client.query.return_value = current_response
    obj.azure_auth = SimpleNamespace(
        _cloud_environment=SimpleNamespace(endpoints=SimpleNamespace(resource_manager='https://management.azure.com')),
        subscription_id='sub')
    obj.check_mode = check_mode
    obj.module = SimpleNamespace(log=MagicMock(), debug=MagicMock())
    obj.fail = MagicMock(side_effect=lambda message: (_ for _ in ()).throw(ValueError(message)))
    return obj


def params(**overrides):
    values = dict(resource_group='rg', workspace_name='ws', name='warehouse', server='sql.example.net',
                  database='warehouse', user_name='user', password='secret', integration_runtime='AutoResolve',
                  force_password_update=False, state='present')
    values.update(overrides)
    return values


def test_create_secure_linked_service_and_redact_password():
    obj = module()
    result = obj.exec_module(**params())
    request = obj._resource_client.query.call_args_list[1]
    body = json.loads(request.args[4])
    assert result['changed']
    assert 'secret' in body['properties']['typeProperties']['connectionString']['value']
    assert 'secret' not in json.dumps(result)
    assert request.args[1] == 'PUT'


def test_linked_service_check_mode_does_not_put():
    obj = module(check_mode=True)
    result = obj.exec_module(**params())
    assert result['changed']
    assert obj._resource_client.query.call_count == 1
    assert 'secret' not in json.dumps(result)


def test_linked_service_idempotency_and_password_rotation():
    obj = module()
    obj._current = {}
    obj.server = 'sql.example.net'
    obj.database = 'warehouse'
    obj.user_name = 'user'
    obj.password = 'secret'
    obj.integration_runtime = 'AutoResolve'
    desired = obj._body(include_password=True)
    obj._resource_client.query.return_value = SimpleNamespace(status_code=200,
                                                              body=lambda: json.dumps(desired).encode())
    result = obj.exec_module(**params())
    assert not result['changed']
    obj = module(current=desired)
    result = obj.exec_module(**params(force_password_update=True))
    assert result['changed']
    assert obj._resource_client.query.call_args_list[-1].args[1] == 'PUT'


def test_absent_check_mode():
    obj = module(current={'properties': {'type': 'AzureSqlDatabase'}} , check_mode=True)
    result = obj.exec_module(**params(state='absent'))
    assert result['changed']
    assert obj._resource_client.query.call_count == 1
