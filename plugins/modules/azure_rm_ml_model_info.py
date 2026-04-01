#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_model_info
version_added: "3.17.0"
short_description: List ML Model resources
description:
    - List ML Model resources.
options:
    name:
        description:
            - Name of the Azure ML model.
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
            - Version of the model. Must be provided, if label
              is not provided. Mutually exclusive with label.
        required: false
        type: str
    label:
        description:
            - Label of the model. Must be provided, if version
              is not provided. Mutually exclusive with version.
        required: false
        type: str
    stage:
        description:
            - Stage of the model.
        required: false
        type: str
    list_type:
        description:
            - Specify if you want active, archived or all models.
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
- name: List ML Model by name
  azure.azcollection.azure_rm_ml_model_info:
    name: MyModel
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List Archived ML Models
  azure.azcollection.azure_rm_ml_model_info:
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    list_type: archived
'''

RETURN = '''
ml_models:
    description:
        - Models that match the query.
    returned: always
    type: dict
    sample: [
      {
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
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLModelInfo(MLClientCommon):
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
            stage=dict(
                type='str',
            ),
            list_type=dict(
                type='str',
                choices=['archived', 'active', 'all'],
            ),
        )

        self._client = None

        self.results = dict(
            ml_models=[]
        )

        required_one_of = [('ml_workspace', 'ml_registry')]
        mutually_exclusive = [('version', 'label'),
                              ('ml_workspace', 'ml_registry'),
                              ('name', 'list_type'),
                              ('name', 'stage')]
        required_together = [('ml_workspace', 'resource_group')]

        super(AzureRMMLModelInfo, self).__init__(self.module_arg_spec,
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
                result = self.client.models.get(name=self.name,
                                                version=self.version,
                                                label=self.label)
                ml_models = [self.entity_to_dict(result)]
            except ResourceNotFoundError:
                ml_models = []
        else:
            list_view_type = self.get_list_view_type(self.list_type)
            results = self.client.models.list(name=self.name,
                                              stage=self.stage,
                                              list_view_type=list_view_type)
            ml_models = [self.entity_to_dict(self.client.models.get(x.name, version=x.latest_version)) for x in results]

        self.results['ml_models'] = ml_models
        return self.results


def main():
    AzureRMMLModelInfo()


if __name__ == '__main__':
    main()
