import base64
import json
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_databrickscluster import AzureRMDatabricksCluster
from ansible_collections.azure.azcollection.plugins.modules.azure_rm_databricksnotebook import AzureRMDatabricksNotebook
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_databricks import databricks_request


def make_module(cls, workspace_url='adb.example.net', check_mode=False):
    module = cls.__new__(cls)
    keys = (('resource_group', 'workspace_name', 'name', 'spark_version', 'node_type_id', 'num_workers',
             'autoscale', 'autotermination_minutes', 'state') if cls is AzureRMDatabricksCluster else
            ('resource_group', 'workspace_name', 'path', 'state', 'source', 'dest', 'format', 'language', 'overwrite'))
    module.module_arg_spec = dict.fromkeys(keys)
    module.azure_auth = SimpleNamespace(azure_credential_track2=SimpleNamespace(
        get_token=MagicMock(return_value=SimpleNamespace(token='secret-token'))))
    module._databricks_client = SimpleNamespace(workspaces=SimpleNamespace(
        get=MagicMock(return_value=SimpleNamespace(workspace_url=workspace_url))))
    module.check_mode = check_mode
    module.validate_certs = True
    module.module = SimpleNamespace(params={'polling_timeout': 60}, log=MagicMock(), debug=MagicMock())
    module.fail = MagicMock(side_effect=lambda message: (_ for _ in ()).throw(ValueError(message)))
    return module


def cluster_params(**kwargs):
    result = dict(resource_group='rg', workspace_name='ws', name='etl', spark_version='13.3.x-scala2.12',
                  node_type_id='Standard_DS3_v2', num_workers=2, autoscale=None,
                  autotermination_minutes=60, state='present')
    result.update(kwargs)
    return result


def mock_request(responses):
    return patch('ansible_collections.azure.azcollection.plugins.modules.azure_rm_databrickscluster.databricks_request',
                 side_effect=responses)


def test_cluster_create_and_check_mode():
    planned = make_module(AzureRMDatabricksCluster, check_mode=True)
    with mock_request([{'clusters': []}]):
        result = planned.exec_module(**cluster_params())
    assert result['changed']
    planned.databricks_client.workspaces.get.assert_called_once()

    created = make_module(AzureRMDatabricksCluster)
    with mock_request([{'clusters': []}, {'cluster_id': 'id'}]) as request:
        result = created.exec_module(**cluster_params())
    assert result['changed']
    assert request.call_args_list[1].args[3] == 'POST'
    assert request.call_args_list[1].args[4]['spark_version'] == '13.3.x-scala2.12'


def test_cluster_idempotency_and_edit():
    existing = dict(cluster_id='id', cluster_name='etl', spark_version='13.3.x-scala2.12',
                    node_type_id='Standard_DS3_v2', num_workers=2, autotermination_minutes=60)
    module = make_module(AzureRMDatabricksCluster)
    with mock_request([{'clusters': [existing]}]):
        assert not module.exec_module(**cluster_params())['changed']
    module = make_module(AzureRMDatabricksCluster)
    with mock_request([{'clusters': [existing]}, {}]) as request:
        assert module.exec_module(**cluster_params(num_workers=4))['changed']
    assert request.call_args_list[1].args[2].endswith('/edit')


def test_cluster_delete_and_absent_check_mode():
    existing = {'cluster_id': 'id', 'cluster_name': 'etl'}
    module = make_module(AzureRMDatabricksCluster, check_mode=True)
    with mock_request([{'clusters': [existing]}]) as request:
        assert module.exec_module(**cluster_params(state='absent'))['changed']
    assert request.call_count == 1
    module = make_module(AzureRMDatabricksCluster)
    with mock_request([{'clusters': [existing]}, {}]) as request:
        assert module.exec_module(**cluster_params(state='absent'))['changed']
    assert request.call_args.args[2].endswith('/delete')


def test_databricks_request_uses_aad_token_and_decodes_json():
    module = make_module(AzureRMDatabricksCluster)
    response = SimpleNamespace(code=200, read=lambda: b'{"ok": true}')
    with patch('ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_databricks.open_url',
               return_value=response) as open_request:
        assert databricks_request(module, 'https://adb.example.net/', '/api/2.0/test') == {'ok': True}
    assert open_request.call_args.kwargs['headers']['Authorization'] == 'Bearer secret-token'
    module.azure_auth.azure_credential_track2.get_token.assert_called_once_with(
        '2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default')


def notebook_params(**kwargs):
    result = dict(resource_group='rg', workspace_name='ws', path='/Shared/etl', state='present', source='file.py',
                  dest=None, format='SOURCE', language='PYTHON', overwrite=True)
    result.update(kwargs)
    return result


def test_notebook_import_idempotency_and_export(tmp_path):
    source = tmp_path / 'input.py'
    source.write_text('print(1)')
    module = make_module(AzureRMDatabricksNotebook)
    with patch('ansible_collections.azure.azcollection.plugins.modules.azure_rm_databricksnotebook.databricks_request',
               side_effect=[None, {'path': '/Shared/etl'}]) as request:
        result = module.exec_module(**notebook_params(source=str(source)))
    assert result['changed']
    assert request.call_args.args[4]['content'] == base64.b64encode(b'print(1)').decode('ascii')

    destination = tmp_path / 'output.py'
    exported = make_module(AzureRMDatabricksNotebook)
    with patch('ansible_collections.azure.azcollection.plugins.modules.azure_rm_databricksnotebook.databricks_request',
               return_value={'content': base64.b64encode(b'print(1)').decode('ascii')}):
        result = exported.exec_module(**notebook_params(state='exported', source=None, dest=str(destination)))
    assert result['changed']
    assert destination.read_bytes() == b'print(1)'

    repeated = make_module(AzureRMDatabricksNotebook)
    with patch('ansible_collections.azure.azcollection.plugins.modules.azure_rm_databricksnotebook.databricks_request',
               side_effect=[{'path': '/Shared/etl'}, {'content': base64.b64encode(b'print(1)').decode('ascii')}]) as request:
        result = repeated.exec_module(**notebook_params(source=str(source)))
    assert not result['changed']
    assert request.call_count == 2


def test_notebook_absent_check_mode():
    module = make_module(AzureRMDatabricksNotebook, check_mode=True)
    with patch('ansible_collections.azure.azcollection.plugins.modules.azure_rm_databricksnotebook.databricks_request',
               return_value={'path': '/Shared/etl'}) as request:
        result = module.exec_module(**notebook_params(state='absent', source=None))
    assert result['changed']
    assert request.call_count == 1
