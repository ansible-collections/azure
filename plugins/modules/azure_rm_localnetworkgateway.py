#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_localnetworkgateway
version_added: "1.14.0"
short_description: Manage Azure local network gateways
description: Create, update or delete a local network gateway.
author:
  - Nilashish Chakraborty (@NilashishC)
options:
  resource_group:
    description: Name of a resource group where local network gateway exists or will be created.
    required: true
  name:
    description: Name of Local Network Gateway.
    required: true
  state:
    description: State of the Local Network Gateway. Use C(present) to create or update local network gateway and C(absent) to delete it.
    default: present
    choices: ["absent", "present"]
  location:
    description: Valid Azure location. Defaults to location of the resource group.
    type: str
  local_network_address_space:
    description: Local network site address space.
    type: list
    elements: str
  gateway_ip_address:
    description: IP address of local network gateway.
    type: str
  bgp_settings:
    description: Local network gateway's BGP speaker settings.
    type: dict
    suboptions:
      asn:
        description: The BGP speaker's ASN.
        type: str
      bgp_peering_address:
        description: The BGP peering address and BGP identifier of this BGP speaker.
        type: str
      peer_weight:
        description: The weight added to routes learned from this BGP speaker.
        type: int
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
'''

EXAMPLES = '''
    - name: Create Azure Local Network Gateway
      azure.azcollection.azure_rm_localnetworkgateway:
        name: Test-VPN
        location: West US 3
        resource_group: Test-VPN-RG
        gateway_ip_address: 18.110.215.218
        local_network_address_space:
          - "192.168.1.0/24"
'''

RETURN = '''
id:
    description:
        - Local Network Gateway resource ID.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/LocalNetworkGateways/myLocalNetworkGateway"
'''
try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


def lngw_to_dict(lngw):
    results = dict(
        id=lngw.id,
        name=lngw.name,
        location=lngw.location,
        bgp_settings=dict(
            asn=lngw.bgp_settings.asn,
            bgp_peering_address=lngw.bgp_settings.bgp_peering_address,
            peer_weight=lngw.bgp_settings.peer_weight
        ) if lngw.bgp_settings else None,
        etag=lngw.etag,
        fqdn=lngw.fqdn,
        tags=lngw.tags,
        provisioning_state=lngw.provisioning_state,
        local_network_address_space=lngw.local_network_address_space.address_prefixes,
        gateway_ip_address=lngw.gateway_ip_address,
    )
    return results

class AzureRMLocalNetworkGateway(AzureRMModuleBase):

    def __init__(self):
        
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            local_network_address_space=dict(type='list', elements='str'),
            gateway_ip_address=dict(type='str'),
            bgp_settings=dict(
                type='dict', 
                options=dict(
                    asn=dict(type='str'), 
                    bgp_peering_address=dict(type='str'),
                    peer_weight=dict(type='int'),
                )
            )
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None

        self.results = dict(
            changed=False,
            state=dict()
        )

        super(AzureRMLocalNetworkGateway, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                           supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False
        results = dict()
        lngw = None

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        resource_group = self.get_resource_group(self.resource_group)

        # get local network gateway if it exists
        try:
            lngw = self.network_client.local_network_gateways.get(self.resource_group, self.name)
            if self.state == 'absent':
                self.log("CHANGED: Local Network Gateway exists but requested state is 'absent'")
                changed = True
        except ResourceNotFoundError:
            if self.state == 'present':
                self.log("CHANGED: Local Network Gateway {0} does not exist but requested state is 'present'".format(self.name))
                changed = True
            
        if lngw:
            results = lngw_to_dict(lngw)
            if self.state == 'present':
                update_tags, results['tags'] = self.update_tags(results['tags'])
                if update_tags:
                    changed = True
                if self.bgp_settings and self.bgp_settings != results['bgp_settings']:
                    changed = True
                if self.local_network_address_space != results['local_network_address_space']:
                    changed = True
                if self.gateway_ip_address != results['gateway_ip_address']:
                    changed = True
                lngw_addr = self.network_models.AddressSpace(
                    address_prefixes=self.local_network_address_space,
                )
            
        self.results['changed'] = changed
        self.results['id'] = results.get('id')

        if self.check_mode:
            return self.results
        
        if changed:
            if self.state == "present":
                lngw_addr = self.network_models.AddressSpace(
                    address_prefixes=self.local_network_address_space,
                )
                lngw_bgp = self.network_models.BgpSettings(
                        asn=self.bgp_settings['asn'],
                        bgp_peering_address=self.bgp_settings['bgp_peering_address'],
                        peer_weight=self.bgp_settings['peer_weight'],
                ) if self.bgp_settings is not None else None

                lngw = self.network_models.LocalNetworkGateway(
                    location=self.location,
                    local_network_address_space=lngw_addr,
                    bgp_settings=lngw_bgp,
                    gateway_ip_address=self.gateway_ip_address,
                )
                if self.tags:
                    lngw.tags = self.tags
                results = self.create_or_update_lngw(lngw)

            else:
                results = self.delete_lngw()
        
        if self.state == 'present':
            self.results['id'] = results['id']
        return self.results

    def create_or_update_lngw(self, lngw):
        try:
            poller = self.network_client.local_network_gateways.begin_create_or_update(self.resource_group, self.name, lngw)
            new_lngw = self.get_poller_result(poller)
            return lngw_to_dict(new_lngw)
        except Exception as exc:
            self.fail("Error creating or updating local network gateway {0} - {1}".format(self.name, str(exc)))
    
    def delete_lngw(self):
        try:
            poller = self.network_client.local_network_gateways.begin_delete(self.resource_group, self.name)
            self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error deleting local network gateway {0} - {1}".format(self.name, str(exc)))
        return True


def main():
    AzureRMLocalNetworkGateway()


if __name__ == '__main__':
    main()
