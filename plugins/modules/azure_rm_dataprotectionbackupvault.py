#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang, (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_dataprotectionbackupvault
version_added: "4.1.0"
short_description: Manage Azure Backup vault (Microsoft.DataProtection)
description:
    - Create, update and delete an Azure Backup vault used by the Azure Data Protection service.

options:
    resource_group:
        description:
            - The name of the resource group to which the backup vault belongs.
        required: True
        type: str
    name:
        description:
            - The name of the backup vault.
        required: True
        type: str
    location:
        description:
            - Azure Resource location. If not set, location from the resource group will be used as default.
        type: str
    datastore_type:
        description:
            - Specifies the type of the data store.
            - Cannot be changed after the backup vault has been created.
        type: str
        choices:
            - ArchiveStore
            - OperationalStore
            - VaultStore
        default: VaultStore
    redundancy:
        description:
            - Specifies the backup storage redundancy.
            - Cannot be changed after the backup vault has been created.
        type: str
        choices:
            - GeoRedundant
            - LocallyRedundant
            - ZoneRedundant
        default: LocallyRedundant
    security_settings:
        description:
            - Security settings of the backup vault.
        type: dict
        suboptions:
            soft_delete_settings:
                description:
                    - Soft delete related settings.
                type: dict
                suboptions:
                    state:
                        description:
                            - State of soft delete.
                            - C(AlwaysOn) cannot be reverted once set.
                        type: str
                        choices:
                            - "Off"
                            - "On"
                            - AlwaysOn
                    retention_duration_in_days:
                        description:
                            - Soft delete retention duration in days. Valid range is 14 to 180.
                        type: float
            immutability_settings:
                description:
                    - Immutability settings at vault level.
                type: dict
                suboptions:
                    state:
                        description:
                            - Immutability state.
                            - C(Locked) cannot be reverted once set.
                        type: str
                        choices:
                            - Disabled
                            - Unlocked
                            - Locked
            encryption_settings:
                description:
                    - Customer managed key (CMK) settings of the backup vault.
                type: dict
                suboptions:
                    state:
                        description:
                            - Encryption state of the backup vault.
                        type: str
                        choices:
                            - Enabled
                            - Disabled
                    infrastructure_encryption:
                        description:
                            - Enabling or disabling double (infrastructure) encryption.
                        type: str
                        choices:
                            - Enabled
                            - Disabled
                    key_vault_properties:
                        description:
                            - Properties of the Key Vault which hosts the CMK.
                        type: dict
                        suboptions:
                            key_uri:
                                description:
                                    - The key URI of the customer managed key.
                                type: str
                    kek_identity:
                        description:
                            - The managed identity used for the CMK.
                        type: dict
                        suboptions:
                            identity_type:
                                description:
                                    - The identity type used to access the Key Vault.
                                type: str
                                choices:
                                    - SystemAssigned
                                    - UserAssigned
                            identity_id:
                                description:
                                    - Resource ID of the user assigned managed identity (required when I(identity_type=UserAssigned)).
                                type: str
    feature_settings:
        description:
            - Feature settings of the backup vault.
        type: dict
        suboptions:
            cross_subscription_restore_settings:
                description:
                    - Cross subscription restore settings.
                type: dict
                suboptions:
                    state:
                        description:
                            - Cross subscription restore state.
                            - C(PermanentlyDisabled) cannot be reverted once set.
                        type: str
                        choices:
                            - Disabled
                            - PermanentlyDisabled
                            - Enabled
            cross_region_restore_settings:
                description:
                    - Cross region restore settings.
                    - Only valid when I(redundancy=GeoRedundant). Once enabled it cannot be disabled.
                type: dict
                suboptions:
                    state:
                        description:
                            - Cross region restore state.
                        type: str
                        choices:
                            - Disabled
                            - Enabled
    monitoring_settings:
        description:
            - Monitoring settings of the backup vault.
        type: dict
        suboptions:
            azure_monitor_alert_settings:
                description:
                    - Settings for Azure Monitor based alerts.
                type: dict
                suboptions:
                    alerts_for_all_job_failures:
                        description:
                            - Enable or disable Azure Monitor alerts for all job failures.
                        type: str
                        choices:
                            - Enabled
                            - Disabled
    cost_management_settings:
        description:
            - Cost management settings of the backup vault.
        type: dict
        suboptions:
            granularity_level:
                description:
                    - Granularity level for cost management.
                type: str
                choices:
                    - VaultLevel
                    - ProtectedItemLevel
                    - ProtectedItemWithParentTag
    resource_guard_operation_requests:
        description:
            - Resource guard operation requests on which LAC (least-access-control) check will be performed.
        type: list
        elements: str
    replicated_regions:
        description:
            - List of replicated regions for the backup vault.
        type: list
        elements: str
    state:
        description:
            - Assert the state of the backup vault.
            - Use C(present) to create or update a backup vault and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
    - azure.azcollection.azure_identity_multiple

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Create a Backup vault with a minimal configuration
  azure_rm_dataprotectionbackupvault:
    resource_group: myResourceGroup
    name: mybackupvault
    location: eastus
    datastore_type: VaultStore
    redundancy: LocallyRedundant
    identity:
      type: SystemAssigned
    tags:
      env: test

- name: Update Backup vault security, feature, monitoring and cost settings
  azure_rm_dataprotectionbackupvault:
    resource_group: myResourceGroup
    name: mybackupvault
    location: eastus
    datastore_type: VaultStore
    redundancy: GeoRedundant
    security_settings:
      soft_delete_settings:
        state: "On"
        retention_duration_in_days: 30
      immutability_settings:
        state: Unlocked
      encryption_settings:
        state: Enabled
        infrastructure_encryption: Enabled
        key_vault_properties:
          key_uri: https://mykeyvault.vault.azure.net/keys/mykey/1234
        kek_identity:
          identity_type: UserAssigned
          identity_id: /subscriptions/xxxx-xxxx/resourceGroups/myResourceGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myuai
    feature_settings:
      cross_subscription_restore_settings:
        state: Enabled
      cross_region_restore_settings:
        state: Enabled
    monitoring_settings:
      azure_monitor_alert_settings:
        alerts_for_all_job_failures: Enabled
    cost_management_settings:
      granularity_level: VaultLevel

- name: Delete a Backup vault
  azure_rm_dataprotectionbackupvault:
    resource_group: myResourceGroup
    name: mybackupvault
    state: absent
'''

RETURN = '''
id:
    description:
        - The Azure Resource Manager resource ID for the backup vault.
    returned: always
    type: str
    sample: /subscriptions/xxxx-xxxx/resourceGroups/myResourceGroup/providers/Microsoft.DataProtection/backupVaults/mybackupvault
'''

import copy

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.polling import LROPoller
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.dataprotection.models import (
        BackupVaultResource, BackupVault, StorageSetting, DppIdentityDetails, UserAssignedIdentity,
        SecuritySettings, SoftDeleteSettings, ImmutabilitySettings, EncryptionSettings,
        CmkKeyVaultProperties, CmkKekIdentity,
        FeatureSettings, CrossSubscriptionRestoreSettings, CrossRegionRestoreSettings,
        MonitoringSettings, AzureMonitorAlertSettings, CostManagementSettings,
    )
except ImportError:
    # This is handled in azure_rm_common
    pass


def _deep_merge(base, overrides):
    # PATCH does not support sending just the values you want to update, so merge requested
    # keys onto the existing settings, same workaround as azure_rm_recoveryservicesvaultconfig.
    # https://github.com/Azure/azure-rest-api-specs/issues/34530
    if overrides is None:
        return copy.deepcopy(base) if isinstance(base, dict) else base
    if not isinstance(overrides, dict):
        return overrides
    result = copy.deepcopy(base) if isinstance(base, dict) else {}
    for key, value in overrides.items():
        if value is None:
            continue
        if isinstance(value, dict):
            result[key] = _deep_merge(result.get(key), value)
        else:
            result[key] = value
    return result


def _build_security_settings(payload):
    if not payload:
        return None
    kwargs = {}
    sd = payload.get('soft_delete_settings')
    if sd:
        kwargs['soft_delete_settings'] = SoftDeleteSettings(
            state=sd.get('state'),
            retention_duration_in_days=sd.get('retention_duration_in_days'),
        )
    im = payload.get('immutability_settings')
    if im:
        kwargs['immutability_settings'] = ImmutabilitySettings(state=im.get('state'))
    enc = payload.get('encryption_settings')
    if enc:
        enc_kwargs = dict(
            state=enc.get('state'),
            infrastructure_encryption=enc.get('infrastructure_encryption'),
        )
        kvp = enc.get('key_vault_properties')
        if kvp:
            enc_kwargs['key_vault_properties'] = CmkKeyVaultProperties(key_uri=kvp.get('key_uri'))
        kek = enc.get('kek_identity')
        if kek:
            enc_kwargs['kek_identity'] = CmkKekIdentity(
                identity_type=kek.get('identity_type'),
                identity_id=kek.get('identity_id'),
            )
        kwargs['encryption_settings'] = EncryptionSettings(**{k: v for k, v in enc_kwargs.items() if v is not None})
    return SecuritySettings(**kwargs) if kwargs else None


def _build_feature_settings(payload):
    if not payload:
        return None
    kwargs = {}
    csr = payload.get('cross_subscription_restore_settings')
    if csr:
        kwargs['cross_subscription_restore_settings'] = CrossSubscriptionRestoreSettings(state=csr.get('state'))
    crr = payload.get('cross_region_restore_settings')
    if crr:
        kwargs['cross_region_restore_settings'] = CrossRegionRestoreSettings(state=crr.get('state'))
    return FeatureSettings(**kwargs) if kwargs else None


def _build_monitoring_settings(payload):
    if not payload:
        return None
    ama = payload.get('azure_monitor_alert_settings')
    if not ama:
        return None
    return MonitoringSettings(
        azure_monitor_alert_settings=AzureMonitorAlertSettings(
            alerts_for_all_job_failures=ama.get('alerts_for_all_job_failures'),
        ),
    )


def _build_cost_management_settings(payload):
    if not payload:
        return None
    if payload.get('granularity_level') is None:
        return None
    return CostManagementSettings(granularity_level=payload['granularity_level'])


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDataProtectionBackupVault(AzureRMModuleBaseExt):
    """Configuration class for an Azure RM Backup vault resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            datastore_type=dict(
                type='str',
                choices=['ArchiveStore', 'OperationalStore', 'VaultStore'],
                default='VaultStore',
            ),
            redundancy=dict(
                type='str',
                choices=['GeoRedundant', 'LocallyRedundant', 'ZoneRedundant'],
                default='LocallyRedundant',
            ),
            identity=dict(
                type='dict',
                options=self.managed_identity_multiple_spec,
            ),
            security_settings=dict(
                type='dict',
                options=dict(
                    soft_delete_settings=dict(
                        type='dict',
                        options=dict(
                            state=dict(type='str', choices=['Off', 'On', 'AlwaysOn']),
                            retention_duration_in_days=dict(type='float'),
                        ),
                    ),
                    immutability_settings=dict(
                        type='dict',
                        options=dict(
                            state=dict(type='str', choices=['Disabled', 'Unlocked', 'Locked']),
                        ),
                    ),
                    encryption_settings=dict(
                        type='dict',
                        options=dict(
                            state=dict(type='str', choices=['Enabled', 'Disabled']),
                            infrastructure_encryption=dict(type='str', choices=['Enabled', 'Disabled']),
                            key_vault_properties=dict(
                                type='dict',
                                no_log=False,
                                options=dict(
                                    key_uri=dict(type='str', no_log=True),
                                ),
                            ),
                            kek_identity=dict(
                                type='dict',
                                options=dict(
                                    identity_type=dict(type='str', choices=['SystemAssigned', 'UserAssigned']),
                                    identity_id=dict(type='str'),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            feature_settings=dict(
                type='dict',
                options=dict(
                    cross_subscription_restore_settings=dict(
                        type='dict',
                        options=dict(
                            state=dict(type='str', choices=['Disabled', 'PermanentlyDisabled', 'Enabled']),
                        ),
                    ),
                    cross_region_restore_settings=dict(
                        type='dict',
                        options=dict(
                            state=dict(type='str', choices=['Disabled', 'Enabled']),
                        ),
                    ),
                ),
            ),
            monitoring_settings=dict(
                type='dict',
                options=dict(
                    azure_monitor_alert_settings=dict(
                        type='dict',
                        options=dict(
                            alerts_for_all_job_failures=dict(type='str', choices=['Enabled', 'Disabled']),
                        ),
                    ),
                ),
            ),
            cost_management_settings=dict(
                type='dict',
                options=dict(
                    granularity_level=dict(
                        type='str',
                        choices=['VaultLevel', 'ProtectedItemLevel', 'ProtectedItemWithParentTag'],
                    ),
                ),
            ),
            resource_guard_operation_requests=dict(type='list', elements='str'),
            replicated_regions=dict(type='list', elements='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.datastore_type = None
        self.redundancy = None
        self.identity = None
        self.security_settings = None
        self.feature_settings = None
        self.monitoring_settings = None
        self.cost_management_settings = None
        self.resource_guard_operation_requests = None
        self.replicated_regions = None
        self.state = None
        self.tags = None

        self.results = dict(changed=False)
        self.to_do = Actions.NoAction
        self._managed_identity = None

        super(AzureRMDataProtectionBackupVault, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=True,
        )

    @property
    def managed_identity(self):
        if not self._managed_identity:
            self._managed_identity = {"identity": DppIdentityDetails,
                                      "user_assigned": UserAssignedIdentity}
        return self._managed_identity

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = self.get_instance()
        old_props = (old_response or {}).get('properties') or {}

        if not self.location:
            if old_response:
                self.location = old_response.get('location')
            else:
                resource_group = self.get_resource_group(self.resource_group)
                self.location = resource_group.location

        curr_identity = old_response.get('identity') if old_response else None
        if self.identity:
            new_identity = self.identity
        else:
            # Nothing requested: resubmit the current identity unchanged so it is not stripped on update
            new_identity = dict(
                type=(curr_identity or {}).get('type', 'None'),
                user_assigned_identities=dict(id=list((curr_identity or {}).get('user_assigned_identities', {}) or {})),
            )
        update_identity, identity_result = self.update_managed_identity(new_identity=new_identity, curr_identity=curr_identity)

        if self.identity:
            append = (self.identity.get('user_assigned_identities') or {}).get('append', True)
            if not append:
                curr_ids = set((curr_identity or {}).get('user_assigned_identities', {}) or {})
                new_ids = set((self.identity.get('user_assigned_identities') or {}).get('id') or [])
                if curr_ids - new_ids:
                    update_identity = True

        merged_security = _deep_merge(old_props.get('security_settings'), self.security_settings)
        merged_feature = _deep_merge(old_props.get('feature_settings'), self.feature_settings)
        merged_monitoring = _deep_merge(old_props.get('monitoring_settings'), self.monitoring_settings)
        merged_cost = _deep_merge(old_props.get('cost_management_settings'), self.cost_management_settings)
        merged_guard = self.resource_guard_operation_requests if self.resource_guard_operation_requests is not None \
            else old_props.get('resource_guard_operation_requests')
        merged_regions = self.replicated_regions if self.replicated_regions is not None \
            else old_props.get('replicated_regions')

        effective_datastore_type = self.datastore_type
        effective_redundancy = self.redundancy

        response = None
        if not old_response:
            if self.state == 'absent':
                self.log("Backup vault does not exist")
            else:
                self.to_do = Actions.Create
        else:
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if old_props.get('storage_settings'):
                    existing_storage = old_props['storage_settings'][0]
                    effective_datastore_type = existing_storage.get('datastore_type') or self.datastore_type
                    effective_redundancy = existing_storage.get('type') or self.redundancy
                    if existing_storage.get('datastore_type') != self.datastore_type or existing_storage.get('type') != self.redundancy:
                        self.module.warn("datastore_type and redundancy cannot be changed after the backup vault has been created")

                update_tags, newtags = self.update_tags(old_response.get('tags', dict()))
                if update_tags:
                    self.to_do = Actions.Update
                    self.tags = newtags

                if update_identity:
                    self.to_do = Actions.Update

                if not self.default_compare({}, merged_security, old_props.get('security_settings'), '', dict(compare=[])):
                    self.to_do = Actions.Update
                if not self.default_compare({}, merged_feature, old_props.get('feature_settings'), '', dict(compare=[])):
                    self.to_do = Actions.Update
                if not self.default_compare({}, merged_monitoring, old_props.get('monitoring_settings'), '', dict(compare=[])):
                    self.to_do = Actions.Update
                if not self.default_compare({}, merged_cost, old_props.get('cost_management_settings'), '', dict(compare=[])):
                    self.to_do = Actions.Update
                if not self.default_compare({}, merged_guard, old_props.get('resource_guard_operation_requests'), '', dict(compare=[])):
                    self.to_do = Actions.Update
                if not self.default_compare({}, merged_regions, old_props.get('replicated_regions'), '', dict(compare=[])):
                    self.to_do = Actions.Update

        if self.to_do in (Actions.Create, Actions.Update):
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.create_update_backupvault(
                identity=identity_result,
                datastore_type=effective_datastore_type,
                redundancy=effective_redundancy,
                security_settings=merged_security,
                feature_settings=merged_feature,
                monitoring_settings=merged_monitoring,
                cost_management_settings=merged_cost,
                resource_guard_operation_requests=merged_guard,
                replicated_regions=merged_regions,
            )
            if response is None:
                response = self.get_instance()
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            self.delete_backupvault()
        else:
            self.results['changed'] = False
            response = old_response

        if response:
            self.results['id'] = response['id']

        return self.results

    def create_update_backupvault(self, identity, datastore_type, redundancy, security_settings, feature_settings,
                                  monitoring_settings, cost_management_settings,
                                  resource_guard_operation_requests, replicated_regions):
        self.log("Creating / Updating the Backup vault {0}".format(self.name))
        backup_vault_kwargs = dict(
            storage_settings=[StorageSetting(datastore_type=datastore_type, type=redundancy)],
            security_settings=_build_security_settings(security_settings),
            feature_settings=_build_feature_settings(feature_settings),
            monitoring_settings=_build_monitoring_settings(monitoring_settings),
            cost_management_settings=_build_cost_management_settings(cost_management_settings),
            resource_guard_operation_requests=resource_guard_operation_requests,
            replicated_regions=replicated_regions,
        )
        parameters = BackupVaultResource(
            location=self.location,
            tags=self.tags,
            identity=identity,
            properties=BackupVault(**{k: v for k, v in backup_vault_kwargs.items() if v is not None}),
        )
        try:
            response = self.dataprotection_client.backup_vaults.begin_create_or_update(
                resource_group_name=self.resource_group,
                vault_name=self.name,
                parameters=parameters,
            )
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error creating/updating the Backup vault: {0}".format(str(exc)))
        return response and as_attribute_dict(response, exclude_readonly=False) or None

    def delete_backupvault(self):
        self.log("Deleting the Backup vault {0}".format(self.name))
        try:
            response = self.dataprotection_client.backup_vaults.begin_delete(
                resource_group_name=self.resource_group,
                vault_name=self.name,
            )
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error deleting the Backup vault: {0}".format(str(exc)))
        return True

    def get_instance(self):
        self.log("Checking if the Backup vault {0} is present".format(self.name))
        try:
            response = self.dataprotection_client.backup_vaults.get(
                resource_group_name=self.resource_group,
                vault_name=self.name,
            )
            return as_attribute_dict(response, exclude_readonly=False)
        except ResourceNotFoundError:
            self.log("Did not find the Backup vault.")
            return False


def main():
    """Main execution"""
    AzureRMDataProtectionBackupVault()


if __name__ == '__main__':
    main()
