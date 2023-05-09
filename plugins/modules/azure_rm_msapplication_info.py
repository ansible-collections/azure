#!/usr/bin/python
#
# Copyright (c) 2023 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
module: azure_rm_msapplication_info

version_added: "1.16.0"

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
            - The service principal's object ID.
        type: str
    all:
        description:
            - If True, will return all applicatins in tenant.
            - Mutually exclusive with I(object_id) and I(app_id).
        type: bool

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
  - name: get MS sp info by object_id
    azure_rm_msapplication_info:
      object_id: "{{ object_id }}"

  - name: get all MS application info
    azure_rm_msapplication_info:
        all: True

  - name: get Microsoft Graph application info by App ID
    azure_rm_msapplication_info:
      app_id: "{{ app_id }}"

'''

RETURN = '''
app_display_name:
    description:
        - Object's display name or its prefix.
    type: str
    returned: always
    sample: sp
app_id:
    description:
        - The application ID.
    returned: always
    type: str
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
app_roles:
    description:
        - The collection of application roles that an application may declare.
        - These roles can be assigned to users, groups or service principals.
    type: list
    returned: always
    sample: []
object_id:
    description:
        - The application's object ID.
    returned: always
    type: str
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
spa:
    description:
        - The single page application(SPA) URI of redirects.
    returned: always
    type: dict
    sample: {'redirect_uris':['https://spa.com']}
web:
    description:
        - The Web URI of redirects.
    returned: always
    type: dict
    sample: {'redirect_uris':['https://web.com']}
public_client:
    description:
        - The public client/native URI of redirects.
    returned: always
    type: dict
    sample: {'redirect_uris':['https://localhost']}
sign_in_audience:
    description:
        - The application account type.
    type: str
    returned: always
    sample: PersonalMicrosoftAccount
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase


class AzureRMMSApplicationInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            app_id=dict(type='str'),
            object_id=dict(type='str'),
            all=dict(type='bool'),
        )

        self.app_id = None
        self.object_id = None
        self.all = None
        self.results = dict(changed=False)

        mutually_exclusive = [['all', 'app_id', 'object_id']]

        super(AzureRMMSApplicationInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False,
                                                       mutually_exclusive=mutually_exclusive,
                                                       )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        service_principals = []

        try:
            client = self.get_msgraph_client()
            if self.object_id is not None:
                service_principals = [client.get('/applications/' + self.object_id).json()]
            elif self.app_id is not None:
                response = client.get('/applications/').json()['value']
                for item in response:
                    if item['appId'] == self.app_id:
                        service_principals.append(item)
            elif self.all:
                service_principals = client.get('/applications/').json()['value']

            self.results['applications'] = [self.to_dict(sp) for sp in service_principals]
        except Exception as ge:
            self.fail("failed to get application info {0}".format(str(ge)))

        return self.results

    def to_dict(self, object):
        if object is not None:
            return dict(
                app_id=object['appId'],
                object_id=object['id'],
                app_display_name=object['displayName'],
                app_roles=object['appRoles'],
                sign_in_audience=object['signInAudience'],
                web={'redirect_uris': object['web']['redirectUris']},
                public_client={'redirect_uris': object['publicClient']['redirectUris']},
                spa={'redirect_uris': object['spa']['redirectUris']},
            )


def main():
    AzureRMMSApplicationInfo()


if __name__ == '__main__':
    main()
