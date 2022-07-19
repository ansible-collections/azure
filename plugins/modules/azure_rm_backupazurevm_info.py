#!/usr/bin/python
#
# Copyright (c) 2020 Suyeb Ansari(@suyeb786), Pallavi Chaudhari(@PallaviC2510)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = \
    '''
---
module: azure_rm_backupazurevm_info
version_added: '1.1.0'
short_description: Back up an Azure Virtual Machine using Azure Backup Information
description:
    - Get Recovery point details for protected items.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    recovery_vault_name:
        description:
            - The name of the Azure Recovery Service Vault.
        required: true
        type: str
    resource_id:
        description:
            - Azure Virtual Machine Resource ID.
        required: true
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Suyeb Ansari (@suyeb786)
    - Pallavi Chaudhari (@PallaviC2510)

'''

EXAMPLES = \
    '''
    - name: Get Recovery Point Details
      azure_rm_backupazurevm_info:
        resource_group: 'myResourceGroup'
        recovery_vault_name: 'testVault'
        resource_id: '/subscriptions/00000000-0000-0000-0000-000000000000/ \
        resourceGroups/myResourceGroup/providers/Microsoft.Compute/virtualMachines/testVM'
    '''

RETURN = \
    '''
id:
    description:
        - VM Protection details.
    returned: always
    type: str
    sample: '{"response":{"id":"protection_id","name":"protection_item_name","properties":{}}}'
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
import re
import json
import time


class Actions:
    (NoAction, Create, Update, Delete) = range(4)


class BackupAzureVMInfo(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            recovery_vault_name=dict(
                type='str',
                required=True
            ),
            resource_id=dict(
                type='str',
                required=True
            )
        )

        self.resource_group = None
        self.recovery_vault_name = None
        self.resource_id = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.url = None
        self.status_code = [200, 201, 202, 204]
        self.to_do = Actions.NoAction

        self.body = {}
        self.query_parameters = {}
        self.query_parameters['api-version'] = '2019-05-13'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(BackupAzureVMInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def get_url(self):
        return '/subscriptions' + '/' + self.subscription_id \
               + '/resourceGroups' + '/' + self.resource_group + '/providers' \
               + '/Microsoft.RecoveryServices' + '/vaults' + '/' \
               + self.recovery_vault_name \
               + '/backupFabrics/Azure/protectionContainers/' \
               + 'iaasvmcontainer;iaasvmcontainerv2;' + self.parse_resource_to_dict(self.resource_id)['resource_group'] \
               + ';' + self.parse_resource_to_dict(self.resource_id)['name'] + '/protectedItems/' \
               + 'vm;iaasvmcontainerv2;' + self.parse_resource_to_dict(self.resource_id)['resource_group'] + ';' \
               + self.parse_resource_to_dict(self.resource_id)['name']

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_parameters(self.module_arg_spec, self.body, 0)
        self.url = self.get_url()

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        response = self.get_recovery_point_info()
        self.results['response'] = response
        return self.results

    def get_recovery_point_info(self):

        # self.log('Fetching protection details for the Azure Virtual Machine {0}'.format(self.))

        try:
            response = self.mgmt_client.query(
                self.url,
                'GET',
                self.query_parameters,
                self.header_parameters,
                None,
                self.status_code,
                600,
                30,
            )
        except Exception as e:
            self.log('Error in fetching recovery point.')
            self.fail('Error in fetching recovery point {0}'.format(str(e)))

        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}

        return response


def main():
    BackupAzureVMInfo()


if __name__ == '__main__':
    main()
