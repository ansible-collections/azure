#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
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
    - Bill Peck (@p3ck)
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
    description: Synapse workspace. Administrator passwords are omitted.
    returned: when I(state=present)
    type: dict
    sample: {"name": "analytics-synapse", "location": "eastus", "provisioning_state": "Succeeded"}
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.mgmt.synapse import models
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMSynapseWorkspace(AzureRMModuleBase):
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

        self.resource_group = None
        self.name = None
        self.location = None
        self.storage_account_url = None
        self.filesystem = None
        self.sql_admin_login = None
        self.sql_admin_password = None
        self.managed_resource_group_name = None
        self.public_network_access = None
        self.tags = None
        self.force_password_update = None
        self.state = None

        self.results = dict(changed=False)

        super(AzureRMSynapseWorkspace, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        existing = self.get_workspace()

        if self.state == 'absent':
            if existing is not None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.delete_workspace()
            return self.results

        return self.create_or_update_workspace(existing)

    def get_workspace(self):
        self.log('Get Synapse workspace {0}'.format(self.name))
        try:
            return self.synapse_client.workspaces.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            return None
        except Exception as exc:
            self.fail('Error retrieving Synapse workspace {0}: {1}'.format(self.name, str(exc)))

    def create_or_update_workspace(self, existing):
        tags_changed = False
        if existing is not None:
            if self.location is not None and self.location.lower() != existing.location.lower():
                self.fail('The location of Synapse workspace {0} is immutable'.format(self.name))
            if self.tags is not None:
                tags_changed, self.tags = self.update_tags(existing.tags)
        else:
            # required_if cannot express fields that are only needed when the
            # workspace does not exist yet.
            if not all((self.location, self.storage_account_url, self.filesystem,
                        self.sql_admin_login, self.sql_admin_password)):
                self.fail('location, storage_account_url, filesystem, sql_admin_login, and sql_admin_password '
                          'are required when creating a Synapse workspace')

        desired = self._workspace(existing)
        self.results['changed'] = (existing is None or tags_changed or
                                   self._comparable(existing) != self._comparable(desired) or
                                   self.force_password_update)

        if self.check_mode or not self.results['changed']:
            self.results['workspace'] = self._format(desired if existing is None else existing)
            return self.results

        try:
            poller = self.synapse_client.workspaces.begin_create_or_update(
                self.resource_group, self.name, desired)
            existing = self.get_poller_result(poller)
        except Exception as exc:
            self.fail('Error creating / updating Synapse workspace {0}: {1}'.format(self.name, str(exc)))

        self.results['workspace'] = self._format(existing)
        return self.results

    def delete_workspace(self):
        self.log('Delete Synapse workspace {0}'.format(self.name))
        try:
            poller = self.synapse_client.workspaces.begin_delete(self.resource_group, self.name)
            self.get_poller_result(poller)
        except Exception as exc:
            self.fail('Error deleting Synapse workspace {0}: {1}'.format(self.name, str(exc)))

    def _workspace(self, existing):
        """Build the full workspace payload for the create / update call."""
        if existing is None:
            storage = models.DataLakeStorageAccountDetails()
        else:
            storage = existing.default_data_lake_storage or models.DataLakeStorageAccountDetails()
        data_lake = models.DataLakeStorageAccountDetails(
            account_url=self.storage_account_url or storage.account_url,
            filesystem=self.filesystem or storage.filesystem)

        password = None
        if existing is None or self.force_password_update:
            password = self.sql_admin_password

        workspace = models.Workspace(
            location=self.location or (existing.location if existing is not None else None),
            tags=self.tags if self.tags is not None else (existing.tags if existing is not None else None),
            default_data_lake_storage=data_lake,
            sql_administrator_login=self.sql_admin_login or (
                existing.sql_administrator_login if existing is not None else None),
            sql_administrator_login_password=password,
            managed_resource_group_name=self.managed_resource_group_name or (
                existing.managed_resource_group_name if existing is not None else None),
            public_network_access=self.public_network_access or (
                existing.public_network_access if existing is not None else None),
        )
        if existing is not None:
            # Carry forward the properties this module does not manage so the
            # full-replace update does not reset them.
            workspace.identity = existing.identity
            workspace.encryption = existing.encryption
            workspace.virtual_network_profile = existing.virtual_network_profile
            workspace.managed_virtual_network = existing.managed_virtual_network
            workspace.managed_virtual_network_settings = existing.managed_virtual_network_settings
            workspace.workspace_repository_configuration = existing.workspace_repository_configuration
            workspace.purview_configuration = existing.purview_configuration
        return workspace

    def _comparable(self, workspace):
        storage = workspace.default_data_lake_storage or models.DataLakeStorageAccountDetails()
        return dict(
            location=workspace.location.lower() if workspace.location else None,
            tags=workspace.tags or {},
            account_url=storage.account_url,
            filesystem=storage.filesystem,
            sql_admin_login=workspace.sql_administrator_login,
            managed_resource_group_name=workspace.managed_resource_group_name,
            public_network_access=workspace.public_network_access,
        )

    def _format(self, workspace):
        result = workspace.as_dict()
        result.pop('sql_administrator_login_password', None)
        return result


def main():
    AzureRMSynapseWorkspace()


if __name__ == '__main__':
    main()
