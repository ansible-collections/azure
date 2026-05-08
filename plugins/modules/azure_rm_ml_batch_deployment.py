#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_batch_deployment
version_added: "3.18.0"
short_description: Create, Delete for an Azure Machine Learning Batch Deployment
description:
    - Create, Delete for an Azure Machine Learning Batch Deployment.
options:
    name:
        description:
            - Name of the Azure ML batch_deployment.
        type: str
        required: false
    endpoint_name:
        description:
            - Name of the batch endpoint. If not specified here will need to
              be referenced in the I(resource_definition).
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
    resource_definition:
        description:
            - Batch Deployment definition in YAML
        type: str
        required: false
    description:
        description:
            - Description of the batch_deployment.
        type: str
    set_default:
        description:
            - Sets endpoint defaults.deployment_name to this deployment
              after successful creation.
        type: bool
        default: false
    state:
        description:
            - State of the Batch Deployment. Use C(present) to create
              or update.
        default: present
        type: str
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create ML Batch Deployment
  azure.azcollection.azure_rm_ml_batch_deployment:
    endpoint_name: endpoint-command-ansible
    resource_group: xxxxx-ml-batch_deployment
    ml_workspace: workspace-xxxxxxxxxx
    resource_definition: |
      $schema: https://azuremlschemas.azureedge.net/latest/pipelineComponentBatchDeployment.schema.json
      name: {{ batch_deployment_name }}
      endpoint_name: hello-pipeline-batch
      type: pipeline
      component: azureml:hello_batch@latest
      settings:
          default_compute: batch-cluster
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
ml_batch_deployment:
    description:
        - Batch Deployment that was just created or updated.
    returned: always
    type: dict
    sample: {
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
'''  # NOQA


try:
    import io
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.exceptions import ValidationException
    from azure.ai.ml.entities._load_functions import load_batch_deployment
    from azure.ai.ml.entities._load_functions import (
        load_batch_deployment, _try_load_yaml_dict,
        load_pipeline_component_batch_deployment,
        load_model_batch_deployment
    )
    from azure.ai.ml.constants._deployment import BatchDeploymentType
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLBatchDeployment(MLClientCommon):

    UPDATE_OVERRIDES = ['description',
                        'tags',
                        'endpoint_name']

    PARAM_OVERRIDES = UPDATE_OVERRIDES + ['name']

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=False,
            ),
            endpoint_name=dict(
                type='str',
                required=False,
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
            set_default=dict(
                type='bool',
                default=False,
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent'],
            ),
        )

        self._client = None
        self.ml_registry = None
        self.state = None

        self.results = dict(
            changed=False,
            compare=[],
            ml_batch_deployment={}
        )

        required_if = [
            ('state', 'present', ['resource_definition']),
            ('resource_definition', None, ['name', 'endpoint_name'])
        ]

        super(AzureRMMLBatchDeployment, self).__init__(self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       required_if=required_if,
                                                       )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False

        # Process resource_file yaml and passed in parameters
        try:
            resource_definition = io.StringIO(self.resource_definition)
            yaml_dict = _try_load_yaml_dict(resource_definition)
        except ValidationException:
            yaml_dict = dict()
        deployment_name = self.name or yaml_dict.get('name', None)
        endpoint_name = self.endpoint_name or yaml_dict.get('endpoint_name', None)

        ml_batch_deployment_info = self.get(deployment_name,
                                            endpoint_name)

        if self.state == 'present':

            if ml_batch_deployment_info:
                # Update
                resource_definition = io.StringIO(self.resource_definition)
                params_override = self.update_params(
                    kwargs,
                    self.UPDATE_OVERRIDES,
                    ml_batch_deployment=ml_batch_deployment_info
                )
                ml_batch_deployment = self.get_model(yaml_dict,
                                                     resource_definition,
                                                     params_override)

                orig_deployment_info = self.entity_to_dict(ml_batch_deployment_info)
                orig_deployment_info.pop('creation_context')
                if not self.check_mode:
                    # If requested make this deployment the default for the endpoint
                    endpoint_changed = False
                    if self.set_default:
                        endpoint = self.client.batch_endpoints.get(
                            ml_batch_deployment.endpoint_name
                        )
                        if endpoint.defaults.deployment_name != ml_batch_deployment.name:

                            endpoint.defaults = {"deployment_name": ml_batch_deployment.name}
                            endpoint = self.client.begin_create_or_update(entity=endpoint)
                            endpoint = self.get_poller_result(endpoint)
                            endpoint_changed = True
                    response = self.client.begin_create_or_update(
                        entity=ml_batch_deployment
                    )
                    ml_batch_deployment_object = self.get_poller_result(response)
                    ml_batch_deployment_info = self.entity_to_dict(ml_batch_deployment_object)
                    new_deployment_info = self.entity_to_dict(
                        self.get(deployment_name, endpoint_name)
                    )
                    new_deployment_info.pop('creation_context')
                    changed = not self.default_compare(
                        {},
                        new_deployment_info,
                        orig_deployment_info,
                        '',
                        self.results
                    )
                    # We flag as changed on either endpoint default or deployment
                    changed = changed or endpoint_changed
            else:
                # Create
                params_override = self.update_params(kwargs,
                                                     self.PARAM_OVERRIDES)
                resource_definition = io.StringIO(self.resource_definition)

                ml_batch_deployment = self.get_model(yaml_dict,
                                                     resource_definition,
                                                     params_override)
                changed = True
                if not self.check_mode:
                    response = self.client.begin_create_or_update(
                        entity=ml_batch_deployment
                    )
                    ml_batch_deployment = self.get_poller_result(response)
                    ml_batch_deployment_info = self.entity_to_dict(ml_batch_deployment)
                    # If requested make this deployment the default for the endpoint
                    if self.set_default:
                        endpoint = self.client.batch_endpoints.get(
                            ml_batch_deployment.endpoint_name
                        )
                        endpoint.defaults = {"deployment_name": ml_batch_deployment.name}
                        endpoint = self.client.begin_create_or_update(entity=endpoint)
                        endpoint = self.get_poller_result(endpoint)
        elif self.state == 'absent':
            if ml_batch_deployment_info:
                # Delete
                changed = True
                if not self.check_mode:
                    response = self.client.batch_deployments.begin_delete(
                        name=deployment_name,
                        endpoint_name=endpoint_name
                    )
                    ml_batch_deployment_info = self.get_poller_result(response)

        self.results['ml_batch_deployment'] = ml_batch_deployment_info
        self.results['changed'] = changed
        return self.results

    def update_params(self, kwargs, param_overrides, ml_batch_deployment=None):
        params_override = []

        skip_params = ["creation_context", "properties", "id", "output_action",
                       "retry_settings", "resources", "error_threshold",
                       "provisioning_state", "environment_variables",
                       "mini_batch_size", "logging_level",
                       "max_concurrency_per_instance"]

        # If ml_batch_deployment is defined use those values as a base.
        # Update can't change some of these values but we need
        # to keep the same values as before the update.
        if ml_batch_deployment:
            items = ml_batch_deployment._to_dict().items()
            params_override = [{k: v} for k, v in items if k not in skip_params]

        # Update values based on what param_overrides says we can update.
        for key in list(self.module_arg_spec.keys()):
            if kwargs[key] is not None and key in param_overrides:
                params_override.append({key: kwargs[key]})
        return params_override

    def get(self, name, endpoint_name, as_dict=False):
        try:
            # Attempt to retrieve ml_batch_deployment based on name
            ml_batch_deployment_info = self.client.batch_deployments.get(
                name=name,
                endpoint_name=endpoint_name
            )
            if as_dict:
                ml_batch_deployment_info = self.entity_to_dict(ml_batch_deployment_info)
        except ResourceNotFoundError:
            ml_batch_deployment_info = None
        return ml_batch_deployment_info

    def get_model(self, yaml_dict, resource_definition, params_override):
        if yaml_dict.get('type') == BatchDeploymentType.MODEL:
            ml_batch_deployment = load_model_batch_deployment(
                source=resource_definition,
                params_override=params_override
            )
        elif yaml_dict.get('type') == BatchDeploymentType.PIPELINE:
            ml_batch_deployment = load_pipeline_component_batch_deployment(
                source=resource_definition,
                params_override=params_override
            )
        else:
            ml_batch_deployment = load_batch_deployment(
                source=resource_definition,
                params_override=params_override
            )
        return ml_batch_deployment


def main():
    AzureRMMLBatchDeployment()


if __name__ == '__main__':
    main()
