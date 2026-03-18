#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_component_info
version_added: "3.16.0"
short_description: List ML Component resources
description:
    - List ML Component resources.
options:
    name:
        description:
            - Name of the Azure ML component.
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
    ml_registry:
        description:
            - If provided, the command will target the registry
              instead of a workspace.  Hence resource group and
              workspace won't be required. Must be provided if
              ml_workspace and resource_group are not provided.
        required: false
        type: str
    version:
        description:
            - Version of the data asset. Must be provided, if label
              is not provided. Mutually exclusive with label.
        required: false
        type: str
    label:
        description:
            - Label of the data asset. Must be provided, if version
              is not provided. Mutually exclusive with version.
        required: false
        type: str
    list_type:
        description:
            - Specify if you want active, archived or all datasets.
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
- name: List ML Components
  azure.azcollection.azure_rm_ml_component_info:
    name: MyComponent
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List ML Components
  azure.azcollection.azure_rm_ml_component_info:
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
'''

RETURN = '''
ml_components:
    description:
        - Components that match the query.
    returned: always
    type: dict
    sample: [
      {
        "$schema": "https://azuremlschemas.azureedge.net/latest/commandComponent.schema.json",
        "code": "azureml:/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-component/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/codes/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/versions/1",
        "command": "python train.py  --training_data ${{inputs.training_data}}  --max_epocs ${{inputs.max_epocs}}    --learning_rate ${{inputs.learning_rate}}  --learning_rate_schedule ${{inputs.learning_rate_schedule}}  --model_output ${{outputs.model_output}}",
        "creation_context": {
            "created_at": "2026-03-18T14:02:54.635544+00:00",
            "created_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "created_by_type": "Application",
            "last_modified_at": "2026-03-18T14:02:54.773038+00:00",
            "last_modified_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "last_modified_by_type": "Application"
        },
        "display_name": "Train_upper_case",
        "environment": "azureml://registries/azureml/environments/sklearn-1.5/versions/41",
        "id": "azureml:/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-component/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/components/componentxxxxxxxxxx/labels/default",
        "inputs": {
            "learning_rate": {
                "default": "0.01",
                "optional": false,
                "type": "number"
            },
            "learning_rate_schedule": {
                "default": "time-based",
                "enum": [
                    "step",
                    "time-based"
                ],
                "optional": false,
                "type": "string"
            },
            "max_epocs": {
                "max": "100",
                "min": "0",
                "optional": false,
                "type": "integer"
            },
            "training_data": {
                "optional": false,
                "type": "uri_folder"
            }
        },
        "is_deterministic": true,
        "name": "componentxxxxxxxxxx",
        "outputs": {
            "model_output": {
                "type": "uri_folder"
            }
        },
        "resources": {
            "instance_count": 1
        },
        "type": "command",
        "version": "2"
      }
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLComponentInfo(MLClientCommon):
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
            ml_registry=dict(
                type='str',
            ),
            version=dict(
                type='str',
            ),
            label=dict(
                type='str',
            ),
            list_type=dict(
                type='str',
                choices=['archived', 'active', 'all'],
            ),
        )

        self._client = None

        self.results = dict(
            ml_components=[]
        )

        required_one_of = [('ml_workspace', 'ml_registry')]
        mutually_exclusive = [('version', 'label'),
                              ('ml_workspace', 'ml_registry'),
                              ('name', 'list_type')]
        required_together = [('ml_workspace', 'resource_group')]

        super(AzureRMMLComponentInfo, self).__init__(self.module_arg_spec,
                                                     supports_tags=False,
                                                     supports_check_mode=True,
                                                     facts_module=True,
                                                     required_one_of=required_one_of,
                                                     mutually_exclusive=mutually_exclusive,
                                                     required_together=required_together
                                                     )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            try:
                result = self.client.components.get(name=self.name,
                                                    version=self.version,
                                                    label=self.label)
                ml_components = [self.entity_to_dict(result)]
            except ResourceNotFoundError:
                ml_components = []
        else:
            list_view_type = self.get_list_view_type(self.list_type)
            results = self.client.components.list(name=self.name,
                                                  list_view_type=list_view_type)
            ml_components = [self.entity_to_dict(self.client.components.get(x.name, version=x.latest_version)) for x in results]

        self.results['ml_components'] = ml_components
        return self.results


def main():
    AzureRMMLComponentInfo()


if __name__ == '__main__':
    main()
