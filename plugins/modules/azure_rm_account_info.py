#!/usr/bin/python
#
# Copyright (c) 2020 Paul Aiton, < @paultaiton >
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_account_info

version_added: "1.2.0"

short_description: Get Azure Account facts (output of az account show)

description:
    - Get facts for a specific account or all accounts.

options:
    id:
        description:
            - Limit results to a specific subscription by id.
            - Mutually exclusive with I(name).
        type: str
    name:
        description:
            - Limit results to a specific subscription by name.
            - Mutually exclusive with I(id).
        aliases:
            - subscription_name
        type: str
    all:
        description:
            - If true, will return all subscriptions.
            - If false will omit disabled subscriptions (default).
            - Option has no effect when searching by id or name, and will be silently ignored.
        type: bool
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key:value'.
            - Option has no effect when searching by id or name, and will be silently ignored.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Paul Aiton (@paultaiton)
'''

EXAMPLES = '''
- name: Get facts for one subscription by id
  azure_rm_subscription_info:
    id: 00000000-0000-0000-0000-000000000000

- name: Get facts for one subscription by name
  azure_rm_subscription_info:
    name: "my-subscription"

- name: Get facts for all subscriptions, including ones that are disabled.
  azure_rm_subscription_info:
    all: True

- name: Get facts for subscriptions containing tags provided.
  azure_rm_subscription_info:
    tags:
        - testing
        - foo:bar
'''

RETURN = '''
subscriptions:
    description:
        - List of subscription dicts.
    returned: always
    type: list
    contains:
        display_name:
            description: Subscription display name.
            returned: always
            type: str
            sample: my-subscription
        fqid:
            description: Subscription fully qualified id.
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000000"
        subscription_id:
            description: Subscription guid.
            returned: always
            type: str
            sample: "00000000-0000-0000-0000-000000000000"
        state:
            description: Subscription state.
            returned: always
            type: str
            sample: "'Enabled' or 'Disabled'"
        tags:
            description: Tags assigned to resource group.
            returned: always
            type: dict
            sample: { "tag1": "value1", "tag2": "value2" }
        tenant_id:
            description: Subscription tenant id
            returned: always
            type: str
            sample: "00000000-0000-0000-0000-000000000000"
'''

try:
    from msrestazure.azure_exceptions import CloudError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

class AzureRMAccountInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
        )

        self.results = dict(
            changed=False,
            account_info=[]
        )

        super(AzureRMAccountInfo, self).__init__(self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False,
                                                      facts_module=True)

    def exec_module(self, **kwargs):

        result = []
        result = self.list_items()

        self.results['account_info'] = result
        return self.results

    def list_items(self):

        results = {}
        
        try:
            subscription_list_response = list(self.subscription_client.subscriptions.list())
        except CloudError as exc:
            self.fail("Failed to list all subscriptions - {0}".format(str(exc)))

        results['id'] = subscription_list_response[0].subscription_id
        results['tenant_id'] = subscription_list_response[0].tenant_id
        results['homeTenantId'] = subscription_list_response[0].tenant_id
        results['name'] = subscription_list_response[0].display_name
        results['state'] = subscription_list_response[0].state
        results['managedByTenants'] = self.get_managed_by_tenants_list(subscription_list_response[0].managed_by_tenants)

        return results

    def get_managed_by_tenants_list(self, object_list):

        result = []
        
        for item in object_list:
            result.append({"tenantId": item.tenant_id })

        return result

def main():
    AzureRMAccountInfo()


if __name__ == '__main__':
    main()
