from types import SimpleNamespace
from unittest.mock import MagicMock

from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.resource.policy import models

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_policyassignment import AzureRMPolicyAssignment


def module(existing=None, check_mode=False):
    obj = AzureRMPolicyAssignment.__new__(AzureRMPolicyAssignment)
    obj.module_arg_spec = dict.fromkeys(('name', 'policy_definition_id', 'display_name', 'description',
                                         'enforcement_mode', 'parameters', 'resource_group', 'scope', 'state'))
    obj.results = dict(changed=False)
    obj.azure_auth = SimpleNamespace(subscription_id='sub')
    client = MagicMock()
    if existing is None:
        client.policy_assignments.get.side_effect = ResourceNotFoundError('missing')
    else:
        client.policy_assignments.get.return_value = existing
    obj._policy_client = client
    obj.module = SimpleNamespace(debug=MagicMock())
    obj.check_mode = check_mode

    def fail(message):
        raise ValueError(message)
    obj.fail = MagicMock(side_effect=fail)
    return obj, client


def params(**overrides):
    values = dict(name='audit-vm-tags',
                  policy_definition_id='/subscriptions/sub/providers/Microsoft.Authorization/policyDefinitions/audit-vm-tags',
                  display_name='Audit VM tags', description='Audits VM tags',
                  enforcement_mode='Default', parameters=None,
                  resource_group=None, scope=None, state='present')
    values.update(overrides)
    return values


def existing_assignment():
    # The model constructor ignores readonly attributes such as id and scope,
    # so they are assigned after construction like the SDK deserializer does.
    assignment = models.PolicyAssignment(
        policy_definition_id=params()['policy_definition_id'],
        display_name='Audit VM tags', description='Audits VM tags',
        enforcement_mode='Default',
        parameters={'tagName': models.ParameterValuesValue(value='costCenter')})
    assignment.id = '/subscriptions/sub/providers/Microsoft.Authorization/policyAssignments/audit-vm-tags'
    assignment.name = 'audit-vm-tags'
    assignment.scope = '/subscriptions/sub'
    return assignment


def test_create_policy_assignment():
    obj, client = module()
    client.policy_assignments.create.return_value = existing_assignment()
    result = obj.exec_module(**params())
    assert result['changed']
    body = client.policy_assignments.create.call_args.kwargs['parameters']
    client.policy_assignments.create.assert_called_once_with(
        scope='/subscriptions/sub', policy_assignment_name='audit-vm-tags', parameters=body)
    assert body.policy_definition_id == params()['policy_definition_id']
    assert result['policy_assignment']['scope'] == '/subscriptions/sub'


def test_create_defaults_display_name_to_the_name():
    obj, client = module()
    client.policy_assignments.create.return_value = existing_assignment()
    obj.exec_module(**params(display_name=None))
    assert client.policy_assignments.create.call_args.kwargs['parameters'].display_name == 'audit-vm-tags'


def test_create_passes_parameter_values_as_models():
    obj, client = module()
    client.policy_assignments.create.return_value = existing_assignment()
    obj.exec_module(**params(parameters={'tagName': {'value': 'costCenter'}}))
    body = client.policy_assignments.create.call_args.kwargs['parameters']
    assert isinstance(body.parameters['tagName'], models.ParameterValuesValue)
    assert body.parameters['tagName'].value == 'costCenter'


def test_create_check_mode():
    obj, client = module(check_mode=True)
    result = obj.exec_module(**params())
    assert result['changed']
    client.policy_assignments.create.assert_not_called()


def test_existing_assignment_idempotency():
    obj, client = module(existing_assignment())
    assert not obj.exec_module(**params(parameters={'tagName': {'value': 'costCenter'}}))['changed']
    client.policy_assignments.create.assert_not_called()


def test_service_parameter_objects_compare_idempotent():
    obj, client = module(existing_assignment())
    assert not obj.exec_module(**params(parameters={'tagName': {'value': 'costCenter'}}))['changed']
    client.policy_assignments.create.assert_not_called()


def test_assignment_parameter_value_change():
    obj, client = module(existing_assignment())
    result = obj.exec_module(**params(parameters={'tagName': {'value': 'environment'}}))
    assert result['changed']


def test_assignment_enforcement_mode_change():
    obj, client = module(existing_assignment())
    result = obj.exec_module(**params(parameters={'tagName': {'value': 'costCenter'}},
                                      enforcement_mode='DoNotEnforce'))
    assert result['changed']
    body = client.policy_assignments.create.call_args.kwargs['parameters']
    assert body.enforcement_mode == 'DoNotEnforce'


def test_resource_group_scope():
    obj, client = module()
    client.policy_assignments.create.return_value = existing_assignment()
    obj.exec_module(**params(resource_group='analytics'))
    assert client.policy_assignments.create.call_args.kwargs['scope'] == '/subscriptions/sub/resourceGroups/analytics'


def test_explicit_scope():
    obj, client = module()
    client.policy_assignments.create.return_value = existing_assignment()
    scope = '/providers/Microsoft.Management/managementGroups/landing-zones'
    obj.exec_module(**params(scope=scope))
    assert client.policy_assignments.create.call_args.kwargs['scope'] == scope


def test_delete_policy_assignment():
    obj, client = module(existing_assignment())
    assert obj.exec_module(**params(state='absent'))['changed']
    client.policy_assignments.delete.assert_called_once_with(
        scope='/subscriptions/sub', policy_assignment_name='audit-vm-tags')


def test_delete_at_resource_group_scope():
    obj, client = module(existing_assignment())
    assert obj.exec_module(**params(state='absent', resource_group='analytics'))['changed']
    client.policy_assignments.delete.assert_called_once_with(
        scope='/subscriptions/sub/resourceGroups/analytics', policy_assignment_name='audit-vm-tags')


def test_delete_check_mode():
    obj, client = module(existing_assignment(), check_mode=True)
    assert obj.exec_module(**params(state='absent'))['changed']
    client.policy_assignments.delete.assert_not_called()


def test_delete_idempotency():
    obj, client = module()
    assert not obj.exec_module(**params(state='absent'))['changed']
    client.policy_assignments.delete.assert_not_called()
