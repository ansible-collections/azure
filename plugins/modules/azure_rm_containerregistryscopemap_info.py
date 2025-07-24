#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_containerregistryscopemap_info
version_added: "3.7.0"
short_description: Get Azure Container Registry Scope Map facts
description:
    - Get or list facts for Container Registry Scope Map.

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
            - The name of the container registry scope map.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Get instance of Registry Scope Map
  azure_rm_containerregistryscopemap_info:
    resource_group: myResourceGroup
    registry_name: myRegistry
    name: myscopemap

- name: List instances of Registry Scope Map
  azure_rm_containerregistryscopemap_info:
    resource_group: myResourceGroup
    registry_name: myRegistry
'''

RETURN = '''
registry_scope_maps:
    description:
        - A list of dictionaries containing facts for scope map.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.ContainerRegistry/registries/acr01/scopeMaps/map01"
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: map01
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
        actions:
            description:
                - The list of scoped permissions for registry artifacts.
            type: list
            returned: always
            sample: ["repositories/test01/content/read"]
        creation_date:
            description:
                - The creation date of scope map.
            type: str
            returned: always
            sample: "2025-07-21T03:15:59.951533Z"
        description:
            description:
                - The user friendly description of the scope map.
            type: str
            returned: always
            sample: "Just for test"
        provisioning_state:
            description:
                - Provisioning state of the resource.
            type: str
            returned: always
            sample: Success
        system_data:
            description:
                - Metadata pertaining to creation and last modification of the resource.
            type: str
            returned: always
            sample: {
                    "created_at": "2025-07-21T03:15:59.287282Z",
                    "created_by": "v-xisu@microsoft.com",
                    "created_by_type": "User",
                    "last_modified_at": "2025-07-21T03:15:59.287282Z",
                    "last_modified_by": "v-xisu@microsoft.com",
                    "last_modified_by_type": "User"
                }
        type:
            description:
                - The type of the resource.
            type: str
            returned: always
            sample: 'Microsoft.ContainerRegistry/registries/scopeMaps'
        type_properties_type:
            description:
                - The type of the scope map.
            type: str
            returned: always
            sample: UserDefined
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMContainerRegistryScopeMapInfo(AzureRMModuleBase):
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

        super(AzureRMContainerRegistryScopeMapInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec):
            setattr(self, key, kwargs[key])

        if self.name:
            self.results['registry_scope_maps'] = self.get()
        else:
            self.results['registry_scope_maps'] = self.list()

        return self.results

    def get(self):
        try:
            response = self.containerregistrytoken_client.scope_maps.get(resource_group_name=self.resource_group,
                                                                         registry_name=self.registry_name,
                                                                         scope_map_name=self.name)
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.log("Could not get facts for Registry Scope Map: {0}".format(str(e)))
            return []

        return [self.format_item(response)]

    def list(self):
        response = None
        try:
            response = self.containerregistrytoken_client.scope_maps.list(resource_group_name=self.resource_group,
                                                                          registry_name=self.registry_name)
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.log("Could not list facts for Registry Scope Map: {0}".format(str(e)))

        return [self.format_item(item) for item in response if response]

    def format_item(self, item):
        result = item.as_dict()
        result['resource_group'] = self.resource_group
        result['registry_name'] = self.registry_name

        return result


def main():
    AzureRMContainerRegistryScopeMapInfo()


if __name__ == '__main__':
    main()
