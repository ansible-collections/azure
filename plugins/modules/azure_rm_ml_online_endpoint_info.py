#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_online_endpoint_info
version_added: "3.17.0"
short_description: List ML Online Endpoint resources
description:
    - List ML Online Endpoint resources.
options:
    name:
        description:
            - Name of the Azure ML online endpoint.
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
    include_auth_keys:
        description:
            - If True then auth_keys will be populated in the return data.
        default: false
        type: bool
    local:
        description:
            - List all local endpoints.
        type: bool
        default: false

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get Specific ML Online Endpoint by name w/auth_keys
  azure.azcollection.azure_rm_ml_online_endpoint_info:
    name: endpoint-command-xxxxxxxxxx
    include_auth_keys: true
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List Local ML Online Endpoints
  azure.azcollection.azure_rm_ml_online_endpoint_info:
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    local: true
'''

RETURN = '''
ml_online_endpoints:
    description:
        - Online Endpoints that match the query.
    returned: always
    type: dict
    sample: [
      {
          "auth_mode": "key",
          "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-online_endpoint/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/onlineEndpoints/endpoint-command-xxxxxxxxxx",
          "identity": {
              "principal_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
              "tenant_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
              "type": "system_assigned"
          },
          "auth_keys": {
              "primary_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
              "secondary_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
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
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLOnlineEndpointInfo(MLClientCommon):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=False,
            ),
            include_auth_keys=dict(
                type='bool',
                default=False,
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
            ml_online_endpoints=[]
        )

        mutually_exclusive = [('include_auth_keys', 'local')]

        super(AzureRMMLOnlineEndpointInfo, self).__init__(self.module_arg_spec,
                                                          supports_tags=False,
                                                          supports_check_mode=True,
                                                          facts_module=True,
                                                          mutually_exclusive=mutually_exclusive,
                                                          )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            ml_online_endpoints = [self.get(self.name,
                                            include_auth_keys=self.include_auth_keys,
                                            local=self.local)]
        else:
            results = self.client.online_endpoints.list(local=self.local)
            ml_online_endpoints = [self.get(x.name, include_auth_keys=self.include_auth_keys, local=self.local) for x in results]

        self.results['ml_online_endpoints'] = ml_online_endpoints
        return self.results

    def get(self, name, include_auth_keys=False, local=False):
        try:
            result = self.client.online_endpoints.get(name=name,
                                                      local=self.local)
            ml_online_endpoint = self.entity_to_dict(result)
            if include_auth_keys and not local:
                auth_keys = self.client.online_endpoints.get_keys(name=name)
                ml_online_endpoint['auth_keys'] = dict(primary_key=auth_keys.primary_key,
                                                       secondary_key=auth_keys.secondary_key)
        except ResourceNotFoundError:
            ml_online_endpoint = None

        return ml_online_endpoint


def main():
    AzureRMMLOnlineEndpointInfo()


if __name__ == '__main__':
    main()
