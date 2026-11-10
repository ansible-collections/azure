#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_dataprotectionbackuppolicydisk_info
version_added: "4.3.0"
short_description: Get Azure Disk Backup policy facts
description:
    - Get facts of Azure Disk Backup policies (Microsoft.DataProtection).
    - Only policies for Azure managed disks (C(Microsoft.Compute/disks)) are returned.

options:
    resource_group:
        description:
            - The name of the resource group to which the Backup vault belongs.
        required: True
        type: str
    vault_name:
        description:
            - The name of the Backup vault the policy belongs to.
        required: True
        type: str
    name:
        description:
            - The name of the backup policy.
            - When omitted, all Disk Backup policies in the vault are returned.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Get Disk Backup policy by name
  azure_rm_dataprotectionbackuppolicydisk_info:
    resource_group: myResourceGroup
    vault_name: mybackupvault
    name: mydiskbackuppolicy

- name: List Disk Backup policies in a vault
  azure_rm_dataprotectionbackuppolicydisk_info:
    resource_group: myResourceGroup
    vault_name: mybackupvault
'''

RETURN = '''
backuppolicies:
    description: List of Disk Backup policies.
    returned: always
    type: list
    contains:
        id:
            description:
                - Resource ID of the backup policy.
            returned: always
            type: str
            sample: >-
                /subscriptions/xxxx-xxxx/resourceGroups/myRG/providers/Microsoft.DataProtection/backupVaults/myvault/backupPolicies/mypolicy
        name:
            description:
                - Name of the backup policy.
            returned: always
            type: str
            sample: mydiskbackuppolicy
        backup_repeating_time_intervals:
            description:
                - ISO 8601 repeating time intervals that define the backup schedule.
            returned: always
            type: list
            elements: str
            sample: ["R/2024-01-01T00:00:00+00:00/P1D"]
        time_zone:
            description:
                - Time zone used by the backup schedule.
            returned: always
            type: str
            sample: UTC
        default_retention_duration:
            description:
                - ISO 8601 duration for which backups are retained when no retention rule applies.
            returned: always
            type: str
            sample: P7D
        retention_rules:
            description:
                - Additional retention rules of the policy.
            returned: always
            type: list
            elements: dict
            contains:
                name:
                    description:
                        - Name of the retention rule.
                    type: str
                    sample: Weekly
                duration:
                    description:
                        - ISO 8601 duration for which matching backups are retained.
                    type: str
                    sample: P30D
                priority:
                    description:
                        - Priority of the rule. A lower value is evaluated first.
                    type: int
                    sample: 20
                absolute_criteria:
                    description:
                        - Selects which backups the rule applies to.
                    type: str
                    sample: FirstOfWeek
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
except ImportError:
    # This is handled in azure_rm_common
    pass

DISK_DATASOURCE_TYPE = 'Microsoft.Compute/disks'


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


class AzureRMDataProtectionBackupPolicyDiskInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            vault_name=dict(type='str', required=True),
            name=dict(type='str'),
        )

        self.resource_group = None
        self.vault_name = None
        self.name = None

        self.results = dict(changed=False)

        super(AzureRMDataProtectionBackupPolicyDiskInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        if self.name:
            self.results['backuppolicies'] = self.get_by_name()
        else:
            self.results['backuppolicies'] = self.list_by_vault()

        return self.results

    def get_by_name(self):
        self.log("Get the Backup policy {0}".format(self.name))
        results = []
        try:
            response = self.dataprotection_client.backup_policies.get(
                resource_group_name=self.resource_group, vault_name=self.vault_name, backup_policy_name=self.name)
            policy = policy_to_dict(response) if response else None
            if policy is not None:
                results.append(policy)
        except ResourceNotFoundError as e:
            self.log("Did not find the Backup policy {0}: {1}".format(self.name, str(e)))
        return results

    def list_by_vault(self):
        self.log("List Backup policies in vault {0}".format(self.vault_name))
        results = []
        try:
            response = list(self.dataprotection_client.backup_policies.list(
                resource_group_name=self.resource_group, vault_name=self.vault_name))
            for item in response:
                policy = policy_to_dict(item)
                if policy is not None:
                    results.append(policy)
        except ResourceNotFoundError as e:
            self.log("Did not find Backup policies in vault {0}: {1}".format(self.vault_name, str(e)))
        except Exception as e:
            self.fail("Error listing Backup policies in vault {0}: {1}".format(self.vault_name, str(e)))
        return results


def main():
    AzureRMDataProtectionBackupPolicyDiskInfo()


if __name__ == '__main__':
    main()
