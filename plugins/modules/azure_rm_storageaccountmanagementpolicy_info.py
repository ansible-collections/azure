#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_storageaccountmanagementpolicy_info

version_added: "2.4.0"

short_description: Get the data policy rules associated with the specified storage account

description:
    - Get the data policy rules associated with the specified storage account.

options:
    resource_group:
        description:
            - Name of the resource group to use.
        required: true
        type: str
        aliases:
            - resource_group_name
    storage_account_name:
        description:
            - Name of the storage account to update or create.
        type: str
        required: true

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get the data policy rules associated with the specified storage account
  azure_rm_storageaccountmanagementpolicy_info:
    resource_group: myResourceGroup
    storage_account_name: testaccount
'''


RETURN = '''
state:
    description:
        - The data policy rules associated with the specified storage account.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The data policy's ID.
            returned: always
            type: str
            sample: "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.Storage/storageAccounts/sttest/managementPolicies/default"
        resource_group:
            description:
                - The resource group name.
            returned: always
            type: str
            sample: testRG
        storage_account_name:
            description:
                - The storage account name.
            returned: always
            type: str
            sample: teststname
        type:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: "Microsoft.Storage/storageAccounts/managementPolicies"
        last_modified_time:
            description:
                - Returns the date and time the ManagementPolicies was last modified.
            returned: always
            type: str
            sample: "2024-04-12T11:40:10.376465+00:00"
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: DefaultManagementPolicy
        policy:
            description:
                - The Storage Account ManagementPolicy.
            returned: always
            type: complex
            contains:
                rules:
                    description:
                        - The Storage Account ManagementPolicies Rules.
                    type: list
                    returned: always
                    sample: [
                    {
                        "definition": {
                            "actions": {
                                "base_blob": {
                                    "delete": {
                                        "days_after_last_access_time_greater_than": 33.0,
                                        "days_after_modification_greater_than": 33.0
                                    },
                                    "enable_auto_tier_to_hot_from_cool": true,
                                    "tier_to_archive": {
                                        "days_after_last_access_time_greater_than": 33.0,
                                        "days_after_modification_greater_than": 33.0
                                    },
                                    "tier_to_cool": {
                                        "days_after_last_access_time_greater_than": 33.0,
                                        "days_after_modification_greater_than": 33.0
                                    }
                                },
                                "snapshot": {
                                    "delete": {
                                        "days_after_creation_greater_than": 33.0
                                    },
                                    "tier_to_archive": {
                                        "days_after_creation_greater_than": 33.0
                                    },
                                    "tier_to_cool": {
                                        "days_after_creation_greater_than": 33.0
                                    }
                                },
                                "version": {
                                    "delete": {
                                        "days_after_creation_greater_than": 33.0
                                    },
                                    "tier_to_archive": {
                                        "days_after_creation_greater_than": 33.0
                                    },
                                    "tier_to_cool": {
                                        "days_after_creation_greater_than": 33.0
                                    }
                                }
                            },
                            "filters": {
                                "blob_index_match": [
                                    {
                                        "name": "tags3",
                                        "op": "==",
                                        "value": "value3"
                                    }
                                ],
                                "blob_types": [
                                    "blockBlob",
                                    "appendBlob"
                                ],
                                "prefix_match": [
                                    "olcmtestcontainer2"
                                ]
                            }
                        },
                        "enabled": false,
                        "name": "olcmtest5",
                        "type": "Lifecycle"
                    }
                ]
'''


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
except Exception:
    # This is handled in azure_rm_common
    pass


class AzureRMStorageAccountManagementPolicyInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(required=True, type='str', aliases=['resource_group_name']),
            storage_account_name=dict(type='str', required=True),
        )

        self.results = dict(
            changed=False,
            state=dict()
        )

        self.resource_group = None
        self.storage_account_name = None
        self.state = None
        self.rules = None

        super(AzureRMStorageAccountManagementPolicyInfo, self).__init__(self.module_arg_spec,
                                                                        supports_tags=False,
                                                                        supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self.results['state'] = self.get_management_policy()

        return self.results

    def get_management_policy(self):
        self.log('Get info for storage account management policy')

        response = None
        try:
            response = self.storage_client.management_policies.get(self.resource_group, self.storage_account_name, 'default')
        except ResourceNotFoundError as ec:
            self.log("Failed to obtain the storage acount management policy, detail as {0}".format(ec))
            return

        return self.format_to_dict(response)

    def format_to_dict(self, obj):
        result = dict()
        result['id'] = obj.id
        result['resource_group'] = self.resource_group
        result['storage_account_name'] = self.storage_account_name
        result['name'] = obj.name
        result['type'] = obj.type
        result['last_modified_time'] = obj.last_modified_time
        result['policy'] = dict(rules=[])
        if obj.policy is not None:
            result['policy'] = as_attribute_dict(obj.policy)

        return result


def main():
    AzureRMStorageAccountManagementPolicyInfo()


if __name__ == '__main__':
    main()
