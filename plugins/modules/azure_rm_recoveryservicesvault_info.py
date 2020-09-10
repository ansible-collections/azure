#!/usr/bin/python
#
# Copyright (c) 2020 Suyeb Ansari (@suyeb786)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = \
    '''
---
module: azure_rm_recoveryservicesvault_info
version_added: '1.1.0'
short_description: Get Azure Recovery Services vault Details
description:
    - Get Azure Recovery Services vault Details.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - The name of the Azure Recovery Service Vault.
        required: true
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Suyeb Ansari ( @suyeb786 )
'''

EXAMPLES = '''
    - name: Get Azure Recovery Services Vault Details.
      azure_rm_recoveryservicesvault_info:
        resource_group: 'myResourceGroup'
        name: 'testVault'
'''

RETURN = '''
id:
    description:
        - Azure Recovery Service Vault Details.
    returned: always
    type: str
    sample: '{"response":{"location":"resource_location","name":"recovery_vault_name","properties":{},"id":"vault_id"}}'
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
import re
import json
import time
try:
    from msrestazure.azure_exceptions import CloudError
except ImportError:
    # This is handled in azure_rm_common
    pass

class azure_rm_recoveryservicesvault_info(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            )
        )

        self.resource_group = None
        self.name = None

        self.body = {}
        self.results = dict(changed=False)
        self.mgmt_client = None
        self.url = None
        self.status_code = [200, 201, 202, 204]

        self.query_parameters = {}
        self.query_parameters['api-version'] = None
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(azure_rm_recoveryservicesvault_info, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=True)

    def get_api_version(self):
        return '2016-06-01'

    def get_url(self):
        return '/subscriptions/' \
                + self.subscription_id \
                + '/resourceGroups/' \
                + self.resource_group \
                + '/providers/Microsoft.RecoveryServices' \
                + '/vaults' + '/' \
                + self.name

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_parameters(self.module_arg_spec, self.body, 0)

        self.query_parameters['api-version'] = self.get_api_version()
        self.url = self.get_url()
        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        changed = True
        response = self.get_recovery_service_vault_info()

        self.results['response'] = response
        self.results['changed'] = changed

        return self.results

    def get_recovery_service_vault_info(self):
        # self.log('Creating Recovery Service Vault Name {0}'.format(self.))
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
        except CloudError as e:
            self.log('Error in fetching Azure Recovery Service Vault Details.')
            self.fail('Error in fetching Azure Recovery Service Vault Details {0}'.format(str(e)))

        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}

        return response

def main():
    azure_rm_recoveryservicesvault_info()

if __name__ == '__main__':
    main()
