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
version_added: "1.4.0"
short_description: Manage Azure Backup Policy
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
    state:
        description:
            - Assert the state of the backup policy.
            - Use C(present) to create or update a backup policy and C(absent) to delete it.
        default: present
        choices:
            - absent
            - present
        type: str
    backup_management_type:
        description:
            - Defines the type of resource the policy will be applied to.
        choices:
            - AzureIaasVM
        type: str
    policy_type:
        description:
            - Defines the type of backup policy
        default: V1
        choices:
            - V1
            - V2
        type: str
    schedule_run_time:
        description:
            - The hour to run backups.
            - Valid choices are on 24 hour scale (0-23).
        type: int
    instant_recovery_snapshot_retention:
        description:
            - How many days to retain instant recovery snapshots.
        type: int
    schedule_run_frequency:
        description:
            - The frequency to run the policy.
        choices:
            - Daily
            - Weekly
        type: str
    schedule_days:
        description:
            - List of days to execute the schedule.
            - Does not apply to Daily frequency.
        type: list
        elements: str
    weekly_retention_count:
        description:
            - The amount of weeks to retain backups.
        type: int
    daily_retention_count:
        description:
            - The amount of days to retain backups.
            - Does not apply to Weekly frequency.
        type: int
    schedule_weekly_frequency:
        description:
            - The amount of weeks between backups.
            - Backup every I(schedule_weekly_frequency) week(s).
            - Azure will default behavior to running weekly if this is left blank.
            - Does not apply to Daily frequency.
        type: int
    time_zone:
        description:
            - Timezone to apply I(schedule_run_time).
        default: UTC
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Cole Neubauer(@coleneubauer)
'''

EXAMPLES = '''
- name: Delete a backup policy
  azure_rm_backuppolicy:
    vault_name: Vault_Name
    name: Policy_Name
    resource_group: Resource_Group_Name
    state: absent

- name: Create a daily VM backup policy
  azure_rm_backuppolicy:
    vault_name: Vault_Name
    name: Policy_Name
    resource_group: Resource_Group_Name
    state: present
    backup_management_type: "AzureIaasVM"
    schedule_run_frequency: "Daily"
    instant_recovery_snapshot_retention: 2
    daily_retention_count: 12
    time_zone: "Pacific Standard Time"
    schedule_run_time: 14

- name: Create a weekly VM backup policy
  azure.azcollection.azure_rm_backuppolicy:
    vault_name: Vault_Name
    name: Policy_Name
    resource_group: Resource_Group_Name
    state: present
    backup_management_type: "AzureIaasVM"
    schedule_run_frequency: "Weekly"
    instant_recovery_snapshot_retention: 5
    weekly_retention_count: 4
    schedule_days:
      - "Monday"
      - "Wednesday"
      - "Friday"
    time_zone: "Pacific Standard Time"
    schedule_run_time: 8

- name: Create daily enhanced policy
  azure.azcollection.azure_rm_backuppolicy:
    vault_name: Vault_Name
    name: Policy_Name_Enhanced
    resource_group: Resource_Group_Name
    policy_type: V2
    state: present
    backup_management_type: AzureIaasVM
    schedule_run_frequency: Daily
    instant_recovery_snapshot_retention: 7
    daily_retention_count: 28
    time_zone: UTC
    schedule_run_time: 20
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

from datetime import datetime
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError

except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBackupPolicy(AzureRMModuleBase):
    """Configuration class for an Azure RM Backup Policy"""

    def __init__(self):
        self.module_arg_spec = dict(
            vault_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            backup_management_type=dict(type='str', choices=['AzureIaasVM']),
            policy_type=dict(type='str', default='V1', choices=['V1', 'V2']),
            schedule_run_time=dict(type='int'),
            instant_recovery_snapshot_retention=dict(type='int'),
            schedule_run_frequency=dict(type='str', choices=['Daily', 'Weekly']),
            schedule_days=dict(type='list', elements='str'),
            weekly_retention_count=dict(type='int'),
            daily_retention_count=dict(type='int'),
            schedule_weekly_frequency=dict(type='int'),
            time_zone=dict(type='str', default='UTC'),
        )

        self.vault_name = None
        self.name = None
        self.resource_group = None
        self.backup_management_type = None
        self.policy_type = None
        self.schedule_run_time = None
        self.instant_recovery_snapshot_retention = None
        self.schedule_run_frequency = None
        self.schedule_days = None
        self.weekly_retention_count = None
        self.schedule_weekly_frequency = None
        self.daily_retention_count = None
        self.time_zone = None

        self.results = dict(
            changed=False,
            id=None,
        )

        required_if = [('schedule_run_frequency', 'Weekly', ['schedule_days', 'weekly_retention_count', 'schedule_run_time']),
                       ('schedule_run_frequency', 'Daily', ['daily_retention_count', 'schedule_run_time']),
                       ('state', 'present', ['schedule_run_frequency', 'backup_management_type']),
                       ('log_mode', 'file', ['log_path'])]

        super(AzureRMBackupPolicy, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False,
                                                  required_if=required_if)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        existing_backup_policy = None
        response = None

        old_res = self.get_backup_policy()

        # either create or update
        if self.state == 'present':
            # check if the backup policy exists
            if not old_res:
                self.log("Backup policy {0} for vault {1} in resource group {2} does not exist.".format(self.name,
                                                                                                        self.vault_name,
                                                                                                        self.resource_group))

                self.results['changed'] = True

                if self.check_mode:
                    return self.results

                response = self.create_or_update_backup_policy()
                self.results.update(self.set_results(response))

            # log that we're doing an update
            else:
                self.log("Backup policy {0} for vault {1} in resource group {2} already exists, updating".format(self.name,
                                                                                                                 self.vault_name,
                                                                                                                 self.resource_group))
                if self.schedule_run_frequency is not None and\
                   self.schedule_run_frequency != old_res['properties']['schedule_policy']['schedule_run_frequency']:
                    self.results['changed'] = True
                elif self.time_zone is not None and self.time_zone != old_res['properties']['time_zone']:
                    self.results['changed'] = True
                elif self.instant_recovery_snapshot_retention is not None and\
                        self.instant_recovery_snapshot_retention != old_res['properties']['instant_rp_retention_range_in_days']:
                    self.results['changed'] = True
                elif self.schedule_weekly_frequency is not None and\
                        self.schedule_weekly_frequency != old_res['properties']['schedule_policy']['schedule_weekly_frequency']:
                    self.results['changed'] = True
                if self.weekly_retention_count is not None:
                    if self.weekly_retention_count !=\
                       old_res['properties']['retention_policy'].get('weekly_schedule', {}).get('retention_duration', {}).get('count'):
                        self.results['changed'] = True
                if self.daily_retention_count is not None:
                    if self.daily_retention_count !=\
                       old_res['properties']['retention_policy'].get('daily_schedule', {}).get('retention_duration', {}).get('count'):
                        self.results['changed'] = True
                if self.schedule_days is not None:
                    if old_res['properties']['schedule_policy'].get('schedule_run_days') is not None:
                        if set(self.schedule_days) != set(old_res['properties']['schedule_policy']['schedule_run_days']):
                            self.results['changed'] = True
                    else:
                        self.results['changed'] = True

                if self.check_mode:
                    self.results.update(old_res)
                    self.results['changed'] = True
                    return self.results
                else:
                    if self.results['changed']:
                        response = self.create_or_update_backup_policy()
                        self.results.update(self.set_results(response))
                    else:
                        self.results.update(old_res)

        elif self.state == 'absent':
            if old_res:
                self.log("Delete backup policy")
                self.results['changed'] = True

                if self.check_mode:
                    self.results.update(old_res)
                    return self.results

                self.delete_backup_policy()

                self.log('backup policy deleted')

            else:
                # If backup policy doesn't exist, that's the desired state.
                self.log("Backup policy {0} for vault {1} in resource group {2} does not exist.".format(self.name,
                                                                                                        self.vault_name,
                                                                                                        self.resource_group))

        return self.results

    def create_or_update_backup_policy(self):
        '''
        Creates or updates backup policy.

        :return: ProtectionPolicyResource
        '''
        self.log("Creating backup policy {0} for vault {1} in resource group {2}".format(self.name,
                                                                                         self.vault_name,
                                                                                         self.resource_group))
        self.log("Creating backup policy in progress")

        response = None

        try:
            instant_rp_details = None
            # need to represent the run time as a date_time
            # year, month, day has no impact on run time but is more consistent to see it as the time of creation rather than hardcoded value
            dt = datetime.utcnow()
            dt = datetime(dt.year, dt.month, dt.day, 0, 0)

            # azure requires this as a list but at this time doesn't support multiple run times
            # should easily be converted at this step if they support it in the future
            schedule_run_times_as_datetimes = []
            schedule_run_time = self.schedule_run_time

            # basic parameter checking. try to provide a better description of faults than azure does at this time
            try:
                if 0 <= schedule_run_time <= 23:
                    schedule_run_times_as_datetimes = [(dt.replace(hour=schedule_run_time))]
                else:
                    raise ValueError('Paramater schedule_run_time {0} is badly formed must be on the 24 hour scale'.format(schedule_run_time))
                # azure forces instant_recovery_snapshot_retention to be 5 when schedule type is Weekly
                if self.schedule_run_frequency == "Weekly" and self.instant_recovery_snapshot_retention != 5:
                    raise ValueError('Paramater instant_recovery_snapshot_retention was {0} but must be 5 when schedule_run_frequency is Weekly'
                                     .format(self.instant_recovery_snapshot_retention))

                if self.schedule_run_frequency == "Weekly" and not (1 <= self.weekly_retention_count <= 5163):
                    raise ValueError('Paramater weekly_retention_count was {0} but must be between 1 and 5163 when schedule_run_frequency is Weekly'
                                     .format(self.weekly_retention_count))

                if self.schedule_run_frequency == "Daily" and not (7 <= self.daily_retention_count <= 9999):
                    raise ValueError('Paramater daily_retention_count was {0} but must be between 7 and 9999 when schedule_run_frequency is Daily'
                                     .format(self.daily_retention_count))

            except ValueError as e:
                self.results['changed'] = False
                self.fail(e)

            # create a schedule policy based on schedule_run_frequency
            if self.policy_type == 'V1':
                schedule_policy = self.recovery_services_backup_models.SimpleSchedulePolicy(schedule_run_frequency=self.schedule_run_frequency,
                                                                                            schedule_run_days=self.schedule_days,
                                                                                            schedule_run_times=schedule_run_times_as_datetimes,
                                                                                            schedule_weekly_frequency=self.schedule_weekly_frequency)
            elif self.policy_type == 'V2':
                schedule_policy = self.recovery_services_backup_models.SimpleSchedulePolicyV2(
                    schedule_run_frequency=self.schedule_run_frequency, daily_schedule=self.recovery_services_backup_models.WeeklySchedule(
                        schedule_run_days=self.schedule_days, schedule_run_times=schedule_run_times_as_datetimes))

            daily_retention_schedule = None
            weekly_retention_schedule = None

            # Daily backups can have a daily retention or weekly but Weekly backups cannot have a daily retention
            if (self.daily_retention_count and self.schedule_run_frequency == "Daily"):
                retention_duration = self.recovery_services_backup_models.RetentionDuration(count=self.daily_retention_count, duration_type="Days")
                daily_retention_schedule = self.recovery_services_backup_models.DailyRetentionSchedule(retention_times=schedule_run_times_as_datetimes,
                                                                                                       retention_duration=retention_duration)

            if (self.weekly_retention_count):
                retention_duration = self.recovery_services_backup_models.RetentionDuration(count=self.weekly_retention_count,
                                                                                            duration_type="Weeks")
                weekly_retention_schedule = self.recovery_services_backup_models.WeeklyRetentionSchedule(days_of_the_week=self.schedule_days,
                                                                                                         retention_times=schedule_run_times_as_datetimes,
                                                                                                         retention_duration=retention_duration)

            retention_policy = self.recovery_services_backup_models.LongTermRetentionPolicy(daily_schedule=daily_retention_schedule,
                                                                                            weekly_schedule=weekly_retention_schedule)

            policy_definition = None

            if self.backup_management_type == "AzureIaasVM":
                # This assignment exists exclusively to deal with the following line being too long otherwise
                AzureIaaSVMProtectionPolicy = self.recovery_services_backup_models.AzureIaaSVMProtectionPolicy
                policy_definition = AzureIaaSVMProtectionPolicy(instant_rp_details=instant_rp_details,
                                                                schedule_policy=schedule_policy,
                                                                retention_policy=retention_policy,
                                                                instant_rp_retention_range_in_days=self.instant_recovery_snapshot_retention,
                                                                time_zone=self.time_zone,
                                                                policy_type=self.policy_type)

            if policy_definition:
                policy_resource = self.recovery_services_backup_models.ProtectionPolicyResource(properties=policy_definition)
                response = self.recovery_services_backup_client.protection_policies.create_or_update(vault_name=self.vault_name,
                                                                                                     resource_group_name=self.resource_group,
                                                                                                     policy_name=self.name,
                                                                                                     parameters=policy_resource)

        except Exception as e:
            self.log('Error attempting to create the backup policy.')
            self.fail("Error creating the backup policy {0} for vault {1} in resource group {2}. Error Reads: {3}".format(self.name,
                                                                                                                          self.vault_name,
                                                                                                                          self.resource_group, e))

        return response

    def delete_backup_policy(self):
        '''
        Deletes specified backup policy.

        :return: ProtectionPolicyResource
        '''
        self.log("Deleting the backup policy {0} for vault {1} in resource group {2}".format(self.name, self.vault_name, self.resource_group))

        response = None

        try:
            response = self.recovery_services_backup_client.protection_policies.begin_delete(vault_name=self.vault_name,
                                                                                             resource_group_name=self.resource_group,
                                                                                             policy_name=self.name)

        except Exception as e:
            self.log('Error attempting to delete the backup policy.')
            self.fail("Error deleting the backup policy {0} for vault {1} in resource group {2}. Error Reads: {3}".format(self.name,
                                                                                                                          self.vault_name,
                                                                                                                          self.resource_group, e))

        return response

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

        return self.set_results(policy)

    def set_results(self, policy):
        result = dict()
        if policy:
            result['id'] = policy.id
            result['location'] = policy.location
            result['name'] = policy.name
            result['type'] = policy.type
            result['properties'] = policy.properties.as_dict()
            return result
        else:
            return None


def main():
    """Main execution"""
    AzureRMBackupPolicy()


if __name__ == '__main__':
    main()
