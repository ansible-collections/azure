#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_job_info
version_added: "3.17.0"
short_description: List ML Job resources
description:
    - List ML Job resources.
options:
    name:
        description:
            - Name of the Azure ML job.
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
    parent_job_name:
        description:
            - Name of the parent job. Will list all jobs whose
              parent_job_name matches the given name.
        required: false
        type: str
    list_type:
        description:
            - Specify if you want active, archived or all jobs.
        type: str
        choices:
            - active
            - archived
            - all

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: List ML Job by name
  azure.azcollection.azure_rm_ml_job_info:
    name: jobxxxxxxxxxx
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List Archived ML Jobs
  azure.azcollection.azure_rm_ml_job_info:
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    list_type: archived
'''

RETURN = '''
ml_jobs:
    description:
        - Jobs that match the query.
    returned: always
    type: dict
    sample: [
      {
          "code": "azureml:/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-job/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/codes/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/versions/1",
          "command": "python train.py --data_dir ${{inputs.fashion_mnist}} --model_dir ${{outputs.model}}",
          "compute": "azureml:cluster-cpu",
          "creation_context": {
              "created_at": "2026-03-31T17:55:36.317328+00:00",
              "created_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
              "created_by_type": "Application"
          },
          "description": "Trains a simple neural network on the Fashion-MNIST dataset.",
          "display_name": "jobxxxxxxxxxx",
          "environment": "azureml:CliV2AnonymousEnvironment:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          "environment_variables": {},
          "experiment_name": "aml_command_cli",
          "id": "azureml:/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-job/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/jobs/jobxxxxxxxxxx",
          "inputs": {
              "fashion_mnist": {
                  "mode": "ro_mount",
                  "path": "azureml:data-fashion-mnist:1",
                  "type": "uri_folder"
              }
          },
          "name": "jobxxxxxxxxxx",
          "outputs": {
              "default": {
                  "mode": "rw_mount",
                  "path": "azureml://datastores/workspaceartifactstore/ExperimentRun/dcid.jobxxxxxxxxxx",
                  "type": "uri_folder"
              },
              "model": {
                  "mode": "rw_mount",
                  "type": "mlflow_model"
              }
          },
          "parameters": {},
          "properties": {
              "ContentSnapshotId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
              "EndTimeUtc": "2026-03-31 18:18:41",
              "ProcessInfoFile": "azureml-logs/process_info.json",
              "ProcessStatusFile": "azureml-logs/process_status.json",
              "StartTimeUtc": "2026-03-31 18:14:56",
              "_azureml.ClusterName": "cluster-cpu",
              "_azureml.ComputeTargetType": "amlctrain"
          },
          "queue_settings": {
              "job_tier": "null"
          },
          "resources": {
              "instance_count": 1,
              "properties": {},
              "shm_size": "2g"
          },
          "services": {
              "Studio": {
                  "endpoint": "https://ml.azure.com/runs/jobxxxxxxxxxx?wsid=/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/xxxxx-ml-job/workspaces/workspace-xxxxxxxxxx&tid=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                  "type": "Studio"
              },
              "Tracking": {
                  "endpoint": "azureml://eastus.api.azureml.ms/mlflow/v1.0/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-job/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx?",
                  "type": "Tracking"
              }
          },
          "status": "Completed",
          "tags": {},
          "type": "command"
      }
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLJobInfo(MLClientCommon):
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
            parent_job_name=dict(
                type='str',
                required=False,
            ),
            list_type=dict(
                type='str',
                required=False,
                choices=['archived', 'active', 'all'],
            ),
        )

        self._client = None
        self.ml_registry = None

        self.results = dict(
            ml_jobs=[]
        )

        required_one_of = [('name', 'list_type')]
        mutually_exclusive = [('name', 'list_type'),
                              ('name', 'parent_job_name')]

        super(AzureRMMLJobInfo, self).__init__(self.module_arg_spec,
                                               supports_tags=False,
                                               supports_check_mode=True,
                                               facts_module=True,
                                               required_one_of=required_one_of,
                                               mutually_exclusive=mutually_exclusive,
                                               )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            try:
                result = self.client.jobs.get(name=self.name)
                ml_jobs = [self.entity_to_dict(result)]
            except ResourceNotFoundError:
                ml_jobs = []
        else:
            list_view_type = self.get_list_view_type(self.list_type)
            results = self.client.jobs.list(parent_job_name=self.parent_job_name,
                                            list_view_type=list_view_type)
            ml_jobs = [self.entity_to_dict(self.client.jobs.get(x.name)) for x in results]

        self.results['ml_jobs'] = ml_jobs
        return self.results


def main():
    AzureRMMLJobInfo()


if __name__ == '__main__':
    main()
