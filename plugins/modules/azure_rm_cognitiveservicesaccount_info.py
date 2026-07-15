#!/usr/bin/python
#
# Copyright (c) 2026 Microsoft
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_cognitiveservicesaccount_info
version_added: "3.21.0"
short_description: Get Azure Cognitive Services account information
description:
    - Retrieve information about Azure Cognitive Services accounts.
    - Can query a specific account, all accounts in a resource group, or all accounts in a subscription.
options:
    resource_group:
        description:
            - Name of the resource group.
            - Required when querying a specific account by name.
        type: str
    name:
        description:
            - Name of the Cognitive Services account.
            - When specified, returns information for this specific account.
        type: str
    show_keys:
        description:
            - Include API keys in the response.
            - Keys are sensitive - use C(no_log) on the task when retrieving keys.
        type: bool
        default: false

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get specific Cognitive Services account info
  azure.azcollection.azure_rm_cognitiveservicesaccount_info:
    resource_group: myResourceGroup
    name: mycontentsafety
  register: account_info

- name: Get account with API keys
  azure.azcollection.azure_rm_cognitiveservicesaccount_info:
    resource_group: myResourceGroup
    name: mycontentsafety
    show_keys: true
  register: account_with_keys
  no_log: true

- name: Use the endpoint
  debug:
    msg: "Endpoint: {{ account_info.accounts[0].endpoint }}"

- name: List all Cognitive Services accounts in resource group
  azure.azcollection.azure_rm_cognitiveservicesaccount_info:
    resource_group: myResourceGroup
  register: rg_accounts

- name: List all Cognitive Services accounts in subscription
  azure.azcollection.azure_rm_cognitiveservicesaccount_info:
  register: all_accounts
'''

RETURN = '''
accounts:
    description:
        - List of Cognitive Services accounts.
    returned: always
    type: list
    elements: dict
    sample: [
      {
          "etag": "\\"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\\"",
          "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-csa/providers/Microsoft.CognitiveServices/accounts/csexxxxxxxxxxxxxxx",
          "identity": {
              "principal_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
              "tenant_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
              "type": "SystemAssigned"
          },
          "kind": "ContentSafety",
          "location": "eastus",
          "name": "csexxxxxxxxxxxxxxx",
          "properties": {
              "allow_project_management": false,
              "call_rate_limit": {
                  "rules": [
                      {
                          "count": 10.0,
                          "dynamic_throttling_enabled": true,
                          "key": "ContentSafety.GPTFeature",
                          "match_patterns": [
                              {
                                  "method": "*",
                                  "path": "contentsafety/text:detectungroundedness*"
                              }
                          ],
                          "renewal_period": 10.0
                      },
                      {
                          "count": 5.0,
                          "key": "ContentSafety.All",
                          "match_patterns": [
                              {
                                  "method": "*",
                                  "path": "contentsafety/*"
                              }
                          ],
                          "renewal_period": 1.0
                      },
                      {
                          "count": 5.0,
                          "key": "default",
                          "match_patterns": [
                              {
                                  "method": "*",
                                  "path": "*"
                              }
                          ],
                          "renewal_period": 1.0
                      }
                  ]
              },
              "capabilities": [
                  {
                      "name": "VirtualNetworks"
                  },
                  {
                      "name": "EnabledApimVnet",
                      "value": "true"
                  },
                  {
                      "name": "Container",
                      "value": "ContentSafety.TextAnalyze,ContentSafety.ImageAnalyze,ContentSafety.Jailbreak,ContentSafety.jailbreakanalyze,ContentSafety.jailbreakanalyzenew"
                  }
              ],
              "date_created": "2026-06-24T18:41:21.7869275Z",
              "disable_local_auth": true,
              "endpoint": "https://csexxxxxxxxxxxxxxx-2b94a.cognitiveservices.azure.com/",
              "endpoints": {
                  "Container": "https://csexxxxxxxxxxxxxxx-2b94a.cognitiveservices.azure.com/",
                  "Content Safety": "https://csexxxxxxxxxxxxxxx-2b94a.cognitiveservices.azure.com/"
              },
              "internal_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
              "is_migrated": false,
              "private_endpoint_connections": [],
              "provisioning_state": "Succeeded",
              "public_network_access": "Enabled",
              "quota_limit": {
                  "rules": [
                      {
                          "count": 5000.0,
                          "key": "ContentSafety.All",
                          "match_patterns": [
                              {
                                  "method": "*",
                                  "path": "contentsafety/*"
                              }
                          ],
                          "renewal_period": 2592000.0
                      }
                  ]
              }
          },
          "sku": {
              "name": "F0"
          },
          "system_data": {
              "created_at": "2026-06-24T18:41:21.200238Z",
              "created_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
              "created_by_type": "Application",
              "last_modified_at": "2026-06-24T18:41:21.200238Z",
              "last_modified_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
              "last_modified_by_type": "Application"
          },
          "type": "Microsoft.CognitiveServices/accounts"
      }
    ]
'''  # NOQA

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMCognitiveServicesAccountInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            show_keys=dict(type='bool', default=False)
        )

        self.resource_group = None
        self.name = None
        self.show_keys = False

        self.results = dict(
            changed=False,
            accounts=[]
        )

        super(AzureRMCognitiveServicesAccountInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False
        )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        # Validate parameters
        if self.name and not self.resource_group:
            self.module.fail_json(msg="Parameter error: resource_group required when filtering by name")

        # Query accounts based on parameters
        if self.name:
            # Specific account
            results = self.get_account()
        elif self.resource_group:
            # All accounts in resource group
            results = self.list_by_resource_group()
        else:
            # All accounts in subscription
            results = self.list_all()

        self.results['accounts'] = results
        return self.results

    def get_account(self):
        """Get specific Cognitive Services account"""
        self.log('Getting Cognitive Services account {0}'.format(self.name))
        try:
            account_obj = self.cognitive_services_management_client.accounts.get(
                self.resource_group,
                self.name
            )
            account_dict = account_obj.as_dict()
            if self.show_keys:
                account_dict['auth_keys'] = self.get_keys(self.resource_group,
                                                          self.name)
            return [account_dict]
        except ResourceNotFoundError:
            self.log('Account {0} not found'.format(self.name))
            return []

    def list_by_resource_group(self):
        """List all Cognitive Services accounts in resource group"""
        self.log('Listing Cognitive Services accounts in resource group {0}'.format(self.resource_group))
        results = []
        try:
            accounts = self.cognitive_services_management_client.accounts.list_by_resource_group(
                self.resource_group
            )
            for account_obj in accounts:
                account_dict = account_obj.as_dict()
                if self.show_keys:
                    account_dict['auth_keys'] = self.get_keys(self.resource_group,
                                                              account_obj.name)
                results.append(account_dict)
        except Exception as exc:
            self.module.fail_json(msg='Error listing accounts: {0}'.format(str(exc)))
        return results

    def list_all(self):
        """List all Cognitive Services accounts in subscription"""
        self.log('Listing all Cognitive Services accounts in subscription')
        results = []
        try:
            accounts = self.cognitive_services_management_client.accounts.list()
            for account_obj in accounts:
                account_dict = account_obj.as_dict()
                if self.show_keys:
                    # Extract resource group from account ID
                    # Format: /subscriptions/{sub}/resourceGroups/{rg}/providers/...
                    id_parts = account_obj.id.split('/')
                    rg_index = id_parts.index('resourceGroups') + 1
                    account_dict['auth_keys'] = self.get_keys(id_parts[rg_index],
                                                              account_obj.name)
                results.append(account_dict)
        except Exception as exc:
            self.module.fail_json(msg='Error listing accounts: {0}'.format(str(exc)))
        return results

    def get_keys(self, resource_group, account_name):
        """Get API keys for the account"""
        try:
            keys_obj = self.cognitive_services_management_client.accounts.list_keys(
                resource_group,
                account_name
            )
            return {
                'key1': keys_obj.key1,
                'key2': keys_obj.key2
            }
        except Exception as exc:
            self.module.fail_json(msg='Error retrieving keys: {0}'.format(str(exc)))


def main():
    AzureRMCognitiveServicesAccountInfo()


if __name__ == '__main__':
    main()
