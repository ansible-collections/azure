#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck, <bpeck@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_databricksworkspace
version_added: "3.20.0"
short_description: Manage Azure Databricks workspaces
description:
    - Create, update or delete Azure Databricks workspaces.
options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    name:
        description:
            - Name of the workspace.
        required: true
        type: str
    state:
        description:
            - Assert the state of the workspace. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present
    location:
        description:
            - Resource location.
        type: str
    sku:
        description:
            - The SKU of the workspace.
        type: dict
        suboptions:
            name:
                description:
                    - The SKU name.
                type: str
                required: true
                choices:
                    - standard
                    - premium
                    - trial
    managed_resource_group_id:
        description:
            - The managed resource group ID.
        type: str
    parameters:
        description:
            - Custom parameters for the workspace.
        type: dict
        suboptions:
            enable_no_public_ip:
                description:
                    - Whether to enable no public IP.
                type: dict
                suboptions:
                    value:
                        description:
                            - The value to enable or disable no public IP.
                        type: bool
                        required: true
            prepare_encryption:
                description:
                    - Whether to prepare encryption.
                type: dict
                suboptions:
                    value:
                        description:
                            - The value to enable or disable prepare encryption.
                        type: bool
                        required: true
            require_infrastructure_encryption:
                description:
                    - Whether to require infrastructure encryption.
                type: dict
                suboptions:
                    value:
                        description:
                            - The value to enable or disable require infrastructure encryption.
                        type: bool
                        required: true
            custom_virtual_network_id:
                description:
                    - Custom virtual network ID.
                type: dict
                suboptions:
                    value:
                        description:
                            - The resource ID of the custom VNet.
                        type: str
                        required: true
            custom_public_subnet_name:
                description:
                    - Custom public subnet name.
                type: dict
                suboptions:
                    value:
                        description:
                            - The name of the public subnet.
                        type: str
                        required: true
            custom_private_subnet_name:
                description:
                    - Custom private subnet name.
                type: dict
                suboptions:
                    value:
                        description:
                            - The name of the private subnet.
                        type: str
                        required: true
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create a Databricks workspace
  azure_rm_databricksworkspace:
    resource_group: myResourceGroup
    name: myDatabricksWorkspace
    location: eastus
    managed_resource_group_id: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx/resourceGroups/myManagedResourceGroup"
    sku:
      name: premium
    tags:
      environment: test

- name: Create a Databricks workspace with custom VNet
  azure_rm_databricksworkspace:
    resource_group: myResourceGroup
    name: myDatabricksWorkspace
    location: eastus
    managed_resource_group_id: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx/resourceGroups/myManagedResourceGroup"
    sku:
      name: premium
    parameters:
      custom_virtual_network_id:
        value: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myVnetRG/providers/Microsoft.Network/virtualNetworks/myVnet
      custom_public_subnet_name:
        value: public-subnet
      custom_private_subnet_name:
        value: private-subnet
      enable_no_public_ip:
        value: true

- name: Delete a Databricks workspace
  azure_rm_databricksworkspace:
    resource_group: myResourceGroup
    name: myDatabricksWorkspace
    state: absent
'''

RETURN = '''
id:
    description:
        - Workspace resource path.
    type: str
    returned: success
    example: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Databricks/workspaces/myDatabricksWorkspace"
name:
    description:
        - The name of the workspace.
    type: str
    returned: success
    example: myDatabricksWorkspace
location:
    description:
        - Resource location.
    type: str
    returned: success
    example: eastus
type:
    description:
        - Resource type.
    type: str
    returned: success
    example: Microsoft.Databricks/workspaces
sku:
    description:
        - The SKU of the workspace.
    type: dict
    returned: success
    example: {'name': 'premium'}
managed_resource_group_id:
    description:
        - The managed resource group ID.
    type: str
    returned: success
    example: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/databricks-rg-myDatabricksWorkspace-abc123
workspace_id:
    description:
        - The unique identifier of the Databricks workspace.
    type: str
    returned: success
    example: 1234567890123456
workspace_url:
    description:
        - The workspace URL.
    type: str
    returned: success
    example: adb-1234567890123456.12.azuredatabricks.net
provisioning_state:
    description:
        - The workspace provisioning state.
    type: str
    returned: success
    example: Succeeded
tags:
    description:
        - Resource tags.
    type: dict
    returned: success
    example: {'environment': 'test'}
'''  # NOQA

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass


class AzureRMDatabricksWorkspace(AzureRMModuleBaseExt):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(type='str', required=True, choices=['standard', 'premium', 'trial']),
                )
            ),
            managed_resource_group_id=dict(type='str'),
            parameters=dict(
                type='dict',
                options=dict(
                    enable_no_public_ip=dict(
                        type='dict',
                        options=dict(
                            value=dict(type='bool', required=True)
                        )
                    ),
                    prepare_encryption=dict(
                        type='dict',
                        options=dict(
                            value=dict(type='bool', required=True)
                        )
                    ),
                    require_infrastructure_encryption=dict(
                        type='dict',
                        options=dict(
                            value=dict(type='bool', required=True)
                        )
                    ),
                    custom_virtual_network_id=dict(
                        type='dict',
                        options=dict(
                            value=dict(type='str', required=True)
                        )
                    ),
                    custom_public_subnet_name=dict(
                        type='dict',
                        options=dict(
                            value=dict(type='str', required=True)
                        )
                    ),
                    custom_private_subnet_name=dict(
                        type='dict',
                        options=dict(
                            value=dict(type='str', required=True)
                        )
                    )
                )
            )
        )

        self.results = dict(
            changed=False,
            id=None
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None
        self.sku = None
        self.managed_resource_group_id = None
        self.parameters = None

        required_if = [
            ('state', 'present', ['managed_resource_group_id']),
        ]

        super(AzureRMDatabricksWorkspace, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True, required_if=required_if)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        self.results = dict(
            compare=[],
        )

        changed = False

        if not self.location:
            resource_group = self.get_resource_group(self.resource_group)
            self.location = resource_group.location

        workspace = self.get_workspace()

        if not workspace and self.state == 'present':
            workspace_obj = self.create_workspace_obj()
            changed = True
            if not self.check_mode:
                workspace = self.create_or_update_workspace(workspace_obj)
        elif workspace and self.state == 'present':
            update_tags, new_tags = self.update_tags(workspace.tags)
            if update_tags:
                self.tags = new_tags

            workspace_obj = self.create_workspace_obj()

            changed = not self.default_compare({},
                                               workspace_obj.as_dict(),
                                               workspace.as_dict(),
                                               '',
                                               self.results)

            if changed and not self.check_mode:
                workspace = self.create_or_update_workspace(workspace_obj)
        elif workspace and self.state == 'absent':
            changed = True
            workspace = None
            if not self.check_mode:
                self.delete_workspace()

        if workspace:
            self.results = workspace.as_dict()

        self.results['changed'] = changed
        return self.results

    def create_workspace_obj(self):
        try:
            workspace_params = {
                'location': self.location,
                'tags': self.tags
            }

            if self.sku:
                workspace_params['sku'] = self.databricks_models.Sku(
                    name=self.sku.get('name'),
                )

            if self.managed_resource_group_id:
                workspace_params['managed_resource_group_id'] = self.managed_resource_group_id

            if self.parameters:
                parameters = {}

                if 'enable_no_public_ip' in self.parameters and self.parameters['enable_no_public_ip']:
                    parameters['enable_no_public_ip'] = self.databricks_models.WorkspaceCustomBooleanParameter(
                        value=self.parameters['enable_no_public_ip']['value']
                    )

                if 'prepare_encryption' in self.parameters and self.parameters['prepare_encryption']:
                    parameters['prepare_encryption'] = self.databricks_models.WorkspaceCustomBooleanParameter(
                        value=self.parameters['prepare_encryption']['value']
                    )

                if 'require_infrastructure_encryption' in self.parameters and self.parameters['require_infrastructure_encryption']:
                    parameters['require_infrastructure_encryption'] = self.databricks_models.WorkspaceCustomBooleanParameter(
                        value=self.parameters['require_infrastructure_encryption']['value']
                    )

                if 'custom_virtual_network_id' in self.parameters and self.parameters['custom_virtual_network_id']:
                    parameters['custom_virtual_network_id'] = self.databricks_models.WorkspaceCustomStringParameter(
                        value=self.parameters['custom_virtual_network_id']['value']
                    )

                if 'custom_public_subnet_name' in self.parameters and self.parameters['custom_public_subnet_name']:
                    parameters['custom_public_subnet_name'] = self.databricks_models.WorkspaceCustomStringParameter(
                        value=self.parameters['custom_public_subnet_name']['value']
                    )

                if 'custom_private_subnet_name' in self.parameters and self.parameters['custom_private_subnet_name']:
                    parameters['custom_private_subnet_name'] = self.databricks_models.WorkspaceCustomStringParameter(
                        value=self.parameters['custom_private_subnet_name']['value']
                    )
                workspace_params['parameters'] = self.databricks_models.WorkspaceCustomParameters(**parameters)

            return self.databricks_models.Workspace(**workspace_params)
        except Exception as exc:
            self.fail('Error creating workspace_obj {0} - {1}'.format(self.name, str(exc)))

    def create_or_update_workspace(self, workspace_obj):
        try:
            poller = self.databricks_client.workspaces.begin_create_or_update(
                self.resource_group,
                self.name,
                workspace_obj
            )
            return self.get_poller_result(poller)
        except Exception as exc:
            self.fail('Error creating/updating workspace {0} - {1}'.format(self.name, str(exc)))

    def get_workspace(self):
        try:
            return self.databricks_client.workspaces.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            pass
        return None

    def delete_workspace(self):
        try:
            poller = self.databricks_client.workspaces.begin_delete(self.resource_group, self.name)
            return self.get_poller_result(poller)
        except Exception as exc:
            self.fail('Error deleting workspace {0} - {1}'.format(self.name, str(exc)))


def main():
    AzureRMDatabricksWorkspace()


if __name__ == '__main__':
    main()
