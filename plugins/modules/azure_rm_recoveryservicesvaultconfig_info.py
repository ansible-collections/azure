#!/usr/bin/python
#
# Copyright (c) 2025 Klaas Demter (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_recoveryservicesvaultconfig_info
version_added: "3.4.0"
short_description: Get Info on Azure Backup Vault Configs
description:
    - Get Azure Backup Vault Config
    - Most of the information here is also part of azure_rm_recoveryservicesvault_info
    - it's seperated out because of https://github.com/Azure/azure-rest-api-specs/issues/34218

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
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Klaas Demter (@Klaas-)
'''

EXAMPLES = '''
- name: Get backup vault config information
  azure.azcollection.azure_rm_recoveryservicesvaultconfig_info:
    vault_name: Vault_Name
    resource_group: Resource_Group_Name
'''

RETURN = '''
id:
    description:
        - Id of specified backup vault config.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/yyyyyyyyy/
            providers/Microsoft.RecoveryServices/vaults/zzzzzzzzzz/backupconfig/vaultconfig"
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

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError

except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBackupVaultConfigInfo(AzureRMModuleBase):
    """Information class for an Azure RM Backup Vault Configs"""

    def __init__(self):
        self.module_arg_spec = dict(
            vault_name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
        )

        self.vault_name = None
        self.resource_group = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            id=None,
            changed=False
        )

        super(AzureRMBackupVaultConfigInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                           supports_check_mode=True,
                                                           supports_tags=False,
                                                           facts_module=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        existing_backup_vault_config = None
        response = None

        existing_backup_vault_config = self.get_vault_config()

        self.set_results(existing_backup_vault_config)

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

    def set_results(self, vault_config):
        if vault_config:
            self.results['id'] = vault_config.id
            # Not properly returned by sdk nor API
            # https://github.com/Azure/azure-rest-api-specs/issues/34530#issuecomment-2862950321
            # self.results['location'] = vault_config.location
            self.results['name'] = vault_config.name
            self.results['type'] = vault_config.type
            self.results['properties'] = vault_config.properties.as_dict()

        else:
            self.results['id'] = None
            self.results['name'] = None
            self.results['type'] = None


def main():
    """Main execution"""
    AzureRMBackupVaultConfigInfo()


if __name__ == '__main__':
    main()
