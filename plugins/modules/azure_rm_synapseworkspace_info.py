#!/usr/bin/python
#
# Copyright (c) 2026
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_synapseworkspace_info
version_added: "4.3.0"
short_description: Get Azure Synapse workspace facts
description:
    - Get one Synapse workspace or list workspaces in a resource group.
    - SQL administrator passwords are never returned by the module.
options:
    resource_group:
        description: Resource group containing the workspace.
        type: str
        required: true
    name:
        description: Return only this workspace. When omitted, list resource-group workspaces.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - OpenAI (@openai)
'''

EXAMPLES = '''
- name: Get a Synapse workspace
  azure.azcollection.azure_rm_synapseworkspace_info:
    resource_group: analytics
    name: analytics-synapse

- name: List Synapse workspaces in a resource group
  azure.azcollection.azure_rm_synapseworkspace_info:
    resource_group: analytics
'''

RETURN = '''
workspaces:
    description: Synapse workspace ARM resources. Administrator passwords are omitted.
    returned: always
    type: list
    elements: dict
    sample: [{"name": "analytics-synapse", "location": "eastus", "properties": {"provisioningState": "Succeeded"}}]
'''

import json

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMSynapseWorkspaceInfo(AzureRMModuleBase):
    API_VERSION = '2021-06-01'

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str'),
        )
        self.results = dict(changed=False, workspaces=[])
        super(AzureRMSynapseWorkspaceInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True,
            supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        base_url = '{0}subscriptions/{1}/resourceGroups/{2}/providers/Microsoft.Synapse/workspaces'.format(
            self._cloud_environment.endpoints.resource_manager.rstrip('/') + '/', self.subscription_id,
            self.resource_group)
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
            self.fail('Error retrieving Synapse workspaces: {0}'.format(exc))
        for workspace in values:
            workspace.setdefault('resource_group', self.resource_group)
            workspace['properties'] = dict(workspace.get('properties') or {})
            workspace['properties'].pop('sqlAdministratorLoginPassword', None)
        self.results['workspaces'] = values
        return self.results


def main():
    AzureRMSynapseWorkspaceInfo()


if __name__ == '__main__':
    main()
