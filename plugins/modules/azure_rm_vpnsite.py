#!/usr/bin/python
#
# Copyright (c) 2020 Gu Fred-Sun, (@Fred-Sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_vpnsite
version_added: '1.5.0'
short_description: Manage Azure VpnSite instance
description:
    - Create, update and delete instance of Azure VpnSite.
options:
    resource_group:
        description:
            - The resource group name of the VpnSite.
        required: true
        type: str
    location:
        description:
            - The location of the VpnSite
        type: str
    name:
        description:
            - The name of the VpnSite.
        required: true
        type: str
    virtual_wan:
        description:
            - The VirtualWAN to which the vpnSite belongs.
        type: dict
        suboptions:
            id:
                description:
                    - The resource ID of the related virtual wan.
                type: str
    device_properties:
        description:
            - The device properties.
        type: dict
        suboptions:
            device_vendor:
                description:
                    - Name of the device Vendor.
                type: str
            device_model:
                description:
                    - Model of the device.
                type: str
            link_speed_in_mbps:
                description:
                    - Link speed.
                type: int
    ip_address:
        description:
            - The ip-address for the vpn-site.
        type: str
    site_key:
        description:
            - The key for vpn-site that can be used for connections.
        type: str
    address_space:
        description:
            - The AddressSpace that contains an array of IP address ranges.
        type: dict
        suboptions:
            address_prefixes:
                description:
                    - A list of address blocks reserved for this virtual network in CIDR notation.
                type: list
                elements: str
    bgp_properties:
        description:
            - The set of bgp properties.
        type: dict
        suboptions:
            asn:
                description:
                    - The BGP speaker's ASN.
                type: int
            bgp_peering_address:
                description:
                    - The BGP peering address and BGP identifier of this BGP speaker.
                type: str
            peer_weight:
                description:
                    - The weight added to routes learned from this BGP speaker.
                type: int
            bgp_peering_addresses:
                description:
                    - BGP peering address with IP configuration ID for virtual network gateway.
                type: list
                elements: dict
                suboptions:
                    ipconfiguration_id:
                        description:
                            - The ID of IP configuration which belongs to gateway.
                        type: str
                    default_bgp_ip_addresses:
                        description:
                            - The list of default BGP peering addresses which belong to IP configuration.
                        type: list
                        elements: str
                    custom_bgp_ip_addresses:
                        description:
                            - The list of custom BGP peering addresses which belong to IP configuration.
                        type: list
                        elements: str
                    tunnel_ip_addresses:
                        description:
                            - The list of tunnel public IP addresses which belong to IP configuration.
                        type: list
                        elements: str
    is_security_site:
        description:
            - IsSecuritySite flag.
        type: bool
    vpn_site_links:
        description:
            - List of all vpn site links.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of the resource that is unique within a resource group.
                    - This name can be used to access the resource.
                type: str
            link_properties:
                description:
                    - The link provider properties.
                type: dict
                suboptions:
                    link_provider_name:
                        description:
                            - Name of the link provider.
                        type: str
                    link_speed_in_mbps:
                        description:
                            - Link speed.
                        type: int
            ip_address:
                description:
                    - The IP address for the vpn site link.
                type: str
            fqdn:
                description:
                    - FQDN of vpn-site-link.
                type: str
            bgp_properties:
                description:
                    - The set of bgp properties.
                type: dict
                suboptions:
                    asn:
                        description:
                            - The BGP speaker's ASN.
                        type: int
                    bgp_peering_address:
                        description:
                            - The BGP peering address and BGP identifier of this BGP speaker.
                        type: str
    o365_policy:
        description:
            - Office365 Policy.
        type: dict
        suboptions:
            break_out_categories:
                description:
                    - Office365 breakout categories.
                type: dict
                suboptions:
                    allow:
                        description:
                            - Flag to control allow category.
                        type: bool
                    optimize:
                        description:
                            - Flag to control optimize category.
                        type: bool
                    default:
                        description:
                            - Flag to control default category.
                        type: bool
    state:
        description:
            - Assert the state of the VpnSite.
            - Use C(present) to create or update an VpnSite and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Fred-Sun (@Fred-Sun)

'''

EXAMPLES = '''
- name: Create VpnSite
  azure_rm_vpnsite:
    resource_group: myResourceGroup
    name: vpnSite_name

- name: Delete Vpn Site
  azure_rm_vpnsite:
    resource_group: myResourceGroup
    name: vpnSite_name
'''

RETURN = '''
state:
    description:
        - Current state of the vpn site.
    type: complex
    returned: success
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/v-xisuRG/providers/Microsoft.Network/vpnSites/vpn_site_name
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: vpn_site_name
        type:
            description:
                - Resource type.
            returned: always
            type: str
            sample: Microsoft.Network/vpnSites
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
            sample: { 'key1': 'value1'}
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: 8d7415fe-d92c-4331-92ea-460aadfb9648
        virtual_wan:
            description:
                - The VirtualWAN to which the vpnSite belongs.
            returned: always
            type: complex
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: /subscriptions/xxx-xxx/resourceGroups/v-xisuRG/providers/Microsoft.Network/virtualWans/virtualwan_name
        device_properties:
            description:
                - The device properties.
            returned: always
            type: complex
            contains:
                device_vendor:
                    description:
                        - Name of the device Vendor.
                    returned: always
                    type: str
                    sample: {"link_speed_in_mbps": 0}
        provisioning_state:
            description:
                - The provisioning state of the VPN site resource.
            returned: always
            type: str
            sample: "Succeeded"
        is_security_site:
            description:
                - IsSecuritySite flag.
            returned: always
            type: bool
            sample: false
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete, Update_tags = range(5)


class AzureRMVpnSite(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            virtual_wan=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str',
                    )
                )
            ),
            device_properties=dict(
                type='dict',
                options=dict(
                    device_vendor=dict(
                        type='str',
                    ),
                    device_model=dict(
                        type='str',
                    ),
                    link_speed_in_mbps=dict(
                        type='int',
                    )
                )
            ),
            ip_address=dict(
                type='str',
            ),
            site_key=dict(
                type='str',
                no_log=True,
            ),
            address_space=dict(
                type='dict',
                options=dict(
                    address_prefixes=dict(
                        type='list',
                        elements='str'
                    )
                )
            ),
            bgp_properties=dict(
                type='dict',
                options=dict(
                    asn=dict(
                        type='int',
                    ),
                    bgp_peering_address=dict(
                        type='str',
                    ),
                    peer_weight=dict(
                        type='int',
                    ),
                    bgp_peering_addresses=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            ipconfiguration_id=dict(
                                type='str',
                            ),
                            default_bgp_ip_addresses=dict(
                                type='list',
                                elements='str'
                            ),
                            custom_bgp_ip_addresses=dict(
                                type='list',
                                elements='str'
                            ),
                            tunnel_ip_addresses=dict(
                                type='list',
                                elements='str'
                            )
                        )
                    )
                )
            ),
            is_security_site=dict(
                type='bool',
            ),
            vpn_site_links=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(
                        type='str',
                    ),
                    link_properties=dict(
                        type='dict',
                        options=dict(
                            link_provider_name=dict(
                                type='str',
                            ),
                            link_speed_in_mbps=dict(
                                type='int',
                            )
                        )
                    ),
                    ip_address=dict(
                        type='str',
                    ),
                    fqdn=dict(
                        type='str',
                    ),
                    bgp_properties=dict(
                        type='dict',
                        options=dict(
                            asn=dict(
                                type='int',
                            ),
                            bgp_peering_address=dict(
                                type='str',
                            )
                        )
                    )
                )
            ),
            o365_policy=dict(
                type='dict',
                options=dict(
                    break_out_categories=dict(
                        type='dict',
                        options=dict(
                            allow=dict(
                                type='bool',
                            ),
                            optimize=dict(
                                type='bool',
                            ),
                            default=dict(
                                type='bool',
                            )
                        )
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.body = {}

        self.results = dict(changed=False)
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVpnSite, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_parameters(self.module_arg_spec, self.body, 0)

        resource_group = self.get_resource_group(self.resource_group)
        if self.location is None:
            # Set default location
            self.location = resource_group.location
        self.body['location'] = self.location

        old_response = None
        response = None

        old_response = self.get_resource()

        if not old_response:
            if self.state == 'present':
                self.to_do = Actions.Create
        else:
            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                if self.body.get('virtual_wan') is not None and self.body['virtual_wan'] != old_response.get('virtual_wan'):
                    self.to_do = Actions.Update
                for key in self.body.keys():
                    if key == 'address_space':
                        if old_response.get('address_space') is None or\
                           len(self.body['address_space']['address_prefixes']) > len(old_response['address_space']['address_prefixes']) or\
                           not all(key in old_response['address_space']['address_prefixes'] for key in self.body['address_space']['address_prefixes']):
                            self.to_do = Actions.Update
                    elif key == 'device_properties':
                        if old_response.get('device_properties') is None or\
                           not all(self.body['device_properties'][key] == old_response['device_properties'].get(key)
                           for key in self.body['device_properties'].keys()):
                            self.to_do = Actions.Update
                    elif key == 'o365_policy':
                        if old_response.get('o365_policy') is None or\
                           not all(self.body['o365_policy']['break_out_categories'][key] == old_response['o365_policy']['break_out_categories'].get(key)
                           for key in self.body['o365_policy']['break_out_categories'].keys()):
                            self.to_do = Actions.Update
                    elif key == 'vpn_site_links':
                        if old_response.get('vpn_site_links') is None or\
                           not all(self.body['vpn_site_links'][key] == old_response['vpn_site_links'].get(key)
                           for key in self.body['vpn_site_links'].keys()):
                            self.to_do = Actions.Update
                    elif key == 'bgp_properties':
                        if old_response.get('bgp_properties') is None:
                            self.to_do = Actions.Update
                        else:
                            for item in self.body['bgp_properties'].keys():
                                if item != 'bgp_peering_addresses' and item != 'peer_weight':
                                    if self.body['bgp_properties'][item] != old_response['bgp_properties'].get(item):
                                        self.to_do = Actions.Update
                                else:
                                    if self.body['bgp_properties'].get('bgp_peering_addresses') is not None:
                                        bgp_address = old_response['bgp_properties']['bgp_peering_addresses']
                                        if old_response['bgp_properties'].get('bgp_peering_addresses') is None or\
                                           not all(self.body['bgp_properties']['bgp_peering_addresses'][value] == bgp_address.get(value)
                                           for value in ['ipconfiguration_id', 'custom_bgp_ip_addresses']):
                                            self.to_do = Actions.Update

                    elif self.body[key] != old_response.get(key):
                        self.to_do = Actions.Update

                update_tags, self.tags = self.update_tags(old_response.get('tags'))
                if update_tags:
                    self.to_do = Actions.Update_tags

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.create_update_resource()
        elif self.to_do == Actions.Update_tags:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.update_resource_tags(dict(tags=self.tags))
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            self.delete_resource()
        else:
            self.results['changed'] = False
            response = old_response

        if response is not None:
            self.results['state'] = response
        return self.results

    def update_resource_tags(self, tags_parameters):
        try:
            response = self.network_client.vpn_sites.update_tags(resource_group_name=self.resource_group,
                                                                 vpn_site_name=self.name,
                                                                 vpn_site_parameters=tags_parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.log('Error attempting to update the VpnSite instance tags.')
            self.fail('Error updating the VpnSite instance: {0}'.format(str(exc)))
        return response.as_dict()

    def create_update_resource(self):
        try:
            response = self.network_client.vpn_sites.begin_create_or_update(resource_group_name=self.resource_group,
                                                                            vpn_site_name=self.name,
                                                                            vpn_site_parameters=self.body)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.log('Error attempting to create the VpnSite instance.')
            self.fail('Error creating the VpnSite instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.network_client.vpn_sites.begin_delete(resource_group_name=self.resource_group,
                                                                  vpn_site_name=self.name)
        except Exception as e:
            self.log('Error attempting to delete the VpnSite instance.')
            self.fail('Error deleting the VpnSite instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.network_client.vpn_sites.get(resource_group_name=self.resource_group,
                                                         vpn_site_name=self.name)
        except ResourceNotFoundError as e:
            return False
        return response.as_dict()


def main():
    AzureRMVpnSite()


if __name__ == '__main__':
    main()
