#!/usr/bin/python
#
# Copyright (c) 2018 Fred-sun, <xiuxi.sun@qq.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_datafactory

version_added: "0.1.12"

short_description: Managed data factory

description:
    - Create, update or delete data factory.

options:
    name:
        description:
            - The factory name.
        type: str
        required: true
    resource_group:
        description:
            - Limit results by resource group. Required when using name parameter.
        type: str
        required: true
    if_match:
        description:
            - ETag of the factory entity.
            - Should only be specified for get.
            - If the ETag matches the existing entity tag, or if * was provided, then no content will be returned.
        type: str
    repo_configuration:
        description:
            - The data factory repo configration.
        type: dict
        suboptions:
            type:
                description:
                    - Type of repo configuration.
                type: str
                required: True
                choices:
                    - FactoryGitHubConfiguration
                    - FactoryVSTSConfiguration
            account_name:
                description:
                    - Account name.
                type: str
                required: True
            collaboration_branch:
                description:
                    - Collaboration branch.
                type: str
                required: True
            root_folder:
                description:
                    - Root folder.
                type: str
                required: True
            repository_name:
                description:
                    - Repository name.
                type: str
                required: True
            project_name:
                description:
                    - VSTS project name.
                    - Required when I(type=FactoryVSTSConfiguration).
                type: str
    location:
        description:
            - Valid Azure location. Defaults to location of the resource group.
        type: str
    public_network_access:
        description:
            - Whether or not public network access is allowed for the data factory.
        type: str
        choices:
            - Enabled
            - Disabled
    state:
        description:
            - Assert the state of the Public IP. Use C(present) to create or update a and C(absent) to delete.
        default: present
        choices:
            - absent
            - present
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Fred-sun (@Fred-sun)
    - xuzhang3 (@xuzhang3)
'''

EXAMPLES = '''
- name: Create the data factory
  azure_rm_datafactory:
    resource_group: "{{ resource_group }}"
    name: "{{ name }}"
    repo_configuration:
      type: FactoryGitHubConfiguration
      account_name: Fred-sun
      collaboration_branch: testbranch
      root_folder: "./"
      repository_name: vault
'''

RETURN = '''
state:
    description:
        - Current state fo the data factory.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The data facotry ID.
            type: str
            returned: always
            sample: "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.DataFactory/factories/testpro"
        create_time:
            description:
                - Time the factory was created in ISO8601 format.
            type: str
            returned: always
            sample: "2022-04-26T08:24:41.391164+00:00"
        location:
            description:
                - The resource location.
            type: str
            returned: always
            sample: eastus
        name:
            description:
                - The resource name.
            type: str
            returned: always
            sample: testfactory
        provisioning_state:
            description:
                - Factory provisioning state, example Succeeded.
            type: str
            returned: always
            sample: Succeeded
        e_tag:
            description:
                - Etag identifies change in the resource.
            type: str
            returned: always
            sample: "3000fa80-0000-0100-0000-6267ac490000"
        type:
            description:
                - The resource type.
            type: str
            returned: always
            sample: "Microsoft.DataFactory/factories"
        public_network_access:
            description:
                - Whether or not public network access is allowed for the data factory.
            type: str
            returned: always
            sample: "Enabled"
        tags:
            description:
                - List the data factory tags.
            type: str
            returned: always
            sample: {'key1':'value1'}
        identity:
            description:
                -  Managed service identity of the factory.
            type: str
            returned: always
            contains:
                principal_id:
                    description:
                        - The principal id of the identity.
                    type: str
                    returned: always
                    sample: "***********"
                tenant_id:
                    description:
                        - The client tenant id of the identity.
                    type: str
                    returned: always
                    sample: "***********"
        repo_configuration:
            description:
                - Git repo information of the factory.
            type: str
            returned: always
            contains:
                type:
                    description:
                        - Type of repo configuration.
                    type: str
                    returned: always
                    sample: FactoryGitHubConfiguration
                ccount_name:
                    description:
                        - Account name.
                    type: str
                    returned: always
                    sample: fredaccount
                collaboration_branch:
                    description:
                        - Collaboration branch.
                    type: str
                    returned: always
                    sample: branch
                repository_name:
                    description:
                        - Repository name.
                    type: str
                    returned: always
                    sample:  "vault"
                root_folder:
                    description:
                        - Root folder.
                    type: str
                    returned: always
                    sample: "/home/"
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

AZURE_OBJECT_CLASS = 'DataFactory'

repo_configuration_spec = dict(
    type=dict(type='str', required=True, choices=['FactoryVSTSConfiguration', 'FactoryGitHubConfiguration']),
    account_name=dict(type='str', required=True),
    repository_name=dict(type='str', required=True),
    collaboration_branch=dict(type='str', required=True),
    root_folder=dict(type='str', required=True),
    project_name=dict(type='str'),
)


class AzureRMDataFactory(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            if_match=dict(type='str'),
            location=dict(type='str'),
            public_network_access=dict(type='str', choices=["Enabled", "Disabled"]),
            state=dict(type='str', default='present', choices=['absent', 'present']),
            repo_configuration=dict(type='dict', options=repo_configuration_spec),
        )

        self.results = dict(
            changed=False,
        )

        self.name = None
        self.resource_group = None
        self.if_match = None
        self.location = None
        self.tags = None
        self.public_network_access = None
        self.repo_configuration = None

        super(AzureRMDataFactory, self).__init__(self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True,
                                                 facts_module=False)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        response = self.get_item()
        changed = False
        if self.state == 'present':
            if response:
                if self.tags is not None:
                    update_tags, tags = self.update_tags(response['tags'])
                    if update_tags:
                        changed = True
                        self.tags = tags
                if self.public_network_access is not None and self.public_network_access != response['public_network_access']:
                    changed = True
                else:
                    self.public_network_access = response['public_network_access']

                if self.repo_configuration is not None and self.repo_configuration != response['repo_configuration']:
                    changed = True
                else:
                    self.repo_configuration = response['repo_configuration']
            else:
                changed = True

            if self.check_mode:
                changed = True
                self.log("Check mode test, Data factory will be create or update")
            else:
                if changed:
                    if self.repo_configuration:
                        if self.repo_configuration['type'] == 'FactoryGitHubConfiguration':
                            repo_parameters = self.datafactory_model.FactoryGitHubConfiguration(
                                account_name=self.repo_configuration.get('account_name'),
                                repository_name=self.repo_configuration.get('repository_name'),
                                collaboration_branch=self.repo_configuration.get('collaboration_branch'),
                                root_folder=self.repo_configuration.get('root_folder')
                            )
                        else:
                            repo_parameters = self.datafactory_model.FactoryVSTSConfiguration(
                                account_name=self.repo_configuration.get('account_name'),
                                repository_name=self.repo_configuration.get('repository_name'),
                                collaboration_branch=self.repo_configuration.get('collaboration_branch'),
                                root_folder=self.repo_configuration.get('root_folder'),
                                project_name=self.repo_configuration.get('project_name'),
                            )
                    else:
                        repo_parameters = None

                    update_parameters = self.datafactory_model.Factory(
                        location=self.location,
                        tags=self.tags,
                        public_network_access=self.public_network_access,
                        repo_configuration=repo_parameters
                    )

                    response = self.create_or_update(update_parameters)

        else:
            if self.check_mode:
                changed = True
                self.log("Check mode test")
            if response:
                self.log("The Data factory {0} exist, will be deleted".format(self.name))
                changed = True
                response = self.delete()
            else:
                changed = False

        self.results['changed'] = changed
        self.results['state'] = response
        return self.results

    def get_item(self):
        response = None
        self.log('Get properties for {0}'.format(self.name))
        try:
            response = self.datafactory_client.factories.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            pass
        return self.pip_to_dict(response) if response else None

    def delete(self):
        response = None
        self.log('Delete data factory for {0}'.format(self.name))
        try:
            response = self.datafactory_client.factories.delete(self.resource_group, self.name)
        except Exception as ec:
            self.fail("Delete fail {0}, error message {1}".format(self.name, ec))
        return self.pip_to_dict(response) if response else None

    def create_or_update(self, parameters):
        response = None
        self.log('Create data factory for {0}'.format(self.name))
        try:
            response = self.datafactory_client.factories.create_or_update(self.resource_group,
                                                                          self.name,
                                                                          parameters,
                                                                          self.if_match)
        except Exception as ec:
            self.fail("Create fail {0}, error message {1}".format(self.name, ec))
        return self.pip_to_dict(response) if response else None

    def pip_to_dict(self, pip):
        result = dict(
            id=pip.id,
            name=pip.name,
            type=pip.type,
            location=pip.location,
            tags=pip.tags,
            e_tag=pip.e_tag,
            provisioning_state=pip.provisioning_state,
            create_time=pip.create_time,
            public_network_access=pip.public_network_access,
            repo_configuration=dict(),
            identity=dict()
        )
        if pip.identity:
            result['identity']['principal_id'] = pip.identity.principal_id
            result['identity']['tenant_id'] = pip.identity.tenant_id
        if pip.repo_configuration:
            result['repo_configuration']['account_name'] = pip.repo_configuration.account_name
            result['repo_configuration']['repository_name'] = pip.repo_configuration.repository_name
            result['repo_configuration']['collaboration_branch'] = pip.repo_configuration.collaboration_branch
            result['repo_configuration']['root_folder'] = pip.repo_configuration.root_folder
            result['repo_configuration']['type'] = pip.repo_configuration.type
            if pip.repo_configuration.type == "FactoryVSTSConfiguration":
                result['repo_configuration']['project_name'] = pip.repo_configuration.project_name
        return result


def main():
    AzureRMDataFactory()


if __name__ == '__main__':
    main()
