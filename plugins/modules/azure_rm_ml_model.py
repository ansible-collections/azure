#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_model
version_added: "3.17.0"
short_description: Create, Archive or Restore an Azure Machine Learning Model
description:
    - Create, Archive or Restore an Azure Machine Learning Model.
options:
    name:
        description:
            - Name of the Azure ML model.
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
            - Model definition in YAML
        type: str
        required: false
    version:
        description:
            - Data Asset version.
        type: str
    path:
        description:
            - Path to the model file(s). This can be either a local
              or a remote location. If specified, name and version
              must also be provided.
        type: str
    stage:
        description:
            - Stage of the model.
        type: str
        choices:
            - Staging
            - Production
            - Archived
            - Logged
            - Development
            - Deprecated
            - Retired
    datastore:
        description:
            - The datastore to upload the local artifact to.
        type: str
    description:
        description:
            - Description of the model.
        type: str
    type:
        description:
            - Type of the model.
        default: custom_model
        type: str
        choices:
            - custom_model
            - mlflow_model
            - triton_model
    state:
        description:
            - State of the Model. Use C(present) to create
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
    - azure.azcollection.azure_tags

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create ML Model
  azure.azcollection.azure_rm_ml_model:
    name: modelxxxxxxxxxx
    resource_group: xxxxx-ml-model
    ml_workspace: workspace-xxxxxxxxxx
    version: 2
    stage: Production
    resource_definition: |
      $schema: https://azuremlschemas.azureedge.net/latest/model.schema.json
      path: ./files/mlflow-model/model.pkl
      description: Model created from local file.
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
ml_model:
    description:
        - Model that was just created or updated.
    returned: always
    type: dict
    sample: {
        "creation_context": {
            "created_at": "2026-03-25T17:48:05.464195+00:00",
            "created_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "created_by_type": "Application",
            "last_modified_at": "2026-03-25T17:48:12.822846+00:00",
            "last_modified_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "last_modified_by_type": "Application"
        },
        "description": "Model created from local file.",
        "id": "azureml:/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-model/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/models/modelxxxxxxxxxx/versions/2",
        "name": "modelxxxxxxxxxx",
        "path": "azureml://subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-model/workspaces/workspace-xxxxxxxxxx/datastores/workspaceblobstore/paths/LocalUpload/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/model.pkl",
        "properties": {},
        "stage": "Production",
        "tags": {},
        "type": "custom_model",
        "version": "2"
    }
'''  # NOQA


try:
    import io
    import time
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_model
    from azure.ai.ml.entities._assets import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLModel(MLClientCommon):

    UPDATE_OVERRIDES = ['stage']

    PARAM_OVERRIDES = UPDATE_OVERRIDES + ['name',
                                          'version',
                                          'path',
                                          'type',
                                          'description',
                                          'tags',
                                          'datastore']

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
            path=dict(
                type='str',
                required=False,
            ),
            stage=dict(
                type='str',
                required=False,
                choices=['Staging', 'Production', 'Archived',
                         'Logged', 'Development', 'Deprecated', 'Retired'],
            ),
            datastore=dict(
                type='str',
                required=False,
            ),
            description=dict(
                type='str',
                required=False,
            ),
            type=dict(
                type='str',
                default='custom_model',
                choices=['custom_model', 'mlflow_model', 'triton_model'],
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
            ml_model={}
        )

        required_one_of = [('ml_workspace', 'ml_registry')]
        mutually_exclusive = [('ml_workspace', 'ml_registry')]
        required_together = [('ml_workspace', 'resource_group')]

        super(AzureRMMLModel, self).__init__(self.module_arg_spec,
                                             supports_check_mode=True,
                                             required_one_of=required_one_of,
                                             mutually_exclusive=mutually_exclusive,
                                             required_together=required_together,
                                             )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False

        if self.state == 'present':
            ml_model_info = self.get(name=self.name,
                                     version=self.version)

            if ml_model_info:
                # Update
                params_override = self.update_params(kwargs,
                                                     self.UPDATE_OVERRIDES,
                                                     ml_model_info)

                # Generate ml_model based on ansible args passed in.
                ml_model = Model._load(data=[],
                                       params_override=params_override)

                ml_model = load_model(None, params_override=params_override)
                ml_model_info = self.entity_to_dict(ml_model_info)
                changed = not self.default_compare({},
                                                   self.entity_to_dict(ml_model),
                                                   ml_model_info,
                                                   '',
                                                   self.results)
                if changed and not self.check_mode:
                    response = self.client.create_or_update(ml_model)
                    ml_model_info = self.entity_to_dict(response)
            else:
                # Create
                params_override = self.update_params(kwargs, self.PARAM_OVERRIDES)

                # Generate ml_model based on ansible args passed in.
                if self.resource_definition:
                    resource_definition = io.StringIO(self.resource_definition)
                    ml_model = load_model(source=resource_definition,
                                          params_override=params_override)
                else:
                    ml_model = Model(
                        name=self.name,
                        version=self.version,
                        path=self.path,
                        description=self.description,
                        tags=self.tags,
                        stage=self.stage,
                        type=self.type,
                        datastore=self.datastore,
                    )

                changed = True
                if not self.check_mode:
                    response = self.client.create_or_update(ml_model)
                    ml_model_info = self.entity_to_dict(response)
        elif self.state == 'archive':
            # Archive
            list_view_type = self.get_list_view_type('active')
            results = self.client.models.list(list_view_type=list_view_type)
            ml_models = [x.name for x in results]

            if self.name in ml_models:
                changed = True
                if not self.check_mode:
                    self.archive(name=self.name)
            ml_model_info = None
        elif self.state == 'restore':
            # Restore
            list_view_type = self.get_list_view_type('archived')
            results = self.client.models.list(list_view_type=list_view_type)
            ml_models = [x.name for x in results]

            if self.name in ml_models:
                changed = True
                if not self.check_mode:
                    self.restore(name=self.name)
                    # If we query too quick it hasn't fully restored.
                    # Seems the api shouldn't return until it's finished,
                    # but here we are.
                    time.sleep(1)
            ml_model_info = self.get(name=self.name,
                                     label='latest',
                                     as_dict=True)

        self.results['ml_model'] = ml_model_info
        self.results['changed'] = changed
        return self.results

    def update_params(self, kwargs, param_overrides, ml_model=None):
        params_override = []

        # If ml_model is defined use those values as a base.
        # Update can't change some of these values but we need
        # to keep the same values as before the update.
        if ml_model:
            items = self.entity_to_dict(ml_model).items()
            params_override = [{k: v} for k, v in items]

        # Update values based on what param_overrides says we can update.
        for key in list(self.module_arg_spec.keys()):
            if kwargs[key] is not None and key in param_overrides:
                params_override.append({key: kwargs[key]})
        return params_override

    def get(self, name, version=None, label=None, as_dict=False):
        try:
            # Attempt to retrieve ml_model based on name
            ml_model_info = self.client.models.get(name=name,
                                                   version=version,
                                                   label=label)
            if as_dict:
                ml_model_info = self.entity_to_dict(ml_model_info)
        except ResourceNotFoundError:
            ml_model_info = None
        return ml_model_info

    def archive(self, name=None):
        try:
            self.client.models.archive(name=name)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error archive the model instance: {0}".format(str(e)))

    def restore(self, name=None):
        try:
            self.client.models.restore(name=name)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error restore the model instance: {0}".format(str(e)))


def main():
    AzureRMMLModel()


if __name__ == '__main__':
    main()
