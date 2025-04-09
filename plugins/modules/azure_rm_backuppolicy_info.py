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
module: azure_rm_backuppolicy_info
version_added: "1.4.0"
short_description: Get Info on Azure Backup Policy
description:
    - Create and delete instance of Azure Backup Policy.

options:
    vault_name:
        description:
            - The name of the Recovery Services Vault the policy belongs to.
        required: true
        type: str
    name:
        description:
            - The name of the backup policy.
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
    - Cole Neubauer(@coleneubauer)
'''

EXAMPLES = '''
- name: Get backup policy information
  azure_rm_backuppolicy_info:
    vault_name: Vault_Name
    name: Policy_Name
    resource_group: Resource_Group_Name
  register: backup_policy
'''

RETURN = '''
id:
    description:
        - Id of specified backup policy.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.RecoveryServices/vaults/Vault_Name/backupPolicies/Policy_Name"
location:
    description:
        - Location of backup policy.
    type: str
    returned: always
    sample: eastus
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
properties:
    description:
        - Attributes of the backup policy.
    type: dict
    returned: always
    sample: {
                "backup_management_type": "AzureIaasVM",
                "instant_rp_details": {},
                "instant_rp_retention_range_in_days": 5,
                "protected_items_count": 0,
                "retention_policy": {
                    "retention_policy_type": "LongTermRetentionPolicy",
                    "weekly_schedule": {
                        "days_of_the_week": [
                            "Monday",
                            "Wednesday",
                            "Thursday"
                        ],
                        "retention_duration": {
                            "count": 4,
                            "duration_type": "Weeks"
                        },
                        "retention_times": [
                            "2025-04-09T10:00:00.000Z"
                        ]
                    }
                },
                "schedule_policy": {
                    "schedule_policy_type": "SimpleSchedulePolicy",
                    "schedule_run_days": [
                        "Monday",
                        "Wednesday",
                        "Thursday"
                    ],
                    "schedule_run_frequency": "Weekly",
                    "schedule_run_times": [
                        "2025-04-09T10:00:00.000Z"
                    ],
                    "schedule_weekly_frequency": 0
                },
                "time_zone": "Pacific Standard Time"
            }
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError

except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBackupPolicyInfo(AzureRMModuleBase):
    """Information class for an Azure RM Backup Policy"""

    def __init__(self):
        self.module_arg_spec = dict(
            vault_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
        )

        self.vault_name = None
        self.name = None
        self.resource_group = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            id=None,
            changed=False
        )

        super(AzureRMBackupPolicyInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False,
                                                      facts_module=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        existing_backup_policy = None
        response = None

        existing_backup_policy = self.get_backup_policy()

        self.set_results(existing_backup_policy)

        return self.results

    def get_backup_policy(self):
        '''
        Gets the properties of the specified backup policy.

        :return: ProtectionPolicyResource
        '''
        self.log("Checking if the backup policy {0} for vault {1} in resource group {2} is present".format(self.name,
                                                                                                           self.vault_name,
                                                                                                           self.resource_group))

        policy = None

        try:
            policy = self.recovery_services_backup_client.protection_policies.get(vault_name=self.vault_name,
                                                                                  resource_group_name=self.resource_group,
                                                                                  policy_name=self.name)
        except ResourceNotFoundError as ex:
            self.log("Could not find backup policy {0} for vault {1} in resource group {2}".format(self.name, self.vault_name, self.resource_group))

        return policy

    def set_results(self, policy):
        if policy:
            self.results['id'] = policy.id
            self.results['location'] = policy.location
            self.results['name'] = policy.name
            self.results['type'] = policy.type
            self.results['properties'] = policy.properties.as_dict()

        else:
            self.results['id'] = None
            self.results['location'] = None
            self.results['name'] = None
            self.results['type'] = None


def main():
    """Main execution"""
    AzureRMBackupPolicyInfo()


if __name__ == '__main__':
    main()
