#!/usr/bin/python
#
# Copyright (c) 2025 Klaas Demter (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitoractivitylogalerts_info
version_added: "3.7.0"
short_description: Get Activity log alerts
description:
    - Get Activity log alerts

options:
    name:
        description:
            - The name of the activity log alert you're trying to get details about.
        type: str
    resource_group:
        description:
            - The name of the resource group in which the activity log alert is (if you use name)
            - The name of the resource group where you want to list Activity log alerts (if you don't use name)
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Klaas Demter (@Klaas-)
'''

EXAMPLES = '''
- name: Get activity log alert details
  azure.azcollection.azure_rm_monitoractivitylogalerts_info:
    name: activity_log_alert_name
    resource_group: resource_group_name

- name: Get all Activity log alerts in specific resource group
  azure.azcollection.azure_rm_monitoractivitylogalerts_info:
    resource_group: resource_group_name

- name: Get all Activity log alerts in the current subscription
  azure.azcollection.azure_rm_monitoractivitylogalerts_info:
'''

RETURN = '''
activitylogalerts:
    description:
        - List of Activity log alerts
        - Can be empty if listing Activity log alerts
    type: list
    returned: always
    sample: [
        {
            "actions": {
                "action_groups": [
                    {
                        "action_group_id": \
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/Microsoft.Insights/actionGroups/action_group_name",
                        "webhook_properties": {}
                    }
                ]
            },
            "condition": {
                "all_of": [
                    {
                        "equals": "ResourceHealth",
                        "field": "category"
                    },
                    {
                        "any_of": [
                            {
                                "equals": "Unknown",
                                "field": "properties.currentHealthStatus"
                            },
                            {
                                "equals": "Unavailable",
                                "field": "properties.currentHealthStatus"
                            },
                            {
                                "equals": "Degraded",
                                "field": "properties.currentHealthStatus"
                            }
                        ]
                    },
                    {
                        "any_of": [
                            {
                                "equals": "Unknown",
                                "field": "properties.previousHealthStatus"
                            },
                            {
                                "equals": "Unavailable",
                                "field": "properties.previousHealthStatus"
                            },
                            {
                                "equals": "Degraded",
                                "field": "properties.previousHealthStatus"
                            },
                            {
                                "equals": "Available",
                                "field": "properties.previousHealthStatus"
                            }
                        ]
                    },
                    {
                        "any_of": [
                            {
                                "equals": "PlatformInitiated",
                                "field": "properties.cause"
                            }
                        ]
                    }
                ]
            },
            "description": "Good description of the alert",
            "enabled": true,
            "id": \
"/subscriptions/xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/Microsoft.Insights/activityLogAlerts/activity_log_alert_name",
            "location": "global",
            "name": "activity_log_alert_name",
            "scopes": [
                "/subscriptions/xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name"
            ],
            "tags": {},
            "type": "Microsoft.Insights/ActivityLogAlerts"
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'activitylogalerts'


class AzureRMactivitylogalertsInfo(AzureRMModuleBase):
    """Information class for an Azure RM Activity log alerts"""

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
            activitylogalerts=[]
        )

        super(AzureRMactivitylogalertsInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                           supports_check_mode=True,
                                                           supports_tags=False,
                                                           facts_module=True,
                                                           required_by=self.required_by)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            result = self.get_activity_log_alert()
        else:
            result = self.list_activity_log_alerts()

        self.results['activitylogalerts'] = result

        return self.results

    def get_activity_log_alert(self):
        '''
        Gets the properties of the specified activity log alert.

        :return: List of Activity log alerts
        '''
        self.log("Checking if activity log alert {0} in resource group {1} is present".format(self.name,
                                                                                              self.resource_group))

        result = []
        activity_log_alert = None

        try:
            activity_log_alert = self.monitor_management_client_activity_log_alerts.activity_log_alerts.get(activity_log_alert_name=self.name,
                                                                                                            resource_group_name=self.resource_group)
        except ResourceNotFoundError as ex:
            self.log("Could not find activity log alert {0} in resource group {1}".format(self.name, self.resource_group))
            return []
        except HttpResponseError as ex:
            if ex.error.code == 'InvalidSubscriptionId':
                self.log("Could not find subscription id")
                return []
            else:
                raise Exception(ex)
        if activity_log_alert:
            result = [self.serialize_obj(activity_log_alert, AZURE_OBJECT_CLASS)]

        return result

    def list_activity_log_alerts(self):
        '''
        Gets the properties of the specified Activity log alerts in resource group or subscription.

        :return: List of Activity log alerts
        '''

        result = []
        activity_log_alerts = None

        if self.resource_group:
            self.log("Checking if the Activity log alerts in resource group {0} are present".format(self.resource_group))
            activity_log_alerts_mgmt_client = self.monitor_management_client_activity_log_alerts.activity_log_alerts
            activity_log_alerts = activity_log_alerts_mgmt_client.list_by_resource_group(resource_group_name=self.resource_group)
        else:
            self.log("Checking if the Activity log alerts are present in subscription")
            activity_log_alerts = self.monitor_management_client_activity_log_alerts.activity_log_alerts.list_by_subscription_id()
        if activity_log_alerts:
            # it seems the exception is thrown when iterating through activity_log_alerts, not when setting activity_log_alerts
            try:
                for item in activity_log_alerts:
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
    AzureRMactivitylogalertsInfo()


if __name__ == '__main__':
    main()
