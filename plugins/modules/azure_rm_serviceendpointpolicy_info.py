#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_serviceendpointpolicy_info
version_added: "3.9.0"
short_description: Get or list the service endpoint policy
description:
    - Get or list the service endpoint policy.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
    name:
        description:
            - The name of the service endpoint policy name.
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
- name: Get the specified service endpoint policy
  azure.azcollection.azure_rm_serviceendpointpolicy_info:
    resource_group: testRG
    name: testpolicy

- name: List all service endpoint policy under same resource group
  azure.azcollection.azure_rm_serviceendpointpolicy_info:
    resource_group: testRG

- name: List all service endpoint policy
  azure.azcollection.azure_rm_serviceendpointpolicy_info:
'''

RETURN = '''
serviceendpointpolicies:
    description:
        - List the facts of service endpoint policy.
    type: complex
    returned: always
    contains:
        id:
            description:
                - Fully qualified ID of the resource.
            type: str
            returned: always
            sample: "/subscriptions/xxx-xxx/resourceGroups/TestRG/providers/Microsoft.Network/serviceEndpointPolicies/testpolicy"
        name:
            description:
                - The name of the resource that is unique within a resource group.
            type: str
            returned: always
            sample: testpolicy
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: "49e15a7b-1bff-46ba-b962-7a11e75cb729"
        resource_group:
            description:
                - The name of the resource group.
            type: str
            returned: always
            sample: TestRG
        location:
            description:
                - The resource's location.
            type: str
            returned: always
            sample: eastus
        type:
            description:
                - The type of the resource.
            type: str
            returned: always
            sample: Microsoft.Network/serviceEndpointPolicies
        service_endpoint_policy_definitions:
            description:
                - A collection of service endpoint policy definitions of the service endpoint policy.
            type: list
            returned: always
            sample: []
        provisioning_state:
            description:
                - The provisioning state of the service endpoint policy resource.
            type: str
            returned: always
            sample: Successded
        resource_guid:
            description:
                - The resource GUID property of the service endpoint policy resource.
            type: str
            returned: always
            sample: 77ee69ee-4152-4271-bfc0-1d431b7b7d28
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMServiceEndpointPolicyInfo(AzureRMModuleBase):
    """Information class for an Azure RM Data Collection Rules"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.resource_group = None
        self.name = None
        self.tags = None
        self.log_path = None
        self.log_mode = None
        self.required_by = {
            'name': 'resource_group'
        }

        self.results = dict(
            changed=False,
            serviceendpointpolicies=[]
        )

        super(AzureRMServiceEndpointPolicyInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                               supports_check_mode=True,
                                                               supports_tags=False,
                                                               facts_module=True,
                                                               required_by=self.required_by)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        result = []
        if self.name:
            result = self.get_policy(self.name)
        else:
            result = self.list_all_policy()
        self.results['serviceendpointpolicies'] = result

        return self.results

    def get_policy(self, name):
        '''
        Gets the specified service endpoint policy
        '''
        result = []
        response = None

        try:
            response = self.network_client.service_endpoint_policies.get(self.resource_group, self.name)
        except Exception:
            self.log("Could not get the specified service endpoint policy {0}".format(self.name))
            return []
        if response and self.has_tags(response.tags, self.tags):
            result = [self.format_item(response)]
        return result

    def list_all_policy(self):
        '''
        List all service endpoint policys for the specified resource.
        '''
        result = []
        response = None
        try:
            if self.resource_group:
                response = self.network_client.service_endpoint_policies.list_by_resource_group(self.resource_group)
            else:
                response = self.network_client.service_endpoint_policies.list()
        except Exception as ex:
            self.log("Could not list all service endpoint policys for the specified resource, Exception as {0}".format(ex))
            return []
        if response:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    result.append(self.format_item(item))
        return result

    def format_item(self, item):
        response = item.as_dict()
        response['resource_group'] = self.parse_resource_to_dict(response['id']).get('resource_group')
        return response


def main():
    """Main execution"""
    AzureRMServiceEndpointPolicyInfo()


if __name__ == '__main__':
    main()
