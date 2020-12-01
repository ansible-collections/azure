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
module: azure_rm_applicationsecuritygroup
version_added: '2.9'
short_description: Manage Azure ApplicationSecurityGroup instance
description:
    - Create, update and delete instance of Azure ApplicationSecurityGroup.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    locaion:
        description:
            - The location of the application security group.
        type: str
    name:
        description:
            - The name of the application security group.
        required: true
        type: str
    state:
        description:
            - Assert the state of the ApplicationSecurityGroup.
            - Use C(present) to create or update an ApplicationSecurityGroup and C(absent) to delete it.
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
    - name: Delete application security group
      azure_rm_applicationsecuritygroup: 
        application_security_group_name: test-asg
        resource_group_name: rg1
        

    - name: Create application security group
      azure_rm_applicationsecuritygroup: 
        application_security_group_name: test-asg
        resource_group_name: rg1
        location: westus
        properties: {}
        

'''

RETURN = '''
state:
    description:
        - Current state of the storage account
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/applicationSecurityGroups/fred03
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: fred03
        type:
            description:
                - Resource type.
            returned: always
            type: str
            sample: Microsoft.Network/applicationSecurityGroups
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
            sample: {'key1':'value1'}
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: 25e03ada-e3d1-4129-bfbe-f7f1cb69ac60
        provisioning_state:
            description:
                - The provisioning state of the application security group resource.
            returned: always
            type: str
            sample: Succeeded

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


class AzureRMApplicationSecurityGroup(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
            ),
            name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.body = {}

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApplicationSecurityGroup, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                              supports_check_mode=True,
                                                              supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]
        
        resource_group = self.get_resource_group(self.resource_group)
        if 'location' not in self.body.keys():
            # Set default location
            self.body['location'] = resource_group.location

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
                if not self.default_compare(modifiers, self.body, old_response, '', self.results):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.create_update_resource()
            self.results['state'] = response
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            self.delete_resource()
        else:
            self.results['changed'] = False
            response = old_response
            self.results['state'] = response

        return self.results

    def create_update_resource(self):
        try:
            response = self.mgmt_client.application_security_groups.create_or_update(resource_group_name=self.resource_group,
                                                                                     application_security_group_name=self.name,
                                                                                     parameters=self.body)
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the ApplicationSecurityGroup instance.')
            self.fail('Error creating the ApplicationSecurityGroup instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.mgmt_client.application_security_groups.delete(resource_group_name=self.resource_group,
                                                                           application_security_group_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the ApplicationSecurityGroup instance.')
            self.fail('Error deleting the ApplicationSecurityGroup instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.mgmt_client.application_security_groups.get(resource_group_name=self.resource_group,
                                                                        application_security_group_name=self.name)
        except CloudError as e:
            return False
        return response.as_dict()


def main():
    AzureRMApplicationSecurityGroup()


if __name__ == '__main__':
    main()
