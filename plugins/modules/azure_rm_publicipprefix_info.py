#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-Sun (@Fred-Sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_publicipprefix_info

version_added: "2.2.0"

short_description: Get public IP prefix facts

description:
    - Get facts for a specific public IP prefix.
    - Get all facts for a specific public IP prefixes within a resource group.

options:
    name:
        description:
            - The name of the public IP prefix.
        type: str
    resource_group:
        description:
            - Limit results by resource group. Required when using name parameter.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get facts for one Public IP Prefix
  azure_rm_publicipprefix_info:
    resource_group: myResourceGroup
    name: publicipprefix

- name: Get facts for all Public IPs within a resource groups
  azure_rm_publicipprefix_info:
    resource_group: myResourceGroup
    tags:
      - key:value
'''

RETURN = '''
publicipprefix:
    description:
        - List of public IP prefixes dicts.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx---xxxxx/resourceGroups/v-xisuRG/providers/Microsoft.Network/publicIPPrefixes/pipb57dc95224
        name:
            description:
                - Name of the public IP prefix.
            returned: always
            type: str
            sample: prefix57dc95224
        type:
            description:
                - Resource type.
            returned: always
            type: str
            sample: "Microsoft.Network/publicIPPrefixes"
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: eastus
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: {
                    "delete": "on-exit",
                    "testing": "testing"
                    }
        public_ip_address_version:
            description:
                - The public IP address version.
                - Possible values are C(IPv4) and C(IPv6).
            returned: always
            type: str
            sample: IPv4
        ip_tags:
            description:
                - The list of tags associated with the public IP prefixes.
            returned: always
            type: list
            sample: [
                    {
                        "type": "FirstPartyUsage",
                        "value": "Storage"
                    }
                    ]
        provisioning_state:
            description:
                - The provisioning state of the PublicIP Prefix resource.
                - Possible values is C(Succeeded).
            returned: always
            type: str
            sample: Succeeded
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: "W/'1905ee13-7623-45b1-bc6b-4a12b2fb9d15'"
        sku:
            description:
                - The public IP prefix SKU.
            returned: always
            type: dict
            sample: {'name': 'standard', 'tier': 'Regional'}
        zones:
            description:
                - A list of availability zones denoting the IP allocated for the resource needs to come from.
            returned: always
            type: list
            sample: ['1', '2']
        prefix_length:
            description:
                - The Length of the Public IP Prefix.
            type: int
            returned: always
            sample: 29
        extended_location:
            description:
                - The extended location of the public ip address.
            type: str
            returned: always
            sample: 'eastus2'
        custom_ip_prefix:
            description:
                - The customIpPrefix that this prefix is associated with.
            type: dict
            returned: always
            sample: {}
        public_ip_addresses:
            description:
                - The list of all referenced PublicIPAddresses.
            type: list
            sample: []
        resource_guid:
            description:
                - The resource GUID property of the public IP prefix resource.
            type: str
            sample: "47cafa04-851d-4579-894d-74ad6afe3233"
        ip_prefix:
            description:
                - The allocated Prefix.
            type: str
            sample: 20.199.95.80/29
'''
try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

AZURE_OBJECT_CLASS = 'PublicIpPrefix'


class AzureRMPublicIPPrefixInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.results = dict(
            changed=False,
        )

        self.name = None
        self.resource_group = None
        self.tags = None

        super(AzureRMPublicIPPrefixInfo, self).__init__(self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=False,
                                                        facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        result = []
        if self.name is not None and self.resource_group is not None:
            result = self.get_item()
        elif self.resource_group:
            result = self.list_resource_group()
        else:
            result = self.list_all()

        raw = self.filter(result)

        self.results['publicipprefixes'] = self.format(raw)

        return self.results

    def format(self, raw):
        return [self.prefix_to_dict(item) for item in raw]

    def filter(self, response):
        return [item for item in response if self.has_tags(item.tags, self.tags)]

    def prefix_to_dict(self, prefix):
        result = dict(
            id=prefix.id,
            name=prefix.name,
            tags=prefix.tags,
            type=prefix.type,
            location=prefix.location,
            public_ip_address_version=prefix.public_ip_address_version,
            prefix_length=prefix.prefix_length,
            provisioning_state=prefix.provisioning_state,
            etag=prefix.etag,
            zones=prefix.zones,
            sku=dict(),
            ip_tags=list(),
            custom_ip_prefix=dict(),
            ip_prefix=prefix.ip_prefix,
            resource_guid=prefix.resource_guid,
            public_ip_addresses=list(),
            extended_location=prefix.extended_location
        )
        if prefix.public_ip_addresses:
            result['public_ip_addresses'] = [x.id for x in prefix.public_ip_addresses]
        if prefix.sku:
            result['sku']['name'] = prefix.sku.name
            result['sku']['tier'] = prefix.sku.tier
        if prefix.custom_ip_prefix:
            result['custom_ip_prefix']['id'] = prefix.custom_ip_prefix.id
        if prefix.ip_tags:
            result['ip_tags'] = [dict(type=x.ip_tag_type, value=x.tag) for x in prefix.ip_tags]
        return result

    def get_item(self):
        self.log('Get properties for {0}'.format(self.name))
        item = None
        try:
            item = self.network_client.public_ip_prefixes.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            pass
        return [item] if item else []

    def list_resource_group(self):
        self.log('List items in resource groups')
        try:
            response = self.network_client.public_ip_prefixes.list(self.resource_group)
        except ResourceNotFoundError as exc:
            self.fail("Error listing items in resource groups {0} - {1}".format(self.resource_group, str(exc)))
        return response

    def list_all(self):
        self.log('List all items')
        try:
            response = self.network_client.public_ip_prefixes.list_all()
        except ResourceNotFoundError as exc:
            self.fail("Error listing all items - {0}".format(str(exc)))
        return response


def main():
    AzureRMPublicIPPrefixInfo()


if __name__ == '__main__':
    main()
