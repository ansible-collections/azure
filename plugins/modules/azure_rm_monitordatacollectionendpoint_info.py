#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitordatacollectionendpoint_info
version_added: "3.9.0"
short_description: Get or list Data Collection Endpoints
description:
    - Get or list Data Collection Rules Endpoints.

options:
    name:
        description:
            - The name of the data collection endpoint.
            - The name is case insensitive.
        type: str
    resource_group:
        description:
            - The name of the resource group in which the data collection endpoint is (if you use name)
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get data collection endpoint details
  azure.azcollection.azure_rm_monitordatacollectionendpoint_info:
    name: fredendpoint01
    resource_group: Resource_Group_Name

- name: List all data collection endpoints in specific resource group
  azure.azcollection.azure_rm_monitordatacollectionendpoint_info:
    resource_group: Resource_Group_Name

- name: List all data collection endpoints in the current subscription
  azure.azcollection.azure_rm_monitordatacollectionendpoint_info:
'''

RETURN = '''
datacollectionendpoints:
    description:
        - List of data collection rule association.
        - Can be empty if listing data collection rule association.
    type: list
    returned: always
    sample: [
            {
                "configuration_access": {
                    "endpoint": "https://fredendpoint1-tdt8.eastus-1.handler.control.monitor.azure.com"
                },
                "description": "fredtestend",
                "etag": "\"3d00ef18-0000-0100-0000-68ca28010000\"",
                "id": "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG/providers/Microsoft.Insights/dataCollectionEndpoints/fredendpoint1",
                "immutable_id": "dce-703ef7fab85d4391af585d91c2b0b5a7",
                "kind": "Linux",
                "location": "eastus",
                "logs_ingestion": {
                    "endpoint": "https://fredendpoint1-tdt8.eastus-1.ingest.monitor.azure.com"
                },
                "metrics_ingestion": {
                    "endpoint": "https://fredendpoint1-tdt8.eastus-1.metrics.ingest.monitor.azure.com"
                },
                "name": "fredendpoint1",
                "network_acls": {
                    "public_network_access": "Enabled"
                },
                "provisioning_state": "Succeeded",
                "system_data": {
                    "created_at": "2025-09-17T03:16:17.037276Z",
                    "created_by": "00867800-0fa3-4d02-8bc8-35edac3a0d32",
                    "created_by_type": "Application",
                    "last_modified_at": "2025-09-17T03:16:17.037276Z",
                    "last_modified_by": "00867800-0fa3-4d02-8bc8-35edac3a0d32",
                    "last_modified_by_type": "Application"
                },
                "tags": {
                    "key1": "value1",
                    "key2": "value2"
                },
                "type": "Microsoft.Insights/dataCollectionEndpoints"
            }
        ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMDataCollectionRuleEndpointInfo(AzureRMModuleBase):
    """Information class for an Azure RM Data Collection Rules"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.required_by = {
            'endpoint_name': 'resource_group'
        }

        self.resource_group = None
        self.name = None
        self.tags = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            datacollectionendpoints=[]
        )

        super(AzureRMDataCollectionRuleEndpointInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                             supports_check_mode=True,
                                                             supports_tags=False,
                                                             facts_module=True,
                                                             required_by=self.required_by)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            result = self.get_endpoint()
        else:
            result = self.list_endpoints()

        self.results['datacollectionendpoints'] = result

        return self.results
        return [item for item in self.results if self.has_tags(item.get('tags'), self.tags)]

    def get_endpoint(self):
        '''
        Gets the specified data collection rule endpoint
        '''
        result = []
        response = None

        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_endpoints.get(resource_group_name=self.resource_group,
                                                                                                              data_collection_endpoint_name=self.name)
        except Exception as ex:
            self.log("Could not find data collection endpoint {0} in resource group {1}, Exception as {2}".format(self.name, self.resource_group, ex))
            return []
        if response and self.has_tags(response.tags, self.tags):
            result = [response.as_dict()]
        return result

    def list_endpoints(self):
        '''
        Lists Data Collection Endpoint for the specified resource.
        '''
        result = []
        response = None

        if self.resource_group:
            try:
                response = self.monitor_management_client_data_collection_rules.data_collection_endpoints.list_by_resource_group(resource_group_name=self.resource_group)
            except Exception as ex:
                self.log("Could not list data collection endponts in resource group {0}, Exception as {1}".format(self.resource_uri, ex))
                return []
        else:
            try:
                response = self.monitor_management_client_data_collection_rules.data_collection_endpoints.list_by_subscription()
            except Exception as ex:
                self.log("Could not list data collection endpoint in the subscription_id, Exception as {0}".format(ex))
                return []
        if response:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    result.append(item.as_dict())

        return result


def main():
    """Main execution"""
    AzureRMDataCollectionRuleEndpointInfo()


if __name__ == '__main__':
    main()
