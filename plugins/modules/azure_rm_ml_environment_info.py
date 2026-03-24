#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_environment_info
version_added: "3.16.0"
short_description: List ML Environment resources
description:
    - List ML Environment resources.
options:
    name:
        description:
            - Name of the Azure ML environment.
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
- name: List ML Environment by name
  azure.azcollection.azure_rm_ml_environment_info:
    name: MyEnvironment
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List Archived ML Environments
  azure.azcollection.azure_rm_ml_environment_info:
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    list_type: archived
'''

RETURN = '''
ml_environments:
    description:
        - Environments that match the query.
    returned: always
    type: dict
    sample: [
      {
          "conda_file": {
              "channels": [
                  "conda-forge"
              ],
              "dependencies": [
                  "python=3.8",
                  "pip=20.0.2",
                  {
                      "pip": [
                          "numpy",
                          "pandas",
                          "pyarrow",
                          "scikit-learn",
                          "mlflow",
                          "azureml-mlflow",
                          "responsibleai~=0.17.0",
                          "raiwidgets~=0.17.0",
                          "markupsafe<=2.0.1",
                          "itsdangerous==2.0.1",
                          "azureml-dataset-runtime",
                          "azureml-core"
                      ]
                  }
              ],
              "name": "aml-rai-environment"
          },
          "creation_context": {
              "created_at": "2026-03-20T17:34:28.790877+00:00",
              "created_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
              "created_by_type": "Application",
              "last_modified_at": "2026-03-20T17:34:28.790877+00:00",
              "last_modified_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
              "last_modified_by_type": "Application"
          },
          "id": "azureml:/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-environment/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/environments/environmentxxxxxxxxxx/versions/2",
          "image": "mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04:20220303.v1",
          "name": "environmentxxxxxxxxxx",
          "os_type": "linux",
          "tags": {},
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


class AzureRMMLEnvironmentInfo(MLClientCommon):
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
            ml_environments=[]
        )

        required_one_of = [('ml_workspace', 'ml_registry')]
        mutually_exclusive = [('version', 'label'),
                              ('ml_workspace', 'ml_registry'),
                              ('name', 'list_type')]
        required_together = [('ml_workspace', 'resource_group')]

        super(AzureRMMLEnvironmentInfo, self).__init__(self.module_arg_spec,
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
                result = self.client.environments.get(name=self.name,
                                                      version=self.version,
                                                      label=self.label)
                ml_environments = [self.entity_to_dict(result)]
            except ResourceNotFoundError:
                ml_environments = []
        else:
            list_view_type = self.get_list_view_type(self.list_type)
            results = self.client.environments.list(name=self.name,
                                                    list_view_type=list_view_type)
            ml_environments = [self.entity_to_dict(self.client.environments.get(x.name, version=x.latest_version)) for x in results]

        self.results['ml_environments'] = ml_environments
        return self.results


def main():
    AzureRMMLEnvironmentInfo()


if __name__ == '__main__':
    main()
