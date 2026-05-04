#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_batch_endpoint_info
version_added: "3.18.0"
short_description: List ML Batch Endpoint resources
description:
    - List ML Batch Endpoint resources.
options:
    name:
        description:
            - Name of the Azure ML batch endpoint.
        type: str
        required: false
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
- name: Get Specific ML Batch Endpoint by name
  azure.azcollection.azure_rm_ml_batch_endpoint_info:
    name: endpoint-command-xxxxxxxxxx
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List ML Batch Endpoints
  azure.azcollection.azure_rm_ml_batch_endpoint_info:
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
'''

RETURN = '''
ml_batch_endpoints:
    description:
        - Batch Endpoints that match the query.
    returned: always
    type: dict
    sample: [
      {
          "auth_mode": "aad_token",
          "defaults": {
              "deployment_name": "deployment-xxxxxxxxxx-ansible"
          },
          "description": "A hello world endpoint for component deployments.",
          "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-batch_endpoint_invoke/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/batchEndpoints/endpoint-xxxxxxxxxx-ansible",
          "jobs": [
              {
                  "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-batch_endpoint_invoke/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/batchEndpoints/endpoint-xxxxxxxxxx-ansible/deployments/deployment-xxxxxxxxxx-ansible/jobs/pipelinejob-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                  "name": "pipelinejob-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                  "properties": {
                      "compute": {
                          "is_local": false
                      },
                      "interaction_endpoints": {
                          "Studio": {
                              "endpoint": "https://ml.azure.com/runs/pipelinejob-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx?wsid=/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/xxxxx-ml-batch_endpoint_invoke/workspaces/workspace-xxxxxxxxxx",
                              "job_endpoint_type": "Studio"
                          },
                          "Tracking": {
                              "endpoint": "azureml://eastus.api.azureml.ms/mlflow/v1.0/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-batch_endpoint_invoke/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx?",
                              "job_endpoint_type": "Tracking"
                          }
                      },
                      "name": "honest_grape_xxxxxxxx",
                      "output": {
                          "datastore_id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-batch_endpoint_invoke/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/datastores/workspaceartifactstore",
                          "path": "ExperimentRun/dcid.xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                      },
                      "output_data": {
                          "score": {
                              "job_output_type": "UriFile",
                              "mode": "ReadWriteMount",
                              "uri": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-batch_endpoint_invoke/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/datastores/workspaceblobstore/paths/azureml/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/score/predictions.csv"
                          }
                      },
                      "properties": {
                          "azureml.DatasetAccessMode": "Asset",
                          "azureml.DevPlatv2": "true",
                          "azureml.SourceComponentId": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-batch_endpoint_invoke/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/components/hello_batch/versions/1",
                          "azureml.continue_on_failed_optional_input": "True",
                          "azureml.continue_on_step_failure": "True",
                          "azureml.defaultComputeName": "batch-cluster",
                          "azureml.defaultDataStoreName": "workspaceblobstore",
                          "azureml.deploymentname": "deployment-xxxxxxxxxx-ansible",
                          "azureml.endpointname": "endpoint-xxxxxxxxxx-ansible",
                          "azureml.enforceRerun": "False",
                          "azureml.parameters": "{}",
                          "azureml.pipelineComponent": "pipelinerun",
                          "azureml.pipelines.stages": "{\\"Initialization\\":null,\\"Execution\\":{\\"StartTime\\":\\"2026-05-04T13:51:04.3564364+00:00\\",\\"EndTime\\":\\"2026-05-04T13:55:32.6682006+00:00\\",\\"Status\\":\\"Finished\\"}}",
                          "azureml.runLineageType": "batchDeployment",
                          "azureml.runsource": "azureml.PipelineRun",
                          "azureml.sourcepipelinerunid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                          "runSource": "BatchDeployment",
                          "runType": "HTTP"
                      },
                      "provisioning_state": "Succeeded",
                      "status": "Completed",
                      "tags": {
                          "azureml.batchrun": "true",
                          "azureml.deploymentname": "deployment-xxxxxxxxxx-ansible",
                          "azureml.jobtype": "azureml.pipelinejob"
                      }
                  },
                  "system_data": {
                      "created_at": "2026-05-04T13:51:03.171352Z",
                      "created_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                      "last_modified_at": "2026-05-04T13:55:32.837426Z",
                      "last_modified_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                  },
                  "type": "Microsoft.MachineLearningServices/workspaces/batchEndpoints/deployments/jobs"
              }
          ],
          "location": "eastus",
          "name": "endpoint-xxxxxxxxxx-ansible",
          "properties": {
              "BatchEndpointCreationApiVersion": "2023-10-01",
              "azureml.onlineendpointid": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-batch_endpoint_invoke/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/batchEndpoints/endpoint-xxxxxxxxxx-ansible"
          },
          "provisioning_state": "Succeeded",
          "scoring_uri": "https://endpoint-xxxxxxxxxx-ansible.eastus.inference.ml.azure.com/jobs",
          "tags": {}
      }
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLBatchEndpointInfo(MLClientCommon):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=False,
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
            ml_batch_endpoints=[]
        )

        super(AzureRMMLBatchEndpointInfo, self).__init__(self.module_arg_spec,
                                                         supports_tags=False,
                                                         supports_check_mode=True,
                                                         facts_module=True,
                                                         )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            ml_batch_endpoints = [self.get(self.name)]
        else:
            results = self.client.batch_endpoints.list()
            ml_batch_endpoints = [self.get(x.name) for x in results]

        self.results['ml_batch_endpoints'] = ml_batch_endpoints
        return self.results

    def get(self, name):
        try:
            result = self.client.batch_endpoints.get(name=name)
            ml_batch_endpoint = self.entity_to_dict(result)
            jobs = [self.entity_to_dict(x) for x in self.client.batch_endpoints.list_jobs(endpoint_name=name)]
            ml_batch_endpoint['jobs'] = jobs
        except ResourceNotFoundError:
            ml_batch_endpoint = None

        return ml_batch_endpoint


def main():
    AzureRMMLBatchEndpointInfo()


if __name__ == '__main__':
    main()
