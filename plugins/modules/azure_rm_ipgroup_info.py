#!/usr/bin/python
#
# Copyright (c) 2021 Aparna Patil(@techcon65)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ipgroup_info

version_added: "1.6.0"

short_description: Get IP group facts

description:
    - Get facts for specified IP group or all IP groups in a given resource group.

options:
    resource_group:
        description:
            - Name of the resource group.
        type: str
    name:
        description:
            - Name of the IP group.
        type: str
    tags:
        description:
            -  Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Aparna Patil (@techcon65)

'''

EXAMPLES = '''
- name: Get facts for one IP group
  azure_rm_ipgroup_info:
    resource_group: myAzureResourceGroup
    name: myipgroup

- name: Get facts for all IP groups in resource group
  azure_rm_ipgroup_info:
    resource_group: myAzureResourceGroup
'''

RETURN = '''
ipgroups:
    description:
        - Gets a list of IP groups.
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "etag": "c67388ea-6dab-481b-9387-bd441c0d32f8",
            "firewalls": [],
            "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/MyAzureResourceGroup/providers/
                   Microsoft.Network/ipGroups/myipgroup",
            "ip_addresses": [
                "13.64.39.16/32",
                "40.74.146.80/31",
                "40.74.147.32/28"
            ],
            "location": "eastus",
            "name": "myipgroup",
            "provisioning_state": "Succeeded",
            "tags": {
                "key1": "value1"
            }
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.common import AzureMissingResourceHttpError, AzureHttpError
except Exception:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'IpGroup'


class AzureRMIPGroupInfo(AzureRMModuleBase):

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

        super(AzureRMIPGroupInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        results = []
        # list the conditions and results to return based on user input
        if self.name is not None:
            # if there is IP group name provided, return facts about that specific IP group
            results = self.get_item()
        elif self.resource_group:
            # all the IP groups listed in specific resource group
            results = self.list_resource_group()
        else:
            # all the IP groups in a subscription
            results = self.list_items()

        self.results['ipgroups'] = self.curated_items(results)

        return self.results

    def get_item(self):
        self.log('Get properties for {0}'.format(self.name))
        item = None
        results = []
        # get specific IP group
        try:
            item = self.network_client.ip_groups.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            pass

        # serialize result
        if item and self.has_tags(item.tags, self.tags):
            results = [item]
        return results

    def list_resource_group(self):
        self.log('List all IP groups for resource group - {0}'.format(self.resource_group))
        try:
            response = self.network_client.ip_groups.list_by_resource_group(self.resource_group)
        except ResourceNotFoundError as exc:
            self.fail("Failed to list for resource group {0} - {1}".format(self.resource_group, str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def list_items(self):
        self.log('List all IP groups for a subscription ')
        try:
            response = self.network_client.ip_groups.list()
        except ResourceNotFoundError as exc:
            self.fail("Failed to list all items - {0}".format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def curated_items(self, raws):
        return [self.ipgroup_to_dict(item) for item in raws] if raws else []

    def ipgroup_to_dict(self, ipgroup):
        result = dict(
            id=ipgroup.id,
            name=ipgroup.name,
            location=ipgroup.location,
            tags=ipgroup.tags,
            ip_addresses=ipgroup.ip_addresses,
            provisioning_state=ipgroup.provisioning_state,
            firewalls=[dict(id=x.id) for x in ipgroup.firewalls],
            etag=ipgroup.etag
        )
        return result


def main():
    AzureRMIPGroupInfo()


if __name__ == '__main__':
    main()
