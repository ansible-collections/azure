#!/usr/bin/python
#
# Copyright (c) 2025 Klaas Demter (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitoractiongroups
version_added: "3.7.0"
short_description: Create, update and delete Action Groups.
description:
    - Create, update and delete Action Groups.
    - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.actiongroupresource?view=azure-python)

options:
    name:
        description:
            - The name of the action group you're creating/changing.
        required: true
        type: str
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    location:
        description:
            - Location of the action group.
            - defaults to location of exiting action group or location of the resource group if unspecified.
            - Action groups are usually 'Global'.
        required: false
        type: str
    group_short_name:
        description:
            - The short name of the action group. This will be used in SMS messages.
        type: str
    enabled:
        description:
            - Indicates whether this action group is enabled. If an action group is not enabled, then none of its receivers will receive communications.
        type: bool
    email_receivers:
        description:
            - The list of email receivers that are part of this action group.
            - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.emailreceiver?view=azure-python)
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of this receiver. Names must be unique across all receivers within an action group.
                    - Required when setting this receiver.
                type: str
            email_address:
                description:
                    - The email address of this receiver.
                    - Required when setting this receiver.
                type: str
            use_common_alert_schema:
                description:
                    - Indicates whether to use common alert schema.
                    - Defaults to False when not set (server side default).
                type: bool
    sms_receivers:
        description:
            - The list of SMS receivers that are part of this action group.
            - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.smsreceiver?view=azure-python)
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name this receiver. Names must be unique across all receivers within an action group.
                    - Required when setting this receiver.
                type: str
            country_code:
                description:
                    - The country code of the SMS receiver.
                    - Required when setting this receiver.
                type: str
            phone_number:
                description:
                    - The phone number of the SMS receiver.
                    - Required when setting this receiver.
                type: str
    webhook_receivers:
        description:
            - The list of webhook receivers that are part of this action group.
            - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.webhookreceiver?view=azure-python)
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of this receiver. Names must be unique across all receivers within an action group.
                    - Required when setting this receiver.
                type: str
            service_uri:
                description:
                    - The URI where webhooks should be sent.
                    - Required when setting this receiver.
                type: str
            use_common_alert_schema:
                description:
                    - Indicates whether to use common alert schema.
                    - Defaults to False when not set (server side default).
                type: bool
            use_aad_auth:
                description:
                    - Indicates whether or not use AAD authentication.
                    - Defaults to False when not set (server side default).
                type: bool
            object_id:
                description:
                    - Indicates the webhook app object Id for aad auth.
                type: str
            identifier_uri:
                description:
                    - Indicates the identifier uri for aad auth.
                type: str
            tenant_id:
                description:
                    - Indicates the tenant id for aad auth.
                type: str
    itsm_receivers:
        description:
            - The list of webhook receivers that are part of this action group.
            - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.itsmreceiver?view=azure-python)
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of this receiver. Names must be unique across all receivers within an action group.
                    - Required when setting this receiver.
                type: str
            workspace_id:
                description:
                    - OMS LA instance identifier.
                    - Required when setting this receiver.
                type: str
            connection_id:
                description:
                    - Unique identification of ITSM connection among multiple defined in above workspace.
                    - Required when setting this receiver.
                type: str
            ticket_configuration:
                description:
                    - JSON blob for the configurations of the ITSM action. CreateMultipleWorkItems option will be part of this blob as well.
                    - Required when setting this receiver.
                type: str
            region:
                description:
                    - Region in which workspace resides.
                    - Required when setting this receiver.
                type: str
    azure_app_push_receivers:
        description:
            - The list of AzureAppPush receivers that are part of this action group.
            - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.azureapppushreceiver?view=azure-python)
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of this receiver. Names must be unique across all receivers within an action group.
                    - Required when setting this receiver.
                type: str
            email_address:
                description:
                    - The email address registered for the Azure mobile app.
                    - Required when setting this receiver.
                type: str
    automation_runbook_receivers:
        description:
            - The list of AutomationRunbook receivers that are part of this action group.
            - >-
              U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.automationrunbookreceiver?view=azure-python)
        type: list
        elements: dict
        suboptions:
            automation_account_id:
                description:
                    - The Azure automation account Id which holds this runbook and authenticate to Azure resource.
                    - Required when setting this receiver.
                type: str
            runbook_name:
                description:
                    - The name for this runbook.
                    - Required when setting this receiver.
                type: str
            webhook_resource_id:
                description:
                    - The resource id for webhook linked to this runbook.
                    - Required when setting this receiver.
                type: str
            is_global_runbook:
                description:
                    - Indicates whether this instance is global runbook.
                type: bool
            name:
                description:
                    - Indicates name of the webhook.
                type: str
            service_uri:
                description:
                    - The URI where webhooks should be sent.
                type: str
            use_common_alert_schema:
                description:
                    - Indicates whether to use common alert schema.
                    - Defaults to False when not set (server side default).
                type: bool
    voice_receivers:
        description:
            - The list of voice receivers that are part of this action group.
            - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.voicereceiver?view=azure-python)
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name this receiver. Names must be unique across all receivers within an action group.
                    - Required when setting this receiver.
                type: str
            country_code:
                description:
                    - The country code of the voice receiver.
                    - Required when setting this receiver.
                type: str
            phone_number:
                description:
                    - The phone number of the voice receiver.
                    - Required when setting this receiver.
                type: str
    logic_app_receivers:
        description:
            - The list of logic app receivers that are part of this action group.
            - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.logicappreceiver?view=azure-python)
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name this receiver. Names must be unique across all receivers within an action group.
                    - Required when setting this receiver.
                type: str
            resource_id:
                description:
                    - The azure resource id of the logic app receiver.
                    - Required when setting this receiver.
                type: str
            callback_url:
                description:
                    - The callback url where http request sent to.
                    - Required when setting this receiver.
                type: str
            use_common_alert_schema:
                description:
                    - Indicates whether to use common alert schema.
                    - Defaults to False when not set (server side default).
                type: bool
    azure_function_receivers:
        description:
            - The list of azure function receivers that are part of this action group.
            - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.azurefunctionreceiver?view=azure-python)
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name this receiver. Names must be unique across all receivers within an action group.
                    - Required when setting this receiver.
                type: str
            function_app_resource_id:
                description:
                    - The azure resource id of the function app.
                    - Required when setting this receiver.
                type: str
            function_name:
                description:
                    - The function name in the function app.
                    - Required when setting this receiver.
                type: str
            http_trigger_url:
                description:
                    - The http trigger url where http request sent to.
                    - Required when setting this receiver.
                type: str
            use_common_alert_schema:
                description:
                    - Indicates whether to use common alert schema.
                    - Defaults to False when not set (server side default).
                type: bool
    arm_role_receivers:
        description:
            - The list of ARM role receivers that are part of this action group. Roles are Azure RBAC roles and only built-in roles are supported.
            - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.armrolereceiver?view=azure-python)
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name this receiver. Names must be unique across all receivers within an action group.
                    - Required when setting this receiver.
                type: str
            role_id:
                description:
                    - The arm role id.
                    - Required when setting this receiver.
                type: str
            use_common_alert_schema:
                description:
                    - Indicates whether to use common alert schema.
                    - Defaults to False when not set (server side default).
                type: bool
    event_hub_receivers:
        description:
            - The list of event hub receivers that are part of this action group.
            - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.eventhubreceiver?view=azure-python)
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name this receiver. Names must be unique across all receivers within an action group.
                    - Required when setting this receiver.
                type: str
            event_hub_name_space:
                description:
                    - The Event Hub namespace.
                    - Required when setting this receiver.
                type: str
            event_hub_name:
                description:
                    - The name of the specific Event Hub queue.
                    - Required when setting this receiver.
                type: str
            use_common_alert_schema:
                description:
                    - Indicates whether to use common alert schema.
                    - Defaults to False when not set (server side default).
                type: bool
            tenant_id:
                description:
                    - The tenant Id for the subscription containing this event hub.
                type: str
            subscription_id:
                description:
                    - The Id for the subscription containing this event hub.
                    - Required when setting this receiver.
                type: str
    state:
        description:
            - State of the action group.
            - Use C(present) for creating/updating a action group.
            - Use C(absent) for deleting a action group.
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
- name: Add a action group
  azure.azcollection.azure_rm_monitoractiongroups:
    state: present
    name: action_group_name
    resource_group: resource_group_name
    enabled: true
    location: Global
    email_receivers:
      - email_address: xxx@hostname.tld
        name: sendmail
        use_common_alert_schema: true
    group_short_name: short_name
    append_tags: false
    tags:
      ThisIsAnExampleTag: ExampleValue

- name: Add tag to existing action group
  azure.azcollection.azure_rm_monitoractiongroups:
    state: present
    name: action_group_name
    resource_group: resource_group_name
    append_tags: true
    tags:
      ThisIsAnAddedExampleTag: ExampleValue

- name: Remove all tags on existing action group
  azure.azcollection.azure_rm_monitoractiongroups:
    state: present
    name: action_group_name
    resource_group: resource_group_name
    append_tags: false

- name: Delete a action group
  azure.azcollection.azure_rm_monitoractiongroups:
    state: absent
    name: action_group_name
    resource_group: resource_group_name
'''

RETURN = '''
actiongroup:
    description:
        - Details of the action group
        - Is null on state==absent (action group does not exist or will be deleted)
        - Assumes you make legal changes in check mode
    type: dict
    returned: always
    sample: {
        "arm_role_receivers": [],
        "automation_runbook_receivers": [],
        "azure_app_push_receivers": [],
        "azure_function_receivers": [],
        "email_receivers": [
            {
                "email_address": "xxx@hostname.tld",
                "name": "sendmail",
                "use_common_alert_schema": true
            }
        ],
        "enabled": true,
        "event_hub_receivers": [],
        "group_short_name": "shortname",
        "id": \
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resougce_group_name/providers/microsoft.insights/actionGroups/action_group_name",
        "itsm_receivers": [],
        "location": "Global",
        "logic_app_receivers": [],
        "name": "action_group_name",
        "sms_receivers": [],
        "tags": {},
        "type": "Microsoft.Insights/ActionGroups",
        "voice_receivers": [],
        "webhook_receivers": []
    }
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'ActionGroup'

email_receivers_spec = dict(
    name=dict(type='str'),
    email_address=dict(type='str'),
    use_common_alert_schema=dict(type='bool')
)

sms_receivers_spec = dict(
    name=dict(type='str'),
    country_code=dict(type='str'),
    phone_number=dict(type='str')
)

webhook_receivers_spec = dict(
    name=dict(type='str'),
    service_uri=dict(type='str'),
    use_common_alert_schema=dict(type='bool'),
    use_aad_auth=dict(type='bool'),
    object_id=dict(type='str'),
    identifier_uri=dict(type='str'),
    tenant_id=dict(type='str')
)

itsm_receivers_spec = dict(
    name=dict(type='str'),
    workspace_id=dict(type='str'),
    connection_id=dict(type='str'),
    ticket_configuration=dict(type='str'),
    region=dict(type='str')
)

azure_app_push_receivers_spec = dict(
    name=dict(type='str'),
    email_address=dict(type='str')
)

automation_runbook_receivers_spec = dict(
    automation_account_id=dict(type='str'),
    runbook_name=dict(type='str'),
    webhook_resource_id=dict(type='str'),
    is_global_runbook=dict(type='bool'),
    name=dict(type='str'),
    service_uri=dict(type='str'),
    use_common_alert_schema=dict(type='bool')
)

voice_receivers_spec = dict(
    name=dict(type='str'),
    country_code=dict(type='str'),
    phone_number=dict(type='str')
)

logic_app_receivers_spec = dict(
    name=dict(type='str'),
    resource_id=dict(type='str'),
    callback_url=dict(type='str'),
    use_common_alert_schema=dict(type='bool')
)

azure_function_receivers_spec = dict(
    name=dict(type='str'),
    function_app_resource_id=dict(type='str'),
    function_name=dict(type='str'),
    http_trigger_url=dict(type='str'),
    use_common_alert_schema=dict(type='bool')
)

arm_role_receivers_spec = dict(
    name=dict(type='str'),
    role_id=dict(type='str'),
    use_common_alert_schema=dict(type='bool')
)

event_hub_receivers_spec = dict(
    name=dict(type='str'),
    event_hub_name_space=dict(type='str'),
    event_hub_name=dict(type='str'),
    use_common_alert_schema=dict(type='bool'),
    tenant_id=dict(type='str'),
    subscription_id=dict(type='str')
)


class AzureRMActionGroup(AzureRMModuleBaseExt):
    """Information class for an Azure RM Action Groups"""

    def __init__(self):
        # https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.actiongroupresource?view=azure-python
        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            location=dict(type='str'),
            group_short_name=dict(type='str'),
            enabled=dict(type='bool'),
            email_receivers=dict(type='list', elements='dict', options=email_receivers_spec),
            sms_receivers=dict(type='list', elements='dict', options=sms_receivers_spec),
            webhook_receivers=dict(type='list', elements='dict', options=webhook_receivers_spec),
            itsm_receivers=dict(type='list', elements='dict', options=itsm_receivers_spec),
            azure_app_push_receivers=dict(type='list', elements='dict', options=azure_app_push_receivers_spec),
            automation_runbook_receivers=dict(type='list', elements='dict', options=automation_runbook_receivers_spec),
            voice_receivers=dict(type='list', elements='dict', options=voice_receivers_spec),
            logic_app_receivers=dict(type='list', elements='dict', options=logic_app_receivers_spec),
            azure_function_receivers=dict(type='list', elements='dict', options=azure_function_receivers_spec),
            arm_role_receivers=dict(type='list', elements='dict', options=arm_role_receivers_spec),
            event_hub_receivers=dict(type='list', elements='dict', options=event_hub_receivers_spec),
            state=dict(type='str', choices=['present', 'absent'], default='present')
        )

        self.name = None
        self.resource_group = None
        self.location = None
        self.group_short_name = None
        self.enabled = None
        self.email_receivers = None
        self.sms_receivers = None
        self.webhook_receivers = None
        self.itsm_receivers = None
        self.azure_app_push_receivers = None
        self.automation_runbook_receivers = None
        self.voice_receivers = None
        self.logic_app_receivers = None
        self.azure_function_receivers = None
        self.arm_role_receivers = None
        self.event_hub_receivers = None
        self.state = None
        self.tags = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            actiongroup=dict(),
            diff=dict(
                before=None,
                after=None
            )
        )

        super(AzureRMActionGroup, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        # Get current action group if it exists
        before_dict = self.get_action_group()

        # Create dict from input, without None values
        # https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2023_01_01.models.actiongroupresource?view=azure-python
        action_group_template = {
            "location": self.location,
            "group_short_name": self.group_short_name,
            "enabled": self.enabled,
            "email_receivers": self.email_receivers,
            "sms_receivers": self.sms_receivers,
            "webhook_receivers": self.webhook_receivers,
            "itsm_receivers": self.itsm_receivers,
            "azure_app_push_receivers": self.azure_app_push_receivers,
            "automation_runbook_receivers": self.automation_runbook_receivers,
            "voice_receivers": self.voice_receivers,
            "logic_app_receivers": self.logic_app_receivers,
            "azure_function_receivers": self.azure_function_receivers,
            "arm_role_receivers": self.arm_role_receivers,
            "event_hub_receivers": self.event_hub_receivers,
        }
        # Filter out all None values
        action_group_input = {key: value for key, value in action_group_template.items() if value is not None}

        # Create/Update if state==present
        if self.state == 'present':
            if before_dict is None:
                # action group does not exist, create
                # On creation default to location of resource group unless otherwise noted in input variables
                if not self.location:
                    resource_group = self.get_resource_group(self.resource_group)
                    action_group_input['location'] = resource_group.location
                # On creation input == what we send to api
                action_group_update = action_group_input
                # Needs to be extended by tags if set
                if self.tags:
                    action_group_update['tags'] = self.tags
                self.results['changed'] = True
                if self.check_mode:
                    # Check mode, skipping actual creation
                    pass
                else:
                    create_response = self.create_or_update(action_group_update)
            else:
                # action group already exists, updating it
                # Dict for update is the union of existing object overwritten by input data
                action_group_update = before_dict | action_group_input

                # Enhanced with tags (special behaviour because of append_tags possibility)
                update_tags, update_tags_content = self.update_tags(before_dict.get('tags'))
                if update_tags or not self.default_compare({}, action_group_update, before_dict, '', result_compare):
                    action_group_update['tags'] = update_tags_content
                    self.results['changed'] = True
                    if self.check_mode:
                        # Check mode, skipping actual creation
                        pass
                    else:
                        create_response = self.create_or_update(action_group_update)

            if self.check_mode or not self.results['changed']:
                # When object was not updated or when running in check mode
                # assume action_group_update is resulting object
                result = action_group_update
            else:
                # otherwise take resulting new object from response of create call
                result = create_response

        # Delete action group if state is absent and it exists
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
        self.results['actiongroup'] = result

        return self.results

    def get_action_group(self):
        '''
        Gets the properties of the specified action group.

        :return: List of Action Groups
        '''
        self.log("Checking if action group {0} in resource group {1} is present".format(self.name,
                                                                                        self.resource_group))

        result = None
        response = None

        try:
            response = self.monitor_management_client_action_groups.action_groups.get(action_group_name=self.name,
                                                                                      resource_group_name=self.resource_group)
        except ResourceNotFoundError as ex:
            self.log("Could not find action group {0} in resource group {1}".format(self.name, self.resource_group))
        if response:
            result = self.serialize_obj(response, AZURE_OBJECT_CLASS)

        return result

    def create_or_update(self, action_group_update):
        result = None
        response = None
        try:
            response = self.monitor_management_client_action_groups.action_groups.create_or_update(resource_group_name=self.resource_group,
                                                                                                   action_group_name=self.name,
                                                                                                   action_group=action_group_update,
                                                                                                   logging_enable=False)
        except Exception as ex:
            self.fail("Error creating or update action group {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

        if response:
            result = self.serialize_obj(response, AZURE_OBJECT_CLASS)

        return result

    def delete(self):
        response = None
        try:
            response = self.monitor_management_client_action_groups.action_groups.delete(resource_group_name=self.resource_group,
                                                                                         action_group_name=self.name)
        except Exception as ex:
            self.fail("Error deleting action group {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

        return response


def main():
    """Main execution"""
    AzureRMActionGroup()


if __name__ == '__main__':
    main()
