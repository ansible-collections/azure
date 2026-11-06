import json
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_databrickscluster_info import AzureRMDatabricksClusterInfo
from ansible_collections.azure.azcollection.plugins.modules.azure_rm_synapselinkedservice_info import AzureRMSynapseLinkedServiceInfo
from ansible_collections.azure.azcollection.plugins.modules.azure_rm_synapseworkspace_info import AzureRMSynapseWorkspaceInfo


def new_module(cls, keys):
    obj = cls.__new__(cls)
    obj.module_arg_spec = dict.fromkeys(keys)
    output_key = 'clusters' if cls is AzureRMDatabricksClusterInfo else (
        'workspaces' if cls is AzureRMSynapseWorkspaceInfo else 'linked_services')
    obj.results = dict(changed=False, **{output_key: []})
    obj.module = SimpleNamespace(debug=MagicMock())
    obj.check_mode = False

    def fail(message):
        raise ValueError(message)
    obj.fail = MagicMock(side_effect=fail)
    return obj


def response(status, body):
    return SimpleNamespace(status_code=status, body=lambda: json.dumps(body).encode('utf-8'))


def test_databricks_cluster_info_list_and_filter():
    obj = new_module(AzureRMDatabricksClusterInfo, ('resource_group', 'workspace_name', 'name', 'cluster_id'))
    obj._databricks_client = SimpleNamespace(workspaces=SimpleNamespace(
        get=MagicMock(return_value=SimpleNamespace(workspace_url='adb.example.net'))))
    clusters = [{'cluster_id': 'id1', 'cluster_name': 'one'}, {'cluster_id': 'id2', 'cluster_name': 'two'}]
    with patch('ansible_collections.azure.azcollection.plugins.modules.azure_rm_databrickscluster_info.databricks_request',
               return_value={'clusters': clusters}):
        result = obj.exec_module(resource_group='rg', workspace_name='ws', name='two', cluster_id=None)
    assert result['clusters'] == [clusters[1]]


def test_databricks_cluster_info_by_id():
    obj = new_module(AzureRMDatabricksClusterInfo, ('resource_group', 'workspace_name', 'name', 'cluster_id'))
    obj._databricks_client = SimpleNamespace(workspaces=SimpleNamespace(
        get=MagicMock(return_value=SimpleNamespace(workspace_url='adb.example.net'))))
    cluster = {'cluster_id': 'id1', 'cluster_name': 'one'}
    with patch('ansible_collections.azure.azcollection.plugins.modules.azure_rm_databrickscluster_info.databricks_request',
               return_value=cluster) as request:
        result = obj.exec_module(resource_group='rg', workspace_name='ws', name=None, cluster_id='id1')
    assert result['clusters'] == [cluster]
    assert 'cluster_id=id1' in request.call_args.args[2]


def test_synapse_workspace_info_get_and_list():
    obj = new_module(AzureRMSynapseWorkspaceInfo, ('resource_group', 'name'))
    obj.azure_auth = SimpleNamespace(
        _cloud_environment=SimpleNamespace(endpoints=SimpleNamespace(resource_manager='https://management.azure.com')),
        subscription_id='sub')
    obj._resource_client = MagicMock()
    obj._resource_client.query.return_value = response(200, {'name': 'ws', 'properties': {
        'sqlAdministratorLoginPassword': 'hidden', 'provisioningState': 'Succeeded'}})
    result = obj.exec_module(resource_group='rg', name='ws')
    assert result['workspaces'][0]['name'] == 'ws'
    assert 'sqlAdministratorLoginPassword' not in result['workspaces'][0]['properties']

    obj._resource_client.query.return_value = response(200, {'value': [{'name': 'ws'}]})
    assert len(obj.exec_module(resource_group='rg', name=None)['workspaces']) == 1


def test_synapse_linked_service_info_get_and_redact():
    obj = new_module(AzureRMSynapseLinkedServiceInfo, ('resource_group', 'workspace_name', 'name'))
    obj.azure_auth = SimpleNamespace(
        _cloud_environment=SimpleNamespace(endpoints=SimpleNamespace(resource_manager='https://management.azure.com')),
        subscription_id='sub')
    obj._resource_client = MagicMock()
    obj._resource_client.query.return_value = response(200, {'name': 'sql', 'properties': {
        'type': 'AzureSqlDatabase', 'typeProperties': {
            'connectionString': {'type': 'SecureString', 'value': 'secret'},
            'encryptedCredential': 'secret',
        }}})
    result = obj.exec_module(resource_group='rg', workspace_name='ws', name='sql')
    type_properties = result['linked_services'][0]['properties']['typeProperties']
    assert 'connectionString' not in type_properties
    assert 'encryptedCredential' not in type_properties

    obj._resource_client.query.return_value = response(200, {'value': [{'name': 'sql'}]})
    assert len(obj.exec_module(resource_group='rg', workspace_name='ws', name=None)['linked_services']) == 1
