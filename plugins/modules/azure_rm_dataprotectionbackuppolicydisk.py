#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_dataprotectionbackuppolicydisk
version_added: "4.3.0"
short_description: Manage Azure Disk Backup policy (Microsoft.DataProtection)
description:
    - Create or delete a Disk Backup policy in an Azure Backup vault.
    - The policy applies to Azure managed disks (C(Microsoft.Compute/disks)) using incremental backups
      stored in the operational datastore.
    - Azure does not support updating an existing policy. The module fails when a policy with the same name exists
      with different settings; create a policy with a new name instead.
    - A policy name that already exists for a different datasource type is rejected.

options:
    resource_group:
        description:
            - The name of the resource group to which the Backup vault belongs.
        type: str
        required: True
    vault_name:
        description:
            - The name of the Backup vault the policy belongs to.
        type: str
        required: True
    name:
        description:
            - The name of the backup policy.
        type: str
        required: True
    backup_repeating_time_intervals:
        description:
            - ISO 8601 repeating time intervals that define the backup schedule, for example C(R/2024-01-01T00:00:00+00:00/P1D).
            - Required when I(state=present).
        type: list
        elements: str
    time_zone:
        description:
            - The time zone used by I(backup_repeating_time_intervals), for example C(UTC).
        type: str
    default_retention_duration:
        description:
            - ISO 8601 duration for which backups are retained when no entry of I(retention_rules) applies, for example C(P7D).
            - Required when I(state=present).
        type: str
    retention_rules:
        description:
            - Additional retention rules. Backups matching the I(absolute_criteria) of a rule are retained for its I(duration).
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of the retention rule. C(Default) is reserved for I(default_retention_duration).
                type: str
                required: True
            duration:
                description:
                    - ISO 8601 duration for which matching backups are retained, for example C(P30D).
                type: str
                required: True
            priority:
                description:
                    - The retention tag priority of the rule. The default retention rule uses priority C(99).
                type: int
                required: True
            absolute_criteria:
                description:
                    - Selects which backups the rule applies to.
                type: str
                required: True
                choices:
                    - AllBackup
                    - FirstOfDay
                    - FirstOfWeek
                    - FirstOfMonth
                    - FirstOfYear
    state:
        description:
            - Assert the state of the backup policy.
            - Use C(present) to create the policy and C(absent) to delete it.
        type: str
        default: present
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Create a Disk Backup policy that backs up daily and keeps backups for 7 days
  azure_rm_dataprotectionbackuppolicydisk:
    resource_group: myResourceGroup
    vault_name: mybackupvault
    name: mydiskbackuppolicy
    backup_repeating_time_intervals:
      - "R/2024-01-01T00:00:00+00:00/P1D"
    time_zone: UTC
    default_retention_duration: P7D

- name: Create a policy that also keeps the first backup of each week for 30 days
  azure_rm_dataprotectionbackuppolicydisk:
    resource_group: myResourceGroup
    vault_name: mybackupvault
    name: mydiskbackuppolicyweekly
    backup_repeating_time_intervals:
      - "R/2024-01-01T00:00:00+00:00/P1D"
    time_zone: UTC
    default_retention_duration: P7D
    retention_rules:
      - name: Weekly
        duration: P30D
        priority: 20
        absolute_criteria: FirstOfWeek

- name: Delete a Disk Backup policy
  azure_rm_dataprotectionbackuppolicydisk:
    resource_group: myResourceGroup
    vault_name: mybackupvault
    name: mydiskbackuppolicy
    state: absent
'''

RETURN = '''
id:
    description:
        - The Azure Resource Manager resource ID of the backup policy.
    returned: when I(state=present), except in check mode when the policy would be created
    type: str
    sample: >-
        /subscriptions/xxxx-xxxx/resourceGroups/myRG/providers/Microsoft.DataProtection/backupVaults/myvault/backupPolicies/mypolicy
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.dataprotection.models import (
        BaseBackupPolicyResource, BackupPolicy, AzureBackupRule, AzureBackupParams, AzureRetentionRule,
        AbsoluteDeleteOption, DataStoreInfoBase, DataStoreTypes, BackupSchedule, ScheduleBasedTriggerContext,
        ScheduleBasedBackupCriteria, SourceLifeCycle, TaggingCriteria, RetentionTag,
    )
except ImportError:
    # handled in azure_rm_common
    pass

DISK_DATASOURCE_TYPE = 'Microsoft.Compute/disks'
DEFAULT_RULE_NAME = 'Default'


class Actions:
    NoAction, Create, Delete = range(3)


def _value(item):
    return getattr(item, 'value', item)


def policy_to_dict(policy):
    policy_dict = as_attribute_dict(policy, exclude_readonly=False)
    properties = policy_dict.get('properties', {}) or {}
    if DISK_DATASOURCE_TYPE not in (properties.get('datasource_types') or []):
        return None

    rules = properties.get('policy_rules') or []
    backup_rule = next((rule for rule in rules if rule.get('object_type') == 'AzureBackupRule'), {})
    trigger = backup_rule.get('trigger') or {}
    schedule = trigger.get('schedule') or {}
    tagging_criteria = dict(
        ((item.get('tag_info') or {}).get('tag_name'), item) for item in trigger.get('tagging_criteria') or [])

    default_retention_duration = None
    retention_rules = []
    for rule in rules:
        if rule.get('object_type') != 'AzureRetentionRule':
            continue
        lifecycles = rule.get('lifecycles') or [{}]
        duration = (lifecycles[0].get('delete_after') or {}).get('duration')
        if rule.get('is_default'):
            default_retention_duration = duration
            continue
        tagging = tagging_criteria.get(rule.get('name')) or {}
        markers = [_value(marker) for criteria in tagging.get('criteria') or [] for marker in criteria.get('absolute_criteria') or []]
        retention_rules.append(dict(
            name=rule.get('name'),
            duration=duration,
            priority=tagging.get('tagging_priority'),
            absolute_criteria=markers[0] if markers else None,
        ))

    return dict(
        id=policy_dict.get('id'),
        name=policy_dict.get('name'),
        backup_repeating_time_intervals=schedule.get('repeating_time_intervals') or [],
        time_zone=schedule.get('time_zone'),
        default_retention_duration=default_retention_duration,
        retention_rules=sorted(retention_rules, key=lambda rule: rule['name']),
    )


class AzureRMDataProtectionBackupPolicyDisk(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            vault_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            backup_repeating_time_intervals=dict(type='list', elements='str'),
            time_zone=dict(type='str'),
            default_retention_duration=dict(type='str'),
            retention_rules=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(type='str', required=True),
                    duration=dict(type='str', required=True),
                    priority=dict(type='int', required=True),
                    absolute_criteria=dict(
                        type='str',
                        required=True,
                        choices=['AllBackup', 'FirstOfDay', 'FirstOfWeek', 'FirstOfMonth', 'FirstOfYear'],
                    ),
                ),
            ),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.resource_group = None
        self.vault_name = None
        self.name = None
        self.backup_repeating_time_intervals = None
        self.time_zone = None
        self.default_retention_duration = None
        self.retention_rules = None
        self.state = None

        self.results = dict(changed=False)
        self.to_do = Actions.NoAction

        required_if = [('state', 'present', ['backup_repeating_time_intervals', 'default_retention_duration'])]

        super(AzureRMDataProtectionBackupPolicyDisk, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            required_if=required_if)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        self.retention_rules = self.retention_rules or []
        rule_names = [rule['name'] for rule in self.retention_rules]
        if DEFAULT_RULE_NAME in rule_names or len(set(rule_names)) != len(rule_names):
            self.fail("retention_rules names must be unique and must not be '{0}'".format(DEFAULT_RULE_NAME))

        old_response = self.get_policy()

        if old_response is None:
            if self.state == 'present':
                self.to_do = Actions.Create
        else:
            current = policy_to_dict(old_response)
            if current is None:
                self.fail("The backup policy {0} exists but is not a Disk Backup policy".format(self.name))
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif not self.policy_matches(current):
                self.fail("The backup policy {0} already exists with different settings and Azure does not support updating "
                          "an existing policy. Create a policy with a new name instead.".format(self.name))

        response = old_response
        if self.to_do == Actions.Create:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.create_policy()
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            self.delete_policy()
            response = None

        if response is not None:
            self.results['id'] = response.id

        return self.results

    def policy_matches(self, current):
        desired = dict(
            backup_repeating_time_intervals=self.backup_repeating_time_intervals,
            time_zone=self.time_zone,
            default_retention_duration=self.default_retention_duration,
            retention_rules=sorted(self.retention_rules, key=lambda rule: rule['name']),
        )
        return self.default_compare({}, desired, current, '', dict(compare=[]))

    def build_policy(self):
        def data_store():
            return DataStoreInfoBase(data_store_type=DataStoreTypes.OPERATIONAL_STORE, object_type='DataStoreInfoBase')

        def retention_rule(name, duration, is_default):
            return AzureRetentionRule(
                name=name,
                object_type='AzureRetentionRule',
                is_default=is_default,
                lifecycles=[
                    SourceLifeCycle(
                        delete_after=AbsoluteDeleteOption(duration=duration, object_type='AbsoluteDeleteOption'),
                        source_data_store=data_store(),
                    )
                ],
            )

        tagging_criteria = [
            TaggingCriteria(
                is_default=True,
                tagging_priority=99,
                tag_info=RetentionTag(tag_name=DEFAULT_RULE_NAME),
            )
        ]
        policy_rules = []
        for rule in self.retention_rules:
            tagging_criteria.append(TaggingCriteria(
                is_default=False,
                tagging_priority=rule['priority'],
                tag_info=RetentionTag(tag_name=rule['name']),
                criteria=[
                    ScheduleBasedBackupCriteria(
                        object_type='ScheduleBasedBackupCriteria',
                        absolute_criteria=[rule['absolute_criteria']],
                    )
                ],
            ))
            policy_rules.append(retention_rule(rule['name'], rule['duration'], False))

        backup_rule = AzureBackupRule(
            name='BackupIntervals',
            object_type='AzureBackupRule',
            backup_parameters=AzureBackupParams(backup_type='Incremental', object_type='AzureBackupParams'),
            data_store=data_store(),
            trigger=ScheduleBasedTriggerContext(
                object_type='ScheduleBasedTriggerContext',
                schedule=BackupSchedule(
                    repeating_time_intervals=self.backup_repeating_time_intervals,
                    time_zone=self.time_zone,
                ),
                tagging_criteria=tagging_criteria,
            ),
        )
        policy_rules = [backup_rule, retention_rule(DEFAULT_RULE_NAME, self.default_retention_duration, True)] + policy_rules

        return BaseBackupPolicyResource(
            properties=BackupPolicy(
                object_type='BackupPolicy',
                datasource_types=[DISK_DATASOURCE_TYPE],
                policy_rules=policy_rules,
            )
        )

    def get_policy(self):
        try:
            return self.dataprotection_client.backup_policies.get(
                resource_group_name=self.resource_group,
                vault_name=self.vault_name,
                backup_policy_name=self.name)
        except ResourceNotFoundError:
            return None

    def create_policy(self):
        self.log("Creating the Backup policy {0}".format(self.name))
        try:
            return self.dataprotection_client.backup_policies.create_or_update(
                resource_group_name=self.resource_group,
                vault_name=self.vault_name,
                backup_policy_name=self.name,
                parameters=self.build_policy())
        except Exception as exc:
            self.fail('Error creating the Backup policy: {0}'.format(str(exc)))

    def delete_policy(self):
        self.log("Deleting the Backup policy {0}".format(self.name))
        try:
            self.dataprotection_client.backup_policies.delete(
                resource_group_name=self.resource_group,
                vault_name=self.vault_name,
                backup_policy_name=self.name)
        except Exception as exc:
            self.fail('Error deleting the Backup policy: {0}'.format(str(exc)))


def main():
    """Main execution"""
    AzureRMDataProtectionBackupPolicyDisk()


if __name__ == '__main__':
    main()
