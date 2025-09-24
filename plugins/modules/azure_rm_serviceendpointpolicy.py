#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_serviceendpointpolicy
version_added: "3.9.0"
short_description: Managed the service endpoint policy
description:
    - Create, update or delete the service endpoint policy.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: true
    name:
        description:
            - The name of the service endpoint policy name.
        type: str
        required: true
    location:
        description:
            - THe resource's location.
        type: str
    state:
        description:
            - Set to C(present) to create or update the service endpoint policy.
            - Set to C(absent) to remove the service endpoint policy.
        default: present
        type: str
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - magodo (@magodo)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Create a new service endpoint policy
  azure.azcollection.azure_rm_serviceendpointpolicy:
    resource_group: testRG
    name: policyname
    locaiton: eastus
    tags:
      key: value

- name: Delete the service endpoint policy
  azure.azcollection.azure_rm_serviceendpointpolicy:
    resource_group: testRG
    name: policyname
    state: absent
'''

RETURN = '''
serviceendpointpolicypolicy:
    description:
        - The fact of the service endpoint policys in a service end point policy.
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
try:
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServiceEndpointPolicy(AzureRMModuleBase):
    """Information class for an Azure RM Data Collection Rules"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent'])
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None
        self.tags = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            serviceendpointpolicypolicy=dict()
        )

        super(AzureRMServiceEndpointPolicy, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                           supports_check_mode=True,
                                                           supports_tags=True,
                                                           facts_module=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        response = self.get_policy(self.name)
        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        changed = False
        if self.state == 'present':
            if response:
                update_tags, self.tags = self.update_tags(response.get('tags', dict()))
                if update_tags:
                    changed = True
                    if not self.check_mode:
                        response = self.update_tag()
            else:
                changed = True
                if not self.check_mode:
                    response = self.create_or_update()
        else:
            if response:
                changed = True
                if self.check_mode:
                    self.log("The service endpoint policy already exist, will be delete")
                else:
                    response = self.delete()
            else:
                if self.check_mode:
                    self.log("There is no service endpoint policy.")

        self.results['changed'] = changed
        self.results['serviceendpointpolicypolicy'] = response
        return self.results

    def get_policy(self, name):
        '''
        Gets the specified service endpoint policy
        '''
        response = None
        try:
            response = self.network_client.service_endpoint_policies.get(self.resource_group, self.name)
        except Exception:
            self.log("Could not get the specified service endpoint policy {0}".format(self.name))
        return self.format_item(response) if response else None

    def create_or_update(self):
        '''
        Create or update the service endpoint policy.
        '''
        response = None
        try:
            response = self.network_client.service_endpoint_policies.begin_create_or_update(resource_group_name=self.resource_group,
                                                                                            service_endpoint_policy_name=self.name,
                                                                                            parameters=dict(location=self.location,
                                                                                                            tags=self.tags))
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as ex:
            self.fail("Could not create or update the service endpoint policy, Exception as {0}".format(ex))
        return self.format_item(response) if response else None

    def update_tag(self):
        '''
        Update the service endpoint policy tags.
        '''
        response = None
        try:
            response = self.network_client.service_endpoint_policies.update_tags(resource_group_name=self.resource_group,
                                                                                 service_endpoint_policy_name=self.name,
                                                                                 parameters=dict(tags=self.tags))
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as ex:
            self.fail("Could not create or update the service endpoint policy, Exception as {0}".format(ex))
        return self.format_item(response) if response else None

    def delete(self):
        '''
        Delete the service endpoint policy.
        '''
        try:
            response = self.network_client.service_endpoint_policies.begin_delete(self.resource_group, self.name)
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except Exception as ex:
            self.fail("Could not delete the service endpoint policy, Exception as {0}".format(ex))

    def format_item(self, item):
        response = item.as_dict()
        response['resource_group'] = self.resource_group
        return response


def main():
    """Main execution"""
    AzureRMServiceEndpointPolicy()


if __name__ == '__main__':
    main()
