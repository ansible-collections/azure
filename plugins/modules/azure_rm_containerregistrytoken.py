#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_containerregistrytoken
version_added: "3.7.0"
short_description: Managed the Azure Container Registry Token
description:
    - Create, update or delete the Container Registry Token.

options:
    resource_group:
        description:
            - The name of the resource group to which the container registry belongs.
        type: str
        required: true
    registry_name:
        description:
            - The name of the container registry.
        type: str
        required: true
    name:
        description:
            - The name of the container registry token.
        type: str
        required: true
    scope_map_id:
        description:
            - The resource ID of the scope map to which the token will be associated with.
        type: str
    status:
        description:
            - The status of the token example enabled or disabled.
        type: str
        choices:
            - enabled
            - disabled
    state:
        description:
            - Assert the state of the container registry token.
            - Use C(present) to create or update a server and C(absent) to delete it.
        default: present
        type: str
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Create a new Container Registry Token
  azure_rm_containerregistrytoken:
    resource_group: myResourceGroup
    registry_name: myRegistry
    name: mytoken
    status: enabled
    scope_map_id: scopemap_id

- name: Delete the container registry token
  azure_rm_containerregistrytoken:
    resource_group: myResourceGroup
    registry_name: myRegistry
    name: mytoken
'''

RETURN = '''
registry_token:
    description:
        - A list of dictionaries containing facts for token.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.ContainerRegistry/registries/registry01/tokens/token01"
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: token01
        registry_name:
            description:
                - The name of the container registry.
            type: str
            returned: always
            sample: registry01
        resource_group:
            description:
                - The name fo the resource group.
            type: str
            returned: always
            sample: myRG
        creation_date:
            description:
                - The creation date of scope map.
            type: str
            returned: always
            sample: '2025-07-21T03:16:03.828541Z'
        credentials:
            description:
                - The credentials that can be used for authenticating the token.
            type: str
            returned: always
            sample: {
                    "passwords": [
                        {
                            "creation_time": "2025-07-21T03:17:14.528612Z",
                            "expiry": "2026-07-22T03:17:00.551Z",
                            "name": "password1"
                        }
                    ]
                }
        provisioning_state:
            description:
                - Provisioning state of the container registry token.
            returned: always
            type: str
            sample: Succeeded
        scope_map_id:
            description:
                - The resource ID of the scope map to which the token will be associated with.
            type: str
            returned: always
            sample: "/subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.ContainerRegistry/registries/registry01/scopeMaps/map01"
        status:
            description:
                - The status of the token example enabled or disabled.
            type: str
            returned: always
            sample: enabled
        system_data:
            description:
                - Metadata pertaining to creation and last modification of the resource.
            type: dict
            returned: always
            sample: {
                    "created_at": "2025-07-21T03:16:50.586036Z",
                    "created_by": "test@domain.com",
                    "created_by_type": "User",
                    "last_modified_at": "2025-07-21T03:16:50.586036Z",
                    "last_modified_by": "test@domain.com",
                    "last_modified_by_type": "User"
                }
        type:
            description:
                - The type of the resource.
            type: str
            returned: always
            sample: 'Microsoft.ContainerRegistry/registries/tokens'
'''

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMContainerRegistryToken(AzureRMModuleBaseExt):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True,
            ),
            registry_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True,
            ),
            scope_map_id=dict(
                type='str'
            ),
            status=dict(
                type='str',
                choices=['enabled', 'disabled']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
            diff=[],
            token=None,
        )
        self.resource_group = None
        self.registry_name = None
        self.name = None
        self.status = None
        self.scope_map_id = None

        self.state = None

        super(AzureRMContainerRegistryToken, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=False)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec):
            setattr(self, key, kwargs[key])

        # Defaults for variables
        result = None

        # Get current container registry token
        old_response = self.get()

        # Create/Update if state==present
        if self.state == 'present':
            if old_response:
                # The container registry token already exists, try to update
                if self.scope_map_id is not None and self.scope_map_id.lower() != old_response['scope_map_id'].lower():
                    self.results['changed'] = True
                    self.results['diff'].append('scope_map_id')
                if self.status is not None and self.status != old_response['status'].lower():
                    self.results['changed'] = True
                    self.results['diff'].append('status')

                if self.results['changed']:
                    if self.check_mode:
                        # Check mode, skipping actual creation
                        pass
                    else:
                        result = self.update()
                else:
                    result = old_response
            else:
                self.results['changed'] = True
                # The container registry token not exist, create
                if self.check_mode:
                    # Check mode, Skipping actual creation
                    pass
                else:
                    result = self.create()
        elif self.state == 'absent' and old_response:
            self.results['changed'] = True
            if not self.check_mode:
                self.delete()
            else:
                # Do not delete in check mode
                pass

        self.results['registry_token'] = result
        return self.results

    def get(self):
        # Gets the properties of the specified token
        try:
            response = self.containerregistrytoken_client.tokens.get(resource_group_name=self.resource_group,
                                                                     registry_name=self.registry_name,
                                                                     token_name=self.name)
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.log("Could not get facts for Registry Token: {0}".format(str(e)))
            return None

        return self.format_item(response)

    def create(self):
        # Creates a token for a container registry with the specified parameters
        try:
            response = self.containerregistrytoken_client.tokens.begin_create(resource_group_name=self.resource_group,
                                                                              registry_name=self.registry_name,
                                                                              token_name=self.name,
                                                                              token_create_parameters=dict(scope_map_id=self.scope_map_id,
                                                                                                           status=self.status))
            self.log("Response: {0}".format(response))
        except Exception as e:
            self.fail("Create {0} failed. Abnormal message as {1}".format(self.name, str(e)))

        if isinstance(response, LROPoller):
            response = self.get_poller_result(response)

        return self.format_item(response)

    def update(self):
        # Updates a token with the specified parameters
        try:
            response = self.containerregistrytoken_client.tokens.begin_update(resource_group_name=self.resource_group,
                                                                              registry_name=self.registry_name,
                                                                              token_name=self.name,
                                                                              token_update_parameters=dict(scope_map_id=self.scope_map_id,
                                                                                                           status=self.status))
            self.log("Response: {0}".format(response))
        except Exception as e:
            self.fail("Update {0} failed. Abnormal message as {1}".format(self.name, str(e)))

        if isinstance(response, LROPoller):
            response = self.get_poller_result(response)

        return self.format_item(response)

    def delete(self):
        # Deletes a token from a container registry
        try:
            response = self.containerregistrytoken_client.tokens.begin_delete(resource_group_name=self.resource_group,
                                                                              registry_name=self.registry_name,
                                                                              token_name=self.name)
            self.log("Response: {0}".format(response))
        except Exception as e:
            self.fail("Deletion {0} failed. Abnormal message as {1}".format(self.name, str(e)))

        if isinstance(response, LROPoller):
            self.get_poller_result(response)

    def format_item(self, item):
        result = item.as_dict()
        result['resource_group'] = self.resource_group
        result['registry_name'] = self.registry_name

        return result


def main():
    AzureRMContainerRegistryToken()


if __name__ == '__main__':
    main()
