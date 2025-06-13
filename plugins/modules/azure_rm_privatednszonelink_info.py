#!/usr/bin/python
#
# Copyright (c) 2021 Aparna Patil(@techcon65)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_privatednszonelink_info

version_added: "1.6.0"

short_description: Get Virtual Network link facts for private DNS zone

description:
    - Get a specified virtual network link or all virtual network links facts for a Private DNS zone.

options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    name:
        description:
            - The name of the virtual network link.
        type: str
    zone_name:
        description:
            - The name of the Private DNS zone.
        required: true
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Aparna Patil (@techcon65)

'''

EXAMPLES = '''
- name: Get facts for one virtual network link in private DNS zone
  azure_rm_privatednszonelink_info:
    resource_group: myResourceGroup
    name: vnetlink1
    zone_name: privatezone.com

- name: Get facts for all virtual network links in private DNS zone
  azure_rm_privatednszonelink_info:
    resource_group: myResourceGroup
    zone_name: privatezone.com
'''

RETURN = '''
virtualnetworklinks:
    description:
        - Gets a list of virtual network links dict in a Private DNS zone.
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/
                   Microsoft.Network/privateDnsZones/privatezone.com/virtualNetworkLinks/vnetlink1",
            "name": "vnetlink1",
            "provisioning_state": "Succeeded",
            "registration_enabled": true,
            "tags": {
                "key1": "value1"
            },
            "virtual_network": {
                "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/
                       providers/Microsoft.Network/virtualNetworks/MyAzureVNet"
            },
            "virtual_network_link_state": "Completed",
            'resolution_policy': 'null'
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'VirtualNetworkLink'


class AzureRMVirtualNetworkLinkInfo(AzureRMModuleBase):

    def __init__(self):

        # define user inputs into argument
        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str', required=True),
            zone_name=dict(type='str', required=True),
            tags=dict(type='list', elements='str')
        )

        # store the results of the module operation
        self.results = dict(
            changed=False
        )

        self.name = None
        self.resource_group = None
        self.zone_name = None
        self.tags = None
        self.log_path = None
        self.log_mode = None

        super(AzureRMVirtualNetworkLinkInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        results = []
        # list the conditions and results to return based on user input
        if self.name is not None:
            # if there is a link name provided, return facts about that specific virtual network link
            results = self.get_item()
        else:
            # all the virtual network links in specified private DNS zone
            results = self.list_items()

        self.results['virtualnetworklinks'] = self.curated_items(results)

        return self.results

    def get_item(self):
        self.log('Get properties for {0}'.format(self.name))
        item = None
        results = []
        # get specific virtual network link
        try:
            item = self.private_dns_client.virtual_network_links.get(self.resource_group,
                                                                     self.zone_name,
                                                                     self.name)
        except ResourceNotFoundError:
            pass

        # serialize result
        if item and self.has_tags(item.tags, self.tags):
            results = [item]
        return results

    def list_items(self):
        self.log('List all virtual network links for private DNS zone - {0}'.format(self.zone_name))
        try:
            response = self.private_dns_client.virtual_network_links.list(self.resource_group, self.zone_name)
        except Exception as exc:
            self.fail("Failed to list all items - {0}".format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def curated_items(self, raws):
        return [self.vnetlink_to_dict(item) for item in raws] if raws else []

    def vnetlink_to_dict(self, link):
        result = dict(
            id=link.id,
            name=link.name,
            virtual_network=dict(id=link.virtual_network.id),
            registration_enabled=link.registration_enabled,
            tags=link.tags,
            virtual_network_link_state=link.virtual_network_link_state,
            provisioning_state=link.provisioning_state,
            resolution_policy=link.resolution_policy
        )
        return result


def main():
    AzureRMVirtualNetworkLinkInfo()


if __name__ == '__main__':
    main()
