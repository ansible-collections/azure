#!/usr/bin/python
#
# Copyright (c) 2021 Aparna Patil(@techcon65)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_proximityplacementgroup

version_added: "1.6.0"

short_description: Create, delete and update proximity placement group

description:
    - Creates, deletes, and updates proximity placement group.

options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    name:
        description:
            - The name of the proximity placement group.
        required: true
        type: str
    location:
        description:
            - Valid Azure location for proximity placement group. Defaults to location of resource group.
        type: str
    state:
        description:
            - Assert the state of the placement group. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Aparna Patil (@techcon65)
'''

EXAMPLES = '''
- name: Create a proximity placement group
  azure_rm_proximityplacementgroup:
    resource_group: myAzureResourceGroup
    location: eastus
    name: myppg
    state: present

- name: Update proximity placement group
  azure_rm_proximityplacementgroup:
    resource_group: myAzureResourceGroup
    location: eastus
    name: myppg
    tags:
      key1: "value1"
    state: present

- name: Delete a proximity placement group
  azure_rm_proximityplacementgroup:
    resource_group: myAzureResourceGroup
    name: myppg
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the proximity placement group.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The proximity placement group ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myAzureResourceGroup/providers/
                     Microsoft.Compute/proximityPlacementGroups/myppg"
        name:
            description:
                - The proximity placement group name.
            returned: always
            type: str
            sample: 'myppg'
        location:
            description:
                - The Azure Region where the resource lives.
            returned: always
            type: str
            sample: eastus
        proximity_placement_group_type:
            description:
                - The type of proximity placement group.
            returned: always
            type: str
            sample: Standard
        tags:
            description:
                - Resource tags.
            returned: always
            type: list
            sample: [{"key1": "value1"}]
        type:
            description:
                - The type of resource.
            returned: always
            type: str
            sample: Microsoft.Compute/proximityPlacementGroups
'''

from ansible.module_utils.basic import _load_params
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, HAS_AZURE, \
    format_resource_id, normalize_location_name

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMProximityPlacementGroup(AzureRMModuleBase):

    def __init__(self):

        _load_params()
        # define user inputs from playbook
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            state=dict(choices=['present', 'absent'], default='present', type='str')
        )

        self.results = dict(
            changed=False,
            state=dict()
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None
        self.tags = None

        super(AzureRMProximityPlacementGroup, self).__init__(self.module_arg_spec,
                                                             supports_check_mode=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False
        results = dict()
        proximity_placement_group = None

        # retrieve resource group to make sure it exists
        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        self.location = normalize_location_name(self.location)

        try:
            self.log('Fetching Proximity placement group {0}'.format(self.name))
            proximity_placement_group = self.compute_client.proximity_placement_groups.get(self.resource_group,
                                                                                           self.name)
            # serialize object into a dictionary
            results = self.ppg_to_dict(proximity_placement_group)
            if self.state == 'present':
                changed = False
                update_tags, results['tags'] = self.update_tags(results['tags'])
                if update_tags:
                    changed = True
                self.tags = results['tags']
            elif self.state == 'absent':
                changed = True

        except ResourceNotFoundError:
            if self.state == 'present':
                changed = True
            else:
                changed = False

        self.results['changed'] = changed
        self.results['state'] = results

        if self.check_mode:
            return self.results

        if changed:
            if self.state == 'present':
                # create or update proximity placement group
                proximity_placement_group_new = \
                    self.compute_models.ProximityPlacementGroup(location=self.location,
                                                                proximity_placement_group_type='Standard')
                if self.tags:
                    proximity_placement_group_new.tags = self.tags
                self.results['state'] = self.create_or_update_placementgroup(proximity_placement_group_new)

            elif self.state == 'absent':
                # delete proximity placement group
                self.delete_placementgroup()
                self.results['state'] = 'Deleted'

        return self.results

    def create_or_update_placementgroup(self, proximity_placement_group):
        try:
            # create the placement group
            response = self.compute_client.proximity_placement_groups.create_or_update(resource_group_name=self.resource_group,
                                                                                       proximity_placement_group_name=self.name,
                                                                                       parameters=proximity_placement_group)
        except Exception as exc:
            self.fail("Error creating or updating proximity placement group {0} - {1}".format(self.name, str(exc)))
        return self.ppg_to_dict(response)

    def delete_placementgroup(self):
        try:
            # delete the placement group
            response = self.compute_client.proximity_placement_groups.delete(resource_group_name=self.resource_group,
                                                                             proximity_placement_group_name=self.name)
        except Exception as exc:
            self.fail("Error deleting proximity placement group {0} - {1}".format(self.name, str(exc)))
        return response

    def ppg_to_dict(self, proximityplacementgroup):
        result = proximityplacementgroup.as_dict()
        result['tags'] = proximityplacementgroup.tags
        return result


def main():
    AzureRMProximityPlacementGroup()


if __name__ == '__main__':
    main()
