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
module: azure_rm_virtualwan
version_added: '2.0.0'
short_description: Manage Azure VirtualWan instance
description:
    - Create, update and delete instance of Azure VirtualWan.
options:
    resource_group_name:
        description:
            - The resource group name of the VirtualWan.
        required: true
        type: str
    virtual_wan_name:
        description:
            - The name of the VirtualWAN being retrieved.
            - The name of the VirtualWAN being created or updated.
            - The name of the VirtualWAN being deleted.
        required: true
        type: str
    location:
        description:
            - The virtual wan location.
        type: str
        required: true
    disable_vpn_encryption:
        description:
            - Vpn encryption to be disabled or not.
        type: bool
    virtual_hubs:
        description:
            - List of VirtualHubs in the VirtualWAN.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
                type: str
    vpn_sites:
        description:
            - List of VpnSites in the VirtualWAN.
        type: list
        suboptions:
            id:
               description:
                   - Resource ID.
               type: str
    allow_branch_to_branch_traffic:
        description:
            - True if branch to branch traffic is allowed.
        type: bool
    allow_vnet_to_vnet_traffic:
        description:
            - True if Vnet to Vnet traffic is allowed.
        type: bool
    virtual_wan_type:
        description:
            - The type of the VirtualWAN.
        type: str
    state:
        description:
            - Assert the state of the VirtualWan.
            - Use C(present) to create or update an VirtualWan and C(absent) to delete it.
        default: present
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - GuopengLin (@t-glin)
    - Fred-Sun (@Fred-Sun)
    - Haiyuan Zhang (@haiyuazhang)

'''

EXAMPLES = '''
 - name: Create a VirtualWan
   azure_rm_virtualwan:
     resource_group_name: "{{ resource_group }}"
     virtual_wan_name: "{{ virtual_wan_name }}"
     location: eastus
     disable_vpn_encryption: true
     allow_branch_to_branch_traffic: true
     allow_vnet_to_vnet_traffic: true
     virtual_wan_type: Standard

 - name: Delete the VirtualWan
   azure_rm_virtualwan:
     resource_group_name: "{{ resource_group }}"
     virtual_wan_name: "{{ virtual_wan_name }}"
     location: eastus
     state: absent

'''

RETURN = '''
id:
  description:
    - Resource ID.
  returned: always
  type: str
  sample: null
name:
  description:
    - Resource name.
  returned: always
  type: str
  sample: null
type:
  description:
    - Resource type.
  returned: always
  type: str
  sample: null
location:
  description:
    - Resource location.
  returned: always
  type: str
  sample: null
tags:
  description:
    - Resource tags.
  returned: always
  type: dict
  sample: null
etag:
  description:
    - A unique read-only string that changes whenever the resource is updated.
  returned: always
  type: str
  sample: null
disable_vpn_encryption:
  description:
    - Vpn encryption to be disabled or not.
  returned: always
  type: bool
  sample: null
virtual_hubs:
  description:
    - List of VirtualHubs in the VirtualWAN.
  returned: always
  type: list
  sample: null
  contains:
    id:
      description:
        - Resource ID.
      returned: always
      type: str
      sample: null
vpn_sites:
  description:
    - List of VpnSites in the VirtualWAN.
  returned: always
  type: list
  sample: null
  contains:
    id:
      description:
        - Resource ID.
      returned: always
      type: str
      sample: null
allow_branch_to_branch_traffic:
  description:
    - True if branch to branch traffic is allowed.
  returned: always
  type: bool
  sample: null
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
  sample: null
provisioning_state:
  description:
    - The provisioning state of the virtual WAN resource.
  returned: always
  type: str
  sample: null
virtual_wan_type:
  description:
    - The type of the VirtualWAN.
  returned: always
  type: str
  sample: null

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMVirtualWan(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            location=dict(
                type='str',
                required=True
            ),
            resource_group_name=dict(
                type='str',
                required=True
            ),
            virtual_wan_name=dict(
                type='str',
                required=True
            ),
            disable_vpn_encryption=dict(
                type='bool',
                disposition='/disable_vpn_encryption'
            ),
            virtual_hubs=dict(
                type='list',
                updatable=False,
                disposition='/virtual_hubs',
                options=dict(
                    id=dict(
                        type='str',
                        disposition='id'
                    )
                )
            ),
            vpn_sites=dict(
                type='list',
                updatable=False,
                disposition='/vpn_sites',
                options=dict(
                    id=dict(
                        type='str',
                        disposition='id'
                    )
                )
            ),
            allow_branch_to_branch_traffic=dict(
                type='bool',
                disposition='/allow_branch_to_branch_traffic'
            ),
            allow_vnet_to_vnet_traffic=dict(
                type='bool',
                disposition='/allow_vnet_to_vnet_traffic'
            ),
            virtual_wan_type=dict(
                type='str',
                disposition='/virtual_wan_type'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group_name = None
        self.virtual_wan_name = None
        self.body = {}

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualWan, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_parameters(self.module_arg_spec, self.body, 0)

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2020-04-01')

        old_response = self.get_resource()

        if not old_response:
            if self.state == 'present':
                self.to_do = Actions.Create
        else:
            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                modifiers = {}
                self.create_compare_modifiers(self.module_arg_spec, '', modifiers)
                self.results['modifiers'] = modifiers
                self.results['compare'] = []
                allo_vnet_to_vnet_traffic = self.body.get('allow_vnet_to_vnet_traffic', None)
                if allo_vnet_to_vnet_traffic is not None:
                    del self.body['allow_vnet_to_vnet_traffic']
                if not self.default_compare(modifiers, self.body, old_response, '', self.results):
                    self.to_do = Actions.Update
                if allo_vnet_to_vnet_traffic is not None:
                    self.body['allow_vnet_to_vnet_traffic'] = allo_vnet_to_vnet_traffic

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.create_update_resource()
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            self.delete_resource()
        else:
            self.results['changed'] = False
            response = old_response

        return self.results

    def create_update_resource(self):
        try:
            response = self.mgmt_client.virtual_wans.create_or_update(resource_group_name=self.resource_group_name,
                                                                      virtual_wan_name=self.virtual_wan_name,
                                                                      wan_parameters=self.body)
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the VirtualWan instance.')
            self.fail('Error creating the VirtualWan instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.mgmt_client.virtual_wans.delete(resource_group_name=self.resource_group_name,
                                                            virtual_wan_name=self.virtual_wan_name)
        except CloudError as e:
            self.log('Error attempting to delete the VirtualWan instance.')
            self.fail('Error deleting the VirtualWan instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.mgmt_client.virtual_wans.get(resource_group_name=self.resource_group_name,
                                                         virtual_wan_name=self.virtual_wan_name)
        except CloudError as e:
            return False
        return response.as_dict()


def main():
    AzureRMVirtualWan()


if __name__ == '__main__':
    main()
