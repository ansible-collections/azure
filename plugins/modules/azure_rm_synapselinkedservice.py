#!/usr/bin/python
#
# Copyright (c) 2026
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_synapselinkedservice
version_added: "4.3.0"
short_description: Manage an Azure Synapse SQL linked service
description:
    - Create, update, or delete an Azure SQL Database linked service in an existing Synapse workspace.
    - SQL credentials are sent to Azure as a secure connection string and are never returned.
    - Azure masks secure values when reading a linked service. Use I(force_password_update) to rotate
      the password on an existing linked service.
options:
    resource_group:
        description: Resource group containing the Synapse workspace.
        required: true
        type: str
    workspace_name:
        description: Synapse workspace name.
        required: true
        type: str
    name:
        description: Linked service name.
        required: true
        type: str
    server:
        description: Azure SQL server hostname. Required when creating a linked service.
        type: str
    database:
        description: Azure SQL database name. Required when creating a linked service.
        type: str
    user_name:
        description: SQL authentication user name. Required when creating a linked service.
        type: str
    password:
        description: SQL authentication password. Required when creating a linked service.
        type: str
    integration_runtime:
        description: Existing Synapse integration runtime name used by the linked service.
        type: str
    force_password_update:
        description: Update the secure connection string even if non-secret settings are unchanged.
        type: bool
        default: false
    state:
        description: Desired state of the linked service.
        type: str
        choices: [present, absent]
        default: present
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - OpenAI (@openai)
'''

EXAMPLES = '''
- name: Configure an Azure SQL linked service
  azure.azcollection.azure_rm_synapselinkedservice:
    resource_group: analytics
    workspace_name: analytics-synapse
    name: warehouse
    server: sql.example.database.windows.net
    database: warehouse
    user_name: pipeline-user
    password: "{{ vault_sql_password }}"
    integration_runtime: AutoResolveIntegrationRuntime
'''

RETURN = '''
linked_service:
    description: Linked service settings. Secure connection details are omitted.
    returned: when I(state=present)
    type: dict
    sample: {"name": "warehouse", "properties": {"type": "AzureSqlDatabase"}}
'''

import hashlib
import json

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMSynapseLinkedService(AzureRMModuleBase):
    API_VERSION = '2021-06-01'

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            workspace_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            server=dict(type='str'),
            database=dict(type='str'),
            user_name=dict(type='str'),
            password=dict(type='str', no_log=True),
            integration_runtime=dict(type='str'),
            force_password_update=dict(type='bool', default=False),
            state=dict(type='str', choices=['present', 'absent'], default='present'),
        )
        super(AzureRMSynapseLinkedService, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        if self.state == 'present' and not all((self.server, self.database, self.user_name, self.password)):
            self.fail('server, database, user_name, and password are required for state=present')

        url = '{0}subscriptions/{1}/resourceGroups/{2}/providers/Microsoft.Synapse/workspaces/{3}/linkedServices/{4}'.format(
            self._cloud_environment.endpoints.resource_manager.rstrip('/') + '/', self.subscription_id,
            self.resource_group, self.workspace_name, self.name)
        query = {'api-version': self.API_VERSION}
        try:
            response = self.rm_client.query(url, 'GET', query, None, None, [200, 404], 0, 0)
        except Exception as exc:
            self.fail('Error retrieving Synapse linked service {0}: {1}'.format(self.name, exc))
        current = json.loads(response.body()) if response.status_code == 200 else None
        self._current = current or {}

        if self.state == 'absent':
            if current and not self.check_mode:
                try:
                    self.rm_client.query(url, 'DELETE', query, None, None, [200, 202, 204], 0, 0)
                except Exception as exc:
                    self.fail('Error deleting Synapse linked service {0}: {1}'.format(self.name, exc))
            return dict(changed=current is not None)

        if current is None:
            desired = self._body(include_password=True)
            changed = True
        else:
            desired = self._body(include_password=self.force_password_update)
            current_comparable = self._comparable(current)
            desired_comparable = self._comparable(desired)
            changed = current_comparable != desired_comparable or self.force_password_update
        if changed and not self.check_mode:
            try:
                response = self.rm_client.query(url, 'PUT', query, {'Content-Type': 'application/json'},
                                                json.dumps(desired), [200, 201, 202], 0, 0)
                if response.status_code in (200, 201) and response.body():
                    current = json.loads(response.body())
                else:
                    current = desired
            except Exception as exc:
                self.fail('Error creating or updating Synapse linked service {0}: {1}'.format(self.name, exc))
        if self.check_mode and current is None:
            current = desired
        return dict(changed=changed, linked_service=self._redact(current) if current else {})

    def _body(self, include_password):
        marker_prefix = 'ansible.azure_rm_synapselinkedservice:'
        current_annotations = self._current.get('properties', {}).get('annotations', [])
        annotations = [value for value in current_annotations
                       if not (isinstance(value, str) and value.startswith(marker_prefix))]
        config = '\0'.join((self.server, self.database, self.user_name)).encode('utf-8')
        annotations.append(marker_prefix + hashlib.sha256(config).hexdigest())
        properties = dict(self._current.get('properties') or {})
        type_properties = dict(properties.get('typeProperties') or {})
        properties['type'] = 'AzureSqlDatabase'
        properties['annotations'] = annotations
        if include_password:
            type_properties['connectionString'] = dict(
                type='SecureString', value=self._connection_string())
        elif type_properties.get('encryptedCredential'):
            type_properties.pop('connectionString', None)
        properties['typeProperties'] = type_properties
        if self.integration_runtime:
            properties['connectVia'] = dict(
                referenceName=self.integration_runtime,
                type='IntegrationRuntimeReference',
            )
        return dict(properties=properties)

    def _connection_string(self):
        def quote(value):
            return '{' + value.replace('}', '}}') + '}'

        return ('Server=tcp:{0},1433;Initial Catalog={1};Persist Security Info=False;'
                'User ID={2};Password={3};MultipleActiveResultSets=False;Encrypt=True;'
                'TrustServerCertificate=False;Connection Timeout=30;').format(
                    quote(self.server), quote(self.database), quote(self.user_name), quote(self.password))

    def _comparable(self, body):
        properties = body.get('properties', {})
        type_properties = properties.get('typeProperties', {})
        return dict(
            type=properties.get('type'),
            connect_via=properties.get('connectVia'),
            annotations=properties.get('annotations', []),
        )

    def _redact(self, body):
        result = dict(body)
        properties = dict(result.get('properties') or {})
        type_properties = dict(properties.get('typeProperties') or {})
        type_properties.pop('connectionString', None)
        type_properties.pop('encryptedCredential', None)
        type_properties.pop('password', None)
        properties['typeProperties'] = type_properties
        result['properties'] = properties
        return result


def main():
    AzureRMSynapseLinkedService()


if __name__ == '__main__':
    main()
