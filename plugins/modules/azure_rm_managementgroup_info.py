#!/usr/bin/python
#
# Copyright (c) 2021 Paul Aiton, < @paultaiton >
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_managementgroup_info

version_added: "1.5.0"

short_description: Get Azure Management Group facts

description:
    - Get facts for a specific Management Group or all Management Groups.

options:
    name:
        description:
            - Limit results to a specific management group by name.
            - Mutually exclusive with I(id).
        aliases:
            - management_group_name
        type: str
    id:
        description:
            - Limit results to a specific management group by id.
            - Mutually exclusive with I(name).
        type: str
    flatten:
        description:
            - If c(True) then child management_groups and subscriptions will be copied to the root
              of the management_groups and subscriptions return list respectively.
            - By default c(False), child elements will only apear in the nested complex.
            - Option only matters when I(children) is c(True), and will otherwise be silently ignored.
        type: bool
        default: False
    children:
        description:
            - If c(False), then only I(name) or I(id) group will be fetched, or only the list of root groups.
            - If c(True), then the children groups will also be returned.
        type: bool
        default: False
    recurse:
        description:
            - By default, c(False), only the direct children are returned if I(children) is c(True).
            - If c(True), then all descendants of the heirarchy are returned.
            - Option only matters when I(children) is c(True), and will otherwise be silently ignored.
        type: bool
        default: False

notes:
    - azure_rm_managementgroup_info - The roles assigned to the principal executing the playbook will determine what is
      a root management_group. You may also be able to request the details of a parent management group, but unable to
      fetch that group. It is highly recommended that if I(children) is set c(True) that specific management groups are
      requested since a list of all groups will require an additional Azure API call for each returned group.

seealso:
    - module: azure_rm_subscription_info
      description: module to look up more in depth information on subscriptions; for example tags.
    - module: azure_rm_roleassignment_info
      description: module to look up RBAC role assignments, which can use management group id as scope.

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Paul Aiton (@paultaiton)
'''

EXAMPLES = '''
- name: Get facts for all root management groups for authenticated principal
  azure_rm_managementgroup_info:

- name: Get facts for one management group by id with direct children
  azure_rm_managementgroup_info:
    id: /providers/Microsoft.Management/managementGroups/contoso-group
    children: True

- name: Get facts for one management group by name with all children, flattened into top list
  azure_rm_managementgroup_info:
    name: "contoso-group"
    children: True
    recurse: True
    flatten: True
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
        id:
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
        children:
            description: Child management groups or subscriptions.
            returned: if I(children) is c(True)
            type: list
            sample: Nested list of children. Same as top groups, but without tenant_id.
subscriptions:
    description:
        - List of subscription objects.
    returned: if I(children) and I(flatten) are both c(True)
    type: list
    contains:
        display_name:
            description: subscription display name.
            returned: always
            type: str
            sample: "some-subscription-name"
        id:
            description: subscription fully qualified id.
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-feedc0ffee000000"
        subscription_id:
            description: subscription guid.
            returned: always
            type: str
            sample: "00000000-0000-0000-0000-feedc0ffee000000"
        type:
            description: Management Group type
            returned: always
            type: str
            sample: "/subscriptions"
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
            children=dict(type='bool', default=False),
            flatten=dict(type='bool', default=False),
            id=dict(type='str'),
            name=dict(type='str', aliases=['management_group_name']),
            recurse=dict(type='bool', default=False)
        )

        self.results = dict(
            changed=False,
            management_groups=[]
        )

        self.children = None
        self.flatten = None
        self.id = None
        self.name = None
        self.recurse = None

        mutually_exclusive = [['name', 'id']]

        super(AzureRMManagementGroupInfo, self).__init__(self.module_arg_spec,
                                                         supports_check_mode=True,
                                                         supports_tags=False,
                                                         mutually_exclusive=mutually_exclusive,
                                                         facts_module=True)

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
            # The parameter to SDK's management_groups.get(group_id) is not correct,
            # it only works with a bare name value, and not the fqid.
            if self.id and not self.name:
                mg_name = self.id.split('/')[-1]
            else:
                mg_name = self.name

        expand = 'children' if self.children else None
        try:
            response = self.management_groups_client.management_groups.get(group_id=mg_name,
                                                                           expand=expand,
                                                                           recurse=self.recurse)
        except CloudError:
            self.log('No Management group {0} found.'.format(mg_name))
            response = None

        return self.to_dict(response)

    def list_items(self):
        self.log('List all management groups.')

        results = []
        response = []

        try:
            response = self.management_groups_client.management_groups.list()
        except CloudError:
            self.log('No Management groups found.')
            pass  # default to response of an empty list

        if self.children:
            # list method cannot return children, so we must iterate over root management groups to
            # get each one individually.
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

            # If group has no children, then property will be set to None type.
            # We want an empty list so that it can be used in loops without issue.
            if self.children and azure_object.as_dict().get('children'):
                return_dict['children'] = [self.to_dict(item) for item in azure_object.children]
            elif self.children:
                return_dict['children'] = []

            if azure_object.as_dict().get('details', {}).get('parent'):
                parent_dict = azure_object.as_dict().get('details', {}).get('parent')
                return_dict['parent'] = dict(
                    display_name=parent_dict.get('display_name'),
                    id=parent_dict.get('id'),
                    name=parent_dict.get('name')
                )

        elif azure_object.type == '/subscriptions':
            return_dict = dict(
                display_name=azure_object.display_name,
                id=azure_object.id,
                subscription_id=azure_object.name,
                type=azure_object.type
            )
        else:
            # In theory if the Azure API is updated to include another child type of management groups,
            # the code here will prevent an exception. But there should be logic added in an update to take
            # care of a new child type of management groups.
            return_dict = dict(
                state="This is an unknown and unexpected object. "
                      + "You should report this as a bug to the ansible-collection/azcollection "
                      + "project on github. Please include the object type in your issue report, "
                      + "and @ the authors of this module. ",
                type=azure_object.as_dict().get('type', None)
            )

        if azure_object.as_dict().get('tenant_id'):
            return_dict['tenant_id'] = azure_object.tenant_id

        return return_dict

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


def main():
    AzureRMManagementGroupInfo()


if __name__ == '__main__':
    main()
