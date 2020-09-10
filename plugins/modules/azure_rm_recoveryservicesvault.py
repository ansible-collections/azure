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
module: azure_rm_recoveryservicesvault
version_added: '1.1.0'
short_description: Create and Update Azure Recovery Services vault
description:
    - Create Azure Recovery Services vault.
    - Update Azure Recovery Services vault.
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
    location:
        description:
            - Azure Resource location.
        required: true
        type: str
    enhanced_security_state:
        description:
            - Enhanced Security for backup configuration.
        default: Enabled
        type: str
        choices:
            - Enabled
            - Disabled
    soft_delete_feature_state:
        description:
            - Soft delete state for backup configuration.
        default: Enabled
        type: str
        choices:
            - Enabled
            - Disabled
    state:
        description:
            - Assert the state of the protection item.
            - Use C(present) for Creating Azure Recovery Service Vault.
            - Use C(update) for Updating Azure Recovery Service Vault backup configuration.
            - Use C(absent) for Deleting Azure Recovery Service Vault.
        default: create
        type: str
        choices:
            - present
            - update
            - absent
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Suyeb Ansari ( @suyeb786 )
'''

EXAMPLES = '''
    - name: Create/Update Azure Recovery Service vault
      azure_rm_recoveryservicesvault:
        resource_group: 'myResourceGroup'
        name: 'testVault'
        location: 'westeurope'
        state: 'present'
    - name: Update Azure Recovery Service vault backup configuration
      azure_rm_recoveryservicesvault:
        resource_group: 'myResourceGroup'
        name: 'testVault'
        location: 'westeurope'
        enhanced_security_state: 'Enabled'
        soft_delete_feature_state: "Disabled"
        state: 'update'
    - name: Delete Recovery Service Vault
      azure_rm_recoveryservicesvault:
        resource_group: 'myResourceGroup'
        name: 'testVault'
        location: 'westeurope'
        enhanced_security_state: 'Enabled'
        soft_delete_feature_state: "Disabled"
        state: 'absent'
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

class AzureRMRecoveryServicesVault(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
                required=True
            ),
            enhanced_security_state=dict(
                type='str',
                default='Disabled',
                choices=['Enabled', 'Disabled']
            ),
            soft_delete_feature_state=dict(
                type='str',
                default='Enabled',
                choices=['Enabled', 'Disabled']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent', 'update']
            )
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.enhanced_security_state = None
        self.soft_delete_feature_state = None
        self.state = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.url = None
        self.status_code = [200, 201, 202, 204]

        self.body = {}
        self.query_parameters = {}
        self.query_parameters['api-version'] = None
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(AzureRMRecoveryServicesVault, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=True)

    def get_api_version(self):
        return '2016-06-01' if self.state == 'present' or self.state == 'absent' else '2019-05-13'

    def get_url(self):
        if self.state == 'present' or self.state == 'absent':
            return '/subscriptions/' \
                   + self.subscription_id \
                   + '/resourceGroups/' \
                   + self.resource_group \
                   + '/providers/Microsoft.RecoveryServices' \
                   + '/vaults' + '/' \
                   + self.name
        if self.state == 'update':
            return '/subscriptions/' \
                   + self.subscription_id \
                   + '/resourceGroups/' \
                   + self.resource_group \
                   + '/providers/Microsoft.RecoveryServices' \
                   + '/vaults' + '/' \
                   + self.name \
                   + "/backupconfig/vaultconfig"

    def get_body(self):
        if self.state == 'present':
            return {
                "properties": {},
                "sku": {
                    "name": "Standard"  #The SKU is always "Standard".
                    },
                "location": self.location
            }
        elif self.state == 'update':
            return {
                "properties": {
                "enhancedSecurityState": self.enhanced_security_state,
                "softDeleteFeatureState": self.soft_delete_feature_state
                    }
                }
        else:
            return {}

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_parameters(self.module_arg_spec, self.body, 0)

        self.query_parameters['api-version'] = self.get_api_version()
        self.url = self.get_url()
        self.body = self.get_body()
        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        changed = False
        if self.state == 'present':
            changed = True
            response = self.create_recovery_service_vault()
        if self.state == 'update':
            changed = True
            response = self.update_recovery_service_vault()
        if self.state == 'absent':
            changed = True
            response = self.delete_recovery_service_vault()

        self.results['response'] = response
        self.results['changed'] = changed

        return self.results

    def create_recovery_service_vault(self):
        # self.log('Creating Recovery Service Vault Name {0}'.format(self.))
        try:
            response = self.mgmt_client.query(
                self.url,
                'PUT',
                self.query_parameters,
                self.header_parameters,
                self.body,
                self.status_code,
                600,
                30,
            )
        except CloudError as e:
            self.log('Error in creating Azure Recovery Service Vault.')
            self.fail('Error in creating Azure Recovery Service Vault {0}'.format(str(e)))

        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}

        return response

    def update_recovery_service_vault(self):
        # self.log('Updating Recovery Service Vault Name {0}'.format(self.))
        try:
            response = self.mgmt_client.query(
                self.url,
                'PATCH',
                self.query_parameters,
                self.header_parameters,
                self.body,
                self.status_code,
                600,
                30,
            )
        except CloudError as e:
            self.log('Error attempting to update Azure Recovery Service Vault.')
            self.fail('Error while updating Azure Recovery Service Vault: {0}'.format(str(e)))

        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}
        return response

    def delete_recovery_service_vault(self):
        # self.log('Deleting Recovery Service Vault {0}'.format(self.))
        try:
            response = self.mgmt_client.query(
                self.url,
                'DELETE',
                self.query_parameters,
                self.header_parameters,
                None,
                self.status_code,
                600,
                30,
            )
        except CloudError as e:
            self.log('Error attempting to delete Azure Recovery Service Vault.')
            self.fail('Error while deleting Azure Recovery Service Vault: {0}'.format(str(e)))

        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}
        return response

def main():
    AzureRMRecoveryServicesVault()

if __name__ == '__main__':
    main()
