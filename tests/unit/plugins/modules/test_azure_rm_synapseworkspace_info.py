from types import SimpleNamespace
from unittest.mock import MagicMock

from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.synapse import models

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_synapseworkspace_info import AzureRMSynapseWorkspaceInfo


def module(name=None, not_found=False):
    obj = AzureRMSynapseWorkspaceInfo.__new__(AzureRMSynapseWorkspaceInfo)
    obj.module_arg_spec = dict.fromkeys(('resource_group', 'name'))
    obj.results = dict(changed=False, workspaces=[])
    client = MagicMock()
    if not_found:
        client.workspaces.get.side_effect = ResourceNotFoundError('missing')
    else:
        client.workspaces.get.return_value = models.Workspace(
            location='eastus', sql_administrator_login='admin')
        client.workspaces.list_by_resource_group.return_value = [models.Workspace(location='eastus')]
    obj._synapse_client = client
    obj.resource_group = 'rg'
    obj.name = name
    obj.module = SimpleNamespace(debug=MagicMock())

    def fail(message):
        raise ValueError(message)
    obj.fail = MagicMock(side_effect=fail)
    return obj, client


def test_synapse_workspace_info_get():
    obj, client = module(name='ws')
    result = obj.exec_module(resource_group='rg', name='ws')
    client.workspaces.get.assert_called_once_with('rg', 'ws')
    assert result['workspaces'][0]['location'] == 'eastus'
    assert 'sql_administrator_login_password' not in result['workspaces'][0]
    assert result['workspaces'][0]['resource_group'] == 'rg'


def test_synapse_workspace_info_list():
    obj, client = module()
    result = obj.exec_module(resource_group='rg', name=None)
    client.workspaces.list_by_resource_group.assert_called_once_with('rg')
    assert len(result['workspaces']) == 1


def test_synapse_workspace_info_missing_name_is_empty():
    obj, client = module(name='missing', not_found=True)
    assert obj.exec_module(resource_group='rg', name='missing')['workspaces'] == []
