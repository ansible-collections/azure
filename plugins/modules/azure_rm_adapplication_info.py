#!/usr/bin/python
#
# Copyright (c) 2020 Guopeng Lin, <linguopeng1998@google.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
module: azure_rm_adapplication_info

version_added: "1.6.0"

short_description: Get Azure Active Directory application info

description:
    - Get Azure Active Directory application info.

options:
    app_id:
        description:
            - The application ID.
        type: str
    object_id:
        description:
            - The application's object ID.
        type: str
    identifier_uri:
        description:
            - The identifier_uri's object ID.
        type: str
    app_display_name:
        description:
            - The applications' Name.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    haiyuan_zhang (@haiyuazhang)
    Fred-sun (@Fred-sun)
    guopeng_lin (@guopenglin)
    Xu Zhang (@xuzhang)
'''

EXAMPLES = '''
- name: get ad app info by App ID
  azure_rm_adapplication_info:
    app_id: "{{ app_id }}"

- name: get ad app info ---- by object ID
  azure_rm_adapplication_info:
    object_id: "{{ object_id }}"

- name: get ad app info ---- by identifier uri
  azure_rm_adapplication_info:
    identifier_uri: "{{ identifier_uri }}"

- name: get ad app info ---- by display name
  azure_rm_adapplication_info:
    app_display_name: "{{ display_name }}"
'''

RETURN = '''
applications:
    description:
        - The info of the ad application.
    type: complex
    returned: aways
    contains:
        app_display_name:
            description:
                - Object's display name or its prefix.
            type: str
            returned: always
            sample: app
        app_id:
            description:
                - The application ID.
            returned: always
            type: str
            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        identifier_uris:
            description:
                - The identifiers_uri list of app.
            type: list
            returned: always
            sample: ["http://ansible-atodorov"]
        object_id:
            description:
                - It's application's object ID.
            returned: always
            type: str
            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        sign_in_audience:
            description:
                - The application can be used from any Azure AD tenants
            type: str
            returned: always
            sample: AzureADandPersonalMicrosoftAccount
        available_to_other_tenants:
            description:
                - The application can be used from any Azure AD tenants
            type: str
            returned: always
            sample: AzureADandPersonalMicrosoftAccount
        public_client_reply_urls:
            description:
                - The public client redirect urls.
                - Space-separated URIs to which Azure AD will redirect in response to an OAuth 2.0 request.
            returned: always
            type: list
            sample: []
        web_reply_urls:
            description:
                - The web redirect urls.
                - Space-separated URIs to which Azure AD will redirect in response to an OAuth 2.0 request.
            returned: always
            type: list
            sample: []
        spa_reply_urls:
            description:
                - The spa redirect urls.
                - Space-separated URIs to which Azure AD will redirect in response to an OAuth 2.0 request.
            returned: always
            type: list
            sample: []
        optional_claims:
            description:
                - Declare the optional claims for the application.
            type: complex
            returned: always
            contains:
                access_token_claims :
                    description:
                        - The optional claims returned in the JWT access token
                    type: list
                    returned: always
                    sample: ['name': 'aud', 'source': null, 'essential': false, 'additional_properties': []]
                id_token_claims:
                    description:
                        - The optional claims returned in the JWT ID token
                    type: list
                    returned: always
                    sample: ['name': 'acct', 'source': null, 'essential': false, 'additional_properties': []]
                saml2_token_claims:
                    description:
                        - The optional claims returned in the SAML token
                    type: list
                    returned: always
                    sample: ['name': 'acct', 'source': null, 'essential': false, 'additional_properties': []]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase

try:
    import asyncio
    from msgraph.generated.applications.applications_request_builder import ApplicationsRequestBuilder
    from kiota_abstractions.api_error import APIError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMADApplicationInfo(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            app_id=dict(type='str'),
            object_id=dict(type='str'),
            identifier_uri=dict(type='str'),
            app_display_name=dict(type='str')
        )
        self.app_id = None
        self.app_display_name = None
        self.object_id = None
        self.identifier_uri = None
        self.results = dict(changed=False)
        self._client = None
        super(AzureRMADApplicationInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False,
                                                       is_ad_resource=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        applications = []

        try:
            self._client = self.get_msgraph_client()
            if self.object_id:
                applications = [asyncio.get_event_loop().run_until_complete(self.get_application(self.object_id))]
            else:
                sub_filters = []
                if self.identifier_uri:
                    sub_filters.append("identifierUris/any(s:s eq '{0}')".format(self.identifier_uri))
                if self.app_id:
                    sub_filters.append("appId eq '{0}'".format(self.app_id))
                if self.app_display_name:
                    sub_filters.append("displayName eq '{0}'".format(self.app_display_name))
                apps = asyncio.get_event_loop().run_until_complete(self.get_applications(sub_filters))
                applications = list(apps)
            self.results['applications'] = [self.to_dict(app) for app in applications]
        except APIError as e:
            if e.response_status_code != 404:
                self.fail("failed to get application info {0}".format(str(e)))
        except Exception as ge:
            self.fail("failed to get application info {0}".format(str(ge)))

        return self.results

    def serialize_claims(self, claims):
        if claims is None:
            return None
        return [{
            "additional_properties": claim.additional_properties,
            "essential": claim.essential,
            "name": claim.name,
            "source": claim.source} for claim in claims]

    def to_dict(self, object):
        response = dict(
            app_id=object.app_id,
            object_id=object.id,
            app_display_name=object.display_name,
            identifier_uris=object.identifier_uris,
            available_to_other_tenants=object.sign_in_audience,
            sign_in_audience=object.sign_in_audience,
            web_reply_urls=object.web.redirect_uris,
            spa_reply_urls=object.spa.redirect_uris,
            public_client_reply_urls=object.public_client.redirect_uris,
            optional_claims=dict(access_token=[], id_token=[], saml2_token=[])
        )

        if object.optional_claims is not None:
            response['optional_claims']['id_token'] = self.serialize_claims(object.optional_claims.id_token)
            response['optional_claims']['saml2_token'] = self.serialize_claims(object.optional_claims.saml2_token)
            response['optional_claims']['access_token'] = self.serialize_claims(object.optional_claims.access_token)
        return response

    async def get_application(self, obj_id):
        return await self._client.applications.by_application_id(obj_id).get()

    async def get_applications(self, sub_filters):
        if sub_filters:
            request_configuration = ApplicationsRequestBuilder.ApplicationsRequestBuilderGetRequestConfiguration(
                query_parameters=ApplicationsRequestBuilder.ApplicationsRequestBuilderGetQueryParameters(
                    filter=(' and '.join(sub_filters)),
                ),
            )
            applications = await self._client.applications.get(request_configuration=request_configuration)
            return applications.value
        else:
            applications_list = []
            applications = await self._client.applications.get()
            for app in applications.value:
                applications_list.append(app)

            if applications.odata_next_link:
                next_link = applications.odata_next_link
            else:
                next_link = None

            while next_link:
                applications = await self._client.applications.with_url(next_link).get()
                next_link = applications.odata_next_link
                for app in applications.value:
                    applications_list.append(app)
            return applications_list


def main():
    AzureRMADApplicationInfo()


if __name__ == '__main__':
    main()
