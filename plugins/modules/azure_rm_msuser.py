#!/usr/bin/python
#
# Copyright (c) 2023 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: azure_rm_msuser

version_added: "1.16.0"

short_description: Modify an Azure Active Directory user

description:
    - Create, delete, and update an Azure Active Directory user.

options:
    state:
        description:
            - State of the ad user. Use C(present) to create or update an ad user and C(absent) to delete an ad user.
        type: str
        default: present
        choices:
            - absent
            - present
    object_id:
        description:
            - The object id for the user.
            - Updates or deletes the user who has this object ID.
        type: str
    account_enabled:
        description:
            - A boolean determing whether or not the user account is enabled.
            - Used when either creating or updating a user account.
        type: bool
        default: True
    display_name:
        description:
            - The display name of the user.
            - Used when either creating or updating a user account.
        type: str
    mail:
        description:
            - The primary email address of the user.
            - Used when either creating or updating a user account.
        type: str
    mail_nickname:
        description:
            - The mail alias for the user.
            - Used when either creating or updating a user account.
        type: str
    password_profile:
        description:
            - The password config for the user.
            - Used when either creating or updating a user account.
        type: dict
        suboptions:
            Password:
                description:
                    - The password for the ad user.
                type: str
    user_principal_name:
        description:
            - The principal name of the user.
            - Creates, updates, or deletes the user who has this principal name.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
    - name: Create a new ad user
      azure_rm_msuser:
        user_principal_name: xiuxi.sun_qq.com#EXT#@824736848qq.onmicrosoft.com
        display_name: xiuxi.sun
        account_enabled: True
        mail_nickname: fred
        password_profile:
          Password: Password@0329
        mail: xiuxi.sun@qq.com

    - name: Delete microsoft groups
      azure_rm_msuser:
        display_name: xiuxi.sun
        state: absent
'''

RETURN = '''
object_id:
    description:
        - The object_id for the user.
    type: str
    returned: always
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
displayName:
    description:
        - The display name of the user.
    returned: always
    type: str
    sample: ansibletest
userPrincipalName:
    description:
        - The principal name of the user.
    returned: always
    type: str
    sample: 824736848_qq.com#EXT#@824736848qq.onmicrosoft.com
mail:
    description:
        - The primary email address of the user.
    returned: always
    type: str
    sample: 824736848qq.onmicrosoft.com
surname:
    description:
        - The user's surname (family name or last name).
    type: str
    returned: always
    sample: '张'
givenName:
    description:
        - The given name for the user.
    returned: always
    type: str
    sample: '旭'
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase
import json


class AzureRMMSUser(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            user_principal_name=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            object_id=dict(type='str'),
            account_enabled=dict(type='bool', default=True),
            display_name=dict(type='str'),
            password_profile=dict(
                type='dict',
                no_log=True,
                options=dict(
                    Password=dict(type='str', no_log=True),
                )
            ),
            mail_nickname=dict(type='str'),
            mail=dict(type='str'),
        )

        self.user_principal_name = None
        self.state = None
        self.object_id = None
        self.account_enabled = None
        self.display_name = None
        self.password_profile = None
        self.mail_nickname = None
        self.mail = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(changed=False)
        self.body = dict()

        super(AzureRMMSUser, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=False,
                                            supports_tags=False,
                                            )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

            if key == 'display_name':
                self.body['displayName'] = kwargs[key]
            elif key == 'password_profile':
                self.body['passwordProfile'] = kwargs[key]
            elif key == 'account_enabled':
                self.body['accountEnabled'] = kwargs[key]
            elif key == 'mail_nickname':
                self.body['mailNickname'] = kwargs[key]
            elif key == 'mail':
                self.body['mail'] = kwargs[key]
            elif key == 'user_principal_name':
                self.body['userPrincipalName'] = kwargs[key]

        client = self.get_msgraph_client()
        changed = False
        response = None
        try:
            if self.object_id:
                response = client.get('/users/' + self.object_id).json()
            elif self.display_name is not None:
                response = client.get('/users/').json()['value']
                flag = False
                for item in response:
                    if item['displayName'] == self.display_name:
                        flag = True
                        response = item
                        break
                if not flag:
                    response = None
            elif self.user_principal_name is not None:
                response = client.get('/users/').json()['value']
                flag = False
                for item in response:
                    if item['userPrincipalName'] == self.user_principal_name:
                        flag = True
                        response = item
                        break
                if not flag:
                    response = None
        except Exception as e:
            self.fail("failed to get ad user info {0}".format(str(e)))

        if response is not None and response.get('error'):
            response = None

        if response is not None:
            if self.state == 'present':
                changed = False
                self.log("The ad user account exist, don't recreate")
            else:
                response = self.delete_resource(response['id'])
                changed = True
        else:
            if self.state == 'present':
                response = self.create_resource(self.body)
                changed = True
            else:
                changed = False
                response = None
                self.log("The ad user account not exist")

        self.results['state'] = self.user_to_dict(response)
        self.results['changed'] = changed

        return self.results

    def create_resource(self, obj):
        client = self.get_msgraph_client()
        res = None
        try:
            res = client.post('/users/', data=json.dumps(obj), headers={'Content-Type': 'application/json'})
            return res.json()
        except Exception as e:
            self.fail("Error creating ad user, {0}".format(str(e)))

    def delete_resource(self, obj):
        client = self.get_msgraph_client()
        try:
            client.delete('/users/' + obj)
        except Exception as e:
            self.fail("Error deleting ad users {0}".format(str(e)))

    def user_to_dict(self, object):
        if object:
            return dict(
                object_id=object['id'],
                display_name=object['displayName'],
                user_principal_name=object['userPrincipalName'],
                give_name=object['givenName'],
                surname=object['surname'],
                mail=object['mail'],
            )
        else:
            return []


def main():
    AzureRMMSUser()


if __name__ == '__main__':
    main()
