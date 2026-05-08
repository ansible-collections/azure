#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_batch_endpoint_invoke
version_added: "3.18.0"
short_description: Invoke ML Batch Endpoint resources
description:
    - Invoke ML Batch Endpoint resources.
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
    invocation_definition:
        description:
            - Batch Endpoint Invocations definition in YAML.
        required: false
        type: str
    deployment_name:
        description:
            - Name of the deployment to target.
        required: false
        type: str
    experiment_name:
        description:
            - Name of the experiment for pipeline component deployment.
        required: false
        type: str
    input:
        description:
            - Reference to input data to use for batch inferencing.
              It can be a path on the datastore, public URI, a registered
              data asset, or a local folder path.
        required: false
        type: str
    input_type:
        description:
            - Type of the input, specifying whether it's a file or a folder.
              Use this when you are using a path on datastore or public URI.
        required: false
        type: str
        choices:
            - uri_folder
            - uri_file
    inputs:
        description:
            - Dictionary of Inputs of invoke jobs.
        required: false
        type: dict
    instance_count:
        description:
            - Number of instances the prediction will run on.
        required: false
        type: int
    job_name:
        description:
            - Name of the job for batch invoke.
        required: false
        type: str
    mini_batch_size:
        description:
            - Size of each mini batch that the input data will be split into
              for prediction.
        required: false
        type: int
    output_path:
        description:
            - Path on the datastore where output files will be uploaded to.
        required: false
        type: str
    outputs:
        description:
            - Dictionary to specify where to store the results.
        required: false
        type: dict

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Invoke ML Batch Endpoint
  azure.azcollection.azure_rm_ml_batch_endpoint_invoke:
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
'''

RETURN = '''
changed:
    description:
        - Will return True if successfully invoked
    returned: always
    type: bool
    sample: true
ml_batch_endpoint_invoke:
    description:
        - Batch Endpoints that match the query.
    returned: always
    type: dict
    sample: {
        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-batch_endpoint_invoke/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/batchEndpoints//jobs/pipelinejob-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "name": "pipelinejob-xxxxxxxx-xxxx-xxxxxxxxx-xxxxxxxxxxxx",
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
            "name": "bold_egg_xxxxxxxx",
            "output": {},
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
                "azureml.runLineageType": "batchDeployment",
                "azureml.runsource": "azureml.PipelineRun",
                "azureml.sourcepipelinerunid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "runSource": "BatchDeployment",
                "runType": "HTTP"
            },
            "provisioning_state": "Succeeded",
            "status": "Preparing",
            "tags": {
                "azureml.batchrun": "true",
                "azureml.deploymentname": "deployment-xxxxxxxxxx-ansible",
                "azureml.jobtype": "azureml.pipelinejob"
            }
        },
        "system_data": {
            "created_at": "2026-05-04T13:56:02.890323Z",
            "created_by": "xxxx xxxx-xxxxxxxxxx",
            "last_modified_at": "2026-05-04T13:56:02.890323Z",
            "last_modified_by": "xxxx xxxx-xxxxxxxxxx"
        },
        "type": "Microsoft.MachineLearningServices/workspaces/batchEndpoints/jobs"
    }
'''  # NOQA


try:
    import io
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.constants._endpoint import BatchEndpointInvoke, EndpointYamlFields
    from azure.ai.ml.constants._common import ARM_ID_PREFIX, AssetTypes, InputTypes
    from azure.ai.ml.entities._inputs_outputs import Input, Output
    from azure.ai.ml.entities._load_functions import _try_load_yaml_dict
    from azure.ai.ml._utils._arm_id_utils import parse_name_version, remove_aml_prefix
    from azure.ai.ml._utils._storage_utils import AzureMLDatastorePathUri
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLBatchEndpointInvoke(MLClientCommon):
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
            invocation_definition=dict(
                type='str',
                required=False,
            ),
            deployment_name=dict(
                type='str',
                required=False,
            ),
            experiment_name=dict(
                type='str',
                required=False,
            ),
            input=dict(
                type='str',
                required=False,
            ),
            input_type=dict(
                type='str',
                required=False,
                choices=['uri_folder', 'uri_file'],
            ),
            inputs=dict(
                type='dict',
                required=False,
            ),
            instance_count=dict(
                type='int',
                required=False,
            ),
            job_name=dict(
                type='str',
                required=False,
            ),
            mini_batch_size=dict(
                type='int',
                required=False,
            ),
            output_path=dict(
                type='str',
                required=False,
            ),
            outputs=dict(
                type='dict',
                required=False,
            ),
        )

        self._client = None
        self.ml_registry = None

        self.results = dict(
            ml_batch_endpoint_invoke=None,
            changed=False,
        )

        required_if = [
            ('invocation_definition', None, ['name'])
        ]

        super(AzureRMMLBatchEndpointInvoke, self).__init__(self.module_arg_spec,
                                                           supports_tags=False,
                                                           supports_check_mode=False,
                                                           facts_module=True,
                                                           required_if=required_if,
                                                           )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        params_override = []
        input = None
        inputs = None
        outputs = None

        try:
            if self.deployment_name:
                self.client.batch_endpoints._validate_deployment_name(
                    self.name, self.deployment_name
                )

            if self.invocation_definition:
                invocation_definition = io.StringIO(self.invocation_definition)
                batch_endpoint_invocation = _try_load_yaml_dict(invocation_definition)

                inputs_dict = batch_endpoint_invocation.get(BatchEndpointInvoke.INPUTS)
                if inputs_dict:
                    inputs = _parse_inputs(inputs_dict)
                outputs_dict = batch_endpoint_invocation.get(BatchEndpointInvoke.OUTPUTS)
                if outputs_dict:
                    outputs = {}
                    for key, data in outputs_dict.items():
                        output = Output(
                            type=data.get(BatchEndpointInvoke.TYPE),
                            path=data.get(BatchEndpointInvoke.PATH),
                            mode=data.get(BatchEndpointInvoke.MODE),
                        )
                        outputs[key] = output
                if not self.deployment_name:
                    self.deployment_name = batch_endpoint_invocation.get(BatchEndpointInvoke.DEPLOYMENT)
                if not self.name:
                    self.name = batch_endpoint_invocation.get(BatchEndpointInvoke.ENDPOINT)
            elif self.input or self.input_type:
                if self.input and not self.input_type:
                    if self.input.startswith(ARM_ID_PREFIX):  # azureml:data:version
                        self.input = remove_aml_prefix(self.input)
                        asset_name, asset_version = parse_name_version(self.input)
                        try:
                            data = self.client.data.get(asset_name, asset_version)
                            # invoke input should be of type Input based on the data type
                            if data.type == AssetTypes.URI_FOLDER:
                                input = Input(type=AssetTypes.URI_FOLDER, path=data.id)
                            elif data.type == AssetTypes.URI_FILE:
                                input = Input(type=AssetTypes.URI_FILE, path=data.id)
                        except ResourceNotFoundError:
                            # We have a case that the input is not a registered data asset
                            self.fail(
                                "Value passed to input is not a supported data. "
                                "Please use an Azure Machine Learning registered V2 data asset "
                                "(with the type of either `uri_file` or `uri_folder`). Refer to how-to guide for "
                                "batch endpoint for more information on supported input data types."
                            )
                    else:  # ./path
                        input = Input(type=AssetTypes.URI_FOLDER, path=self.input)
                elif self.input_type == AssetTypes.URI_FOLDER:
                    input = Input(type=AssetTypes.URI_FOLDER, path=self.input)
                elif self.input_type == AssetTypes.URI_FILE:
                    input = Input(type=AssetTypes.URI_FILE, path=self.input)
                else:
                    self.fail(
                        "Unsupported input please use either a path on the datastore, "
                        "public URI, a registered data asset, or a local folder path."
                    )
            properties = {}
            if self.mini_batch_size:
                params_override.append({EndpointYamlFields.MINI_BATCH_SIZE: self.mini_batch_size})
            if self.instance_count:
                params_override.append({EndpointYamlFields.BATCH_JOB_INSTANCE_COUNT: self.instance_count})
            if self.output_path:
                try:
                    output = validate_and_split_output_path(self.output_path)
                except ValueError as err:
                    self.fail(err)
                params_override.append(
                    {EndpointYamlFields.BATCH_JOB_OUTPUT_PATH: output.path}
                )
                params_override.append(
                    {EndpointYamlFields.BATCH_JOB_OUTPUT_DATSTORE: "azureml:" + output.datastore}
                )
            if self.job_name:
                params_override.append(
                    {EndpointYamlFields.BATCH_JOB_NAME: self.job_name}
                )
            if self.experiment_name:
                properties["experimentName"] = self.experiment_name
            if properties:
                params_override.append(
                    {EndpointYamlFields.BATCH_JOB_PROPERTIES: properties}
                )
            if self.inputs:
                inputs = _parse_inputs(self.inputs)
            if self.outputs:
                outputs = {}
                for key, data in self.outputs.items():
                    output = Output(
                        type=data.get(BatchEndpointInvoke.TYPE),
                        path=data.get(BatchEndpointInvoke.PATH),
                        mode=data.get(BatchEndpointInvoke.MODE),
                    )
                    outputs[key] = output

            ml_batch_endpoint_invoke = self.client.batch_endpoints.invoke(
                endpoint_name=self.name,
                input=input,
                inputs=inputs,
                outputs=outputs,
                deployment_name=self.deployment_name,
                params_override=params_override,
            )

        except Exception as err:
            if isinstance(err, ResourceNotFoundError) and self.deployment_name is None:
                self.fail("Set a default deployment or provide a deployment name.")
            else:
                self.fail(err)

        self.results['ml_batch_endpoint_invoke'] = self.entity_to_dict(
            ml_batch_endpoint_invoke
        )
        self.results['changed'] = True
        return self.results

    def get(self, name):
        try:
            result = self.client.batch_endpoints.get(name=name)
            ml_batch_endpoint = self.entity_to_dict(result)
            jobs = self.client.batch_endpoints.list_jobs(endpoint_name=name)
            ml_batch_endpoint['jobs'] = jobs
        except ResourceNotFoundError:
            ml_batch_endpoint = None

        return ml_batch_endpoint


def _parse_inputs(inputs_dict):
    inputs = {}
    if inputs_dict:
        for key, data in inputs_dict.items():
            if isinstance(data, str):
                inputs[key] = Input(type=InputTypes.STRING, default=data)
            elif isinstance(data, bool):
                inputs[key] = Input(type=InputTypes.BOOLEAN, default=data)
            elif isinstance(data, int):
                inputs[key] = Input(type=InputTypes.INTEGER, default=data)
            elif isinstance(data, float):
                inputs[key] = Input(type=InputTypes.NUMBER, default=data)
            else:
                if data.get(BatchEndpointInvoke.TYPE) in [InputTypes.NUMBER, InputTypes.INTEGER]:
                    inputs[key] = Input(
                        type=data.get(BatchEndpointInvoke.TYPE, None),
                        default=data.get(BatchEndpointInvoke.DEFAULT, None),
                        min=data.get(BatchEndpointInvoke.MIN, None),
                        max=data.get(BatchEndpointInvoke.MAX, None),
                    )
                elif data.get(BatchEndpointInvoke.TYPE) in [InputTypes.STRING, InputTypes.BOOLEAN]:
                    inputs[key] = Input(
                        type=data.get(BatchEndpointInvoke.TYPE, None),
                        default=data.get(BatchEndpointInvoke.DEFAULT, None),
                    )
                else:
                    inputs[key] = Input(
                        type=data.get(BatchEndpointInvoke.TYPE, None),
                        path=data.get(BatchEndpointInvoke.PATH, None),
                        mode=data.get(BatchEndpointInvoke.MODE, None),
                    )
    return inputs


def validate_and_split_output_path(output_path):
    if output_path.startswith(ARM_ID_PREFIX):
        datastore_path = AzureMLDatastorePathUri(output_path)
        return datastore_path
    raise ValueError("Not a valid output_path, it should start with 'azureml:'")


def main():
    AzureRMMLBatchEndpointInvoke()


if __name__ == '__main__':
    main()
