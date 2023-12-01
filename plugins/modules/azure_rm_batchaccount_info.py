#!/usr/bin/python
#
# Copyright (c) 2023 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_batchaccount_info
version_added: "0.1.2"
short_description: Get the Batch Account on Azure facts
description:
    - Get the Batch Account on Azure facts.

options:
    resource_group:
        description:
            - The name of the resource group in which to create the Batch Account.
        type: str
    name:
        description:
            - The name of the Batch Account.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get the Batch Account by name
  azure_rm_batchaccount_info:
    resource_group: MyResGroup
    name: mybatchaccount

- name: List the Batch Account by subscription
  azure_rm_batchaccount_info:
    tags:
      - key1
'''

RETURN = '''
id:
    description:
        - The ID of the Batch account.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Batch/batchAccounts/sampleacct"
account_endpoint:
    description:
        - The account endpoint used to interact with the Batch service.
    returned: always
    type: str
    sample: sampleacct.westus.batch.azure.com
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.mgmt.batch import BatchManagementClient
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBatchAccountInfo(AzureRMModuleBaseExt):
    """Configuration class for an Azure RM Batch Account resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
            ),
            name=dict(
                type='str',
            ),
            tags=dict(
                type='list',
                elements='str'
            )
        )

        self.resource_group = None
        self.name = None
        self.tags = None

        self.results = dict(changed=False)
        self.mgmt_client = None

        super(AzureRMBatchAccountInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        response = []

        self.mgmt_client = self.get_mgmt_svc_client(BatchManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)
        if self.resource_group is not None and self.name is not None:
            response = [self.get_batchaccount()]
        elif self.resource_group is not None:
            response = self.list_by_resourcegroup()
        else:
            response = self.list_all()

        self.results['batch_account'] = [self.format_item(item) for item in response if item and self.has_tags(item.get('tags'), self.tags)]

        return self.results

    def list_by_resourcegroup(self):
        self.log("List all Batch Account in the rsource group {0}".format(self.resource_group))
        result = []
        response = []
        try:
            response = self.mgmt_client.batch_account.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.log('Did not find the Batch Account instance. Exception as {0}'.format(e))
        for item in response:
            result.append(item.as_dict())
        return result

    def list_all(self):
        self.log("List all Batch Account in the same subscritpion")
        result = []
        response = []
        try:
            response = self.mgmt_client.batch_account.list()
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.log('Did not find the Batch Account instance.')
        for item in response:
            result.append(item.as_dict())
        return result

    def get_batchaccount(self):
        '''
        Gets the properties of the specified Batch Account
        :return: deserialized Batch Account instance state dictionary
        '''
        self.log("Checking if the Batch Account instance {0} is present".format(self.name))
        try:
            response = self.mgmt_client.batch_account.get(resource_group_name=self.resource_group,
                                                          account_name=self.name)
            self.log("Response : {0}".format(response))
            self.log("Batch Account instance : {0} found".format(response.name))
        except ResourceNotFoundError as e:
            self.log('Did not find the Batch Account instance.')
            return
        return response.as_dict()

    def format_item(self, item):
        result = {
            'id': item['id'],
            'name': item['name'],
            'type': item['type'],
            'location': item['location'],
            'account_endpoint': item['account_endpoint'],
            'provisioning_state': item['provisioning_state'],
            'pool_allocation_mode': item['pool_allocation_mode'],
            'auto_storage': item['auto_storage'],
            'dedicated_core_quota': item['dedicated_core_quota'],
            'low_priority_core_quota': item['low_priority_core_quota'],
            'pool_quota': item['pool_quota'],
            'active_job_and_job_schedule_quota': item['active_job_and_job_schedule_quota'],
            'tags': item.get('tags')
        }
        return result


def main():
    """Main execution"""
    AzureRMBatchAccountInfo()


if __name__ == '__main__':
    main()
