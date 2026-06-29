#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck, <bpeck@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_databricksworkspace_info
version_added: "3.20.0"
short_description: Get facts of Azure Databricks workspaces
description:
    - Get, query Azure Databricks workspaces.
options:
    resource_group:
        description:
            - Name of resource group.
        type: str
    name:
        description:
            - Name of the workspace.
            - The resource group must be configured when name exists.
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
- name: Get a specific workspace
  azure_rm_databricksworkspace_info:
    resource_group: myResourceGroup
    name: myDatabricksWorkspace

- name: List workspaces in a resource group
  azure_rm_databricksworkspace_info:
    resource_group: myResourceGroup

- name: List all workspaces in subscription
  azure_rm_databricksworkspace_info:

- name: List workspaces with specific tags
  azure_rm_databricksworkspace_info:
    tags:
      - environment:test
      - purpose:databricks
'''

RETURN = '''
workspaces:
    description:
        - List of Databricks workspaces.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description:
                - Workspace resource path.
            type: str
            returned: success
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Databricks/workspaces/myDatabricksWorkspace"
        name:
            description:
                - The name of the workspace.
            type: str
            returned: success
            sample: myDatabricksWorkspace
        location:
            description:
                - Resource location.
            type: str
            returned: success
            sample: eastus
        type:
            description:
                - Resource type.
            type: str
            returned: success
            sample: Microsoft.Databricks/workspaces
        sku:
            description:
                - The SKU of the workspace.
            type: dict
            returned: success
            sample: {'name': 'premium', 'tier': 'Premium'}
        managed_resource_group_id:
            description:
                - The managed resource group ID.
            type: str
            returned: success
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/databricks-rg-myDatabricksWorkspace-abc123
        workspace_id:
            description:
                - The unique identifier of the Databricks workspace.
            type: str
            returned: success
            sample: "1234567890123456"
        workspace_url:
            description:
                - The workspace URL.
            type: str
            returned: success
            sample: adb-1234567890123456.12.azuredatabricks.net
        provisioning_state:
            description:
                - The workspace provisioning state.
            type: str
            returned: success
            sample: Succeeded
        resource_group:
            description:
                - The resource group of the workspace.
            type: str
            returned: success
            sample: myResourceGroup
        tags:
            description:
                - Resource tags.
            type: dict
            returned: success
            sample: {'environment': 'test'}
'''  # NOQA

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
    from azure.mgmt.core.tools import parse_resource_id
except ImportError:
    pass


class AzureRMDatabricksWorkspaceInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.results = dict(
            changed=False,
            workspaces=[]
        )

        self.resource_group = None
        self.name = None
        self.tags = None

        super(AzureRMDatabricksWorkspaceInfo, self).__init__(
            self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            if self.resource_group:
                item = self.get_workspace()
                response = [item] if item else []
            else:
                self.fail('The resource_group must be configured when name exists')
        elif self.resource_group:
            response = self.list_by_resource_group()
        else:
            response = self.list_by_subscription()

        self.results['workspaces'] = [self.to_dict(x) for x in response if self.has_tags(x.tags, self.tags)]
        return self.results

    def get_workspace(self):
        try:
            return self.databricks_client.workspaces.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            pass
        return None

    def list_by_resource_group(self):
        try:
            return list(self.databricks_client.workspaces.list_by_resource_group(self.resource_group))
        except Exception as exc:
            self.fail('Error listing workspaces by resource group {0} - {1}'.format(self.resource_group, str(exc)))
        return []

    def list_by_subscription(self):
        try:
            return list(self.databricks_client.workspaces.list_by_subscription())
        except Exception as exc:
            self.fail('Error listing workspaces by subscription - {0}'.format(str(exc)))
        return []

    def to_dict(self, workspace):
        result = workspace.as_dict()
        result['resource_group'] = parse_resource_id(result['id'])['resource_group']
        return result


def main():
    AzureRMDatabricksWorkspaceInfo()


if __name__ == '__main__':
    main()
