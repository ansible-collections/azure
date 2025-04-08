#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Python SDK Reference: https://learn.microsoft.com/en-us/python/api/azure-mgmt-cdn/azure.mgmt.cdn.operations.rulesoperations?view=azure-python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_afdrules
version_added: "3.4.0"
short_description: Manage an Azure Front Door Rules
description:
    - Create, update and delete an Azure Front Door Rules to be used by a Front Door Service Profile created using azure_rm_cdnprofile.

options:
    actions:
        description:
            - A list of actions that are executed when all the conditions of a rule are satisfied.
        type: list
        elements: dict
        suboptions:
            cache_behavior:
                description:
                    - Caching behavior for the requests.
                type: str
                choices:
                    - BypassCache
                    - Override
                    - SetIfMissing
                    - HonorOrigin
                    - OverrideAlways
                    - OverrideIfOriginMissing
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
                default: MatchRequest
                type: str
                choices:
                    - Http
                    - Https
                    - MatchRequest
            forwarding_protocol:
                description:
                    - Protocol this rule will use when forwarding traffic to backends.
                default: MatchRequest
                type: str
                choices:
                    - Http
                    - Https
                    - MatchRequest
            header_action:
                description:
                    - Action to perform.
                type: str
                choices:
                    - Append
                    - Overwrite
                    - Delete
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
                choices:
                    - Enabled
                    - Disabled
            name:
                description:
                    - The name of the action for the delivery rule.
                type: str
                required: true
                choices:
                    - ModifyRequestHeader
                    - ModifyResponseHeader
                    - RouteConfigurationOverride
                    - UrlRedirect
                    - UrlRewrite
            origin_group:
                description:
                    - defines the OriginGroup that would override the DefaultOriginGroup.
                type: str
            preserve_unmatched_path:
                description:
                    - Whether to preserve unmatched path.
                default: True
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
                choices:
                    - IgnoreQueryString
                    - UseQueryString
                    - IgnoreSpecifiedQueryStrings
                    - IncludeSpecifiedQueryStrings
            redirect_type:
                description:
                    - The redirect type the rule will use when redirecting traffic.
                type: str
                choices:
                    - Moved
                    - Found
                    - TemporaryRedirect
                    - PermanentRedirect
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
        suboptions:
            name:
                description:
                    - The name of the condition for the delivery rule.
                type: str
                required: true
                choices:
                    - ClientPort
                    - Cookies
                    - HostName
                    - HttpVersion
                    - IsDevice
                    - PostArgs
                    - QueryString
                    - RemoteAddress
                    - RequestBody
                    - RequestHeader
                    - RequestMethod
                    - RequestScheme
                    - RequestUri
                    - ServerPort
                    - SocketAddr
                    - SslProtocol
                    - UrlFileExtension
                    - UrlFileName
                    - UrlPath
            operator:
                description:
                    - Describes operator to be matched.
                type: str
                required: true
                choices:
                    - Any
                    - Equal
                    - Contains
                    - BeginsWith
                    - EndsWith
                    - LessThan
                    - LessThanOrEqual
                    - GreaterThan
                    - GreaterThanOrEqual
                    - RegEx
                    - IPMatch
                    - GeoMatch
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
                choices:
                    - Lowercase
                    - RemoveNulls
                    - Trim
                    - Uppercase
                    - URLDecode
                    - URLEncode
    match_processing_behavior:
        description:
            - If this rule is a match should the rules engine continue running the remaining rules or stop.
        default: Continue
        type: str
        choices:
            - Continue
            - Stop
    name:
        description:
            - Name of the delivery rule which is unique within the endpoint.
        required: true
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
    state:
        description:
            - Assert the state of the CDN profile. Use C(present) to create or update a CDN profile and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Jarret Tooley (@jartoo)
'''
EXAMPLES = '''
- name: Create an AFD Rule with some actions and conditions
  azure_rm_afdrules:
    name: myRule1
    rule_set_name: myRuleset
    profile_name: myProfile
    resource_group: myResourceGroup
    match_processing_behavior: Continue
    order: 1
    action:
      - name: ModifyResponseHeader
        header_action: Append
        header_name: Content-Security-Policy
        value: "frame-ancestors 'response'"
      - name: RouteConfigurationOverride
        origin_group: "myOtherOriginGroup"
    conditions:
      - name: UrlPath
        match_values:
          - ".auth"
        negate_condition: false
        operator: "BeginsWith"
        transforms:
          - LowerCase
'''
RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    example:  # TODO: Put example value in here
'''
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.mgmt.cdn.models import Rule, RuleUpdateParameters, ResourceReference

    # Models for Actions:
    from azure.mgmt.cdn.models import DeliveryRuleRequestHeaderAction, HeaderActionParameters  # ModifyRequestHeader
    from azure.mgmt.cdn.models import DeliveryRuleResponseHeaderAction  # ModifyResponseHeader
    from azure.mgmt.cdn.models import DeliveryRuleRouteConfigurationOverrideAction, RouteConfigurationOverrideActionParameters, \
        OriginGroupOverride, ForwardingProtocol, CacheConfiguration  # RouteConfigurationOverride
    from azure.mgmt.cdn.models import UrlRedirectAction, UrlRedirectActionParameters  # UrlRedirect
    from azure.mgmt.cdn.models import UrlRewriteAction, UrlRewriteActionParameters  # UrlRewrite

    # Models for Conditions:
    from azure.mgmt.cdn.models import DeliveryRuleClientPortCondition, ClientPortMatchConditionParameters  # ClientPort
    from azure.mgmt.cdn.models import DeliveryRuleCookiesCondition, CookiesMatchConditionParameters  # Cookies
    from azure.mgmt.cdn.models import DeliveryRuleHostNameCondition, HostNameMatchConditionParameters  # HostName
    from azure.mgmt.cdn.models import DeliveryRuleHttpVersionCondition, HttpVersionMatchConditionParameters  # HttpVersion
    from azure.mgmt.cdn.models import DeliveryRuleIsDeviceCondition, IsDeviceMatchConditionParameters  # IsDevice
    from azure.mgmt.cdn.models import DeliveryRulePostArgsCondition, PostArgsMatchConditionParameters  # PostArgs
    from azure.mgmt.cdn.models import DeliveryRuleQueryStringCondition, QueryStringMatchConditionParameters  # QueryString
    from azure.mgmt.cdn.models import DeliveryRuleRemoteAddressCondition, RemoteAddressMatchConditionParameters  # RemoteAddress
    from azure.mgmt.cdn.models import DeliveryRuleRequestBodyCondition, RequestBodyMatchConditionParameters  # RequestBody
    from azure.mgmt.cdn.models import DeliveryRuleRequestHeaderCondition, RequestHeaderMatchConditionParameters  # RequestHeader
    from azure.mgmt.cdn.models import DeliveryRuleRequestMethodCondition, RequestMethodMatchConditionParameters  # RequestMethod
    from azure.mgmt.cdn.models import DeliveryRuleRequestSchemeCondition, RequestSchemeMatchConditionParameters  # RequestScheme
    from azure.mgmt.cdn.models import DeliveryRuleRequestUriCondition, RequestUriMatchConditionParameters  # RequestUri
    from azure.mgmt.cdn.models import DeliveryRuleServerPortCondition, ServerPortMatchConditionParameters  # ServerPort
    from azure.mgmt.cdn.models import DeliveryRuleSocketAddrCondition, SocketAddrMatchConditionParameters  # SocketAddr
    from azure.mgmt.cdn.models import DeliveryRuleSslProtocolCondition, SslProtocolMatchConditionParameters  # SslProtocol
    from azure.mgmt.cdn.models import DeliveryRuleUrlFileExtensionCondition, UrlFileExtensionMatchConditionParameters  # UrlFileExtension
    from azure.mgmt.cdn.models import DeliveryRuleUrlFileNameCondition, UrlFileNameMatchConditionParameters  # UrlFileName
    from azure.mgmt.cdn.models import DeliveryRuleUrlPathCondition, UrlPathMatchConditionParameters  # UrlPath

    from azure.core.serialization import NULL as AzureCoreNull
except ImportError as ec:
    # This is handled in azure_rm_common
    pass


class AzureRMRules(AzureRMModuleBase):
    ''' Class for Azure Front Door Rules '''

    def __init__(self):
        self.module_arg_spec = dict(
            actions=dict(
                type='list',
                elements='dict',
                options=dict(
                    cache_behavior=dict(
                        type='str',
                        choices=[
                            'BypassCache',
                            'Override',
                            'SetIfMissing',
                            'HonorOrigin',
                            'OverrideAlways',
                            'OverrideIfOriginMissing'
                        ]
                    ),
                    cache_duration=dict(type='str'),
                    custom_fragment=dict(type='str'),
                    custom_hostname=dict(type='str'),
                    custom_path=dict(type='str'),
                    custom_query_string=dict(type='str'),
                    destination=dict(type='str'),
                    destination_protocol=dict(
                        type='str',
                        default='MatchRequest',
                        choices=['Http', 'Https', 'MatchRequest']
                    ),
                    forwarding_protocol=dict(
                        type='str',
                        default="MatchRequest",
                        choices=['Http', 'Https', 'MatchRequest']
                    ),
                    header_action=dict(
                        type='str',
                        choices=['Append', 'Overwrite', 'Delete']
                    ),
                    header_name=dict(type='str'),
                    is_compression_enabled=dict(
                        type='str',
                        choices=['Enabled', 'Disabled']
                    ),
                    name=dict(
                        type='str',
                        required=True,
                        choices=[
                            'ModifyRequestHeader',
                            'ModifyResponseHeader',
                            'RouteConfigurationOverride',
                            'UrlRedirect',
                            'UrlRewrite'
                        ]
                    ),
                    origin_group=dict(type='str'),
                    preserve_unmatched_path=dict(type='bool', default=True),
                    query_parameters=dict(type='str'),
                    query_string_caching_behavior=dict(
                        type='str',
                        choices=[
                            "IgnoreQueryString",
                            "UseQueryString",
                            "IgnoreSpecifiedQueryStrings",
                            "IncludeSpecifiedQueryStrings"
                        ]
                    ),
                    redirect_type=dict(
                        type='str',
                        choices=[
                            "Moved",
                            "Found",
                            "TemporaryRedirect",
                            "PermanentRedirect"
                        ]
                    ),
                    source_pattern=dict(type='str'),
                    value=dict(type='str')
                )
            ),
            conditions=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(
                        type='str',
                        required=True,
                        choices=[
                            "ClientPort",
                            "Cookies",
                            "HostName",
                            "HttpVersion",
                            "IsDevice",
                            "PostArgs",
                            "QueryString",
                            "RemoteAddress",
                            "RequestBody",
                            "RequestHeader",
                            "RequestMethod",
                            "RequestScheme",
                            "RequestUri",
                            "ServerPort",
                            "SocketAddr",
                            "SslProtocol",
                            "UrlFileExtension",
                            "UrlFileName",
                            "UrlPath"
                        ]
                    ),
                    operator=dict(
                        type='str',
                        required=True,
                        choices=[
                            'Any',
                            'Equal',
                            'Contains',
                            'BeginsWith',
                            'EndsWith',
                            'LessThan',
                            'LessThanOrEqual',
                            'GreaterThan',
                            'GreaterThanOrEqual',
                            'RegEx',
                            'IPMatch',
                            'GeoMatch'
                        ]
                    ),
                    match_values=dict(type='list', elements='str'),
                    negate_condition=dict(type='bool'),
                    selector=dict(type='str'),
                    transforms=dict(
                        type='list',
                        elements='str',
                        choices=[
                            'Lowercase',
                            'RemoveNulls',
                            'Trim',
                            'Uppercase',
                            'URLDecode',
                            'URLEncode'
                        ]
                    )
                )
            ),
            match_processing_behavior=dict(
                type='str',
                default='Continue',
                choices=['Continue', 'Stop']
            ),
            name=dict(type='str', required=True),
            order=dict(type='int'),
            profile_name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            rule_set_name=dict(type='str', required=True),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )
        self.actions = None
        self.conditions = None
        self.match_processing_behavior = None
        self.rule_set_name = None

        self.name = None
        self.order = None
        self.profile_name = None
        self.resource_group = None
        self.state = None

        self.response = None
        self.parameters = None

        self.results = dict(changed=False)

        super(AzureRMRules, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False)

    def check_for_field(self, param_list, item, field):
        ''' Utility to check for a field and fail if not found '''
        if field not in param_list.keys():
            self.fail('Required field {1} missing for {0}'.format(item, field))
        elif param_list[field] is None:
            self.fail('Required field {1} missing for {0}'.format(item, field))
        return

    def check_required_fields(self):
        ''' A slightly more complex parameters check for Actions and Conditions '''

        if self.actions:
            required_fields_actions = {
                'ModifyRequestHeader': ['header_action', 'header_name'],
                'ModifyResponseHeader': ['header_action', 'header_name'],
                'RouteConfigurationOverride': [],
                'UrlRedirect': ['redirect_type', 'custom_path'],
                'UrlRewrite': ['source_pattern', 'destination']
            }
            for action in self.actions:
                if 'name' not in action.keys():
                    self.fail("Required field 'Name' missing for Action")
                fields = required_fields_actions[action['name']]
                for field in fields:
                    self.check_for_field(action, action['name'], field)

            if len(self.actions) > 10:
                self.fail("Error: You cannot have more than 10 Actions in a single Rule.")

        if self.conditions:
            for condition in self.conditions:
                if 'name' not in condition.keys():
                    self.fail("Required field 'Name' missing for Condition")
                field = "operator"
                self.check_for_field(condition, condition['name'], field)

            if len(self.conditions) > 10:
                self.fail("Error: You cannot have more than 10 Conditions in a single Rule.")

        return False

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self.check_required_fields()

        self.response = self.get_rule()

        if self.state == 'present':

            if not self.response:
                self.log("Need to create the Rule")
                self.build_parameters()

                if not self.check_mode:
                    new_response = self.create_rules()
                    self.results['id'] = new_response['id']

                self.results['changed'] = True

            else:
                self.build_parameters(update=True)
                if self.check_if_rules_are_different():
                    self.update_rules()
                    self.results['changed'] = True

                self.results['id'] = self.response['id']
                self.log('Results : {0}'.format(self.response))

        elif self.state == 'absent':
            if not self.response:
                self.log("Rule {0} does not exist.".format(self.name))
            else:
                self.log("Need to delete the Rule")
                self.results['changed'] = True

                self.results['id'] = self.response['id']
                if not self.check_mode:
                    self.delete_rules()

        return self.results

    def create_rules(self):
        '''
        Creates a Azure Rules.

        :return: deserialized Azure Rules instance state dictionary
        '''
        self.log("Creating the Azure Rules instance {0}".format(self.name))

        try:
            poller = self.cdn_client.rules.begin_create(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                rule_set_name=self.rule_set_name,
                rule_name=self.name,
                rule=self.parameters
            )
            response = self.get_poller_result(poller)
            return rules_to_dict(response)
        except Exception as exc:
            self.log('Error attempting to create Azure Rules instance.')
            self.fail("Error Creating Azure Rules instance: {0}".format(str(exc)))

    def update_rules(self):
        '''
        Update Azure Rules.

        :return: deserialized Azure Rules instance state dictionary
        '''
        self.log("Updating the Azure Rules instance {0}".format(self.name))

        try:
            poller = self.cdn_client.rules.begin_update(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                rule_set_name=self.rule_set_name,
                rule_name=self.name,
                rule_update_properties=self.parameters
            )
            response = self.get_poller_result(poller)
            return rules_to_dict(response)
        except Exception as exc:
            self.log('Error attempting to update Azure Rules instance.')
            self.fail("Error Updating Azure Rules instance: {0}".format(str(exc)))

    def check_if_rules_are_different(self):
        ''' Check if the Rules are different from what exists and what is defined in the yaml '''

        if self.response['match_processing_behavior'] != self.match_processing_behavior:
            return True
        if self.response['order'] != self.order:
            return True

        if len(self.response['actions']) != len(self.actions):
            return True
        for i, item in enumerate(self.response['actions']):
            for field in item:
                if field not in ['type_name']:
                    if field not in ['cache_configuration', 'origin_group_override']:
                        if item[field] != self.actions[i][field]:
                            return True
                    elif field == 'origin_group_override':
                        if (not item[field] and self.actions[i].get("origin_group")) or (item[field] and not self.actions[i].get("origin_group")):
                            return True
                        if item[field] and self.actions[i].get("origin_group"):  # They both exist so check if the values match
                            origin_group_id = item[field].origin_group.id
                            forwarding_protocol = item[field].forwarding_protocol
                            if origin_group_id != self.actions[i].get("origin_group_id"):
                                return True
                            if forwarding_protocol != self.actions[i].get("forwarding_protocol"):
                                return True
                    elif field == 'cache_configuration':
                        if not item[field] and (
                            self.actions[i].get("query_string_caching_behavior") or
                            self.actions[i].get("query_parameters") or
                            self.actions[i].get("is_compression_enabled") or
                            self.actions[i].get("cache_behavior") or
                            self.actions[i].get("cache_duration")
                        ):
                            return True
                        elif item[field] and not (
                            self.actions[i].get("query_string_caching_behavior") or
                            self.actions[i].get("query_parameters") or
                            self.actions[i].get("is_compression_enabled") or
                            self.actions[i].get("cache_behavior") or
                            self.actions[i].get("cache_duration")
                        ):
                            return True
                        elif item[field]:
                            if item[field].query_string_caching_behavior != self.actions[i].get("query_string_caching_behavior"):
                                return True
                            elif item[field].query_parameters != self.actions[i].get("query_parameters"):
                                return True
                            elif item[field].is_compression_enabled != self.actions[i].get("is_compression_enabled"):
                                return True
                            elif item[field].cache_behavior != self.actions[i].get("cache_behavior"):
                                return True
                            elif item[field].cache_duration != self.actions[i].get("cache_duration"):
                                return True
        if len(self.response['conditions']) != len(self.conditions):
            return True
        for i, item in enumerate(self.response['conditions']):
            for field in item:
                if field not in ['type_name']:
                    if isinstance(item[field], list) and len(item[field]) == 0 and not self.conditions[i][field]:
                        pass  # Catch the edge case where we have an empty list and a None object
                    elif item[field] is False and not self.conditions[i][field]:
                        pass  # Catch where a default of False matches the None object
                    elif item[field] != self.conditions[i][field]:
                        return True
        return False

    def build_parameters(self, update=False):
        ''' Build the parameters to be used by either Create or Update '''
        conditions = None
        if self.conditions:
            conditions = []
            for condition in self.conditions:
                conditionrule = None
                if condition.get('name') == 'ClientPort':
                    conditionrule = DeliveryRuleClientPortCondition(
                        parameters=ClientPortMatchConditionParameters(
                            type_name='DeliveryRuleClientPortConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'Cookies':
                    conditionrule = DeliveryRuleCookiesCondition(
                        parameters=CookiesMatchConditionParameters(
                            type_name='DeliveryRuleCookiesConditionParameters',
                            selector=condition.get('selector'),
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'HostName':
                    conditionrule = DeliveryRuleHostNameCondition(
                        parameters=HostNameMatchConditionParameters(
                            type_name='DeliveryRuleHostNameConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'HttpVersion':
                    conditionrule = DeliveryRuleHttpVersionCondition(
                        parameters=HttpVersionMatchConditionParameters(
                            type_name='DeliveryRuleHttpVersionConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'IsDevice':
                    conditionrule = DeliveryRuleIsDeviceCondition(
                        parameters=IsDeviceMatchConditionParameters(
                            type_name='DeliveryRuleIsDeviceConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'PostArgs':
                    conditionrule = DeliveryRulePostArgsCondition(
                        parameters=PostArgsMatchConditionParameters(
                            type_name='DeliveryRulePostArgsConditionParameters',
                            selector=condition.get('selector'),
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'QueryString':
                    conditionrule = DeliveryRuleQueryStringCondition(
                        parameters=QueryStringMatchConditionParameters(
                            type_name='DeliveryRuleQueryStringConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'RemoteAddress':
                    conditionrule = DeliveryRuleRemoteAddressCondition(
                        parameters=RemoteAddressMatchConditionParameters(
                            type_name='DeliveryRuleRemoteAddressConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'RequestBody':
                    conditionrule = DeliveryRuleRequestBodyCondition(
                        parameters=RequestBodyMatchConditionParameters(
                            type_name='DeliveryRuleRequestBodyConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'RequestHeader':
                    conditionrule = DeliveryRuleRequestHeaderCondition(
                        parameters=RequestHeaderMatchConditionParameters(
                            type_name='DeliveryRuleRequestHeaderConditionParameters',
                            selector=condition.get('selector'),
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'RequestMethod':
                    conditionrule = DeliveryRuleRequestMethodCondition(
                        parameters=RequestMethodMatchConditionParameters(
                            type_name='DeliveryRuleRequestMethodConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'RequestScheme':
                    conditionrule = DeliveryRuleRequestSchemeCondition(
                        parameters=RequestSchemeMatchConditionParameters(
                            type_name='DeliveryRuleRequestSchemeConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'RequestUri':
                    conditionrule = DeliveryRuleRequestUriCondition(
                        parameters=RequestUriMatchConditionParameters(
                            type_name='DeliveryRuleRequestUriConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'ServerPort':
                    conditionrule = DeliveryRuleServerPortCondition(
                        parameters=ServerPortMatchConditionParameters(
                            type_name='DeliveryRuleServerPortConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'SocketAddr':
                    conditionrule = DeliveryRuleSocketAddrCondition(
                        parameters=SocketAddrMatchConditionParameters(
                            type_name='DeliveryRuleSocketAddrConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'SslProtocol':
                    conditionrule = DeliveryRuleSslProtocolCondition(
                        parameters=SslProtocolMatchConditionParameters(
                            type_name='DeliveryRuleSslProtocolConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'UrlFileExtension':
                    conditionrule = DeliveryRuleUrlFileExtensionCondition(
                        parameters=UrlFileExtensionMatchConditionParameters(
                            type_name='DeliveryRuleUrlFileExtensionMatchConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'UrlFileName':
                    conditionrule = DeliveryRuleUrlFileNameCondition(
                        parameters=UrlFileNameMatchConditionParameters(
                            type_name='DeliveryRuleUrlFilenameConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                elif condition.get('name') == 'UrlPath':
                    conditionrule = DeliveryRuleUrlPathCondition(
                        parameters=UrlPathMatchConditionParameters(
                            type_name='DeliveryRuleUrlPathMatchConditionParameters',
                            operator=condition.get('operator'),
                            negate_condition=condition.get('negate_condition'),
                            match_values=condition.get('match_values'),
                            transforms=condition.get('transforms')
                        )
                    )
                if conditionrule:
                    conditions.append(conditionrule)

        actions = None
        if self.actions:
            actions = []
            for action in self.actions:
                actionrule = None
                if action.get('name') == 'ModifyRequestHeader':
                    actionrule = DeliveryRuleRequestHeaderAction(
                        parameters=HeaderActionParameters(
                            type_name='DeliveryRuleHeaderActionParameters',
                            header_action=action.get('header_action'),
                            header_name=action.get('header_name'),
                            value=action.get('value')
                        )
                    )
                elif action.get('name') == 'ModifyResponseHeader':
                    actionrule = DeliveryRuleResponseHeaderAction(
                        parameters=HeaderActionParameters(
                            type_name='DeliveryRuleHeaderActionParameters',
                            header_action=action.get('header_action'),
                            header_name=action.get('header_name'),
                            value=action.get('value')
                        )
                    )
                elif action.get('name') == 'RouteConfigurationOverride':
                    origin_group_override = None
                    action['origin_group_id'] = None
                    if action.get('origin_group'):
                        origin_group_id = self.get_origin_group_id(action.get('origin_group'))
                        origin_group_ref = ResourceReference(id=origin_group_id)
                        action['origin_group_id'] = origin_group_id
                        origin_group_override = OriginGroupOverride(
                            origin_group=origin_group_ref,
                            forwarding_protocol=ForwardingProtocol(
                                action.get('forwarding_protocol')
                            )
                        )
                    cache_configuration = AzureCoreNull
                    if action.get('query_string_caching_behavior') or action.get('query_parameters') or \
                            action.get('is_compression_enabled') or action.get('cache_behavior') or action.get('cache_duration'):
                        cache_configuration = CacheConfiguration(
                            query_string_caching_behavior=action.get('query_string_caching_behavior'),
                            query_parameters=action.get('query_parameters'),
                            is_compression_enabled=action.get('is_compression_enabled'),
                            cache_behavior=action.get('cache_behavior'),
                            cache_duration=action.get('cache_duration')
                        )
                    actionrule = DeliveryRuleRouteConfigurationOverrideAction(
                        parameters=RouteConfigurationOverrideActionParameters(
                            type_name="DeliveryRuleRouteConfigurationOverrideActionParameters",
                            origin_group_override=origin_group_override,
                            cache_configuration=cache_configuration
                        )
                    )
                elif action.get('name') == 'UrlRedirect':
                    actionrule = UrlRedirectAction(
                        parameters=UrlRedirectActionParameters(
                            type_name='DeliveryRuleUrlRedirectActionParameters',
                            redirect_type=action.get('redirect_type'),
                            destination_protocol=action.get('destination_protocol'),
                            custom_path=action.get('custom_path'),
                            custom_hostname=action.get('custom_hostname'),
                            custom_query_string=action.get('custom_query_string'),
                            custom_fragment=action.get('custom_fragment')
                        )
                    )
                elif action.get('name') == 'UrlRewrite':
                    actionrule = UrlRewriteAction(
                        parameters=UrlRewriteActionParameters(
                            type_name='DeliveryRuleUrlRewriteActionParameters',
                            source_pattern=action.get('source_pattern'),
                            destination=action.get('destination'),
                            preserve_unmatched_path=action.get('preserve_unmatched_path')
                        )
                    )

                if actionrule:
                    actions.append(actionrule)

        if update:
            self.parameters = RuleUpdateParameters(
                order=self.order,
                conditions=conditions,
                actions=actions,
                match_processing_behavior=self.match_processing_behavior
            )
        else:
            self.parameters = Rule(
                order=self.order,
                conditions=conditions,
                actions=actions,
                match_processing_behavior=self.match_processing_behavior
            )
        return

    def delete_rules(self):
        '''
        Deletes the specified Azure Rules in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Rules {0}".format(self.name))
        try:
            poller = self.cdn_client.rules.begin_delete(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                rule_set_name=self.rule_set_name,
                rule_name=self.name)
            self.get_poller_result(poller)
            return True
        except Exception as exc:
            self.log('Error attempting to delete the Rules.')
            self.fail("Error deleting the Rules: {0}".format(str(exc)))
            return False

    def get_rule(self):
        '''
        Gets the properties of the specified Rules.

        :return: deserialized Rules state dictionary
        '''
        self.log(
            "Checking if the Rules {0} is present".format(self.name))
        try:
            response = self.cdn_client.rules.get(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                rule_set_name=self.rule_set_name,
                rule_name=self.name
            )
            self.log("Response : {0}".format(response))
            self.log("Rules : {0} found".format(response.name))
            return rules_to_dict(response)
        except Exception as err:
            self.log('Did not find the Rule: {0}'.format(str(err)))
            return False

    def get_origin_group_id(self, origin_group):
        '''
        Gets the ID of the specified Origin Group.

        :return: ID for the Origin Group.
        '''
        self.log(
            "Obtaining ID for Origin Group {0}".format(origin_group))
        try:
            response = self.cdn_client.afd_origin_groups.get(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                origin_group_name=origin_group)
            self.log("Response : {0}".format(response))
            self.log("Origin Group ID found : {0} found".format(response.id))
            return response.id
        except Exception as err:
            self.fail('Did not find the Origin Group.' + str(err))
            return False


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
                    if subfield != 'additional_properties':
                        new_item[subfield] = subvitem[subfield]
            elif field != 'additional_properties':
                new_item[field] = vitem[field]
        parsed.append(new_item)
    return parsed


def rules_to_dict(rules):
    ''' Convert Rules object to dictionary '''

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


def main():
    """Main execution"""
    AzureRMRules()


if __name__ == '__main__':
    main()
