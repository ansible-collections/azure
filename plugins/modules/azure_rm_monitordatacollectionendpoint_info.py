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
    type: complex
    returned: always
    contains:
        configuration_access:
            description:
                - The endpoint used by clients to access their configuration.
            type: dict
            returned: always
            sample: {"endpoint": "https://fredendpoint-q7lu.eastus-1.handler.control.monitor.azure.com"}
        description:
            description:
                - Description of the data collection endpoint.
            type: str
            returned: always
            sample: Created
        etag:
            description:
                - Resource entity tag (ETag).
            type: str
            returned: always
            sample: "3d001f14-0000-0100-0000-68ca270a0000"
        id:
            description:
                - Fully qualified ID of the resource.
            type: str
            returned: always
            sample: "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG/providers/Microsoft.Insights/dataCollectionEndpoints/fredendpoint"
        immutable_id:
            description:
                - The immutable ID of this data collection endpoint resource.
                - This property is READ-ONLY.
            type: str
            returned: always
            sample: dce-9897a7cde9b54676a1c07ab3ea222768
        kind:
            description:
                - The kind of the resource.
            type: str
            returned: always
            sample: Linux
        logs_ingestion:
            description:
                - The endpoint used by clients to ingest logs.
            type: dict
            returned: always
            sample: {"endpoint": "https://fredendpoint-q7lu.eastus-1.ingest.monitor.azure.com"}
        metrics_ingestion:
            description:
                - The endpoint used by clients to ingest metrics.
            type: dict
            returned: always
            sample: {"endpoint": "https://fredendpoint-q7lu.eastus-1.metrics.ingest.monitor.azure.com"}
        name:
            description:
                - The name of the resource.
            type: str
            returned: always
            sample: testendpoint
        network_acls:
            description:
                - Network access control rules for the endpoints.
            type: dict
            returned: always
            sample: {"public_network_access": "Enabled"}
        provisioning_state:
            description:
                - The resource provisioning state. This property is READ-ONLY.
            type: str
            returned: always
            sample: Succeeded
        system_data:
            description:
                - Metadata pertaining to creation and last modification of the resource.
            type: dict
            returned: always
            sample: {
                "created_at": "2025-09-17T03:12:08.743499Z",
                "created_by": "00867800-0fa3-4d02-8bc8-35edac3a0d32",
                "created_by_type": "Application",
                "last_modified_at": "2025-09-17T03:12:08.743499Z",
                "last_modified_by": "00867800-0fa3-4d02-8bc8-35edac3a0d32",
                "last_modified_by_type": "Application"
            }
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: {'key1': 'value1'}
        type:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: "Microsoft.Insights/dataCollectionEndpoints"
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
            'name': 'resource_group'
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
                response = self.monitor_management_client_data_collection_rules.data_collection_endpoints.list_by_resource_group(
                    resource_group_name=self.resource_group)
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
