from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_databrickscluster_info import AzureRMDatabricksClusterInfo


def new_module():
    obj = AzureRMDatabricksClusterInfo.__new__(AzureRMDatabricksClusterInfo)
    obj.module_arg_spec = dict.fromkeys(('resource_group', 'workspace_name', 'name', 'cluster_id'))
    obj.results = dict(changed=False, clusters=[])
    obj._databricks_client = SimpleNamespace(workspaces=SimpleNamespace(
        get=MagicMock(return_value=SimpleNamespace(workspace_url='adb.example.net'))))
    obj.module = SimpleNamespace(debug=MagicMock())
    obj.check_mode = False

    def fail(message):
        raise ValueError(message)
    obj.fail = MagicMock(side_effect=fail)
    return obj


def test_databricks_cluster_info_list_and_filter():
    obj = new_module()
    clusters = [{'cluster_id': 'id1', 'cluster_name': 'one'}, {'cluster_id': 'id2', 'cluster_name': 'two'}]
    with patch('ansible_collections.azure.azcollection.plugins.modules.azure_rm_databrickscluster_info.databricks_request',
               return_value={'clusters': clusters}):
        result = obj.exec_module(resource_group='rg', workspace_name='ws', name='two', cluster_id=None)
    assert result['clusters'] == [clusters[1]]


def test_databricks_cluster_info_by_id():
    obj = new_module()
    cluster = {'cluster_id': 'id1', 'cluster_name': 'one'}
    with patch('ansible_collections.azure.azcollection.plugins.modules.azure_rm_databrickscluster_info.databricks_request',
               return_value=cluster) as request:
        result = obj.exec_module(resource_group='rg', workspace_name='ws', name=None, cluster_id='id1')
    assert result['clusters'] == [cluster]
    assert 'cluster_id=id1' in request.call_args.args[2]
