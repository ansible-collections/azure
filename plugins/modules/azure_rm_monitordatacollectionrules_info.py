#!/usr/bin/python
#
# Copyright (c) 2025 Klaas Demter (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitordatacollectionrules_info
version_added: "3.7.0"
short_description: Get Data Collection Rules
description:
    - Get Data Collection Rules

options:
    name:
        description:
            - The name of the data collection rule you're trying to get details about.
        type: str
    resource_group:
        description:
            - The name of the resource group in which the data collection rule is (if you use name)
            - The name of the resource group where you want to list data collection rules (if you don't use name)
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Klaas Demter (@Klaas-)
'''

EXAMPLES = '''
- name: Get data collection rule details
  azure.azcollection.azure_rm_monitordatacollectionrules_info:
    name: DCRName
    resource_group: Resource_Group_Name

- name: Get all data collection rules in specific resource group
  azure.azcollection.azure_rm_monitordatacollectionrules_info:
    resource_group: Resource_Group_Name

- name: Get all data collection rules in the current subscription
  azure.azcollection.azure_rm_monitordatacollectionrules_info:
'''

RETURN = '''
datacollectionrules:
    description:
        - List of data collection rules
        - Can be empty if listing data collection rules
    type: list
    returned: always
    sample: [
        {
            "data_flows": [...],
            "data_sources": {},
            "description": "Description of your data collection rule",
            "destinations": {},
            "etag": "str",
            "id": \
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/Microsoft.Insights/dataCollectionRules/data_collection_rule_name",
            "immutable_id": "dcr-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "kind": "Linux",
            "location": "westeurope",
            "name": "data_collection_rule_name",
            "provisioning_state": "Succeeded",
            "system_data": {
                "created_at": "2025-01-01T00:00:00.000000Z",
                "created_by": "xxx@domain.tld",
                "created_by_type": "User",
                "last_modified_at": "2025-01-01T00:00:00.000000Z",
                "last_modified_by": "xxx@domain.tld",
                "last_modified_by_type": "User"
            },
            "tags": {},
            "type": "Microsoft.Insights/dataCollectionRules"
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'DataCollectionRules'


class AzureRMDataCollectionRulesInfo(AzureRMModuleBase):
    """Information class for an Azure RM Data Collection Rules"""

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
            datacollectionrules=[]
        )

        super(AzureRMDataCollectionRulesInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                             supports_check_mode=True,
                                                             supports_tags=False,
                                                             facts_module=True,
                                                             required_by=self.required_by)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            result = self.get_data_collection_rule()
        else:
            result = self.list_data_collection_rules()

        self.results['datacollectionrules'] = result

        return self.results

    def get_data_collection_rule(self):
        '''
        Gets the properties of the specified data collection rule.

        :return: List of Data Collection Rules
        '''
        self.log("Checking if data collection rule {0} in resource group {1} is present".format(self.name,
                                                                                                self.resource_group))

        result = []
        data_collection_rule = None

        try:
            data_collection_rule = self.monitor_management_client_data_collection_rules.data_collection_rules.get(data_collection_rule_name=self.name,
                                                                                                                  resource_group_name=self.resource_group)
        except ResourceNotFoundError as ex:
            self.log("Could not find data collection rule {0} in resource group {1}".format(self.name, self.resource_group))
            return []
        except HttpResponseError as ex:
            if ex.error.code == 'InvalidSubscriptionId':
                self.log("Could not find subscription id")
                return []
            else:
                raise Exception(ex)
        if data_collection_rule:
            result = [self.serialize_obj(data_collection_rule, AZURE_OBJECT_CLASS)]

        return result

    def list_data_collection_rules(self):
        '''
        Gets the properties of the specified data collection rules in resource group or subscription.

        :return: List of Data Collection Rules
        '''

        result = []
        data_collection_rules = None

        if self.resource_group:
            self.log("Checking if the data collection rules in resource group {0} are present".format(self.resource_group))
            data_collection_rules_mgmt_client = self.monitor_management_client_data_collection_rules.data_collection_rules
            data_collection_rules = data_collection_rules_mgmt_client.list_by_resource_group(resource_group_name=self.resource_group)
        else:
            self.log("Checking if the data collection rules are present in subscription")
            data_collection_rules = self.monitor_management_client_data_collection_rules.data_collection_rules.list_by_subscription()
        if data_collection_rules:
            # it seems the exception is thrown when iterating through data_collection_rules, not when setting data_collection_rules
            try:
                for item in data_collection_rules:
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
    AzureRMDataCollectionRulesInfo()


if __name__ == '__main__':
    main()
