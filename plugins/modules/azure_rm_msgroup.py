#!/usr/bin/python
#
# Copyright (c) 2023 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: azure_rm_msgroup
version_added: "1.16.0"
short_description: Manage Azure Active Directory group
description:
    - Create, update or delete Azure Active Directory group.
options:
    state:
        description:
            - If I(state=absent),  It must to be config C(display_name) or C(object_id).
            - Assert the state of the resource group. Use C(present) to create or update and C(absent) to delete.
        default: present
        choices:
            - absent
            - present
        type: str
    object_id:
        description:
            - The object id for the ad group.
            - Can be used to reference when updating an existing group.
            - Ignored when attempting to create a group.
        type: str
    display_name:
        description:
            - The display name of the ad group.
            - Can be used with I(mail_nickname) instead of I(object_id) to reference existing group.
            - Required when creating a new ad group.
        type: str
    mail_nickname:
        description:
            - The mail nickname of the ad group.
            - Can be used with I(display_name) instead of I(object_id) to reference existing group.
            - Required when creating a new ad group.
        type: str
    mail_enabled:
        description:
            - Whether the group is mail-enabled. Must be false.
            - This is because only pure security groups can be created using the Graph API.
        type: bool
        default: False
    security_enabled:
        description:
            - Whether the group is security-enable.
        type: bool
        default: True
    description:
        description:
            - Description of the groups.
        type: str
    group_types:
        description:
            - The type of the groups.
        type: str
        choices:
            - Unified
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
    - name: create new microsoft groups
      azure_rm_msgroup:
        display_name: testmsgroup
        description: "For test group "
        mail_nickname: msgrouptest
        group_types: Unified
        mail_enabled: True
        security_enabled: True

    - name: Delete microsoft groups
      azure_rm_msgroup:
        display_name: testmsgroup
        state: absent
'''

RETURN = '''
object_id:
    description:
        - The object_id for the group.
    type: str
    returned: always
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
display_name:
    description:
        - The display name of the group.
    returned: always
    type: str
    sample: GroupName
mail_nickname:
    description:
        - The mail alias for the group.
    returned: always
    type: str
    sample: groupname
mail_enabled:
    description:
        - Whether the group is mail-enabled. Must be false.
        - This is because only pure security groups can be created using the Graph API.
    returned: always
    type: bool
    sample: False
security_enabled:
    description:
        - Whether the group is security-enable.
    returned: always
    type: bool
    sample: True
description:
    description:
        - Describe of the ad group.
    type: str
    returned: always
    sample: For test
group_type:
    description:
        - The Type of the ad group.
    type: str
    returned: always
    sample: Microsoft 365
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase
import json


class AzureRMMSGroup(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            object_id=dict(type='str'),
            display_name=dict(type='str'),
            mail_nickname=dict(type='str'),
            group_types=dict(type='str', choices=['Unified']),
            description=dict(type='str'),
            security_enabled=dict(type='bool', default=True),
            mail_enabled=dict(type='bool', default=False),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
        )

        self.display_name = None
        self.mail_nickname = None
        self.object_id = None
        self.description = None
        self.group_types = []
        self.security_enabled = None
        self.mail_enabled = None
        self.state = None

        self.results = dict(changed=False)
        self.body = dict()

        super(AzureRMMSGroup, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=False,
                                             supports_tags=False,
                                             )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])
            if key == 'display_name':
                self.body['displayName'] = kwargs[key]
            elif key == 'description':
                self.body['description'] = kwargs[key]
            elif key == 'group_types':
                self.body['groupTypes'] = [kwargs[key]]
            elif key == 'security_enabled':
                self.body['securityEnabled'] = kwargs[key]
            elif key == 'mail_enabled':
                self.body['mailEnabled'] = kwargs[key]
            elif key == 'mail_nickname':
                self.body['mailNickname'] = kwargs[key]

        client = self.get_msgraph_client()
        response = None
        changed = False

        try:
            if self.object_id:
                response = client.get('/groups/' + self.object_id).json()
            elif self.display_name is not None:
                response = client.get('/groups/').json()['value']
                flag = False
                for item in response:
                    if item['displayName'] == self.display_name:
                        flag = True
                        response = item
                        break
                if not flag:
                    response = None
        except Exception as e:
            self.log("There is no group {0}".format(str(e)))

        if response is not None and response.get('error'):
            response = None

        if response is not None:
            if self.state == 'present':
                changed = False
                self.log("The group already exist")
            else:
                changed = True
                response = self.delete_resource(response['id'])
        else:
            if self.state == 'present':
                changed = True
                response = self.create_resource(self.body)
            else:
                changed = False
                self.log("The group do not exist")

        self.results['changed'] = changed
        self.results['state'] = response

        return self.results

    def create_resource(self, obj):
        client = self.get_msgraph_client()
        res = None
        try:
            res = client.post('/groups/', data=json.dumps(obj), headers={'Content-Type': 'application/json'})

            if res.json().get('error') is not None:
                self.fail("Create ad group fail, Msg {0}".format(res.json().get('error')))
            else:
                return self.group_to_dict(res.json())
        except Exception as e:
            self.fail("Error creating group, msg {0}".format(str(e)))

    def delete_resource(self, obj):
        client = self.get_msgraph_client()
        try:
            client.delete('/groups/' + obj)
        except Exception as e:
            self.fail("Error deleting group {0}".format(str(e)))

    def group_to_dict(self, object):
        return dict(
            object_id=object['id'],
            display_name=object['displayName'],
            mail_nickname=object['mailNickname'],
            mail_enabled=object['mailEnabled'],
            security_enabled=object['securityEnabled'],
            description=object['description'],
            group_type=object['groupTypes'],
        )


def main():
    AzureRMMSGroup()


if __name__ == '__main__':
    main()
