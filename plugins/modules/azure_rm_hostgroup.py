#!/usr/bin/python
#
# Copyright (c) 2021 Aparna Patil(@aparna-patil)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_hostgroup

version_added: "1.10.0"

short_description: Create, delete and update a dedicated host group

description:
    - Creates, deletes, and updates a dedicated host group.

options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    name:
        description:
            - The name of the dedicated host group.
        required: true
        type: str
    location:
        description:
            - Valid Azure location for host group. Defaults to location of resource group.
        type: str
    platform_fault_domain_count:
        description:
            - Number of fault domains that the host group can span.
        type: int
    zones:
        description:
            - Availability Zone to use for this host group. Only single zone is supported. The zone can be assigned only
             during creation. If not provided, the group supports all zones in the region.
        type: list
        elements: str
    state:
        description:
            - Assert the state of the host group. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Aparna Patil (@aparna-patil)
'''

EXAMPLES = '''
- name: Create a host group
  azure_rm_hostgroup:
    resource_group: myAzureResourceGroup
    name: myhostgroup
    location: eastus
    zones:
      - "1"
    platform_fault_domain_count: 1
    state: present

- name: Update a host group
  azure_rm_hostgroup:
    resource_group: myAzureResourceGroup
    name: myhostgroup
    location: eastus
    zones:
      - "1"
    platform_fault_domain_count: 1
    state: present
    tags:
      key1: "value1"

- name: Delete a host group
  azure_rm_hostgroup:
    resource_group: myAzureResourceGroup
    name: myhostgroup
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the host group.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The host group ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myAzureResourceGroup/providers/
                     Microsoft.Compute/hostGroups/myhostgroup"
        name:
            description:
                - The host group name.
            returned: always
            type: str
            sample: 'myhostgroup'
        location:
            description:
                - The Azure Region where the resource lives.
            returned: always
            type: str
            sample: eastus
        platform_fault_domain_count:
            description:
                - Number of fault domains.
            returned: always
            type: int
            sample: 1
        zones:
            description:
                - Availability zones configured for this host group.
            returned: always
            type: list
            sample: ["1"]
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
            sample: Microsoft.Compute/hostGroups
'''

from ansible.module_utils.basic import _load_params
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, HAS_AZURE, \
    normalize_location_name

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMHostGroup(AzureRMModuleBase):

    def __init__(self):

        _load_params()
        # define user inputs from playbook
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            platform_fault_domain_count=dict(type='int'),
            zones=dict(type='list', elements='str'),
            state=dict(choices=['present', 'absent'], default='present', type='str')
        )

        required_if = [
            ('state', 'present', ['platform_fault_domain_count'])
        ]

        self.results = dict(
            changed=False,
            state=dict()
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None
        self.tags = None
        self.platform_fault_domain_count = None
        self.zones = None

        super(AzureRMHostGroup, self).__init__(self.module_arg_spec,
                                               required_if=required_if,
                                               supports_check_mode=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False
        results = dict()
        host_group = None

        # retrieve resource group to make sure it exists
        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        self.location = normalize_location_name(self.location)

        try:
            self.log('Fetching host group {0}'.format(self.name))
            host_group = self.compute_client.dedicated_host_groups.get(self.resource_group, self.name)
            # serialize object into a dictionary
            results = self.hostgroup_to_dict(host_group)
            if self.state == 'present':
                changed = False
                update_tags, results['tags'] = self.update_tags(results['tags'])
                if update_tags:
                    changed = True
                self.tags = results['tags']
                if self.platform_fault_domain_count != results['platform_fault_domain_count']:
                    self.fail("Error updating host group : {0}. Changing platform_fault_domain_count is not allowed."
                              .format(self.name))
                if self.zones:
                    if ('zones' in results and self.zones[0] != results['zones'][0]) or 'zones' not in results:
                        self.fail("Error updating host group : {0}. Changing property zones is not allowed."
                                  .format(self.name))
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
                # create or update a dedicated host group
                host_group_new = \
                    self.compute_models.DedicatedHostGroup(location=self.location,
                                                           platform_fault_domain_count=self.platform_fault_domain_count,
                                                           zones=self.zones)
                if self.tags:
                    host_group_new.tags = self.tags
                self.results['state'] = self.create_or_update_hostgroup(host_group_new)

            elif self.state == 'absent':
                # delete a host group
                self.delete_hostgroup()
                self.results['state'] = 'Deleted'

        return self.results

    def create_or_update_hostgroup(self, host_group):
        try:
            # create the host group
            response = self.compute_client.dedicated_host_groups.create_or_update(
                resource_group_name=self.resource_group,
                host_group_name=self.name,
                parameters=host_group)
        except Exception as exc:
            self.fail("Error creating or updating host group {0} - {1}".format(self.name, str(exc)))
        return self.hostgroup_to_dict(response)

    def delete_hostgroup(self):
        try:
            # delete the host group
            response = self.compute_client.dedicated_host_groups.delete(resource_group_name=self.resource_group,
                                                                        host_group_name=self.name)
        except Exception as exc:
            self.fail("Error deleting host group {0} - {1}".format(self.name, str(exc)))
        return response

    def hostgroup_to_dict(self, hostgroup):
        result = hostgroup.as_dict()
        result['tags'] = hostgroup.tags
        return result


def main():
    AzureRMHostGroup()


if __name__ == '__main__':
    main()
