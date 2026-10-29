#!/usr/bin/python
#
# Copyright (c) 2020 Suyeb Ansari (@suyeb786)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = \
    '''
---
module: azure_rm_recoveryservicesvault
version_added: '1.1.0'
short_description: Create, update and delete Azure Recovery Services vault
description:
    - Create, update or delete Azure Recovery Services vault.
    - Configure the public network access, security, encryption, redundancy and monitoring settings of the vault.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - The name of the Azure Recovery Service Vault.
        required: true
        type: str
    location:
        description:
            - Azure Resource location.
        required: true
        type: str
    state:
        description:
            - Assert the state of the protection item.
            - Use C(present) for Creating Azure Recovery Service Vault.
            - Use C(absent) for Deleting Azure Recovery Service Vault.
        default: present
        type: str
        choices:
            - present
            - absent
    public_network_access:
        description:
            - Whether the vault accepts traffic from public networks.
        type: str
        choices:
            - Enabled
            - Disabled
        version_added: '4.2.0'
    security_settings:
        description:
            - Security settings of the vault.
            - Only the settings you specify are changed, the others keep their current values.
        type: dict
        version_added: '4.2.0'
        suboptions:
            soft_delete_settings:
                description:
                    - Soft delete settings of the vault.
                    - Once changed through this module, the vault no longer accepts soft delete changes from
                      M(azure.azcollection.azure_rm_recoveryservicesvaultconfig).
                type: dict
                suboptions:
                    soft_delete_state:
                        description:
                            - Soft delete state for cloud workloads.
                            - C(AlwaysON) cannot be reverted.
                            - Azure rejects C(Disabled) when secure by default soft delete is enforced for the region.
                        type: str
                        choices:
                            - Enabled
                            - Disabled
                            - AlwaysON
                    soft_delete_retention_period_in_days:
                        description:
                            - Number of days deleted backup data is retained in the soft deleted state.
                            - Valid range is 14 to 180.
                        type: int
                    enhanced_security_state:
                        description:
                            - Soft delete and security settings for hybrid workloads.
                            - C(AlwaysON) cannot be reverted.
                        type: str
                        choices:
                            - Enabled
                            - Disabled
                            - AlwaysON
            immutability_settings:
                description:
                    - Immutability settings of the vault.
                type: dict
                suboptions:
                    state:
                        description:
                            - Immutability state of the vault.
                            - C(Locked) cannot be reverted.
                        type: str
                        choices:
                            - Disabled
                            - Unlocked
                            - Locked
                    configuration:
                        description:
                            - Immutability configuration of the vault.
                            - Only used when I(state=Unlocked) or I(state=Locked). When not set, I(type=AsPerPolicy) is used.
                        type: dict
                        suboptions:
                            type:
                                description:
                                    - C(AsPerPolicy) inherits the immutability duration from the backup policies.
                                    - C(TimeBased) uses the fixed I(duration_in_days).
                                type: str
                                choices:
                                    - AsPerPolicy
                                    - TimeBased
                            duration_in_days:
                                description:
                                    - Immutability duration in days, between 30 and 36135.
                                    - Required when I(type=TimeBased).
                                    - Azure does not allow reducing the immutability duration while immutability is enabled.
                                type: int
    encryption:
        description:
            - Customer managed key (CMK) encryption settings of the vault.
            - The managed identity used to access the key vault must be assigned to the vault through I(identity).
            - CMK encryption cannot be disabled once enabled.
        type: dict
        version_added: '4.2.0'
        suboptions:
            key_vault_properties:
                description:
                    - Properties of the key vault which hosts the customer managed key.
                type: dict
                suboptions:
                    key_uri:
                        description:
                            - The key URI of the customer managed key.
                        type: str
            kek_identity:
                description:
                    - The managed identity used to access the customer managed key.
                type: dict
                suboptions:
                    use_system_assigned_identity:
                        description:
                            - Whether to use the system assigned identity of the vault.
                            - Set to C(false) when using I(user_assigned_identity).
                        type: bool
                    user_assigned_identity:
                        description:
                            - Resource ID of the user assigned identity.
                        type: str
            infrastructure_encryption:
                description:
                    - Enable or disable double (infrastructure) encryption.
                    - Can only be set on a vault which has no protected items, and cannot be changed afterwards.
                type: str
                choices:
                    - Enabled
                    - Disabled
    redundancy_settings:
        description:
            - Backup storage redundancy settings of the vault.
            - Storage redundancy can only be changed before any item is protected in the vault.
        type: dict
        version_added: '4.2.0'
        suboptions:
            standard_tier_storage_redundancy:
                description:
                    - The storage redundancy type of the vault.
                type: str
                choices:
                    - LocallyRedundant
                    - GeoRedundant
                    - ZoneRedundant
            cross_region_restore:
                description:
                    - Cross region restore state of the vault.
                    - Only valid when I(redundancy_settings.standard_tier_storage_redundancy=GeoRedundant).
                    - Cannot be disabled once enabled.
                type: str
                choices:
                    - Enabled
                    - Disabled
    monitoring_settings:
        description:
            - Monitoring and alerting settings of the vault.
            - Alert settings which are not specified keep their current value, or default to C(Enabled) when the vault has no
              monitoring settings yet.
        type: dict
        version_added: '4.2.0'
        suboptions:
            azure_monitor_alert_settings:
                description:
                    - Settings for Azure Monitor based alerts.
                type: dict
                suboptions:
                    alerts_for_all_job_failures:
                        description:
                            - Enable or disable built-in Azure Monitor alerts for all job failures.
                        type: str
                        choices:
                            - Enabled
                            - Disabled
                    alerts_for_all_replication_issues:
                        description:
                            - Enable or disable built-in Azure Monitor alerts for all replication issues.
                        type: str
                        choices:
                            - Enabled
                            - Disabled
                    alerts_for_all_failover_issues:
                        description:
                            - Enable or disable built-in Azure Monitor alerts for all failover issues.
                        type: str
                        choices:
                            - Enabled
                            - Disabled
            classic_alert_settings:
                description:
                    - Settings for the classic alert solution.
                type: dict
                suboptions:
                    alerts_for_critical_operations:
                        description:
                            - Enable or disable classic alerts for critical operations.
                        type: str
                        choices:
                            - Enabled
                            - Disabled
                    email_notifications_for_site_recovery:
                        description:
                            - Enable or disable classic email notifications for Site Recovery.
                        type: str
                        choices:
                            - Enabled
                            - Disabled
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
    - azure.azcollection.azure_identity_multiple
author:
    - Suyeb Ansari (@suyeb786)
'''

EXAMPLES = '''
- name: Create/Update Azure Recovery Service vault
  azure_rm_recoveryservicesvault:
    resource_group: 'myResourceGroup'
    name: 'testVault'
    location: 'westeurope'
    state: 'present'
- name: Configure security, redundancy and monitoring settings of a Recovery Service vault
  azure_rm_recoveryservicesvault:
    resource_group: 'myResourceGroup'
    name: 'testVault'
    location: 'westeurope'
    public_network_access: Enabled
    security_settings:
      soft_delete_settings:
        soft_delete_state: AlwaysON
        soft_delete_retention_period_in_days: 30
      immutability_settings:
        state: Unlocked
    redundancy_settings:
      standard_tier_storage_redundancy: GeoRedundant
      cross_region_restore: Enabled
    monitoring_settings:
      azure_monitor_alert_settings:
        alerts_for_all_job_failures: Enabled
      classic_alert_settings:
        alerts_for_critical_operations: Disabled

- name: Encrypt a Recovery Service vault with a customer managed key
  azure_rm_recoveryservicesvault:
    resource_group: 'myResourceGroup'
    name: 'testVault'
    location: 'westeurope'
    identity:
      type: UserAssigned
      user_assigned_identities:
        id:
          - "/subscriptions/xxx/resourceGroups/myResourceGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myIdentity"
    encryption:
      key_vault_properties:
        key_uri: https://mykeyvault.vault.azure.net/keys/mykey
      kek_identity:
        use_system_assigned_identity: false
        user_assigned_identity: "/subscriptions/xxx/resourceGroups/myResourceGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myIdentity"
      infrastructure_encryption: Disabled

- name: Delete Recovery Service Vault
  azure_rm_recoveryservicesvault:
    resource_group: 'myResourceGroup'
    name: 'testVault'
    location: 'westeurope'
    state: 'absent'
'''

RETURN = '''
response:
    description:
        - The response about the current state of the recovery services vault.
        - Deprecated, will be removed in version 5.0.0. Use RV(state) instead, which returns the same information in snake_case.
    returned: always
    type: complex
    contains:
        etag:
            description:
                - A unique read-only string that changes whenever the resource create.
            returned: always
            type: str
            sample: "datetime'2020-09-16T02%3A44%3A27.834293Z'"
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample:  "/subscriptions/xxxxxxx/resourceGroups/resourcegroup_name/ \
            providers/Microsoft.RecoveryServices/vaults/rev_name"
        location:
            description:
                - The location of the resource.
            returned: always
            type: str
            sample: "eastus"
        name:
            description:
                - Name of the recovery services vault name.
            returned: always
            type: str
            sample: revault_name
        properties:
            description:
                - The recovery service vault properties.
            returned: always
            type: dict
            sample: {
                    "privateEndpointStateForBackup": "None",
                    "privateEndpointStateForSiteRecovery": "None",
                    "provisioningState": "Succeeded"
                    }
        sku:
            description:
                - The sku type of the recovery service vault.
            returned: always
            type: str
            sample: Standard
        type:
            description:
                - The type of the recovery service vault.
            returned: always
            type: str
            sample: "Microsoft.RecoveryServices/vaults"
        tags:
            description:
                - The resource tags.
            returned: when-used
            type: dict
            sample: {'key1': 'value'}
state:
    description:
        - The current state of the recovery services vault, with snake_case keys.
    returned: when the vault exists
    type: complex
    version_added: '4.2.0'
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.RecoveryServices/vaults/testVault"
        name:
            description:
                - Name of the recovery services vault.
            returned: always
            type: str
            sample: testVault
        type:
            description:
                - The type of the recovery services vault.
            returned: always
            type: str
            sample: "Microsoft.RecoveryServices/vaults"
        location:
            description:
                - The location of the resource.
            returned: always
            type: str
            sample: "eastus"
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: "W/datetime'2026-10-22T02%3A44%3A27.834293Z'"
        sku:
            description:
                - The SKU of the recovery services vault.
            returned: always
            type: dict
            sample: {"name": "Standard"}
        identity:
            description:
                - The managed identity of the recovery services vault.
            returned: when-used
            type: dict
            sample: {"type": "SystemAssigned", "principal_id": "xxxxxxx", "tenant_id": "xxxxxxx"}
        tags:
            description:
                - The resource tags.
            returned: when-used
            type: dict
            sample: {'key1': 'value'}
        properties:
            description:
                - The recovery services vault properties.
                - The settings managed by this module use the same names as the module options, for example
                  C(properties.security_settings.soft_delete_settings).
            returned: always
            type: dict
            sample: {
                    "provisioning_state": "Succeeded",
                    "public_network_access": "Enabled",
                    "security_settings": {
                        "soft_delete_settings": {
                            "soft_delete_state": "AlwaysON",
                            "soft_delete_retention_period_in_days": 30,
                            "enhanced_security_state": "Enabled"
                        },
                        "immutability_settings": {"state": "Unlocked"}
                    },
                    "redundancy_settings": {
                        "standard_tier_storage_redundancy": "LocallyRedundant",
                        "cross_region_restore": "Disabled"
                    },
                    "monitoring_settings": {
                        "azure_monitor_alert_settings": {"alerts_for_all_job_failures": "Enabled"},
                        "classic_alert_settings": {"alerts_for_critical_operations": "Disabled"}
                    }
                    }
'''

try:
    from azure.core.polling import LROPoller
    from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.recoveryservices.models import IdentityData, UserIdentity
except ImportError:
    # This is handled in azure_rm_common
    pass

import copy
import json
import time

from ansible.module_utils.common.dict_transformations import snake_dict_to_camel_dict
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

VAULT_PROPERTY_OPTIONS = ['public_network_access', 'security_settings', 'encryption', 'redundancy_settings', 'monitoring_settings']

# Azure rejects partial monitoring settings, so unset alert flags fall back to the service defaults
# (also the defaults used by az backup vault create and the azurerm provider).
MONITORING_SETTINGS_DEFAULTS = dict(
    azureMonitorAlertSettings=dict(
        alertsForAllJobFailures='Enabled',
        alertsForAllReplicationIssues='Enabled',
        alertsForAllFailoverIssues='Enabled'
    ),
    classicAlertSettings=dict(
        alertsForCriticalOperations='Enabled',
        emailNotificationsForSiteRecovery='Enabled'
    )
)


def _strip_none(value):
    if isinstance(value, dict):
        result = dict()
        for key, item in value.items():
            item = _strip_none(item)
            if item is not None and item != {}:
                result[key] = item
        return result
    return value


def _deep_merge(base, overrides):
    # Vault PATCH replaces nested settings objects, so merge requested keys onto the existing settings,
    # same approach as azure_rm_dataprotectionbackupvault.
    if overrides is None:
        return copy.deepcopy(base)
    if not isinstance(overrides, dict):
        return overrides
    result = copy.deepcopy(base) if isinstance(base, dict) else dict()
    for key, value in overrides.items():
        result[key] = _deep_merge(result.get(key), value) if isinstance(value, dict) else value
    return result


def _immutability_settings(settings):
    # Enabled immutability requires a configuration type, AsPerPolicy (the az cli default) must not have a
    # duration and Disabled must not send a configuration at all.
    settings = copy.deepcopy(settings)
    if settings.get('state') == 'Disabled':
        settings.pop('configuration', None)
    else:
        configuration = settings.setdefault('configuration', dict())
        configuration.setdefault('type', 'AsPerPolicy')
        if configuration['type'] == 'AsPerPolicy':
            configuration.pop('durationInDays', None)
    return settings


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRecoveryServicesVault(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
                required=True
            ),
            identity=dict(
                type='dict',
                options=self.managed_identity_multiple_spec
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            public_network_access=dict(
                type='str',
                choices=['Enabled', 'Disabled']
            ),
            security_settings=dict(
                type='dict',
                options=dict(
                    soft_delete_settings=dict(
                        type='dict',
                        options=dict(
                            soft_delete_state=dict(type='str', choices=['Enabled', 'Disabled', 'AlwaysON']),
                            soft_delete_retention_period_in_days=dict(type='int'),
                            enhanced_security_state=dict(type='str', choices=['Enabled', 'Disabled', 'AlwaysON'])
                        )
                    ),
                    immutability_settings=dict(
                        type='dict',
                        options=dict(
                            state=dict(type='str', choices=['Disabled', 'Unlocked', 'Locked']),
                            configuration=dict(
                                type='dict',
                                options=dict(
                                    type=dict(type='str', choices=['AsPerPolicy', 'TimeBased']),
                                    duration_in_days=dict(type='int')
                                )
                            )
                        )
                    )
                )
            ),
            encryption=dict(
                type='dict',
                options=dict(
                    key_vault_properties=dict(
                        type='dict',
                        no_log=False,
                        options=dict(
                            key_uri=dict(type='str', no_log=False)
                        )
                    ),
                    kek_identity=dict(
                        type='dict',
                        options=dict(
                            use_system_assigned_identity=dict(type='bool'),
                            user_assigned_identity=dict(type='str')
                        )
                    ),
                    infrastructure_encryption=dict(type='str', choices=['Enabled', 'Disabled'])
                )
            ),
            redundancy_settings=dict(
                type='dict',
                options=dict(
                    standard_tier_storage_redundancy=dict(type='str', choices=['LocallyRedundant', 'GeoRedundant', 'ZoneRedundant']),
                    cross_region_restore=dict(type='str', choices=['Enabled', 'Disabled'])
                )
            ),
            monitoring_settings=dict(
                type='dict',
                options=dict(
                    azure_monitor_alert_settings=dict(
                        type='dict',
                        options=dict(
                            alerts_for_all_job_failures=dict(type='str', choices=['Enabled', 'Disabled']),
                            alerts_for_all_replication_issues=dict(type='str', choices=['Enabled', 'Disabled']),
                            alerts_for_all_failover_issues=dict(type='str', choices=['Enabled', 'Disabled'])
                        )
                    ),
                    classic_alert_settings=dict(
                        type='dict',
                        options=dict(
                            alerts_for_critical_operations=dict(type='str', choices=['Enabled', 'Disabled']),
                            email_notifications_for_site_recovery=dict(type='str', choices=['Enabled', 'Disabled'])
                        )
                    )
                )
            )
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.state = None
        self.identity = None
        self.tags = None
        self.public_network_access = None
        self.security_settings = None
        self.encryption = None
        self.redundancy_settings = None
        self.monitoring_settings = None

        self.results = dict(changed=False)
        self.to_do = Actions.NoAction
        self.body = dict()
        self.desired_properties = None
        self.properties_patch = None

        self._managed_identity = None

        super(AzureRMRecoveryServicesVault, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                           supports_check_mode=True,
                                                           supports_tags=True
                                                           )

    @property
    def managed_identity(self):
        if not self._managed_identity:
            self._managed_identity = {"identity": IdentityData,
                                      "user_assigned": UserIdentity
                                      }
        return self._managed_identity

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        old_vault = self.get_resource()
        old_response = self.format_response(old_vault)

        update_identity = False
        if self.identity:
            old_identity = self.format_for_helper(old_response.get('identity') if old_response else None)
            update_identity, identity = self.update_managed_identity(curr_identity=old_identity,
                                                                     new_identity=self.identity)
            self.identity = self.format_for_body(identity)
        elif old_response:
            self.identity = old_response.get('identity')

        update_tags = False
        if old_response:
            update_tags, self.tags = self.update_tags(old_response.get('tags'))

        self.body = self.get_body()
        self.desired_properties = self.get_desired_properties()

        if self.state == 'absent':
            if old_vault is not None:
                self.to_do = Actions.Delete
        elif old_vault is None:
            self.to_do = Actions.Create
        else:
            self.properties_patch = self.get_properties_patch(old_response)
            if update_identity or update_tags or self.properties_patch is not None:
                self.to_do = Actions.Update

        vault = old_vault
        if self.to_do in (Actions.Create, Actions.Update):
            if not self.check_mode:
                vault = self.create_update_resource(old_response, put_required=update_identity or update_tags)
        elif self.to_do == Actions.Delete:
            if not self.check_mode:
                self.delete_resource()
                vault = None

        self.results['changed'] = self.to_do != Actions.NoAction
        self.results['response'] = self.format_response(vault)
        self.results['state'] = self.format_item(vault)
        self.module.deprecate("The 'response' return value is deprecated, use 'state' instead which returns the same "
                              "information in snake_case.", version='5.0.0', collection_name='azure.azcollection')

        return self.results

    def get_body(self):
        return {
            "properties": {},
            "sku": {
                "name": "Standard"
            },
            "identity": self.identity,
            "location": self.location,
            'tags': self.tags
        }

    def format_for_body(self, identity):
        return identity.as_dict() if identity else identity

    def format_for_helper(self, identity):
        if identity and identity.get("userAssignedIdentities"):
            identity["user_assigned_identities"] = identity.pop("userAssignedIdentities")
        return identity

    def get_desired_properties(self):
        desired = _strip_none(dict((key, getattr(self, key)) for key in VAULT_PROPERTY_OPTIONS))
        return snake_dict_to_camel_dict(desired)

    def get_properties_patch(self, response):
        '''
        Returns the vault properties to PATCH, or None when the vault already matches the desired properties.
        Each requested settings object is merged with its current value, so a partial change such as
        only the soft delete retention still sends the softDeleteState that Azure requires.
        '''
        if not self.desired_properties:
            return None
        current = (response or {}).get('properties') or {}
        patch = dict()
        for key, value in self.desired_properties.items():
            if key == 'securitySettings':
                current_security = current.get(key) or {}
                patch[key] = dict((sub, _deep_merge(current_security.get(sub), item)) for sub, item in value.items())
                if 'immutabilitySettings' in patch[key]:
                    patch[key]['immutabilitySettings'] = _immutability_settings(patch[key]['immutabilitySettings'])
            elif key == 'monitoringSettings':
                patch[key] = _deep_merge(_deep_merge(MONITORING_SETTINGS_DEFAULTS, current.get(key)), value)
            else:
                patch[key] = _deep_merge(current.get(key), value)
        if self.default_compare({}, copy.deepcopy(patch), current, '', dict(compare=[])):
            return None
        return patch

    def create_update_resource(self, old_response, put_required):
        self.log("Creating / Updating Recovery Service Vault {0}".format(self.name))
        if self.to_do == Actions.Create or put_required:
            self.put_resource()
            if self.desired_properties:
                current = self.wait_for_vault_initialization() if self.to_do == Actions.Create else self.get_resource()
                old_response = self.format_response(current)
                self.properties_patch = self.get_properties_patch(old_response)

        if self.properties_patch is not None:
            self.patch_resource(old_response)

        vault = self.get_resource()
        if self.properties_patch is not None and self.get_properties_patch(self.format_response(vault)) is not None:
            self.fail("Azure accepted the update of Recovery Service Vault {0} but did not apply all requested "
                      "properties: {1}".format(self.name, json.dumps(self.properties_patch)))
        return vault

    def put_resource(self):
        # Create, tags and identity use the legacy client so the vault stays manageable by
        # azure_rm_recoveryservicesvaultconfig until the vault properties are changed through this module.
        try:
            response = self.recovery_services_legacy_client.vaults.begin_create_or_update(
                resource_group_name=self.resource_group,
                vault_name=self.name,
                vault=self.body,
            )
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error creating/updating Recovery Service Vault {0}: {1}".format(self.name, str(exc)))

    def patch_resource(self, old_response):
        current = ((old_response or {}).get('properties') or {}).get('securitySettings') or {}
        desired = self.properties_patch.get('securitySettings') or {}
        if (desired.get('immutabilitySettings') or {}).get('state') == 'Locked' and \
                (current.get('immutabilitySettings') or {}).get('state') not in ('Unlocked', 'Locked'):
            # Azure does not allow switching immutability from Disabled to Locked directly
            unlocked = dict(desired['immutabilitySettings'], state='Unlocked')
            self._update_properties(dict(securitySettings=dict(immutabilitySettings=unlocked)))
        self._update_properties(self.properties_patch)

    def _update_properties(self, properties):
        retry_limit = 20
        for attempt in range(retry_limit):
            try:
                response = self.recovery_services_client.vaults.begin_update(
                    resource_group_name=self.resource_group,
                    vault_name=self.name,
                    vault=dict(properties=properties),
                )
                if isinstance(response, LROPoller):
                    self.get_poller_result(response)
                return
            except HttpResponseError as exc:
                # The vault rejects updates with 409 while another operation (such as its initialization) is running
                error_code = exc.error.code if exc.error else None
                if exc.status_code == 409 and error_code and 'ConflictingOperation' in error_code and attempt < retry_limit - 1:
                    time.sleep(15)
                    continue
                self.fail("Error updating properties of Recovery Service Vault {0}: {1}".format(self.name, str(exc)))
            except Exception as exc:
                self.fail("Error updating properties of Recovery Service Vault {0}: {1}".format(self.name, str(exc)))

    def wait_for_vault_initialization(self):
        # The soft delete settings of a new vault are populated asynchronously, and the vault
        # rejects updates with a conflicting operation error until then.
        vault = None
        for dummy in range(30):
            vault = self.get_resource()
            properties = (self.format_response(vault) or {}).get('properties') or {}
            if (properties.get('securitySettings') or {}).get('softDeleteSettings'):
                break
            time.sleep(10)
        return vault

    def delete_resource(self):
        self.log("Deleting Recovery Service Vault {0}".format(self.name))
        try:
            response = self.recovery_services_client.vaults.begin_delete(
                resource_group_name=self.resource_group,
                vault_name=self.name,
            )
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except HttpResponseError as exc:
            # The final poll of a completed delete returns 404 once the vault is gone
            if exc.status_code != 404:
                self.fail("Error deleting Recovery Service Vault {0}: {1}".format(self.name, str(exc)))
        except Exception as exc:
            self.fail("Error deleting Recovery Service Vault {0}: {1}".format(self.name, str(exc)))
        return True

    def get_resource(self):
        self.log("Checking if Recovery Service Vault {0} exists".format(self.name))
        # Some operations of Recovery Service Vault can take a while to provision, wait for it and
        # warn if we time out waiting.
        retry_limit = 60
        vault = None
        try:
            for dummy in range(retry_limit):
                vault = self.recovery_services_client.vaults.get(
                    resource_group_name=self.resource_group,
                    vault_name=self.name,
                )
                if vault.properties is None or vault.properties.provisioning_state == 'Succeeded':
                    return vault
                time.sleep(2)
        except ResourceNotFoundError:
            return None
        except Exception as exc:
            self.fail("Error retrieving Recovery Service Vault {0}: {1}".format(self.name, str(exc)))
        self.module.warn('Retry limit {0} exceeded while waiting for resource to provision'.format(retry_limit))
        return vault

    def format_response(self, item):
        return item.as_dict(exclude_readonly=False) if item else None

    def format_item(self, item):
        return as_attribute_dict(item, exclude_readonly=False) if item else None


def main():
    AzureRMRecoveryServicesVault()


if __name__ == '__main__':
    main()
