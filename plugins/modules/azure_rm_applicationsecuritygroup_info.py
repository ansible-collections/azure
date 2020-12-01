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
module: azure_rm_applicationsecuritygroup_info
version_added: '2.9'
short_description: Get ApplicationSecurityGroup info
description:
    - Get info of ApplicationSecurityGroup.
options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
    name:
        description:
            - The name of the application security group.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - GuopengLin (@t-glin)
    - Fred-Sun (@Fred-Sun)
    - Haiyuan Zhang (@haiyuazhang)

'''

EXAMPLES = '''
    - name: Get application security group by name
      azure_rm_applicationsecuritygroup_info: 
        name: testgroup
        resource_group: myResourceGroup

    - name: List all application security groups by subscription
      azure_rm_applicationsecuritygroup_info: 

    - name: List all application security groups by ressource group
      azure_rm_applicationsecuritygroup_info: 
        resource_group: myResourceGroup
        

'''

RETURN = '''
application_security_groups:
    description:
        - A list of dict results where the key is the name of the ApplicationSecurityGroup and the values are the facts for that ApplicationSecurityGroup.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/v-xisuRG/providers/Microsoft.Network/applicationSecurityGroups/v-xisuRGname
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: Fred01
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
            sample: “{{'key1':'value1'}}”
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: ad671408-bc59-4880-8a64-523e01d1f26b
        provisioning_state:
            description:
                - The provisioning state of the application security group resource.
            returned: always
            type: str
            sample: Succeeded
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


class AzureRMApplicationSecurityGroupInfo(AzureRMModuleBase):
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
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        self.mgmt_client = None
        super(AzureRMApplicationSecurityGroupInfo, self).__init__(self.module_arg_spec, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2020-04-01')

        if (self.resource_group is not None and self.name is not None):
            self.results['application_security_groups'] = self.format_item(self.get())
        elif (self.resource_group is not None):
            self.results['application_security_groups'] = self.format_item(self.list())
        else:
            self.results['application_security_groups'] = self.format_item(self.list_all())
        return self.results

    def get(self):
        response = None

        try:
            response = self.mgmt_client.application_security_groups.get(resource_group_name=self.resource_group,
                                                                        application_security_group_name=self.name)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list(self):
        response = None

        try:
            response = self.mgmt_client.application_security_groups.list(resource_group_name=self.resource_group)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list_all(self):
        response = None

        try:
            response = self.mgmt_client.application_security_groups.list_all()
        except CloudError as e:
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
    AzureRMApplicationSecurityGroupInfo()


if __name__ == '__main__':
    main()
