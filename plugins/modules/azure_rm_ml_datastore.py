#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_datastore
version_added: "3.16.0"
short_description: Create, Update, Archive, Restore an Azure Machine Learning Datastore
description:
    - Create, Update, Delete an Azure Machine Learning Datastore.
options:
    name:
        description:
            - Name of the Azure ML datastore asset.
        type: str
        required: true
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
    description:
        description:
            - Description of the datastore target.
        type: str
        required: false
    resource_definition:
        description:
            - "Local path to the YAML file containing the Azure ML
              datastore specification. The YAML reference docs for
              datastore can be found at:
              https://aka.ms/ml-cli-v2-datastore-blob-yaml-reference,
              https://aka.ms/ml-cli-v2-datastore-file-yaml-reference,
              https://aka.ms/ml-cli-v2-datastore-data-lake-gen1-yaml-reference,
              https://aka.ms/ml-cli-v2-datastore-data-lake-gen2-yaml-reference."
        type: str
        required: false
    state:
        description:
            - State of the Datastore. Use C(present) to create
              or update. C(absent) to delete.
        default: present
        type: str
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create ML Datastore
  azure.azcollection.azure_rm_ml_datastore:
    name: MyDataStore
    description: My Datastore created by Ansible
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    resource_definition: |
      FIXME.....
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
ml_datastore:
    description:
        - Datastore that was just created or updated.
    returned: always
    type: dict
    sample: {
      "account_name": "workspacstoragexxxxxxxxx",
      "container_name": "datastorexxxxxxxxx-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "credentials": {},
      "description": "here is a description",
      "endpoint": "core.windows.net",
      "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-datastore/providers/Microsoft.MachineLearningServices/workspaces/workspaceexxxxxxxx/datastores/datastorexxxxxxxxxx",
      "name": "datastorexxxxxxxxx",
      "protocol": "https",
      "tags": {},
      "type": "azure_blob",
    }
'''  # NOQA


try:
    import io
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_datastore
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLDatastore(MLClientCommon):

    UPDATE_OVERRIDES = ['description',
                        'tags'
                        ]

    PARAM_OVERRIDES = UPDATE_OVERRIDES + ['name']

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
            resource_group=dict(
                type='str',
                required=True,
            ),
            ml_workspace=dict(
                type='str',
                required=True,
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent'],
            ),
        )

        self._client = None
        self.ml_registry = None
        self.state = None

        self.results = dict(
            changed=False,
            compare=[],
            ml_datastore={}
        )

        required_if = [
            ('state', 'present', ['resource_definition'])
        ]
        super(AzureRMMLDatastore, self).__init__(self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 required_if=required_if)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        if self.resource_definition:
            resource_definition = io.StringIO(self.resource_definition)
        else:
            resource_definition = None

        changed = False
        ml_datastore_info = self.get(self.name)

        if self.state == 'present':
            if ml_datastore_info:
                # Update
                params_override = self.update_params(kwargs,
                                                     self.UPDATE_OVERRIDES,
                                                     ml_datastore_info)

                # Generate ml_datastore based on ansible args passed in.
                ml_datastore = load_datastore(None, params_override=params_override)
                ml_datastore_info = self.entity_to_dict(ml_datastore_info)
                changed = not self.default_compare({},
                                                   self.entity_to_dict(ml_datastore),
                                                   ml_datastore_info,
                                                   '',
                                                   self.results)
                if changed and not self.check_mode:
                    response = self.client.datastores.create_or_update(ml_datastore)
                    ml_datastore_info = self.entity_to_dict(response)

            else:
                # Create
                params_override = self.update_params(kwargs, self.PARAM_OVERRIDES)

                # Generate ml_datastore based on ansible args passed in.
                ml_datastore = load_datastore(resource_definition,
                                              params_override=params_override)
                changed = True
                if not self.check_mode:
                    response = self.client.datastores.create_or_update(ml_datastore)
                    ml_datastore_info = self.entity_to_dict(response)
        elif self.state == 'absent':
            # Delete
            if ml_datastore_info:
                changed = True
                if not self.check_mode:
                    self.delete(self.name)
                ml_datastore_info = self.get(self.name,
                                             as_dict=True)

        self.results['ml_datastore'] = ml_datastore_info
        self.results['changed'] = changed
        return self.results

    def update_params(self, kwargs, param_overrides, ml_datastore=None):
        params_override = []

        # If ml_datastore is defined use those values as a base.
        # Update can't change some of these values but we need
        # to keep the same values as before the update.
        if ml_datastore:
            items = self.entity_to_dict(ml_datastore).items()
            params_override = [{k: v} for k, v in items]

        # Update values based on what param_overrides says we can update.
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if kwargs[key] is not None and key in param_overrides:
                params_override.append({key: kwargs[key]})
        return params_override

    def get(self, name, as_dict=False):
        try:
            # Attempt to retrieve ml_datastore based on name
            ml_datastore_info = self.client.datastores.get(name=name,
                                                           include_secrets=False)
            if as_dict:
                ml_datastore_info = self.entity_to_dict(ml_datastore_info)
        except ResourceNotFoundError:
            ml_datastore_info = None
        except Exception as e:  # pylint: disable=broad-exception-caught
            ml_datastore_info = None
        return ml_datastore_info

    def delete(self, name=None):
        try:
            response = self.client.datastores.delete(name=name)
            return response
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error delete the data instance: {0}".format(str(e)))


def main():
    AzureRMMLDatastore()


if __name__ == '__main__':
    main()
