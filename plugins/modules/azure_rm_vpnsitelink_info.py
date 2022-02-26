#!/usr/bin/python
#
# Copyright (c) 2020 GuopengLin, (@t-glin)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_vpnsitelink_info
version_added: '1.5.0'
short_description: Get VpnSiteLink info
description:
    - Get info of Vpn Site Link relate infomation.
options:
    resource_group:
        description:
            - The resource group name of the VpnSite.
        required: true
        type: str
    vpn_site_name:
        description:
            - The name of the Vpn Site.
        required: true
        type: str
    name:
        description:
            - The name of the VpnSiteLink being retrieved.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Fred-Sun (@Fred-Sun)
    - Haiyuan Zhang (@haiyuazhang)

'''

EXAMPLES = '''
    - name: Get Vpn Site Link info by the name
      azure_rm_vpnsitelink_info:
        resource_group: myResourceGroup
        name: vpnSiteLink1
        vpn_site_name: vpnSite1


    - name: Get Vpn Site Links by the Vpn Site
      azure_rm_vpnsitelink_info:
        resource_group: myResourceGroup
        vpn_site_name: vpnSite1
'''

RETURN = '''
vpn_site_links:
    description:
        - A list of dict results where the key is the name of the VpnSiteLink and the values are the facts for that VpnSiteLink.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/vpnSites/fred/vpnSiteLinks/azureuser
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: 1ec5c61b-d66f-4b1c-b7b5-f27d0a9ad9d3
        name:
            description:
                - The name of the resource that is unique within a resource group.
                - This name can be used to access the resource.
            returned: always
            type: str
            sample: azureuser
        type:
            description:
                - Resource type.
            returned: always
            type: str
            sample: Microsoft.Network/vpnSites/vpnSiteLinks
        link_properties:
            description:
                - The link provider properties.
            returned: always
            type: complex
            contains:
                link_provider_name:
                    description:
                        - Name of the link provider.
                    returned: always
                    type: str
                    sample: azureuser
                link_speed_in_mbps:
                    description:
                        - Link speed.
                    returned: always
                    type: int
                    sample: 100
        ip_address:
            description:
                - The ip-address for the vpn-site-link.
            returned: always
            type: str
            sample: 192.168.33.223
        provisioning_state:
            description:
                - The provisioning state of the VPN site link resource.
            returned: always
            type: str
            sample: Succeeded
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase
try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVpnSiteLinkInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            vpn_site_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            )
        )

        self.resource_group = None
        self.vpn_site_name = None
        name = None

        self.results = dict(changed=False)
        self.state = None

        super(AzureRMVpnSiteLinkInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if (self.resource_group is not None and self.vpn_site_name is not None and self.name is not None):
            self.results['vpn_site_links'] = self.format_item(self.get())
        elif (self.resource_group is not None and self.vpn_site_name is not None):
            self.results['vpn_site_links'] = self.format_item(self.list_by_vpn_site())
        return self.results

    def get(self):
        response = None

        try:
            response = self.network_client.vpn_site_links.get(resource_group_name=self.resource_group,
                                                              vpn_site_name=self.vpn_site_name,
                                                              vpn_site_link_name=self.name)
        except ResourceNotFoundError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list_by_vpn_site(self):
        response = None

        try:
            response = self.network_client.vpn_site_links.list_by_vpn_site(resource_group_name=self.resource_group,
                                                                           vpn_site_name=self.vpn_site_name)
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
    AzureRMVpnSiteLinkInfo()


if __name__ == '__main__':
    main()
