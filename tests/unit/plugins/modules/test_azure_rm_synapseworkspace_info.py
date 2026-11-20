from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.synapse import models

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_synapseworkspace_info import AzureRMSynapseWorkspaceInfo


def module(name=None, not_found=False, resource_group_in_id='resourceGroups'):
    obj = AzureRMSynapseWorkspaceInfo.__new__(AzureRMSynapseWorkspaceInfo)
    obj.module_arg_spec = dict.fromkeys(('resource_group', 'name'))
    obj.results = dict(changed=False, workspaces=[])
    client = MagicMock()
    resource_id = '/subscriptions/sub/{0}/rg/providers/Microsoft.Synapse/workspaces/ws'.format(resource_group_in_id)
    # The model constructor ignores readonly attributes such as id, so they
    # are assigned after construction like the SDK deserializer does.

    def workspace_with_id():
        workspace = models.Workspace(location='eastus')
        workspace.id = resource_id
        return workspace

    if not_found:
        client.workspaces.get.side_effect = ResourceNotFoundError('missing')
    else:
        client.workspaces.get.return_value = workspace_with_id()
        client.workspaces.list_by_resource_group.return_value = [models.Workspace(location='eastus')]
        client.workspaces.list.return_value = [workspace_with_id()]
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


def test_synapse_workspace_info_list_subscription():
    obj, client = module()
    result = obj.exec_module(resource_group=None, name=None)
    client.workspaces.list.assert_called_once_with()
    assert len(result['workspaces']) == 1
    assert result['workspaces'][0]['resource_group'] == 'rg'


def test_synapse_workspace_info_parses_resource_group_case_insensitively():
    obj, client = module(resource_group_in_id='resourcegroups')
    result = obj.exec_module(resource_group=None, name=None)
    assert result['workspaces'][0]['resource_group'] == 'rg'


def test_synapse_workspace_info_name_requires_resource_group():
    obj, client = module(name='ws')
    with pytest.raises(ValueError, match='resource_group is required'):
        obj.exec_module(resource_group=None, name='ws')
