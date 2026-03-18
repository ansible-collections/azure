#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_data
version_added: "3.16.0"
short_description: Create, Update, Archive, Restore an Azure Machine Learning Data Asset
description:
    - Create, Update, Archive, Restore an Azure Machine Learning Data Asset.
options:
    name:
        description:
            - Name of the Azure ML data asset.
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
    description:
        description:
            - Description of the data target.
        type: str
        required: false
    resource_definition:
        description:
            - "Local path to the YAML file containing the Azure ML data specification.
               The YAML reference docs for data can be found at:
               https://aka.ms/ml-cli-v2-data-yaml-reference."
        type: str
        required: false
    version:
        description:
            - Data Asset version.
        type: str
    label:
        description:
            - Label of the data asset. Must be provided, if version is not
              provided. Mutually exclusive with version.
        type: str
    data_type:
        description:
            - The type of managed identity.
        type: str
        choices:
            - mltable
            - uri_file
            - uri_folder
        required: false
    path:
        description:
            - Path to the data asset, can be local or remote.
        type: str
        required: false
    datastore:
        description:
            - The datastore to upload the local artifact to.
        type: str
        required: false
    skip_validation:
        description:
            - Skip validation of MLTable metadata when type is MLTable.
        type: bool
        required: false
    location:
        description:
            - The location to be used for the new data.
              If not specified, defaults to the location of the workspace.
        type: str
        required: false
    state:
        description:
            - State of the Data. Use C(present) to create
              or update. C(archive) to archive and C(restore)
              to restore.
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
- name: Create ML Data
  azure.azcollection.azure_rm_ml_data:
    location: eastus
    name: MyData
    description: My Data created by Ansible
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    tags:
      createdByToolkit: Ansible
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
ml_data_asset:
    description:
        - Data that was just created or updated.
    returned: always
    type: dict
    sample: {
      "creation_context":
        {
          "created_at": "2026-03-05T20:28:42.120932+00:00",
          "created_by": "ca413070-9a06-4e0a-8bb8-c167d29fa09e",
          "created_by_type": "Application",
          "last_modified_at": "2026-03-05T20:28:57.237566+00:00",
          "last_modified_by": "ca413070-9a06-4e0a-8bb8-c167d29fa09e",
          "last_modified_by_type": "Application",
        },
      "description": "Data asset created from local folder.",
      "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-data/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxx-xxx/data/data-xxxxxxx-xxx/versions/2",
      "name": "data-xxxxxxx-xxx",
      "path": "azureml://subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/xxxxx-ml-data/workspaces/workspace-xxxxxxx-xxx/datastores/workspaceblobstore/paths/LocalUpload/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/data/",
      "properties": {},
      "tags": {},
      "type": "uri_folder",
      "version": "2",
    }
'''  # NOQA


try:
    import io
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_data
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLData(MLClientCommon):

    UPDATE_OVERRIDES = ['description',
                        'tags'
                        ]

    PARAM_OVERRIDES = UPDATE_OVERRIDES + ['name',
                                          'data_type',
                                          'version',
                                          'label',
                                          'datastore',
                                          'path',
                                          'skip_validation',
                                          'location',
                                          ]

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True,
            ),
            description=dict(
                type='str',
                required=False,
            ),
            resource_definition=dict(
                type='str',
                required=False,
            ),
            location=dict(
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
            data_type=dict(
                type='str',
                required=False,
                choices=['mltable', 'uri_file', 'uri_folder'],
            ),
            version=dict(
                type='str',
                required=False,
            ),
            label=dict(
                type='str',
                required=False,
            ),
            path=dict(
                type='str',
                required=False,
            ),
            skip_validation=dict(
                type='bool',
            ),
            datastore=dict(
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
        self.ml_data_asset = None
        self.ml_registry = None
        self.state = None

        self.results = dict(
            changed=False,
            compare=[],
            ml_data_asset={}
        )

        required_one_of = [('ml_workspace', 'ml_registry')]
        mutually_exclusive = [('version', 'label'),
                              ('ml_workspace', 'ml_registry')]
        required_together = [('ml_workspace', 'resource_group')]

        super(AzureRMMLData, self).__init__(self.module_arg_spec,
                                            supports_check_mode=True,
                                            required_one_of=required_one_of,
                                            mutually_exclusive=mutually_exclusive,
                                            required_together=required_together)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        if self.resource_definition:
            resource_definition = io.StringIO(self.resource_definition)
        else:
            resource_definition = None

        changed = False
        ml_data_asset_info = self.get(name=self.name,
                                      version=self.version,
                                      label=self.label)

        if self.state == 'present':
            if ml_data_asset_info:
                # Update
                params_override = self.update_params(kwargs,
                                                     self.UPDATE_OVERRIDES,
                                                     ml_data_asset_info)

                # Generate ml_data_asset based on ansible args passed in.
                ml_data_asset = load_data(None, params_override=params_override)
                ml_data_asset_info = self.entity_to_dict(ml_data_asset_info)
                changed = not self.default_compare({},
                                                   self.entity_to_dict(ml_data_asset),
                                                   ml_data_asset_info,
                                                   '',
                                                   self.results)
                if changed and not self.check_mode:
                    response = self.client.data.create_or_update(ml_data_asset)
                    ml_data_asset_info = self.entity_to_dict(response)

            else:
                # Create
                params_override = self.update_params(kwargs, self.PARAM_OVERRIDES)

                # Generate ml_data_asset based on ansible args passed in.
                ml_data_asset = load_data(resource_definition,
                                          params_override=params_override)
                changed = True
                if not self.check_mode:
                    response = self.client.data.create_or_update(ml_data_asset)
                    ml_data_asset_info = self.entity_to_dict(response)
        elif self.state == 'archive':
            # Archive
            list_view_type = self.get_list_view_type('active')
            results = self.client.data.list(list_view_type=list_view_type)
            ml_data_assets = [x.name for x in results]

            if self.name in ml_data_assets:
                changed = True
                if not self.check_mode:
                    self.archive(name=self.name,
                                 version=self.version,
                                 label=self.label)
                ml_data_asset_info = self.get(name=self.name,
                                              version=self.version,
                                              label=self.label,
                                              as_dict=True)
        elif self.state == 'restore':
            # Restore
            list_view_type = self.get_list_view_type('archived')
            results = self.client.data.list(list_view_type=list_view_type)
            ml_data_assets = [x.name for x in results]

            if self.name in ml_data_assets:
                changed = True
                if not self.check_mode:
                    self.restore(name=self.name,
                                 version=self.version,
                                 label=self.label)
                ml_data_asset_info = self.get(name=self.name,
                                              version=self.version,
                                              label=self.label,
                                              as_dict=True)

        self.results['ml_data_asset'] = ml_data_asset_info
        self.results['changed'] = changed
        return self.results

    def update_params(self, kwargs, param_overrides, ml_data_asset=None):
        params_override = []

        # If ml_data_asset is defined use those values as a base.
        # Update can't change some of these values but we need
        # to keep the same values as before the update.
        if ml_data_asset:
            items = self.entity_to_dict(ml_data_asset).items()
            params_override = [{k: v} for k, v in items if k != "ssh_settings"]

        # Update values based on what param_overrides says we can update.
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if kwargs[key] is not None and key in param_overrides:
                params_override.append({key: kwargs[key]})
        return params_override

    def get(self, name=None, version=None, label=None, as_dict=False):
        try:
            # Attempt to retrieve ml_data_asset based on name
            ml_data_asset_info = self.client.data.get(name=name,
                                                      version=version,
                                                      label=label)
            if as_dict:
                ml_data_asset_info = self.entity_to_dict(ml_data_asset_info)
        except ResourceNotFoundError:
            ml_data_asset_info = None
        except Exception as e:  # pylint: disable=broad-exception-caught
            ml_data_asset_info = None
        return ml_data_asset_info

    def archive(self, name=None, version=None, label=None):
        try:
            response = self.client.data.archive(name=name,
                                                version=version,
                                                label=label)
            return response
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error archive the data instance: {0}".format(str(e)))

    def restore(self, name=None, version=None, label=None):
        try:
            response = self.client.data.restore(name=name,
                                                version=version,
                                                label=label)
            return response
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error restore the data instance: {0}".format(str(e)))


def main():
    AzureRMMLData()


if __name__ == '__main__':
    main()
