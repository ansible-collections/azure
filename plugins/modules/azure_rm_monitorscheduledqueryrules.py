#!/usr/bin/python
#
# Copyright (c) 2025 Klaas Demter (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitorscheduledqueryrules
version_added: "3.11.0"
short_description: Create, update and delete Scheduled query rules
description:
    - Create, update and delete Scheduled query rules

options:
    name:
        description:
            - The name of the scheduled query rule you're creating/changing
        required: true
        type: str
    resource_group:
        description:
            - The name of the resource group
        required: true
        type: str
    location:
        description:
            - Location of the scheduled query rule
            - Scheduled query rules are usually reside at the location of your log analytics workspace.
        required: false
        type: str
    action:
        description:
            - The actions that will activate when the condition is met
        type: dict
        suboptions:
            azns_action:
                description: Azure action group reference
                type: dict
                suboptions:
                    action_group:
                        description:
                            - The list of the Action Group IDs
                        type: list
                        elements: str
                    email_subject:
                        description:
                            - Custom subject override for all email ids in Azure action group
                        type: str
            odata_type:
                description: Specifies the action
                type: str
                choices:
                    - AlertingAction
                    - LogToMetricAction
                    - >-
                      Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.AlertingAction
            severity:
                description: Severity of the alert
                type: int
                choices:
                    - 0
                    - 1
                    - 2
                    - 3
                    - 4
            trigger:
                description: The trigger condition that results in the alert rule being.
                type: dict
                suboptions:
                    metric_trigger:
                        description: The trigger condition that results in the alert rule being.
                        type: dict
                        suboptions:
                            metric_column:
                                description: Evaluation of metric on a particular column.
                                type: str
                            metric_trigger_type:
                                description: Metric Trigger Type.
                                type: str
                                choices:
                                    - Consecutive
                                    - Total
                            threshold:
                                description: The threshold of the metric trigger.
                                type: float
                            threshold_operator:
                                description: Evaluation operation for Metric.
                                type: str
                                choices:
                                    - GreaterThanOrEqual
                                    - GreaterThan
                                    - LessThan
                                    - Equal
                    threshold:
                        description: Result or count threshold based on which rule should be triggered.
                        type: float
                    threshold_operator:
                        description: Result or count threshold based on which rule should be triggered.
                        type: str
                        choices:
                            - GreaterThanOrEqual
                            - GreaterThan
                            - LessThan
    source:
        description: Data Source against which rule will Query Data.
        type: dict
        suboptions:
            authorized_resources:
                description: List of Resource referred into query.
                type: list
                elements: str
            data_source_id:
                description: The resource uri over which log search query is to be run.
                type: str
            query:
                description: Log search query. Required for action type - AlertingAction.
                type: str
            query_type:
                description: Set value to 'ResultCount'.
                type: str
                choices:
                    - ResultCount
    schedule:
        description: Schedule (Frequency, Time Window) for rule. Required for action type - AlertingAction.
        type: dict
        suboptions:
            frequency_in_minutes:
                description: Frequency (in minutes) at which rule condition should be evaluated.
                type: int
            time_window_in_minutes:
                description: Time window for which data needs to be fetched for query (should be greater than or equal to frequencyInMinutes).
                type: int
    enabled:
        description:
            - The flag which indicates whether the Log Search rule is enabled.
        type: str
        choices:
          - "False"
          - "True"
    auto_mitigate:
        description:
            - The flag that indicates whether the alert should be automatically resolved or not.
        type: bool
    description:
        description:
            - The description of the Log Search rule.
        type: str
    display_name:
        description:
            - The display name of the alert rule.
        type: str
    state:
        description:
            - State of the scheduled query rule
            - Use C(present) for creating/updating a scheduled query rule.
            - Use C(absent) for deleting a scheduled query rule.
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
- name: Add a scheduled query rule
  azure.azcollection.azure_rm_monitorscheduledqueryrules:
    state: present
    resource_group: resource_group_name
    name: scheduled_query_rule_name
    location: eastus
    action:
      azns_action:
        action_group:
          - /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/microsoft.insights/actionGroups/action_group_name
        email_subject: ''
      odata_type: \
Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.AlertingAction
      severity: 2
      trigger:
        metric_trigger:
          metric_column: InstanceName,_ResourceId
          metric_trigger_type: Total
          threshold: 1
          threshold_operator: GreaterThanOrEqual
        threshold: 10
        threshold_operator: LessThan
    auto_mitigate: true
    description: 'Monitoring: Disks/logical volumes with less than 10% free space'
    display_name: Free_Space_Severity_2_Percentage
    enabled: "true"
    schedule:
      frequency_in_minutes: 5
      time_window_in_minutes: 5
    source:
      authorized_resources: []
      data_source_id: \
/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/Microsoft.OperationalInsights/workspaces/log_analytics_workspace_name
      query: >
        Perf
        | where CounterName == "% Free Space"
        | where InstanceName != "total"
        | summarize AggregatedValue = max(CounterValue) by bin(TimeGenerated, 5m), _ResourceId, InstanceName
      query_type: ResultCount


- name: Add tag to existing scheduled query rule
  azure.azcollection.azure_rm_monitorscheduledqueryrules:
    state: present
    name: scheduled_query_rule_name
    resource_group: resource_group_name
    append_tags: true
    tags:
      ThisIsAnAddedExampleTag: ExampleValue

- name: Delete a scheduled query rule
  azure.azcollection.azure_rm_monitorscheduledqueryrules:
    state: absent
    name: scheduled_query_rule_name
    resource_group: resource_group_name
'''

RETURN = '''
scheduledqueryrule:
    description:
        - Details of the scheduled query rule
        - Is null on state==absent (scheduled query rule does not exist or will be deleted)
        - Assumes you make legal changes in check mode
    type: dict
    returned: always
    sample: {
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
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'scheduledqueryrule'

azns_action_spec = dict(
    action_group=dict(type='list', elements='str'),
    email_subject=dict(type='str')
)

metric_trigger_spec = dict(
    metric_column=dict(type='str'),
    metric_trigger_type=dict(type='str', choices=['Consecutive', 'Total']),
    threshold=dict(type='float'),
    threshold_operator=dict(type='str', choices=[
        "GreaterThanOrEqual",
        "GreaterThan",
        "LessThan",
        "Equal"
    ])
)

trigger_spec = dict(
    metric_trigger=dict(type='dict', options=metric_trigger_spec),
    threshold=dict(type='float'),
    threshold_operator=dict(type='str', choices=[
        "GreaterThanOrEqual",
        "GreaterThan",
        "LessThan"
    ])
)

action_spec = dict(
    azns_action=dict(type='dict', options=azns_action_spec),
    odata_type=dict(type='str', choices=[
        'AlertingAction',
        'LogToMetricAction',
        'Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.AlertingAction'
    ]),
    severity=dict(type='int', choices=[0, 1, 2, 3, 4]),
    trigger=dict(type='dict', options=trigger_spec)
)

schedule_spec = dict(
    frequency_in_minutes=dict(type='int'),
    time_window_in_minutes=dict(type='int')
)

source_spec = dict(
    authorized_resources=dict(type='list', elements='str'),
    data_source_id=dict(type='str'),
    query=dict(type='str'),
    query_type=dict(type='str', choices=['ResultCount'])
)


class AzureRMMonitorscheduledqueryrule(AzureRMModuleBaseExt):
    """Information class for an Azure RM Scheduled query rules"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            location=dict(type='str'),
            action=dict(type='dict', options=action_spec),
            auto_mitigate=dict(type='bool'),
            description=dict(type='str'),
            display_name=dict(type='str'),
            enabled=dict(type='str', choices=['True', 'False']),
            schedule=dict(type='dict', options=schedule_spec),
            source=dict(type='dict', options=source_spec),
            state=dict(type='str', choices=['present', 'absent'], default='present')
        )

        self.name = None
        self.resource_group = None
        self.location = None
        self.tags = None
        self.action = None
        self.auto_mitigate = None
        self.description = None
        self.display_name = None
        self.enabled = None
        self.schedule = None
        self.source = None
        self.state = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            scheduledqueryrule=dict(),
            diff=dict(
                before=None,
                after=None
            )
        )

        super(AzureRMMonitorscheduledqueryrule, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        # Get current scheduled query rule if it exists
        before_dict = self.get_scheduled_query_rule()

        # Create dict from input, without None values
        scheduled_query_rule_template = {
            "location": self.location,
            "action": self.action,
            "auto_mitigate": self.auto_mitigate,
            "description": self.description,
            "display_name": self.display_name,
            "enabled": self.enabled,
            "schedule": self.schedule,
            "source": self.source
        }
        # Filter out all None values
        scheduled_query_rule_input = {key: value for key, value in scheduled_query_rule_template.items() if value is not None}

        # Create/Update if state==present
        if self.state == 'present':
            if before_dict is None:
                # scheduled query rule does not exist, create
                # On creation default to location of resource group unless otherwise noted in input variables
                if not self.location:
                    resource_group = self.get_resource_group(self.resource_group)
                    scheduled_query_rule_input['location'] = resource_group.location
                # On creation input == what we send to api
                scheduled_query_rule_update = scheduled_query_rule_input
                # Needs to be extended by tags if set
                if self.tags:
                    scheduled_query_rule_update['tags'] = self.tags
                self.results['changed'] = True
                if self.check_mode:
                    # Check mode, skipping actual creation
                    pass
                else:
                    create_response = self.create_or_update(scheduled_query_rule_update)
            else:
                # scheduled query rule already exists, updating it
                # Dict for update is the union of existing object overwritten by input data
                scheduled_query_rule_update = before_dict | scheduled_query_rule_input

                # Enhanced with tags (special behaviour because of append_tags possibility)
                update_tags, update_tags_content = self.update_tags(before_dict.get('tags'))
                # Check if we need to update the scheduled query rule
                if update_tags or not self.default_compare({}, scheduled_query_rule_update, before_dict, '', result_compare):
                    scheduled_query_rule_update['tags'] = update_tags_content
                    # Need to create/update the scheduled query rule; changed -> True
                    self.results['changed'] = True
                    if self.check_mode:
                        # Check mode, skipping actual creation
                        pass
                    else:
                        create_response = self.create_or_update(scheduled_query_rule_update)

            if self.check_mode or not self.results['changed']:
                # When object was not updated or when running in check mode
                # assume scheduled_query_rule_update is resulting object
                result = scheduled_query_rule_update
            else:
                # otherwise take resulting new object from response of create call
                result = create_response

        # Delete scheduled query rule if state is absent and it exists
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
        self.results['scheduledqueryrule'] = result

        return self.results

    def get_scheduled_query_rule(self):
        '''
        Gets the properties of the specified scheduled query rule.

        :return: List of Scheduled query rules
        '''
        self.log("Checking if scheduled query rule {0} in resource group {1} is present".format(self.name,
                                                                                                self.resource_group))

        result = None
        response = None

        try:
            response = self.monitor_management_client_scheduled_query_rules.scheduled_query_rules.get(rule_name=self.name,
                                                                                                      resource_group_name=self.resource_group)
        except ResourceNotFoundError as ex:
            self.log("Could not find scheduled query rule {0} in resource group {1}".format(self.name, self.resource_group))
        if response:
            result = self.serialize_obj(response, AZURE_OBJECT_CLASS)

        return result

    def create_or_update(self, scheduled_query_rule_update):
        result = None
        response = None
        scheduled_query_rules = self.monitor_management_client_scheduled_query_rules.scheduled_query_rules
        try:
            response = scheduled_query_rules.create_or_update(resource_group_name=self.resource_group,
                                                              rule_name=self.name,
                                                              parameters=scheduled_query_rule_update,
                                                              logging_enable=False)
        except Exception as ex:
            self.fail("Error creating or update scheduled query rule {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

        if response:
            result = self.serialize_obj(response, AZURE_OBJECT_CLASS)

        return result

    def delete(self):
        response = None
        try:
            response = self.monitor_management_client_scheduled_query_rules.scheduled_query_rules.delete(resource_group_name=self.resource_group,
                                                                                                         rule_name=self.name)
        except Exception as ex:
            self.fail("Error deleting scheduled query rule {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

        return response


def main():
    """Main execution"""
    AzureRMMonitorscheduledqueryrule()


if __name__ == '__main__':
    main()
