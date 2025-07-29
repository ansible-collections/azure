#!/usr/bin/python
#
# Copyright (c) 2025 Klaas Demter (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitormetricalerts
version_added: "3.7.0"
short_description: Create, update and delete metric alerts.
description:
    - Create, update and delete metric alerts.
    - >-
      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2018_03_01.operations.metricalertsoperations?view=azure-python#azure-mgmt-monitor-v2018-03-01-operations-metricalertsoperations-create-or-update)
    - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2018_03_01.models.metricalertresource?view=azure-python)
options:
    name:
        description:
            - The name of the metric alert you're creating, updateing or deleting.
        required: true
        type: str
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    location:
        description:
            - Location of the metric alert.
            - Metric alerts are usually 'Global'.
            - If unspecified will default to 'Global' on creation.
        required: false
        type: str
    description:
        description:
            - A description of this metric alert rule.
        type: str
    severity:
        description:
            - Severity 1-4 of the alert.
            - Required on creation.
        type: int
    enabled:
        description:
            - Indicates whether this metric alert is enabled.
            - If an metric alert is not enabled, then none of its receivers will receive communications.
            - Required on creation.
        type: bool
    scopes:
        description:
            - A list of resource IDs that will be used as prefixes.
            - The alert will only apply to Metric events with resource IDs that fall under one of these prefixes.
            - This list must include at least one item for creation.
        type: list
        elements: str
    evaluation_frequency:
        description:
            - How often the metric alert is evaluated represented in ISO 8601 duration format.
            - U(https://en.wikipedia.org/wiki/ISO_8601#Durations)
            - Required for creation.
        type: str
    window_size:
        description:
            - The period of time (in ISO 8601 duration format) that is used to monitor alert activity based on the threshold.
            - U(https://en.wikipedia.org/wiki/ISO_8601#Durations)
            - Required for creation.
        type: str
    target_resource_type:
        description:
            - The resource type of the target resource(s) on which the alert is created/updated.
            - Mandatory (for creation) if the scope contains a subscription, resource group, or more than one resource.
        type: str
    target_resource_region:
        description:
            - The region of the target resource(s) on which the alert is created/updated.
            - Mandatory (for creation) if the scope contains a subscription, resource group, or more than one resource.
        type: str
    criteria:
        description:
            - Defines the specific alert criteria information.
            - Required for creation.
        type: dict
        suboptions:
            extra_keys:
                description:
                    - U(https://learn.microsoft.com/en-us/rest/api/monitor/metric-alerts/create-or-update?view=rest-monitor-2018-03-01&tabs=HTTP#request-body)
                    - extra keys depends on the odata_type
                type: dict
            odata_type:
                description:
                    - Specifies the type of the alert criteria.
                    - Required on creation.
                type: str
                choices:
                    - Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria
                    - Microsoft.Azure.Monitor.MultipleResourceMultipleMetricCriteria
                    - Microsoft.Azure.Monitor.WebtestLocationAvailabilityCriteria
    auto_mitigate:
        description:
            - the flag that indicates whether the alert should be auto resolved or not. The default is true.
        type: bool
    actions:
        description:
            - The actions that will activate when the condition is met.
            - U(https://learn.microsoft.com/en-us/rest/api/monitor/metric-alerts/create-or-update?view=rest-monitor-2018-03-01&tabs=HTTP#metricalertaction)
        type: list
        elements: dict
        suboptions:
            action_group_id:
                description:
                    - The resource ID of the Action Group.
                    - Must be set when setting an action group.
                type: str
            webhook_properties:
                description:
                    - The dictionary of custom properties to include with the post operation. These data are appended to the webhook payload.
                type: dict
    state:
        description:
            - State of the metric alert
            - Use C(present) for creating/updating a metric alert.
            - Use C(absent) for deleting a metric alert.
        default: present
        type: str
        choices:
            - present
            - absent
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Klaas Demter (@Klaas-)
'''

EXAMPLES = '''
- name: Add a metric alert
  azure.azcollection.azure_rm_monitormetricalerts:
    state: present
    resource_group: resource_group_name
    location: Global
    name: metric_alert_name
    actions:
      - action_group_id: \
/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/microsoft.insights/actionGroups/action_group_name
    auto_mitigate: true
    criteria:
      all_of:
        - criterion_type: StaticThresholdCriterion
          dimensions:
            - name: dataSourceURL
              operator: Include
              values:
                - '*'
            - name: healthStatus
              operator: Exclude
              values:
                - Healthy
          metric_name: BackupHealthEvent
          metric_namespace: Microsoft.RecoveryServices/vaults
          name: Metric1
          operator: GreaterThan
          skip_metric_validation: false
          threshold: 0.0
          time_aggregation: Count
      odata_type: Microsoft.Azure.Monitor.MultipleResourceMultipleMetricCriteria
    description: Alert on Backup Health Events
    enabled: true
    evaluation_frequency: PT1H
    scopes:
      - /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/Microsoft.RecoveryServices/vaults/recovery_vault_name
    severity: 3
    tags:
      TestTag1: TestValue1
    target_resource_type: Microsoft.RecoveryServices/vaults
    window_size: P1D

- name: Add tag to existing metric alert
  azure.azcollection.azure_rm_monitormetricalerts:
    state: present
    name: metric_alert_name
    resource_group: resource_group_name
    append_tags: true
    tags:
      ThisIsAnAddedExampleTag: ExampleValue

- name: Delete a metric alert
  azure.azcollection.azure_rm_monitormetricalerts:
    state: absent
    name: metric_alert_name
    resource_group: resource_group_name
'''

RETURN = '''
metricalert:
    description:
        - Details of the metric alert
        - Is null on state==absent (metric alert does not exist or will be deleted)
        - Assumes you make legal changes in check mode
    type: dict
    returned: always
    sample: {
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
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/Microsoft.Insights/metricAlerts/metric_alert_name",
        "location": "Global",
        "name": "metric_alert_name",
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
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'MetricAlert'

actions_spec = dict(
    action_group_id=dict(type='str'),
    webhook_properties=dict(type='dict')
)


class AzureRMMonitorMetricAlert(AzureRMModuleBaseExt):
    """Information class for an Azure RM metric alerts"""

    def __init__(self):
        # https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2020_10_01.models.MetricAlertresource?view=azure-python
        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            location=dict(type='str'),
            description=dict(type='str'),
            severity=dict(type='int'),
            enabled=dict(type='bool'),
            scopes=dict(type='list', elements='str'),
            evaluation_frequency=dict(type='str'),
            window_size=dict(type='str'),
            target_resource_type=dict(type='str'),
            target_resource_region=dict(type='str'),
            # https://github.com/ansible/ansible/issues/74001
            # Can't properly define criteria in arg spec
            criteria=dict(type='dict'),
            auto_mitigate=dict(type='bool'),
            actions=dict(type='list', elements='dict', options=actions_spec),
            state=dict(type='str', choices=['present', 'absent'], default='present')
        )

        self.name = None
        self.resource_group = None
        self.location = None
        self.tags = None
        self.description = None
        self.severity = None
        self.enabled = None
        self.scopes = None
        self.evaluation_frequency = None
        self.window_size = None
        self.target_resource_type = None
        self.target_resource_region = None
        self.criteria = None
        self.auto_mitigate = None
        self.actions = None
        self.state = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            metricalert=dict(),
            diff=dict(
                before=None,
                after=None
            )
        )

        super(AzureRMMonitorMetricAlert, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        # Defaults for variables
        result = None
        result_compare = dict(compare=[])
        before_dict = None

        # Get current metric alert if it exists
        before_dict = self.get_metric_alert()

        # Create dict from input, without None values
        # https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2018_03_01.models.metricalertresource?view=azure-python
        # tags seperately because of update_tags behavior
        metric_alert_template = {
            "location": self.location,
            "description": self.description,
            "severity": self.severity,
            "enabled": self.enabled,
            "scopes": self.scopes,
            "evaluation_frequency": self.evaluation_frequency,
            "window_size": self.window_size,
            "target_resource_type": self.target_resource_type,
            "target_resource_region": self.target_resource_region,
            "criteria": self.criteria,
            "auto_mitigate": self.auto_mitigate,
            "actions": self.actions
        }
        # Filter out all None values
        metric_alert_input = {key: value for key, value in metric_alert_template.items() if value is not None}

        # Create/Update if state==present
        if self.state == 'present':
            if before_dict is None:
                # metric alert does not exist, create
                # On creation default to 'Global' unless otherwise noted in input variables
                if not self.location:
                    metric_alert_input['location'] = 'Global'
                # On creation input == what we send to api
                metric_alert_update = metric_alert_input
                # Needs to be extended by tags if set
                if self.tags:
                    metric_alert_update['tags'] = self.tags
                self.results['changed'] = True
                if self.check_mode:
                    # Check mode, skipping actual creation
                    pass
                else:
                    create_response = self.create_or_update(metric_alert_update)
            else:
                # metric alert already exists, updating it
                # Dict for update is the union of existing object overwritten by input data
                metric_alert_update = before_dict | metric_alert_input

                # Enhanced with tags (special behaviour because of append_tags possibility)
                update_tags, update_tags_content = self.update_tags(before_dict.get('tags'))
                # Check if we need to update the metric alert
                if update_tags or not self.default_compare({}, metric_alert_update, before_dict, '', result_compare):
                    metric_alert_update['tags'] = update_tags_content
                    # Need to create/update the metric alert; changed -> True
                    self.results['changed'] = True
                    if self.check_mode:
                        # Check mode, skipping actual creation
                        pass
                    else:
                        create_response = self.create_or_update(metric_alert_update)

            if self.check_mode or not self.results['changed']:
                # When object was not updated or when running in check mode
                # assume metric_alert_update is resulting object
                result = metric_alert_update
            else:
                # otherwise take resulting new object from response of create call
                result = create_response

        # Delete metric alert if state is absent and it exists
        # if it doesn't exist, it's already absent
        elif self.state == 'absent' and before_dict is not None:
            self.results['changed'] = True
            if self.check_mode:
                # do not delete in check mode
                pass
            else:
                self.delete()

        self.results['diff']['before'] = before_dict
        self.results['diff']['after'] = result
        self.results['metricalert'] = result

        return self.results

    def get_metric_alert(self):
        '''
        Gets the properties of the specified metric alert.

        :return: List of metric alerts
        '''
        self.log("Checking if metric alert {0} in resource group {1} is present".format(self.name,
                                                                                        self.resource_group))

        result = None
        response = None

        try:
            response = self.monitor_management_client_metric_alerts.metric_alerts.get(rule_name=self.name,
                                                                                      resource_group_name=self.resource_group)
        except ResourceNotFoundError as ex:
            self.log("Could not find metric alert {0} in resource group {1}".format(self.name, self.resource_group))
        if response:
            result = self.serialize_obj(response, AZURE_OBJECT_CLASS)

        return result

    def create_or_update(self, metric_alert_update):
        result = None
        response = None
        metric_alerts = self.monitor_management_client_metric_alerts.metric_alerts
        try:
            response = metric_alerts.create_or_update(resource_group_name=self.resource_group,
                                                      rule_name=self.name,
                                                      parameters=metric_alert_update,
                                                      logging_enable=False)
        except Exception as ex:
            self.fail("Error creating or update metric alert {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

        if response:
            result = self.serialize_obj(response, AZURE_OBJECT_CLASS)

        return result

    def delete(self):
        response = None
        try:
            response = self.monitor_management_client_metric_alerts.metric_alerts.delete(resource_group_name=self.resource_group,
                                                                                         rule_name=self.name)
        except Exception as ex:
            self.fail("Error deleting metric alert {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

        return response


def main():
    """Main execution"""
    AzureRMMonitorMetricAlert()


if __name__ == '__main__':
    main()
