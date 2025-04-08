#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Python SDK Reference: https://learn.microsoft.com/en-us/python/api/azure-mgmt-cdn/azure.mgmt.cdn.operations.rulesoperations?view=azure-python
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_afdrules_info
version_added: "3.4.0"
short_description: Get Azure Front Door Rule facts to be used with Standard or Premium Frontdoor Service
description:
    - Get facts for a specific Azure Front Door (AFD) Rule or all AFD Rules in a Ruleset.
    - This differs from the Front Door classic service and only is intended to be used by the Standard or Premium service offering.

options:
    name:
        description:
            - Name of the delivery rule which is unique within the endpoint.
        type: str
    profile_name:
        description:
            - Name of the Azure Front Door Standard or Azure Front Door Premium profile which is unique within the resource group
        required: true
        type: str
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: true
        type: str
    rule_set_name:
        description:
            - Name of the rule set under the profile.
        required: true
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Jarret Tooley (@jartoo)
'''

EXAMPLES = '''
- name: Get facts for all Rules in the AFD Profile
  azure_rm_afdrule_info:
    rule_set_name: myRuleset
    profile_name: myProfile
    resource_group: myResourceGroup

- name: Get facts of specific AFD Rule
  azure_rm_afdrule_info:
    name: myRule1
    rule_set_name: myRuleset
    profile_name: myProfile
    resource_group: myResourceGroup
'''

RETURN = '''
afdrules:
    description: List of AFD Rules.
    returned: always
    type: complex
    contains:
        actions:
            description:
                - A list of actions that are executed when all the conditions of a rule are satisfied.
            type: list
            elements: dict
            contains:
                cache_behavior:
                    description:
                        - Caching behavior for the requests.
                    type: str
                cache_duration:
                    description:
                        - The duration for which the content needs to be cached. Allowed format is [d.]hh:mm:ss.
                    type: str
                custom_fragment:
                    description:
                        - Fragment to add to the redirect URL. Fragment is the part of the URL that comes after #. Do not include the #
                    type: str
                custom_hostname:
                    description:
                        - Host to redirect. Leave empty to use the incoming host as the destination host.
                    type: str
                custom_path:
                    description:
                        - The full path to redirect. Path cannot be empty and must start with /. Leave empty to use the incoming path as destination path.
                    type: str
                custom_query_string:
                    description:
                        - The set of query strings to be placed in the redirect URL.
                        - Setting this value would replace any existing query string; leave empty to preserve the incoming query string.
                        - Query string must be in <key>=:code:<value> format. ? and & will be added automatically so do not include them.
                    type: str
                destination:
                    description:
                        - Define the relative URL to which the above requests will be rewritten by.
                    type: str
                destination_protocol:
                    description:
                        - Protocol to use for the redirect.
                    type: str
                forwarding_protocol:
                    description:
                        - Protocol this rule will use when forwarding traffic to backends.
                    type: str
                header_action:
                    description:
                        - Action to perform.
                    type: str
                header_name:
                    description:
                        - Name of the header to modify.
                    type: str
                is_compression_enabled:
                    description:
                        - The caching configuration for this route. Indicates whether content compression is enabled on AzureFrontDoor.
                        - If compression is enabled, content will be served as compressed if user requests for a compressed version.
                        - Content won't be compressed on AzureFrontDoor when requested content is smaller than 1 byte or larger than 1 MB.
                    type: str
                name:
                    description:
                        - The name of the action for the delivery rule.
                    type: str
                origin_group:
                    description:
                        - defines the OriginGroup that would override the DefaultOriginGroup.
                    type: str
                preserve_unmatched_path:
                    description:
                        - Whether to preserve unmatched path.
                    type: bool
                query_parameters:
                    description:
                        - query parameters to include or exclude (comma separated).
                    type: str
                query_string_caching_behavior:
                    description:
                        - The caching configuration for this route. Defines how Frontdoor caches requests that include query strings.
                        - You can ignore any query strings when caching, ignore specific query strings, cache every request with a unique URL,
                        - or cache specific query strings.
                    type: str
                redirect_type:
                    description:
                        - The redirect type the rule will use when redirecting traffic.
                    type: str
                source_pattern:
                    description:
                        - Define a request URI pattern that identifies the type of requests that may be rewritten.
                        - If value is blank, all strings are matched.
                    type: str
                value:
                    description:
                        - Value for the specified action.
                    type: str
        conditions:
            description:
                - A list of conditions that must be matched for the actions to be executed.
            type: list
            elements: dict
            contains:
                name:
                    description:
                        - The name of the condition for the delivery rule.
                    type: str
                operator:
                    description:
                        - Describes operator to be matched.
                    type: str
                match_values:
                    description:
                        - The match value for the condition of the delivery rule.
                    type: list
                    elements: str
                negate_condition:
                    description:
                        - Describes if this is a negate condition or not.
                    type: bool
                selector:
                    description:
                        - Name of item to be matched.
                    type: str
                transforms:
                    description:
                        - List of transforms.
                    type: list
                    elements: str
        match_processing_behavior:
            description:
                - If this rule is a match should the rules engine continue running the remaining rules or stop.
            type: str
        name:
            description:
                - Name of the delivery rule which is unique within the endpoint.
            type: str
        order:
            description:
                - The order in which the rules are applied for the endpoint.
                - A rule with a lesser order will be applied before a rule with a greater order. Rule with order 0 is a special rule.
                - It does not require any condition and actions listed in it will always be applied.
            type: int
        profile_name:
            description:
                - Name of the Azure Front Door Standard or Azure Front Door Premium profile which is unique within the resource group.
            type: str
        resource_group:
            description:
                - Name of the Resource group within the Azure subscription.
            type: str
        rule_set_name:
            description:
                - Name of the rule set under the profile.
            type: str
        state:
            description:
                - Assert the state of the CDN profile. Use C(present) to create or update a CDN profile and C(absent) to delete it.
            type: str
        type:
            description:
                - Resource type.
            type: str
'''

# import re
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


AZURE_OBJECT_CLASS = 'AFDRules'


class AzureRMAFDRuleInfo(AzureRMModuleBase):
    """Utility class to get Azure AFD Rule facts"""

    def __init__(self):

        self.module_args = dict(
            name=dict(type='str'),
            profile_name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            rule_set_name=dict(type='str', required=True)
        )

        self.results = dict(
            changed=False,
            afdrules=[]
        )

        self.name = None
        self.profile_name = None
        self.resource_group = None
        self.rule_set_name = None

        super(AzureRMAFDRuleInfo, self).__init__(
            supports_check_mode=True,
            derived_arg_spec=self.module_args,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):

        for key in self.module_args:
            setattr(self, key, kwargs[key])

        if self.name:
            self.results['afdrules'] = self.get_item()
        else:
            self.results['afdrules'] = self.list_by_endpoint()

        return self.results

    def get_item(self):
        """Get a single Azure AFD Rule"""

        self.log('Get properties for {0}'.format(self.name))

        item = None
        result = []

        try:
            item = self.cdn_client.rules.get(resource_group_name=self.resource_group,
                                             profile_name=self.profile_name,
                                             rule_set_name=self.rule_set_name,
                                             rule_name=self.name)
        except Exception as exc:
            self.log("Failed to find an existing resource. {0}".format(str(exc)))

        if item:
            result = [self.serialize_afdrule(item)]

        return result

    def list_by_endpoint(self):
        """Get all Azure AFD Rules within an AFD profile"""

        self.log('List all AFD Rules within an AFD profile')

        try:
            response = self.cdn_client.rules.list_by_rule_set(resource_group_name=self.resource_group,
                                                              profile_name=self.profile_name,
                                                              rule_set_name=self.rule_set_name)
        except Exception as exc:
            self.fail('Failed to list all items - {0}'.format(str(exc)))

        results = []
        for item in response:
            results.append(self.serialize_afdrule(item))

        return results

    def serialize_afdrule(self, rules):
        '''
        Convert a AFD Rule object to dict.
        :param afdrule: AFD Rule object
        :return: dict
        '''
        return dict(
            actions=parse_action_condition(rules.actions),
            conditions=parse_action_condition(rules.conditions),
            deployment_status=rules.deployment_status,
            id=rules.id,
            match_processing_behavior=rules.match_processing_behavior,
            name=rules.name,
            order=rules.order,
            provisioning_state=rules.provisioning_state,
            rule_set_name=rules.rule_set_name,
            type=rules.type
        )


def parse_action_condition(items):
    ''' Convert Actions and Conditions objects to list '''

    parsed = []
    for item in items:
        new_item = {}
        vitem = vars(item)
        for field in vitem:
            if field == 'parameters':
                subvitem = vars(vitem.get('parameters'))
                for subfield in subvitem:
                    if subfield == 'origin_group_override':
                        ogo = subvitem["origin_group_override"]
                        new_item["forwarding_protocol"] = None
                        new_item['origin_group_id'] = None
                        if ogo:
                            new_item["forwarding_protocol"] = ogo.forwarding_protocol
                            og = ogo.origin_group
                            if og:
                                new_item['origin_group_id'] = og.id
                    elif subfield == 'cache_configuration':
                        cc = subvitem["cache_configuration"]
                        new_item["query_string_caching_behavior"] = None
                        new_item['query_parameters'] = None
                        new_item['is_compression_enabled'] = None
                        new_item['cache_behavior'] = None
                        new_item['cache_duration'] = None
                        if cc:
                            new_item["query_string_caching_behavior"] = ogo.query_string_caching_behavior
                            new_item["query_parameters"] = ogo.query_parameters
                            new_item["is_compression_enabled"] = ogo.is_compression_enabled
                            new_item["cache_behavior"] = ogo.cache_behavior
                            new_item["cache_duration"] = ogo.cache_duration
                    elif subfield != 'additional_properties':
                        new_item[subfield] = subvitem[subfield]
            elif field != 'additional_properties':
                new_item[field] = vitem[field]
        parsed.append(new_item)
    return parsed


def main():
    """Main module execution code path"""
    AzureRMAFDRuleInfo()


if __name__ == '__main__':
    main()
