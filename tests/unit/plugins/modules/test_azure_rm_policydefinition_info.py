from types import SimpleNamespace
from unittest.mock import MagicMock

from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.resource.policy import models

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_policydefinition_info import AzureRMPolicyDefinitionInfo


def module(not_found=False):
    obj = AzureRMPolicyDefinitionInfo.__new__(AzureRMPolicyDefinitionInfo)
    obj.module_arg_spec = dict.fromkeys(('name', 'management_group'))
    obj.results = dict(changed=False, policy_definitions=[])
    client = MagicMock()
    # The model constructor ignores readonly attributes such as id and
    # policy_type, so they are assigned after construction like the SDK
    # deserializer does.

    def definition():
        definition = models.PolicyDefinition(
            policy_rule={'then': {'effect': 'audit'}}, display_name='audit-vm-tags', mode='Indexed')
        definition.id = '/subscriptions/sub/providers/Microsoft.Authorization/policyDefinitions/audit-vm-tags'
        definition.name = 'audit-vm-tags'
        definition.policy_type = 'Custom'
        return definition

    if not_found:
        client.policy_definitions.get.side_effect = ResourceNotFoundError('missing')
        client.policy_definitions.get_at_management_group.side_effect = ResourceNotFoundError('missing')
    else:
        client.policy_definitions.get.return_value = definition()
        client.policy_definitions.get_at_management_group.return_value = definition()
        client.policy_definitions.list.return_value = [definition()]
        client.policy_definitions.list_by_management_group.return_value = [definition()]
    obj._policy_client = client
    obj.name = None
    obj.management_group = None
    obj.module = SimpleNamespace(debug=MagicMock())

    def fail(message):
        raise ValueError(message)
    obj.fail = MagicMock(side_effect=fail)
    return obj, client


def test_policy_definition_info_get():
    obj, client = module()
    result = obj.exec_module(name='audit-vm-tags', management_group=None)
    client.policy_definitions.get.assert_called_once_with('audit-vm-tags')
    assert len(result['policy_definitions']) == 1
    assert result['policy_definitions'][0]['name'] == 'audit-vm-tags'
    assert result['policy_definitions'][0]['policy_type'] == 'Custom'


def test_policy_definition_info_missing_name_is_empty():
    obj, client = module(not_found=True)
    result = obj.exec_module(name='missing', management_group=None)
    client.policy_definitions.get.assert_called_once_with('missing')
    assert result['policy_definitions'] == []


def test_policy_definition_info_list():
    obj, client = module()
    result = obj.exec_module(name=None, management_group=None)
    client.policy_definitions.list.assert_called_once_with()
    assert len(result['policy_definitions']) == 1


def test_policy_definition_info_get_at_management_group():
    obj, client = module()
    result = obj.exec_module(name='audit-vm-tags', management_group='landing-zones')
    client.policy_definitions.get_at_management_group.assert_called_once_with(management_group_id='landing-zones', policy_definition_name='audit-vm-tags')
    client.policy_definitions.get.assert_not_called()
    assert len(result['policy_definitions']) == 1


def test_policy_definition_info_list_by_management_group():
    obj, client = module()
    result = obj.exec_module(name=None, management_group='landing-zones')
    client.policy_definitions.list_by_management_group.assert_called_once_with(management_group_id='landing-zones')
    client.policy_definitions.list.assert_not_called()
    assert len(result['policy_definitions']) == 1
