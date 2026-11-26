#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_policyassignment_info
version_added: "4.4.0"
short_description: Get Azure policy assignment facts
description:
    - Get one policy assignment or list policy assignments at the subscription, resource group, or an explicit scope.
options:
    name:
        description: Return only this policy assignment. When omitted, list assignments.
        type: str
    resource_group:
        description:
            - List assignments at the resource group scope.
            - Mutually exclusive with I(scope); when both are omitted assignments are listed at the subscription scope.
        type: str
    scope:
        description:
            - The full scope ID to query assignments at, for example a management group or an individual resource.
            - Mutually exclusive with I(resource_group); when both are omitted assignments are listed at the subscription scope.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get a policy assignment
  azure.azcollection.azure_rm_policyassignment_info:
    name: audit-vm-tags

- name: List policy assignments in the subscription
  azure.azcollection.azure_rm_policyassignment_info:

- name: List policy assignments at a resource group scope
  azure.azcollection.azure_rm_policyassignment_info:
    resource_group: analytics
'''

RETURN = '''
policy_assignments:
    description: List of policy assignments.
    returned: always
    type: list
    elements: dict
    sample: [{"name": "audit-vm-tags", "display_name": "Audit VM tags", "enforcement_mode": "Default",
              "scope": "/subscriptions/sub", "policy_definition_id": "/subscriptions/sub/providers/Microsoft.Authorization/policyDefinitions/audit-vm-tags"}]
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMPolicyAssignmentInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            scope=dict(type='str'),
        )
        self.results = dict(changed=False, policy_assignments=[])
        super(AzureRMPolicyAssignmentInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True,
            supports_tags=False, facts_module=True,
            mutually_exclusive=[('resource_group', 'scope')])

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        scope = self._scope()
        if self.name:
            try:
                assignments = [self.policy_client.policy_assignments.get(
                    scope=scope, policy_assignment_name=self.name)]
            except ResourceNotFoundError:
                assignments = []
            except Exception as exc:
                self.fail('Error retrieving policy assignment {0}: {1}'.format(self.name, str(exc)))
        elif self.resource_group:
            try:
                assignments = list(self.policy_client.policy_assignments.list_for_resource_group(
                    resource_group_name=self.resource_group))
            except Exception as exc:
                self.fail('Error listing policy assignments in resource group {0}: {1}'.format(
                    self.resource_group, str(exc)))
        elif self.scope:
            # There is no list-by-scope operation; fall back to the named lookup
            # requirement, which every scope supports.
            self.fail('name is required when scope is set')
        else:
            try:
                assignments = list(self.policy_client.policy_assignments.list())
            except Exception as exc:
                self.fail('Error listing policy assignments: {0}'.format(str(exc)))
        self.results['policy_assignments'] = [self._format(assignment) for assignment in assignments]
        return self.results

    def _scope(self):
        if self.scope:
            return self.scope
        if self.resource_group:
            return '/subscriptions/{0}/resourceGroups/{1}'.format(self.subscription_id, self.resource_group)
        return '/subscriptions/{0}'.format(self.subscription_id)

    def _format(self, assignment):
        return assignment.as_dict()


def main():
    AzureRMPolicyAssignmentInfo()


if __name__ == '__main__':
    main()
