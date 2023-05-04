#!/usr/bin/python
#
# Copyright (c) 2023 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_msserviceprincipal

version_added: "1.16.0"

short_description: Manage Azure Active Directory service principal

description:
    - Manage Azure Active Directory service principal.

options:
    app_id:
        description:
            - The application ID.
        type: str
    object_id:
        description:
            - The service principal's object ID.
        type: str
    name:
        description:
            - The display name of the service principal.
        type: str
    web:
        description:
            - Configure the redirect Web URI.
        type: dict
        suboptions:
            redirect_uris:
                description:
                    - The authentication response to this URI.
                type: list
                elements: str
    spa:
        description:
            - Configure the redirection Single Page Application (SPA) URI.
        type: dict
        suboptions:
            redirect_uris:
                description:
                    - The authentication response to this URI.
                type: list
                elements: str
    public_client:
        description:
            - Redirects the public client/native URI,
        type: dict
        suboptions:
            redirect_uris:
                description:
                    - Configure the redirection public client/local URI.
                type: list
                elements: str
    sign_in_audience:
        description:
            - The service principal account type.
        type: str
        choices:
            - PersonalMicrosoftAccount
            - AzureADandPersonalMicrosoftAccount
            - AzureADMultipleOrgs
            - AzureADMyOrg
        default: AzureADMyOrg
    state:
        description:
            - Assert the state of Active Dirctory service principal.
            - Use C(present) to create or update a Password and use C(absent) to delete.
            - If use I(state=absent), It must to be config C(app_id) or C(object_id).
        default: present
        choices:
            - absent
            - present
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
  - name: create ad sp
    azure_rm_msserviceprincipal:
      app_id: "{{ app_id }}"
      state: present
      name: test
      sign_in_audience: AzureADMyOrg
      web:
        redirect_uris:
            - https://localhost
'''

RETURN = '''
app_display_name:
    description:
        - Object's display name or its prefix.
    type: str
    returned: always
    sample: fredAKSCluster
app_id:
    description:
        - The application ID.
    returned: always
    type: str
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
app_role:
    description:
        - The collection of application roles that an application may declare.
        - These roles can be assigned to users, groups or service principals.
    returned: always
    type: list
    sample: []
object_id:
    description:
        - Object ID of the associated service principal.
    returned: always
    type: str
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
spa:
    description:
        - The single page application(SPA) URI of Redirects.
    returned: always
    type: dict
    sample: {'redirect_uris':['https://spa.com']}
web:
    description:
        - The WEB URI of Redirects.
    returned: always
    type: dict
    sample: {'redirect_uris':['https://web.com']}
public_client:
    description:
        - The public client/native URI of Redirects.
    returned: always
    type: dict
    sample: {'redirect_uris':['https://localhost']}
sign_in_audience:
    description:
        - The service principal account type.
    type: str
    returned: always
    sample: PersonalMicrosoftAccount
'''
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
import json


spa_spec = dict(
    redirect_uris=dict(type='list', elements='str')
)

public_client_spec = dict(
    redirect_uris=dict(type='list', elements='str')
)

web_spec = dict(
    redirect_uris=dict(type='list', elements='str')
)


class AzureRMMSServicePrincipal(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            object_id=dict(type='str'),
            app_id=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            name=dict(type='str'),
            sign_in_audience=dict(
                type='str',
                choices=['AzureADMyOrg', 'AzureADMultipleOrgs', 'AzureADandPersonalMicrosoftAccount', 'PersonalMicrosoftAccount'],
                default='AzureADMyOrg'
            ),
            web=dict(type='dict', options=web_spec),
            spa=dict(type='dict', options=spa_spec),
            public_client=dict(type='dict', options=public_client_spec)
        )

        self.state = None
        self.app_id = None
        self.object_id = None
        self.name = None
        self.sign_in_audience = None
        self.web = None
        self.spa = None
        self.public_client = None

        self.results = dict(changed=False)
        self.body = dict()

        super(AzureRMMSServicePrincipal, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=False,
                                                        supports_tags=False
                                                        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

            if key == 'name':
                self.body['displayName'] = kwargs[key]
            elif key == 'sign_in_audience':
                self.body['signInAudience'] = kwargs[key]
            elif key == 'public_client':
                self.body['publicClient'] = dict()
                self.body['publicClient']['redirectUris'] = kwargs[key]['redirect_uris']
            elif key == 'web':
                self.body['web'] = dict()
                self.body['web']['redirectUris'] = kwargs[key]['redirect_uris']
            elif key == 'spa':
                self.body['spa'] = dict()
                self.body['spa']['redirectUris'] = kwargs[key]['redirect_uris']

        client = self.get_msgraph_client()
        response = None
        changed = False
        try:
            if self.object_id is not None:
                response = client.get('/applications/' + self.object_id).json()
            elif self.app_id is not None:
                response = client.get('/applications/').json()['value']
                flag = False
                for item in response:
                    if item['appId'] == self.app_id:
                        flag = True
                        response = item
                        break
                if not flag:
                    response = None

        except Exception as e:
            self.log("There is no service principal {0}".format(str(e)))
        if response is not None and response.get('error'):
            response = None

        if response is not None:
            if self.state == 'present':
                changed = True
                client.delete('/applications/' + response['id'])
                response = self.create_resource(self.body)
            else:
                changed = True
                response = self.delete_resource(response['id'])
        else:
            if self.state == 'present':
                response = self.create_resource(self.body)
                changed = True
            else:
                self.log("The Service principal does not exist")

        self.results['changed'] = changed
        self.results['state'] = response

        return self.results

    def create_resource(self, obj):
        client = self.get_msgraph_client()
        res = None
        try:
            res = client.post('/applications/', data=json.dumps(obj), headers={'Content-Type': 'application/json'})

            if res.json().get('error') is not None:
                self.fail("Create ad service princiapl fail, Msg {0}".format(res.json().get('error')))
            else:
                return self.to_dict(res.json())
        except Exception as e:
            self.fail("Error creating service principle, {0}".format(str(e)))

    def delete_resource(self, obj):
        client = self.get_msgraph_client()
        try:
            client.delete('/applications/' + obj)
        except Exception as e:
            self.fail("Error deleting service principal {0}".format(str(e)))

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
    AzureRMMSServicePrincipal()


if __name__ == '__main__':
    main()
