#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_datastore_info
version_added: "3.16.0"
short_description: List ML Data resources
description:
    - List ML Data resources.
options:
    name:
        description:
            - Name of the datastore.
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

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: List Specific ML datastore
  azure.azcollection.azure_rm_ml_datastore_info:
    name: MyData
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List ML datastore
  azure.azcollection.azure_rm_ml_datastore_info:
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
'''

RETURN = '''
ml_datastore:
    description:
        - Datastore that was just created or updated.
    returned: always
    type: dict
    sample: [
      {
        "account_name": "workspacstoragexxxxxxxxx",
        "container_name": "datastorexxxxxxxxx-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "credentials": {},
        "description": "here is a description",
        "endpoint": "core.windows.net",
        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-datastore/providers/Microsoft.MachineLearningServices/workspaces/workspaceexxxxxxxx/datastores/datastorexxxxxxxxx",
        "name": "datastorexxxxxxxxx",
        "protocol": "https",
        "tags": {},
        "type": "azure_blob",
      }
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLDatastoreInfo(MLClientCommon):
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
        )

        self._client = None
        self.ml_registry = None

        self.results = dict(
            ml_datastores=[]
        )

        super(AzureRMMLDatastoreInfo, self).__init__(self.module_arg_spec,
                                                     supports_tags=False,
                                                     supports_check_mode=True,
                                                     facts_module=True,
                                                     )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            try:
                result = self.client.datastores.get(name=self.name,
                                                    include_secrets=False)
                ml_datastores = [self.entity_to_dict(result)]
            except ResourceNotFoundError:
                ml_datastores = []
        else:
            results = self.client.datastores.list(include_secrets=False)

            ml_datastores = [self.entity_to_dict(x) for x in results]

        self.results['ml_datastores'] = ml_datastores
        return self.results


def main():
    AzureRMMLDatastoreInfo()


if __name__ == '__main__':
    main()
