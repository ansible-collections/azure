#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_firewallpolicyrulecollectiongroup_info
version_added: "3.19.0"
short_description: Get facts about rule collection groups of an Azure Firewall Policy
description:
    - Get facts about a specific rule collection group, or list all rule collection groups
      of a given Azure Firewall Policy.
options:
    resource_group:
        description:
            - Name of the resource group.
        required: true
        type: str
    firewall_policy_name:
        description:
            - The name of the parent firewall policy.
        required: true
        type: str
    name:
        description:
            - The name of the rule collection group.
            - If omitted, all rule collection groups of the firewall policy are returned.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Get facts of one rule collection group
  azure_rm_firewallpolicyrulecollectiongroup_info:
    resource_group: myResourceGroup
    firewall_policy_name: myFirewallPolicy
    name: myRuleCollectionGroup

- name: List all rule collection groups of a firewall policy
  azure_rm_firewallpolicyrulecollectiongroup_info:
    resource_group: myResourceGroup
    firewall_policy_name: myFirewallPolicy
'''

RETURN = '''
rule_collection_groups:
    description:
        - List of rule collection groups.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
        name:
            description:
                - Resource name.
            returned: always
            type: str
        priority:
            description:
                - Priority of the rule collection group.
            returned: always
            type: int
        provisioning_state:
            description:
                - Provisioning state.
            returned: always
            type: str
        rule_collections:
            description:
                - Group of rule collections.
            returned: always
            type: list
            elements: dict
        etag:
            description:
                - Resource ETag.
            returned: always
            type: str
        type:
            description:
                - Resource type.
            returned: always
            type: str
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # Handled in azure_rm_common
    pass


class AzureRMFirewallPolicyRuleCollectionGroupInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            firewall_policy_name=dict(type='str', required=True),
            name=dict(type='str'),
        )

        self.results = dict(
            changed=False,
            rule_collection_groups=[],
        )

        self.resource_group = None
        self.firewall_policy_name = None
        self.name = None

        super(AzureRMFirewallPolicyRuleCollectionGroupInfo, self).__init__(
            self.module_arg_spec,
            supports_check_mode=True,
            facts_module=True,
            supports_tags=False,
        )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            items = self.get_item()
        else:
            items = self.list_items()

        self.results['rule_collection_groups'] = [item.as_dict() for item in items]
        return self.results

    def get_item(self):
        try:
            item = self.network_client.firewall_policy_rule_collection_groups.get(
                resource_group_name=self.resource_group,
                firewall_policy_name=self.firewall_policy_name,
                rule_collection_group_name=self.name,
            )
            return [item]
        except ResourceNotFoundError:
            return []

    def list_items(self):
        try:
            return list(self.network_client.firewall_policy_rule_collection_groups.list(
                resource_group_name=self.resource_group,
                firewall_policy_name=self.firewall_policy_name,
            ))
        except Exception as exc:
            self.fail("Error listing rule collection groups for firewall policy {0} - {1}".format(
                self.firewall_policy_name, str(exc)))


def main():
    AzureRMFirewallPolicyRuleCollectionGroupInfo()


if __name__ == '__main__':
    main()
