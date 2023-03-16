#!/usr/bin/python
#
# Copyright (c) 2023 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: azure_rm_msgroup_info
version_added: "1.16.0"
short_description: Get Microsoft Graph group info
description:
    - Get Microsoft Graph group info.
options:
    object_id:
        description:
            - The object id for the ad group.
            - returns the group which has this object ID.
        type: str
    attribute_name:
        description:
            - The name of an attribute that you want to match to attribute_value.
            - If attribute_name is not a collection type it will return groups where attribute_name is equal to attribute_value.
            - If attribute_name is a collection type it will return groups where attribute_value is in attribute_name.
        type: str
    attribute_value:
        description:
            - The value to match attribute_name to.
            - If attribute_name is not a collection type it will return groups where attribute_name is equal to attribute_value.
            - If attribute_name is a collection type it will groups users where attribute_value is in attribute_name.
        type: str
    all:
        description:
            - If True, will return all groups in tenant.
            - If False will return no users.
            - It is recommended that you instead identify a subset of groups and use filter.
        default: False
        type: bool
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
    - name: Return a specific group using object_id
      azure_rm_msgroup_info:
        object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Return a specific group using displayName for attribute_name
      azure_rm_msgroup_info:
        attribute_name: "displayName"
        attribute_value: "Display-Name-Of-AD-Group"

    - name: Return all groups
      azure_rm_msgroup_info:
        all: True
'''

RETURN = '''
object_id:
    description:
        - The object_id for the group.
    type: str
    returned: always
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
displayName:
    description:
        - The display name of the group.
    returned: always
    type: str
    sample: GroupName
securityEnabled:
    description:
        - Whether the group is security-enable.
    returned: always
    type: bool
    sample: False
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


class AzureRMMSGroupInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            object_id=dict(type='str'),
            attribute_name=dict(type='str'),
            attribute_value=dict(type='str'),
            all=dict(type='bool', default=False),
        )

        self.object_id = None
        self.attribute_name = None
        self.attribute_value = None
        self.all = False

        self.results = dict(changed=False)

        mutually_exclusive = [['attribute_name', 'object_id', 'all']]
        required_together = [['attribute_name', 'attribute_value']]
        required_one_of = [['attribute_name', 'object_id', 'all']]

        super(AzureRMMSGroupInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=False,
                                                 mutually_exclusive=mutually_exclusive,
                                                 required_together=required_together,
                                                 required_one_of=required_one_of,
                                                 )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        ms_groups = []

        try:
            client = self.get_msgraph_client()

            if self.object_id is not None:
                ms_groups = [client.get('/groups/' + self.object_id).json()]
            elif self.attribute_name is not None and self.attribute_value is not None:
                response = client.get('/groups/').json()['value']
                for item in response:
                    if item[self.attribute_name] == self.attribute_value:
                        ms_groups.append(item)
            elif self.all:
                ms_groups = client.get('/groups/').json()['value']

            self.results['ms_groups'] = [self.group_to_dict(sp_item) for sp_item in ms_groups]

        except Exception as e:
            self.log("failed to get MS group info {0}".format(str(e)))
            self.results['ms_groups'] = []

        return self.results


    def group_to_dict(self, object):
        if object is not None:
            return dict(
                object_id=object['id'],
                displayName=object['displayName'],
                securityEnabled=object['securityEnabled'],
                description=object['description'],
                mail_nickname=object['mailNickname'],
                mail_enabled=object['mailEnabled'],
                group_type=object['groupTypes'],
            )

def main():
    AzureRMMSGroupInfo()


if __name__ == '__main__':
    main()
