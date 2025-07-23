#!/usr/bin/python
#
# Copyright (c) 2020 Fred-Sun, (@Fred-Sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_virtualwan
version_added: '1.5.0'
short_description: Manage Azure VirtualWan instance
description:
    - Create, update and delete instance of Azure VirtualWan.
options:
    resource_group:
        description:
            - The resource group name of the VirtualWan.
        required: true
        type: str
    office365_local_breakout_category:
        description:
            - Specifies the Office365 local breakout category.
            - Default value is C(None).
        type: str
        choices:
            - Optimize
            - OptimizeAndAllow
            - All
            - None
    name:
        description:
            - The name of the VirtualWAN being retrieved.
        required: true
        type: str
    location:
        description:
            - The virtual wan location.
        type: str
    disable_vpn_encryption:
        description:
            - Vpn encryption to be disabled or not.
        type: bool
    virtual_hubs:
        description:
            - List of VirtualHubs in the VirtualWAN.
        type: list
        elements: dict
        suboptions:
            id:
                description:
                    - The virtual hub resource ID.
                type: str
    vpn_sites:
        description:
            - List of VpnSites in the VirtualWAN.
        type: list
        elements: dict
        suboptions:
            id:
                description:
                    - The vpn site resource ID.
                type: str
    allow_branch_to_branch_traffic:
        description:
            - True if branch to branch traffic is allowed.
        type: bool
    allow_vnet_to_vnet_traffic:
        description:
            - C(True) if Vnet to Vnet traffic is allowed.
        type: bool
    virtual_wan_type:
        description:
            - The type of the VirtualWAN.
        type: str
        choices:
            - Basic
            - Standard
    state:
        description:
            - Assert the state of the VirtualWan.
            - Use C(present) to create or update an VirtualWan and C(absent) to delete it.
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
- name: Create a VirtualWan
  azure_rm_virtualwan:
    resource_group: myResouceGroup
    name: testwan
    disable_vpn_encryption: true
    allow_branch_to_branch_traffic: true
    allow_vnet_to_vnet_traffic: true
    virtual_wan_type: Standard

- name: Delete the VirtualWan
  azure_rm_virtualwan:
    resource_group: myResouceGroup
    name: testwan
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the virtual wan.
    type: complex
    returned: success
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualWans/virtual_wan_name
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: virtualwanb57dc9555691
        type:
            description:
                - Resource type.
            returned: always
            type: str
            sample: Microsoft.Network/virtualWans
        location:
            description:
                - The virtual wan resource location.
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
            sample: 52def36b-84b6-49aa-a825-16ba167fc559
        disable_vpn_encryption:
            description:
                - Vpn encryption to be disabled or not.
            returned: always
            type: bool
            sample: true
        virtual_hubs:
            description:
                - List of VirtualHubs in the VirtualWAN.
            type: complex
            returned: always
            contains:
                id:
                    description:
                        - The virtual hubs ID.
                    type: str
                    returned: always
                    sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualHubs/test
        vpn_sites:
            description:
                - List of VpnSites in the VirtualWAN.
            returned: always
            type: list
            contains:
                id:
                    description:
                        - The vpn sites resouce ID.
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
            sample: true
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
                - The type of the VirtualWAN.
            returned: always
            type: str
            sample: Standard

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Update_tags, Delete = range(5)


class AzureRMVirtualWan(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            location=dict(
                type='str'
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            office365_local_breakout_category=dict(
                type='str',
                choices=['Optimize', 'OptimizeAndAllow', 'All', 'None']
            ),
            name=dict(
                type='str',
                required=True
            ),
            disable_vpn_encryption=dict(
                type='bool'
            ),
            virtual_hubs=dict(
                type='list',
                elements='dict',
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
            ),
            vpn_sites=dict(
                type='list',
                elements='dict',
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
            ),
            allow_branch_to_branch_traffic=dict(
                type='bool'
            ),
            allow_vnet_to_vnet_traffic=dict(
                type='bool'
            ),
            virtual_wan_type=dict(
                type='str',
                choices=['Basic', 'Standard']
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

        super(AzureRMVirtualWan, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

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
                compare_list = ['disable_vpn_encryption', 'allow_branch_to_branch_traffic']
                for key in compare_list:
                    if self.body.get(key) is not None and self.body[key] != old_response[key]:
                        self.log('parameter {0} does not match the configuration'.format(key))
                        self.to_do = Actions.Update
                    else:
                        self.body[key] = old_response[key]

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
            response = self.network_client.virtual_wans.update_tags(resource_group_name=self.resource_group,
                                                                    virtual_wan_name=self.name,
                                                                    wan_parameters=tags_parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.log('Error attempting to Update the VirtualWan instance.')
            self.fail('Error Updating the VirtualWan instance tags: {0}'.format(str(exc)))
        return response.as_dict()

    def create_update_resource(self):
        try:
            response = self.network_client.virtual_wans.begin_create_or_update(resource_group_name=self.resource_group,
                                                                               virtual_wan_name=self.name,
                                                                               wan_parameters=self.body)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.log('Error attempting to create the VirtualWan instance.')
            self.fail('Error creating the VirtualWan instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.network_client.virtual_wans.begin_delete(resource_group_name=self.resource_group,
                                                                     virtual_wan_name=self.name)
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except Exception as e:
            self.log('Error attempting to delete the VirtualWan instance.')
            self.fail('Error deleting the VirtualWan instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.network_client.virtual_wans.get(resource_group_name=self.resource_group,
                                                            virtual_wan_name=self.name)
        except ResourceNotFoundError as e:
            return False
        return response.as_dict()


def main():
    AzureRMVirtualWan()


if __name__ == '__main__':
    main()
