#!/usr/bin/python
#
# Copyright (c) 2021 Paul Aiton, < @paultaiton >
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from msrestazure.tools import parse_resource_id
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_managementgroup_info

version_added: "1.5.0"

short_description: Get Azure Management Group facts

description:
    - Get facts for a specific Management Group or all Management Groups.

options:
    id:
        description:
            - Limit results to a specific management group by id.
            - Mutually exclusive with I(name).
        type: str
    name:
        description:
            - Limit results to a specific management group by name.
            - Mutually exclusive with I(id).
        aliases:
            - management_group_name
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Paul Aiton (@paultaiton)
'''

EXAMPLES = '''
'''

RETURN = '''
management_groups:
    description:
        - List of Management Group dicts.
    returned: always
    type: list
    contains:
        display_name:
            description: Management Group display name.
            returned: always
            type: str
            sample: "My Management Group"
        fqid:
            description: Management Group fully qualified id.
            returned: always
            type: str
            sample: "/providers/Microsoft.Management/managementGroups/group-name"
        name:
            description: Management Group display name.
            returned: always
            type: str
            sample: group-name
        tenant_id:
            description: Management Group tenant id
            returned: always
            type: str
            sample: "00000000-0000-0000-0000-000000000000"
        type:
            description: Management Group type
            returned: always
            type: str
            sample: "/providers/Microsoft.Management/managementGroups"
'''

try:
    from msrestazure.azure_exceptions import CloudError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMManagementGroupInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            # display_name_filter=dict(type='str')
            name=dict(type='str'),
            id=dict(type='str'),
            flatten=dict(type='bool', default=False),
            children=dict(type='bool', default=False),
            recurse=dict(type='bool', default=False)
        )

        self.results = dict(
            changed=False,
            management_groups=[]
        )

        self.name = None
        self.id = None
        self.flatten = None
        self.children = None
        self.recurse = None

        mutually_exclusive = [['name', 'id']]

        super(AzureRMManagementGroupInfo, self).__init__(self.module_arg_spec,
                                                         supports_tags=False,
                                                         mutually_exclusive=mutually_exclusive,
                                                         facts_module=True)

    def flatten_group(self, management_group):
        management_group_list = []
        subscription_list = []
        if management_group.get('children'):
            for child in management_group.get('children', []):
                if child.get('type') == '/providers/Microsoft.Management/managementGroups':
                    management_group_list.append(child)
                    new_groups, new_subscriptions = self.flatten_group(child)
                    management_group_list += new_groups
                    subscription_list += new_subscriptions
                elif child.get('type') == '/subscriptions':
                    subscription_list.append(child)
        return management_group_list, subscription_list

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        response = []

        if self.name or self.id:
            response = [self.get_item()]
        else:
            response = self.list_items()

        if self.flatten and self.children:
            self.results['subscriptions'] = []
            for group in response:
                new_groups = []
                new_subscriptions = []
                self.results['management_groups'].append(group)
                new_groups, new_subscriptions = self.flatten_group(group)
                self.results['management_groups'] += new_groups
                self.results['subscriptions'] += new_subscriptions
        else:
            self.results['management_groups'] = response

        return self.results

    def get_item(self, mg_name=None):
        if not mg_name:
            if self.id and not self.name:
                mg_name = self.id.split('/')[-1]
            else:
                mg_name = self.name

        expand = 'children' if self.children else None

        try:
            # The parameter to SDK's management_groups.get(group_id) is not correct,
            # it only works with a bare name value.
            response = self.management_groups_client.management_groups.get(group_id=mg_name, expand=expand, recurse=self.recurse)
        except CloudError:
            response = None

        return self.to_dict(response)

    def list_items(self):
        self.log('List all management groups.')

        results = []
        response = []

        try:
            response = self.management_groups_client.management_groups.list()
        except CloudError:
            pass  # default to response empty list

        if self.children:
            # list method cannot return children, so we must iterate over root management groups to get each one individually.
            results = [self.get_item(mg_name=item.name) for item in response]
        else:
            results = [self.to_dict(item) for item in response]

        return results

    def to_dict(self, azure_object):
        if azure_object.type == '/providers/Microsoft.Management/managementGroups':
            return_dict = dict(
                display_name=azure_object.display_name,
                id=azure_object.id,
                name=azure_object.name,
                type=azure_object.type
            )
            if self.children and azure_object.as_dict().get('children'):
                return_dict['children'] = [self.to_dict(item) for item in azure_object.children]  # if item.type == '/providers/Microsoft.Management/managementGroups']
        elif azure_object.type == '/subscriptions':
            return_dict = dict(
                display_name=azure_object.display_name,
                id=azure_object.id,
                subscription_id=azure_object.name,
                type=azure_object.type
            )
        else:
            # This should never happen. The code here will prevent a problem,
            # but there should be logic to take care of a new child type of management groups.
            return_dict = dict(
                state='You should report this as a bug.'
            )

        if azure_object.as_dict().get('tenant_id'):
            return_dict['tenant_id'] = azure_object.tenant_id

        return return_dict

    def flatten(self, azure_object):
        return [azure_object]


def main():
    AzureRMManagementGroupInfo()


if __name__ == '__main__':
    main()
