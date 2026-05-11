#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_registry
version_added: "3.19.0"
short_description: Create, Update or Delete an Azure Machine Learning Registry
description:
    - Create, Update or Delete an Azure Machine Learning Registry.
options:
    name:
        description:
            - Name of the Azure ML registry.
        type: str
        required: true
    display_name:
        description:
            - Display name for the registry.
        type: str
        required: false
    resource_definition:
        description:
            - Registry definition in YAML
        type: str
        required: false
    public_network_access:
        description:
            - Allow public endpoint connectivity when a registry
              is private link enabled.
        type: str
        choices:
            - Disabled
            - Enabled
        default: Disabled
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    state:
        description:
            - State of the Registry. Use C(present) to create
              or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create ML Registry
  azure.azcollection.azure_rm_ml_registry:
    name: MyRegistry
    description: My Registry created by Ansible
    resource_group: myResourceGroup
    resource_definition: |
      name: MyRegistry
      tags:
        foo: bar
      location: eastus
      replication_locations:
        - location: eastus
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
ml_registry:
    description:
        - Registry that was just created or updated.
    returned: always
    type: dict
    sample: {
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
'''  # NOQA


try:
    import io
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_registry
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLRegistry(MLClientCommon):

    PARAM_OVERRIDES = ['name',
                       'display_name',
                       'tags',
                       'public_network_access',
                       ]

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True
            ),
            display_name=dict(
                type='str',
                required=False,
            ),
            resource_definition=dict(
                type='str',
                required=False,
            ),
            public_network_access=dict(
                type='str',
                choices=['Disabled', 'Enabled'],
                default='Disabled',
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
        )

        self._client = None
        self.ml_registry = None
        self.ml_workspace = None
        self.state = None

        self.results = dict(
            changed=False,
            compare=[],
            ml_registry={}
        )

        super(AzureRMMLRegistry, self).__init__(self.module_arg_spec,
                                                supports_check_mode=True,
                                                )

    def exec_module(self, **kwargs):

        params_override = []
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])
            if kwargs[key] is not None and key in self.PARAM_OVERRIDES:
                params_override.append({key: kwargs[key]})

        if self.resource_definition:
            resource_definition = io.StringIO(self.resource_definition)
        else:
            resource_definition = None

        changed = False

        try:
            # Attempt to retrieve ml_registry based on name
            ml_registry_info = self.client.registries.get(self.name)
        except ResourceNotFoundError:
            ml_registry_info = None

        if self.state == 'present':
            # Generate ml_registry based on ansible args passed in.
            ml_registry = load_registry(resource_definition,
                                        params_override=params_override)
            if ml_registry_info:
                # Update
                ml_registry_info = self.entity_to_dict(ml_registry_info)
                changed = not self.default_compare({},
                                                   self.entity_to_dict(ml_registry),
                                                   ml_registry_info,
                                                   '',
                                                   self.results)
                if changed and not self.check_mode:
                    response = self.client.registries.begin_create(
                        registry=ml_registry
                    )
                    ml_registry_object = self.get_poller_result(response)
                    ml_registry_info = self.entity_to_dict(ml_registry_object)

            else:
                # Create
                changed = True
                if not self.check_mode:
                    response = self.client.registries.begin_create(
                        registry=ml_registry
                    )
                    ml_registry_object = self.get_poller_result(response)
                    ml_registry_info = self.entity_to_dict(ml_registry_object)
        else:
            # Delete
            if ml_registry_info:
                changed = True
                if not self.check_mode:
                    response = self.client.registries.begin_delete(
                        name=self.name
                    )
                    ml_registry_object = self.get_poller_result(response)
                    ml_registry_info = self.entity_to_dict(ml_registry_object)

        self.results['ml_registry'] = ml_registry_info
        self.results['changed'] = changed
        return self.results


def main():
    AzureRMMLRegistry()


if __name__ == '__main__':
    main()
