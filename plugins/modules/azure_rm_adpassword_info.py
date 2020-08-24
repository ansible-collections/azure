#!/usr/bin/python
#
# Copyright (c) 2020 Haiyuan Zhang, <haiyzhan@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import datetime

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

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
    tenant:
        description:
            - The tenant ID.
        type: str
        required: True
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
    - azure.azcollection.azure_tags

author:
    haiyuan_zhang (@haiyuazhang)
    Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
  - name: get ad password info
    azure_rm_adpassword_info:
      app_id: "{{ app_id }}"
      tenant: "{{ tenant_id }}"
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
            type: datetime
            returned: always
            sample: 2021-06-18T06:51:25.508304+00:00
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
            type: datetime
            returned: always
            sample: 2020-06-18T06:51:25.508304+00:00

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.graphrbac.models import GraphErrorException
    from azure.graphrbac.models import PasswordCredential
    from azure.graphrbac.models import ApplicationUpdateParameters
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
            tenant=dict(type='str', required=True),
            value=dict(type='str'),
            end_date=dict(type='str'),
        )

        self.tenant = None
        self.app_id = None
        self.service_principal_object_id = None
        self.app_object_id = None
        self.key_id = None
        self.value = None
        self.end_date = None
        self.results = dict(changed=False)

        self.client = None

        super(AzureRMADPasswordInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=False,
                                                    supports_tags=False,
                                                    is_ad_resource=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self.client = self.get_graphrbac_client(self.tenant)
        self.resolve_app_obj_id()
        passwords = self.get_all_passwords()

        if self.key_id:
            filtered = [pd for pd in passwords if pd.key_id == self.key_id]
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
                    sp = self.client.service_principals.get(self.service_principal_id)
                    self.app_id = sp.app_id
                if not self.app_id:
                    self.fail("can't resolve app via service principal object id {0}".format(self.service_principal_object_id))

                result = list(self.client.applications.list(filter="appId eq '{0}'".format(self.app_id)))
                if result:
                    self.app_object_id = result[0].object_id
                else:
                    self.fail("can't resolve app via app id {0}".format(self.app_id))
            else:
                self.fail("one of the [app_id, app_object_id, service_principal_id] must be set")

        except GraphErrorException as ge:
            self.fail("error in resolve app_object_id {0}".format(str(ge)))

    def get_all_passwords(self):

        try:
            return list(self.client.applications.list_password_credentials(self.app_object_id))
        except GraphErrorException as ge:
            self.fail("failed to fetch passwords for app {0}: {1}".format(self.app_object_id, str(ge)))

    def to_dict(self, pd):
        return dict(
            end_date=pd.end_date,
            start_date=pd.start_date,
            key_id=pd.key_id,
            custom_key_identifier=str(pd.custom_key_identifier)
        )


def main():
    AzureRMADPasswordInfo()


if __name__ == '__main__':
    main()
