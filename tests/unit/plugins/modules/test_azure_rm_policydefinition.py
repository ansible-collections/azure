from types import SimpleNamespace
from unittest.mock import MagicMock

from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.resource.policy import models

from ansible_collections.azure.azcollection.plugins.modules.azure_rm_policydefinition import AzureRMPolicyDefinition


def module(existing=None, check_mode=False):
    obj = AzureRMPolicyDefinition.__new__(AzureRMPolicyDefinition)
    obj.module_arg_spec = dict.fromkeys(('name', 'policy_rule', 'display_name', 'description', 'mode',
                                         'metadata', 'parameters', 'management_group', 'state'))
    obj.results = dict(changed=False)
    client = MagicMock()
    if existing is None:
        client.policy_definitions.get.side_effect = ResourceNotFoundError('missing')
        client.policy_definitions.get_at_management_group.side_effect = ResourceNotFoundError('missing')
    else:
        client.policy_definitions.get.return_value = existing
        client.policy_definitions.get_at_management_group.return_value = existing
    obj._policy_client = client
    obj.module = SimpleNamespace(debug=MagicMock())
    obj.check_mode = check_mode

    def fail(message):
        raise ValueError(message)
    obj.fail = MagicMock(side_effect=fail)
    return obj, client


def params(**overrides):
    values = dict(name='audit-vm-tags',
                  policy_rule={'if': {'field': 'type', 'equals': 'Microsoft.Compute/virtualMachines'},
                               'then': {'effect': 'audit'}},
                  display_name='Audit VM tags', description='Audits VM tags',
                  mode='Indexed', metadata=None, parameters=None,
                  management_group=None, state='present')
    values.update(overrides)
    return values


def existing_definition():
    # The model constructor ignores readonly attributes such as id and
    # policy_type, so they are assigned after construction like the SDK
    # deserializer does.
    definition = models.PolicyDefinition(
        policy_rule={'if': {'field': 'type', 'equals': 'Microsoft.Compute/virtualMachines'},
                     'then': {'effect': 'audit'}},
        display_name='Audit VM tags', description='Audits VM tags', mode='Indexed')
    definition.id = '/subscriptions/sub/providers/Microsoft.Authorization/policyDefinitions/audit-vm-tags'
    definition.name = 'audit-vm-tags'
    definition.policy_type = 'Custom'
    return definition


def test_create_policy_definition():
    obj, client = module()
    created = existing_definition()
    client.policy_definitions.create_or_update.return_value = created
    result = obj.exec_module(**params())
    body = client.policy_definitions.create_or_update.call_args.args[1]
    assert result['changed']
    assert result['policy_definition']['policy_type'] == 'Custom'
    assert body.policy_rule == params()['policy_rule']
    client.policy_definitions.create_or_update.assert_called_once_with('audit-vm-tags', body)


def test_create_defaults_display_name_to_the_name():
    obj, client = module()
    client.policy_definitions.create_or_update.return_value = existing_definition()
    obj.exec_module(**params(display_name=None))
    body = client.policy_definitions.create_or_update.call_args.args[1]
    assert body.display_name == 'audit-vm-tags'


def test_create_check_mode():
    obj, client = module(check_mode=True)
    result = obj.exec_module(**params())
    assert result['changed']
    client.policy_definitions.create_or_update.assert_not_called()


def test_existing_definition_idempotency():
    obj, client = module(existing_definition())
    assert not obj.exec_module(**params())['changed']
    client.policy_definitions.create_or_update.assert_not_called()


def test_definition_rule_change():
    obj, client = module(existing_definition())
    result = obj.exec_module(**params(policy_rule={'if': {'field': 'type'},
                                                   'then': {'effect': 'deny'}}))
    assert result['changed']
    body = client.policy_definitions.create_or_update.call_args.args[1]
    assert body.policy_rule['then']['effect'] == 'deny'


def test_definition_mode_defaults_are_idempotent():
    # The service behaves as if an omitted mode were Indexed.
    definition = models.PolicyDefinition(
        policy_rule={'if': {'field': 'type', 'equals': 'Microsoft.Compute/virtualMachines'},
                     'then': {'effect': 'audit'}},
        display_name='audit-vm-tags', mode='Indexed')
    obj, client = module(definition)
    assert not obj.exec_module(**params(mode=None, display_name='audit-vm-tags',
                                        description=None))['changed']
    client.policy_definitions.create_or_update.assert_not_called()


def test_definition_empty_metadata_is_idempotent():
    definition = models.PolicyDefinition(
        policy_rule={'if': {'field': 'type', 'equals': 'Microsoft.Compute/virtualMachines'},
                     'then': {'effect': 'audit'}},
        display_name='audit-vm-tags', mode='Indexed', metadata={})
    obj, client = module(definition)
    assert not obj.exec_module(**params(metadata={}, display_name='audit-vm-tags',
                                        description=None, mode=None))['changed']
    client.policy_definitions.create_or_update.assert_not_called()


def test_definition_service_metadata_is_ignored():
    definition = models.PolicyDefinition(
        policy_rule={'if': {'field': 'type', 'equals': 'Microsoft.Compute/virtualMachines'},
                     'then': {'effect': 'audit'}},
        display_name='audit-vm-tags', mode='Indexed',
        metadata={'createdBy': 'user', 'createdOn': '2026-11-23T16:10:11Z',
                  'updatedBy': 'user', 'updatedOn': '2026-11-23T16:10:14Z'})
    obj, client = module(definition)
    assert not obj.exec_module(**params(metadata=None, display_name='audit-vm-tags',
                                        description=None, mode=None))['changed']
    client.policy_definitions.create_or_update.assert_not_called()


def test_definition_service_parameter_objects_are_idempotent():
    # The service deserializes parameters into ParameterDefinitionsValue
    # objects while the task passes raw dicts.
    definition = models.PolicyDefinition(
        policy_rule={'if': {'field': "tags[parameters('tagName')]"},
                     'then': {'effect': 'audit'}},
        display_name='audit-vm-tags', mode='Indexed',
        parameters={'tagName': models.ParameterDefinitionsValue(
            type='String', metadata=models.ParameterDefinitionsValueMetadata(display_name='Tag name'))})
    obj, client = module(definition)
    assert not obj.exec_module(**params(
        policy_rule={'if': {'field': "tags[parameters('tagName')]"}, 'then': {'effect': 'audit'}},
        parameters={'tagName': {'type': 'String', 'metadata': {'displayName': 'Tag name'}}},
        mode='Indexed', display_name='audit-vm-tags', description=None))['changed']
    client.policy_definitions.create_or_update.assert_not_called()


def test_definition_parameter_change():
    obj, client = module(existing_definition())
    result = obj.exec_module(**params(parameters={'tagName': {'type': 'String'}}))
    assert result['changed']
    body = client.policy_definitions.create_or_update.call_args.args[1]
    assert body.parameters['tagName'].type == 'String'


def test_payload_parameters_are_converted_to_models():
    # The client rejects raw dicts where the API expects
    # ParameterDefinitionsValue objects.
    obj, client = module()
    client.policy_definitions.create_or_update.return_value = existing_definition()
    obj.exec_module(**params(parameters={'tagName': {'type': 'String',
                                                     'metadata': {'displayName': 'Tag name'}}}))
    body = client.policy_definitions.create_or_update.call_args.args[1]
    assert isinstance(body.parameters['tagName'], models.ParameterDefinitionsValue)
    assert body.parameters['tagName'].type == 'String'
    assert body.parameters['tagName'].metadata.display_name == 'Tag name'


def test_management_group_scope_uses_the_management_group_apis():
    obj, client = module()
    client.policy_definitions.create_or_update_at_management_group.return_value = existing_definition()
    result = obj.exec_module(**params(management_group='landing-zones'))
    assert result['changed']
    client.policy_definitions.get_at_management_group.assert_called_once_with(management_group_id='landing-zones', policy_definition_name='audit-vm-tags')
    body = client.policy_definitions.create_or_update_at_management_group.call_args.kwargs['parameters']
    client.policy_definitions.create_or_update_at_management_group.assert_called_once_with(
        management_group_id='landing-zones', policy_definition_name='audit-vm-tags', parameters=body)
    client.policy_definitions.get.assert_not_called()
    client.policy_definitions.create_or_update.assert_not_called()


def test_delete_policy_definition():
    obj, client = module(existing_definition())
    assert obj.exec_module(**params(state='absent'))['changed']
    client.policy_definitions.delete.assert_called_once_with('audit-vm-tags')


def test_delete_policy_definition_at_management_group_scope():
    obj, client = module(existing_definition())
    assert obj.exec_module(**params(state='absent', management_group='landing-zones'))['changed']
    client.policy_definitions.delete_at_management_group.assert_called_once_with(management_group_id='landing-zones', policy_definition_name='audit-vm-tags')


def test_delete_check_mode():
    obj, client = module(existing_definition(), check_mode=True)
    assert obj.exec_module(**params(state='absent'))['changed']
    client.policy_definitions.delete.assert_not_called()


def test_delete_idempotency():
    obj, client = module()
    assert not obj.exec_module(**params(state='absent'))['changed']
    client.policy_definitions.delete.assert_not_called()
