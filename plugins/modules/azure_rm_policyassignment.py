#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_policyassignment
version_added: "4.4.0"
short_description: Manage an Azure policy assignment
description:
    - Create, update, or delete a policy assignment at the subscription, resource group, or an explicit scope.
    - Policy assignments are replaced wholesale on update; fields omitted from the task are removed.
options:
    name:
        description: Name of the policy assignment.
        required: true
        type: str
    policy_definition_id:
        description:
            - The resource ID of the policy definition or initiative (policy set definition) to assign.
            - Required when I(state=present).
        type: str
    display_name:
        description:
            - Display name of the policy assignment.
            - Defaults to the assignment name when omitted.
        type: str
    description:
        description: Description of the policy assignment.
        type: str
    enforcement_mode:
        description:
            - The enforcement mode of the policy assignment.
            - C(DoNotEnforce) records non-compliant resources but does not enforce the policy effect.
        type: str
        choices: [Default, DoNotEnforce]
        default: Default
    parameters:
        description:
            - Values for the parameters defined by the policy definition, as a dict of parameter
              names mapping to their I(value), for example C(tagName) with I(value) C(costCenter).
        type: dict
    resource_group:
        description:
            - Assign the policy at the resource group scope.
            - Mutually exclusive with I(scope); when both are omitted the assignment is created at the subscription scope.
        type: str
    scope:
        description:
            - The full scope ID to assign the policy at, for example a management group or an individual resource.
            - Mutually exclusive with I(resource_group); when both are omitted the assignment is created at the subscription scope.
        type: str
    state:
        description: Desired state of the policy assignment.
        type: str
        choices: [present, absent]
        default: present
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Assign a policy definition at the subscription scope
  azure.azcollection.azure_rm_policyassignment:
    name: audit-vm-tags
    policy_definition_id: /subscriptions/{{ subscription_id }}/providers/Microsoft.Authorization/policyDefinitions/audit-vm-tags
    display_name: Audit VM tags
    parameters:
      tagName:
        value: tags.costCenter

- name: Assign an initiative at a resource group scope without enforcing it
  azure.azcollection.azure_rm_policyassignment:
    name: landing-zone-baseline
    resource_group: analytics
    policy_definition_id: /providers/Microsoft.Authorization/policySetDefinitions/landing-zone-baseline
    enforcement_mode: DoNotEnforce

- name: Remove a policy assignment
  azure.azcollection.azure_rm_policyassignment:
    name: audit-vm-tags
    state: absent
'''

RETURN = '''
policy_assignment:
    description: The policy assignment.
    returned: when I(state=present)
    type: dict
    sample: {"name": "audit-vm-tags", "display_name": "Audit VM tags", "enforcement_mode": "Default",
             "policy_definition_id": "/subscriptions/sub/providers/Microsoft.Authorization/policyDefinitions/audit-vm-tags"}
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.mgmt.resource.policy import models
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMPolicyAssignment(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            policy_definition_id=dict(type='str'),
            display_name=dict(type='str'),
            description=dict(type='str'),
            enforcement_mode=dict(type='str', choices=['Default', 'DoNotEnforce'], default='Default'),
            parameters=dict(type='dict'),
            resource_group=dict(type='str'),
            scope=dict(type='str'),
            state=dict(type='str', choices=['present', 'absent'], default='present'),
        )

        self.name = None
        self.policy_definition_id = None
        self.display_name = None
        self.description = None
        self.enforcement_mode = None
        self.parameters = None
        self.resource_group = None
        self.scope = None
        self.state = None

        self.results = dict(changed=False)

        super(AzureRMPolicyAssignment, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=False,
            mutually_exclusive=[('resource_group', 'scope')],
            required_if=[('state', 'present', ('policy_definition_id',))])

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        scope = self._scope()
        existing = self.get_policy_assignment(scope)

        if self.state == 'absent':
            if existing is not None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.delete_policy_assignment(scope)
            return self.results

        desired = self._policy_assignment()
        self.results['changed'] = existing is None or self._comparable(existing) != self._comparable(desired)

        if not self.results['changed']:
            self.results['policy_assignment'] = self._format(existing)
            return self.results
        if self.check_mode:
            self.results['policy_assignment'] = self._format(desired)
            return self.results

        try:
            assignment = self.policy_client.policy_assignments.create(
                scope=scope, policy_assignment_name=self.name, parameters=desired)
        except Exception as exc:
            self.fail('Error creating / updating policy assignment {0}: {1}'.format(self.name, str(exc)))

        self.results['policy_assignment'] = self._format(assignment)
        return self.results

    def _scope(self):
        if self.scope:
            return self.scope
        if self.resource_group:
            return '/subscriptions/{0}/resourceGroups/{1}'.format(self.subscription_id, self.resource_group)
        return '/subscriptions/{0}'.format(self.subscription_id)

    def get_policy_assignment(self, scope):
        self.log('Get policy assignment {0}'.format(self.name))
        try:
            return self.policy_client.policy_assignments.get(scope=scope, policy_assignment_name=self.name)
        except ResourceNotFoundError:
            return None
        except Exception as exc:
            self.fail('Error retrieving policy assignment {0}: {1}'.format(self.name, str(exc)))

    def delete_policy_assignment(self, scope):
        self.log('Delete policy assignment {0}'.format(self.name))
        try:
            self.policy_client.policy_assignments.delete(scope=scope, policy_assignment_name=self.name)
        except Exception as exc:
            self.fail('Error deleting policy assignment {0}: {1}'.format(self.name, str(exc)))

    def _policy_assignment(self):
        """Build the assignment payload; the task is authoritative for every field."""
        return models.PolicyAssignment(
            policy_definition_id=self.policy_definition_id,
            display_name=self.display_name or self.name,
            description=self.description,
            enforcement_mode=self.enforcement_mode,
            parameters={name: models.ParameterValuesValue.from_dict(value)
                        for name, value in self.parameters.items()} if self.parameters else None,
        )

    def _comparable(self, assignment):
        return dict(
            policy_definition_id=assignment.policy_definition_id,
            display_name=assignment.display_name,
            description=assignment.description or None,
            # The service behaves as if an omitted enforcement mode were Default.
            enforcement_mode=assignment.enforcement_mode or 'Default',
            parameters={name: value.as_dict()
                        for name, value in (assignment.parameters or {}).items()},
        )

    def _format(self, assignment):
        return assignment.as_dict()


def main():
    AzureRMPolicyAssignment()


if __name__ == '__main__':
    main()
