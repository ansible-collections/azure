#!/usr/bin/python
#
# Copyright (c) 2025 Klaas Demter (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitoractivitylogalerts
version_added: "3.7.0"
short_description: Create, update and delete Activity Log Alerts.
description:
    - Create, update and delete Activity Log Alerts.
    - >-
      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2020_10_01.aio.operations.activitylogalertsoperations?view=azure-python#azure-mgmt-monitor-v2020-10-01-aio-operations-activitylogalertsoperations-create-or-update)
    - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2020_10_01.models.activitylogalertresource?view=azure-python)

options:
    name:
        description:
            - The name of the activity log alert you're creating, updating or deleting.
        required: true
        type: str
    resource_group:
        description:
            - The name of the resource group
        required: true
        type: str
    location:
        description:
            - Location of the activity log alert.
            - Should be optional, but is not optional on creation.
            - U(https://github.com/Azure/azure-rest-api-specs/issues/35342)
            - Activity log alerts are usually 'Global'. On creation module will default to 'Global' if unspecified.
        required: false
        type: str
    scopes:
        description:
            - A list of resource IDs that will be used as prefixes.
            - The alert will only apply to Activity Log events with resource IDs that fall under one of these prefixes.
            - This list must include at least one item for creation.
        type: list
        elements: str
    condition:
        description:
            - The condition that will cause this alert to activate.
            - >-
              U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2020_10_01.models.alertruleallofcondition?view=azure-python)
        type: dict
        suboptions:
            all_of:
                description:
                    - The list of Activity Log Alert rule conditions.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2020_10_01.models.alertruleanyoforleafcondition?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    field:
                        description:
                            - The name of the Activity Log event's field that this condition will examine.
                            - The possible values for this field are (case-insensitive) resourceId, category, caller, level,
                              operationName, resourceGroup, resourceProvider, status, subStatus, resourceType
                              or anything beginning with properties.
                        type: str
                    equals:
                        description:
                            - The value of the events field will be compared to this value (case-insensitive) to determine if the condition is met.
                        type: str
                    contains_any:
                        description:
                            - The value of the events field will be compared to the values in this
                              array (case-insensitive) to determine if the condition is met.
                        type: list
                        elements: str
                    any_of:
                        description:
                            - An Activity Log Alert rule condition that is met when at least one of its member leaf conditions are met.
                            - >-
                              U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2020_10_01.models.alertruleleafcondition?view=azure-python)
                        type: list
                        elements: dict
                        suboptions:
                            field:
                                description:
                                    - The name of the Activity Log events field that this condition will examine. The possible values for this field are
                                      (case-insensitive) resourceId, category, caller, level, operationName, resourceGroup, resourceProvider,
                                      status, subStatus, resourceType, or anything beginning with properties.
                                type: str
                            equals:
                                description:
                                    - The value of the event's field will be compared to this value (case-insensitive) to determine if the condition is met.
                                type: str
                            contains_any:
                                description:
                                    - The value of the event's field will be compared to the values in this array
                                      (case-insensitive) to determine if the condition is met.
                                type: list
                                elements: str
    actions:
        description:
            - The actions that will activate when the condition is met.
            - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2020_10_01.models.actionlist?view=azure-python)
        type: dict
        suboptions:
            action_groups:
                description:
                    - The list of the Action Groups.
                    - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2020_10_01.models.actiongroup?view=azure-python)
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
                            - the dictionary of custom properties to include with the post operation. These data are appended to the webhook payload.
                        type: dict
    enabled:
        description:
            - Indicates whether this activity log alert is enabled.
            - If an activity log alert is not enabled, then none of its receivers will receive communications.
            - Server side default false -- should be true.
            - U(https://github.com/Azure/azure-rest-api-specs/issues/35343)
        type: bool
    description:
        description:
            - A description of this Activity Log Alert rule.
        type: str
    state:
        description:
            - State of the activity log alert.
            - Use C(present) for creating/updating a activity log alert.
            - Use C(absent) for deleting a activity log alert.
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
- name: Add a activity log alert
  azure.azcollection.azure_rm_monitoractivitylogalerts:
    state: present
    resource_group: resource_group_name
    location: global
    name: activity_log_alert_resource_health_example
    scopes:
      - /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name
    condition:
      all_of:
        - equals: ResourceHealth
          field: category
        - any_of:
            - equals: Unknown
              field: properties.currentHealthStatus
            - equals: Unavailable
              field: properties.currentHealthStatus
            - equals: Degraded
              field: properties.currentHealthStatus
        - any_of:
            - equals: Unknown
              field: properties.previousHealthStatus
            - equals: Unavailable
              field: properties.previousHealthStatus
            - equals: Degraded
              field: properties.previousHealthStatus
            - equals: Available
              field: properties.previousHealthStatus
        - any_of:
            - equals: PlatformInitiated
              field: properties.cause
    actions:
      action_groups:
        - action_group_id: \
/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/microsoft.insights/actionGroups/action_group_name

- name: Add tag to existing activity log alert
  azure.azcollection.azure_rm_monitoractivitylogalerts:
    state: present
    name: activity_log_alert_name
    resource_group: resource_group_name
    append_tags: true
    tags:
      ThisIsAnAddedExampleTag: ExampleValue

- name: Delete a activity log alert
  azure.azcollection.azure_rm_monitoractivitylogalerts:
    state: absent
    name: activity_log_alert_name
    resource_group: resource_group_name
'''

RETURN = '''
activitylogalert:
    description:
        - Details of the activity log alert
        - Is null on state==absent (activity log alert does not exist or will be deleted)
        - Assumes you make legal changes in check mode
    type: dict
    returned: always
    sample: {
        "actions": {
            "action_groups": [
                {
                    "action_group_id": \
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/microsoft.insights/actionGroups/action_group_name"
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
        "enabled": false,
        "id": \
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/Microsoft.Insights/activityLogAlerts/activity_log_alert_name",
        "location": "global",
        "name": "activity_log_alert_name",
        "scopes": [
            "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name"
        ],
        "tags": {},
        "type": "Microsoft.Insights/ActivityLogAlerts"
    }
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


try:
    from azure.core.exceptions import ResourceNotFoundError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'ActivityLogAlert'

any_of_all_of_condition_spec = dict(
    field=dict(type='str'),
    equals=dict(type='str'),
    contains_any=dict(type='list', elements='str')
)

all_of_condition_spec = dict(
    field=dict(type='str'),
    equals=dict(type='str'),
    contains_any=dict(type='list', elements='str'),
    any_of=dict(type='list', elements='dict', options=any_of_all_of_condition_spec)
)
condition_spec = dict(
    all_of=dict(type='list', elements='dict', options=all_of_condition_spec)
)

action_groups_actions_spec = dict(
    action_group_id=dict(type='str'),
    webhook_properties=dict(type='dict')
)

actions_spec = dict(
    action_groups=dict(type='list', elements='dict', options=action_groups_actions_spec)
)


class AzureRMMonitorActivityLogAlert(AzureRMModuleBaseExt):
    """Information class for an Azure RM Activity Log Alerts"""

    def __init__(self):
        # https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2020_10_01.models.activitylogalertresource?view=azure-python
        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            location=dict(type='str'),
            scopes=dict(type='list', elements='str'),
            condition=dict(type='dict', options=condition_spec),
            actions=dict(type='dict', options=actions_spec),
            enabled=dict(type='bool'),
            description=dict(type='str'),
            state=dict(type='str', choices=['present', 'absent'], default='present')
        )

        self.name = None
        self.resource_group = None
        self.location = None
        self.tags = None
        self.scopes = None
        self.condition = None
        self.actions = None
        self.enabled = None
        self.description = None
        self.state = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            activitylogalert=dict(),
            diff=dict(
                before=None,
                after=None
            )
        )

        super(AzureRMMonitorActivityLogAlert, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        # Get current activity log alert if it exists
        before_dict = self.get_activity_log_alert()

        # Create dict from input, without None values
        # hhttps://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2020_10_01.models.activitylogalertresource?view=azure-python
        activity_log_alert_template = {
            "location": self.location,
            "scopes": self.scopes,
            "condition": self.condition,
            "actions": self.actions,
            "enabled": self.enabled,
            "description": self.description
        }
        # Filter out all None values
        activity_log_alert_input = {key: value for key, value in activity_log_alert_template.items() if value is not None}

        # Create/Update if state==present
        if self.state == 'present':
            if before_dict is None:
                # activity log alert does not exist, create
                # On creation default to location of resource group unless otherwise noted in input variables
                if not self.location:
                    activity_log_alert_input['location'] = 'Global'
                # On creation input == what we send to api
                activity_log_alert_update = activity_log_alert_input
                # Needs to be extended by tags if set
                if self.tags:
                    activity_log_alert_update['tags'] = self.tags
                self.results['changed'] = True
                if self.check_mode:
                    # Check mode, skipping actual creation
                    pass
                else:
                    create_response = self.create_or_update(activity_log_alert_update)
            else:
                # activity log alert already exists, updating it
                # Dict for update is the union of existing object overwritten by input data
                activity_log_alert_update = before_dict | activity_log_alert_input

                # Enhanced with tags (special behaviour because of append_tags possibility)
                update_tags, update_tags_content = self.update_tags(before_dict.get('tags'))
                # Check if we need to update the activity log alert
                if update_tags or not self.default_compare({}, activity_log_alert_update, before_dict, '', result_compare):
                    activity_log_alert_update['tags'] = update_tags_content
                    # Need to create/update the activity log alert; changed -> True
                    self.results['changed'] = True
                    if self.check_mode:
                        # Check mode, skipping actual creation
                        pass
                    else:
                        create_response = self.create_or_update(activity_log_alert_update)

            if self.check_mode or not self.results['changed']:
                # When object was not updated or when running in check mode
                # assume activity_log_alert_update is resulting object
                result = activity_log_alert_update
            else:
                # otherwise take resulting new object from response of create call
                result = create_response

        # Delete activity log alert if state is absent and it exists
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
        self.results['activitylogalert'] = result

        return self.results

    def get_activity_log_alert(self):
        '''
        Gets the properties of the specified activity log alert.

        :return: List of Activity Log Alerts
        '''
        self.log("Checking if activity log alert {0} in resource group {1} is present".format(self.name,
                                                                                              self.resource_group))

        result = None
        response = None

        try:
            response = self.monitor_management_client_activity_log_alerts.activity_log_alerts.get(activity_log_alert_name=self.name,
                                                                                                  resource_group_name=self.resource_group)
        except ResourceNotFoundError as ex:
            self.log("Could not find activity log alert {0} in resource group {1}".format(self.name, self.resource_group))
        if response:
            result = self.serialize_obj(response, AZURE_OBJECT_CLASS)

        return result

    def create_or_update(self, activity_log_alert_update):
        result = None
        response = None
        activity_log_alerts = self.monitor_management_client_activity_log_alerts.activity_log_alerts
        try:
            response = activity_log_alerts.create_or_update(resource_group_name=self.resource_group,
                                                            activity_log_alert_name=self.name,
                                                            activity_log_alert_rule=activity_log_alert_update,
                                                            logging_enable=False)
        except Exception as ex:
            self.fail("Error creating or update activity log alert {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

        if response:
            result = self.serialize_obj(response, AZURE_OBJECT_CLASS)

        return result

    def delete(self):
        response = None
        try:
            response = self.monitor_management_client_activity_log_alerts.activity_log_alerts.delete(resource_group_name=self.resource_group,
                                                                                                     activity_log_alert_name=self.name)
        except Exception as ex:
            self.fail("Error deleting activity log alert {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

        return response


def main():
    """Main execution"""
    AzureRMMonitorActivityLogAlert()


if __name__ == '__main__':
    main()
