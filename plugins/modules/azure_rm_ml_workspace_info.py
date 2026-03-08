#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_workspace_info
version_added: "3.15.0"
short_description: List ML Workspaces
description:
    - List ML Workspaces.
options:
    name:
        description:
            - Retrieve details about a specific ml workspace.
        type: str
        required: false
    filtered_kinds:
        description:
            - List only the specified kinds of ml workspaces.
        required: false
        type: list
        elements: str
        default: []
        choices:
            - default
            - hub
            - project
    resource_group:
        description:
            - Name of a resource group to limit ml workspaces from.
              If not specified the subscription will be searched.
        required: false
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get info on a specific ml workspaces
  azure.azcollection.azure_rm_ml_workspace_info:
    name: my_workspace
    resource_group: test_ml_workspace
  register: result

- name: List all ml workspaces in subscription
  azure.azcollection.azure_rm_ml_workspace_info:
  register: results

- name: List all hub workspaces in resource group
  azure.azcollection.azure_rm_ml_workspace_info:
    resource_group: test_ml_workspace
    filtered_kinds:
      - hub
  register: results
'''

RETURN = '''
ml_workspaces:
    description:
        - List of ML Workspaces.
    returned: always
    type: dict
    sample: [
        {
            "allow_roleassignment_on_rg": true,
            "application_insights": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.insights/components/workspacinsightsxxxxxxxx",
            "description": "Workspace Integration Tests",
            "discovery_url": "https://westus3.api.azureml.ms/discovery",
            "display_name": "workspace-xxxxxxx-xxx",
            "enable_data_isolation": false,
            "hbi_workspace": false,
            "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxx-xxx",
            "identity": {
                "principal_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "tenant_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "type": "system_assigned"
            },
            "key_vault": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.Keyvault/vaults/workspackeyvaultxxxxxxxx",
            "location": "westus3",
            "managed_network": {
                "firewall_sku": "standard",
                "isolation_mode": "allow_only_approved_outbound",
                "network_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "outbound_rules": [
                    {
                        "category": "user_defined",
                        "destination": "microsoft.com",
                        "name": "microsoft",
                        "status": "Inactive",
                        "type": "fqdn"
                    },
                    {
                        "category": "user_defined",
                        "destination": {
                            "address_prefixes": [
                                "168.63.129.16",
                                "10.0.0.0/24"
                            ],
                            "port_ranges": "80, 8080-8089",
                            "protocol": "TCP",
                            "service_tag": "sometag"
                        },
                        "name": "servicetag-w-prefixes",
                        "status": "Inactive",
                        "type": "service_tag"
                    },
                    {
                        "category": "required",
                        "destination": {
                            "address_prefixes": [],
                            "port_ranges": "443",
                            "protocol": "TCP",
                            "service_tag": "AzureMonitor"
                        },
                        "name": "__SYS_ST_AzureMonitor_TCP",
                        "status": "Inactive",
                        "type": "service_tag"
                    },
                    {
                        "category": "required",
                        "destination": {
                            "address_prefixes": [],
                            "port_ranges": "443",
                            "protocol": "TCP",
                            "service_tag": "AzureResourceManager"
                        },
                        "name": "__SYS_ST_AzureResourceManager_TCP",
                        "status": "Inactive",
                        "type": "service_tag"
                    },
                    {
                        "category": "required",
                        "destination": {
                            "service_resource_id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.Storage/storageAccounts/workspacstoragexxxxxxxxx",
                            "spark_enabled": true,
                            "subresource_target": "file"
                        },
                        "name": "__SYS_PE_workspacstoragexxxxxxxxx_file_xxxxxxxx",
                        "status": "Inactive",
                        "type": "private_endpoint"
                    },
                    {
                        "category": "required",
                        "destination": {
                            "address_prefixes": [],
                            "port_ranges": "443",
                            "protocol": "TCP",
                            "service_tag": "MicrosoftContainerRegistry.westus3"
                        },
                        "name": "__SYS_ST_MicrosoftContainerRegistry.westus3_TCP",
                        "status": "Inactive",
                        "type": "service_tag"
                    },
                    {
                        "category": "required",
                        "destination": {
                            "address_prefixes": [],
                            "port_ranges": "*",
                            "protocol": "*",
                            "service_tag": "VirtualNetwork"
                        },
                        "name": "__SYS_ST_VirtualNetwork",
                        "status": "Inactive",
                        "type": "service_tag"
                    },
                    {
                        "category": "required",
                        "destination": {
                            "address_prefixes": [],
                            "port_ranges": "443",
                            "protocol": "TCP",
                            "service_tag": "BatchNodeManagement"
                        },
                        "name": "__SYS_ST_BatchNodeManagement_TCP",
                        "status": "Inactive",
                        "type": "service_tag"
                    },
                    {
                        "category": "required",
                        "destination": {
                            "address_prefixes": [],
                            "port_ranges": "80, 443",
                            "protocol": "TCP",
                            "service_tag": "AzureActiveDirectory"
                        },
                        "name": "__SYS_ST_AzureActiveDirectory_TCP",
                        "status": "Inactive",
                        "type": "service_tag"
                    },
                    {
                        "category": "required",
                        "destination": {
                            "service_resource_id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.Storage/storageAccounts/workspacstoragexxxxxxxxx",
                            "spark_enabled": true,
                            "subresource_target": "blob"
                        },
                        "name": "__SYS_PE_workspacstoragexxxxxxxxx_blob_xxxxxxxx",
                        "status": "Inactive",
                        "type": "private_endpoint"
                    },
                    {
                        "category": "required",
                        "destination": {
                            "service_resource_id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxx-xxx",
                            "spark_enabled": true,
                            "subresource_target": "amlworkspace"
                        },
                        "name": "__SYS_PE_workspace-xxxxxxx-xxx_amlworkspace_xxxxxxxx",
                        "status": "Inactive",
                        "type": "private_endpoint"
                    },
                    {
                        "category": "required",
                        "destination": {
                            "address_prefixes": [],
                            "port_ranges": "*",
                            "protocol": "*",
                            "service_tag": "AzureFrontDoor.FirstParty"
                        },
                        "name": "__SYS_ST_AzureFrontDoor.FirstParty",
                        "status": "Inactive",
                        "type": "service_tag"
                    },
                    {
                        "category": "required",
                        "destination": {
                            "address_prefixes": [],
                            "port_ranges": "443",
                            "protocol": "TCP",
                            "service_tag": "AzureMachineLearning"
                        },
                        "name": "__SYS_ST_AzureMachineLearning_TCP",
                        "status": "Inactive",
                        "type": "service_tag"
                    },
                    {
                        "category": "required",
                        "destination": {
                            "service_resource_id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.Keyvault/vaults/workspackeyvaultxxxxxxxx",
                            "spark_enabled": true,
                            "subresource_target": "vault"
                        },
                        "name": "__SYS_PE_workspackeyvault2aa0c6bf_vault_xxxxxxxx",
                        "status": "Inactive",
                        "type": "private_endpoint"
                    },
                    {
                        "category": "required",
                        "destination": {
                            "address_prefixes": [],
                            "port_ranges": "5831",
                            "protocol": "UDP",
                            "service_tag": "AzureMachineLearning"
                        },
                        "name": "__SYS_ST_AzureMachineLearning_UDP",
                        "status": "Inactive",
                        "type": "service_tag"
                    }
                ],
                "status": {
                    "spark_ready": false,
                    "status": "Inactive"
                }
            },
            "mlflow_tracking_uri": "azureml://westus3.api.azureml.ms/mlflow/v1.0/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxx-xxx",
            "name": "workspace-xxxxxxx-xxx",
            "network_acls": {
                "default_action": "Allow",
                "ip_rules": []
            },
            "provision_network_now": false,
            "public_network_access": "Disabled",
            "resource_group": "test-ml-workspace",
            "serverless_compute": {
                "no_public_ip": false
            },
            "storage_account": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.Storage/storageAccounts/workspacstoragefxxxxxxxx",
            "system_datastores_auth_mode": "accesskey",
            "tags": {}
        }
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.constants._common import Scope
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLWorkspaceInfo(MLClientCommon):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=False
            ),
            filtered_kinds=dict(
                type='list',
                required=False,
                default=[],
                elements='str',
                choices=['default',
                         'hub',
                         'project']
            ),
            resource_group=dict(
                type='str',
                required=False
            ),
        )

        self._client = None
        self.ml_workspace = None
        self.ml_registry = None

        required_by = {'name': 'resource_group'}

        self.results = dict(
            ml_workspaces=[]
        )

        super(AzureRMMLWorkspaceInfo, self).__init__(self.module_arg_spec,
                                                     supports_tags=False,
                                                     supports_check_mode=True,
                                                     required_by=required_by,
                                                     facts_module=True,
                                                     )

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            try:
                result = self.client.workspaces.get(self.name)
                ml_workspaces = [self.entity_to_dict(result)]
            except ResourceNotFoundError:
                ml_workspaces = []
        else:
            scope = Scope.RESOURCE_GROUP if self.resource_group else Scope.SUBSCRIPTION
            results = self.client.workspaces.list(scope=scope,
                                                  filtered_kinds=','.join(self.filtered_kinds))
            ml_workspaces = list(map(self.entity_to_dict, results))

        self.results['ml_workspaces'] = ml_workspaces

        return self.results


def main():
    AzureRMMLWorkspaceInfo()


if __name__ == '__main__':
    main()
