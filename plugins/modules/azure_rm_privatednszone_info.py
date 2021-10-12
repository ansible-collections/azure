#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Jose Angel Munoz, <josea.munoz@gmail.com>
#
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_privatednszone_info

version_added: "0.0.1"

short_description: Get private DNS zone facts

description:
    - Get facts for a specific private DNS zone or all private DNS zones within a resource group.

options:
    resource_group:
        description:
            - Limit results by resource group. Required when filtering by name.
        type: str
    name:
        description:
            - Only show results for a specific zone.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Jose Angel Munoz (@imjoseangel)

'''

EXAMPLES = '''
- name: Get facts for one zone
  azure_rm_privatednszone_info:
    resource_group: myResourceGroup
    name: foobar22

- name: Get facts for all zones in a resource group
  azure_rm_privatednszone_info:
    resource_group: myResourceGroup

- name: Get facts for privatednszone with tags
  azure_rm_privatednszone_info:
    tags:
      - testing
      - foo:bar
'''

RETURN = '''
azure_privatednszones:
    description:
        - List of private zone dicts.
    returned: always
    type: list
    example:  [{
             "etag": "00000002-0000-0000-0dcb-df5776efd201",
                "location": "global",
                "properties": {
                    "maxNumberOfRecordSets": 5000,
                    "number_of_virtual_network_links": 0,
                    "number_of_virtual_network_links_with_registration": 0
                },
                "tags": {}
        }]
privatednszones:
    description:
        - List of private zone dicts, which share the same layout as azure_rm_privatednszone module parameter.
    returned: always
    type: list
    contains:
        id:
            description:
                - id of the private DNS Zone.
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/privatednszones/azure.com"
            type: str
        name:
            description:
                - name of the private DNS zone.
            sample: azure.com
            type: str
        number_of_record_sets:
            description:
                - The current number of record sets in this private DNS zone.
            type: int
            sample: 2
        number_of_virtual_network_links:
            description:
                - The current number of network links in this private DNS zone.
            type: int
            sample: 0
        number_of_virtual_network_links_with_registration:
            description:
                - The current number of network links with registration in this private DNS zone.
            type: int
            sample: 0
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils._text import to_native

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.common import AzureMissingResourceHttpError, AzureHttpError
except Exception:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'PrivateDnsZone'


class AzurePrivateRMDNSZoneInfo(AzureRMModuleBase):
    def __init__(self):

        # define user inputs into argument
        self.module_arg_spec = dict(name=dict(type='str'),
                                    resource_group=dict(type='str'),
                                    tags=dict(type='list'))

        # store the results of the module operation
        self.results = dict(changed=False,
                            ansible_info=dict(azure_privatednszones=[]))

        self.name = None
        self.resource_group = None
        self.tags = None

        super(AzurePrivateRMDNSZoneInfo, self).__init__(self.module_arg_spec, supports_check_mode=True)

    def exec_module(self, **kwargs):

        is_old_facts = self.module._name == 'azure_rm_privatednszone_facts'
        if is_old_facts:
            self.module.deprecate(
                "The 'azure_rm_privatednszone_facts' module has been renamed to 'azure_rm_privatednszone_info'",
                version=(2.9, ))

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name and not self.resource_group:
            self.fail(
                "Parameter error: resource group required when filtering by name."
            )

        results = []
        # list the conditions and what to return based on user input
        if self.name is not None:
            # if there is a name, facts about that specific zone
            results = self.get_item()
        elif self.resource_group:
            # all the zones listed in that specific resource group
            results = self.list_resource_group()
        else:
            # all the zones in a subscription
            results = self.list_items()

        self.results['ansible_info'][
            'azure_privatednszones'] = self.serialize_items(results)
        self.results['privatednszones'] = self.curated_items(results)

        return self.results

    def get_item(self):
        self.log('Get properties for {0}'.format(self.name))
        item = None
        results = []
        # get specific zone
        try:
            item = self.private_dns_client.private_zones.get(
                self.resource_group, self.name)
        except CloudError:
            pass

        # serialize result
        if item and self.has_tags(item.tags, self.tags):
            results = [item]
        return results

    def list_resource_group(self):
        self.log('List items for resource group')
        try:
            response = self.private_dns_client.private_zones.list_by_resource_group(
                self.resource_group)
        except AzureHttpError as exc:
            self.fail("Failed to list for resource group {0} - {1}".format(
                self.resource_group, str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def list_items(self):
        self.log('List all items')
        try:
            response = self.private_dns_client.private_zones.list()
        except AzureHttpError as exc:
            self.fail("Failed to list all items - {0}".format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def serialize_items(self, raws):
        return [self.serialize_obj(item, AZURE_OBJECT_CLASS)
                for item in raws] if raws else []

    def curated_items(self, raws):
        return [self.zone_to_dict(item) for item in raws] if raws else []

    def zone_to_dict(self, zone):
        return dict(id=zone.id,
                    name=zone.name,
                    number_of_record_sets=zone.number_of_record_sets,
                    number_of_virtual_network_links=zone.
                    number_of_virtual_network_links,
                    number_of_virtual_network_links_with_registration=zone.
                    number_of_virtual_network_links_with_registration,
                    tags=zone.tags)


def main():
    AzurePrivateRMDNSZoneInfo()


if __name__ == '__main__':
    main()
