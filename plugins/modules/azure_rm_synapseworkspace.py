#!/usr/bin/python
#
# Copyright (c) 2026
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_synapseworkspace
version_added: "4.3.0"
short_description: Manage an Azure Synapse workspace
description:
    - Create, update, or delete an Azure Synapse Analytics workspace.
    - Creating a workspace requires an existing ADLS Gen2 storage account and filesystem.
    - SQL administrator passwords are not returned. Use I(force_password_update) to rotate a password.
options:
    resource_group:
        description: Resource group containing the workspace.
        required: true
        type: str
    name:
        description: Synapse workspace name.
        required: true
        type: str
    location:
        description: Azure region for the workspace. Required at creation.
        type: str
    storage_account_url:
        description: DFS endpoint URL of the existing ADLS Gen2 account.
        type: str
    filesystem:
        description: Existing ADLS Gen2 filesystem used as the default data lake.
        type: str
    sql_admin_login:
        description: SQL administrator login name.
        type: str
    sql_admin_password:
        description: SQL administrator password.
        type: str
    managed_resource_group_name:
        description: Managed resource group name for the workspace.
        type: str
    public_network_access:
        description: Controls public network access to the workspace.
        type: str
        choices: [Enabled, Disabled]
    tags:
        description: Resource tags.
        type: dict
    force_password_update:
        description: Update the SQL administrator password even if other settings are unchanged.
        type: bool
        default: false
    state:
        description: Desired state of the workspace.
        type: str
        choices: [present, absent]
        default: present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - OpenAI (@openai)
'''

EXAMPLES = '''
- name: Create a Synapse workspace
  azure.azcollection.azure_rm_synapseworkspace:
    resource_group: analytics
    name: analytics-synapse
    location: eastus
    storage_account_url: https://analyticslake.dfs.core.windows.net
    filesystem: synapse
    sql_admin_login: synapseadmin
    sql_admin_password: "{{ vault_synapse_sql_password }}"
    managed_resource_group_name: analytics-synapse-managed
    tags:
      environment: test
'''

RETURN = '''
workspace:
    description: Synapse workspace ARM resource. Password values are omitted.
    returned: when I(state=present)
    type: dict
    sample: {"name": "analytics-synapse", "location": "eastus", "properties": {"provisioningState": "Succeeded"}}
'''

import json

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMSynapseWorkspace(AzureRMModuleBase):
    API_VERSION = '2021-06-01'

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            storage_account_url=dict(type='str'),
            filesystem=dict(type='str'),
            sql_admin_login=dict(type='str'),
            sql_admin_password=dict(type='str', no_log=True),
            managed_resource_group_name=dict(type='str'),
            public_network_access=dict(type='str', choices=['Enabled', 'Disabled']),
            tags=dict(type='dict'),
            force_password_update=dict(type='bool', default=False),
            state=dict(type='str', choices=['present', 'absent'], default='present'),
        )
        super(AzureRMSynapseWorkspace, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        url = '{0}subscriptions/{1}/resourceGroups/{2}/providers/Microsoft.Synapse/workspaces/{3}'.format(
            self._cloud_environment.endpoints.resource_manager.rstrip('/') + '/', self.subscription_id,
            self.resource_group, self.name)
        query = {'api-version': self.API_VERSION}
        try:
            response = self.rm_client.query(url, 'GET', query, None, None, [200, 404], 0, 0)
        except Exception as exc:
            self.fail('Error retrieving Synapse workspace {0}: {1}'.format(self.name, exc))
        existing = json.loads(response.body()) if response.status_code == 200 else None
        if self.state == 'absent':
            if existing and not self.check_mode:
                try:
                    self.rm_client.query(url, 'DELETE', query, None, None, [200, 202, 204], 0, 0)
                except Exception as exc:
                    self.fail('Error deleting Synapse workspace {0}: {1}'.format(self.name, exc))
            return dict(changed=existing is not None)

        tags_changed = False
        if existing is not None:
            if self.location and self.location.lower() != existing.get('location', '').lower():
                self.fail('The location of Synapse workspace {0} is immutable'.format(self.name))
            if self.tags is not None:
                tags_changed, self.tags = self.update_tags(existing.get('tags'))

        if existing is None and not all((self.location, self.storage_account_url, self.filesystem,
                                         self.sql_admin_login, self.sql_admin_password)):
            self.fail('location, storage_account_url, filesystem, sql_admin_login, and sql_admin_password '
                      'are required when creating a Synapse workspace')
        desired = self._body(existing)
        changed = existing is None or self._comparable(existing) != self._comparable(desired) or tags_changed
        changed = changed or (existing is not None and self.force_password_update)
        if changed and not self.check_mode:
            try:
                response = self.rm_client.query(url, 'PUT', query, {'Content-Type': 'application/json'},
                                                json.dumps(desired), [200, 201, 202], 0, 0)
                result = json.loads(response.body()) if response.status_code in (200, 201) and response.body() else desired
            except Exception as exc:
                self.fail('Error creating or updating Synapse workspace {0}: {1}'.format(self.name, exc))
        else:
            result = desired if existing is None else existing
        return dict(changed=changed, workspace=self._redact(result))

    def _body(self, existing):
        body = dict(existing or {})
        properties = dict(body.get('properties') or {})
        if self.storage_account_url is not None or self.filesystem is not None:
            data_lake = dict(properties.get('defaultDataLakeStorage') or {})
            if self.storage_account_url is not None:
                data_lake['accountUrl'] = self.storage_account_url
            if self.filesystem is not None:
                data_lake['filesystem'] = self.filesystem
            properties['defaultDataLakeStorage'] = data_lake
        if self.sql_admin_login is not None:
            properties['sqlAdministratorLogin'] = self.sql_admin_login
        if self.sql_admin_password is not None and (existing is None or self.force_password_update):
            properties['sqlAdministratorLoginPassword'] = self.sql_admin_password
        if self.managed_resource_group_name is not None:
            properties['managedResourceGroupName'] = self.managed_resource_group_name
        if self.public_network_access is not None:
            properties['publicNetworkAccess'] = self.public_network_access
        body.update(location=self.location or body.get('location'), properties=properties)
        if self.tags is not None:
            body['tags'] = self.tags
        return body

    def _comparable(self, body):
        properties = body.get('properties') or {}
        storage = properties.get('defaultDataLakeStorage') or {}
        return dict(
            location=body.get('location'),
            tags=body.get('tags') or {},
            account_url=storage.get('accountUrl'),
            filesystem=storage.get('filesystem'),
            sql_admin_login=properties.get('sqlAdministratorLogin'),
            managed_resource_group_name=properties.get('managedResourceGroupName'),
            public_network_access=properties.get('publicNetworkAccess'),
        )

    def _redact(self, body):
        result = dict(body)
        properties = dict(result.get('properties') or {})
        properties.pop('sqlAdministratorLoginPassword', None)
        result['properties'] = properties
        return result


def main():
    AzureRMSynapseWorkspace()


if __name__ == '__main__':
    main()
