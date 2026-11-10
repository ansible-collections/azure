#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
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
    - Bill Peck (@p3ck)
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
    description: Synapse workspaces. Administrator passwords are omitted.
    returned: always
    type: list
    elements: dict
    sample: [{"name": "analytics-synapse", "location": "eastus", "provisioning_state": "Succeeded"}]
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMSynapseWorkspaceInfo(AzureRMModuleBase):
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
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            try:
                workspaces = [self.synapse_client.workspaces.get(self.resource_group, self.name)]
            except ResourceNotFoundError:
                workspaces = []
            except Exception as exc:
                self.fail('Error retrieving Synapse workspace {0}: {1}'.format(self.name, str(exc)))
        else:
            try:
                workspaces = list(self.synapse_client.workspaces.list_by_resource_group(self.resource_group))
            except Exception as exc:
                self.fail('Error listing Synapse workspaces in resource group {0}: {1}'.format(
                    self.resource_group, str(exc)))
        self.results['workspaces'] = [self._format(workspace) for workspace in workspaces]
        return self.results

    def _format(self, workspace):
        result = workspace.as_dict()
        result['resource_group'] = self.resource_group
        result.pop('sql_administrator_login_password', None)
        return result


def main():
    AzureRMSynapseWorkspaceInfo()


if __name__ == '__main__':
    main()
