#!/usr/bin/python
#
# Copyright (c) 2026 Microsoft
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_cognitiveservicesaccount
version_added: "3.20.0"
short_description: Manage Azure AI Cognitive Services accounts
description:
    - Create, update, or delete Azure AI Cognitive Services accounts.
options:
    resource_group:
        description:
            - Name of the resource group.
        required: true
        type: str
        aliases:
            - resource_group_name
    name:
        description:
            - Name of the Cognitive Services account.
            - Must be 2-64 characters, alphanumeric, hyphens, underscores.
            - Must be globally unique.
        required: true
        type: str
    kind:
        description:
            - The API name of cognitive services account.
        type: str
        choices:
            - AIServices
            - CognitiveServices
            - ComputerVision
            - ContentModerator
            - ContentSafety
            - ConversationalLanguageUnderstanding
            - CustomVision.Prediction
            - CustomVision.Training
            - Face
            - FormRecognizer
            - HealthInsights
            - ImmersiveReader
            - Internal.AllInOne
            - LUIS.Authoring
            - LanguageAuthoring
            - MetricsAdvisor
            - OpenAI
            - Personalizer
            - QnAMaker.v2
            - SpeechServices
            - TextAnalytics
            - TextTranslation
    state:
        description:
            - Assert the state of the account.
            - Use C(present) to create or update an account.
            - Use C(absent) to delete an account.
        default: present
        type: str
        choices:
            - present
            - absent
    location:
        description:
            - Valid Azure location.
            - Defaults to location of the resource group.
        type: str
    sku:
        description:
            - The SKU/pricing tier of the Cognitive Services account.
            - C(F0) is the free tier with rate limits.
            - C(S0) is the standard tier.
        default: F0
        type: str
        choices:
            - F0
            - S0
    custom_domain_name:
        description:
            - Optional custom subdomain name for token-based authentication.
        type: str
    public_network_access:
        description:
            - Whether public network access is allowed.
        default: Enabled
        type: str
        choices:
            - Enabled
            - Disabled
    disable_local_auth:
        description:
            - Disable key-based authentication, require Microsoft Entra ID.
        default: false
        type: bool
    network_acls:
        description:
            - Network firewall and virtual network rules.
        type: dict
        suboptions:
            default_action:
                description:
                    - Default firewall action.
                type: str
                choices:
                    - Allow
                    - Deny
                default: Allow
            ip_rules:
                description:
                    - List of allowed IP addresses or CIDR ranges.
                type: list
                elements: dict
                suboptions:
                    value:
                        description:
                            - IP address or CIDR range (e.g., '203.0.113.0/24').
                        type: str
                        required: true
            virtual_network_rules:
                description:
                    - List of allowed virtual network subnets.
                type: list
                elements: dict
                suboptions:
                    id:
                        description:
                            - Full resource ID of the subnet.
                        type: str
                        required: true
    identity:
        description:
            - Managed identity configuration.
        type: dict
        suboptions:
            type:
                description:
                    - Type of managed identity.
                type: str
                choices:
                    - None
                    - SystemAssigned
                    - UserAssigned
                    - SystemAssigned, UserAssigned
    purge:
        description:
            - When I(state) is C(absent) setting this to true
              will purge the account as well.
        type: bool
        default: false

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create Cognitive Services account with free tier
  azure.azcollection.azure_rm_cognitiveservicesaccount:
    resource_group: myResourceGroup
    name: mycontentsafety
    kind: ContentSafety
    location: eastus
    sku: F0
    tags:
      purpose: content-moderation

- name: Create Cognitive Services account with network security
  azure.azcollection.azure_rm_cognitiveservicesaccount:
    resource_group: myResourceGroup
    name: mycontentsafety-prod
    kind: ContentSafety
    sku: S0
    public_network_access: Disabled
    network_acls:
      default_action: Deny
      ip_rules:
        - value: "203.0.113.0/24"
    tags:
      environment: production

- name: Create Cognitive Services account with managed identity
  azure.azcollection.azure_rm_cognitiveservicesaccount:
    resource_group: myResourceGroup
    name: mycontentsafety-identity
    kind: ContentSafety
    identity:
      type: SystemAssigned
    disable_local_auth: true

- name: Update tags on existing account
  azure.azcollection.azure_rm_cognitiveservicesaccount:
    resource_group: myResourceGroup
    name: mycontentsafety
    kind: ContentSafety
    tags:
      environment: production

- name: Delete Cognitive Services account
  azure.azcollection.azure_rm_cognitiveservicesaccount:
    resource_group: myResourceGroup
    name: mycontentsafety
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the Cognitive Services account.
    returned: always
    type: dict
    sample: {
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
'''  # NOQA

import re

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMCognitiveServicesAccount(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str',
                                required=True,
                                aliases=['resource_group_name']),
            name=dict(type='str',
                      required=True
                      ),
            kind=dict(type='str',
                      choices=['AIServices',
                               'CognitiveServices',
                               'ComputerVision',
                               'ContentModerator',
                               'ContentSafety',
                               'ConversationalLanguageUnderstanding',
                               'CustomVision.Prediction',
                               'CustomVision.Training',
                               'Face',
                               'FormRecognizer',
                               'HealthInsights',
                               'ImmersiveReader',
                               'Internal.AllInOne',
                               'LUIS.Authoring',
                               'LanguageAuthoring',
                               'MetricsAdvisor',
                               'OpenAI',
                               'Personalizer',
                               'QnAMaker.v2',
                               'SpeechServices',
                               'TextAnalytics',
                               'TextTranslation']
                      ),
            state=dict(type='str',
                       default='present',
                       choices=['present', 'absent']),
            location=dict(type='str'),
            sku=dict(type='str',
                     default='F0',
                     choices=['F0', 'S0']),
            custom_domain_name=dict(type='str'),
            public_network_access=dict(type='str',
                                       default='Enabled',
                                       choices=['Enabled', 'Disabled']),
            disable_local_auth=dict(type='bool',
                                    default=False),
            purge=dict(type='bool',
                       default=False),
            network_acls=dict(
                type='dict',
                options=dict(
                    default_action=dict(type='str',
                                        default='Allow',
                                        choices=['Allow', 'Deny']),
                    ip_rules=dict(type='list',
                                  elements='dict',
                                  options=dict(value=dict(type='str',
                                                          required=True
                                                          )
                                               )
                                  ),
                    virtual_network_rules=dict(type='list',
                                               elements='dict',
                                               options=dict(id=dict(type='str',
                                                                    required=True
                                                                    )
                                                            )
                                               )
                )
            ),
            identity=dict(
                type='dict',
                options=dict(
                    type=dict(type='str',
                              choices=['None',
                                       'SystemAssigned',
                                       'UserAssigned',
                                       'SystemAssigned, UserAssigned']
                              )
                )
            ),
            tags=dict(type='dict')
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None
        self.sku = None
        self.custom_domain_name = None
        self.public_network_access = None
        self.disable_local_auth = None
        self.network_acls = None
        self.identity = None
        self.tags = None
        self.purge = None

        self.results = dict(changed=False,
                            compare=[])

        super(AzureRMCognitiveServicesAccount, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=True
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        # Validate account name
        if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_.-]*$', self.name):
            self.module.fail_json(msg="Account name must start with alphanumeric and contain only alphanumeric, hyphens, underscores, and dots")
        if len(self.name) < 2 or len(self.name) > 64:
            self.module.fail_json(msg="Account name must be between 2 and 64 characters")

        # Get resource group location if location not specified
        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        # Get existing account
        account = self.get_account()

        params = self.build_account_parameters()

        if self.state == 'present':
            if not account:
                if not self.kind:
                    self.module.fail_json(msg="kind must be specified when creating")
                # Create new account
                if not self.check_mode:
                    self.results['state'] = self.create_account(params)
                else:
                    self.results['state'] = dict()
                self.results['changed'] = True
            else:
                # Update existing account
                update_needed = self.check_update_needed(account, params)
                if update_needed:
                    if not self.check_mode:
                        self.results['state'] = self.update_account(account, params)
                    else:
                        self.results['state'] = account
                    self.results['changed'] = True
                else:
                    self.results['state'] = account
        else:  # state == 'absent'
            if account:
                if not self.check_mode:
                    self.delete_account()
                self.results['changed'] = True
                self.results['state'] = dict()
            else:
                self.results['state'] = dict()

        return self.results

    def get_account(self):
        """Get Cognitive Services account if it exists"""
        self.log('Getting Cognitive Services account {0}'.format(self.name))
        try:
            account_obj = self.cognitive_services_management_client.accounts.get(
                self.resource_group,
                self.name
            )
            return account_obj.as_dict()
        except ResourceNotFoundError:
            self.log('Account {0} not found'.format(self.name))
            return None

    def check_update_needed(self, account, params):
        """Check if account needs to be updated"""
        # Check immutable properties
        if account['location'].lower() != self.location.lower():
            self.module.fail_json(msg="Cannot change location of existing account")

        # Check SKU
        if self.sku and account['sku']['name'] != self.sku:
            # Only allow F0 -> S0 upgrade
            if not (account['sku']['name'] == 'F0' and self.sku == 'S0'):
                self.module.fail_json(msg="Cannot change SKU from {0} to {1}".format(account['sku']['name'], self.sku))
            return True

        # Check tags
        update_tags, dummy = self.update_tags(account.get('tags'))
        if update_tags:
            return True

        # Check identity
        if self.identity:
            account_identity_type = account.get('identity', {}).get('type', 'None')
            if account_identity_type != self.identity.get('type', 'None'):
                return True

        if not self.default_compare({},
                                    params,
                                    account,
                                    '',
                                    self.results):
            return True
        return False

    def build_account_parameters(self):
        """Build account parameters for create/update"""
        params = {}

        # Required fields
        params['location'] = self.location
        params['kind'] = self.kind
        params['sku'] = {'name': self.sku}

        # Properties
        properties = {}

        if self.custom_domain_name:
            properties['custom_sub_domain_name'] = self.custom_domain_name

        if self.public_network_access:
            properties['public_network_access'] = self.public_network_access

        if self.disable_local_auth is not None:
            properties['disable_local_auth'] = self.disable_local_auth

        # Network ACLs
        if self.network_acls:
            network_rule_set = {}

            if 'default_action' in self.network_acls:
                network_rule_set['default_action'] = self.network_acls['default_action']

            if 'ip_rules' in self.network_acls and self.network_acls['ip_rules']:
                network_rule_set['ip_rules'] = [
                    {'value': rule['value']} for rule in self.network_acls['ip_rules']
                ]

            if 'virtual_network_rules' in self.network_acls and self.network_acls['virtual_network_rules']:
                network_rule_set['virtual_network_rules'] = [
                    {'id': rule['id']} for rule in self.network_acls['virtual_network_rules']
                ]

            properties['network_acls'] = network_rule_set

        if properties:
            params['properties'] = properties

        # Identity
        if self.identity and self.identity.get('type'):
            params['identity'] = {
                'type': self.identity['type']
            }

        # Tags
        params['tags'] = self.tags

        return params

    def create_account(self, params):
        """Create a new Cognitive Services account"""
        self.log('Creating Cognitive Services account {0}'.format(self.name))

        try:
            poller = self.cognitive_services_management_client.accounts.begin_create(
                self.resource_group,
                self.name,
                params
            )
            account_obj = self.get_poller_result(poller)
            return account_obj.as_dict()
        except Exception as exc:
            self.module.fail_json(msg="Failed to create Cognitive Services account: {0}".format(str(exc)))

    def update_account(self, current_account, params):
        """Update existing Cognitive Services account"""
        self.log('Updating Cognitive Services account {0}'.format(self.name))

        # Preserve immutable fields from current account
        params['kind'] = current_account['kind']

        # Update SKU if specified and different
        if self.sku and current_account['sku'] != self.sku:
            params['sku'] = {'name': self.sku}
        else:
            params['sku'] = {'name': current_account['sku']}

        # Handle tags
        update_tags, new_tags = self.update_tags(current_account.get('tags'))
        params['tags'] = new_tags

        try:
            poller = self.cognitive_services_management_client.accounts.begin_update(
                self.resource_group,
                self.name,
                params
            )
            account_obj = self.get_poller_result(poller)
            return account_obj.as_dict()
        except Exception as exc:
            self.module.fail_json(msg="Failed to update Cognitive Services account: {0}".format(str(exc)))

    def delete_account(self):
        """Delete Cognitive Services account"""
        self.log('Deleting Cognitive Services account {0}'.format(self.name))

        try:
            poller = self.cognitive_services_management_client.accounts.begin_delete(
                self.resource_group,
                self.name
            )
            self.get_poller_result(poller)
        except Exception as exc:
            self.module.fail_json(msg="Failed to delete Cognitive Services account: {0}".format(str(exc)))
        if self.purge:
            try:
                poller = self.cognitive_services_management_client.deleted_accounts.begin_purge(
                    self.location,
                    self.resource_group,
                    self.name
                )
                self.get_poller_result(poller)
            except Exception as exc:
                self.module.fail_json(msg="Failed to purge Cognitive Services account: {0}".format(str(exc)))


def main():
    AzureRMCognitiveServicesAccount()


if __name__ == '__main__':
    main()
