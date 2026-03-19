#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_component
version_added: "3.16.0"
short_description: Create, Archive or Restore an Azure Machine Learning Component
description:
    - Create, Archive or Restore an Azure Machine Learning Component.
options:
    name:
        description:
            - Name of the Azure ML component.
        type: str
        required: true
    resource_group:
        description:
            - Name of resource group.
        required: false
        type: str
    ml_workspace:
        description:
            - Name of the Azure ML workspace.
        required: false
        type: str
    ml_registry:
        description:
            - Name of the Azure ML registry.
        required: false
        type: str
    resource_definition:
        description:
            - Component definition in YAML
        type: str
        required: false
    version:
        description:
            - Data Asset version. Mutually exclusive with label.
        type: str
    label:
        description:
            - Label of the data asset. Mutually exclusive with version.
        type: str
    state:
        description:
            - State of the Component. Use C(present) to create
              or update. C(archive) to archive, C(restore) to
              restore.
        default: present
        type: str
        choices:
            - present
            - archive
            - restore

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create ML Component
  azure.azcollection.azure_rm_ml_component:
    name: MyComponent
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    version: 1b
    resource_definition: |
      $schema: https://azuremlschemas.azureedge.net/latest/commandComponent.schema.json
      name: my_train
      display_name: Train_upper_case
      type: command
      inputs:
        training_data:
          type: uri_folder
        max_epocs:
          type: integer
          min: 0
          max: 100
        learning_rate:
          type: number
          default: 0.01
        learning_rate_schedule:
          type: string
          default: time-based
          enum:
              - "step"
              - "time-based"
      outputs:
        model_output:
          type: uri_folder
      code: ./targets/azure_rm_ml_component/files/train_src
      environment: azureml://registries/azureml/environments/sklearn-1.5/labels/latest
      command: >-
        python train.py
        --training_data ${{ '{{' }}inputs.training_data{{ '}}' }}
        --max_epocs ${{ '{{' }}inputs.max_epocs{{ '}}' }}
        --learning_rate ${{ '{{' }}inputs.learning_rate{{ '}}' }}
        --learning_rate_schedule ${{ '{{' }}inputs.learning_rate_schedule{{ '}}' }}
        --model_output ${{ '{{' }}outputs.model_output{{ '}}' }}
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
ml_component:
    description:
        - Component that was just created or updated.
    returned: always
    type: dict
    sample: {
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
'''  # NOQA


try:
    import io
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_component
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLComponent(MLClientCommon):

    UPDATE_OVERRIDES = []

    PARAM_OVERRIDES = UPDATE_OVERRIDES + ['name', 'version']

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
                required=False,
            ),
            ml_workspace=dict(
                type='str',
                required=False,
            ),
            ml_registry=dict(
                type='str',
                required=False,
            ),
            version=dict(
                type='str',
                required=False,
            ),
            label=dict(
                type='str',
                required=False,
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'archive', 'restore'],
            ),
        )

        self._client = None
        self.ml_registry = None
        self.state = None

        self.results = dict(
            changed=False,
            compare=[],
            ml_component={}
        )

        required_if = [
            ('state', 'present', ['resource_definition'])
        ]
        required_one_of = [('ml_workspace', 'ml_registry')]
        mutually_exclusive = [('version', 'label'),
                              ('ml_workspace', 'ml_registry')]
        required_together = [('ml_workspace', 'resource_group')]

        super(AzureRMMLComponent, self).__init__(self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=False,
                                                 required_one_of=required_one_of,
                                                 mutually_exclusive=mutually_exclusive,
                                                 required_together=required_together,
                                                 required_if=required_if,
                                                 )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.resource_definition:
            resource_definition = io.StringIO(self.resource_definition)
        else:
            resource_definition = None

        changed = False
        ml_component_info = self.get(name=self.name,
                                     version=self.version,
                                     label=self.label)

        if self.state == 'present':
            if ml_component_info:
                # Update
                # No Updates are supported at this time.
                changed = False
                ml_component_info = self.entity_to_dict(ml_component_info)
            else:
                # Create
                params_override = self.update_params(kwargs, self.PARAM_OVERRIDES)

                # Generate ml_component based on ansible args passed in.
                ml_component = load_component(source=resource_definition,
                                              params_override=params_override)
                changed = True
                if not self.check_mode:
                    response = self.client.create_or_update(ml_component)
                    ml_component_info = self.entity_to_dict(response)
        elif self.state == 'archive':
            # Archive
            list_view_type = self.get_list_view_type('active')
            results = self.client.components.list(list_view_type=list_view_type)
            ml_components = [x.name for x in results]

            if self.name in ml_components:
                changed = True
                if not self.check_mode:
                    self.archive(name=self.name)
            ml_component_info = self.get(name=self.name,
                                         version=self.version,
                                         label=self.label,
                                         as_dict=True)
        elif self.state == 'restore':
            # Restore
            list_view_type = self.get_list_view_type('archived')
            results = self.client.components.list(list_view_type=list_view_type)
            ml_components = [x.name for x in results]

            if self.name in ml_components:
                changed = True
                if not self.check_mode:
                    self.restore(name=self.name)
            ml_component_info = self.get(name=self.name,
                                         version=self.version,
                                         label=self.label,
                                         as_dict=True)

        self.results['ml_component'] = ml_component_info
        self.results['changed'] = changed
        return self.results

    def update_params(self, kwargs, param_overrides, ml_component=None):
        params_override = []

        # If ml_ccomponent is defined use those values as a base.
        # Update can't change some of these values but we need
        # to keep the same values as before the update.
        if ml_component:
            items = self.entity_to_dict(ml_component).items()
            params_override = [{k: v} for k, v in items]

        # Update values based on what param_overrides says we can update.
        for key in list(self.module_arg_spec.keys()):
            if kwargs[key] is not None and key in param_overrides:
                params_override.append({key: kwargs[key]})
        return params_override

    def get(self, name, version=None, label=None, as_dict=False):
        try:
            # Attempt to retrieve ml_component based on name
            ml_component_info = self.client.components.get(name=name,
                                                           version=version,
                                                           label=label)
            if as_dict:
                ml_component_info = self.entity_to_dict(ml_component_info)
        except ResourceNotFoundError:
            ml_component_info = None
        return ml_component_info

    def archive(self, name=None):
        try:
            self.client.components.archive(name=name)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error archive the component instance: {0}".format(str(e)))

    def restore(self, name=None):
        try:
            self.client.components.restore(name=name)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error restore the component instance: {0}".format(str(e)))


def main():
    AzureRMMLComponent()


if __name__ == '__main__':
    main()
