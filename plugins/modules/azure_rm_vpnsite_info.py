#!/usr/bin/python
#
# Copyright (c) 2020 Fred-Sun, (@Fred-Sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_vpnsite_info
version_added: '1.5.0'
short_description: Get VpnSite info
description:
    - Get info of VpnSite.
options:
    resource_group:
        description:
            - The resource group name of the VpnSite.
        type: str
    name:
        description:
            - The name of the VpnSite being retrieved.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Fred-Sun (@Fred-Sun)

'''

EXAMPLES = '''
- name: Get Vpn Site Info by name
  azure_rm_vpnsite_info:
    resource_group: myResourceGroup
    name: vwan_site_name

- name: Get Vpn Site List By ResourceGroup
  azure_rm_vpnsite_info:
    resource_group: myResourceGroup

- name: Get Vpn Site List By Subscription
  azure_rm_vpnsite_info:
'''

RETURN = '''
vpn_sites:
    description:
        - A list of dict results where the key is the name of the VpnSite and the values are the facts for that VpnSite.
    returned: always
    type: complex
    contains:
        id:
            description:
               - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/vpnSites/vwam_site_name
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: vwan_site_name
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
            sample: { "key1":"value1"}
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: 1d8c0731-adc6-4022-9c70-3c389cd73e2a
        virtual_wan:
            description:
                - The VirtualWAN to which the vpnSite belongs.
            returned: always
            type: dict
            sample: {"id": "/subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualWans/vwan_name"}
        device_properties:
            description:
                - The device properties.
            returned: always
            type: dict
            sample: {"device_vendor": "myVM", "link_speed_in_mbps": 0}
        address_space:
            description:
                - The AddressSpace that contains an array of IP address ranges.
            returned: always
            type: dict
            sample: {"address_prefixes": ["10.0.0.0/24",]}
        provisioning_state:
            description:
                - The provisioning state of the VPN site resource.
            returned: always
            type: str
            sample: "succeeded"
        is_security_site:
            description:
                - IsSecuritySite flag.
            returned: always
            type: bool
            sample: false
        vpn_site_links:
            description:
                - List of all vpn site links.
            returned: always
            type: complex
            contains:
                name:
                    description:
                         - The name of the resource that is unique within a resource group.
                         - This name can be used to access the resource.
                    returned: always
                    type: str
                    sample: azureuser
                link_properties:
                    description:
                        - The link provider properties.
                    returned: always
                    type: dict
                    sample: {"link_provider_name": "azureuser", "link_speed_in_mbps": 100}
                ip_address:
                    description:
                        - The ip-address for the vpn-site-link.
                    returned: always
                    type: str
                    sample: 192.168.33.223
                etag:
                    description:
                        - A unique read-only string that changes whenever the resource is updated.
                    returned: always
                    type: str
                    sample: 1d8c0731-adc6-4022-9c70-3c389cd73e2a
                id:
                    description:
                       - Resource ID.
                    returned: always
                    type: str
                    sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/vpnSites/vwam_site_name
                type:
                    description:
                        - Resource type.
                    returned: always
                    type: str
                    sample: Microsoft.Network/vpnSites
        o365_policy:
            description:
                - Office365 Policy.
            returned: always
            type: dict
            sample: {"break_out_categories": {"allow": false,"default": false,"optimize": false}}

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase
try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVpnSiteInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            name=dict(
                type='str'
            )
        )

        self.resource_group = None
        self.name = None

        self.results = dict(changed=False)

        super(AzureRMVpnSiteInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if (self.resource_group is not None and self.name is not None):
            self.results['vpn_sites'] = self.format_item(self.get())
        elif (self.resource_group is not None):
            self.results['vpn_sites'] = self.format_item(self.list_by_resource_group())
        else:
            self.results['vpn_sites'] = self.format_item(self.list())
        return self.results

    def get(self):
        response = None

        try:
            response = self.network_client.vpn_sites.get(resource_group_name=self.resource_group,
                                                         vpn_site_name=self.name)
        except ResourceNotFoundError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list_by_resource_group(self):
        response = None

        try:
            response = self.network_client.vpn_sites.list_by_resource_group(resource_group_name=self.resource_group)
        except ResourceNotFoundError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list(self):
        response = None

        try:
            response = self.network_client.vpn_sites.list()
        except ResourceNotFoundError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def format_item(self, item):
        if hasattr(item, 'as_dict'):
            return [item.as_dict()]
        elif item is not None:
            result = []
            items = list(item)
            for tmp in items:
                result.append(tmp.as_dict())
            return result
        else:
            return None


def main():
    AzureRMVpnSiteInfo()


if __name__ == '__main__':
    main()
