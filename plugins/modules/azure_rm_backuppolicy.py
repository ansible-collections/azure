#!/usr/bin/python
#
# Copyright (c) 2020 Cole Neubauer, (@coleneubauer)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_backuppolicy
version_added: "#.#.#"
short_description: Manage Azure Backup Policy
description:
    - Create and delete instance of Azure Backup Policy.

options:
    vault_name:
        description:
            - The name of the Recovery Services Vault the policy belongs to.
            - Required
    policy_name:
        description:
            - The name of the backup policy.
            - Required
    resource_group_name:
        description:
            - The name of the resource group the vault is in.
            - Required
    state:
        description:
            - Assert the state of the backup policy.
            - Use C(present) to create or update a backup policy and C(absent) to delete it.
        default: present
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Cole Neubauer(@coleneubauer)

'''

EXAMPLES = '''
    - name: Delete a backup policy
      azure_rm_backuppolicy:
        vault_name: Vault_Name
        policy_name: Policy_Name
        resource_group_name: Resource_Group_Name
'''

RETURN = '''
id:
    description:
        - Id of specified backup policy.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.RecoveryServices/vaults/Vault_Name/backupPolicies/Policy_Name"
name:
    description:
        - Name of backup policy.
    type: str
    returned: always
    sample: DefaultPolicy
type:
    description:
        - Type of backup policy.
    type: str
    returned: always
    sample: Microsoft.RecoveryServices/vaults/backupPolicies
'''

import uuid
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError

except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBackupPolicy(AzureRMModuleBase):
    """Configuration class for an Azure RM Backup Policy"""

    def __init__(self):
        self.module_arg_spec = dict(
            vault_name=dict(type='str'),
            policy_name=dict(type='str'),
            resource_group_name=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent'])
        )

        self.vault_name = None
        self.policy_name = None
        self.resource_group_name = None

        self.results = dict(
            changed=False,
            id=None,
        )

        mutually_exclusive = []
        required_one_of = []
        required_if = []

        super(AzureRMBackupPolicy, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False,
                                                    required_one_of=required_one_of,
                                                    required_if=required_if,
                                                    mutually_exclusive=mutually_exclusive)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        existing_backup_policy = None
        response = None

        existing_backup_policy = self.get_backup_policy()

        if existing_backup_policy:
            self.set_results(existing_backup_policy)

        if self.state == 'present':
            # check if the backup policy exists
            if not existing_backup_policy:
                self.log("Backup policy {0} for vault {1} in resource group {2} does not exist.".format( self.policy_name, self.vault_name, self.resource_group_name ))

                self.results['changed'] = True

                if self.check_mode:
                    return self.results

                response = self.create_backup_policy()
                self.set_results(response)

            else:
                self.log("Backup policy already exists, not updatable")
                self.log('Result: {0}'.format(existing_backup_policy))

        elif self.state == 'absent':
            if existing_backup_policy:
                self.log("Delete backup policy")
                self.results['changed'] = True

                if self.check_mode:
                    return self.results

                self.delete_backup_policy()

                self.log('backup policy deleted')

            else:
                # If backup policy doesn't exist, that's the desired state.
                self.log("Backup policy {0} for vault {1} in resource group {2} does not exist.".format( self.policy_name, self.vault_name, self.resource_group_name ))

        return self.results

    def create_backup_policy(self):
        '''
        Creates backup policy.

        :return: ProtectionPolicyResource
        '''
        self.log("Creating backup policy {0} for vault {1} in resource group {2}".format( self.policy_name, self.vault_name, self.resource_group_name ))
        self.log("Creating backup policy not implemented")

        return True

    def delete_backup_policy(self):
        '''
        Deletes specified backup policy.

        :return: bool true on success, else fail
        '''
        self.log("Deleting the backup policy {0} for vault {1} in resource group {2}".format( self.policy_name, self.vault_name, self.resource_group_name ))
        try:
            response = self.recovery_services_backup_client.protection_policies.delete( self.policy_name, self.vault_name, self.resource_group_name )
            return True

        except CloudError as e:
            self.log('Error attempting to delete the backup policy.')
            self.fail("Error deleting the backup policy {0} for vault {1} in resource group {2}".format( self.policy_name, self.vault_name, self.resource_group_name ))
            return False

    def get_backup_policy(self):
        '''
        Gets the properties of the specified backup policy.

        :return: ProtectionPolicyResource
        '''
        self.log("Checking if the backup policy {0} for vault {1} in resource group {2} is present".format( self.policy_name, self.vault_name, self.resource_group_name ))

        policy = None

        try:
            policy = self.recovery_services_backup_client.protection_policies.get( vault_name=self.vault_name, resource_group_name=self.resource_group_name, policy_name=self.policy_name )
        except CloudError as ex:
            self.log("Could not find backup policy {0} for vault {1} in resource group {2}".format( self.policy_name, self.vault_name, self.resource_group_name ))

        return policy

    def set_results(self, policy):
        self.results['id'] = policy.id
        self.results['name'] = policy.name
        self.results['type'] = policy.type

def main():
    """Main execution"""
    AzureRMBackupPolicy()


if __name__ == '__main__':
    main()
