#!/usr/bin/python
#
# Copyright (c) 2020 Suyeb Ansari (@suyeb786), Pallavi Chaudhari(@PallaviC2510)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = \
    '''
---
module: azure_rm_backupazurevm
version_added: '1.1.0'
short_description: Back up an Azure Virtual Machine using Azure Backup
description:
    - Back up an Azure VM using Azure Backup.
    - Enabling/Updating protection for the Azure VM.
    - Trigger an on-demand backup for a protected Azure VM.
    - Stop protection but retain existing data.
    - Stop protection and delete data.
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
    backup_policy_id:
        description:
            - Backup Policy ID present under Recovery Service Vault mentioned in recovery_vault_name field.
        required: true
        type: str
    state:
        description:
            - Assert the state of the protection item.
            - Use C(create) for enabling protection for the Azure VM.
            - Use C(update) for changing the policy of protection.
            - Use C(stop) for stop protection but retain existing data.
            - Use C(delete) for stop protection and delete data.
            - Use C(backup) for on-demand backup.
        default: create
        type: str
        choices:
            - create
            - update
            - delete
            - stop
            - backup
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Suyeb Ansari (@suyeb786)
    - Pallavi Chaudhari (@PallaviC2510)

'''

EXAMPLES = \
    '''
    - name: Enabling/Updating protection for the Azure VM
      azure_rm_backupazurevm:
        resource_group: 'myResourceGroup'
        recovery_vault_name: 'testVault'
        resource_id: '/subscriptions/00000000-0000-0000-0000-000000000000/ \
        resourceGroups/myResourceGroup/providers/Microsoft.Compute/virtualMachines/testVM'
        backup_policy_id: '/subscriptions/00000000-0000-0000-0000-000000000000/ \
        resourceGroups/myResourceGroup/providers/microsoft.recoveryservices/vaults/testVault/backupPolicies/ProdPolicy'
        state: 'create'
    - name: Stop protection but retain existing data
      azure_rm_backupazurevm:
        resource_group: 'myResourceGroup'
        recovery_vault_name: 'testVault'
        resource_id: '/subscriptions/00000000-0000-0000-0000-000000000000/ \
        resourceGroups/myResourceGroup/providers/Microsoft.Compute/virtualMachines/testVM'
        state: 'stop'
    - name: Stop protection and delete data
      azure_rm_backupazurevm:
        resource_group: 'myResourceGroup'
        recovery_vault_name: 'testVault'
        resource_id: '/subscriptions/00000000-0000-0000-0000-000000000000/ \
        resourceGroups/myResourceGroup/providers/Microsoft.Compute/virtualMachines/testVM'
        state: 'delete'
    - name: Trigger an on-demand backup for a protected Azure VM
      azure_rm_backupazurevm:
        resource_group: 'myResourceGroup'
        recovery_vault_name: 'testVault'
        resource_id: '/subscriptions/00000000-0000-0000-0000-000000000000/ \
        resourceGroups/myResourceGroup/providers/Microsoft.Compute/virtualMachines/testVM'
        backup_policy_id: '/subscriptions/00000000-0000-0000-0000-000000000000/ \
        resourceGroups/myResourceGroup/providers/microsoft.recoveryservices/vaults/testVault/backupPolicies/ProdPolicy'
        state: 'backup'
    '''

RETURN = \
    '''
id:
    description:
        - VM backup protection details.
    returned: always
    type: str
    sample: '{"response":{"id":"protection_id","name":"protection_item_name","properties":{}}}'
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


class Actions:
    (NoAction, Create, Update, Delete) = range(4)


class BackupAzureVM(AzureRMModuleBaseExt):
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
            ),
            backup_policy_id=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='create',
                choices=['create', 'update', 'delete', 'stop', 'backup']
            )
        )

        self.resource_group = None
        self.recovery_vault_name = None
        self.resource_id = None
        self.backup_policy_id = None
        self.state = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.url = None
        self.status_code = [200, 201, 202, 204]
        self.to_do = Actions.NoAction

        self.body = {}
        self.query_parameters = {}
        self.query_parameters['api-version'] = None
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(BackupAzureVM, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=True)

    def get_api_version(self):
        return '2019-05-13' if self.state == 'create' or self.state == 'update' or self.state == 'delete' or self.state == 'stop' else '2016-12-01'

    def get_url(self):
        if self.state == 'create' or self.state == 'update' or self.state == 'delete' or self.state == 'stop':
            return '/subscriptions' + '/' + self.subscription_id \
                   + '/resourceGroups' + '/' + self.resource_group + '/providers' \
                   + '/Microsoft.RecoveryServices' + '/vaults' + '/' \
                   + self.recovery_vault_name \
                   + '/backupFabrics/Azure/protectionContainers/' \
                   + 'iaasvmcontainer;iaasvmcontainerv2;' + self.parse_resource_to_dict(self.resource_id)['resource_group']\
                   + ';' + self.parse_resource_to_dict(self.resource_id)['name'] + '/protectedItems/' \
                   + 'vm;iaasvmcontainerv2;' + self.parse_resource_to_dict(self.resource_id)['resource_group'] + ';' \
                   + self.parse_resource_to_dict(self.resource_id)['name']
        if self.state == 'backup':
            return '/subscriptions' + '/' + self.subscription_id \
                   + '/resourceGroups' + '/' + self.resource_group + '/providers' \
                   + '/Microsoft.RecoveryServices' + '/vaults' + '/' \
                   + self.recovery_vault_name \
                   + '/backupFabrics/Azure/protectionContainers/' \
                   + 'iaasvmcontainer;iaasvmcontainerv2;' + self.parse_resource_to_dict(self.resource_id)['resource_group'] \
                   + ';' + self.parse_resource_to_dict(self.resource_id)['name'] + '/protectedItems/' \
                   + 'vm;iaasvmcontainerv2;' + self.parse_resource_to_dict(self.resource_id)['resource_group'] + ';' \
                   + self.parse_resource_to_dict(self.resource_id)['name'] + '/backup'

    def get_body(self):
        if self.state == 'create' or self.state == 'update':
            return {
                'properties':
                    {
                        'protectedItemType': 'Microsoft.Compute/virtualMachines',
                        'sourceResourceId': self.resource_id,
                        'policyId': self.backup_policy_id
                    }
            }
        elif self.state == 'backup':
            return {
                "properties": {
                    "objectType": "IaasVMBackupRequest",
                    "recoveryPointExpiryTimeInUTC": ""
                }
            }
        elif self.state == 'stop':
            return {
                "properties": {
                    "protectedItemType": "Microsoft.Compute/virtualMachines",
                    "sourceResourceId": self.resource_id,
                    "protectionState": "ProtectionStopped"
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
        if self.state == 'create' or self.state == 'update':
            changed = True
            response = self.enable_update_protection_for_azure_vm()
        if self.state == 'delete':
            changed = True
            response = self.stop_protection_and_delete_data()
        if self.state == 'stop':
            changed = True
            response = self.stop_protection_but_retain_existing_data()
        if self.state == 'backup':
            changed = True
            response = self.trigger_on_demand_backup()
        self.results['response'] = response
        self.results['changed'] = changed

        return self.results

    def enable_update_protection_for_azure_vm(self):

        # self.log('Enabling/Updating protection for the Azure Virtual Machine {0}'.format(self.))

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
            self.log('Error in enabling/updating protection for Azure VM.')
            self.fail(
                'Error in creating/updating protection for Azure VM {0}'.format(str(e)))

        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}

        return response

    def stop_protection_but_retain_existing_data(self):

        # self.log('Stop protection and retain existing data{0}'.format(self.))

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
            self.log('Error attempting to stop protection.')
            self.fail('Error in disabling the protection: {0}'.format(str(e)))

        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}

        return response

    def stop_protection_and_delete_data(self):

        # self.log('Stop protection and delete data{0}'.format(self.))

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
            self.log('Error attempting to delete backup.')
            self.fail('Error deleting the azure backup: {0}'.format(str(e)))

        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}

        return response

    def trigger_on_demand_backup(self):

        # self.log('Trigger an on-demand backup for a protected Azure VM{0}'.format(self.))

        try:
            response = self.mgmt_client.query(
                self.url,
                'POST',
                self.query_parameters,
                self.header_parameters,
                self.body,
                self.status_code,
                600,
                30,
            )
        except CloudError as e:
            self.log('Error attempting to backup azure vm.')
            self.fail(
                'Error while taking on-demand backup: {0}'.format(str(e)))

        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}

        return response


def main():
    BackupAzureVM()


if __name__ == '__main__':
    main()
