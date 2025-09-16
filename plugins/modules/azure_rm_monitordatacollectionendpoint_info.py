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
    endpoint_name:
        description:
            - The name of the data collection endpoint.
            - The name is case insensitive.
        type: str
    resource_group:
        description:
            - The name of the resource group in which the data collection endpoint is (if you use name)
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get data collection endpoint details
  azure.azcollection.azure_rm_monitordatacollectionendpoint_info:
    endpoint_name: 
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
    sample:
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import HttpResponseError

except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDataCollectionRuleEndpointInfo(AzureRMModuleBase):
    """Information class for an Azure RM Data Collection Rules"""

    def __init__(self):
        self.module_arg_spec = dict(
            endpoint_name=dict(type='str'),
            resource_group=dict(type='str')
        )

        self.required_by = {
            'endpoint_name': 'resource_group'
        }

        self.resource_group = None
        self.endpoint_name = None
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

        if self.endpoint_name:
            result = self.get_endpoint()
        else:
            result = self.list_endpoints()

        self.results['datacollectionruleendpoints'] = result

        return self.results

    def get_endpoint(self):
        '''
        Gets the specified data collection rule endpoint
        '''
        result = []
        response = None

        try:
            response = self.monitor_management_client_data_collection_endpoints.data_collection_endpoints.get(resource_group_name=self.resource_group,
                                                                                                              data_collection_endpoint_name=self.endpoint_name)
        except Exception as ex:
            self.log("Could not find data collection endpoint {0} in resource group {1}".format(self.endpoint_name, self.resource_group))
            return []
        if response:
            result = [response.as_dict()]

        return result

    def list_endpoints(self):
        '''
        Lists Data Collection Endpoint for the specified resource.
        '''
        result = []
        response = None

        if self.resource_gorup:
            try:
                response = self.monitor_management_client_data_collection_endpoints.data_collection_endpoints.list_by_resource_group(resource_group_name=self.resource_group)
            except Exception as ex:
                self.log("Could not list data collection endponts in resource group {0}".format(self.resource_uri))
                return []
        else:
            try:
                response = self.monitor_management_client_data_collection_endpoints.data_collection_endpoints.list_by_subscription()
            except Exception as ex:
                self.log("Could not list data collection endpoint in the subscription_id")
                return []
        if response:
            result.append(item.as_dict() for item in response)

        return result


def main():
    """Main execution"""
    AzureRMDataCollectionRuleEndpointInfo()


if __name__ == '__main__':
    main()
