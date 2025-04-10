#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Python SDK Reference: https://learn.microsoft.com/en-us/python/api/azure-mgmt-cdn/azure.mgmt.cdn.operations.afdrulesetsoperations?view=azure-python
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_afdruleset_info
version_added: "3.4.0"
short_description: Get Azure Front Door Ruleset facts to be used with Standard or Premium Frontdoor Service
description:
    - Get facts for a specific Azure Front Door (AFD) Ruleset or all AFD Rulesets.
    - This differs from the Front Door classic service and only is intended to be used by the Standard or Premium service offering.

options:
    name:
        description:
            - Limit results to a specific AFD Ruleset.
        type: str
    profile_name:
        description:
            - Name of the Azure Front Door Standard or Azure Front Door Premium profile which is unique within the resource group.
        required: true
        type: str
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: true
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Jarret Tooley (@jartoo)
'''

EXAMPLES = '''
- name: Get facts for all Rulesets in AFD Profile
  azure_rm_afdruleset_info:
    resource_group: myResourceGroup
    profile_name: myProfile

- name: Get facts of specific AFD Ruleset
  azure_rm_afdruleset_info:
    name: myRuleset
    profile_name: myProfile
    resource_group: myResourceGroup
'''

RETURN = '''
afdrulesets:
    description: List of AFD Rulesets.
    returned: always
    type: complex
    contains:
        deployment_status:
            description:
                - Current state of the resource.
            type: str
            sample: NotStarted
        id:
            description:
                - ID of the AFD Ruleset.
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/myRG/providers/Microsoft.Cdn/profiles/myProf/rulesets/myRS"
        name:
            description:
                - Name of the AFD Ruleset.
            type: str
        profile_name:
            description:
                - The name of the profile which holds the rule set.
            type: str
        provisioning_state:
            description:
                - Provisioning status.
            type: str
            sample: Succeeded
        resource_group:
            description:
                - Name of a resource group.
            type: str
        type:
            description:
                - Resource type.
            type: str
            sample: Microsoft.Cdn/profiles/afdrulesets
'''

import re
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


AZURE_OBJECT_CLASS = 'Ruleset'


class AzureRMAFDRulesetInfo(AzureRMModuleBase):
    """Utility class to get Azure AFD Ruleset facts"""

    def __init__(self):

        self.module_args = dict(
            name=dict(
                type='str'
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            profile_name=dict(
                type='str',
                required=True
            )
        )

        self.results = dict(
            changed=False,
            afdrulesets=[]
        )

        self.name = None
        self.profile_name = None
        self.resource_group = None

        super(AzureRMAFDRulesetInfo, self).__init__(
            supports_check_mode=True,
            derived_arg_spec=self.module_args,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):

        for key in self.module_args:
            setattr(self, key, kwargs[key])

        if self.name:
            self.results['afdrulesets'] = self.get_item()
        else:
            self.results['afdrulesets'] = self.list_by_profile()

        return self.results

    def get_item(self):
        """Get a single Azure AFD Ruleset"""

        self.log('Get properties for {0}'.format(self.name))

        item = None
        result = []

        try:
            item = self.endpoint_client.rule_sets.get(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                rule_set_name=self.name)
        except Exception:
            pass

        if item:
            result = [self.serialize_afdruleset(item)]

        return result

    def list_by_profile(self):
        """Get all Azure AFD Rulesets within an AFD profile"""

        self.log('List all AFD Rulesets within an AFD profile')

        try:
            response = self.cdn_client.rule_sets.list_by_profile(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name)
        except Exception as exc:
            self.fail('Failed to list all items - {0}'.format(str(exc)))

        results = []
        for item in response:
            results.append(self.serialize_afdruleset(item))

        return results

    def serialize_afdruleset(self, afdruleset):
        '''
        Convert a AFD Ruleset object to dict.
        :param afdruleset: AFD Ruleset object
        :return: dict
        '''
        result = self.serialize_obj(afdruleset, AZURE_OBJECT_CLASS)

        new_result = {}
        new_result['deployment_status'] = afdruleset.deployment_status
        new_result['id'] = afdruleset.id
        new_result['name'] = afdruleset.name
        new_result['profile_name'] = re.sub('\\/.*', '', re.sub('.*profiles\\/', '', result['id']))
        new_result['provisioning_state'] = afdruleset.provisioning_state
        new_result['resource_group'] = re.sub('\\/.*', '', re.sub('.*resourcegroups\\/', '', result['id']))
        new_result['type'] = afdruleset.type
        return new_result


def main():
    """Main module execution code path"""
    AzureRMAFDRulesetInfo()


if __name__ == '__main__':
    main()
