#!/usr/bin/python
#
# Copyright (c) 2020 Fred-Sun, (@Fred-Sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_virtualwan_info
version_added: '1.5.0'
short_description: Get VirtualWan info
description:
    - Get info of VirtualWan.
options:
    resource_group:
        description:
            - The resource group name of the VirtualWan.
        type: str
    name:
        description:
            - The name of the VirtualWAN being retrieved.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Fred-Sun (@Fred-Sun)
'''

EXAMPLES = '''
- name: Get Virtual WAN by name
  azure_rm_virtualwan_info:
    resource_group: myResouceGroup
    name: testwan

- name: List all Virtual WANLs by resource group
  azure_rm_virtualwan_info:
    resource_group: myResourceGroup

- name: List all Virtual WANs by subscription_id
  azure_rm_virtualwan_info:
'''

RETURN = '''
virtual_wans:
    description:
        - A list of dict results where the key is the name of the VirtualWan and the values are the facts for that VirtualWan.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualWans/testwan
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: testwan
        type:
            description:
                - Resource type.
            returned: always
            type: str
            sample: Microsoft.Network/virtualWans
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
            sample:  "86df6f3d-19f2-4cc8-8574-47921de4a6f1"
        disable_vpn_encryption:
            description:
                - Vpn encryption to be disabled or not.
            returned: always
            type: bool
            sample: false
        virtual_hubs:
            description:
                - List of VirtualHubs in the VirtualWAN.
            type: complex
            contains:
                id:
                    description:
                        - The virtual hubs list of the virtual wan.
                    returned: always
                    type: str
                    sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualHubs/test
        vpn_sites:
            description:
                - List of VpnSites in the VirtualWAN.
            returned: always
            type: complex
            contains:
                id:
                    description:
                        - The vpn site resource ID.
                    returned: always
                    type: str
                    sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/vpnSites/test1
        allow_branch_to_branch_traffic:
            description:
                - True if branch to branch traffic is allowed.
            returned: always
            type: bool
            sample: true
        allow_vnet_to_vnet_traffic:
            description:
                - True if Vnet to Vnet traffic is allowed.
            returned: always
            type: bool
            sample: True
        office365_local_breakout_category:
            description:
                - The office local breakout category.
            returned: always
            type: str
            sample: None
        provisioning_state:
            description:
                - The provisioning state of the virtual WAN resource.
            returned: always
            type: str
            sample: Succeeded
        virtual_wan_type:
            description:
                - The type of virtual wan.
            returned: always
            type: str
            sample: Standard
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase
try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVirtualWanInfo(AzureRMModuleBase):
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

        super(AzureRMVirtualWanInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if (self.resource_group is not None and self.name is not None):
            self.results['virtual_wans'] = self.format_item(self.get())
        elif (self.resource_group is not None):
            self.results['virtual_wans'] = self.format_item(self.list_by_resource_group())
        else:
            self.results['virtual_wans'] = self.format_item(self.list())
        return self.results

    def get(self):
        response = None

        try:
            response = self.network_client.virtual_wans.get(resource_group_name=self.resource_group,
                                                            virtual_wan_name=self.name)
        except ResourceNotFoundError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list_by_resource_group(self):
        response = None

        try:
            response = self.network_client.virtual_wans.list_by_resource_group(resource_group_name=self.resource_group)
        except ResourceNotFoundError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list(self):
        response = None

        try:
            response = self.network_client.virtual_wans.list()
        except ResourceNotFoundError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def format_item(self, item):
        if hasattr(item, 'as_dict'):
            return [item.as_dict()]
        else:
            result = []
            items = list(item)
            for tmp in items:
                result.append(tmp.as_dict())
            return result


def main():
    AzureRMVirtualWanInfo()


if __name__ == '__main__':
    main()
