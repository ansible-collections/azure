#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_cognitiveservicesdeployment_info
version_added: "4.2.0"
short_description: Get Azure AI / OpenAI model deployment facts
description:
    - Get facts for a specific model deployment or list all deployments in an
      Azure AI Services / Azure OpenAI (Cognitive Services) account.
options:
    resource_group:
        description:
            - Name of the resource group containing the account.
        required: true
        type: str
        aliases:
            - resource_group_name
    account_name:
        description:
            - Name of the Cognitive Services / Azure OpenAI account.
        required: true
        type: str
    name:
        description:
            - Name of a specific deployment. If omitted, all deployments in the account are returned.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get facts for a specific deployment
  azure.azcollection.azure_rm_cognitiveservicesdeployment_info:
    resource_group: myResourceGroup
    account_name: myopenaiaccount
    name: gpt-4o-mini

- name: List all deployments in an account
  azure.azcollection.azure_rm_cognitiveservicesdeployment_info:
    resource_group: myResourceGroup
    account_name: myopenaiaccount
'''

RETURN = '''
deployments:
    description:
        - List of model deployments.
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "id": "/subscriptions/xxx/resourceGroups/myResourceGroup/providers/Microsoft.CognitiveServices/accounts/myopenaiaccount/deployments/gpt-4o-mini",
            "name": "gpt-4o-mini",
            "sku": {"name": "Standard", "capacity": 10},
            "properties": {
                "model": {"format": "OpenAI", "name": "gpt-4o-mini", "version": "2024-07-18"},
                "provisioning_state": "Succeeded"
            },
            "type": "Microsoft.CognitiveServices/accounts/deployments"
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMCognitiveServicesDeploymentInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True, aliases=['resource_group_name']),
            account_name=dict(type='str', required=True),
            name=dict(type='str'),
            tags=dict(type='list', elements='str'),
        )

        self.resource_group = None
        self.account_name = None
        self.name = None
        self.tags = None

        self.results = dict(
            changed=False,
            deployments=[]
        )

        super(AzureRMCognitiveServicesDeploymentInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            results = self.get_deployment()
        else:
            results = self.list_deployments()

        self.results['deployments'] = [
            d for d in results if self.has_tags(d.get('tags'), self.tags)
        ]
        return self.results

    def get_deployment(self):
        """Get a specific deployment."""
        self.log('Getting deployment {0}'.format(self.name))
        try:
            obj = self.cognitive_services_management_client.deployments.get(
                self.resource_group,
                self.account_name,
                self.name
            )
            return [obj.as_dict()]
        except ResourceNotFoundError:
            self.log('Deployment {0} not found'.format(self.name))
            return []

    def list_deployments(self):
        """List all deployments in the account."""
        self.log('Listing deployments in account {0}'.format(self.account_name))
        results = []
        try:
            deployments = self.cognitive_services_management_client.deployments.list(
                self.resource_group,
                self.account_name
            )
            for obj in deployments:
                results.append(obj.as_dict())
        except ResourceNotFoundError:
            self.log('Account {0} not found'.format(self.account_name))
        return results


def main():
    AzureRMCognitiveServicesDeploymentInfo()


if __name__ == '__main__':
    main()
