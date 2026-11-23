#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_policydefinition_info
version_added: "4.3.0"
short_description: Get Azure policy definition facts
description:
    - Get one policy definition or list policy definitions at the subscription or management group scope.
options:
    name:
        description: Return only this policy definition. When omitted, list definitions.
        type: str
    management_group:
        description:
            - Query definitions at the management group scope instead of the subscription.
            - The management group ID (the last segment of the management group ID, not its display name).
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get a policy definition
  azure.azcollection.azure_rm_policydefinition_info:
    name: audit-vm-tags

- name: List policy definitions in the subscription
  azure.azcollection.azure_rm_policydefinition_info:

- name: List policy definitions at the management group scope
  azure.azcollection.azure_rm_policydefinition_info:
    management_group: landing-zones
'''

RETURN = '''
policy_definitions:
    description: List of policy definitions.
    returned: always
    type: list
    elements: dict
    sample: [{"name": "audit-vm-tags", "display_name": "Audit VM tags", "mode": "Indexed",
              "policy_type": "Custom",
              "policy_rule": {"if": {"field": "type", "equals": "Microsoft.Compute/virtualMachines"},
                              "then": {"effect": "audit"}}}]
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMPolicyDefinitionInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str'),
            management_group=dict(type='str'),
        )
        self.results = dict(changed=False, policy_definitions=[])
        super(AzureRMPolicyDefinitionInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True,
            supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            try:
                if self.management_group is None:
                    definitions = [self.policy_client.policy_definitions.get(self.name)]
                else:
                    definitions = [self.policy_client.policy_definitions.get_at_management_group(
                        self.management_group, self.name)]
            except ResourceNotFoundError:
                definitions = []
            except Exception as exc:
                self.fail('Error retrieving policy definition {0}: {1}'.format(self.name, str(exc)))
        else:
            try:
                if self.management_group is None:
                    definitions = list(self.policy_client.policy_definitions.list())
                else:
                    definitions = list(self.policy_client.policy_definitions.list_by_management_group(
                        self.management_group))
            except Exception as exc:
                self.fail('Error listing policy definitions: {0}'.format(str(exc)))
        self.results['policy_definitions'] = [self._format(definition) for definition in definitions]
        return self.results

    def _format(self, definition):
        return definition.as_dict()


def main():
    AzureRMPolicyDefinitionInfo()


if __name__ == '__main__':
    main()
