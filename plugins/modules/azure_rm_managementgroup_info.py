#!/usr/bin/python
#
# Copyright (c) 2020 Paul Aiton, < @paultaiton >
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_managementgroup_info

version_added: "1.2.0"

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
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
            - Option has no effect when searching by id or name, and will be silently ignored.
        type: list

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


class AzureRMSubscriptionInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str', aliases=['subscription_name']),
            id=dict(type='str')
        )

        self.results = dict(
            changed=False,
            management_groups=[]
        )

        self.name = None
        self.id = None
        self.tags = None
        self.all = False

        mutually_exclusive = [['name', 'id']]

        super(AzureRMSubscriptionInfo, self).__init__(self.module_arg_spec,
                                                      supports_tags=False,
                                                      mutually_exclusive=mutually_exclusive,
                                                      facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.id and self.name:
            self.fail("Parameter error: cannot search subscriptions by both name and id.")

        result = []

        if self.id:
            result = self.get_item()
        else:
            result = self.list_items()

        self.results['subscriptions'] = result
        return self.results

    def get_item(self):
        self.log('Get properties for {0}'.format(self.id))
        item = None
        result = []

        try:
            item = self.subscription_client.subscriptions.get(self.id)
        except CloudError:
            pass

        result = self.to_dict(item)

        return result

    def list_items(self):
        self.log('List all items')
        try:
            response = self.subscription_client.subscriptions.list()
        except CloudError as exc:
            self.fail("Failed to list all items - {0}".format(str(exc)))

        results = []
        for item in response:
            # If the name matches, return result regardless of anything else.
            # If name is not defined and either state is Enabled or all is true, and tags match, return result.
            if self.name and self.name.lower() == item.display_name.lower():
                results.append(self.to_dict(item))
            elif not self.name and (self.all or item.state == "Enabled") and self.has_tags(item.tags, self.tags):
                results.append(self.to_dict(item))

        return results

    def to_dict(self, subscription_object):
        return dict(
            display_name=subscription_object.display_name,
            fqid=subscription_object.id,
            state=subscription_object.state,
            subscription_id=subscription_object.subscription_id,
            tags=subscription_object.tags,
            tenant_id=subscription_object.tenant_id
        )


def main():
    AzureRMSubscriptionInfo()


if __name__ == '__main__':
    main()
