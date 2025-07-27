#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_containerregistrytoken_info
version_added: "3.7.0"
short_description: Get Azure Container Registry Token facts
description:
    - Get or list facts for Container Registry Token.

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

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Get instance of Registry Token
  azure_rm_containerregistrytoken_info:
    resource_group: myResourceGroup
    registry_name: myRegistry
    name: myToken

- name: List instances of Registry Token
  azure_rm_containerregistrytoken_info:
    resource_group: myResourceGroup
    registry_name: myRegistry
'''

RETURN = '''
registry_tokens:
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

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMContainerRegistryTokenInfo(AzureRMModuleBase):
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
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.registry_name = None
        self.name = None

        super(AzureRMContainerRegistryTokenInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec):
            setattr(self, key, kwargs[key])

        if self.name:
            self.results['registry_tokens'] = self.get()
        else:
            self.results['registry_tokens'] = self.list()

        return self.results

    def get(self):
        try:
            response = self.containerregistrytoken_client.tokens.get(resource_group_name=self.resource_group,
                                                                     registry_name=self.registry_name,
                                                                     token_name=self.name)
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.log("Could not get facts for Registry Token: {0}".format(str(e)))
            return []

        if response:
            return [self.format_item(response)]

    def list(self):
        response = None
        try:
            response = self.containerregistrytoken_client.tokens.list(resource_group_name=self.resource_group,
                                                                      registry_name=self.registry_name)
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.log("Could not list facts for Registry Token: {0}".format(str(e)))

        return [self.format_item(item) for item in response if response]

    def format_item(self, item):
        result = item.as_dict()
        result['resource_group'] = self.resource_group
        result['registry_name'] = self.registry_name

        return result


def main():
    AzureRMContainerRegistryTokenInfo()


if __name__ == '__main__':
    main()
