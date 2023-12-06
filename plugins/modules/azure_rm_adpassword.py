#!/usr/bin/python
#
# Copyright (c) 2020 Haiyuan Zhang, <haiyzhan@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_adpassword

version_added: "0.2.0"

short_description: Manage application password

description:
    - Manage application password.

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
            - It isn't supported anymore in the create operation. See the Azure documentation for more information
              U(https://learn.microsoft.com/en-us/graph/api/application-addpassword?view=graph-rest-1.0&tabs=http#request-body).
        type: str
    end_date:
        description:
            - Date or datemtime after which credentials expire.
            - Default value is one year after current time.
        type: str
    display_name:
        description:
            - The friendly name of the application password.
        type: str
    app_object_id:
        description:
            - The application object ID.
        type: str
    state:
        description:
            - Assert the state of Active Dirctory Password.
            - Use C(present) to create or update a Password and use C(absent) to delete.
            - Update is not supported, if I(state=absent) and I(key_id=None), then all passwords of the application will be deleted.
        default: present
        choices:
            - absent
            - present
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    haiyuan_zhang (@haiyuazhang)
    Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: create ad password
  azure_rm_adpassword:
    app_id: "{{ app_id }}"
    state: present
    display_name: "Password friendly name"
'''

RETURN = '''
end_date:
    description:
        - Date or datemtime after which credentials expire.
        - Default value is one year after current time.
    type: str
    returned: always
    sample: "2021-06-28T06:00:32.637070+00:00"
key_id:
    description:
        - The password key ID
    type: str
    returned: always
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
start_date:
    description:
        - Date or datetime at which credentials become valid.
        - Default value is current time.
    type: str
    returned: always
    sample: "2020-06-28T06:00:32.637070+00:00"
secret_text:
    description:
        - The application password value.
        - API only returns the application password value at creation.
    type: str
    returned: created
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
import datetime

try:
    import asyncio
    from msgraph.generated.models.password_credential import PasswordCredential
    from msgraph.generated.applications.item.add_password.add_password_post_request_body import \
        AddPasswordPostRequestBody
    from msgraph.generated.applications.item.remove_password.remove_password_post_request_body import \
        RemovePasswordPostRequestBody
    from msgraph.generated.applications.applications_request_builder import ApplicationsRequestBuilder
    from dateutil.relativedelta import relativedelta
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMADPassword(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            app_id=dict(type='str'),
            service_principal_object_id=dict(type='str'),
            app_object_id=dict(type='str'),
            key_id=dict(type='str'),
            display_name=dict(type='str'),
            end_date=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.state = None
        self.app_id = None
        self.service_principal_object_id = None
        self.app_object_id = None
        self.key_id = None
        self.display_name = None
        self.end_date = None
        self.results = dict(changed=False)

        self.client = None

        super(AzureRMADPassword, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=False,
                                                supports_tags=False,
                                                is_ad_resource=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self._client = self.get_msgraph_client()
        self.resolve_app_obj_id()
        passwords = self.get_all_passwords()

        if self.state == 'present':
            if self.key_id and self.key_exists(passwords):
                self.update_password(passwords)
            else:
                self.create_password(passwords)
        else:
            if self.key_id is None:
                self.delete_all_passwords(passwords)
            else:
                self.delete_password(passwords)

        return self.results

    def key_exists(self, old_passwords):
        for pd in old_passwords:
            if str(pd.key_id) == self.key_id:
                return True
        return False

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
                self.fail("one of the [app_id, app_object_id, service_principal_id] must be set")

        except Exception as ge:
            self.fail("error in resolve app_object_id {0}".format(str(ge)))

    def get_all_passwords(self):

        try:
            application = asyncio.get_event_loop().run_until_complete(self.get_application())
            passwordCredentials = application.password_credentials
            return passwordCredentials
        except Exception as ge:
            self.fail("failed to fetch passwords for app {0}: {1}".format(self.app_object_id, str(ge)))

    def delete_all_passwords(self, old_passwords):

        if len(old_passwords) == 0:
            self.results['changed'] = False
            return
        try:
            for pd in old_passwords:
                asyncio.get_event_loop().run_until_complete(self.remove_password(pd.key_id))
            self.results['changed'] = True
        except Exception as ge:
            self.fail("fail to purge all passwords for app: {0} - {1}".format(self.app_object_id, str(ge)))

    def delete_password(self, old_passwords):
        if not self.key_exists(old_passwords):
            self.results['changed'] = False
            return

        num_of_passwords_before_delete = len(old_passwords)

        for pd in old_passwords:
            if str(pd.key_id) == self.key_id:
                try:
                    asyncio.get_event_loop().run_until_complete(self.remove_password(pd.key_id))

                    num_of_passwords_after_delete = len(self.get_all_passwords())
                    if num_of_passwords_after_delete != num_of_passwords_before_delete:
                        self.results['changed'] = True
                except Exception as ge:
                    self.fail("failed to delete password with key id {0} - {1}".format(self.app_id, str(ge)))
                break

    def create_password(self, old_passwords):
        start_date = datetime.datetime.now(datetime.timezone.utc)
        end_date = self.end_date or start_date + relativedelta(years=1)
        display_name = self.display_name
        num_of_passwords_before_add = len(old_passwords)

        try:
            request_body = AddPasswordPostRequestBody(
                password_credential=PasswordCredential(
                    start_date_time=start_date,
                    end_date_time=end_date,
                    display_name=display_name
                ),
            )
            pd = asyncio.get_event_loop().run_until_complete(self.add_password(request_body))

            num_of_passwords_after_add = len(self.get_all_passwords())
            if num_of_passwords_after_add != num_of_passwords_before_add:
                self.results['changed'] = True
                self.results.update(self.to_dict(pd))
        except Exception as ge:
            self.fail("failed to create new password: {0}".format(str(ge)))

    def update_password(self, old_passwords):
        self.fail("update existing password is not supported")

    def to_dict(self, pd):
        return dict(
            end_date=str(pd.end_date_time),
            start_date=str(pd.start_date_time),
            key_id=str(pd.key_id),
            secret_text=str(pd.secret_text)
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

    async def remove_password(self, key_id):
        request_body = RemovePasswordPostRequestBody(
            key_id=key_id,
        )
        return await self._client.applications.by_application_id(self.app_object_id).remove_password.post(
            body=request_body)

    async def add_password(self, request_body):
        return await self._client.applications.by_application_id(self.app_object_id).add_password.post(
            body=request_body)


def main():
    AzureRMADPassword()


if __name__ == '__main__':
    main()
