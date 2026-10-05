#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_dataprotectionbackupinstancedisk
version_added: "4.2.0"
short_description: Manage Azure Disk Backup instance (Microsoft.DataProtection)
description:
    - Configure or remove backup protection for an Azure managed disk under a Backup vault.
    - The Backup vault must have a system-assigned or user-assigned managed identity granted
      C(Disk Snapshot Contributor) on the snapshot resource group and C(Disk Backup Reader) on the disk
      before this module can succeed.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: True
    name:
        description:
            - The name of the backup instance.
        type: str
        required: True
    vault_name:
        description:
            - The name of the Backup vault the instance belongs to.
        type: str
        required: True
    location:
        description:
            - Azure location. Defaults to the resource group's location.
        type: str
    friendly_name:
        description:
            - A friendly name for the backup instance.
        type: str
    disk_id:
        description:
            - The resource ID of the Azure managed disk to protect.
            - Required when I(state=present).
        type: str
    backup_policy_id:
        description:
            - The resource ID of the Disk Backup policy to apply.
            - Required when I(state=present).
        type: str
    snapshot_resource_group:
        description:
            - The name of the resource group where disk snapshots are stored.
            - Defaults to the disk's own resource group when not specified.
            - Must be in the same subscription as I(disk_id); cross-subscription snapshot storage is not
              supported by the Azure Backup service.
        type: str
    identity:
        description:
            - Identity used by this backup instance to perform data operations. This identity must
              already be assigned to the Backup vault, and must be granted
              C(Disk Snapshot Contributor) on the snapshot resource group and C(Disk Backup Reader) on
              the disk.
        type: dict
        suboptions:
            type:
                description:
                    - Type of the managed identity to use.
                    - When not specified, the current identity is left unchanged (or Azure's own
                      system-assigned default applies on first creation).
                choices:
                    - SystemAssigned
                    - UserAssigned
                type: str
            user_assigned_identity:
                description:
                    - The resource ID of the user-assigned managed identity to use.
                    - Required when I(identity.type=UserAssigned).
                type: str
    state:
        description:
            - Use C(present) to create or update and C(absent) to delete.
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
- name: Configure backup for a managed disk
  azure_rm_dataprotectionbackupinstancedisk:
    resource_group: myResourceGroup
    vault_name: mybackupvault
    name: mydiskbackupinstance
    location: eastus
    disk_id: /subscriptions/xxxx-xxxx/resourceGroups/myResourceGroup/providers/Microsoft.Compute/disks/mydisk
    backup_policy_id: >-
        /subscriptions/xxxx-xxxx/resourceGroups/myResourceGroup/providers/Microsoft.DataProtection/backupVaults/mybackupvault/backupPolicies/mydiskbackuppolicy

- name: Configure backup for a managed disk using a user-assigned identity
  azure_rm_dataprotectionbackupinstancedisk:
    resource_group: myResourceGroup
    vault_name: mybackupvault
    name: mydiskbackupinstance
    location: eastus
    disk_id: /subscriptions/xxxx-xxxx/resourceGroups/myResourceGroup/providers/Microsoft.Compute/disks/mydisk
    backup_policy_id: >-
        /subscriptions/xxxx-xxxx/resourceGroups/myResourceGroup/providers/Microsoft.DataProtection/backupVaults/mybackupvault/backupPolicies/mydiskbackuppolicy
    identity:
      type: UserAssigned
      user_assigned_identity: >-
          /subscriptions/xxxx-xxxx/resourceGroups/myResourceGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myuai

- name: Remove backup protection for a managed disk
  azure_rm_dataprotectionbackupinstancedisk:
    resource_group: myResourceGroup
    vault_name: mybackupvault
    name: mydiskbackupinstance
    state: absent
'''

RETURN = '''
id:
  description: The Azure Resource Manager resource ID for the backup instance.
  returned: always
  type: str
  sample: >-
      /subscriptions/xxxx-xxxx/resourceGroups/myResourceGroup/providers/Microsoft.DataProtection/backupVaults/mybackupvault/backupInstances/mydiskbackupinstance
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.polling import LROPoller
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.core.tools import parse_resource_id
    from azure.mgmt.dataprotection.models import (
        BackupInstanceResource, BackupInstance, Datasource, PolicyInfo, PolicyParameters,
        AzureOperationalStoreParameters, DataStoreTypes, IdentityDetails,
    )
except ImportError:
    # handled in azure_rm_common
    pass

DISK_DATASOURCE_TYPE = 'Microsoft.Compute/disks'


class Actions:
    NoAction, Create, Delete = range(3)


class AzureRMBackupInstance(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            vault_name=dict(type='str', required=True),
            location=dict(type='str'),
            friendly_name=dict(type='str'),
            disk_id=dict(type='str'),
            backup_policy_id=dict(type='str'),
            snapshot_resource_group=dict(type='str'),
            identity=dict(
                type='dict',
                options=dict(
                    type=dict(type='str', choices=['SystemAssigned', 'UserAssigned']),
                    user_assigned_identity=dict(type='str'),
                ),
            ),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.resource_group = None
        self.name = None
        self.vault_name = None
        self.location = None
        self.friendly_name = None
        self.disk_id = None
        self.backup_policy_id = None
        self.snapshot_resource_group = None
        self.identity = None
        self.state = None

        self.results = dict(changed=False)
        self.to_do = Actions.NoAction

        required_if = [('state', 'present', ['disk_id', 'backup_policy_id'])]

        super(AzureRMBackupInstance, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            required_if=required_if)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        old_response = self.get_backupinstancedisk()

        if old_response is None:
            if self.state == 'present':
                self.to_do = Actions.Create
        else:
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                properties = old_response.get('properties', {}) or {}
                properties_match = self.default_compare({}, self._desired_properties(), properties, '', dict(compare=[]))
                if not properties_match or not self._identity_matches(properties.get('identity_details')):
                    self.to_do = Actions.Create

        response = old_response
        if self.to_do == Actions.Create:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            current_identity_details = ((old_response or {}).get('properties', {}) or {}).get('identity_details')
            response = self.create_update_backupinstancedisk(current_identity_details)
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            self.delete_backupinstancedisk()
            response = None

        if response is not None:
            self.results['id'] = response.get('id')

        return self.results

    def _snapshot_resource_group_id(self):
        disk_identity = parse_resource_id(self.disk_id)
        subscription_id = disk_identity.get('subscription')
        resource_group = self.snapshot_resource_group or disk_identity.get('resource_group')
        return "/subscriptions/{0}/resourceGroups/{1}".format(subscription_id, resource_group)

    def _identity_details(self, current_identity_details=None):
        if self.identity is None:
            return current_identity_details
        if self.identity.get('type') != 'UserAssigned':
            return dict(use_system_assigned_identity=True, user_assigned_identity_arm_url=None)
        user_assigned_identity = self.identity.get('user_assigned_identity')
        if not user_assigned_identity:
            self.fail('identity.user_assigned_identity is required when identity.type is UserAssigned')
        return dict(
            use_system_assigned_identity=False,
            user_assigned_identity_arm_url=user_assigned_identity,
        )

    def _identity_matches(self, actual_identity_details):
        if self.identity is None:
            return True
        actual = actual_identity_details or {}
        desired = self._identity_details()
        if desired.get('use_system_assigned_identity'):
            return not actual.get('user_assigned_identity_arm_url')
        return (actual.get('use_system_assigned_identity') is False
                and actual.get('user_assigned_identity_arm_url') == desired['user_assigned_identity_arm_url'])

    def _desired_properties(self):
        properties = dict(
            friendly_name=self.friendly_name,
            data_source_info=dict(resource_id=self.disk_id),
            policy_info=dict(
                policy_id=self.backup_policy_id,
                policy_parameters=dict(
                    data_store_parameters_list=[
                        dict(resource_group_id=self._snapshot_resource_group_id())
                    ]
                ),
            ),
        )
        return properties

    def get_backupinstancedisk(self):
        try:
            response = self.dataprotection_client.backup_instances.get(
                resource_group_name=self.resource_group,
                vault_name=self.vault_name,
                backup_instance_name=self.name)
            return as_attribute_dict(response, exclude_readonly=False)
        except ResourceNotFoundError:
            return None

    def create_update_backupinstancedisk(self, current_identity_details=None):
        self.log("Configuring the Backup instance {0}".format(self.name))
        disk_name = parse_resource_id(self.disk_id).get('name')
        snapshot_resource_group_id = self._snapshot_resource_group_id()
        identity_details = self._identity_details(current_identity_details)
        if identity_details is not None:
            identity_details = IdentityDetails(**identity_details)

        parameters = BackupInstanceResource(
            properties=BackupInstance(
                object_type='BackupInstance',
                friendly_name=self.friendly_name,
                identity_details=identity_details,
                data_source_info=Datasource(
                    object_type='Datasource',
                    datasource_type=DISK_DATASOURCE_TYPE,
                    resource_id=self.disk_id,
                    resource_location=self.location,
                    resource_name=disk_name,
                    resource_type=DISK_DATASOURCE_TYPE,
                    resource_uri=self.disk_id,
                ),
                policy_info=PolicyInfo(
                    policy_id=self.backup_policy_id,
                    policy_parameters=PolicyParameters(
                        data_store_parameters_list=[
                            AzureOperationalStoreParameters(
                                data_store_type=DataStoreTypes.OPERATIONAL_STORE,
                                resource_group_id=snapshot_resource_group_id,
                            )
                        ]
                    ),
                ),
            )
        )
        try:
            poller = self.dataprotection_client.backup_instances.begin_create_or_update(
                resource_group_name=self.resource_group,
                vault_name=self.vault_name,
                backup_instance_name=self.name,
                parameters=parameters)
            if isinstance(poller, LROPoller):
                poller = self.get_poller_result(poller)
            return as_attribute_dict(poller, exclude_readonly=False)
        except Exception as exc:
            self.fail('Error creating/updating the Backup instance: {0}'.format(str(exc)))

    def delete_backupinstancedisk(self):
        try:
            poller = self.dataprotection_client.backup_instances.begin_delete(
                resource_group_name=self.resource_group,
                vault_name=self.vault_name,
                backup_instance_name=self.name)
            if isinstance(poller, LROPoller):
                self.get_poller_result(poller)
        except Exception as exc:
            self.fail('Error deleting the Backup instance: {0}'.format(str(exc)))


def main():
    """Main execution"""
    AzureRMBackupInstance()


if __name__ == '__main__':
    main()
