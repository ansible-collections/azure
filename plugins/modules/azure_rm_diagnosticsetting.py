#!/usr/bin/python
#
# Copyright (c) 2021 Alvin Ramoutar, (@AlvinRamoutar)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
module: azure_rm_diagnosticsetting
version_added: "1.7.0"
short_description: Manage Azure diagnostic settings
description:
    - Create, update or delete a diagnostic setting.
options:
    name:
        description:
            - The name of the diagnostic setting entry.
        required: true
        type: str
    resource_id:
        description:
            - The resource ID of the resource in which to apply the diagnostic setting.
        required: true
        type: str
    state:
        description:
            - Assert state of the diagnostic setting. Use C(present) to create or update diagnostic setting and use C(absent) to delete diagnostic setting.
        default: present
        choices:
            - absent
            - present
        type: str
    workspace_id:
        description:
            - The full ARM resource ID of the Log Analytics workspace to which you would like to send Diagnostic Logs.
        type: str
    log_analytics_destination_type:
        description:
            - whether the export to Log Analytics should use the default destination type, or use a destination type.
        choices:
            - Dedicated
            - null
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
        elements: dict
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
                default: true
            retention_policy:
                description:
                    - The retention policy for this category.
                type: dict
                suboptions:
                    enabled:
                        description:
                            - A value indicating whether the retention policy is enabled.
                        type: bool
                        default: true
                    days:
                        description:
                            - The number of days for the retention in days. A value of 0 will retain indefinitely.
                        type: int
                        default: 0
                        required: true
    metrics:
        description:
            - The list of metric settings.
        type: list
        elements: dict
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
                default: true
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
                        default: true
                        required: true
                    days:
                        description:
                            - The number of days for the retention in days. A value of 0 will retain indefinitely.
                        type: int
                        default: 0
                        required: true

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Alvin Ramoutar (@AlvinRamoutar)
'''

EXAMPLES = '''
  - name: Create Diagnostic Setting
    azure_rm_diagnosticsetting:
      name: myDiagnosticSetting
      resource_id: /subscriptions/1234abc0/resourceGroups/myResourceGroup/providers/Microsoft.Network/applicationGateways/myApplicationGateway
      storage_account_id: /subscriptions/1234abc0/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/myStorageAccount
      logs:
        - category: ApplicationGatewayFirewallLog
          retention_policy:
            days: 0
'''

RETURN = '''
state:
    description:
        - Facts for Azure Diagnostic Setting created/updated.
    returned: always
    type: complex
    contains:
        name:
            description:
                - The name of the diagnostic setting entry.
            returned: always
            type: str
            sample: myDiagnosticSetting
        resource_id:
            description:
                - The resource ID of the resource in which to apply the diagnostic setting.
            returned: always
            type: str
            sample: /subscriptions/1234abc0/resourceGroups/myResourceGroup/providers/Microsoft.Network/applicationGateways/myApplicationGateway
        state:
            description:
                - Assert state of the diagnostic setting. Use C(present) to create or update diagnostic setting and use C(absent) to delete diagnostic setting.
            returned: always
            type: str
            sample: present
        workspace_id:
            description:
                - The full ARM resource ID of the Log Analytics workspace to which you would like to send Diagnostic Logs.
            type: str
            sample: /subscriptions/1234abc0/resourceGroups/myResourceGroup/providers/Microsoft.OperationalInsights/workspaces/myLogAnalyticsWorkspace
        log_analytics_destination_type:
            description:
                - whether the export to Log Analytics should use the default destination type, or use a destination type.
            choices:
                - Dedicated
                - null
            type: str
            sample: Dedicated
        storage_account_id:
            description:
                - The resource ID of the storage account to which you would like to send Diagnostic Logs.
            type: str
            sample: /subscriptions/1234abc0/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/myStorageAccount
        service_bus_rule_id:
            description:
                - The service bus rule Id of the diagnostic setting. This is here to maintain backwards compatibility.
            type: str
            sample: my_service_bus_rule_id
        event_hub_name:
            description:
                - The name of the event hub. If none is specified, the default event hub will be selected.
            type: str
            sample: myEventHub
        event_hub_authorization_rule_id:
            description:
                - The resource Id for the event hub authorization rule.
            type: str
            sample: my_event_hub_authorization_rule_id
        logs:
            description:
                - The list of logs settings.
            type: list
            contains:
                category:
                    description:
                        - Name of a Diagnostic Log category for a resource type this setting is applied to.
                    type: str
                enabled:
                    description:
                        - A value indicating whether this log is enabled.
                    type: bool
                retention_policy:
                    description:
                        - The retention policy for this category.
                    type: complex
                    contains:
                        enabled:
                            description:
                                - A value indicating whether the retention policy is enabled.
                            type: bool
                        days:
                            description:
                                - The number of days for the retention in days. A value of 0 will retain indefinitely.
                            type: int
        metrics:
            description:
                - The list of metric settings.
            type: list
            contains:
                time_grain:
                    description:
                        - The timegrain of the metric in ISO8601 format.
                    type: str
                category:
                    description:
                        - Name of a Diagnostic Metric category for a resource type this setting is applied to.
                    type: str
                enabled:
                    description:
                        - A value indicating whether this metric is enabled.
                    type: bool
                retention_policy:
                    description:
                        - The retention policy for this category.
                    type: complex
                    contains:
                        enabled:
                            description:
                                - A value indicating whether the retention policy is enabled.
                            type: bool
                        days:
                            description:
                                - The number of days for the retention in days. A value of 0 will retain indefinitely.
                            type: int
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
import datetime

try:
    from msrestazure.azure_exceptions import CloudError
except ImportError:
    # This is handled in azure_rm_common
    pass

retention_policy_object = dict(
    enabled=dict(type='bool', default=True),
    days=dict(type='int', default=0)
)

log_settings_object = dict(
    category=dict(type='str', required=True),
    enabled=dict(type='bool', default=True),
    retention_policy=retention_policy_object
)

metric_settings_object = dict(
    time_grain=dict(type='str'),
    category=dict(type='str', required=True),
    enabled=dict(type='bool', default=True),
    retention_policy=retention_policy_object
)


class AzureRMDiagnosticSetting(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_id=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            workspace_id=dict(type='str'),
            log_analytics_destination_type=dict(type='str', default=None, choices=['Dedicated', None]),
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
        self.log_analytics_destination_type = None
        self.storage_account_id = None
        self.service_bus_rule_id = None
        self.event_hub_name = None
        self.event_hub_authorization_rule_id = None
        self.logs = []
        self.metrics = []

        self.results = dict(changed=False)
        self.diagnostic_setting_dict = None

        super(AzureRMDiagnosticSetting, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=False,
                                                       supports_tags=True)

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
            self.results['state'] = dict(state='Deleted')

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

    def create_diagnostic_setting(self, existingDiagnosticSettingsResource=None):
        self.log("Create diagnostic setting {0}".format(self.name))
        resource = self.parse_resource_id(self)
        parameters = None

        self.results['changed'] = True
        if self.check_mode:
            diagnostic_setting_dict = dict(
                name=self.name,
                resource_id=self.resource_id
            )
            return diagnostic_setting_dict

        if not self.logs and not self.metrics:
            self.fail('Parameter error: must provide at least 1 log and/or metric categories when creating a diagnostic setting.')
        if not self.storage_account_id and not self.workspace_id and not self.service_bus_rule_id and not self.event_hub_name:
            self.fail('Parameter error: must provide at least 1 destination.')
        if not (self.event_hub_name ^ self.event_hub_authorization_rule_id):
            self.fail('Parameter error: must provide both event_hub_name and event_hub_authorization_rule_id if using an eventhub destination.')
        self.add_retention_policy_where_missing()

        if existingDiagnosticSettingsResource:
            parameters = self.monitor_client.models.DiagnosticSettingsResource(
                storage_account_id=self.storage_account_id,
                service_bus_rule_id=self.service_bus_rule_id,
                event_hub_authorization_rule_id=self.event_hub_authorization_rule_id,
                event_hub_name=self.event_hub_name,
                metrics=self.metrics,
                logs=self.logs,
                workspace_id=self.workspace_id,
                log_analytics_destination_type=self.log_analytics_destination_type
            )
        else:
            parameters = existingDiagnosticSettingsResource

        self.log(str(parameters))
        try:
            poller = self.monitor_client.diagnostic_setting.create(self.resource_id, self.name, parameters)
            self.get_poller_result(poller)
        except CloudError as e:
            self.log('Error creating diagnostic settings.')
            self.fail("Failed to create diagnostic settings: {0}".format(str(e)))

        return self.get_diagnostic_setting()

    def update_diagnostic_setting(self):
        self.log('Update diagnostic setting {0}'.format(self.name))

        self.results['changed'] = self.compare_diagnostic_settings(self.diagnostic_setting_dict())

        if self.results['changed']:
            update_error = None
            self.log("Updating diagnostic setting by deleting old:")
            try:
                self.delete_diagnostic_setting()
            except CloudError as e:
                self.log('Error updating diagnostic setting when deleting old.')
                update_error = e
            try:
                self.create_diagnostic_setting()
            except CloudError as e:
                self.log('Error updating diagnostic setting when creating new.')
                self.log('Re-creating old diagnostic setting.')
                existingDiagnosticSettingsResource = self.monitor_client.models.DiagnosticSettingsResource(
                    storage_account_id=self.diagnostic_setting_dict.get('storage_account_id'),
                    service_bus_rule_id=self.diagnostic_setting_dict.get('service_bus_rule_id'),
                    event_hub_authorization_rule_id=self.diagnostic_setting_dict.get('event_hub_authorization_rule_id'),
                    event_hub_name=self.diagnostic_setting_dict.get('event_hub_name'),
                    metrics=self.diagnostic_setting_dict.get('metrics'),
                    logs=self.diagnostic_setting_dict.get('logs'),
                    workspace_id=self.diagnostic_setting_dict.get('workspace_id'),
                    log_analytics_destination_type=self.diagnostic_setting_dict.get('log_analytics_destination_type')
                )
                self.create_diagnostic_setting(existingDiagnosticSettingsResource)
                update_error = e

            if update_error:
                self.fail("Failed to update diagnostic setting: {0}".format(str(update_error)))

        return self.get_diagnostic_setting()

    def delete_diagnostic_setting(self):
        self.log('Delete diagnostic setting {0}'.format(self.name))

        self.results['changed'] = True if self.diagnostic_setting is not None else False
        if not self.check_mode and self.diagnostic_setting is not None:
            try:
                status = self.monitor_client.diagnostic_settings.delete(self.resourceId, self.name)
                self.log("Delete status: ")
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
                    time_grain=entry.time_grain,
                    category=entry.category,
                    enabled=entry.enabled,
                    retention_policy=dict(
                        days=entry.retention_policy.days,
                        enabled=entry.retention_policy.enabled
                    ))
                diagnostic_setting_dict['metrics'].append(entry_item)

        diagnostic_setting_dict['logs'] = list()
        if diagnostic_setting_obj.logs:
            for entry in diagnostic_setting_obj.logs:
                entry_item = dict(
                    category=entry.category,
                    enabled=entry.enabled,
                    retention_policy=dict(
                        days=entry.retention_policy.days,
                        enabled=entry.retention_policy.enabled
                    ))
                diagnostic_setting_dict['logs'].append(entry_item)

        return diagnostic_setting_dict

    def parse_resource_id(self):
        sects = self.resource_id.split('/')

        if len(sects) != 9:
            self.fail("Invalid format, expecting: /subscriptions/{subscriptionId}/resourceGroups/{resGroup}/providers/{resType}/{resSubType}/{identity}")
        else:
            return {
                "subscription": sects[2],
                "resourceGroup": sects[4],
                "provider": sects[6] + '/' + sects[7],
                "name": sects[8]
            }

    def add_retention_policy_where_missing(self):
        infinite_retention_policy = dict(
            enabled=True,
            days=0
        )

        for index, log in enumerate(self.logs):
            if not log.retention_policy:
                self.logs[index] = infinite_retention_policy

        for index, metric in enumerate(self.metrics):
            if not metric.retention_policy:
                self.metrics[index] = infinite_retention_policy

    def compare_diagnostic_settings(self):
        changed = False

        if self.storage_account_id and self.diagnostic_setting_dict.get('storage_account_id') != self.storage_account_id:
            changed = True
        if self.service_bus_rule_id and self.diagnostic_setting_dict.get('service_bus_rule_id') != self.service_bus_rule_id:
            changed = True
        if self.event_hub_authorization_rule_id and self.diagnostic_setting_dict.get('event_hub_authorization_rule_id') != self.event_hub_authorization_rule_id:
            changed = True
        if self.event_hub_name and self.diagnostic_setting_dict.get('event_hub_name') != self.event_hub_name:
            changed = True
        if self.workspace_id and self.diagnostic_setting_dict.get('workspace_id') != self.workspace_id:
            changed = True
        if self.log_analytics_destination_type and self.diagnostic_setting_dict.get('log_analytics_destination_type') != self.log_analytics_destination_type:
            changed = True
        if not self.compare_lists(self.logs, self.diagnostic_setting_dict.get('logs')):
            changed = True
        if not self.compare_lists(self.metrics, self.diagnostic_setting_dict.get('metrics')):
            changed = True

        return changed

    def compare_lists(self, list1, list2):
        if len(list1) != len(list2):
            return False
        for element in list1:
            if element not in list2:
                return False
        return True


def main():
    AzureRMDiagnosticSetting()


if __name__ == '__main__':
    main()
