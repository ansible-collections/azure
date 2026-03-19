#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_data_info
version_added: "3.16.0"
short_description: List ML Data resources
description:
    - List ML Data resources.
options:
    name:
        description:
            - Name of the data asset. If provided, all the data versions
              under this name will be returned.
        type: str
        required: false
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
- name: List ML Data
  azure.azcollection.azure_rm_ml_data_info:
    name: MyData
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List ML Data
  azure.azcollection.azure_rm_ml_data_info:
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    list_type: archived
'''

RETURN = '''
ml_data_assets:
    description:
        - Data that was just created or updated.
    returned: always
    type: dict
    sample: [
      {
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
      },
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLDataInfo(MLClientCommon):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
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
        self.ml_data = None

        self.results = dict(
            ml_data_assets=[]
        )

        required_one_of = [('ml_workspace', 'ml_registry')]
        mutually_exclusive = [('version', 'label'),
                              ('ml_workspace', 'ml_registry'),
                              ('name', 'list_type')]
        required_together = [('ml_workspace', 'resource_group')]

        super(AzureRMMLDataInfo, self).__init__(self.module_arg_spec,
                                                supports_tags=False,
                                                supports_check_mode=True,
                                                required_one_of=required_one_of,
                                                mutually_exclusive=mutually_exclusive,
                                                required_together=required_together,
                                                facts_module=True,
                                                )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            label = self.label
            if not self.version and not label:
                label = 'latest'
            try:
                result = self.client.data.get(name=self.name,
                                              version=self.version,
                                              label=label)
                ml_data_assets = [self.entity_to_dict(result)]
            except ResourceNotFoundError:
                ml_data_assets = []
        else:
            list_view_type = self.get_list_view_type(self.list_type)
            results = self.client.data.list(list_view_type=list_view_type)

            ml_data_assets = [self.entity_to_dict(self.client.data.get(name=x.name, version=x.latest_version)) for x in results]

        self.results['ml_data_assets'] = ml_data_assets
        return self.results


def main():
    AzureRMMLDataInfo()


if __name__ == '__main__':
    main()
