#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Python SDK Reference: https://learn.microsoft.com/en-us/python/api/azure-mgmt-cdn/azure.mgmt.cdn.operations.routesoperations?view=azure-python
#
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_afdroute
version_added: "3.4.0"
short_description: Manage an Azure Front Door Route
description:
    - Create, update and delete an Azure Front Door Route to be used by a Front Door Service Profile created using azure_rm_cdnprofile.

options:
    content_types_to_compress:
        description:
            - The caching configuration/compression settings for this route.
            - List of content types (str) on which compression applies. The value should be a valid MIME type.
            - Required together (is_compression_enabled, content_types_to_compress, query_string_caching_behavior, query_parameters)
        type: list
        elements: str
    custom_domains:
        description:
            - Domain names referenced by this endpoint. ID will be looked up based on the name.
        type: list
        elements: str
    disable_cache_configuration:
        description:
            - To disable cache configuration, set this to true and do not include cache_configuration.
            - This will override any cache_configuration settings you include.
        type: bool
        default: false
    enabled_state:
        description:
            - Whether to enable use of this rule. Permitted values are 'Enabled' or 'Disabled'.
        type: str
        choices:
            - Enabled
            - Disabled
    endpoint_name:
        description:
            - Name of the endpoint under the profile which is unique globally.
        required: true
        type: str
    forwarding_protocol:
        description:
            - Protocol this rule will use when forwarding traffic to backends.
        type: str
        choices:
            - HttpOnly
            - HttpsOnly
            - MatchRequest
    https_redirect:
        description:
            - Whether to automatically redirect HTTP traffic to HTTPS traffic.
        type: str
        default: Disabled
        choices:
            - Enabled
            - Disabled
    is_compression_enabled:
        description:
            - The caching configuration/compression settings for this route.
            - Indicates whether content compression is enabled on AzureFrontDoor.
            - If compression is enabled, content will be served as compressed if user requests for a compressed version.
            - Content won't be compressed on AzureFrontDoor when requested content is smaller than 1 byte or larger than 1 MB.
            - Required together (is_compression_enabled, content_types_to_compress, query_string_caching_behavior, query_parameters)
        type: bool
    link_to_default_domain:
        description:
            - whether this route will be linked to the default endpoint domain.
        type: str
        default: Disabled
        choices:
            - Enabled
            - Disabled
    name:
        description:
            - Name of the routing rule.
        required: true
        type: str
    origin_group:
        description:
            - A reference to the origin group.
        type: str
    origin_path:
        description:
            - A directory path on the origin that AzureFrontDoor can use to retrieve content from, e.g. contoso.cloudapp.net/originpath.
        type: str
    patterns_to_match:
        description:
            - The route patterns of the rule.
        type: list
        elements: str
    profile_name:
        description:
            - Name of the Azure Front Door Standard or Azure Front Door Premium profile which is unique within the resource group.
        required: true
        type: str
    query_parameters:
        description:
            - The caching configuration for this route.
            - query parameters to include or exclude (comma separated).
            - Required together (is_compression_enabled, content_types_to_compress, query_string_caching_behavior, query_parameters)
        type: str
    query_string_caching_behavior:
        description:
            - The caching configuration for this route.
            - Defines how Frontdoor caches requests that include query strings.
            - You can ignore any query strings when caching, ignore specific query strings,
            - cache every request with a unique URL, or cache specific query strings.
            - Required together (is_compression_enabled, content_types_to_compress, query_string_caching_behavior, query_parameters)
        type: str
        choices:
            - IgnoreQueryString
            - IgnoreSpecifiedQueryStrings
            - IncludeSpecifiedQueryStrings
            - UseQueryString
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: true
        type: str
    rule_sets:
        description:
            - List of rule set names referenced by this endpoint.
        type: list
        elements: str
    state:
        description:
            - Assert the state of the Route. Use C(present) to create or update a CDN profile and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present
    supported_protocols:
        description:
            - List of supported protocols for this route.
        type: list
        elements: str
        default: ['Http', 'Https']
        choices:
            - Http
            - Https

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Jarret Tooley (@jartoo)
'''

EXAMPLES = '''
- name: Create an AFD Route
  azure_rm_afdroute:
    name: myRoute
    endpoint_name: myEndpoint
    origin_group: myOriginGroup
    profile_name: myProfile
    resource_group_name: myResourceGroup
    state: present
    route:
      enabled_state: Disabled
      forwarding_protocol: HttpsOnly
      https_redirect: Enabled
      patterns_to_match:
        - "/*"
      rule_sets:
        - Security
      supported_protocols:
        - Https
        - Http
      link_to_default_domain: Enabled

- name: Delete an AFD Origin
  azure_rm_afdroute:
    name: myRoute
    endpoint_name: myEndpoint
    origin_group: myOriginGroup
    profile_name: myProfile
    resource_group_name: myResourceGroup
    state: absent
'''
RETURN = '''
id:
    description:
        - ID of the Route.
    returned: always
    type: str
    sample: "id: '/subscriptions/xxxxxx-xxxx-xxxx-xxxx-xxxxxxxx/resourcegroups/myRG/providers/Microsoft.Cdn/profiles/myProf/afdendpoints/myEP/routes/myRoute'"
'''
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
# from azure.core.serialization import NULL as AzureCoreNull

try:
    from azure.mgmt.cdn.models import Route, RouteUpdateParameters, CompressionSettings, \
        ResourceReference, AfdRouteCacheConfiguration
except ImportError as ec:
    # This is handled in azure_rm_common
    pass


class AzureRMRoute(AzureRMModuleBase):
    ''' Main Class '''
    def __init__(self):
        self.module_arg_spec = dict(
            content_types_to_compress=dict(
                type='list',
                elements='str'
            ),
            custom_domains=dict(
                type='list',
                elements='str'
            ),
            disable_cache_configuration=dict(
                type='bool',
                default=False
            ),
            enabled_state=dict(
                type='str',
                choices=['Enabled', 'Disabled']
            ),
            endpoint_name=dict(
                type='str',
                required=True
            ),
            forwarding_protocol=dict(
                type='str',
                choices=['HttpOnly', 'HttpsOnly', 'MatchRequest']
            ),
            https_redirect=dict(
                type='str',
                choices=['Enabled', 'Disabled'],
                default='Disabled'
            ),
            is_compression_enabled=dict(
                type='bool'
            ),
            link_to_default_domain=dict(
                type='str',
                choices=['Enabled', 'Disabled'],
                default='Disabled'
            ),
            name=dict(
                type='str',
                required=True
            ),
            origin_group=dict(
                type='str'
            ),
            origin_path=dict(
                type='str'
            ),
            patterns_to_match=dict(
                type='list',
                elements='str'
            ),
            profile_name=dict(
                type='str',
                required=True
            ),
            query_string_caching_behavior=dict(
                type='str',
                choices=['IgnoreQueryString', 'IgnoreSpecifiedQueryStrings', 'IncludeSpecifiedQueryStrings', 'UseQueryString']
            ),
            query_parameters=dict(
                type='str'
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            rule_sets=dict(
                type='list',
                elements='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            supported_protocols=dict(
                type='list',
                elements='str',
                choices=['Http', 'Https'],
                default=['Http', 'Https']
            )
        )

        self.content_types_to_compress = None
        self.custom_domains = None
        self.disable_cache_configuration = None
        self.enabled_state = None
        self.forwarding_protocol = None
        self.https_redirect = None
        self.is_compression_enabled = None
        self.link_to_default_domain = None
        self.origin_path = None
        self.origin_group = None
        self.patterns_to_match = None
        self.query_parameters = None
        self.query_string_caching_behavior = None
        self.rule_sets = []
        self.supported_protocols = None

        self.origin_group_id = None

        self.name = None
        self.endpoint_name = None
        self.profile_name = None
        self.resource_group = None
        self.state = None

        self.rule_set_ids = []
        self.custom_domain_ids = []

        required_together = [['is_compression_enabled', 'content_types_to_compress', 'query_string_caching_behavior', 'query_parameters']]

        self.results = dict(changed=False)

        super(AzureRMRoute, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            required_together=required_together
        )

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        to_be_updated = False

        # Ignore query_parameters when query_string_caching_behavior is "IgnoreQueryString" or "UseQueryString"
        if self.query_string_caching_behavior in ["IgnoreQueryString", "UseQueryString"]:
            self.query_parameters = None
            self.log("Ignoring query_parameters when query_string_caching_behavior is IgnoreQueryString or UseQueryString")

        # Get the existing resource
        response = self.get_route()

        if self.state == 'present':
            # Get the Origin Group ID
            self.origin_group_id = self.get_origin_group_id()
            if self.origin_group_id is False:
                self.fail("Could not obtain Origin Group ID from {0}, please create it first.".format(self.origin_group))

            # Get a list of all the Custom Domain IDs
            if isinstance(self.custom_domains, list):
                if len(self.custom_domains) > 0:
                    for custom_domain in self.custom_domains:
                        cd_id = self.get_custom_domain_id(custom_domain)
                        if cd_id:
                            ref = ResourceReference(
                                id=cd_id)
                            self.custom_domain_ids.append(ref)

            # Populate the rule_set_ids
            convert_rules = self.get_rule_set_ids()
            if not convert_rules:
                self.fail("Failed to convert the Rule Set names to IDs")

            if not response:
                self.log("Need to create the Route")

                if not self.check_mode:
                    new_results = self.create_route()
                    self.results['id'] = new_results['id']
                self.results['changed'] = True

            else:
                self.log('Results : {0}'.format(response))

                to_be_updated = self.update_needed(response)

                self.results['id'] = response['id']
                if to_be_updated:
                    self.log("Need to update the Route")

                    if not self.check_mode:
                        new_results = self.update_route()
                        self.results['id'] = new_results['id']

                    self.results['changed'] = True

        elif self.state == 'absent':
            if not response:
                self.log("Route {0} does not exist.".format(self.name))
                self.results['id'] = None
                self.results['changed'] = False
            else:
                self.log("Need to delete the Route")
                self.results['changed'] = True

                if not self.check_mode:
                    self.delete_route()
                    self.results['id'] = response['id']
        return self.results

    def update_needed(self, response):
        '''
        Check if the resource needs to be updated

        return: bool
        '''
        to_be_updated = False
        cache_configuration = response['cache_configuration']
        if cache_configuration and self.disable_cache_configuration:
            to_be_updated = True
        if cache_configuration:
            if cache_configuration.query_parameters != self.query_parameters and self.query_parameters:
                to_be_updated = True
            if cache_configuration.query_string_caching_behavior != self.query_string_caching_behavior and self.query_string_caching_behavior:
                to_be_updated = True
            if cache_configuration.compression_settings.is_compression_enabled != self.is_compression_enabled and self.is_compression_enabled:
                to_be_updated = True
            if cache_configuration.compression_settings.content_types_to_compress != self.content_types_to_compress and self.content_types_to_compress:
                to_be_updated = True
        else:
            if self.is_compression_enabled or self.query_parameters or self.query_string_caching_behavior or self.content_types_to_compress:
                to_be_updated = True
        # Test for custom_domain equality
        equal = True
        if len(response['custom_domains']) != len(self.custom_domain_ids):
            equal = False
        for x in response['custom_domains']:
            found = False
            for y in self.custom_domain_ids:
                if x.id == y.id:
                    found = True
                    continue
            if not found:
                equal = False
        if not equal:
            to_be_updated = True

        if response['enabled_state'] != self.enabled_state and self.enabled_state:
            to_be_updated = True
        if response['forwarding_protocol'] != self.forwarding_protocol and self.forwarding_protocol:
            to_be_updated = True
        if response['https_redirect'] != self.https_redirect and self.https_redirect:
            to_be_updated = True
        if response['link_to_default_domain'] != self.link_to_default_domain and self.link_to_default_domain:
            to_be_updated = True
        if response['origin_group_id'] != self.origin_group_id and self.origin_group_id:
            to_be_updated = True
        if response['origin_path'] != self.origin_path and self.origin_path:
            to_be_updated = True
        if response['patterns_to_match'] != self.patterns_to_match and self.patterns_to_match:
            to_be_updated = True
        if response["rule_sets"] != self.rule_set_ids and self.rule_set_ids:
            to_be_updated = True
        if response['supported_protocols'] != self.supported_protocols and self.supported_protocols:
            to_be_updated = True

        return to_be_updated

    def create_route(self):
        '''
        Creates a Azure Route.

        :return: deserialized Azure Route instance state dictionary
        '''
        self.log("Creating the Azure Route instance {0}".format(self.name))
        cache_configuration = None
        compression_settings = None

        if self.disable_cache_configuration:
            # cache_configuration = AzureCoreNull # Reported as issue to azure-mgmt-cdn: https://github.com/Azure/azure-sdk-for-python/issues/35801
            cache_configuration = None
        else:
            if not self.is_compression_enabled and not self.content_types_to_compress:
                compression_settings = None
            else:
                compression_settings = CompressionSettings(
                    content_types_to_compress=self.content_types_to_compress,
                    is_compression_enabled=self.is_compression_enabled
                )
            if not self.query_string_caching_behavior and not self.query_parameters and not compression_settings:
                cache_configuration = None
            else:
                cache_configuration = AfdRouteCacheConfiguration(
                    query_string_caching_behavior=self.query_string_caching_behavior,
                    query_parameters=self.query_parameters,
                    compression_settings=compression_settings
                )

        origin_group = ResourceReference(
            id=self.origin_group_id
        )

        parameters = Route(
            cache_configuration=cache_configuration,
            custom_domains=self.custom_domain_ids,
            enabled_state=self.enabled_state,
            forwarding_protocol=self.forwarding_protocol,
            https_redirect=self.https_redirect,
            link_to_default_domain=self.link_to_default_domain,
            origin_group=origin_group,
            origin_path=self.origin_path,
            patterns_to_match=self.patterns_to_match,
            rule_sets=self.rule_set_ids,
            supported_protocols=self.supported_protocols
        )

        try:
            poller = self.cdn_client.routes.begin_create(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                endpoint_name=self.endpoint_name,
                route_name=self.name,
                route=parameters
            )
            response = self.get_poller_result(poller)
            return route_to_dict(response)
        except Exception as exc:
            self.log('Error attempting to create Azure Route instance.')
            self.fail("Error Creating Azure Route instance: {0}".format(str(exc)))

    def update_route(self):
        '''
        Updates an Azure Route.

        :return: deserialized Azure Route instance state dictionary
        '''
        self.log("Updating the Azure Route instance {0}".format(self.name))

        cache_configuration = None
        compression_settings = None

        if self.disable_cache_configuration:
            # cache_configuration = AzureCoreNull # Reported as issue to azure-mgmt-cdn: https://github.com/Azure/azure-sdk-for-python/issues/35801
            cache_configuration = None
        else:
            if not self.is_compression_enabled and not self.content_types_to_compress:
                compression_settings = None
            else:
                compression_settings = CompressionSettings(
                    content_types_to_compress=self.content_types_to_compress,
                    is_compression_enabled=self.is_compression_enabled
                )
            if not self.query_string_caching_behavior and not self.query_parameters and not compression_settings:
                cache_configuration = None
            else:
                cache_configuration = AfdRouteCacheConfiguration(
                    query_string_caching_behavior=self.query_string_caching_behavior,
                    query_parameters=self.query_parameters,
                    compression_settings=compression_settings
                )

        origin_group = ResourceReference(
            id=self.origin_group_id
        )

        parameters = RouteUpdateParameters(
            cache_configuration=cache_configuration,
            custom_domains=self.custom_domain_ids,
            enabled_state=self.enabled_state,
            forwarding_protocol=self.forwarding_protocol,
            https_redirect=self.https_redirect,
            link_to_default_domain=self.link_to_default_domain,
            origin_group=origin_group,
            origin_path=self.origin_path,
            patterns_to_match=self.patterns_to_match,
            rule_sets=self.rule_set_ids,
            supported_protocols=self.supported_protocols
        )

        try:
            poller = self.cdn_client.routes.begin_update(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                endpoint_name=self.endpoint_name,
                route_name=self.name,
                route_update_properties=parameters
            )
            response = self.get_poller_result(poller)
            return route_to_dict(response)
        except Exception as exc:
            self.log('Error attempting to update Azure Route instance.')
            self.fail("Error updating Azure Route instance: {0}".format(str(exc)))

    def delete_route(self):
        '''
        Deletes the specified Azure Route in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Route {0}".format(self.name))
        try:
            poller = self.cdn_client.routes.begin_delete(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                endpoint_name=self.endpoint_name,
                route_name=self.name
            )
            self.get_poller_result(poller)
            return True
        except Exception as exc:
            self.log('Error attempting to delete the Route.')
            self.fail("Error deleting the Route: {0}".format(str(exc)))
            return False

    def get_route(self):
        '''
        Gets the properties of the specified Route.

        :return: deserialized Route state dictionary
        '''
        self.log(
            "Checking if the Route {0} is present".format(self.name))
        try:
            response = self.cdn_client.routes.get(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                endpoint_name=self.endpoint_name,
                route_name=self.name,
            )
            self.log("Response : {0}".format(response))
            self.log("Route : {0} found".format(response.name))
            return route_to_dict(response)
        except Exception as err:
            self.log('Did not find the Route.' + err.args[0])
            return False

    def get_origin_group_id(self):
        '''
        Gets the ID of the specified Origin Group.

        :return: ID for the Origin Group.
        '''
        self.log(
            "Obtaining ID for Origin Group {0}".format(self.origin_group))
        try:
            response = self.cdn_client.afd_origin_groups.get(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                origin_group_name=self.origin_group
            )
            self.log("Response : {0}".format(response))
            self.log("Origin Group ID found : {0} found".format(response.id))
            return response.id
        except Exception as err:
            self.log('Did not find the Origin Group.' + err.args[0])
            return False

    def get_custom_domain_id(self, custom_domain):
        '''
        Gets the ID of the specified Custom Domain.

        :return: ID for the Custom Domain.
        '''
        self.log("Obtaining ID for Custom Domain {0}".format(self.origin_group))
        try:
            response = self.cdn_client.afd_custom_domains.get(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                custom_domain_name=custom_domain
            )
            self.log("Response : {0}".format(response))
            self.log("Custom Domain found : {0} found".format(response.id))
            return response.id
        except Exception as err:
            self.log('Did not find the Custom Domain.' + err.args[0])
            return False

    def get_rule_set_ids(self):
        '''
        Gets the IDs of the specified Rule Sets.

        :return: Boolean if Rule Sets were found and translated.
        '''
        if self.rule_sets is None or len(self.rule_sets) == 0:
            return True

        self.log("Obtaining IDs for Rule Sets")

        try:
            for rule_name in self.rule_sets:
                response = self.cdn_client.rule_sets.get(
                    resource_group_name=self.resource_group,
                    profile_name=self.profile_name,
                    rule_set_name=rule_name,
                )
                self.log("Response : {0}".format(response))
                self.log("Rule Set ID found : {0} found".format(response.id))
                self.rule_set_ids.append(ResourceReference(id=response.id))
            return True
        except Exception as err:
            self.log('Error getting the Rule Set IDs.' + err.args[0])
            return False


def route_to_dict(route):
    '''
        Convert the object to dictionary
    '''
    return dict(
        custom_domains=route.custom_domains,
        cache_configuration=route.cache_configuration,
        deployment_status=route.deployment_status,
        enabled_state=route.enabled_state,
        forwarding_protocol=route.forwarding_protocol,
        https_redirect=route.https_redirect,
        id=route.id,
        link_to_default_domain=route.link_to_default_domain,
        name=route.name,
        origin_group_id=route.origin_group.id,
        origin_path=route.origin_path,
        patterns_to_match=route.patterns_to_match,
        provisioning_state=route.provisioning_state,
        rule_sets=route.rule_sets,
        supported_protocols=route.supported_protocols,
        type=route.type
    )


def main():
    """Main execution"""
    AzureRMRoute()
    # x = CdnManagementClient()
    # x.routes.begin_update()


if __name__ == '__main__':
    main()
