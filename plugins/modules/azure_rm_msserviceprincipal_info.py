#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
module: azure_rm_msserviceprincipal_info

version_added: "0.2.0"

short_description: Get Azure Active Directory service principal info

description:
    - Get Azure Active Directory service principal info.

options:
    app_id:
        description:
            - The application ID.
        type: str
    object_id:
        description:
            - It's service principal's object ID.
        type: str
    all:
        description:
            - If True, will return all applicatin in tenant.
            - If False will return no application.
            - Mutually exclusive with I(object_id) and I(app_id).
        type: bool

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    xuzhang3 (@xuzhang3)    
    Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
  - name: get MS sp info by object_id
    azure_rm_msserviceprincipal_info:
      object_id: "{{ object_id }}"

  - name: get all MS sp info
    azure_rm_msserviceprincipal_info:
        all: True

  - name: get MS sp info by App ID
    azure_rm_msserviceprincipal_info:
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
        -  The collection of application roles that an application may declare.
        - These roles can be assigned to users, groups or service principals.
    type: list
    returned: always
    sample: []
object_id:
    description:
        - It's service principal's object ID.
    returned: always
    type: str
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
spa:
    descriptoin:
        - Redirects the single page application(SPA) URI,
    returnd: always
    type: dcit
    sample: {redirectUris:['https://spa.com']}
web:
    descriptoin:
        - Redirects the Web URI,
    returnd: always
    type: dcit
    sample: {redirectUris:['https://web.com']}
public_client:
    descriptoin:
        - Redirects the public client/native URI.
    returnd: always
    type: dcit
    sample: {redirectUris:['https://localhost']}
sign_in_audience:
    description:
        - The service principal account type.
    type: str
    returned: always
    sample: PersonalMicrosoftAccount
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase


class AzureRMMSServicePrincipalInfo(AzureRMModuleBase):
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

        super(AzureRMMSServicePrincipalInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
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
            elif all:
                service_principals = client.get('/applications/').json()['value']

            self.results['service_principals'] = [self.to_dict(sp) for sp in service_principals]
        except Exception as ge:
            self.fail("failed to get service principal info {0}".format(str(ge)))

        return self.results

    def to_dict(self, object):
        if object is not None:
            return dict(
                app_id=object['appId'],
                object_id=object['id'],
                app_display_name=object['displayName'],
                app_roles=object['appRoles'],
                sign_in_audience=object['signInAudience'],
                web={'redirectUris': object['web']['redirectUris']},
                public_client={'redirectUris': object['publicClient']['redirectUris']},
                spa={'redirectUris': object['spa']['redirectUris']},
            )


def main():
    AzureRMMSServicePrincipalInfo()


if __name__ == '__main__':
    main()
