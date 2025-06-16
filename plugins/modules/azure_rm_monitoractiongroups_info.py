#!/usr/bin/python
#
# Copyright (c) 2025 Klaas Demter (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitoractiongroups_info
version_added: "3.7.0"
short_description: Get Action Groups
description:
    - Get Action Groups

options:
    name:
        description:
            - The name of the action group you're trying to get details about.
        type: str
    resource_group:
        description:
            - The name of the resource group in which the action group is (if you use name)
            - The name of the resource group where you want to list Action Groups (if you don't use name)
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Klaas Demter (@Klaas-)
'''

EXAMPLES = '''
- name: Get action group details
  azure.azcollection.azure_rm_monitoractiongroups_info:
    name: DCRName
    resource_group: Resource_Group_Name

- name: Get all Action Groups in specific resource group
  azure.azcollection.azure_rm_monitoractiongroups_info:
    resource_group: Resource_Group_Name

- name: Get all Action Groups in the current subscription
  azure.azcollection.azure_rm_monitoractiongroups_info:
'''

RETURN = '''
actiongroups:
    description:
        - List of Action Groups
        - Can be empty if listing Action Groups
    type: list
    returned: always
    sample: [
        {
            "arm_role_receivers": [],
            "automation_runbook_receivers": [],
            "azure_app_push_receivers": [],
            "azure_function_receivers": [],
            "email_receivers": [
                {
                    "email_address": "mail@example.com",
                    "name": "sendmailtoexample",
                    "status": "Enabled",
                    "use_common_alert_schema": true
                }
            ],
            "enabled": true,
            "event_hub_receivers": [],
            "group_short_name": "aaa",
            "id": \
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/microsoft.insights/actionGroups/action_group_name",
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
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'actiongroups'


class AzureRMactiongroupsInfo(AzureRMModuleBase):
    """Information class for an Azure RM Action Groups"""

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
            actiongroups=[]
        )

        super(AzureRMactiongroupsInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False,
                                                      facts_module=True,
                                                      required_by=self.required_by)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            result = self.get_action_group()
        else:
            result = self.list_action_groups()

        self.results['actiongroups'] = result

        return self.results

    def get_action_group(self):
        '''
        Gets the properties of the specified action group.

        :return: List of Action Groups
        '''
        self.log("Checking if action group {0} in resource group {1} is present".format(self.name,
                                                                                        self.resource_group))

        result = []
        action_group = None

        try:
            action_group = self.monitor_management_client_action_groups.action_groups.get(action_group_name=self.name,
                                                                                          resource_group_name=self.resource_group)
        except ResourceNotFoundError as ex:
            self.log("Could not find action group {0} in resource group {1}".format(self.name, self.resource_group))
            return []
        except HttpResponseError as ex:
            if ex.error.code == 'InvalidSubscriptionId':
                self.log("Could not find subscription id")
                return []
            else:
                raise Exception(ex)
        if action_group:
            result = [self.serialize_obj(action_group, AZURE_OBJECT_CLASS)]

        return result

    def list_action_groups(self):
        '''
        Gets the properties of the specified Action Groups in resource group or subscription.

        :return: List of Action Groups
        '''

        result = []
        action_groups = None

        if self.resource_group:
            self.log("Checking if the Action Groups in resource group {0} are present".format(self.resource_group))
            action_groups_mgmt_client = self.monitor_management_client_action_groups.action_groups
            action_groups = action_groups_mgmt_client.list_by_resource_group(resource_group_name=self.resource_group)
        else:
            self.log("Checking if the Action Groups are present in subscription")
            action_groups = self.monitor_management_client_action_groups.action_groups.list_by_subscription_id()
        if action_groups:
            # it seems the exception is thrown when iterating through action_groups, not when setting action_groups
            try:
                for item in action_groups:
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
    AzureRMactiongroupsInfo()


if __name__ == '__main__':
    main()
