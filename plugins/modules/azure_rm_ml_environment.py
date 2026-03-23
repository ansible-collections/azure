#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_environment
version_added: "3.16.0"
short_description: Create, Archive or Restore an Azure Machine Learning Environment
description:
    - Create, Archive or Restore an Azure Machine Learning Environment.
options:
    name:
        description:
            - Name of the Azure ML environment.
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
            - Environment definition in YAML
        type: str
        required: false
    version:
        description:
            - Data Asset version.
        type: str
    build_context:
        description:
            - Local path to the directory to use as a Docker build context.
              C(build_context) and C(image) are mutually exclusive arguments.
        type: str
    conda_file:
        description:
            - Local path to a conda specification file. C(image) must
              also be specified if this argument is used.
        type: str
    datastore:
        description:
            - The datastore to upload the local artifact to.
        type: str
    description:
        description:
            - Description of the environment.
        type: str
    dockerfile_path:
        description:
            - Relative path to the Dockerfile within the directory specified by
              C(build_context). If omitted, './Dockerfile' is used.
        default: ./Dockerfile
        type: str
    image:
        description:
            - Docker image. C(image) and C(build_context) are mutually
              exclusive arguments.
        type: str
    os_type:
        description:
            - Type of operating system.
        default: linux
        type: str
        choices:
            - linux
            - windows
    state:
        description:
            - State of the Environment. Use C(present) to create
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
- name: Create ML Environment
  azure.azcollection.azure_rm_ml_environment:
    name: environmentxxxxxxxxxx
    resource_group: xxxxx-ml-environment
    ml_workspace: workspace-xxxxxxxxxx
    version: 2
    resource_definition: |
      $schema: https://azuremlschemas.azureedge.net/latest/environment.schema.json
      image: mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04:20220303.v1
      conda_file: ./files/python-aml-rai.yaml
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
ml_environment:
    description:
        - Environment that was just created or updated.
    returned: always
    type: dict
    sample: {
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
'''  # NOQA


try:
    import io
    import time
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_environment
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLEnvironment(MLClientCommon):

    UPDATE_OVERRIDES = []

    PARAM_OVERRIDES = UPDATE_OVERRIDES + ['name',
                                          'version',
                                          'tags',
                                          'description',
                                          'image',
                                          'conda_file',
                                          'build_context',
                                          'os_type',
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
            build_context=dict(
                type='str',
                required=False,
            ),
            conda_file=dict(
                type='str',
                required=False,
            ),
            datastore=dict(
                type='str',
                required=False,
            ),
            description=dict(
                type='str',
                required=False,
            ),
            dockerfile_path=dict(
                type='str',
                default='./Dockerfile',
            ),
            image=dict(
                type='str',
                required=False,
            ),
            os_type=dict(
                type='str',
                default='linux',
                choices=['linux', 'windows'],
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
            ml_environment={}
        )

        required_if = [
            ('state', 'present', ['resource_definition'])
        ]
        required_one_of = [('ml_workspace', 'ml_registry')]
        mutually_exclusive = [('build_context', 'image'),
                              ('ml_workspace', 'ml_registry')]
        required_together = [('ml_workspace', 'resource_group'),
                             ('conda_file', 'image')]

        super(AzureRMMLEnvironment, self).__init__(self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   required_one_of=required_one_of,
                                                   mutually_exclusive=mutually_exclusive,
                                                   required_together=required_together,
                                                   required_if=required_if,
                                                   )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        if self.resource_definition:
            resource_definition = io.StringIO(self.resource_definition)
        else:
            resource_definition = None

        changed = False

        if self.state == 'present':
            ml_environment_info = self.get(name=self.name,
                                           version=self.version)

            if ml_environment_info:
                # Update
                # No Updates are supported at this time.
                changed = False
                ml_environment_info = self.entity_to_dict(ml_environment_info)
            else:
                # Create
                params_override = self.update_params(kwargs, self.PARAM_OVERRIDES)

                # Generate ml_environment based on ansible args passed in.
                ml_environment = load_environment(source=resource_definition,
                                                  params_override=params_override)
                changed = True
                if not self.check_mode:
                    response = self.client.create_or_update(ml_environment)
                    ml_environment_info = self.entity_to_dict(response)
        elif self.state == 'archive':
            # Archive
            list_view_type = self.get_list_view_type('active')
            results = self.client.environments.list(list_view_type=list_view_type)
            ml_environments = [x.name for x in results]

            if self.name in ml_environments:
                changed = True
                if not self.check_mode:
                    self.archive(name=self.name)
            ml_environment_info = None
        elif self.state == 'restore':
            # Restore
            list_view_type = self.get_list_view_type('archived')
            results = self.client.environments.list(list_view_type=list_view_type)
            ml_environments = [x.name for x in results]

            if self.name in ml_environments:
                changed = True
                if not self.check_mode:
                    self.restore(name=self.name)
                    # If we query too quick it hasn't fully restored.
                    # Seems the api shouldn't return until it's finished,
                    # but here we are.
                    time.sleep(1)
            ml_environment_info = self.get(name=self.name,
                                           label='latest',
                                           as_dict=True)

        self.results['ml_environment'] = ml_environment_info
        self.results['changed'] = changed
        return self.results

    def update_params(self, kwargs, param_overrides, ml_environment=None):
        params_override = []

        # If ml_environment is defined use those values as a base.
        # Update can't change some of these values but we need
        # to keep the same values as before the update.
        if ml_environment:
            items = self.entity_to_dict(ml_environment).items()
            params_override = [{k: v} for k, v in items]

        # Update values based on what param_overrides says we can update.
        for key in list(self.module_arg_spec.keys()):
            if kwargs[key] is not None and key in param_overrides:
                if key == 'build_context:':
                    build = {"path": self.build_context,
                             "dockerfile_path": self.dockerfile_path}
                    params_override.append({"build": build})
                else:
                    params_override.append({key: kwargs[key]})
        return params_override

    def get(self, name, version=None, label=None, as_dict=False):
        try:
            # Attempt to retrieve ml_environment based on name
            ml_environment_info = self.client.environments.get(name=name,
                                                               version=version,
                                                               label=label)
            if as_dict:
                ml_environment_info = self.entity_to_dict(ml_environment_info)
        except ResourceNotFoundError:
            ml_environment_info = None
        return ml_environment_info

    def archive(self, name=None):
        try:
            self.client.environments.archive(name=name)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error archive the environment instance: {0}".format(str(e)))

    def restore(self, name=None):
        try:
            self.client.environments.restore(name=name)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error restore the environment instance: {0}".format(str(e)))


def main():
    AzureRMMLEnvironment()


if __name__ == '__main__':
    main()
