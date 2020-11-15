#!/usr/bin/python
#
# Copyright (c) 2020 GuopengLin, (@t-glin)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_virtualwan_info
version_added: '2.0.0'
short_description: Get VirtualWan info
description:
    - Get info of VirtualWan.
options:
    resource_group_name:
        description:
            - The resource group name of the VirtualWan.
        type: str
    virtual_wan_name:
        description:
            - The name of the VirtualWAN being retrieved.
        type: str
extends_documentation_fragment:
    - azure
author:
    - GuopengLin (@t-glin)
    - Fred-Sun (@Fred-Sun)
    - Haiyuan Zhang (@haiyuazhang)
'''

EXAMPLES = '''
    - name: Get Virtual WAN by name
      azure_rm_virtualwan_info: 
        resource_group_name: "{{ resource_group_name }}"

    - name: List all Virtual WANLs by resource group
      azure_rm_virtualwan_info: 
        resource_group_name: "{{ resource_group_name }}"
        
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
            sample: /subscriptions/xxx-xxx/resourceGroups/resource_group/providers/Microsoft.Network/virtualWans/wan_name
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: myResourceGroup
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
            type: dictionary
            sample: { 'key1': 'value1'}
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample:  "W/\"86df6f3d-19f2-4cc8-8574-47921de4a6f1\""
        disable_vpn_encryption:
            description:
                - Vpn encryption to be disabled or not.
            returned: always
            type: bool
            sample: false
        vpn_sites:
            description:
                - List of VpnSites in the VirtualWAN.
            returned: always
            type: complex
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: /subscriptions/xxx-xxx/resourceGroups/resource_group/providers/Microsoft.Network/vpnSites/test1
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
            sample: null
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
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVirtualWanInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group_name=dict(
                type='str'
            ),
            virtual_wan_name=dict(
                type='str'
            )
        )

        self.resource_group_name = None
        self.virtual_wan_name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        super(AzureRMVirtualWanInfo, self).__init__(self.module_arg_spec, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2020-04-01')

        if (self.resource_group_name is not None and
            self.virtual_wan_name is not None):
            self.results['virtual_wans'] = self.format_item(self.get())
        elif (self.resource_group_name is not None):
            self.results['virtual_wans'] = self.format_item(self.list_by_resource_group())
        else:
            self.results['virtual_wans'] = self.format_item(self.list())
        return self.results

    def get(self):
        response = None

        try:
            response = self.mgmt_client.virtual_wans.get(resource_group_name=self.resource_group_name,
                                                         virtual_wan_name=self.virtual_wan_name)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list_by_resource_group(self):
        response = None

        try:
            response = self.mgmt_client.virtual_wans.list_by_resource_group(resource_group_name=self.resource_group_name)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list(self):
        response = None

        try:
            response = self.mgmt_client.virtual_wans.list()
        except CloudError as e:
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
