#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_connection
version_added: "3.19.0"
short_description: Create or Delete an Azure Machine Learning Connection
description:
    - Create or Delete an Azure Machine Learning Connection.
options:
    name:
        description:
            - Name of the Azure ML connection asset.
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
    resource_definition:
        description:
            - YAML definition containing the Azure ML Connection.
        type: str
        required: false
    populate_secrets:
        description:
            - For API key-based connections, try to populate the returned
              credentials with the actual secret value. Does nothing for
              non-API key-based connections.
        type: bool
        default: false
    state:
        description:
            - State of the Connection. Use C(present) to create.
              C(absent) to delete.
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
- name: Create GIT ML Connection
  azure.azcollection.azure_rm_ml_connection:
    name: MyGitConnection
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    resource_definition: |
      $schema: http://azureml/sdk-2-0/Connection.json
      name: test_ws_conn_git_pat
      type: git
      target: https://test-git-feed.com
      credentials:
        type: username_password
        username: dummy
        password: dummy
    tags:
      createdByToolkit: Ansible

- name: Create S3 ML Connection
  azure.azcollection.azure_rm_ml_connection:
    name: MyS3Connection
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    resource_definition: |
      $schema: http://azureml/sdk-2-0/Connection.json
      type: s3
      name: my_s3_connection
      target: <mybucket># add the s3 bucket details
      credentials:
          type: access_key
          access_key_id: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX # add access key id
          secret_access_key: XxXxXxXXXXXXXxXxXxxXxxXXXXXXXXxXxxXXxXXXXXXXxxxXxXXxXXXXXxXXxXXXxXxXxxxXXxXXxXXXXXxXxxXX # add access key secret
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
ml_connection:
    description:
        - Connection that was just created.
    returned: always
    type: dict
    sample: {
        "creation_context": {
            "created_at": "2026-05-11T20:07:52.118675+00:00",
            "created_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "created_by_type": "Application",
            "last_modified_at": "2026-05-11T20:07:52.118675+00:00",
            "last_modified_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "last_modified_by_type": "Application"
        },
        "credentials": {
            "type": "username_password"
        },
        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-connection/providers/Microsoft.MachineLearningServices/workspaces/workspacexxxxxxxxxx/connections/connectionxxxxxxxxxx",
        "is_shared": true,
        "metadata": {},
        "name": "connectionxxxxxxxxxx",
        "tags": {},
        "target": "https://test-git-feed.com",
        "type": "git"
    }
'''  # NOQA


try:
    import io
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_connection
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLConnection(MLClientCommon):

    PARAM_OVERRIDES = ['name', 'tags']

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
                required=True,
            ),
            ml_workspace=dict(
                type='str',
                required=True,
            ),
            populate_secrets=dict(
                type='bool',
                default=False,
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
            ml_connection={}
        )

        required_if = [
            ('state', 'present', ['resource_definition'])
        ]
        super(AzureRMMLConnection, self).__init__(self.module_arg_spec,
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
        ml_connection_info = self.get(self.name)

        if self.state == 'present':
            if ml_connection_info:
                # Update
                self.module.warn('No Updates are supported at this time.')
                changed = False
                ml_connection_info = self.entity_to_dict(ml_connection_info)
            else:
                # Create
                params_override = self.update_params(kwargs, self.PARAM_OVERRIDES)

                # Generate ml_connection based on ansible args passed in.
                ml_connection = load_connection(resource_definition,
                                                params_override=params_override)
                changed = True
                if not self.check_mode:
                    response = self.client.connections.create_or_update(
                        ml_connection,
                        populate_secrets=self.populate_secrets
                    )
                    ml_connection_info = self.entity_to_dict(response)
        elif self.state == 'absent':
            # Delete
            if ml_connection_info:
                changed = True
                if not self.check_mode:
                    self.delete(self.name)
                ml_connection_info = self.get(self.name,
                                              as_dict=True)

        self.results['ml_connection'] = ml_connection_info
        self.results['changed'] = changed
        return self.results

    def update_params(self, kwargs, param_overrides):
        params_override = []

        # Update values based on what param_overrides says we can update.
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if kwargs[key] is not None and key in param_overrides:
                params_override.append({key: kwargs[key]})
        return params_override

    def get(self, name, as_dict=False):
        try:
            # Attempt to retrieve ml_connection based on name
            ml_connection_info = self.client.connections.get(
                name=name,
                populate_secrets=True)
            if as_dict:
                ml_connection_info = self.entity_to_dict(ml_connection_info)
        except ResourceNotFoundError:
            ml_connection_info = None
        except Exception as e:  # pylint: disable=broad-exception-caught
            ml_connection_info = None
        return ml_connection_info

    def delete(self, name=None):
        try:
            response = self.client.connections.delete(name=name)
            return response
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error delete the data instance: {0}".format(str(e)))


def main():
    AzureRMMLConnection()


if __name__ == '__main__':
    main()
