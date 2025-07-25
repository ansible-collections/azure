#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_containerregistryscopemap
version_added: "3.7.0"
short_description: Managed the Azure Container Registry Scope Map
description:
    - Create, update or delete the Container Registry Scope Map.

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
        required: true
    description:
        description:
            - The user friendly description of the scope map.
        type: str
    actions:
        description:
            - The list of scoped permissions for registry artifacts.
            - Sample as C(repositories/repository-name/content/read) or C(repositories/repository-name/metadata/write).
        type: list
        elements: str
    state:
        description:
            - Assert the state of the container registry scope map.
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
- name: Get instance of Registry Scope Map
  azure_rm_containerregistryscopemap:
    resource_group: myResourceGroup
    registry_name: myRegistry
    name: myscopemap

- name: Delete the container registry scope map
  azure_rm_containerregistryscopemap:
    resource_group: myResourceGroup
    registry_name: myRegistry
    name: myscopemap
'''

RETURN = '''
scope_map:
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

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMContainerRegistryScopeMap(AzureRMModuleBaseExt):
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
            description=dict(
                type='str'
            ),
            actions=dict(
                type='list',
                elements='str'
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
            diff=None,
            scope_map=None,
        )
        self.resource_group = None
        self.registry_name = None
        self.name = None
        self.description = None
        self.state = None
        self.actions = None

        super(AzureRMContainerRegistryScopeMap, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=False)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec):
            setattr(self, key, kwargs[key])

        # Defaults for variables
        result = None
        result_compare = dict(compare=[])

        # Get current container registry token
        before_dict = self.get()

        # Create dict form input, without None value
        scope_map_template = dict(description=self.description, actions=self.actions)

        # Filter out all None values
        scope_map_input = {key: value for key, value in scope_map_template.items() if value is not None}

        # Create/Update if state==present
        if self.state == 'present':
            if before_dict:
                # The container registry already exists, try to update
                # Dict for update is the union of existing object over written by input data
                scope_map_update = before_dict | scope_map_input
                if not self.default_compare({}, scope_map_update, before_dict, '', result_compare):
                    self.results['changed'] = True
                    if self.check_mode:
                        # Check mode, skipping actual creation
                        pass
                    else:
                        result = self.update(scope_map_update)
            else:
                self.results['changed'] = True
                # The container registry scope map not exist, create
                if self.check_mode:
                    # Check mode, Skipping actual creation
                    pass
                else:
                    result = self.create(scope_map_input)
        elif self.state == 'absent' and before_dict:
            self.results['changed'] = True
            if not self.check_mode:
                self.delete()
            else:
                # Do not delete in check mode
                pass

        self.results['diff'] = result_compare
        self.results['scope_map'] = result
        return self.results

    def get(self):
        try:
            response = self.containerregistrytoken_client.scope_maps.get(resource_group_name=self.resource_group,
                                                                         registry_name=self.registry_name,
                                                                         scope_map_name=self.name)
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.log("Could not get facts for Registry Scope Map: {0}".format(str(e)))
            return None

        return self.format_item(response)

    def create(self, body):
        try:
            response = self.containerregistrytoken_client.scope_maps.begin_create(resource_group_name=self.resource_group,
                                                                                  registry_name=self.registry_name,
                                                                                  scope_map_name=self.name,
                                                                                  scope_map_create_parameters=body)
            self.log("Response: {0}".format(response))
        except Exception as e:
            self.fail("Create {0} fail. Abnormal message as {1}".format(self.name, str(e)))

        if isinstance(response, LROPoller):
            response = self.get_poller_result(response)

        return self.format_item(response)

    def update(self, body):
        try:
            response = self.containerregistrytoken_client.scope_maps.begin_update(resource_group_name=self.resource_group,
                                                                                  registry_name=self.registry_name,
                                                                                  scope_map_name=self.name,
                                                                                  scope_map_update_parameters=body)
            self.log("Response: {0}".format(response))
        except Exception as e:
            self.fail("Update {0} fail. Abnormal message as {1}".format(self.name, str(e)))

        if isinstance(response, LROPoller):
            response = self.get_poller_result(response)

        return self.format_item(response)

    def delete(self):
        try:
            response = self.containerregistrytoken_client.scope_maps.begin_delete(resource_group_name=self.resource_group,
                                                                                  registry_name=self.registry_name,
                                                                                  scope_map_name=self.name)
            self.log("Response: {0}".format(response))
        except Exception as e:
            self.fail("Deletion {0} fail. Abnormal message as {1}".format(self.name, str(e)))

        if isinstance(response, LROPoller):
            self.get_poller_result(response)

    def format_item(self, item):
        result = item.as_dict()
        result['resource_group'] = self.resource_group
        result['registry_name'] = self.registry_name

        return result


def main():
    AzureRMContainerRegistryScopeMap()


if __name__ == '__main__':
    main()
