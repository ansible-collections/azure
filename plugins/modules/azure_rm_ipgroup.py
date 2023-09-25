#!/usr/bin/python
#
# Copyright (c) 2021 Aparna Patil(@techcon65)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ipgroup

version_added: "1.6.0"

short_description: Create, delete and update IP group

description:
    - Creates, deletes, and updates IP group in specified resource group.

options:
    resource_group:
        description:
            - Name of the resource group.
        required: true
        type: str
    name:
        description:
            - The name of the IP group.
        required: true
        type: str
    location:
        description:
            - Location for IP group. Defaults to location of resource group if not specified.
        type: str
    ip_addresses:
        description:
            - The List of IP addresses in IP group.
        type: list
        elements: str
    state:
        description:
            - Assert the state of the IP group. Use C(present) to create or update and C(absent) to delete.
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
- name: Create IP Group
  azure_rm_ipgroup:
    resource_group: MyAzureResourceGroup
    name: myipgroup
    location: eastus
    ip_addresses:
      - 13.64.39.16/32
      - 40.74.146.80/31
      - 40.74.147.32/28
    tags:
      key1: "value1"
    state: present

- name: Update IP Group
  azure_rm_ipgroup:
    resource_group: MyAzureResourceGroup
    name: myipgroup
    location: eastus
    ip_addresses:
      - 10.0.0.0/24
    tags:
      key2: "value2"

- name: Delete IP Group
  azure_rm_ipgroup:
    resource_group: MyAzureResourceGroup
    name: myipgroup
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the IP group.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The IP group ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/MyAzureResourceGroup/providers/
                     Microsoft.Network/ipGroups/myipgroup"
        name:
            description:
                - The IP group name.
            returned: always
            type: str
            sample: 'myipgroup'
        location:
            description:
                - The Azure Region where the resource lives.
            returned: always
            type: str
            sample: eastus
        ip_addresses:
            description:
                - The list of IP addresses in IP group.
            returned: always
            type: list
            elements: str
            sample: [
            "13.64.39.16/32",
            "40.74.146.80/31",
            "40.74.147.32/28"
        ]
        provisioning_state:
            description:
                - The provisioning state of the resource.
            returned: always
            type: str
            sample: Succeeded
        firewalls:
            description:
                - List of references to Firewall resources that this IpGroups is associated with.
            returned: always
            type: list
            elements: dict
            sample: [
            {
              "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myAzureResourceGroup/providers/
                     Microsoft.Network/azureFirewalls/azurefirewall"
            }
        ]
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
            sample: Microsoft.Network/IpGroups
        etag:
            description:
                - The etag of the IP group.
            returned: always
            type: str
            sample: c67388ea-6dab-481b-9387-bd441c0d32f8
'''

from ansible.module_utils.basic import _load_params
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, normalize_location_name

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMIPGroup(AzureRMModuleBase):

    def __init__(self):

        _load_params()
        # define user inputs from playbook
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            ip_addresses=dict(type='list', elements='str'),
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
        self.ip_addresses = None
        self.tags = None

        super(AzureRMIPGroup, self).__init__(self.module_arg_spec,
                                             supports_check_mode=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False
        results = dict()
        ip_group_old = None
        ip_group_new = None

        # retrieve resource group to make sure it exists
        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        self.location = normalize_location_name(self.location)

        try:
            self.log('Fetching IP group {0}'.format(self.name))
            ip_group_old = self.network_client.ip_groups.get(self.resource_group, self.name)
            # serialize object into a dictionary
            results = self.ipgroup_to_dict(ip_group_old)
            if self.state == 'present':
                changed = False
                update_tags, results['tags'] = self.update_tags(results['tags'])
                if update_tags:
                    changed = True
                self.tags = results['tags']
                update_ip_address = self.ip_addresses_changed(self.ip_addresses, results['ip_addresses'])
                if update_ip_address:
                    changed = True
                    results['ip_addresses'] = self.ip_addresses
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
                # create or update ip group
                ip_group_new = \
                    self.network_models.IpGroup(location=self.location,
                                                ip_addresses=self.ip_addresses)
                if self.tags:
                    ip_group_new.tags = self.tags
                self.results['state'] = self.create_or_update_ipgroup(ip_group_new)

            elif self.state == 'absent':
                # delete ip group
                self.delete_ipgroup()
                self.results['state'] = 'Deleted'

        return self.results

    def create_or_update_ipgroup(self, ip_group):
        try:
            # create ip group
            response = self.network_client.ip_groups.begin_create_or_update(resource_group_name=self.resource_group,
                                                                            ip_groups_name=self.name,
                                                                            parameters=ip_group)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error creating or updating IP group {0} - {1}".format(self.name, str(exc)))
        return self.ipgroup_to_dict(response)

    def delete_ipgroup(self):
        try:
            # delete ip group
            response = self.network_client.ip_groups.begin_delete(resource_group_name=self.resource_group,
                                                                  ip_groups_name=self.name)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error deleting IP group {0} - {1}".format(self.name, str(exc)))
        return response

    def ip_addresses_changed(self, input_records, ip_group_records):
        # comparing IP addresses list

        input_set = set(input_records)
        ip_group_set = set(ip_group_records)

        changed = input_set != ip_group_set

        return changed

    def ipgroup_to_dict(self, ipgroup):
        result = ipgroup.as_dict()
        result['tags'] = ipgroup.tags
        return result


def main():
    AzureRMIPGroup()


if __name__ == '__main__':
    main()
