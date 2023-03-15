#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_msserviceprincipal

version_added: "1.15.0"

short_description: Manage Azure Active Directory service principal

description:
        - Manage Azure Active Directory service principal.

options:
    app_id:
        description:
            - The application ID.
        type: str
        required: True
    object_id:
        description:
            - It's service principal's object ID.
        type: str
    name:
        description:
            - The display name of the service principal.
        type: str
    web:
        description:
            - Redirects the Web URI,
        type: dict
        subopions:
            redirectUris:
                description:
                    - The authentication response to this URI.
                type: list
                elements: str
    spa:
        description:
            - Redirects the single page application(SPA) URI,
        type: dict
        subopions:
            redirectUris:
                description:
                    - The authentication response to this URI.
                type: list
                elements: str
    public_client:
        description:
            - Redirects the public client/native URI,
        type: dict
        subopions:
            redirectUris:
                description:
                    - The authentication response to this URI.
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
    - azure.azcollection.azure_tags

author:
    xuzhang3 (@xuzhang3)
    Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
  - name: create ad sp
    azure_rm_msserviceprincipal:
      app_id: "{{ app_id }}"
      state: present
      name: test
      sign_in_audience: AzureADMyOrg
      web:
        redirectUris:
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
        -  The collection of application roles that an application may declare.
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
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
import json


spa_spec = dict(
    redirectUris=dict(type='list', elements='str')
)

public_client_spec = dict(
    redirectUris=dict(type='list', elements='str')
)

web_spec = dict(
    redirectUris=dict(type='list', elements='str')
)

class AzureRMMSServicePrincipal(AzureRMModuleBaseExt):
    def __init__(self):

        self.module_arg_spec = dict(
            object_id=dict(type='str'),
            app_id=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            name=dict(type='str'),
            sign_in_audience=dict(type='str', choices=['AzureADMyOrg','AzureADMultipleOrgs', 'AzureADandPersonalMicrosoftAccount', 'PersonalMicrosoftAccount']),
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
                self.body['publicClient'] = kwargs[key]
            elif key == 'web':
                self.body['web'] = kwargs[key]
            elif key == 'spa':
               self.body['spa'] = kwargs[key]

        client = self.get_msgraph_client()
        response = None
        changed = False
        try:
            if self.object_id is not None:
                response = client.get('/applications/' + self.object_id).json()
            elif self.app_id is not None:
                response = client.get('/applications/').json()['value']
                for item in response:
                    if item['appId'] == self.app_id:
                        response = item
        except Exception as e:
            self.log("There is not service principal {0}".format(str(e)))
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
                self.log("The Service principal is not exist")

        self.results['changed'] = changed
        self.results['state'] = response

        return self.results


    def create_resource(self, obj):
        client = self.get_msgraph_client()
        res = None
        try:
            res = client.post('/applications/', data=json.dumps(obj), headers={'Content-Type': 'application/json'})
            return self.to_dict(res.json())
        except Exception as e:
            self.fail("Error creating service principle, app id {0} - {1}".format(self.app_id, str(e))) 

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
                web={'redirectUris': object['web']['redirectUris']},
                public_client={'redirectUris': object['publicClient']['redirectUris']},
                spa={'redirectUris': object['spa']['redirectUris']},
            )


def main():
    AzureRMMSServicePrincipal()


if __name__ == '__main__':
    main()
