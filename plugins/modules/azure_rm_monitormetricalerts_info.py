#!/usr/bin/python
#
# Copyright (c) 2025 Klaas Demter (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitormetricalerts_info
version_added: "3.7.0"
short_description: Get metric alerts
description:
    - Get metric alerts

options:
    name:
        description:
            - The name of the metric alert you're trying to get details about.
        type: str
    resource_group:
        description:
            - The name of the resource group in which the metric alert is (if you use name)
            - The name of the resource group where you want to list metric alerts (if you don't use name)
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Klaas Demter (@Klaas-)
'''

EXAMPLES = '''
- name: Get metric alert details
  azure.azcollection.azure_rm_monitormetricalerts_info:
    name: metric_alert_name
    resource_group: resource_group_name

- name: Get all metric alerts in specific resource group
  azure.azcollection.azure_rm_monitormetricalerts_info:
    resource_group: resource_group_name

- name: Get all metric alerts in the current subscription
  azure.azcollection.azure_rm_monitormetricalerts_info:
'''

RETURN = '''
metricalerts:
    description:
        - List of metric alerts
        - Can be empty if listing metric alerts or metric alert does not exist
    type: list
    returned: always
    sample: [
        {
            "actions": [
                {
                    "action_group_id": \
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/microsoft.insights/actionGroups/action_group_name"
                }
            ],
            "auto_mitigate": true,
            "criteria": {
                "all_of": [
                    {
                        "criterion_type": "StaticThresholdCriterion",
                        "dimensions": [
                            {
                                "name": "dataSourceURL",
                                "operator": "Include",
                                "values": [
                                    "*"
                                ]
                            },
                            {
                                "name": "healthStatus",
                                "operator": "Exclude",
                                "values": [
                                    "Healthy"
                                ]
                            }
                        ],
                        "metric_name": "BackupHealthEvent",
                        "metric_namespace": "Microsoft.RecoveryServices/vaults",
                        "name": "Metric1",
                        "operator": "GreaterThan",
                        "skip_metric_validation": false,
                        "threshold": 0.0,
                        "time_aggregation": "Count"
                    }
                ],
                "odata_type": "Microsoft.Azure.Monitor.MultipleResourceMultipleMetricCriteria"
            },
            "description": "Alert on Backup Health Events",
            "enabled": true,
            "evaluation_frequency": "PT1H",
            "id": \
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/Microsoft.Insights/metricAlerts/metric_alert",
            "location": "Global",
            "name": "Monitoring-e-app-name-Backup_Health",
            "scopes": [
                "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/Microsoft.RecoveryServices/vaults/recovery_vault_name"
            ],
            "severity": 3,
            "tags": {
                "TestTag1": "TestValue1"
            },
            "target_resource_type": "Microsoft.RecoveryServices/vaults",
            "type": "Microsoft.Insights/metricAlerts",
            "window_size": "P1D"
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'metricalerts'


class AzureRMmetricalertsInfo(AzureRMModuleBase):
    """Information class for an Azure RM metric alerts"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str', required=False),
            resource_group=dict(type='str', required=False),
        )

        self.required_by = {
            'name': 'resource_group'
        }

        self.name = None
        self.resource_group = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            metricalerts=[]
        )

        super(AzureRMmetricalertsInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False,
                                                      facts_module=True,
                                                      required_by=self.required_by)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            result = self.get_metric_alert()
        else:
            result = self.list_metric_alerts()

        self.results['metricalerts'] = result

        return self.results

    def get_metric_alert(self):
        '''
        Gets the properties of the specified metric alert.

        :return: List of metric alerts
        '''
        self.log("Checking if metric alert {0} in resource group {1} is present".format(self.name,
                                                                                        self.resource_group))

        result = []
        metric_alert = None

        try:
            metric_alert = self.monitor_management_client_metric_alerts.metric_alerts.get(rule_name=self.name,
                                                                                          resource_group_name=self.resource_group)
        except ResourceNotFoundError as ex:
            self.log("Could not find metric alert {0} in resource group {1}".format(self.name, self.resource_group))
            return []
        except HttpResponseError as ex:
            if ex.error.code == 'InvalidSubscriptionId':
                self.log("Could not find subscription id")
                return []
            else:
                raise Exception(ex)
        if metric_alert:
            result = [self.serialize_obj(metric_alert, AZURE_OBJECT_CLASS)]

        return result

    def list_metric_alerts(self):
        '''
        Gets the properties of the specified metric alerts in resource group or subscription.

        :return: List of metric alerts
        '''

        result = []
        metric_alerts = None

        if self.resource_group:
            self.log("Checking if the metric alerts in resource group {0} are present".format(self.resource_group))
            metric_alerts_mgmt_client = self.monitor_management_client_metric_alerts.metric_alerts
            metric_alerts = metric_alerts_mgmt_client.list_by_resource_group(resource_group_name=self.resource_group)
        else:
            self.log("Checking if the metric alerts are present in subscription")
            metric_alerts = self.monitor_management_client_metric_alerts.metric_alerts.list_by_subscription()
        if metric_alerts:
            # it seems the exception is thrown when iterating through metric_alerts, not when setting metric_alerts
            try:
                for item in metric_alerts:
                    result.append(self.serialize_obj(item, AZURE_OBJECT_CLASS))
            except ResourceNotFoundError as ex:
                self.log("Could not find resource group {0}".format(self.resource_group))
            except HttpResponseError as ex:
                if ex.error.code == 'InvalidSubscriptionId':
                    self.log("Could not find subscription id")
                else:
                    raise Exception(ex)

        return result


def main():
    """Main execution"""
    AzureRMmetricalertsInfo()


if __name__ == '__main__':
    main()
