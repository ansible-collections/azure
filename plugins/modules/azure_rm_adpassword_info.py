#!/usr/bin/python
#
# Copyright (c) 2020 Haiyuan Zhang, <haiyzhan@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
module: azure_rm_adpassword_info

version_added: "0.2.0"

short_description: Get application password info

description:
        - Get application password info.

options:
    app_id:
        description:
            - The application ID.
        type: str
    service_principal_object_id:
        description:
            - The service principal object ID.
        type: str
    key_id:
        description:
            - The password key ID.
        type: str
    end_date:
        description:
            - Date or datemtime after which credentials expire.
            - Default value is one year after current time.
        type: str
    value:
        description:
            - The application password value.
            - Length greater than 18 characters.
        type: str
    app_object_id:
        description:
            - The application object ID.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    haiyuan_zhang (@haiyuazhang)
    Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: get ad password info
  azure_rm_adpassword_info:
    app_id: "{{ app_id }}"
    key_id: "{{ key_id }}"
'''

RETURN = '''
passwords:
    description:
        - The password info.
    returned: success
    type: dict
    contains:
        custom_key_identifier:
            description:
                - Custom key identifier.
            type: str
            returned: always
            sample: None
        end_date:
            description:
                - Date or datemtime after which credentials expire.
                - Default value is one year after current time.
            type: str
            returned: always
            sample: "2021-06-18T06:51:25.508304+00:00"
        key_id:
            description:
                - The password key ID.
            type: str
            returned: always
            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        start_date:
            description:
                - Date or datetime at which credentials become valid.
                - Default value is current time
            type: str
            returned: always
            sample: "2020-06-18T06:51:25.508304+00:00"

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    import asyncio
    from msgraph.generated.applications.applications_request_builder import ApplicationsRequestBuilder
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMADPasswordInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            app_id=dict(type='str'),
            app_object_id=dict(type='str'),
            service_principal_object_id=dict(type='str'),
            key_id=dict(type='str'),
            value=dict(type='str'),
            end_date=dict(type='str'),
        )

        self.app_id = None
        self.service_principal_object_id = None
        self.app_object_id = None
        self.key_id = None
        self.value = None
        self.end_date = None
        self.results = dict(changed=False)

        self.client = None

        super(AzureRMADPasswordInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_tags=False,
                                                    supports_check_mode=True,
                                                    is_ad_resource=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self._client = self.get_msgraph_client()
        self.resolve_app_obj_id()
        passwords = self.get_all_passwords()

        if self.key_id:
            filtered = [pd for pd in passwords if str(pd.key_id) == self.key_id]
            self.results['passwords'] = [self.to_dict(pd) for pd in filtered]
        else:
            self.results['passwords'] = [self.to_dict(pd) for pd in passwords]

        return self.results

    def resolve_app_obj_id(self):
        try:
            if self.app_object_id is not None:
                return
            elif self.app_id or self.service_principal_object_id:
                if not self.app_id:
                    sp = asyncio.get_event_loop().run_until_complete(self.get_service_principal())
                    self.app_id = sp.app_id
                if not self.app_id:
                    self.fail("can't resolve app via service principal object id {0}".format(
                        self.service_principal_object_id))

                apps = asyncio.get_event_loop().run_until_complete(self.get_applications())
                result = list(apps.value)
                if result:
                    self.app_object_id = result[0].id
                else:
                    self.fail("can't resolve app via app id {0}".format(self.app_id))
            else:
                self.fail("one of the [app_id, app_object_id, service_principal_object_id] must be set")

        except Exception as ge:
            self.fail("error in resolve app_object_id {0}".format(str(ge)))

    def get_all_passwords(self):

        try:
            application = asyncio.get_event_loop().run_until_complete(self.get_application())
            passwordCredentials = application.password_credentials
            return passwordCredentials
        except Exception as ge:
            self.fail("failed to fetch passwords for app {0}: {1}".format(self.app_object_id, str(ge)))

    def to_dict(self, pd):
        return dict(
            end_date=pd.end_date_time,
            start_date=pd.start_date_time,
            key_id=str(pd.key_id),
            custom_key_identifier=str(pd.custom_key_identifier)
        )

    async def get_service_principal(self):
        return await self._client.service_principals.by_service_principal_id(self.service_principal_object_id).get()

    async def get_applications(self):
        request_configuration = ApplicationsRequestBuilder.ApplicationsRequestBuilderGetRequestConfiguration(
            query_parameters=ApplicationsRequestBuilder.ApplicationsRequestBuilderGetQueryParameters(
                filter="appId eq '{0}'".format(self.app_id),
            ),
        )
        return await self._client.applications.get(request_configuration=request_configuration)

    async def get_application(self):
        return await self._client.applications.by_application_id(self.app_object_id).get()


def main():
    AzureRMADPasswordInfo()


if __name__ == '__main__':
    main()
