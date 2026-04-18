#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_online_deployment_info
version_added: "3.17.0"
short_description: List ML Online Deployment resources
description:
    - List ML Online Deployment resources.
options:
    name:
        description:
            - Name of the deployment.
        type: str
        required: false
    endpoint_name:
        description:
            - Name of the endpoint.
        required: true
        type: str
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
    local:
        description:
            - List all local deployments.
        type: bool
        default: false

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get Specific ML Online Deployment by name
  azure.azcollection.azure_rm_ml_online_deployment_info:
    name: deployment-command-xxxxxxxxxx
    endpoint_name: endpoint-command-xxxxxxxxxx
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List Local ML Online Deployments
  azure.azcollection.azure_rm_ml_online_deployment_info:
    endpoint_name: endpoint-command-xxxxxxxxxx
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    local: true
'''

RETURN = '''
ml_online_deployments:
    description:
        - Online Deployments that match the query.
    returned: always
    type: dict
    sample: [
      {
          "app_insights_enabled": false,
          "code_configuration": {
              "code": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-online_deployment/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/codes/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/versions/1",
              "scoring_script": "score.py"
          },
          "creation_context": {
              "created_at": "2026-04-17T20:39:38.864149+00:00",
              "created_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
              "last_modified_at": "2026-04-17T20:39:38.864151+00:00"
          },
          "egress_public_network_access": "enabled",
          "endpoint_name": "endpoint-command-ansible",
          "environment": "azureml:/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-online_deployment/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/environments/CliV2AnonymousEnvironment/versions/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          "environment_variables": {
              "AML_APP_ROOT": "/var/azureml-app/onlinescoring",
              "AZUREML_ENTRY_SCRIPT": "score.py",
              "AZUREML_MODEL_DIR": "/var/azureml-app/azureml-models/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/1"
          },
          "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-online_deployment/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/onlineEndpoints/endpoint-command-ansible/deployments/deployment-command-xxxxxxxxxx",
          "instance_count": 1,
          "instance_type": "Standard_DS3_v2",
          "liveness_probe": {
              "failure_threshold": 30,
              "initial_delay": 10,
              "period": 10,
              "success_threshold": 1,
              "timeout": 2
          },
          "model": "azureml:/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-online_deployment/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/models/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/versions/1",
          "name": "deployment-command-e76e189747",
          "properties": {
              "AzureAsyncOperationUri": "https://management.azure.com/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.MachineLearningServices/locations/eastus/mfeOperationsStatus/odidp:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx?api-version=2023-04-01-preview"
          },
          "provisioning_state": "Succeeded",
          "readiness_probe": {
              "failure_threshold": 30,
              "initial_delay": 10,
              "period": 10,
              "success_threshold": 1,
              "timeout": 2
          },
          "request_settings": {
              "max_concurrent_requests_per_instance": 1,
              "request_timeout_ms": 5000
          },
          "scale_settings": {
              "type": "default"
          },
          "tags": {},
          "type": "managed"
      }
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLOnlineDeploymentInfo(MLClientCommon):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=False,
            ),
            endpoint_name=dict(
                type='str',
                required=True,
            ),
            resource_group=dict(
                type='str',
                required=True,
            ),
            ml_workspace=dict(
                type='str',
                required=True,
            ),
            local=dict(
                type='bool',
                default=False,
            ),
        )

        self._client = None
        self.ml_registry = None

        self.results = dict(
            ml_online_deployments=[]
        )

        super(AzureRMMLOnlineDeploymentInfo, self).__init__(self.module_arg_spec,
                                                            supports_tags=False,
                                                            supports_check_mode=True,
                                                            facts_module=True,
                                                            )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            ml_online_deployments = [self.get(self.name,
                                              endpoint_name=self.endpoint_name,
                                              local=self.local)]
        else:
            results = self.client.online_deployments.list(endpoint_name=self.endpoint_name,
                                                          local=self.local)
            ml_online_deployments = [
                self.get(x.name,
                         endpoint_name=self.endpoint_name,
                         local=self.local)
                for x in results]

        self.results['ml_online_deployments'] = ml_online_deployments
        return self.results

    def get(self, name, endpoint_name=None, local=False):
        try:
            result = self.client.online_deployments.get(name=name,
                                                        endpoint_name=endpoint_name,
                                                        local=self.local)
            ml_online_deployment = self.entity_to_dict(result)
        except ResourceNotFoundError:
            ml_online_deployment = None

        return ml_online_deployment


def main():
    AzureRMMLOnlineDeploymentInfo()


if __name__ == '__main__':
    main()
