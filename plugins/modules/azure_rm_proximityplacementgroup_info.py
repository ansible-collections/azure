#!/usr/bin/python
#
# Copyright (c) 2021 Aparna Patil(@techcon65)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_proximityplacementgroup_info

version_added: "1.6.0"

short_description: Get proximity placement group facts

description:
    - Get facts for specified proximity placement group or all proximity placement groups in a given resource group.

options:
    resource_group:
        description:
            - Name of resource group.
        type: str
    name:
        description:
            - The name of the proximity placement group.
        type: str
    tags:
        description:
            - Limit the results by providing resource tags.
        type: dict

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Aparna Patil (@techcon65)

'''

EXAMPLES = '''
- name: Get facts for one proximity placement group
  azure_rm_proximityplacementgroup_info:
    resource_group: myAzureResourceGroup
    name: myppg

- name: Get facts for all proximity placement groups in resource group
  azure_rm_proximityplacementgroup_info:
    resource_group: myAzureResourceGroup
'''

RETURN = '''
proximityplacementgroups:
    description:
        - Gets a list of proximity placement groups.
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "availability_sets": [
                {
                    "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myAzureResourceGroup/
                           providers/Microsoft.Compute/availabilitySets/availabilityset1"
                },
                {
                    "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myAzureResourceGroup/
                           providers/Microsoft.Compute/availabilitySets/availabilityset2"
                }
            ],
            "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myAzureResourceGroup/providers/
                   Microsoft.Compute/proximityPlacementGroups/myppg",
            "location": "eastus",
            "name": "myppg",
            "proximity_placement_group_type": "Standard",
            "tags": {},
            "virtual_machine_scale_sets": [],
            "virtual_machines": [
                {
                    "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myAzureResourceGroup/
                           providers/Microsoft.Compute/virtualMachines/mylinuxvm"
                }
            ]
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.common import AzureMissingResourceHttpError, AzureHttpError
except Exception:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'ProximityPlacementGroup'


class AzureRMProximityPlacementGroupInfo(AzureRMModuleBase):

    def __init__(self):

        # define user inputs into argument
        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            tags=dict(type='dict')
        )

        # store the results of the module operation
        self.results = dict(
            changed=False
        )

        self.name = None
        self.resource_group = None
        self.tags = None

        super(AzureRMProximityPlacementGroupInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        results = []
        # list the conditions and results to return based on user input
        if self.name is not None:
            # if there is a group name provided, return facts about that specific proximity placement group
            results = self.get_item()
        elif self.resource_group:
            # all the proximity placement groups listed in specific resource group
            results = self.list_resource_group()
        else:
            # all the proximity placement groups in a subscription
            results = self.list_items()

        self.results['proximityplacementgroups'] = self.curated_items(results)

        return self.results

    def get_item(self):
        self.log('Get properties for {0}'.format(self.name))
        item = None
        results = []
        # get specific proximity placement group
        try:
            item = self.compute_client.proximity_placement_groups.get(self.resource_group, self.name)
        except CloudError:
            pass

        # serialize result
        if item and self.has_tags(item.tags, self.tags):
            results = [item]
        return results

    def list_resource_group(self):
        self.log('List all proximity placement groups for resource group - {0}'.format(self.resource_group))
        try:
            response = self.compute_client.proximity_placement_groups.list_by_resource_group(self.resource_group)
        except AzureHttpError as exc:
            self.fail("Failed to list for resource group {0} - {1}".format(self.resource_group, str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def list_items(self):
        self.log('List all proximity placement groups for a subscription ')
        try:
            response = self.compute_client.proximity_placement_groups.list_by_subscription()
        except AzureHttpError as exc:
            self.fail("Failed to list all items - {0}".format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def curated_items(self, raws):
        return [self.ppg_to_dict(item) for item in raws] if raws else []

    def ppg_to_dict(self, ppg):
        result = dict(
            id=ppg.id,
            name=ppg.name,
            location=ppg.location,
            tags=ppg.tags,
            proximity_placement_group_type=ppg.proximity_placement_group_type,
            virtual_machines=[dict(id=x.id) for x in ppg.virtual_machines],
            virtual_machine_scale_sets=[dict(id=x.id) for x in ppg.virtual_machine_scale_sets],
            availability_sets=[dict(id=x.id) for x in ppg.availability_sets]
        )
        return result


def main():
    AzureRMProximityPlacementGroupInfo()


if __name__ == '__main__':
    main()
