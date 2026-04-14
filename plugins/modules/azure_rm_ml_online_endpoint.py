#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_online_endpoint
version_added: "3.17.0"
short_description: Create, Delete or regenerate keys for an Azure Machine Learning Online Endpoint
description:
    - Create, Delete or regenerate keys for an Azure Machine Learning Online Endpoint.
options:
    name:
        description:
            - Name of the Azure ML online_endpoint.
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
            - Online Endpoint definition in YAML
        type: str
        required: false
    description:
        description:
            - Description of the online_endpoint.
        type: str
    local:
        description:
            - Update local endpoint.
        type: bool
        default: false
    auth_mode:
        description:
            - Authentication method for the endpoint.
        default: key
        type: str
        choices:
            - key
            - aml_token
    mirror_traffic:
        description:
            - Key and Numeric value to Direct a duplicate percentage
              of live traffic to a train a deployment.
        required: false
        type: dict
    traffic:
        description:
            - Key and Numeric value for traffic settings of this endpoint.
        required: false
        type: dict
    key_type:
        description:
            - The type of key to regenerate.
        type: str
        default: primary
        choices:
            - primary
            - secondary
    state:
        description:
            - State of the Online Endpoint. Use C(present) to create
              or update. C(regenerate_keys) to regenerate keys.
        default: present
        type: str
        choices:
            - present
            - absent
            - regenerate_keys

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create ML Online Endpoint
  azure.azcollection.azure_rm_ml_online_endpoint:
    name: onlineendpointxxxxxxxxxx
    resource_group: xxxxx-ml-online_endpoint
    ml_workspace: workspace-xxxxxxxxxx
    resource_definition: |
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
ml_online_endpoint:
    description:
        - Online Endpoint that was just created or updated.
    returned: always
    type: dict
    sample: {
      "auth_mode": "key",
      "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-online_endpoint/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/onlineEndpoints/endpoint-command-xxxxxxxxxx",
      "identity": {
          "principal_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "tenant_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "type": "system_assigned"
      },
      "kind": "Managed",
      "location": "eastus",
      "mirror_traffic": {},
      "name": "endpoint-command-xxxxxxxxxx",
      "openapi_uri": "https://endpoint-command-xxxxxxxxxx.eastus.inference.ml.azure.com/swagger.json",
      "properties": {
          "AzureAsyncOperationUri": "https://management.azure.com/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.MachineLearningServices/locations/eastus/mfeOperationsStatus/oeidp:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx?api-version=2022-02-01-preview",
          "azureml.onlineendpointid": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/xxxxx-ml-online_endpoint/providers/microsoft.machinelearningservices/workspaces/workspace-xxxxxxxxxx/onlineendpoints/endpoint-command-xxxxxxxxxx",
          "createdAt": "2026-04-09T15:04:48.831114+0000",
          "createdBy": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "lastModifiedAt": "2026-04-09T15:04:48.831114+0000"
      },
      "provisioning_state": "Succeeded",
      "public_network_access": "enabled",
      "scoring_uri": "https://endpoint-command-xxxxxxxxxx.eastus.inference.ml.azure.com/score",
      "tags": {},
      "traffic": {}
    }
'''  # NOQA


try:
    import io
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_online_endpoint
    from azure.ai.ml.constants._endpoint import EndpointKeyType
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLOnlineEndpoint(MLClientCommon):

    UPDATE_OVERRIDES = ['description',
                        'tags',
                        'mirror_traffic',
                        'traffic']

    PARAM_OVERRIDES = UPDATE_OVERRIDES + ['name',
                                          'auth_mode']

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
            local=dict(
                type='bool',
                default=False,
            ),
            description=dict(
                type='str',
                required=False,
            ),
            auth_mode=dict(
                type='str',
                default='key',
                choices=['key', 'aml_token'],
            ),
            mirror_traffic=dict(
                type='dict',
                required=False,
            ),
            traffic=dict(
                type='dict',
                required=False,
            ),
            key_type=dict(
                type='str',
                default='primary',
                choices=['primary', 'secondary'],
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent', 'regenerate_keys'],
            ),
        )

        self._client = None
        self.ml_registry = None
        self.state = None

        self.results = dict(
            changed=False,
            compare=[],
            ml_online_endpoint={}
        )

        required_if = [
            ('state', 'present', ['resource_definition'])
        ]

        super(AzureRMMLOnlineEndpoint, self).__init__(self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      required_if=required_if,
                                                      )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False

        ml_online_endpoint_info = self.get(name=self.name,
                                           local=self.local)

        if self.state == 'present':
            if self.resource_definition:
                resource_definition = io.StringIO(self.resource_definition)

            if ml_online_endpoint_info:
                # Update
                params_override = self.update_params(kwargs,
                                                     self.UPDATE_OVERRIDES,
                                                     ml_online_endpoint_info)

                # Generate ml_online_endpoint based on ansible args passed in.
                ml_online_endpoint = load_online_endpoint(resource_definition,
                                                          params_override=params_override)
                ml_online_endpoint_info = self.entity_to_dict(ml_online_endpoint_info)
                changed = not self.default_compare({},
                                                   self.entity_to_dict(ml_online_endpoint),
                                                   ml_online_endpoint_info,
                                                   '',
                                                   self.results)
                if changed and not self.check_mode:
                    response = self.client.begin_create_or_update(ml_online_endpoint,
                                                                  local=self.local)
                    ml_online_endpoint_object = self.get_poller_result(response)
                    ml_online_endpoint_info = self.entity_to_dict(ml_online_endpoint_object)
            else:
                # Create
                params_override = self.update_params(kwargs, self.PARAM_OVERRIDES)

                # Generate ml_online_endpoint based on ansible args passed in.
                ml_online_endpoint = load_online_endpoint(source=resource_definition,
                                                          params_override=params_override)

                changed = True
                if not self.check_mode:
                    response = self.client.begin_create_or_update(ml_online_endpoint,
                                                                  local=self.local)
                    ml_online_endpoint_object = self.get_poller_result(response)
                    ml_online_endpoint_info = self.entity_to_dict(ml_online_endpoint_object)
        elif self.state == 'absent':
            if ml_online_endpoint_info:
                # Delete
                changed = True
                if not self.check_mode:
                    response = self.client.online_endpoints.begin_delete(name=self.name,
                                                                         local=self.local)
                    ml_online_endpoint_info = self.get_poller_result(response)
        elif self.state == 'regenerate_keys':
            if ml_online_endpoint_info:
                changed = True
                if not self.check_mode:
                    key_type = self.get_key_type(self.key_type)
                    self.client.online_endpoints.begin_regenerate_keys(name=self.name,
                                                                       key_type=key_type)
                ml_online_endpoint_info = self.entity_to_dict(ml_online_endpoint_info)
            else:
                # Failure.  can't regenerate keys for entity that doesn't exist.
                self.fail("Online Endpoint doesn't exist")

        self.results['ml_online_endpoint'] = ml_online_endpoint_info
        self.results['changed'] = changed
        return self.results

    def update_params(self, kwargs, param_overrides, ml_online_endpoint=None):
        params_override = []

        # If ml_online_endpoint is defined use those values as a base.
        # Update can't change some of these values but we need
        # to keep the same values as before the update.
        if ml_online_endpoint:
            items = self.entity_to_dict(ml_online_endpoint).items()
            params_override = [{k: v} for k, v in items]

        # Update values based on what param_overrides says we can update.
        for key in list(self.module_arg_spec.keys()):
            if kwargs[key] is not None and key in param_overrides:
                params_override.append({key: kwargs[key]})
        return params_override

    def get(self, name, local=None, as_dict=False):
        try:
            # Attempt to retrieve ml_online_endpoint based on name
            ml_online_endpoint_info = self.client.online_endpoints.get(name=name,
                                                                       local=local)
            if as_dict:
                ml_online_endpoint_info = self.entity_to_dict(ml_online_endpoint_info)
        except ResourceNotFoundError:
            ml_online_endpoint_info = None
        return ml_online_endpoint_info

    def get_key_type(self, key_type):
        key_types = dict(primary=EndpointKeyType.PRIMARY_KEY_TYPE,
                         secondary=EndpointKeyType.SECONDARY_KEY_TYPE)
        return key_types.get(key_type, EndpointKeyType.PRIMARY_KEY_TYPE)


def main():
    AzureRMMLOnlineEndpoint()


if __name__ == '__main__':
    main()
