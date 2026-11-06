#!/usr/bin/python
#
# Copyright (c) 2026
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_synapselinkedservice_info
version_added: "4.3.0"
short_description: Get Azure Synapse linked service facts
description:
    - Get one linked service or list linked services in a Synapse workspace.
    - Secure connection strings and credentials are omitted from the returned resources.
options:
    resource_group:
        description: Resource group containing the workspace.
        type: str
        required: true
    workspace_name:
        description: Synapse workspace name.
        type: str
        required: true
    name:
        description: Return only this linked service. When omitted, list workspace linked services.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - OpenAI (@openai)
'''

EXAMPLES = '''
- name: Get an Azure SQL linked service
  azure.azcollection.azure_rm_synapselinkedservice_info:
    resource_group: analytics
    workspace_name: analytics-synapse
    name: warehouse

- name: List linked services
  azure.azcollection.azure_rm_synapselinkedservice_info:
    resource_group: analytics
    workspace_name: analytics-synapse
'''

RETURN = '''
linked_services:
    description: Linked service ARM resources. Credentials and secure strings are omitted.
    returned: always
    type: list
    elements: dict
    sample: [{"name": "warehouse", "properties": {"type": "AzureSqlDatabase"}}]
'''

import json

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMSynapseLinkedServiceInfo(AzureRMModuleBase):
    API_VERSION = '2021-06-01'

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            workspace_name=dict(type='str', required=True),
            name=dict(type='str'),
        )
        self.results = dict(changed=False, linked_services=[])
        super(AzureRMSynapseLinkedServiceInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True,
            supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        base_url = ('{0}subscriptions/{1}/resourceGroups/{2}/providers/Microsoft.Synapse/'
                    'workspaces/{3}/linkedServices').format(
                        self._cloud_environment.endpoints.resource_manager.rstrip('/') + '/',
                        self.subscription_id, self.resource_group, self.workspace_name)
        query = {'api-version': self.API_VERSION}
        try:
            if self.name:
                response = self.rm_client.query(base_url + '/' + self.name, 'GET', query, None, None,
                                                [200, 404], 0, 0)
                values = [json.loads(response.body())] if response.status_code == 200 else []
            else:
                response = self.rm_client.query(base_url, 'GET', query, None, None, [200], 0, 0)
                values = json.loads(response.body()).get('value', [])
        except Exception as exc:
            self.fail('Error retrieving Synapse linked services: {0}'.format(exc))
        self.results['linked_services'] = [self._redact(value) for value in values]
        return self.results

    def _redact(self, value):
        result = dict(value)
        properties = dict(result.get('properties') or {})
        type_properties = dict(properties.get('typeProperties') or {})
        for key in ('connectionString', 'encryptedCredential', 'password', 'servicePrincipalKey'):
            type_properties.pop(key, None)
        properties['typeProperties'] = type_properties
        result['properties'] = properties
        return result


def main():
    AzureRMSynapseLinkedServiceInfo()


if __name__ == '__main__':
    main()
