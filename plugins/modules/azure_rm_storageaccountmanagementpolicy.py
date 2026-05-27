#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_storageaccountmanagementpolicy
version_added: "2.4.0"
short_description: Manage storage account management policies
description:
    - Create, update or delete storage account management policies.
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
            - Name of the storage account.
        type: str
        required: true
    rules:
        description:
            - The Storage Account ManagementPolicies Rules.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of the policy rule.
                    - A rule name can contain any combination of alpha numeric characters.
                type: str
                required: true
            type:
                description:
                    - The type of the policy rule.
                type: str
                required: true
                choices:
                    - Lifecycle
            enabled:
                description:
                    - Whether to enabled the rule
                type: bool
            definition:
                description:
                    - Whether to enabled the rule
                required: true
                type: dict
                suboptions:
                    actions:
                        description:
                            - An object that defines the action set.
                        type: dict
                        required: true
                        suboptions:
                            base_blob:
                                description:
                                    - The management policy action for base blob.
                                type: dict
                                suboptions:
                                    tier_to_cool:
                                        description:
                                            - The function to tier blobs to cool storage.
                                            - Support blobs currently at Hot tier.
                                        type: dict
                                        suboptions:
                                            days_after_modification_greater_than:
                                                description:
                                                    - Value indicating the age in days after last modification.
                                                type: float
                                            days_after_last_access_time_greater_than:
                                                description:
                                                    - This property can only be used in conjunction with last access time tracking policy.
                                                type: float
                                    tier_to_archive:
                                        description:
                                            - The function to tier blobs to archive storage.
                                            - Support blobs currently at Hot or Cool tier.
                                        type: dict
                                        suboptions:
                                            days_after_modification_greater_than:
                                                description:
                                                    - Value indicating the age in days after last modification.
                                                type: float
                                            days_after_last_access_time_greater_than:
                                                description:
                                                    - This property can only be used in conjunction with last access time tracking policy.
                                                type: float
                                    delete:
                                        description:
                                            - The function to delete the blob.
                                        type: dict
                                        suboptions:
                                            days_after_modification_greater_than:
                                                description:
                                                    - Value indicating the age in days after last modification.
                                                type: float
                                            days_after_last_access_time_greater_than:
                                                description:
                                                    - This property can only be used in conjunction with last access time tracking policy.
                                                type: float
                                    enable_auto_tier_to_hot_from_cool:
                                        description:
                                            - This property enables auto tiering of a blob from cool to hot on a blob access.
                                        type: bool
                            snapshot:
                                description:
                                    - The management policy action for snapshot.
                                type: dict
                                suboptions:
                                    tier_to_cool:
                                        description:
                                            - The function to tier blob snapshot to cool storage.
                                            - Support blob snapshot at Hot tier.
                                        type: dict
                                        suboptions:
                                            days_after_creation_greater_than:
                                                description:
                                                    - Value indicating the age in days after creation.
                                                type: float
                                                required: true
                                    tier_to_archive:
                                        description:
                                            - The function to tier blob snapshot to archive storage.
                                            - Support blob snapshot currently at Hot or Cool tier.
                                        type: dict
                                        suboptions:
                                            days_after_creation_greater_than:
                                                description:
                                                    - Value indicating the age in days after creation.
                                                type: float
                                                required: true
                                    delete:
                                        description:
                                            - The function to delete the blob snapshot.
                                        type: dict
                                        suboptions:
                                            days_after_creation_greater_than:
                                                description:
                                                    - Value indicating the age in days after creation.
                                                type: float
                                                required: true
                            version:
                                description:
                                    - The management policy action for version.
                                type: dict
                                suboptions:
                                    tier_to_cool:
                                        description:
                                            - The function to tier blob version to cool storage.
                                            - Support blob version currently at Hot tier.
                                        type: dict
                                        suboptions:
                                            days_after_creation_greater_than:
                                                description:
                                                    - Value indicating the age in days after creation.
                                                type: float
                                                required: true
                                    tier_to_archive:
                                        description:
                                            - The function to tier blob version to archive storage.
                                            - Support blob version currently at Hot or Cool tier.
                                        type: dict
                                        suboptions:
                                            days_after_creation_greater_than:
                                                description:
                                                    - Value indicating the age in days after creation.
                                                type: float
                                                required: true
                                    delete:
                                        description:
                                            - The function to delete the blob version.
                                        type: dict
                                        suboptions:
                                            days_after_creation_greater_than:
                                                description:
                                                    - Value indicating the age in days after creation.
                                                type: float
                                                required: true
                    filters:
                        description:
                            - An object that defines the filter set.
                        type: dict
                        suboptions:
                            prefix_match:
                                description:
                                    - An array of strings for prefixes to be match.
                                type: list
                                elements: str
                            blob_types:
                                description:
                                    - An array of predefined enum values.
                                    - Currently blockBlob supports all tiering and delete actions. Only delete actions are supported for C(appendBlob).
                                type: list
                                required: true
                                elements: str
                                choices:
                                    - blockBlob
                                    - appendBlob
                            blob_index_match:
                                description:
                                    - An array of blob index tag based filters, there can be at most 10 tag filters.
                                type: list
                                elements: dict
                                suboptions:
                                    name:
                                        description:
                                            - This is the filter tag name, it can have 1 - 128 characters.
                                        type: str
                                        required: true
                                    op:
                                        description:
                                            - This is the comparison operator which is used for object comparison and filtering.
                                            - Only C(==) (equality operator) is currently supported.
                                        type: str
                                        required: true
                                    value:
                                        description:
                                            - This is the filter tag value field used for tag based filtering.
                                            - It can have 0-256 characters.
                                        type: str
                                        required: true
    state:
        description:
            - State of the storage account managed policy. Use C(present) add or update the policy rule.
            - Use C(absent) to delete all policy rules.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Create storage account management policy with multi parameters
  azure_rm_storageaccountmanagementpolicy:
    resource_group: testRG
    storage_account_name: testaccount
    rules:
      - name: olcmtest5
        type: Lifecycle
        enabled: false
        definition:
          actions:
            base_blob:
              enable_auto_tier_to_hot_from_cool: true
              delete:
                days_after_modification_greater_than: 33
                days_after_last_access_time_greater_than: 33
              tier_to_cool:
                days_after_modification_greater_than: 33
                days_after_last_access_time_greater_than: 33
              tier_to_archive:
                days_after_modification_greater_than: 33
                days_after_last_access_time_greater_than: 33
            snapshot:
              tier_to_cool:
                days_after_creation_greater_than: 33
              tier_to_archive:
                days_after_creation_greater_than: 33
              delete:
                days_after_creation_greater_than: 33
            version:
              tier_to_archive:
                days_after_creation_greater_than: 33
              tier_to_cool:
                days_after_creation_greater_than: 33
              delete:
                days_after_creation_greater_than: 33
          filters:
            prefix_match:
              - olcmtestcontainer2
            blob_types:
              - blockBlob
              - appendBlob
            blob_index_match:
              - name: tags3
                op: '=='
                value: value3

- name: Delete management policy rules
  azure_rm_storageaccountmanagementpolicy:
    resource_group: "{{ resource_group }}"
    storage_account_name: "st{{ rpfx }}"
    state: absent
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


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible.module_utils.common.dict_transformations import snake_dict_to_camel_dict
try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
except Exception:
    # This is handled in azure_rm_common
    pass


class AzureRMStorageAccountManagementPolicy(AzureRMModuleBaseExt):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(required=True, type='str', aliases=['resource_group_name']),
            storage_account_name=dict(type='str', required=True),
            state=dict(default='present', choices=['present', 'absent']),
            rules=dict(
                type='list',
                elements='dict',
                options=dict(
                    enabled=dict(type='bool'),
                    name=dict(type='str', required=True),
                    type=dict(type='str', required=True, choices=['Lifecycle']),
                    definition=dict(
                        type='dict',
                        required=True,
                        options=dict(
                            actions=dict(
                                type='dict',
                                required=True,
                                options=dict(
                                    base_blob=dict(
                                        type='dict',
                                        options=dict(
                                            tier_to_cool=dict(
                                                type='dict',
                                                options=dict(
                                                    days_after_modification_greater_than=dict(type='float'),
                                                    days_after_last_access_time_greater_than=dict(type='float')
                                                )
                                            ),
                                            tier_to_archive=dict(
                                                type='dict',
                                                options=dict(
                                                    days_after_modification_greater_than=dict(type='float'),
                                                    days_after_last_access_time_greater_than=dict(type='float')
                                                )
                                            ),
                                            delete=dict(
                                                type='dict',
                                                options=dict(
                                                    days_after_modification_greater_than=dict(type='float'),
                                                    days_after_last_access_time_greater_than=dict(type='float')
                                                )
                                            ),
                                            enable_auto_tier_to_hot_from_cool=dict(type='bool')
                                        )
                                    ),
                                    snapshot=dict(
                                        type='dict',
                                        options=dict(
                                            tier_to_cool=dict(
                                                type='dict',
                                                options=dict(
                                                    days_after_creation_greater_than=dict(type='float', required=True)
                                                )
                                            ),
                                            tier_to_archive=dict(
                                                type='dict',
                                                options=dict(
                                                    days_after_creation_greater_than=dict(type='float', required=True)
                                                )
                                            ),
                                            delete=dict(
                                                type='dict',
                                                options=dict(
                                                    days_after_creation_greater_than=dict(type='float', required=True)
                                                )
                                            )
                                        )
                                    ),
                                    version=dict(
                                        type='dict',
                                        options=dict(
                                            tier_to_cool=dict(
                                                type='dict',
                                                options=dict(
                                                    days_after_creation_greater_than=dict(
                                                        type='float',
                                                        required=True
                                                    )
                                                )
                                            ),
                                            tier_to_archive=dict(
                                                type='dict',
                                                options=dict(
                                                    days_after_creation_greater_than=dict(
                                                        type='float',
                                                        required=True
                                                    )
                                                )
                                            ),
                                            delete=dict(
                                                type='dict',
                                                options=dict(
                                                    days_after_creation_greater_than=dict(
                                                        type='float',
                                                        required=True
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            ),
                            filters=dict(
                                type='dict',
                                options=dict(
                                    prefix_match=dict(type='list', elements='str'),
                                    blob_types=dict(type='list', elements='str', choices=['blockBlob', 'appendBlob'], required=True),
                                    blob_index_match=dict(
                                        type='list',
                                        elements='dict',
                                        options=dict(
                                            name=dict(type='str', required=True),
                                            op=dict(type='str', required=True),
                                            value=dict(type='str', required=True)
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )

        self.results = dict(
            changed=False,
            state=dict()
        )

        self.resource_group = None
        self.storage_account_name = None
        self.state = None
        self.rules = []

        super(AzureRMStorageAccountManagementPolicy, self).__init__(self.module_arg_spec,
                                                                    supports_tags=False,
                                                                    supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        managed_policy = self.get_management_policy()
        changed = False

        if self.state == 'present':
            if managed_policy is not None:
                rules = []
                for item in managed_policy['policy']['rules']:
                    rules.append(item)
                rules_name = [item['name'] for item in rules]
                for item in self.rules:
                    if item['name'] in rules_name:
                        for tt in managed_policy['policy']['rules']:
                            if item['name'] == tt['name']:
                                old_item = tt
                                if not self.default_compare({}, item, old_item, '', dict(compare=[])):
                                    rules.remove(old_item)
                                    rules.append(item)
                                    changed = True
                    else:
                        rules.append(item)
                        changed = True
                if changed and not self.check_mode:
                    self.create_or_update_management_policy(rules)
            else:
                changed = True
                if not self.check_mode:
                    self.create_or_update_management_policy(self.rules)
        else:
            if managed_policy is not None:
                changed = True
                if not self.check_mode:
                    self.delete_management_policy()

        self.results['state'] = self.get_management_policy()
        self.results['changed'] = changed

        return self.results

    def get_management_policy(self):
        self.log('Get info for storage account management policy')

        response = None
        try:
            response = self.storage_client.management_policies.get(self.resource_group, self.storage_account_name, 'default')
        except ResourceNotFoundError as ec:
            self.log("Failed to obtain the storage acount management policy, detail as {0}".format(ec))
            return None
        return self.format_to_dict(response)

    def create_or_update_management_policy(self, rules):
        self.log("Creating or updating storage account mangement policy")

        try:
            self.storage_client.management_policies.create_or_update(
                resource_group_name=self.resource_group,
                account_name=self.storage_account_name,
                management_policy_name='default',
                properties={'properties': {'policy': {'rules': [snake_dict_to_camel_dict(rule) for rule in rules]}}})
        except Exception as e:
            self.log('Error creating or updating storage account management policy.')
            self.fail("Failed to create or updating storage account management policy: {0}".format(str(e)))
        return self.get_management_policy()

    def delete_management_policy(self):
        try:
            self.storage_client.management_policies.delete(self.resource_group, self.storage_account_name, 'default')
        except Exception as e:
            self.fail("Failed to delete the storage account management policy: {0}".format(str(e)))

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
    AzureRMStorageAccountManagementPolicy()


if __name__ == '__main__':
    main()
