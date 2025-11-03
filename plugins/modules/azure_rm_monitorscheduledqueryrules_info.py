#!/usr/bin/python
#
# Copyright (c) 2025 Klaas Demter (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitorscheduledqueryrules_info
version_added: "3.11.0"
short_description: Get Scheduled query rules
description:
    - Get Scheduled query rules
    - These rules are also called Log search alert rules

options:
    name:
        description:
            - The name of the scheduled query rule you're trying to get details about.
        type: str
    resource_group:
        description:
            - The name of the resource group in which the scheduled query rule is (if you use name)
            - The name of the resource group where you want to list Scheduled query rules (if you don't use name)
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Klaas Demter (@Klaas-)
'''

EXAMPLES = '''
- name: Get scheduled query rule details
  azure.azcollection.azure_rm_monitorscheduledqueryrules_info:
    name: scheduled_query_rule_name
    resource_group: resource_group_name

- name: Get all Scheduled query rules in specific resource group
  azure.azcollection.azure_rm_monitorscheduledqueryrules_info:
    resource_group: resource_group_name

- name: Get all Scheduled query rules in the current subscription
  azure.azcollection.azure_rm_monitorscheduledqueryrules_info:
'''

RETURN = '''
scheduledqueryrules:
    description:
        - List of Scheduled query rules
        - Can be empty if listing Scheduled query rules
    type: list
    returned: always
    sample: [
        {
            "action": {
                "azns_action": {
                    "action_group": [
                        "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/microsoft.insights/actionGroups/action_group_name"
                    ],
                    "email_subject": ""
                },
                "odata_type": \
"Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.AlertingAction",
                "severity": "2",
                "trigger": {
                    "metric_trigger": {
                        "metric_column": "InstanceName,_ResourceId",
                        "metric_trigger_type": "Total",
                        "threshold": 1.0,
                        "threshold_operator": "GreaterThanOrEqual"
                    },
                    "threshold": 10.0,
                    "threshold_operator": "LessThan"
                }
            },
            "auto_mitigate": true,
            "created_with_api_version": "2018-04-16",
            "description": "Monitoring: Disks/logical volumes with less than 10% free space",
            "display_name": "scheduled_query_alert_name",
            "enabled": "true",
            "id": \
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/microsoft.insights/scheduledqueryrules/scheduled_query_alert_name",
            "last_updated_time": "2025-10-30T16:07:30.773011Z",
            "location": "eastus",
            "name": "scheduled_query_alert_name",
            "provisioning_state": "Succeeded",
            "schedule": {
                "frequency_in_minutes": 5,
                "time_window_in_minutes": 5
            },
            "source": {
                "authorized_resources": [],
                "data_source_id": \
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/Microsoft.OperationalInsights/workspaces/log_analytics_workspace_names",
                "query": "actual query",
                "query_type": "ResultCount"
            },
            "tags": {},
            "type": "Microsoft.Insights/scheduledQueryRules"
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'scheduledqueryrules'


class AzureRMscheduledqueryrulesInfo(AzureRMModuleBase):
    """Information class for an Azure RM Scheduled query rules"""

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
            scheduledqueryrules=[]
        )

        super(AzureRMscheduledqueryrulesInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                             supports_check_mode=True,
                                                             supports_tags=False,
                                                             facts_module=True,
                                                             required_by=self.required_by)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            result = self.get_scheduled_query_rule()
        else:
            result = self.list_scheduled_query_rules()

        self.results['scheduledqueryrules'] = result

        return self.results

    def get_scheduled_query_rule(self):
        '''
        Gets the properties of the specified scheduled query rule.

        :return: List of Scheduled query rules
        '''
        self.log("Checking if scheduled query rule {0} in resource group {1} is present".format(self.name,
                                                                                                self.resource_group))

        result = []
        scheduled_query_rule = None

        try:
            scheduled_query_rule = self.monitor_management_client_scheduled_query_rules.scheduled_query_rules.get(rule_name=self.name,
                                                                                                                  resource_group_name=self.resource_group)
        except ResourceNotFoundError as ex:
            self.log("Could not find scheduled query rule {0} in resource group {1}".format(self.name, self.resource_group))
            return []
        except HttpResponseError as ex:
            if ex.error.code == 'InvalidSubscriptionId':
                self.log("Could not find subscription id")
                return []
            else:
                raise Exception(ex)
        if scheduled_query_rule:
            result = [self.serialize_obj(scheduled_query_rule, AZURE_OBJECT_CLASS)]

        return result

    def list_scheduled_query_rules(self):
        '''
        Gets the properties of the specified Scheduled query rules in resource group or subscription.

        :return: List of Scheduled query rules
        '''

        result = []
        scheduled_query_rules = None

        if self.resource_group:
            self.log("Checking if the Scheduled query rules in resource group {0} are present".format(self.resource_group))
            scheduled_query_rules_mgmt_client = self.monitor_management_client_scheduled_query_rules.scheduled_query_rules
            scheduled_query_rules = scheduled_query_rules_mgmt_client.list_by_resource_group(resource_group_name=self.resource_group)
        else:
            self.log("Checking if the Scheduled query rules are present in subscription")
            scheduled_query_rules = self.monitor_management_client_scheduled_query_rules.scheduled_query_rules.list_by_subscription()
        if scheduled_query_rules:
            # it seems the exception is thrown when iterating through scheduled_query_rules, not when setting scheduled_query_rules
            try:
                for item in scheduled_query_rules:
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
    AzureRMscheduledqueryrulesInfo()


if __name__ == '__main__':
    main()
