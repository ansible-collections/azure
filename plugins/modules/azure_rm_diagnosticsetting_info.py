#!/usr/bin/python
#
# Copyright (c) 2021 Alvin Ramoutar, (@AlvinRamoutar)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_diagnosticsetting_info
version_added: "0.1.0"
short_description: Get Azure Diagnostic Setting info
description:
    - Get Azure Diagnostic Setting info.

options:
    resource_id:
        description:
            - The resource ID of the resource in which has the diagnostic setting.
        required: true
        type: str
        aliases:
            - resource
            - id
    name:
        description:
            - The name of the Diagnostic Setting.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Alvin Ramoutar (@AlvinRamoutar)

'''

EXAMPLES = '''
  - name: Get Diagnostic Setting info of 'myDiagnosticSetting' from resource with id 'myResourceId'
    azure_rm_diagnosticsetting_info:
      resource_id: myResourceId
      name: myDiagnosticSetting

  - name: Get Diagnostic Settings info of all from resource with id 'myResourceId'
    azure_rm_diagnosticsetting_info:
      resource_id: myResourceId
'''

RETURN = '''
diagnostic_setting:
    description:
        - A list of dictionaries containing facts for Diagnostic Settings.
    returned: always
    type: complex
    contains:
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

try:
    from msrestazure.azure_exceptions import CloudError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMDiagnosticSettingInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_id=dict(type='str', aliases=['resource', 'id'])
        )

        self.results = dict(
            changed=False,
            diagnostic_settings=[]
        )

        self.name = None
        self.resource_id = None

        super(AzureRMDiagnosticSettingInfo, self).__init__(self.module_arg_spec,
                                                           supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.parse_resource_id()

        if self.name and not self.resource_id:
            self.fail("Parameter error: must provide resource ID if providing diagnostic setting name.")

        results = []
        if self.name:
            results = self.get_diagnostic_setting()
        else:
            results = self.list_diagnostic_setting()

        self.results['diagnostic_setting'] = results
        return self.results

    def get_diagnostic_setting(self):
        self.log('Get properties for diagnostic setting {0}'.format(self.name))
        diagnostic_setting_obj = None

        try:
            diagnostic_setting_obj = self.monitor_client.diagnostic_settings.get(self.resourceId, self.name)
        except CloudError:
            pass

        if diagnostic_setting_obj:
            return [self.diagnostic_setting_obj_to_dict(diagnostic_setting_obj)]

        return list()

    def list_diagnostic_setting(self):
        self.log('Get properties for all diagnostic settings in {0}'.format(self.resource_id))
        diagnostic_setting_obj = None
        results = list()

        try:
            diagnostic_setting_collection_obj = self.monitor_client.diagnostic_settings.list(self.resourceId)
        except CloudError:
            pass

        if diagnostic_setting_collection_obj:
            for diagnostic_setting in diagnostic_setting_collection_obj:
                results.append(self.diagnostic_setting_obj_to_dict(diagnostic_setting))
            return results

        return list()

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
            self.fail("Invalid format, expecting: /subscriptions/{subscriptionId}/resourceGroups/{resGroupName}/providers/{resType}/{resSubType}/{identity}")
        else:
            return {
                "subscription": sects[2],
                "resourceGroup": sects[4],
                "provider": sects[6] + '/' + sects[7],
                "name": sects[8]
            }


def main():
    AzureRMDiagnosticSettingInfo()


if __name__ == '__main__':
    main()
