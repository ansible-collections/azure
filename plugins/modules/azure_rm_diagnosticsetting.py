#!/usr/bin/python
#
# Copyright (c) 2021 Alvin Ramoutar, (@AlvinRamoutar)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
module: azure_rm_diagnosticsetting
version_added: "0.1.0"
short_description: Manage Azure diagnostic settings
description:
    - Create, update or delete a diagnostic setting.
options:
    name:
        description:
            - The name of the diagnostic setting entry.
        required: True
        type: str
    resource_id:
        description:
            - The resource ID of the resource in which to apply the diagnostic setting.
        required: True
        type: str
    state:
        description:
            - Assert the state of the diagnostic setting. Use C(present) to create or update a diagnostic setting and use C(absent) to delete a diagnostic setting.
        default: present
        choices:
            - absent
            - present
    workspace_id:
        description:
            - The full ARM resource ID of the Log Analytics workspace to which you would like to send Diagnostic Logs.
        type: str
    storage_account_id:
        description:
            - The resource ID of the storage account to which you would like to send Diagnostic Logs.
        type: str
    service_bus_rule_id:
        description:
            - The service bus rule Id of the diagnostic setting. This is here to maintain backwards compatibility.
        type: str
    event_hub_name:
        description:
            - The name of the event hub. If none is specified, the default event hub will be selected.
        type: str
    event_hub_authorization_rule_id:
        description:
            - The resource Id for the event hub authorization rule.
        type: str
    logs:
        description:
            - The list of logs settings.
        type: list
        suboptions:
            category:
                description:
                    - Name of a Diagnostic Log category for a resource type this setting is applied to.
                type: str
                required: true
            enabled:
                description:
                    - A value indicating whether this log is enabled.
                type: bool
                required: true
            retention_policy:
                description:
                    - The retention policy for this category.
                type: dict
                suboptions:
                    enabled:
                        description:
                            - A value indicating whether the retention policy is enabled.
                        type: bool
                        required: true
                    days:
                        description:
                            - The number of days for the retention in days. A value of 0 will retain indefinitely.
                        type: int
                        required: true
    metrics:
        description:
            - The list of metric settings.
        type: list
        suboptions:
            time_grain:
                description:
                    - The timegrain of the metric in ISO8601 format.
                type: str
            category:
                description:
                    - Name of a Diagnostic Metric category for a resource type this setting is applied to.
                type: str
                required: true
            enabled:
                description:
                    - A value indicating whether this metric is enabled.
                type: bool
                required: true
            retention_policy:
                description:
                    - The retention policy for this category.
                type: dict
                suboptions:
                    enabled:
                        description:
                            - A value indicating whether the retention policy is enabled.
                        type: bool
                        required: true
                    days:
                        description:
                            - The number of days for the retention in days. A value of 0 will retain indefinitely.
                        type: int
                        required: true

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Alvin Ramoutar (@AlvinRamoutar)
'''

EXAMPLES = '''
  - name: Create Azure Data Lake Store
    azure_rm_datalakestore:
      resource_group: myResourceGroup
      name: myDataLakeStore
'''

RETURN = '''
state:
    description:
        - Facts for Azure Data Lake Store created/updated.
    returned: always
    type: complex
    contains:
        account_id:
            description:
                - The unique identifier associated with this Data Lake Store account.
            returned: always
            type: str
            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        creation_time:
            description:
                - The account creation time.
            returned: always
            type: str
            sample: '2020-01-01T00:00:00.000000+00:00'
        current_tier:
            description:
                - The commitment tier in use for the current month.
            type: str
            returned: always
            sample: Consumption
        default_group:
            description:
                -  The default owner group for all new folders and files created in the Data Lake Store account.
            type: str
            sample: null
        encryption_config:
            description:
                - The Key Vault encryption configuration.
            type: complex
            contains:
                type:
                    description:
                        - The type of encryption configuration being used.
                    type: str
                    returned: always
                    sample: ServiceManaged
                key_vault_meta_info:
                    description:
                        - The Key Vault information for connecting to user managed encryption keys.
                    type: complex
                    contains:
                        key_vault_resource_id:
                            description:
                                - The resource identifier for the user managed Key Vault being used to encrypt.
                            type: str
                            returned: always
                            sample: /subscriptions/{subscriptionId}/resourceGroups/myResourceGroup/providers/Microsoft.KeyVault/vaults/tstkv
                        encryption_key_name:
                            description:
                                - The name of the user managed encryption key.
                            type: str
                            returned: always
                            sample: KeyName
                        encryption_key_version:
                            description:
                                - The version of the user managed encryption key.
                            type: str
                            returned: always
                            sample: 86a1e3b7406f45afa0d54e21eff47e39
        encryption_provisioning_state:
            description:
                - The current state of encryption provisioning for this Data Lake Store account.
            type: str
            sample: Succeeded
        encryption_state:
            description:
                - The current state of encryption for this Data Lake Store account.
            type: str
            returned: always
            sample: Enabled
        endpoint:
            description:
                - The full CName endpoint for this account.
            returned: always
            type: str
            sample: testaccount.azuredatalakestore.net
        firewall_allow_azure_ips:
            description:
                - The current state of allowing or disallowing IPs originating within Azure through the firewall.
                - If the firewall is disabled, this is not enforced.
            type: str
            returned: always
            sample: Disabled
        firewall_rules:
            description:
                - The list of firewall rules associated with this Data Lake Store account.
            type: list
            returned: always
            contains:
                name:
                    description:
                        - The resource name.
                    type: str
                    returned: always
                    sample: Example Name
                start_ip_address:
                    description:
                        - The start IP address for the firewall rule.
                        - This can be either ipv4 or ipv6.
                        - Start and End should be in the same protocol.
                    type: str
                    returned: always
                    sample: 192.168.1.1
                end_ip_address:
                    description:
                        - The end IP address for the firewall rule.
                        - This can be either ipv4 or ipv6.
                        - Start and End should be in the same protocol.
                    type: str
                    returned: always
                    sample: 192.168.1.254
        firewall_state:
            description:
                - The current state of the IP address firewall for this Data Lake Store account.
            type: str
            returned: always
            sample: Enabled
        id:
            description:
                - The resource identifier.
            returned: always
            type: str
            sample: /subscriptions/{subscriptionId}/resourceGroups/myResourceGroup/providers/Microsoft.DataLakeStore/accounts/testaccount
        identity:
            description:
                - The Key Vault encryption identity, if any.
            type: complex
            contains:
                type:
                    description:
                        - The type of encryption being used.
                    type: str
                    sample: SystemAssigned
                principal_id:
                    description:
                        - The principal identifier associated with the encryption.
                    type: str
                    sample: 00000000-0000-0000-0000-000000000000
                tenant_id:
                    description:
                        - The tenant identifier associated with the encryption.
                    type: str
                    sample: 00000000-0000-0000-0000-000000000000
        last_modified_time:
            description:
                - The account last modified time.
            returned: always
            type: str
            sample: '2020-01-01T00:00:00.000000+00:00'
        location:
            description:
                - The resource location.
            returned: always
            type: str
            sample: westeurope
        name:
            description:
                - The resource name.
            returned: always
            type: str
            sample: testaccount
        new_tier:
            description:
                - The commitment tier to use for next month.
            type: str
            returned: always
            sample: Consumption
        provisioning_state:
            description:
                - The provisioning status of the Data Lake Store account.
            returned: always
            type: str
            sample: Succeeded
        state:
            description:
                - The state of the Data Lake Store account.
            returned: always
            type: str
            sample: Active
        tags:
            description:
                - The resource tags.
            returned: always
            type: dict
            sample: { "tag1":"abc" }
        trusted_id_providers:
            description:
                - The current state of the trusted identity provider feature for this Data Lake Store account.
            type: list
            returned: always
            contains:
                id:
                    description:
                        - The resource identifier.
                    type: str
                name:
                    description:
                        - The resource name.
                    type: str
                type:
                    description:
                        - The resource type.
                    type: str
                id_provider:
                    description:
                        - The URL of this trusted identity provider.
                    type: str
        trusted_id_provider_state:
            description:
                - The list of trusted identity providers associated with this Data Lake Store account.
            type: str
            returned: always
            sample: Enabled
        type:
            description:
                - The resource type.
            returned: always
            type: str
            sample: Microsoft.DataLakeStore/accounts
        virtual_network_rules:
            description:
                - The list of virtual network rules associated with this Data Lake Store account.
            type: list
            returned: always
            contains:
                name:
                    description:
                        - The resource name.
                    type: str
                    sample: Rule Name
                subnet_id:
                    description:
                        - The resource identifier for the subnet.
                    type: str
                    sample: /subscriptions/{subscriptionId}/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/vnet/subnets/default

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
import datetime

try:
    from msrestazure.azure_exceptions import CloudError
except ImportError:
    # This is handled in azure_rm_common
    pass

retention_policy_object = dict(
    enabled=dict(type='bool', required=True),
    days=dict(type='int', required=True)
)

log_settings_object = dict(
    category=dict(type='str', required=True),
    enabled=dict(type='bool', required=True),
    retention_policy=retention_policy_object
)

metric_settings_object = dict(
    time_grain=dict(type='str'),
    category=dict(type='str', required=True),
    enabled=dict(type='bool', required=True),
    retention_policy=retention_policy_object
)


class AzureRMDiagnosticSetting(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_id=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            workspace_id=dict(type='str'),
            storage_account_id=dict(type='str'),
            service_bus_rule_id=dict(type='str'),
            event_hub_name=dict(type='str'),
            event_hub_authorization_rule_id=dict(type='str'),
            logs=dict(
                type='list',
                elements='dict',
                options=log_settings_object
            ),
            metrics=dict(
                type='list',
                elements='dict',
                options=metric_settings_object
            )
        )

        self.name = None
        self.resource_id = None
        self.state = None
        self.workspace_id = None
        self.storage_account_id = None
        self.service_bus_rule_id = None
        self.event_hub_name = None
        self.event_hub_authorization_rule_id = None
        self.logs = dict()
        self.metrics = dict()

        self.results = dict(changed=False)
        self.diagnostic_setting_dict = None

        super(AzureRMDiagnosticSetting, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=False,
                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        self.diagnostic_setting_dict = self.get_diagnostic_setting()

        self.results['state'] = self.diagnostic_setting_dict if self.diagnostic_setting_dict is not None else dict()

        if self.state == 'present':
            if not self.diagnostic_setting_dict:
                self.results['state'] = self.create_diagnostic_setting()
            else:
                self.results['state'] = self.update_diagnostic_setting()
        else:
            self.delete_diagnostic_setting()
            self.results['state'] = dict(state='deleted')

        return self.results

    def get_diagnostic_setting(self):
        self.log('Get properties for diagnostic setting {0}'.format(self.name))
        diagnostic_setting_obj = None
        diagnostic_setting = None

        try:
            diagnostic_setting_obj = self.monitor_client.diagnostic_settings.get(self.resourceId, self.name)
        except CloudError:
            pass

        if diagnostic_setting_obj:
            diagnostic_setting = self.diagnostic_setting_obj_to_dict(diagnostic_setting_obj)

        return diagnostic_setting

    def create_diagnostic_setting(self):
        self.log("Create diagnostic setting {0}".format(self.name))
        
        resource = self.parse_resource_id(self)

        if not self.logs and not self.metrics:
            self.fail('Parameter error: must provide at least 1 log and/or metric categories when creating a diagnostic setting.')
        self.check_retention_policy_provided()
        self.results['changed'] = True

        if self.check_mode:
            diagnostic_setting_dict = dict(
                name=self.name,
                resource_id=self.resource_id
            )


    def update_diagnostic_setting(self):
        self.log('Update diagnostic setting {0}'.format(self.name))

    def delete_diagnostic_setting(self):
        self.log('Delete diagnostic setting {0}'.format(self.name))

        self.results['changed'] = True if self.diagnostic_setting is not None else False
        if not self.check_mode and self.diagnostic_setting is not None:
            try:
                status = self.monitor_client.diagnostic_settings.delete(self.resourceId, self.name)
                self.log("delete status: ")
                self.log(str(status))
            except CloudError as e:
                self.fail("Failed to delete diagnostic setting: {0}".format(str(e)))

        return True

    def diagnostic_setting_obj_to_dict(self, diagnostic_setting_obj):
        diagnostic_setting_dict = dict(
            storage_account_id=diagnostic_setting_obj.storage_account_id,
            service_bus_rule_id=diagnostic_setting_obj.service_bus_rule_id,
            event_hub_authorization_rule_id=diagnostic_setting_obj.event_hub_authorization_rule_id,
            event_hub_name=diagnostic_setting_obj.event_hub_name,
            metrics=None,
            logs=None,
            workspace_id=diagnostic_setting_obj.workspace_id,
            log_analytics_destination_type=diagnostic_setting_obj.log_analytics_destination_type
        )

        diagnostic_setting_dict['metrics'] = list()
        if diagnostic_setting_obj.metrics:
            for entry in diagnostic_setting_obj.metrics:
                entry_item = dict(
                    timeGrain = entry.time_grain,
                    category = entry.category,
                    enabled = entry.enabled,
                    retentionPolicy = dict(
                        days=entry.retention_policy.days,
                        enabled=entry.retention_policy.enabled
                    ))
                diagnostic_setting_dict['metrics'].append(entry_item)

        diagnostic_setting_dict['logs'] = list()
        if diagnostic_setting_obj.logs:
            for entry in diagnostic_setting_obj.logs:
                entry_item = dict(
                    category = entry.category,
                    enabled = entry.enabled,
                    retentionPolicy = dict(
                        days=entry.retention_policy.days,
                        enabled=entry.retention_policy.enabled
                    ))
                diagnostic_setting_dict['logs'].append(entry_item)

        return diagnostic_setting_dict

    def parse_resource_id(self) -> dict:
        sects = self.resource_id.split('/')

        if len(sects) != 9:
            self.fail("Unexpected Azure Resource ID. Expecting format: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}")
        else:
            return {
                "subscription": sects[2],
                "resourceGroup": sects[4],
                "provider": sects[6] + '/' + sects[7],
                "name": sects[8]
            }


def main():
    AzureRMDiagnosticSetting()


if __name__ == '__main__':
    main()
