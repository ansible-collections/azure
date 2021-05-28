#!/usr/bin/python
#
# Copyright (c) 2021 Aparna Patil(@techcon65)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_privatednszonelink

version_added: "1.6.0"

short_description: Create, delete and update Virtual network link for Private DNS zone

description:
    - Creates, deletes, and updates Virtual network links for an existing Azure Private DNS Zone.

options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    name:
        description:
            - The name of the virtual network link.
        required: true
        type: str
    zone_name:
        description:
            - The name of the Private DNS zone.
        required: true
        type: str
    registration_enabled:
        description:
            - Is auto-registration of virtual machine records in the virtual network in the Private DNS zone enabled
        default: false
        type: bool
    virtual_network:
        description:
            - The reference of the virtual network.
        type: str
    state:
        description:
            - Assert the state of the virtual network link. Use C(present) to create or update and C(absent) to delete.
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
- name: Create a virtual network link
  azure_rm_privatednszonelink:
    resource_group: myResourceGroup
    name: vnetlink1
    zone_name: privatezone.com
    virtual_network: MyAzureVNet
    state: present

- name: Update virtual network link
  azure_rm_privatednszonelink:
    resource_group: myResourceGroup
    name: vnetlink1
    zone_name: privatezone.com
    virtual_network: MyAzureVNet
    registration_enabled: true
    state: present
    tags:
      key1: "value1"

- name: Delete a virtual network link
  azure_rm_privatednszonelink:
    resource_group: myResourceGroup
    name: vnetlink1
    zone_name: privatezone.com
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the Virtual network link.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The Virtual network link ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/
                     Microsoft.Network/privateDnsZones/privatezone.com/virtualNetworkLinks/vnetlink1"
        name:
            description:
                - Virtual network link name.
            returned: always
            type: str
            sample: 'vnetlink1'
        location:
            description:
                - The Azure Region where the resource lives.
            returned: always
            type: str
            sample: global
        etag:
            description:
                - The etag of the virtual network link.
            returned: always
            type: str
            sample: 692c3e92-a618-46fc-aecd-8f888807cd6c
        tags:
            description:
                - Resource tags.
            returned: always
            type: list
            sample: [{"key1": "value1"}]
        virtual_network:
            description:
                - Reference to virtual network.
            returned: always
            type: dict
            sample: {
                "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/
                       providers/Microsoft.Network/virtualNetworks/MyAzureVNet"
            }
        registration_enabled:
            description:
                - The status of auto-registration of virtual machine records in the virtual network in private DNS zone.
            returned: always
            type: bool
            sample: true
        provisioning_state:
            description:
                - The provisioning state of the resource.
            returned: always
            type: str
            sample: Succeeded
        virtual_network_link_state:
            description:
                - The status of the virtual network link.
            returned: always
            type: str
            sample: Completed
'''

from ansible.module_utils.basic import _load_params
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, HAS_AZURE, \
    format_resource_id

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVirtualNetworkLink(AzureRMModuleBase):

    def __init__(self):

        _load_params()
        # define user inputs from playbook
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            zone_name=dict(type='str', required=True),
            virtual_network=dict(type='str'),
            state=dict(choices=['present', 'absent'], default='present', type='str'),
            registration_enabled=dict(type='bool', default=False)
        )

        required_if = [
            ('state', 'present', ['virtual_network'])
        ]

        self.results = dict(
            changed=False,
            state=dict()
        )

        self.resource_group = None
        self.name = None
        self.zone_name = None
        self.virtual_network = None
        self.registration_enabled = None
        self.state = None
        self.tags = None
        self.log_path = None
        self.log_mode = None

        super(AzureRMVirtualNetworkLink, self).__init__(self.module_arg_spec,
                                                        required_if=required_if,
                                                        supports_tags=True,
                                                        supports_check_mode=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False
        results = dict()
        zone = None
        virtual_network_link_old = None
        virtual_network_link_new = None

        # retrieve resource group to make sure it exists
        self.get_resource_group(self.resource_group)

        if self.virtual_network:
            virtual_network = self.parse_resource_to_dict(self.virtual_network)
            self.virtual_network = format_resource_id(val=virtual_network['name'],
                                                      subscription_id=virtual_network['subscription_id'],
                                                      namespace='Microsoft.Network',
                                                      types='virtualNetworks',
                                                      resource_group=virtual_network['resource_group'])

        self.log('Fetching Private DNS zone {0}'.format(self.zone_name))
        zone = self.private_dns_client.private_zones.get(self.resource_group, self.zone_name)
        if not zone:
            self.fail('The zone {0} does not exist in the resource group {1}'.format(self.zone_name,
                                                                                     self.resource_group))

        try:
            self.log('Fetching Virtual network link {0}'.format(self.name))
            virtual_network_link_old = self.private_dns_client.virtual_network_links.get(self.resource_group,
                                                                                         self.zone_name,
                                                                                         self.name)
            # serialize object into a dictionary
            results = self.vnetlink_to_dict(virtual_network_link_old)
            if self.state == 'present':
                changed = False
                update_tags, results['tags'] = self.update_tags(results['tags'])
                if update_tags:
                    changed = True
                self.tags = results['tags']
                if self.registration_enabled != results['registration_enabled']:
                    changed = True
                    results['registration_enabled'] = self.registration_enabled
            elif self.state == 'absent':
                changed = True

        except CloudError:
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
                # create or update Virtual network link
                virtual_network_link_new = \
                    self.private_dns_models.VirtualNetworkLink(location='global',
                                                               registration_enabled=self.registration_enabled)
                if self.virtual_network:
                    virtual_network_link_new.virtual_network = \
                        self.network_models.VirtualNetwork(id=self.virtual_network)
                if self.tags:
                    virtual_network_link_new.tags = self.tags
                self.results['state'] = self.create_or_update_network_link(virtual_network_link_new)

            elif self.state == 'absent':
                # delete virtual network link
                self.delete_network_link()
                self.results['state'] = 'Deleted'

        return self.results

    def create_or_update_network_link(self, virtual_network_link):
        try:
            # create the virtual network link
            response = \
                self.private_dns_client.virtual_network_links.create_or_update(resource_group_name=self.resource_group,
                                                                               private_zone_name=self.zone_name,
                                                                               virtual_network_link_name=self.name,
                                                                               parameters=virtual_network_link)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error creating or updating virtual network link {0} - {1}".format(self.name, str(exc)))
        return self.vnetlink_to_dict(response)

    def delete_network_link(self):
        try:
            # delete the virtual network link
            response = self.private_dns_client.virtual_network_links.delete(resource_group_name=self.resource_group,
                                                                            private_zone_name=self.zone_name,
                                                                            virtual_network_link_name=self.name)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error deleting virtual network link {0} - {1}".format(self.name, str(exc)))
        return response

    def vnetlink_to_dict(self, virtualnetworklink):
        result = virtualnetworklink.as_dict()
        result['tags'] = virtualnetworklink.tags
        return result


def main():
    AzureRMVirtualNetworkLink()


if __name__ == '__main__':
    main()
