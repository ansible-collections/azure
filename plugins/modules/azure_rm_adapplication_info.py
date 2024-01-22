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
            - It's application's object ID.
        type: str
    identifier_uri:
        description:
            - It's identifier_uri's object ID.
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
            identifier_uri=dict(type='str')
        )
        self.app_id = None
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

                apps = asyncio.get_event_loop().run_until_complete(self.get_applications(sub_filters))
                applications = list(apps.value)
            self.results['applications'] = [self.to_dict(app) for app in applications]
        except APIError as e:
            if e.response_status_code != 404:
                self.fail("failed to get application info {0}".format(str(e)))
        except Exception as ge:
            self.fail("failed to get application info {0}".format(str(ge)))

        return self.results

    def to_dict(self, object):
        return dict(
            app_id=object.app_id,
            object_id=object.id,
            app_display_name=object.display_name,
            identifier_uris=object.identifier_uris,
            available_to_other_tenants=object.sign_in_audience,
            sign_in_audience=object.sign_in_audience
        )

    async def get_application(self, obj_id):
        return await self._client.applications.by_application_id(obj_id).get()

    async def get_applications(self, sub_filters):
        if sub_filters:
            request_configuration = ApplicationsRequestBuilder.ApplicationsRequestBuilderGetRequestConfiguration(
                query_parameters=ApplicationsRequestBuilder.ApplicationsRequestBuilderGetQueryParameters(
                    filter=(' and '.join(sub_filters)),
                ),
            )
            return await self._client.applications.get(request_configuration=request_configuration)
        else:
            return await self._client.applications.get()


def main():
    AzureRMADApplicationInfo()


if __name__ == '__main__':
    main()
