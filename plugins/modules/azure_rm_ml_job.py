#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_job
version_added: "3.17.0"
short_description: Create, Cancel, Archive or Restore an Azure Machine Learning Job
description:
    - Create, Cancel, Archive or Restore an Azure Machine Learning Job.
options:
    name:
        description:
            - Name of the Azure ML job.
        type: str
        required: true
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
    resource_definition:
        description:
            - Job definition in YAML
        type: str
        required: false
    description:
        description:
            - Description of the job.
        type: str
    state:
        description:
            - State of the Job. Use C(present) to create
              or update. C(cancel) will cancel.
              C(archive) to archive, C(restore) to restore.
        default: present
        type: str
        choices:
            - present
            - cancel
            - archive
            - restore

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create ML Job
  azure.azcollection.azure_rm_ml_job:
    name: jobxxxxxxxxxx
    resource_group: xxxxx-ml-job
    ml_workspace: workspace-xxxxxxxxxx
    resource_definition: |
          $schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
          type: command
          description: Trains a simple neural network on the Fashion-MNIST dataset.
          experiment_name: "aml_command_cli"
          compute: azureml:cluster-cpu
          inputs:
            fashion_mnist:
              path: azureml:data-fashion-mnist@latest
          outputs:
            model:
              type: mlflow_model
          code: ./targets/azure_rm_ml_job/files/src
          environment:
            image: mcr.microsoft.com/azureml/openmpi5.0-ubuntu24.04:latest
            conda_file: ./targets/azure_rm_ml_job/files/conda.yml
          command: python train.py --data_dir ${{ '{{' }}inputs.fashion_mnist{{ '}}' }} --model_dir ${{ '{{' }}outputs.model{{ '}}' }}
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
ml_job:
    description:
        - Job that was just created or updated.
    returned: always
    type: dict
    sample: {
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
'''  # NOQA


try:
    import io
    import time
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_job
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLJob(MLClientCommon):

    UPDATE_OVERRIDES = []

    PARAM_OVERRIDES = UPDATE_OVERRIDES + ['name',
                                          'description',
                                          'tags']

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True,
            ),
            resource_definition=dict(
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
            description=dict(
                type='str',
                required=False,
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'cancel', 'archive', 'restore'],
            ),
        )

        self._client = None
        self.ml_registry = None
        self.state = None

        self.results = dict(
            changed=False,
            compare=[],
            ml_job={}
        )

        required_if = [
            ('state', 'present', ['resource_definition'])
        ]

        super(AzureRMMLJob, self).__init__(self.module_arg_spec,
                                           supports_check_mode=True,
                                           required_if=required_if,
                                           )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False
        ml_job_info = self.get(name=self.name)

        if self.state == 'present':
            if ml_job_info:
                # Update
                # No Updates are supported at this time.
                changed = False
                ml_job_info = self.entity_to_dict(ml_job_info)
            else:
                # Create
                params_override = self.update_params(kwargs, self.PARAM_OVERRIDES)

                # Generate ml_job based on ansible args passed in.
                resource_definition = io.StringIO(self.resource_definition)
                ml_job = load_job(source=resource_definition,
                                  params_override=params_override)

                changed = True
                if not self.check_mode:
                    response = self.client.jobs.create_or_update(job=ml_job)
                    ml_job_info = self.entity_to_dict(response)
        elif self.state == 'cancel':
            # Cancel
            if ml_job_info:
                changed = True
                if not self.check_mode:
                    self.cancel(name=self.name)
        elif self.state == 'archive':
            # Archive
            list_view_type = self.get_list_view_type('active')
            results = self.client.jobs.list(list_view_type=list_view_type)
            ml_jobs = [x.name for x in results]

            if self.name in ml_jobs:
                changed = True
                if not self.check_mode:
                    self.archive(name=self.name)
        elif self.state == 'restore':
            # Restore
            list_view_type = self.get_list_view_type('archived')
            results = self.client.jobs.list(list_view_type=list_view_type)
            ml_jobs = [x.name for x in results]

            if self.name in ml_jobs:
                changed = True
                if not self.check_mode:
                    self.restore(name=self.name)
                    # If we query too quick it hasn't fully restored.
                    # Seems the api shouldn't return until it's finished,
                    # but here we are.
                    time.sleep(1)
            ml_job_info = self.get(name=self.name,
                                   as_dict=True)

        self.results['ml_job'] = ml_job_info
        self.results['changed'] = changed
        return self.results

    def update_params(self, kwargs, param_overrides, ml_job=None):
        params_override = []

        # If ml_job is defined use those values as a base.
        # Update can't change some of these values but we need
        # to keep the same values as before the update.
        if ml_job:
            items = self.entity_to_dict(ml_job).items()
            params_override = [{k: v} for k, v in items]

        # Update values based on what param_overrides says we can update.
        for key in list(self.module_arg_spec.keys()):
            if kwargs[key] is not None and key in param_overrides:
                params_override.append({key: kwargs[key]})
        return params_override

    def get(self, name, as_dict=False):
        try:
            # Attempt to retrieve ml_job based on name
            ml_job_info = self.client.jobs.get(name=name)
            if as_dict:
                ml_job_info = self.entity_to_dict(ml_job_info)
        except ResourceNotFoundError:
            ml_job_info = None
        return ml_job_info

    def archive(self, name=None):
        try:
            self.client.jobs.archive(name=name)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error archive the job instance: {0}".format(str(e)))

    def restore(self, name=None):
        try:
            self.client.jobs.restore(name=name)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error restore the job instance: {0}".format(str(e)))

    def cancel(self, name=None):
        try:
            response = self.client.jobs.begin_cancel(name)
            ml_job_object = self.get_poller_result(response)
            return self.entity_to_dict(ml_job_object)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error cancelling  the job instance: {0}".format(str(e)))


def main():
    AzureRMMLJob()


if __name__ == '__main__':
    main()
