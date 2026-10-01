#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang, (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_dataprotectionbackupinstancedisk_info
version_added: "4.2.0"
short_description: Get Azure Disk Backup instance facts
description:
    - Get facts of Azure Disk Backup instance (Microsoft.DataProtection).

options:
    resource_group:
        description:
            - The name of the resource group to which the backup vault belongs.
        required: True
        type: str
    vault_name:
        description:
            - The name of the Backup vault the instance belongs to.
        required: True
        type: str
    name:
        description:
            - The name of the backup instance.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Get Disk Backup instance by name
  azure_rm_dataprotectionbackupinstancedisk_info:
    resource_group: myResourceGroup
    vault_name: mybackupvault
    name: mydiskbackupinstance

- name: List Disk Backup instances in a vault
  azure_rm_dataprotectionbackupinstancedisk_info:
    resource_group: myResourceGroup
    vault_name: mybackupvault
'''

RETURN = '''
backupinstances:
    description: List of Disk Backup instances.
    returned: always
    type: list
    contains:
        id:
            description:
                - Resource ID of the backup instance.
            returned: always
            type: str
        name:
            description:
                - Name of the backup instance.
            returned: always
            type: str
        disk_id:
            description:
                - Resource ID of the protected disk.
            returned: always
            type: str
        backup_policy_id:
            description:
                - Resource ID of the backup policy applied to the instance.
            returned: always
            type: str
        current_protection_state:
            description:
                - Current protection state of the backup instance.
            returned: always
            type: str
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
except ImportError:
    # This is handled in azure_rm_common
    pass


def backupinstance_to_dict(instance):
    instance_dict = as_attribute_dict(instance, exclude_readonly=False)
    properties = instance_dict.get('properties', {}) or {}
    data_source_info = properties.get('data_source_info', {}) or {}
    policy_info = properties.get('policy_info', {}) or {}
    return dict(
        id=instance_dict.get('id'),
        name=instance_dict.get('name'),
        disk_id=data_source_info.get('resource_id'),
        backup_policy_id=policy_info.get('policy_id'),
        current_protection_state=properties.get('current_protection_state'),
    )


class AzureRMDataProtectionBackupInstanceDiskInfo(AzureRMModuleBase):
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

        super(AzureRMDataProtectionBackupInstanceDiskInfo, self).__init__(
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
            self.results['backupinstances'] = self.get_by_name()
        else:
            self.results['backupinstances'] = self.list_by_vault()

        return self.results

    def get_by_name(self):
        self.log("Get the Backup instance {0}".format(self.name))
        results = []
        try:
            response = self.dataprotection_client.backup_instances.get(
                resource_group_name=self.resource_group, vault_name=self.vault_name, backup_instance_name=self.name)
            if response:
                results.append(backupinstance_to_dict(response))
        except ResourceNotFoundError as e:
            self.log("Did not find the Backup instance {0}: {1}".format(self.name, str(e)))
        return results

    def list_by_vault(self):
        self.log("List Backup instances in vault {0}".format(self.vault_name))
        results = []
        try:
            response = list(self.dataprotection_client.backup_instances.list(
                resource_group_name=self.resource_group, vault_name=self.vault_name))
            for item in response:
                results.append(backupinstance_to_dict(item))
        except Exception as e:
            self.log("Did not find Backup instances in vault {0}: {1}".format(self.vault_name, str(e)))
        return results


def main():
    AzureRMDataProtectionBackupInstanceDiskInfo()


if __name__ == '__main__':
    main()
