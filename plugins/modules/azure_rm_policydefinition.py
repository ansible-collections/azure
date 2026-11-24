#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_policydefinition
version_added: "4.3.0"
short_description: Manage an Azure policy definition
description:
    - Create, update, or delete a resource policy definition at the subscription or management group scope.
    - Policy definitions are replaced wholesale on update; fields omitted from the task are removed.
options:
    name:
        description: Name of the policy definition.
        required: true
        type: str
    policy_rule:
        description: The policy rule, as a dict following the Azure policy rule structure.
        type: dict
    display_name:
        description:
            - Display name of the policy definition.
            - Defaults to the definition name when omitted.
        type: str
    description:
        description: Description of the policy definition.
        type: str
    mode:
        description:
            - The policy definition mode, for example C(Default), C(All), C(Indexed), or a
              resource-provider mode such as C(Microsoft.Kubernetes.Data).
            - An omitted mode behaves as C(Indexed).
        type: str
    metadata:
        description:
            - Additional metadata for the policy definition.
            - The service adds I(createdBy), I(createdOn), I(updatedBy) and I(updatedOn) metadata keys of
              its own; they are ignored when comparing the desired and stored definitions.
        type: dict
    parameters:
        description: Parameter definitions for the policy rule.
        type: dict
    management_group:
        description:
            - Manage the definition at the management group scope instead of the subscription.
            - The management group ID (the last segment of the management group ID, not its display name).
        type: str
    state:
        description: Desired state of the policy definition.
        type: str
        choices: [present, absent]
        default: present
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create a policy definition at the subscription scope
  azure.azcollection.azure_rm_policydefinition:
    name: audit-vm-tags
    display_name: Audit VM tags
    description: Audits virtual machines missing the required tags
    mode: Indexed
    policy_rule:
      if:
        allOf:
          - field: type
            equals: Microsoft.Compute/virtualMachines
          - field: tags.costCenter
            exists: false
      then:
        effect: audit

- name: Create a parameterized definition at the management group scope
  azure.azcollection.azure_rm_policydefinition:
    name: audit-vm-tags
    management_group: landing-zones
    parameters:
      tagName:
        type: String
        metadata:
          displayName: Tag name
    policy_rule:
      if:
        field: tags.[parameters('tagName')]
        exists: false
      then:
        effect: audit

- name: Remove a policy definition
  azure.azcollection.azure_rm_policydefinition:
    name: audit-vm-tags
    state: absent
'''

RETURN = '''
policy_definition:
    description: The policy definition.
    returned: when I(state=present)
    type: dict
    sample: {"name": "audit-vm-tags", "display_name": "Audit VM tags", "mode": "Indexed",
             "policy_type": "Custom", "policy_rule": {"if": {"field": "type", "equals": "Microsoft.Compute/virtualMachines"},
                                                      "then": {"effect": "audit"}}}
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.mgmt.resource.policy import models
    from azure.mgmt.resource.policy import _serialization
    from azure.mgmt.resource.policy.v2023_04_01 import models as _models
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

# The service adds these metadata keys to every custom policy definition;
# they are not task-managed and are ignored when detecting changes.
SERVICE_METADATA_KEYS = ('createdBy', 'createdOn', 'updatedBy', 'updatedOn')


class AzureRMPolicyDefinition(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            policy_rule=dict(type='dict'),
            display_name=dict(type='str'),
            description=dict(type='str'),
            mode=dict(type='str'),
            metadata=dict(type='dict'),
            parameters=dict(type='dict'),
            management_group=dict(type='str'),
            state=dict(type='str', choices=['present', 'absent'], default='present'),
        )

        self.name = None
        self.policy_rule = None
        self.display_name = None
        self.description = None
        self.mode = None
        self.metadata = None
        self.parameters = None
        self.management_group = None
        self.state = None

        self.results = dict(changed=False)

        super(AzureRMPolicyDefinition, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=False,
            required_if=[('state', 'present', ('policy_rule',))])

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        existing = self.get_policy_definition()

        if self.state == 'absent':
            if existing is not None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.delete_policy_definition()
            return self.results

        desired = self._policy_definition()
        self.results['changed'] = existing is None or self._comparable(existing) != self._comparable(desired)

        if not self.results['changed']:
            self.results['policy_definition'] = self._format(existing)
            return self.results
        if self.check_mode:
            self.results['policy_definition'] = self._format(desired)
            return self.results

        try:
            definition = self.policy_client.policy_definitions.create_or_update(
                self.name, desired) if self.management_group is None else \
                self.policy_client.policy_definitions.create_or_update_at_management_group(
                    self.management_group, self.name, desired)
        except Exception as exc:
            self.fail('Error creating / updating policy definition {0}: {1}'.format(self.name, str(exc)))

        self.results['policy_definition'] = self._format(definition)
        return self.results

    def get_policy_definition(self):
        self.log('Get policy definition {0}'.format(self.name))
        try:
            if self.management_group is None:
                return self.policy_client.policy_definitions.get(self.name)
            return self.policy_client.policy_definitions.get_at_management_group(self.management_group, self.name)
        except ResourceNotFoundError:
            return None
        except Exception as exc:
            self.fail('Error retrieving policy definition {0}: {1}'.format(self.name, str(exc)))

    def delete_policy_definition(self):
        self.log('Delete policy definition {0}'.format(self.name))
        try:
            if self.management_group is None:
                self.policy_client.policy_definitions.delete(self.name)
            else:
                self.policy_client.policy_definitions.delete_at_management_group(self.management_group, self.name)
        except Exception as exc:
            self.fail('Error deleting policy definition {0}: {1}'.format(self.name, str(exc)))

    def _policy_definition(self):
        """Build the definition payload; the task is authoritative for every field."""
        return models.PolicyDefinition(
            policy_rule=self.policy_rule,
            display_name=self.display_name or self.name,
            description=self.description,
            mode=self.mode,
            metadata=self.metadata,
            parameters=self._parameter_models(self.parameters),
        )

    def _comparable(self, definition):
        metadata = {key: value for key, value in (definition.metadata or {}).items()
                    if key not in SERVICE_METADATA_KEYS}
        return dict(
            policy_rule=definition.policy_rule,
            display_name=definition.display_name,
            description=definition.description or None,
            # The service behaves as if an omitted mode were Indexed.
            mode=definition.mode or 'Indexed',
            metadata=metadata,
            parameters=self._parameter_definitions(definition.parameters),
        )

    @staticmethod
    def _parameter_models(parameters):
        """Convert the task's raw parameter definitions to SDK models.

        The client rejects raw dicts where the API expects
        ParameterDefinitionsValue objects, so the task's wire dicts are
        deserialized into the models the payload requires.
        """
        if not parameters:
            return None
        deserializer = _serialization.Deserializer(
            {name: cls for name, cls in _models.__dict__.items() if isinstance(cls, type)})
        return {name: deserializer._deserialize('ParameterDefinitionsValue', value)
                for name, value in parameters.items()}

    @staticmethod
    def _parameter_definitions(parameters):
        """Normalize parameter definitions to their REST wire dicts.

        Both the service response and the payload carry
        ParameterDefinitionsValue objects, so both sides are compared in
        the wire format -- the one the service round-trips.
        """
        if not parameters:
            return {}
        serializer = _serialization.Serializer(
            {name: cls for name, cls in _models.__dict__.items() if isinstance(cls, type)})
        return {name: serializer.body(value, 'ParameterDefinitionsValue')
                for name, value in parameters.items()}

    def _format(self, definition):
        result = definition.as_dict()
        return result


def main():
    AzureRMPolicyDefinition()


if __name__ == '__main__':
    main()
