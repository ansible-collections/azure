#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-Sun (@Fred-Sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_publicipprefix

version_added: "2.2.0"

short_description: Manage Azure Public IP prefix

description:
    - Create, update and delete a Public IP prefix.

options:
    resource_group:
        description:
            - Name of resource group with which the Public IP prefix is associated.
        required: true
        type: str
    name:
        description:
            - Name of the Public IP prefix.
        required: true
        type: str
    state:
        description:
            - Assert the state of the Public IP. Use C(present) to create or update a and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present
    location:
        description:
            - Valid Azure location. Defaults to location of the resource group.
        type: str
    sku:
        description:
            - The public IP prefix SKU.
        type: dict
        suboptions:
            name:
                description:
                    - Name of a public IP prefix SKU.
                type: str
                choices:
                    - Standard
            tier:
                description:
                    - Tier of a public IP prefix SKU.
                type: str
                choices:
                    - Regional
                    - Global
    custom_ip_prefix:
        description:
            - The Custom IP prefix that this prefix is associated with.
        type: dict
        suboptions:
            id:
                description:
                    - Resource ID.
                type: str
    extended_location:
        description:
            - The extended location of the public ip address.
        type: str
    ip_tags:
        description:
            - The list of tags associated with the public IP prefix.
        type: list
        elements: dict
        suboptions:
            ip_tag_type:
                description:
                    - The IP tag type. Example as FirstPartyUsage.
                type: str
            tag:
                description:
                    - The value of the IP tag associated with the public IP. Example as SQL.
                type: str
    public_ip_address_version:
        description:
            - The public IP address version.
        type: str
        choices:
            - IPV4
            - IPV6
    zones:
        description:
            - A list of availability zones denoting the IP prefix allocated for the resource needs to come from.
        type: list
        elements: str
        choices:
            - '1'
            - '2'
            - '3'
    prefix_length:
        description:
            - The Length of the Public IP Prefix.
        type: int

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Create a public ip prefix
  azure_rm_publicipprefix:
    resource_group: myResourceGroup
    name: my_public_ip
    public_ip_address_version: IPV4
    prefix_length: 29
    sku:
      name: Standard
      tier: Regional
    zones:
      - 1
    tags:
      key1: value1

- name: Delete public ip prefix
  azure_rm_publicipprefix:
    resource_group: myResourceGroup
    name: my_public_ipprefix
    state: absent
'''

RETURN = '''
state:
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
            sample: [{'type': 'FirstPartyUsage', 'value': 'Storage'}]
        resource_guid:
            description:
                - The resource GUID property of the public IP prefix resource.
            type: str
            sample: "47cafa04-851d-4579-894d-74ad6afe3233"
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
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


def prefix_to_dict(prefix):
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


class AzureRMPublicIPPrefix(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            public_ip_address_version=dict(type='str', choices=['IPV4', 'IPV6']),
            extended_location=dict(type='str'),
            prefix_length=dict(type='int'),
            custom_ip_prefix=dict(
                type='dict',
                options=dict(
                    id=dict(type='str')
                )
            ),
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(type='str', choices=['Standard']),
                    tier=dict(type='str', choices=['Regional', 'Global'])
                )
            ),
            ip_tags=dict(
                type='list',
                elements='dict',
                options=dict(
                    ip_tag_type=dict(type='str'),
                    tag=dict(type='str')
                )
            ),
            zones=dict(type='list', elements='str', choices=['1', '2', '3'])
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.state = None
        self.tags = None
        self.zones = None
        self.sku = None
        self.ip_tags = None
        self.public_ip_address_version = None
        self.prefix_length = None
        self.custom_ip_prefix = None

        self.results = dict(
            changed=False,
            state=dict()
        )

        super(AzureRMPublicIPPrefix, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        results = dict()
        changed = False
        prefix = None
        update_tags = False

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        try:
            self.log("Fetch public ip prefix {0}".format(self.name))
            prefix = self.network_client.public_ip_prefixes.get(self.resource_group, self.name)
            self.log("Public IP prefix {0} exists".format(self.name))

            if self.state == 'present':
                results = prefix_to_dict(prefix)

                if self.public_ip_address_version is not None and \
                   self.public_ip_address_version.lower() != results['public_ip_address_version'].lower():
                    changed = False
                    results['public_ip_address_version'] = self.public_ip_address_version
                    self.fail("The public_ip_address_version can't be updated")

                if self.prefix_length is not None and self.prefix_length != results['prefix_length']:
                    changed = False
                    results['prefix_length'] = self.prefix_length
                    self.fail("The prefix_length can't be updated")

                if self.sku is not None:
                    for key in self.sku.keys():
                        if self.sku[key] != results['sku'].get(key):
                            changed = False
                            self.fail("The sku can't be updated")
                            results['sku'] = self.sku

                if self.zones is not None and not all(key in results['zones'] for key in self.zones):
                    changed = False
                    results['zones'] = self.zones
                    self.fail("The zone can't be updated")

                if self.extended_location is not None and self.extended_location != results['extended_location']:
                    changed = False
                    results['extended_location'] = self.extended_location
                    self.fail("The extended_location can't be updated")

                if self.ip_tags is not None:
                    for key in self.ip_tags.keys():
                        if self.ip_tags[key] != results['ip_tags'].get(key):
                            changed = False
                            results['ip_tags'] = self.ip_tags
                            self.fail("The ip_tags can't be updated")

                if self.custom_ip_prefix is not None:
                    if results.get('custom_ip_prefix') is None:
                        changed = False
                        results['custom_ip_prefix'] = self.custom_ip_prefix
                        self.fail("The custom_ip_prefix can't be updated")
                    elif self.custom_ip_prefix['id'].lower() != results['custom_ip_prefix']['id'].lower():
                        changed = False
                        results['custom_ip_prefix'] = self.custom_ip_prefix
                        self.fail("The custom_ip_prefix can't be updated")

                update_tags, results['tags'] = self.update_tags(results['tags'])
                if update_tags:
                    self.log("CHANGED: tags")
                    changed = True
                self.tags = results['tags']

            elif self.state == 'absent':
                self.log("CHANGED: public ip prefix {0} exists but requested state is 'absent'".format(self.name))
                changed = True
        except ResourceNotFoundError:
            self.log('Public ip prefix {0} does not exist'.format(self.name))
            if self.state == 'present':
                self.log("CHANGED: public IP prefix {0} does not exist but requested state is 'present'".format(self.name))
                changed = True

        self.results['state'] = results
        self.results['changed'] = changed

        if self.check_mode:
            results['changed'] = True
            return results

        if update_tags:
            self.results['state'] = self.update_prefix_tags(self.tags)

        elif changed:
            if self.state == 'present':
                self.log("Create or Update Public IP prefix {0}".format(self.name))
                prefix = self.network_models.PublicIPPrefix(
                    location=self.location,
                    public_ip_address_version=self.public_ip_address_version,
                    prefix_length=self.prefix_length,
                    zones=self.zones,
                    tags=self.tags,
                    sku=self.sku,
                    ip_tags=self.ip_tags,
                    custom_ip_prefix=self.custom_ip_prefix
                )
                self.results['state'] = self.create_or_update_prefix(prefix)

            elif self.state == 'absent':
                self.log('Delete public ip {0}'.format(self.name))
                self.delete_prefix()

        return self.results

    def update_prefix_tags(self, tags):
        try:
            prefix = self.network_client.public_ip_prefixes.update_tags(self.resource_group, self.name, dict(tags=tags))
        except Exception as exc:
            self.fail("Error updating tags {0} - {1}".format(self.name, str(exc)))
        return prefix_to_dict(prefix)

    def create_or_update_prefix(self, prefix):
        try:
            poller = self.network_client.public_ip_prefixes.begin_create_or_update(self.resource_group, self.name, prefix)
            prefix = self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error creating or updating {0} - {1}".format(self.name, str(exc)))
        return prefix_to_dict(prefix)

    def delete_prefix(self):
        try:
            poller = self.network_client.public_ip_prefixes.begin_delete(self.resource_group, self.name)
            self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error deleting {0} - {1}".format(self.name, str(exc)))

        self.results['state']['status'] = 'Deleted'
        return True


def main():
    AzureRMPublicIPPrefix()


if __name__ == '__main__':
    main()
