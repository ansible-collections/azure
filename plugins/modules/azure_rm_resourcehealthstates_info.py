#!/usr/bin/python
#
# Copyright (c) 2025 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_resourcehealthstates_info

version_added: "3.3.0"

short_description: Get or list the current availability status for the resource

description:
    - Get or list the current availability status for the resource.

options:
    resource_group:
        description:
            - Name of resource group.
        type: str
    resource_uri:
        description:
            - The fully qualified ID of the resource, including the resource name and resource type.
            - Currently the API support not nested and one nesting level resource types,
              such as '/subscriptions/{subscriptionId}/resourceGroups/{resource-group-name}/providers/{resource-provider-name}/
              {resource-type}/{resource-name}' and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/
              providers/{resource-provider-name}/{parentResourceType}/{parentResourceName}/{resourceType}/{resourceName}'.
        type: str
    list_all:
        description:
            - Whether lists all historical availability transitions and impacting events for a single resource.
        type: bool
        default: False

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Lists the current availability status for all the resources in the subscription.
  azure_rm_resourcehealthstates_info:

- name: Lists the current availability status for all the resources in the resource group.
  azure_rm_resourcehealthstates_info:
    resource_group: "{{ resource_group }}"

- name: Gets current availability status for a single resource.
  azure_rm_resourcehealthstates_info:
    resource_uri: "/subscriptions/xxxx-xxx/resourcegroups/v-xisurg/providers/microsoft.compute/virtualmachines/testvm"

- name: Lists all historical availability transitions and impacting events for a single resource.
  azure_rm_resourcehealthstates_info:
    resource_uri: "/subscriptions/xxxx-xxx/resourcegroups/v-xisurg/providers/microsoft.compute/virtualmachines/testvm"
    list_all: true
'''

RETURN = '''
health_states:
    description:
        - The facts of availabilityStatus of a resource.
    type: complex
    returned: always
    contains:
        id:
            description:
                - Azure Resource Manager Identity for the availabilityStatuses resource.
            type: str
            returned: always
            sample: "/subscriptions/xxxx-xxx/resourcegroups/defaultresourcegroup-wus2/providers/microsoft.operationalinsights/workspaces/
                    defaultworkspace-e393adb3-b5be-4789-bdc9-848367f0d152-wus2/providers/Microsoft.ResourceHealth/availabilityStatuses/current"
        location:
            description:
                - Azure Resource Manager geo location of the resource.
            type: str
            returned: always
            sample: westus2
        type:
            description:
                - Microsoft.ResourceHealth/AvailabilityStatuses.
            type: str
            returned: always
            sample: "Microsoft.ResourceHealth/AvailabilityStatuses"
        properties:
            description:
                - Properties of availability state.
            type: complex
            contains:
                availability_state:
                    description:
                        - Availability status of the resource.
                    type: str
                    returned: always
                    sample: "Unknown"
                category:
                    description:
                        - When a context field is set to Platform, this field will reflect if the event was planned or unplanned.
                        - If the context field does not have a value of Platform, then this field will be ignored.
                    type: str
                    returned: always
                    sample: "Not Applicable"
                context:
                    description:
                        - This field is connected to the category field in this object.
                    type: str
                    returned: always
                    sample: "Not Applicable"
                occured_time:
                    description:
                        - Timestamp for when last change in health status occurred.
                    type: str
                    returned: always
                    sample: "2025-03-05T01:50:29.67632Z"
                reason_chronicity:
                    description:
                        - Chronicity of the availability transition.
                    type: str
                    returned: always
                    sample: "Transient"
                reason_type:
                    description:
                        - When the resource's availabilityState is Unavailable, it describes where the health impacting event was originated.
                    type: str
                    returned: always
                    sample: ""
                reported_time:
                    description:
                        - Timestamp for when the health was last checked.
                    type: str
                    returned: always
                    sample: "2025-03-05T01:50:29.67632Z"
                summary:
                    description:
                        - Summary description of the availability status.
                    type: str
                    returned: always
                    sample: "We're currently unable to determine the health of this workspace.
                            Either no queries were run on this workspace, or no data was ingested to this workspace recently."
                title:
                    description:
                        - Title description of the availability status.
                    type: str
                    returned: always
                    sample: Unkown
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMResourceHealthStatesInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_args = dict(
            resource_group=dict(type='str'),
            resource_uri=dict(type='str'),
            list_all=dict(type='bool', default=False)
        )

        self.results = dict(
            changed=False,
            health_states=[]
        )

        self.resource_group = None
        self.resource_uri = None
        self.list_all = None
        required_if = [('list_all', True, ['resource_uri'])]

        super(AzureRMResourceHealthStatesInfo, self).__init__(
            derived_arg_spec=self.module_args,
            supports_check_mode=True,
            supports_tags=False,
            required_if=required_if,
            facts_module=True
        )

    def exec_module(self, **kwargs):
        for key in self.module_args:
            setattr(self, key, kwargs[key])

        if self.resource_uri is not None:
            if self.list_all:
                response = self.list_by_resource_uri(self.resource_uri)
            else:
                response = self.get_by_resource(self.resource_uri)
        elif self.resource_group is not None:
            response = self.list_by_resource_group(self.resource_group)
        else:
            response = self.list_by_subscription_id()

        self.results['health_states'] = [item.as_dict() for item in response]
        return self.results

    def get_by_resource(self, resource_uri):
        '''
        Gets current availability status for a single resource.
        :return: AvailabilityStatus or the result of cls(response)
        '''
        try:
            response = [self.resourcehealth_client.availability_statuses.get_by_resource(resource_uri)]
        except Exception as exc:
            self.fail('Error when gets current availability status for a single resource. Error msg: {0}'.format(exc.message or str(exc)))

        return response

    def list_by_resource_uri(self, resource_uri):
        '''
        Lists all historical availability transitions and impacting events for a single resource
        :return: An iterator like instance of either AvailabilityStatus or the result of cls(response)
        '''
        try:
            response = self.resourcehealth_client.availability_statuses.list(resource_uri)
        except Exception as exc:
            self.fail('Error when lists all historical availability transitions and impacting events for a single resource. Error msg: {0}'.format(exc))

        return response

    def list_by_resource_group(self, resource_group):
        '''
        Lists the current availability status for all the resources in the resource group.
        :return: An iterator like instance of either AvailabilityStatus or the result of cls(response)
        '''
        try:
            response = self.resourcehealth_client.availability_statuses.list_by_resource_group(resource_group)
        except Exception as exc:
            self.fail('Error when lists the current availability status for all the resources in the resource group. Error msg: {0}'.format(exc))

        return response

    def list_by_subscription_id(self):
        '''
        Lists the current availability status for all the resources in the subscription.
        :return: An iterator like instance of either AvailabilityStatus or the result of cls(response)
        '''
        try:
            response = self.resourcehealth_client.availability_statuses.list_by_subscription_id()
        except Exception as exc:
            self.fail('Error when lists the current availability status for all the resources in the subscription Error msg: {0}'.format(exc))

        return response


def main():
    """Main module execution code path"""

    AzureRMResourceHealthStatesInfo()


if __name__ == '__main__':
    main()
