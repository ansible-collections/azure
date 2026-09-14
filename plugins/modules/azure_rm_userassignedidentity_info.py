#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_userassignedidentity_info

version_added: "4.1.0"

short_description: Get user-assigned managed identity facts

description:
    - Get facts for a specified user-assigned managed identity or all user-assigned managed identities in a resource group or subscription.

options:
    resource_group:
        description:
            - Name of resource group.
        type: str
    name:
        description:
            - The name of the user-assigned identity.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Get facts for one user-assigned identity
  azure_rm_userassignedidentity_info:
    resource_group: myResourceGroup
    name: myIdentity

- name: Get facts for all user-assigned identities in a resource group
  azure_rm_userassignedidentity_info:
    resource_group: myResourceGroup

- name: Get facts for all user-assigned identities in a subscription
  azure_rm_userassignedidentity_info:
'''

RETURN = '''
userassignedidentities:
    description:
        - Gets a list of user-assigned identities.
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/
                   Microsoft.ManagedIdentity/userAssignedIdentities/myIdentity",
            "name": "myIdentity",
            "location": "eastus",
            "tenant_id": "72f98888-8666-4144-9199-2d7cd0111111",
            "principal_id": "72f98888-8666-4144-9199-2d7cd0222222",
            "client_id": "72f98888-8666-4144-9199-2d7cd0333333",
            "isolation_scope": "None",
            "system_data": {
                "created_at": "2026-08-31T03:12:08.743499Z",
                "created_by": "72f98888-8666-4144-9199-2d7cd0444444",
                "created_by_type": "User",
                "last_modified_at": "2026-08-31T03:12:08.743499Z",
                "last_modified_by": "72f98888-8666-4144-9199-2d7cd0444444",
                "last_modified_by_type": "User"
            },
            "tags": {},
            "type": "Microsoft.ManagedIdentity/userAssignedIdentities"
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMUserAssignedIdentityInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            tags=dict(type='list', elements='str'),
        )

        self.resource_group = None
        self.name = None
        self.tags = None

        self.results = dict(changed=False)

        super(AzureRMUserAssignedIdentityInfo, self).__init__(self.module_arg_spec,
                                                              supports_check_mode=True,
                                                              supports_tags=False,
                                                              facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name and not self.resource_group:
            self.fail("Parameter error: resource group required when filtering by name.")

        if self.name:
            results = self.get_item()
        elif self.resource_group:
            results = self.list_by_resource_group()
        else:
            results = self.list_by_subscription()

        self.results['userassignedidentities'] = [item for item in results if self.has_tags(item.get('tags'), self.tags)]

        return self.results

    def get_item(self):
        try:
            item = self.msi_client.user_assigned_identities.get(
                resource_group_name=self.resource_group,
                resource_name=self.name,
            )
            return [as_attribute_dict(item, exclude_readonly=False)]
        except ResourceNotFoundError:
            return []

    def list_by_resource_group(self):
        try:
            response = self.msi_client.user_assigned_identities.list_by_resource_group(self.resource_group)
            return [as_attribute_dict(item, exclude_readonly=False) for item in response]
        except ResourceNotFoundError as exc:
            self.fail("Failed to list user-assigned identities for resource group {0} - {1}".format(self.resource_group, str(exc)))

    def list_by_subscription(self):
        try:
            response = self.msi_client.user_assigned_identities.list_by_subscription()
            return [as_attribute_dict(item, exclude_readonly=False) for item in response]
        except ResourceNotFoundError as exc:
            self.fail("Failed to list user-assigned identities - {0}".format(str(exc)))


def main():
    AzureRMUserAssignedIdentityInfo()


if __name__ == '__main__':
    main()
