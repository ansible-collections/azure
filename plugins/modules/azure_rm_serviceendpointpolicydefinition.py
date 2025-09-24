#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_serviceendpointpolicydefinition
version_added: "3.9.0"
short_description: Managed the service endpoint policy definition
description:
    - Create, update or delete the service endpoint policy definition.

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
        required: true
    description:
        description:
            - A description for this rule. Restricted to 140 chars.
        type: str
    service:
        description:
            - Service endpoint name.
        type: str
    service_resources:
        description:
            - A list of service resources.
        type: list
        elements: str
    state:
        description:
            - Set to C(present) to create or update the service endpoint policy definition.
            - Set to C(absent) to remove the service endpoint policy definition.
        default: present
        type: str
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Create a new service endpoint policy definition
  azure.azcollection.azure_rm_serviceendpointpolicydefinition:
    resource_group: testRG
    service_endpoint_policy_name: policy01
    name: definition01
    description: definition-test
    service: Microsoft.Storage
    service_resources:
      - "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.Storage/storageAccounts/account01"

- name: Delete the service endpoint policy definition
  azure.azcollection.azure_rm_serviceendpointpolicydefinition:
    resource_group: testRG
    service_endpoint_policy_name: policy01
    name: definition01
    state: absent
'''

RETURN = '''
serviceendpointpolicydefinition:
    description:
        - The fact of the service endpoint policy definitions in a service end point policy.
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
try:
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServiceEndpointPolicyDefinition(AzureRMModuleBase):
    """Information class for an Azure RM Data Collection Rules"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            service_endpoint_policy_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            description=dict(type='str'),
            service=dict(type='str'),
            service_resources=dict(type='list', elements='str'),
            state=dict(type='str', default='present', choices=['present', 'absent'])
        )

        self.resource_group = None
        self.service_endpoint_policy_name = None
        self.name = None
        self.description = None
        self.service = None
        self.service_resurces = None
        self.state = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            serviceendpointpolicydefinition=dict()
        )

        super(AzureRMServiceEndpointPolicyDefinition, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                     supports_check_mode=True,
                                                                     supports_tags=False,
                                                                     facts_module=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        response = self.get_definition(self.name)
        changed = False
        if self.state == 'present':
            if response:
                if self.description and self.description != response.get('description'):
                    changed = True
                else:
                    self.description = response.get('description')
                if self.service and self.service != response.get('service'):
                    changed = True
                else:
                    self.service = response.get('service')
                if self.service_resources:
                    new_service_resources = response.get('service_resources', [])
                    for item in self.service_resources:
                        if item not in response.get('service_resources', []):
                            changed = True
                            new_service_resources.append(item)
                    self.service_resources = new_service_resources
                else:
                    self.service_resources = response.get('service_resources')
            else:
                changed = True
            if not self.check_mode and changed:
                response = self.create_or_update()
        else:
            if response:
                changed = True
                if self.check_mode:
                    self.log("The service endpoint policy definition already exist, will be delete")
                else:
                    response = self.delete()
            else:
                if self.check_mode:
                    self.log("There is no service endpoint policy definition.")

        self.results['changed'] = changed
        self.results['serviceendpointpolicydefinition'] = response
        return self.results

    def get_definition(self, name):
        '''
        Gets the specified service endpoint policy definition
        '''
        response = None
        try:
            response = self.network_client.service_endpoint_policy_definitions.get(self.resource_group, self.service_endpoint_policy_name, self.name)
        except Exception:
            self.log("Could not get the specified service endpoint policy definition {0}".format(self.name))
        return self.format_item(response) if response else None

    def create_or_update(self):
        '''
        Create or update the service endpoint policy definition.
        '''
        response = None
        try:
            response = self.network_client.service_endpoint_policy_definitions.begin_create_or_update(self.resource_group,
                                                                                                      self.service_endpoint_policy_name,
                                                                                                      self.name,
                                                                                                      dict(description=self.description,
                                                                                                           service=self.service,
                                                                                                           service_resources=self.service_resources))
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as ex:
            self.fail("Could not create or update the service endpoint policy definition, Exception as {0}".format(ex))
        return self.format_item(response) if response else None

    def delete(self):
        '''
        Delete the service endpoint policy definition.
        '''
        try:
            response = self.network_client.service_endpoint_policy_definitions.begin_delete(self.resource_group, self.service_endpoint_policy_name, self.name)
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except Exception as ex:
            self.fail("Could not delete the service endpoint policy definition, Exception as {0}".format(ex))

    def format_item(self, item):
        response = item.as_dict()
        response['resource_group'] = self.resource_group
        response['service_endpoint_policy_name'] = self.service_endpoint_policy_name
        return response


def main():
    """Main execution"""
    AzureRMServiceEndpointPolicyDefinition()


if __name__ == '__main__':
    main()
