from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.resource.policy import models

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_policyassignment_info import AzureRMPolicyAssignmentInfo


def module(not_found=False):
    obj = AzureRMPolicyAssignmentInfo.__new__(AzureRMPolicyAssignmentInfo)
    obj.module_arg_spec = dict.fromkeys(('name', 'resource_group', 'scope'))
    obj.results = dict(changed=False, policy_assignments=[])
    obj.azure_auth = SimpleNamespace(subscription_id='sub')
    client = MagicMock()
    # The model constructor ignores readonly attributes such as id and scope,
    # so they are assigned after construction like the SDK deserializer does.

    def assignment():
        assignment = models.PolicyAssignment(
            policy_definition_id='/subscriptions/sub/providers/Microsoft.Authorization/policyDefinitions/audit-vm-tags',
            display_name='Audit VM tags', enforcement_mode='Default')
        assignment.id = '/subscriptions/sub/providers/Microsoft.Authorization/policyAssignments/audit-vm-tags'
        assignment.name = 'audit-vm-tags'
        assignment.scope = '/subscriptions/sub'
        return assignment

    if not_found:
        client.policy_assignments.get.side_effect = ResourceNotFoundError('missing')
    else:
        client.policy_assignments.get.return_value = assignment()
        client.policy_assignments.list.return_value = [assignment()]
        client.policy_assignments.list_for_resource_group.return_value = [assignment()]
    obj._policy_client = client
    obj.name = None
    obj.resource_group = None
    obj.scope = None
    obj.module = SimpleNamespace(debug=MagicMock())

    def fail(message):
        raise ValueError(message)
    obj.fail = MagicMock(side_effect=fail)
    return obj, client


def test_policy_assignment_info_get():
    obj, client = module()
    result = obj.exec_module(name='audit-vm-tags', resource_group=None, scope=None)
    client.policy_assignments.get.assert_called_once_with(
        scope='/subscriptions/sub', policy_assignment_name='audit-vm-tags')
    assert len(result['policy_assignments']) == 1
    assert result['policy_assignments'][0]['name'] == 'audit-vm-tags'
    assert result['policy_assignments'][0]['scope'] == '/subscriptions/sub'


def test_policy_assignment_info_missing_name_is_empty():
    obj, client = module(not_found=True)
    result = obj.exec_module(name='missing', resource_group=None, scope=None)
    assert result['policy_assignments'] == []


def test_policy_assignment_info_list():
    obj, client = module()
    result = obj.exec_module(name=None, resource_group=None, scope=None)
    client.policy_assignments.list.assert_called_once_with()
    assert len(result['policy_assignments']) == 1


def test_policy_assignment_info_get_at_resource_group_scope():
    obj, client = module()
    result = obj.exec_module(name='audit-vm-tags', resource_group='analytics', scope=None)
    client.policy_assignments.get.assert_called_once_with(
        scope='/subscriptions/sub/resourceGroups/analytics', policy_assignment_name='audit-vm-tags')
    assert len(result['policy_assignments']) == 1


def test_policy_assignment_info_list_for_resource_group():
    obj, client = module()
    result = obj.exec_module(name=None, resource_group='analytics', scope=None)
    client.policy_assignments.list_for_resource_group.assert_called_once_with(resource_group_name='analytics')
    client.policy_assignments.list.assert_not_called()
    assert len(result['policy_assignments']) == 1


def test_policy_assignment_info_get_at_explicit_scope():
    obj, client = module()
    scope = '/providers/Microsoft.Management/managementGroups/landing-zones'
    result = obj.exec_module(name='audit-vm-tags', resource_group=None, scope=scope)
    client.policy_assignments.get.assert_called_once_with(
        scope=scope, policy_assignment_name='audit-vm-tags')
    assert len(result['policy_assignments']) == 1


def test_policy_assignment_info_scope_requires_name():
    obj, client = module()
    with pytest.raises(ValueError, match='name is required when scope is set'):
        obj.exec_module(name=None, resource_group=None, scope='/providers/Microsoft.Management/managementGroups/lz')
