#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_registry_info
version_added: "3.19.0"
short_description: List ML Registries
description:
    - List ML Registries.
options:
    name:
        description:
            - Retrieve details about a specific ml registry.
        type: str
        required: false
    resource_group:
        description:
            - Name of a resource group to limit ml registries from.
              If not specified the subscription will be searched.
        required: false
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get info on a specific ml regsitry
  azure.azcollection.azure_rm_ml_registry_info:
    name: my_registry
    resource_group: test_ml_registry
  register: result

- name: List all ml registries in subscription
  azure.azcollection.azure_rm_ml_registry_info:
  register: results
'''

RETURN = '''
ml_registries:
    description:
        - List of ML Registries.
    returned: always
    type: dict
    sample: [
        {
            "container_registry": {
                "acr_account_sku": "premium",
                "arm_resource_id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/azureml-rg-registry-xxxxxxx-xxx_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.ContainerRegistry/registries/xxxxxxxxxxx"
            },
            "discovery_url": "https://eastus.api.azureml.ms/registrymanagement/v1.0/registries/registry-xxxxxxx-xxx/discovery",
            "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-registry/providers/Microsoft.MachineLearningServices/registries/registry-xxxxxxx-xxx",
            "identity": {
                "principal_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "tenant_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "type": "system_assigned"
            },
            "location": "eastus",
            "managed_resource_group": "{'additional_properties': {}, 'resource_id': '/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/azureml-rg-registry-xxxxxxx-xxx_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}",
            "mlflow_registry_uri": "azureml://eastus.api.azureml.ms/mlflow/v1.0/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-registry/providers/Microsoft.MachineLearningServices/registries/registry-xxxxxxx-xxx",
            "name": "registry-xxxxxxx-xxx",
            "public_network_access": "Disabled",
            "replication_locations": [
                {
                    "location": "eastus",
                    "storage_config": {
                        "arm_resource_id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/azureml-rg-registry-xxxxxxx-xxx_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.Storage/storageAccounts/xxxxxxxxxxx",
                        "replication_count": 1,
                        "storage_account_hns": false,
                        "storage_account_type": "standard_lrs"
                    }
                }
            ],
            "tags": {
                "foo": "bar"
            }
        }
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.constants._common import Scope
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLRegistryInfo(MLClientCommon):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=False
            ),
            resource_group=dict(
                type='str',
                required=False
            ),
        )

        self._client = None
        self.ml_workspace = None
        self.ml_registry = None

        required_by = {'name': 'resource_group'}

        self.results = dict(
            ml_registries=[]
        )

        super(AzureRMMLRegistryInfo, self).__init__(self.module_arg_spec,
                                                    supports_tags=False,
                                                    supports_check_mode=True,
                                                    required_by=required_by,
                                                    facts_module=True,
                                                    )

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            try:
                result = self.client.registries.get(self.name)
                ml_registries = [self.entity_to_dict(result)]
            except ResourceNotFoundError:
                ml_registries = []
        else:
            scope = Scope.RESOURCE_GROUP if self.resource_group else Scope.SUBSCRIPTION
            results = self.client.registries.list(scope=scope)
            ml_registries = [self.entity_to_dict(x) for x in results]

        self.results['ml_registries'] = ml_registries

        return self.results


def main():
    AzureRMMLRegistryInfo()


if __name__ == '__main__':
    main()
