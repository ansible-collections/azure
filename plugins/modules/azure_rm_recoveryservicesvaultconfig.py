#!/usr/bin/python
#
# Copyright (c) 2025 Klaas Demter (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_recoveryservicesvaultconfig
version_added: "3.4.0"
short_description: Set Azure Backup Vault Config
description:
    - Get Azure Backup Vault Config
    - Most of the information here is also part of azure_rm_recoveryservicesvault
    - it's seperated out because of https://github.com/Azure/azure-rest-api-specs/issues/34218
    - A vault config has to exist, so you can not change the state, you can only change values, only if they are overwriteable
    - Supports diff mode
    - Check mode assumes all changes you make are legal and accepted by the API

options:
    vault_name:
        description:
            - The name of the Recovery Services Vault the vault config belongs to.
        required: true
        type: str
    resource_group:
        description:
            - The name of the resource group the vault is in.
        required: true
        type: str
    properties:
        description:
            - The recovery service vault config properties.
            - https://learn.microsoft.com/en-us/python/api/azure-mgmt-recoveryservicesbackup/
              azure.mgmt.recoveryservicesbackup.activestamp.models.backupresourcevaultconfig?view=azure-python
        type: dict
        suboptions:
            enhanced_security_state:
                description:
                    - Soft delete and security settings for hybrid workloads
                    - Enables soft delete, MFA and alert notifications for workloads running on premises.
                    - Refer to https://learn.microsoft.com/en-us/azure/backup/backup-azure-security-feature#minimum-version-requirements
                    - for minimum version requirements
                    - Can be reverted, unless set to AlwaysON
                type: str
                choices:
                    - Disabled
                    - Enabled
                    - AlwaysON
            soft_delete_feature_state:
                description:
                    - Enables soft delete for cloud workloads
                    - https://learn.microsoft.com/en-us/azure/backup/backup-azure-enhanced-soft-delete-about#whats-enhanced-soft-delete
                    - Can be reverted, unless set to AlwaysON
                type: str
                choices:
                    - Disabled
                    - Enabled
                    - AlwaysON
            soft_delete_retention_period_in_days:
                description:
                    - Duration of soft delete state
                    - minimum 14 days
                    - maximum 180 days
                type: int
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Klaas Demter (@Klaas-)
'''

EXAMPLES = '''
- name: Set backup vault config soft delete retention time
  azure.azcollection.azure_rm_recoveryservicesvaultconfig:
    vault_name: Vault_Name
    resource_group: Resource_Group_Name
    properties:
      soft_delete_retention_period_in_days: 17

- name: Set backup vault config soft delete to always on for cloud and hybrid workloads (not reversible except by deleting vault)
  azure.azcollection.azure_rm_recoveryservicesvaultconfig:
    vault_name: Vault_Name
    resource_group: Resource_Group_Name
    properties:
      soft_delete_feature_state: AlwaysON
      enhanced_security_state: AlwaysON
'''

RETURN = '''
id:
    description:
        - Id of specified backup vault config.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.RecoveryServices/vaults/Vault_Name/backupconfig/vaultconfig"
name:
    description:
        - always returns "vaultconfig"
    type: str
    returned: always
    sample: "vaultconfig"
type:
    description:
        - Type of backup vault config.
    type: str
    returned: always
    sample: "Microsoft.RecoveryServices/vaults/backupconfig"
properties:
    description:
        - Attributes of the backup vault config.
    type: dict
    returned: always
    sample: {
            "enhanced_security_state": "Enabled",
            "is_soft_delete_feature_state_editable": true,
            "soft_delete_feature_state": "Enabled",
            "soft_delete_retention_period_in_days": 14
        }
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError

except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBackupVaultConfig(AzureRMModuleBaseExt):
    """Information class for an Azure RM Backup Vault Configs"""

    def __init__(self):
        self.module_arg_spec = dict(
            vault_name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            properties=dict(
                type='dict',
                options=dict(
                    enhanced_security_state=dict(type='str', choices=['Disabled', 'Enabled', 'AlwaysON']),
                    soft_delete_feature_state=dict(type='str', choices=['Disabled', 'Enabled', 'AlwaysON']),
                    soft_delete_retention_period_in_days=dict(type='int')
                )
            )
        )

        self.vault_name = None
        self.resource_group = None
        self.properties = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            id=None,
            changed=False,
            diff=dict(
                before=None,
                after=None
            )
        )

        super(AzureRMBackupVaultConfig, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        existing_backup_vault_config_object = None
        existing_backup_vault_config = None

        existing_backup_vault_config_object = self.get_vault_config()

        if existing_backup_vault_config_object:
            existing_backup_vault_config = self.serialize_obj(existing_backup_vault_config_object, 'BackupResourceVaultConfigResource')

        if existing_backup_vault_config:
            self.log("Vault exists, update config")
            result_compare = dict(compare=[])

            # This is a workaround because PATCH does not support sending just the values you want to update
            # https://github.com/Azure/azure-rest-api-specs/issues/34530
            update_backup_vault_config = dict(
                properties=self.properties
            )
            merged_backup_vault_config = existing_backup_vault_config.copy()
            # This may need to be moved to a deep merge if future options are not flat
            merged_backup_vault_config['properties'] = {**existing_backup_vault_config['properties'], **update_backup_vault_config['properties']}

            if not self.default_compare({}, merged_backup_vault_config, existing_backup_vault_config, '', result_compare):
                self.log("Properties update existing vault config")
                if self.check_mode:
                    self.log("Check mode, not actually updating")
                    self.set_results(merged_backup_vault_config, True, existing_backup_vault_config)
                else:
                    self.log("Updating Vault config")
                    updated_backup_vault_config = self.serialize_obj(self.set_vault_config(merged_backup_vault_config), 'BackupResourceVaultConfigResource')
                    self.set_results(updated_backup_vault_config, True, existing_backup_vault_config)
            else:
                self.log("Properties do not update existing vault config")
                self.set_results(existing_backup_vault_config, False, existing_backup_vault_config)
        else:
            self.log("Vault does not exist")
            self.fail("Vault {0} does not exist in resource group {1}, failing".format(self.vault_name, self.resource_group))

        return self.results

    def get_vault_config(self):
        '''
        Gets the properties of the specified backup vault config.
        https://learn.microsoft.com/en-us/python/api/azure-mgmt-recoveryservicesbackup/azure.mgmt.recoveryservicesbackup.activestamp.aio.operations.backupresourcevaultconfigsoperations?view=azure-python

        :return: BackupResourceVaultConfigResource
        '''
        self.log("Checking for vault config of vault {0} in resource group {1}".format(self.vault_name, self.resource_group))

        vault_config = None

        try:
            vault_config = self.recovery_services_backup_client.backup_resource_vault_configs.get(vault_name=self.vault_name,
                                                                                                  resource_group_name=self.resource_group)
        except ResourceNotFoundError as ex:
            self.log("Could not find vault {0} in resource group {1}".format(self.vault_name, self.resource_group))

        return vault_config

    def set_vault_config(self, merged_backup_vault_config):
        '''
        Sets the properties of the specified backup vault config.
        https://learn.microsoft.com/en-us/python/api/azure-mgmt-recoveryservicesbackup/azure.mgmt.recoveryservicesbackup.activestamp.aio.operations.backupresourcevaultconfigsoperations?view=azure-python

        :return: BackupResourceVaultConfigResource
        '''
        self.log("Updating vault config of vault {0} in resource group {1}".format(self.vault_name, self.resource_group))

        vault_config = None

        try:
            vault_config = self.recovery_services_backup_client.backup_resource_vault_configs.update(vault_name=self.vault_name,
                                                                                                     resource_group_name=self.resource_group,
                                                                                                     parameters=merged_backup_vault_config)
        except ResourceNotFoundError as ex:
            self.log("Could not find vault {0} in resource group {1}".format(self.vault_name, self.resource_group))

        return vault_config

    def set_results(self, vault_config, changed=False, before=None):
        if vault_config:
            self.results['id'] = vault_config['id']
            # Not properly returned by sdk nor API
            # https://github.com/Azure/azure-rest-api-specs/issues/34530#issuecomment-2862950321
            # self.results['location'] = vault_config['location']
            self.results['name'] = vault_config['name']
            self.results['type'] = vault_config['type']
            self.results['properties'] = vault_config['properties']
            self.results['changed'] = changed
            self.results['diff']['before'] = before
            self.results['diff']['after'] = vault_config

        else:
            self.results['id'] = None
            self.results['name'] = None
            self.results['type'] = None


def main():
    """Main execution"""
    AzureRMBackupVaultConfig()


if __name__ == '__main__':
    main()
