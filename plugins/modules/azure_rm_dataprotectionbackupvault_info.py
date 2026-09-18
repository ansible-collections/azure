#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang, (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_dataprotectionbackupvault_info
version_added: "4.1.0"
short_description: Get Azure Backup vault facts
description:
    - Get facts of Azure Backup vault (Microsoft.DataProtection).

options:
    resource_group:
        description:
            - The name of the resource group to which the backup vault belongs.
        type: str
    name:
        description:
            - The name of the backup vault.
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
- name: Get Backup vault by name
  azure_rm_dataprotectionbackupvault_info:
    resource_group: myResourceGroup
    name: mybackupvault

- name: List Backup vaults in a resource group
  azure_rm_dataprotectionbackupvault_info:
    resource_group: myResourceGroup

- name: List Backup vaults in current subscription
  azure_rm_dataprotectionbackupvault_info:
'''

RETURN = '''
backupvaults:
    description: List of Backup vaults.
    returned: always
    type: list
    contains:
        id:
            description:
                - Resource ID of the backup vault.
            returned: always
            type: str
            sample: /subscriptions/xxxx-xxxx/resourceGroups/myResourceGroup/providers/Microsoft.DataProtection/backupVaults/mybackupvault
        name:
            description:
                - Name of the backup vault.
            returned: always
            type: str
            sample: mybackupvault
        type:
            description:
                - Type of the resource.
            returned: always
            type: str
            sample: Microsoft.DataProtection/backupVaults
        location:
            description:
                - Location of the backup vault.
            returned: always
            type: str
            sample: eastus
        e_tag:
            description:
                - Optional ETag of the backup vault.
            returned: always
            type: str
        system_data:
            description:
                - Azure Resource Manager metadata containing createdBy and modifiedBy information.
            returned: always
            type: dict
        datastore_type:
            description:
                - Type of the data store.
            returned: always
            type: str
            sample: VaultStore
        redundancy:
            description:
                - Backup storage redundancy.
            returned: always
            type: str
            sample: LocallyRedundant
        storage_settings:
            description:
                - Raw list of storage settings entries as returned by the Azure Data Protection API.
            returned: always
            type: list
        provisioning_state:
            description:
                - Provisioning state of the backup vault.
            returned: always
            type: str
            sample: Succeeded
        resource_move_state:
            description:
                - Resource move state of the backup vault.
            returned: always
            type: str
        resource_move_details:
            description:
                - Resource move details of the backup vault.
            returned: always
            type: dict
        is_vault_protected_by_resource_guard:
            description:
                - Whether the vault is protected by a resource guard.
            returned: always
            type: bool
        secure_score:
            description:
                - Secure score of the backup vault.
            returned: always
            type: str
            sample: Maximum
        bcdr_security_level:
            description:
                - Security level of the backup vault.
            returned: always
            type: str
            sample: Good
        identity:
            description:
                - Managed identity of the backup vault.
            returned: always
            type: dict
        security_settings:
            description:
                - Security settings of the backup vault (soft-delete, immutability, encryption).
            returned: always
            type: dict
        feature_settings:
            description:
                - Feature settings of the backup vault (cross-subscription-restore, cross-region-restore).
            returned: always
            type: dict
        monitoring_settings:
            description:
                - Monitoring settings of the backup vault.
            returned: always
            type: dict
        cost_management_settings:
            description:
                - Cost management settings of the backup vault.
            returned: always
            type: dict
        resource_guard_operation_requests:
            description:
                - Resource guard operation requests on which LAC check will be performed.
            returned: always
            type: list
        replicated_regions:
            description:
                - Replicated regions of the backup vault.
            returned: always
            type: list
        tags:
            description:
                - Tags assigned to the backup vault.
            returned: always
            type: dict
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
except ImportError:
    # This is handled in azure_rm_common
    pass


def backupvault_to_dict(vault):
    vault_dict = as_attribute_dict(vault, exclude_readonly=False)
    properties = vault_dict.get('properties') or {}
    storage_settings = properties.get('storage_settings') or [{}]
    return dict(
        id=vault_dict.get('id'),
        name=vault_dict.get('name'),
        type=vault_dict.get('type'),
        location=vault_dict.get('location'),
        e_tag=vault_dict.get('e_tag'),
        system_data=vault_dict.get('system_data'),
        tags=vault_dict.get('tags'),
        identity=vault_dict.get('identity'),
        datastore_type=storage_settings[0].get('datastore_type'),
        redundancy=storage_settings[0].get('type'),
        storage_settings=properties.get('storage_settings'),
        provisioning_state=properties.get('provisioning_state'),
        resource_move_state=properties.get('resource_move_state'),
        resource_move_details=properties.get('resource_move_details'),
        is_vault_protected_by_resource_guard=properties.get('is_vault_protected_by_resource_guard'),
        secure_score=properties.get('secure_score'),
        bcdr_security_level=properties.get('bcdr_security_level'),
        security_settings=properties.get('security_settings'),
        feature_settings=properties.get('feature_settings'),
        monitoring_settings=properties.get('monitoring_settings'),
        cost_management_settings=properties.get('cost_management_settings'),
        resource_guard_operation_requests=properties.get('resource_guard_operation_requests'),
        replicated_regions=properties.get('replicated_regions'),
    )


class AzureRMDataProtectionBackupVaultInfo(AzureRMModuleBase):

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

        super(AzureRMDataProtectionBackupVaultInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        if self.name:
            if not self.resource_group:
                self.fail("resource_group is required when filtering by name")
            self.results['backupvaults'] = self.get_by_name()
        elif self.resource_group:
            self.results['backupvaults'] = self.list_by_resource_group()
        else:
            self.results['backupvaults'] = self.list_by_subscription()

        return self.results

    def get_by_name(self):
        self.log("Get the Backup vault {0}".format(self.name))
        results = []
        try:
            response = self.dataprotection_client.backup_vaults.get(resource_group_name=self.resource_group, vault_name=self.name)
            if response and self.has_tags(response.tags, self.tags):
                results.append(backupvault_to_dict(response))
        except ResourceNotFoundError as e:
            self.log("Did not find the Backup vault {0}: {1}".format(self.name, str(e)))
        return results

    def list_by_resource_group(self):
        self.log("List Backup vaults in resource group {0}".format(self.resource_group))
        results = []
        try:
            response = list(self.dataprotection_client.backup_vaults.get_in_resource_group(resource_group_name=self.resource_group))
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(backupvault_to_dict(item))
        except Exception as e:
            self.log("Did not find Backup vaults in resource group {0}: {1}".format(self.resource_group, str(e)))
        return results

    def list_by_subscription(self):
        self.log("List Backup vaults in current subscription")
        results = []
        try:
            response = list(self.dataprotection_client.backup_vaults.get_in_subscription())
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(backupvault_to_dict(item))
        except Exception as e:
            self.log("Did not find Backup vaults in current subscription: {0}".format(str(e)))
        return results


def main():
    """Main execution"""
    AzureRMDataProtectionBackupVaultInfo()


if __name__ == '__main__':
    main()
