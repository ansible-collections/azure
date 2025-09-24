#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_serviceendpointpolicydefinition_info
version_added: "3.9.0"
short_description: Get or list the service endpoint policy definition
description:
    - Get or list the service endpoint policy definition.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: true
    service_endpoint_policy_name:
        description:
            - The name of the service endpoint policy name.
        type: str
        required: true
    name:
        description:
            - The name of the service endpoint policy definition name.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get the specified service endpoint policy definitions from service endpoint policy
  azure.azcollection.azure_rm_serviceendpointpolicydefinition_info:
    resource_group: testRG
    service_endpoint_policy_name: testpolicy
    name: definitionname

- name: List all service endpoint policy definitions in a service end point policy
  azure.azcollection.azure_rm_serviceendpointpolicydefinition_info:
    resource_group: testRG
    service_endpoint_policy_name: testpolicy
'''

RETURN = '''
serviceendpointpolicydefinitions:
    description:
        - List of the service endpoint policy definitions in a service end point policy.
    type: complex
    returned: always
    contains:
        id:
            description:
                - Fully qualified ID of the resource.
            type: str
            returned: always
            sample: "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.Network/serviceEndpointPolicies/\
                     policy01/serviceEndpointPolicyDefinitions/definition01"
        name:
            description:
                - The name of the resource that is unique within a resource group.
            type: str
            returned: always
            sample: definition01
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: "4a66fa1c-3d17-43c9-9b9d-da07ffdbb695"
        resource_group:
            description:
                - The name of the resource group.
            type: str
            returned: always
            sample: TestRG
        description:
            description:
                - A description for this rule. Restricted to 140 chars.
            type: str
            returned: always
            sample: definition-test
        service_endpoint_policy_name:
            description:
                - The name of the service endpoint policy name.
            type: str
            returned: always
            sample: policy01
        type:
            description:
                - The type of the resource.
            type: str
            returned: always
            sample: "Microsoft.Network/serviceEndpointPolicies/serviceEndpointPolicyDefinitions"
        provisioning_state:
            description:
                - The provisioning state of the service endpoint policy definition resource.
            type: str
            returned: always
            sample: Successded
        service:
            description:
                - Service endpoint name.
            type: str
            returned: always
            sample: Microsoft.Storage
        service_resources:
            description:
                - A list of service resources.
            type: list
            returned: always
            sample: ["/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.Storage/storageAccounts/account01"]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMServiceEndpointPolicyDefinitionInfo(AzureRMModuleBase):
    """Information class for an Azure RM Data Collection Rules"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            service_endpoint_policy_name=dict(type='str', required=True),
            name=dict(type='str')
        )

        self.resource_group = None
        self.service_endpoint_policy_name = None
        self.name = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            serviceendpointpolicydefinitions=[]
        )

        super(AzureRMServiceEndpointPolicyDefinitionInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                         supports_check_mode=True,
                                                                         supports_tags=False,
                                                                         facts_module=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        result = []
        if self.name:
            result = self.get_definition(self.name)
        else:
            result = self.list_all_definition()
        self.results['serviceendpointpolicydefinitions'] = result

        return self.results

    def get_definition(self, name):
        '''
        Gets the specified service endpoint policy definition
        '''
        result = []
        response = None

        try:
            response = self.network_client.service_endpoint_policy_definitions.get(self.resource_group, self.service_endpoint_policy_name, self.name)
        except Exception:
            self.log("Could not get the specified service endpoint policy definition {0}".format(self.name))
            return []
        if response:
            result = [self.format_item(response)]
        return result

    def list_all_definition(self):
        '''
        List all service endpoint policy definitions for the specified resource.
        '''
        result = []
        response = None

        try:
            response = self.network_client.service_endpoint_policy_definitions.list_by_resource_group(self.resource_group, self.service_endpoint_policy_name)
        except Exception as ex:
            self.log("Could not list all service endpoint policy definitions for the specified resource, Exception as {0}".format(ex))
            return []
        if response:
            for item in response:
                result.append(self.format_item(item))
        return result

    def format_item(self, item):
        response = item.as_dict()
        response['resource_group'] = self.resource_group
        response['service_endpoint_policy_name'] = self.service_endpoint_policy_name
        return response


def main():
    """Main execution"""
    AzureRMServiceEndpointPolicyDefinitionInfo()


if __name__ == '__main__':
    main()
