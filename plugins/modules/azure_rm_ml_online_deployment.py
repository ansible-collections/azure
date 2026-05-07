#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_online_deployment
version_added: "3.17.0"
short_description: Create, Delete for an Azure Machine Learning Online Deployment
description:
    - Create, Delete for an Azure Machine Learning Online Deployment.
options:
    name:
        description:
            - Name of the Azure ML online_deployment.
        type: str
        required: false
    endpoint_name:
        description:
            - Name of the online endpoint. If not specified here will need to
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
            - Online Deployment definition in YAML
        type: str
        required: false
    description:
        description:
            - Description of the online_deployment.
        type: str
    local:
        description:
            - Update local deployment.
        type: bool
        default: false
    local_enable_gpu:
        description:
            - Enable GPU for local deployment.
        type: bool
        default: false
    package_model:
        description:
            - Create packaged environment from the deployment yaml
              and use the packaged environment for the deployment.
        type: bool
        default: false
    all_traffic:
        description:
            - Sets endpoint traffic 100% to this deployment
              after successful creation.
        type: bool
        default: false
    state:
        description:
            - State of the Online Deployment. Use C(present) to create
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
- name: Create ML Online Deployment
  azure.azcollection.azure_rm_ml_online_deployment:
    endpoint_name: endpoint-command-ansible
    resource_group: xxxxx-ml-online_deployment
    ml_workspace: workspace-xxxxxxxxxx
    resource_definition: |
      $schema: https://azuremlschemas.azureedge.net/latest/managedOnlineDeployment.schema.json
      name: {{ online_deployment_name }}
      model:
        path: ./targets/azure_rm_ml_online_deployment/files/model/
      code_configuration:
        code: ./targets/azure_rm_ml_online_deployment/files/onlinescoring/
        scoring_script: score.py
      environment:
        conda_file: ./targets/azure_rm_ml_online_deployment/files/environment/conda.yaml
        image: mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04:latest
      instance_type: Standard_DS3_v2
      instance_count: 1
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
ml_online_deployment:
    description:
        - Online Deployment that was just created or updated.
    returned: always
    type: dict
    sample: {
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
'''  # NOQA


try:
    import io
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_online_deployment
    from azure.ai.ml.constants._common import REGISTRY_URI_FORMAT
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLOnlineDeployment(MLClientCommon):

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
            local=dict(
                type='bool',
                default=False,
            ),
            local_enable_gpu=dict(
                type='bool',
                default=False,
            ),
            package_model=dict(
                type='bool',
                default=False,
            ),
            description=dict(
                type='str',
                required=False,
            ),
            all_traffic=dict(
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
            ml_online_deployment={}
        )

        required_if = [
            ('state', 'present', ['resource_definition']),
            ('resource_definition', None, ['name', 'endpoint_name'])
        ]

        super(AzureRMMLOnlineDeployment, self).__init__(self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        required_if=required_if,
                                                        )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False

        if self.resource_definition:
            resource_definition = io.StringIO(self.resource_definition)
            params_override = self.update_params(kwargs,
                                                 self.UPDATE_OVERRIDES)
            ml_online_deployment = load_online_deployment(
                resource_definition,
                params_override=params_override
            )
            deployment_name = ml_online_deployment.name
            endpoint_name = ml_online_deployment.endpoint_name
        else:
            deployment_name = self.name
            endpoint_name = self.endpoint_name

        ml_online_deployment_info = self.get(deployment_name,
                                             endpoint_name,
                                             local=self.local)

        if self.state == 'present':

            if ml_online_deployment_info:
                # Update
                params_override = self.update_params(kwargs,
                                                     self.UPDATE_OVERRIDES,
                                                     ml_online_deployment_info)

                if self.resource_definition:
                    resource_definition = io.StringIO(self.resource_definition)

                # Generate ml_online_deployment based on ansible args passed in.
                ml_online_deployment = load_online_deployment(
                    resource_definition,
                    params_override=params_override
                )
                ml_online_deployment_info = self.entity_to_dict(ml_online_deployment_info)
                changed = not self.default_compare(
                    {},
                    self.entity_to_dict(ml_online_deployment),
                    ml_online_deployment_info,
                    '',
                    self.results
                )
                if changed and not self.check_mode:
                    response = self.client.begin_create_or_update(
                        ml_online_deployment,
                        local=self.local,
                        local_enable_gpu=self.local_enable_gpu,
                    )
                    ml_online_deployment_object = self.get_poller_result(response)
                    ml_online_deployment_info = self.entity_to_dict(ml_online_deployment_object)
            else:
                # Create
                if isinstance(ml_online_deployment.model, str) and \
                        ml_online_deployment.model.startswith(REGISTRY_URI_FORMAT):
                    self.ml_registry = ml_online_deployment.model.split("/")[3]

                changed = True
                if not self.check_mode:
                    response = self.client.begin_create_or_update(
                        ml_online_deployment,
                        local=self.local,
                        local_enable_gpu=self.local_enable_gpu,
                        package_model=self.package_model
                    )
                    ml_online_deployment = self.get_poller_result(response)
                    ml_online_deployment_info = self.entity_to_dict(ml_online_deployment)
            if not self.check_mode and self.all_traffic:
                self._all_traffic(ml_online_deployment, local=self.local)

        elif self.state == 'absent':
            if ml_online_deployment_info:
                # Delete
                changed = True
                if not self.check_mode:
                    response = self.client.online_deployments.begin_delete(
                        name=deployment_name,
                        endpoint_name=endpoint_name,
                        local=self.local
                    )
                    ml_online_deployment_info = self.get_poller_result(response)

        self.results['ml_online_deployment'] = ml_online_deployment_info
        self.results['changed'] = changed
        return self.results

    def update_params(self, kwargs, param_overrides, ml_online_deployment=None):
        params_override = []

        # If ml_online_deployment is defined use those values as a base.
        # Update can't change some of these values but we need
        # to keep the same values as before the update.
        if ml_online_deployment:
            items = self.entity_to_dict(ml_online_deployment).items()
            params_override = [{k: v} for k, v in items]

        # Update values based on what param_overrides says we can update.
        for key in list(self.module_arg_spec.keys()):
            if kwargs[key] is not None and key in param_overrides:
                params_override.append({key: kwargs[key]})
        return params_override

    def get(self, name, endpoint_name, local=None, as_dict=False):
        try:
            # Attempt to retrieve ml_online_deployment based on name
            ml_online_deployment_info = self.client.online_deployments.get(
                name=name,
                endpoint_name=endpoint_name,
                local=local
            )
            if as_dict:
                ml_online_deployment_info = self.entity_to_dict(ml_online_deployment_info)
        except ResourceNotFoundError:
            ml_online_deployment_info = None
        return ml_online_deployment_info

    def _all_traffic(self, ml_deployment, local=False):
        endpoint = self.client.online_endpoints.get(
            ml_deployment.endpoint_name,
            local=local
        )
        endpoint.traffic = {ml_deployment.name: 100}
        response = self.client.begin_create_or_update(endpoint, local=local)
        return self.get_poller_result(response)


def main():
    AzureRMMLOnlineDeployment()


if __name__ == '__main__':
    main()
