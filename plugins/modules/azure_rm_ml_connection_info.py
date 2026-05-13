#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_connection_info
version_added: "3.19.0"
short_description: List ML Connection resources
description:
    - List ML Connection resources.
options:
    name:
        description:
            - Name of the connection.
        type: str
        required: false
    populate_secrets:
        description:
            - For API key-based connections, try to populate the returned
              credentials with the actual secret value. Does nothing for
              non-API key-based connections.
        type: bool
        default: false
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    ml_workspace:
        description:
            - Name of the Azure ML workspace.
        required: true
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: List Specific ML connection
  azure.azcollection.azure_rm_ml_connection_info:
    name: MyConnection
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List ML connection
  azure.azcollection.azure_rm_ml_connection_info:
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
'''

RETURN = '''
ml_connections:
    description:
        - List of ML Connections.
    returned: always
    type: dict
    sample: [
      {
        "creation_context": {
            "created_at": "2026-05-11T20:07:52.118675+00:00",
            "created_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "created_by_type": "Application",
            "last_modified_at": "2026-05-11T20:07:52.118675+00:00",
            "last_modified_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "last_modified_by_type": "Application"
        },
        "credentials": {
            "type": "username_password"
        },
        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-connection/providers/Microsoft.MachineLearningServices/workspaces/workspacexxxxxxxxxx/connections/connectionxxxxxxxxxx",
        "is_shared": true,
        "metadata": {},
        "name": "connectionxxxxxxxxxx",
        "tags": {},
        "target": "https://test-git-feed.com",
        "type": "git"
      }
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLConnectionInfo(MLClientCommon):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=False,
            ),
            populate_secrets=dict(
                type='bool',
                default=False,
            ),
            resource_group=dict(
                type='str',
                required=True,
            ),
            ml_workspace=dict(
                type='str',
                required=True,
            ),
        )

        self._client = None
        self.ml_registry = None

        self.results = dict(
            ml_connections=[]
        )

        super(AzureRMMLConnectionInfo, self).__init__(self.module_arg_spec,
                                                      supports_tags=False,
                                                      supports_check_mode=True,
                                                      facts_module=True,
                                                      )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            try:
                result = self.client.connections.get(
                    name=self.name,
                    populate_secrets=self.populate_secrets
                )
                ml_connections = [self.entity_to_dict(result)]
            except ResourceNotFoundError:
                ml_connections = []
        else:
            results = self.client.connections.list(
                populate_secrets=self.populate_secrets
            )
            ml_connections = [self.entity_to_dict(x) for x in results]

        self.results['ml_connections'] = ml_connections
        return self.results


def main():
    AzureRMMLConnectionInfo()


if __name__ == '__main__':
    main()
