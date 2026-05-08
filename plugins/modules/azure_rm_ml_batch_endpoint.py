#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_batch_endpoint
version_added: "3.18.0"
short_description: Create, Delete or regenerate keys for an Azure Machine Learning Batch Endpoint
description:
    - Create, Delete or regenerate keys for an Azure Machine Learning Batch Endpoint.
options:
    name:
        description:
            - Name of the Azure ML batch_endpoint.
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
            - Batch Endpoint definition in YAML
        type: str
        required: false
    description:
        description:
            - Description of the batch_endpoint.
        type: str
    state:
        description:
            - State of the Batch Endpoint. Use C(present) to create
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
- name: Create ML Batch Endpoint
  azure.azcollection.azure_rm_ml_batch_endpoint:
    name: endpoint-xxxxxxxxxx-ansible
    resource_group: xxxxx-ml-batch_endpoint
    ml_workspace: workspace-xxxxxxxxxx
    resource_definition: |
      $schema: https://azuremlschemas.azureedge.net/latest/batchEndpoint.schema.json
      name: hello-batch
      description: A hello world endpoint for component deployments.
      auth_mode: aad_token
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
ml_batch_endpoint:
    description:
        - Batch Endpoint that was just created or updated.
    returned: always
    type: dict
    sample: {
        "auth_mode": "aad_token",
        "description": "A hello world endpoint for component deployments.",
        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-batch_endpoint_invoke/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/batchEndpoints/endpoint-xxxxxxxxxx-ansible",
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
'''  # NOQA


try:
    import io
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_batch_endpoint
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLBatchEndpoint(MLClientCommon):

    UPDATE_OVERRIDES = ['description',
                        'tags']

    PARAM_OVERRIDES = UPDATE_OVERRIDES + ['name']

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
                choices=['present', 'absent'],
            ),
        )

        self._client = None
        self.ml_registry = None
        self.state = None

        self.results = dict(
            changed=False,
            compare=[],
            ml_batch_endpoint={}
        )

        required_if = [
            ('state', 'present', ['resource_definition'])
        ]

        super(AzureRMMLBatchEndpoint, self).__init__(self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     required_if=required_if,
                                                     )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False

        ml_batch_endpoint_info = self.get(name=self.name)

        if self.state == 'present':
            if self.resource_definition:
                resource_definition = io.StringIO(self.resource_definition)

            if ml_batch_endpoint_info:
                # Update
                params_override = self.update_params(kwargs,
                                                     self.UPDATE_OVERRIDES,
                                                     ml_batch_endpoint_info)

                # Generate ml_batch_endpoint based on ansible args passed in.
                ml_batch_endpoint = load_batch_endpoint(resource_definition,
                                                        params_override=params_override)
                ml_batch_endpoint_info = self.entity_to_dict(ml_batch_endpoint_info)
                changed = not self.default_compare({},
                                                   self.entity_to_dict(ml_batch_endpoint),
                                                   ml_batch_endpoint_info,
                                                   '',
                                                   self.results)
                if changed and not self.check_mode:
                    response = self.client.begin_create_or_update(ml_batch_endpoint)
                    ml_batch_endpoint_object = self.get_poller_result(response)
                    ml_batch_endpoint_info = self.entity_to_dict(ml_batch_endpoint_object)
            else:
                # Create
                params_override = self.update_params(kwargs, self.PARAM_OVERRIDES)

                # Generate ml_batch_endpoint based on ansible args passed in.
                ml_batch_endpoint = load_batch_endpoint(source=resource_definition,
                                                        params_override=params_override)

                changed = True
                if not self.check_mode:
                    response = self.client.begin_create_or_update(ml_batch_endpoint)
                    ml_batch_endpoint_object = self.get_poller_result(response)
                    ml_batch_endpoint_info = self.entity_to_dict(ml_batch_endpoint_object)
        elif self.state == 'absent':
            if ml_batch_endpoint_info:
                # Delete
                changed = True
                if not self.check_mode:
                    response = self.client.batch_endpoints.begin_delete(name=self.name)
                    ml_batch_endpoint_info = self.get_poller_result(response)

        self.results['ml_batch_endpoint'] = ml_batch_endpoint_info
        self.results['changed'] = changed
        return self.results

    def update_params(self, kwargs, param_overrides, ml_batch_endpoint=None):
        params_override = []

        # If ml_batch_endpoint is defined use those values as a base.
        # Update can't change some of these values but we need
        # to keep the same values as before the update.
        if ml_batch_endpoint:
            items = self.entity_to_dict(ml_batch_endpoint).items()
            params_override = [{k: v} for k, v in items]

        # Update values based on what param_overrides says we can update.
        for key in list(self.module_arg_spec.keys()):
            if kwargs[key] is not None and key in param_overrides:
                params_override.append({key: kwargs[key]})
        return params_override

    def get(self, name, as_dict=False):
        try:
            # Attempt to retrieve ml_batch_endpoint based on name
            ml_batch_endpoint_info = self.client.batch_endpoints.get(name=name)
            if as_dict:
                ml_batch_endpoint_info = self.entity_to_dict(ml_batch_endpoint_info)
        except ResourceNotFoundError:
            ml_batch_endpoint_info = None
        return ml_batch_endpoint_info


def main():
    AzureRMMLBatchEndpoint()


if __name__ == '__main__':
    main()
