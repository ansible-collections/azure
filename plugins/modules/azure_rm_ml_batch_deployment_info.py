#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_batch_deployment_info
version_added: "3.18.0"
short_description: List ML Batch Deployment resources
description:
    - List ML Batch Deployment resources.
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

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get Specific ML Batch Deployment by name
  azure.azcollection.azure_rm_ml_batch_deployment_info:
    name: deployment-command-xxxxxxxxxx
    endpoint_name: endpoint-command-xxxxxxxxxx
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List ML Batch Deployments
  azure.azcollection.azure_rm_ml_batch_deployment_info:
    endpoint_name: endpoint-command-xxxxxxxxxx
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
'''

RETURN = '''
ml_batch_deployments:
    description:
        - Batch Deployments that match the query.
    returned: always
    type: dict
    sample: [
      {
          "creation_context": {
              "created_at": "2026-04-24T15:39:01.058441+00:00",
              "created_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
              "last_modified_at": "2026-04-24T15:39:01.058431+00:00"
          },
          "endpoint_name": "endpoint-command-ansible",
          "environment_variables": {},
          "error_threshold": 0,
          "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-batch_deployment/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/batchEndpoints/endpoint-command-ansible/deployments/deployment-command-xxxxxxxxxx",
          "jobs": [],
          "logging_level": "Info",
          "max_concurrency_per_instance": 0,
          "mini_batch_size": 0,
          "name": "deployment-command-xxxxxxxxxx",
          "output_action": "summary_only",
          "properties": {
              "componentDeployment.Settings.continue_on_step_failure": null,
              "default_compute": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-batch_deployment/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/computes/batch-cluster",
              "default_datastore": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-batch_deployment/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/datastores/workspaceblobstore",
              "deployment_configuration_type": "PipelineComponent"
          },
          "provisioning_state": "Succeeded",
          "resources": {
              "instance_count": 1,
              "properties": {}
          },
          "retry_settings": {
              "max_retries": 0,
              "timeout": 0
          },
          "tags": {
              "PipelineDeployment.ComponentId": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-batch_deployment/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/components/hello_batch/versions/1"
          }
      }
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLBatchDeploymentInfo(MLClientCommon):
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
        )

        self._client = None
        self.ml_registry = None

        self.results = dict(
            ml_batch_deployments=[]
        )

        super(AzureRMMLBatchDeploymentInfo, self).__init__(self.module_arg_spec,
                                                           supports_tags=False,
                                                           supports_check_mode=True,
                                                           facts_module=True,
                                                           )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            ml_batch_deployments = [self.get(self.name,
                                             endpoint_name=self.endpoint_name)]
        else:
            results = self.client.batch_deployments.list(endpoint_name=self.endpoint_name)
            ml_batch_deployments = [
                self.get(x.name,
                         endpoint_name=self.endpoint_name)
                for x in results]

        self.results['ml_batch_deployments'] = ml_batch_deployments
        return self.results

    def get(self, name, endpoint_name=None):
        try:
            result = self.client.batch_deployments.get(name=name,
                                                       endpoint_name=endpoint_name)
            ml_batch_deployment = self.entity_to_dict(result)
            results = self.client.batch_deployments.list_jobs(
                name=name,
                endpoint_name=endpoint_name
            )
            ml_batch_deployment['jobs'] = [self.entity_to_dict(deployment)
                                           for deployment in results]
        except ResourceNotFoundError:
            ml_batch_deployment = None

        return ml_batch_deployment


def main():
    AzureRMMLBatchDeploymentInfo()


if __name__ == '__main__':
    main()
