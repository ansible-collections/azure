#!/usr/bin/python
#
# Copyright (c) 2020 Cole Neubauer, (@coleneubauer)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: azure_rm_msuser_info

version_added: "1.4.0"

short_description: Get Azure Microsoft Graph user info

description:
    - Get Microsoft Graph user info.

options:
    object_id:
        description:
            - The object id for the user.
            - returns the user who has this object ID.
            - Mutually exclusive with I(user_principal_name), I(attribute_name) and I(all).
        type: str
    user_principal_name:
        description:
            - The principal name of the user.
            - returns the user who has this principal name.
            - Mutually exclusive with I(object_id), I(attribute_name) and I(all).
        type: str
    attribute_name:
        description:
            - The name of an attribute that you want to match to attribute_value.
            - If attribute_name is not a collection type it will return users where attribute_name is equal to attribute_value.
            - If attribute_name is a collection type it will return users where attribute_value is in attribute_name.
            - Mutually exclusive with I(object_id), I(user_principal_name) and I(all).
            - Required together with I(attribute_value).
        type: str
    attribute_value:
        description:
            - The value to match attribute_name to.
            - If attribute_name is not a collection type it will return users where attribute_name is equal to attribute_value.
            - If attribute_name is a collection type it will return users where attribute_value is in attribute_name.
            - Required together with I(attribute_name).
        type: str
    all:
        description:
            - If True, will return all users in tenant.
            - If False will return no users.
            - It is recommended that you instead identify a subset of users and use filter.
            - Mutually exclusive with I(object_id), I(attribute_name) and I(user_principal_name).
        type: bool
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Cole Neubauer(@coleneubauer)

'''

EXAMPLES = '''
    - name: Using user_principal_name
      azure.azcollection.azure_rm_msuser_info:
        user_principal_name: user@contoso.com

    - name: Using object_id
      azure.azcollection.azure_rm_msaduser_info:
        object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Using attribute mail - not a collection
      azure.azcollection.azure_rm_msuser_info:
        attribute_name: mail
        attribute_value: foo@contoso.com

    - name: Get all user in same tenant
      azure.azcollection.azure_rm_msuser_info:
        all: True
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

class AzureRMMSUserInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            user_principal_name=dict(type='str'),
            object_id=dict(type='str'),
            attribute_name=dict(type='str'),
            attribute_value=dict(type='str'),
            all=dict(type='bool'),
        )

        self.user_principal_name = None
        self.object_id = None
        self.attribute_name = None
        self.attribute_value = None
        self.all = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(changed=False)

        mutually_exclusive = [['attribute_name', 'object_id', 'user_principal_name', 'all']]
        required_together = [['attribute_name', 'attribute_value']]
        required_one_of = [['attribute_name', 'object_id', 'user_principal_name', 'all']]

        super(AzureRMMSUserInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False,
                                                mutually_exclusive=mutually_exclusive,
                                                required_together=required_together,
                                                required_one_of=required_one_of,
                                                )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        ms_user = []
        try:
            client = self.get_msgraph_client()

            if self.user_principal_name is not None:
                ms_user = [client.get('/users/' + self.user_principal_name).json()]
            elif self.object_id is not None:
                ms_user = [client.get('/users/' + self.object_id).json()]
            elif self.attribute_name is not None and self.attribute_value is not None:
                response = client.get('/users/').json()['value']
                for item in response:
                    if item[self.attribute_name] == self.attribute_value:
                        ms_user.append(item)
            elif self.all:
                ms_user = client.get('/users/').json()['value']

            self.results['ms_users'] = [self.to_dict(user) for user in ms_user]

        except Exception as e:
            self.fail("failed to get Microsoft Grpah user info {0}".format(str(e)))

        return self.results

    def to_dict(self, object):
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
    AzureRMMSUserInfo()


if __name__ == '__main__':
    main()
