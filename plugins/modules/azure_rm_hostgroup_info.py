#!/usr/bin/python
#
# Copyright (c) 2021 Aparna Patil(@aparna-patil)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_hostgroup_info

version_added: "1.10.0"

short_description: Get host group facts

description:
    - Get facts for specified dedicated host group or all host groups in a given resource group.

options:
    resource_group:
        description:
            - Name of the resource group.
        type: str
    name:
        description:
            - Name of the host group.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Aparna Patil (@aparna-patil)

'''

EXAMPLES = '''
- name: Get facts for one host group
  azure_rm_hostgroup_info:
    resource_group: myAzureResourceGroup
    name: myhostgroup

- name: Get facts for all host groups in resource group
  azure_rm_hostgroup_info:
    resource_group: myAzureResourceGroup
'''

RETURN = '''
hostgroups:
    description:
        - Gets a list of dedicated host groups.
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "hosts": null,
            "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myAzureResourceGroup/providers/
                     Microsoft.Compute/hostGroups/myhostgroup",
            "location": "eastus",
            "name": "myhostgroup",
            "platform_fault_domain_count": 1,
            "tags": {
                      "key1": "value1"
                    },
            "zones": [
                       "1"
                     ]
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'HostGroup'


class AzureRMHostGroupInfo(AzureRMModuleBase):

    def __init__(self):

        # define user inputs into argument
        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        # store the results of the module operation
        self.results = dict(
            changed=False
        )

        self.name = None
        self.resource_group = None
        self.tags = None

        super(AzureRMHostGroupInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        results = []
        # list the conditions and results to return based on user input
        if self.name is not None:
            # if there is a host group name provided, return facts about that dedicated host group
            results = self.get_item()
        elif self.resource_group:
            # all the host groups listed in specific resource group
            results = self.list_resource_group()
        else:
            # all the host groups in a subscription
            results = self.list_items()

        self.results['hostgroups'] = self.curated_items(results)

        return self.results

    def get_item(self):
        self.log('Get properties for {0}'.format(self.name))
        item = None
        results = []
        # get specific host group
        try:
            item = self.compute_client.dedicated_host_groups.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            pass

        # serialize result
        if item and self.has_tags(item.tags, self.tags):
            results = [item]
        return results

    def list_resource_group(self):
        self.log('List all host groups for resource group - {0}'.format(self.resource_group))
        try:
            response = self.compute_client.dedicated_host_groups.list_by_resource_group(self.resource_group)
        except ResourceNotFoundError as exc:
            self.fail("Failed to list for resource group {0} - {1}".format(self.resource_group, str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def list_items(self):
        self.log('List all host groups for a subscription ')
        try:
            response = self.compute_client.dedicated_host_groups.list_by_subscription()
        except ResourceNotFoundError as exc:
            self.fail("Failed to list all items - {0}".format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def curated_items(self, raws):
        return [self.hostgroup_to_dict(item) for item in raws] if raws else []

    def hostgroup_to_dict(self, hostgroup):
        result = dict(
            id=hostgroup.id,
            name=hostgroup.name,
            location=hostgroup.location,
            tags=hostgroup.tags,
            platform_fault_domain_count=hostgroup.platform_fault_domain_count,
            zones=hostgroup.zones,
            hosts=[dict(id=x.id) for x in hostgroup.hosts] if hostgroup.hosts else None
        )
        return result


def main():
    AzureRMHostGroupInfo()


if __name__ == '__main__':
    main()
