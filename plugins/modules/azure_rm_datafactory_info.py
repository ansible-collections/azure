#!/usr/bin/python
#
# Copyright (c) 2018 Fred-sun, <xiuxi.sun@qq.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_datafactory_info
version_added: "0.1.12"
short_description: Get data factory facts
description:
    - Get facts for a specific data factory.

options:
    name:
        description:
            - The factory name.
        type: str
    resource_group:
        description:
            - Limit results by resource group. Required when using name parameter.
        type: str
    if_none_match:
        description:
            - ETag of the factory entity.
            - Should only be specified for get.
            - If the ETag matches the existing entity tag, or if * was provided, then no content will be returned.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Fred-sun (@Fred-sun)
    - xuzhang3 (@xuzhang3)
'''

EXAMPLES = '''
- name: Get data factory by name
  azure_rm_datafactory_info:
    resource_group: "{{ resource_group }}"
    name: "{{ name }}"

- name: Get data factory by resource group
  azure_rm_datafactory_info:
    resource_group: "{{ resource_group }}"

- name: Get data factory in relate subscription
  azure_rm_datafactory_info:
    tags:
      - key1
'''

RETURN = '''
datafactory:
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

AZURE_OBJECT_CLASS = 'DataFactoryInfo'


class AzureRMDataFactoryInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            if_none_match=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.results = dict(
            changed=False,
        )

        self.name = None
        self.resource_group = None
        self.if_none_match = None
        self.tags = None

        super(AzureRMDataFactoryInfo, self).__init__(self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=False,
                                                     facts_module=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        result = []

        if self.name and self.resource_group:
            result = self.get_item()
        elif self.resource_group:
            result = self.list_by_resourcegroup()
        else:
            result = self.list_all()

        self.results['datafactory'] = self.format(result)

        return self.results

    def format(self, raw):
        results = []
        for item in raw:
            if self.has_tags(item.tags, self.tags):
                results.append(self.pip_to_dict(item))
        return results

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
            repo_configuration=dict(),
            identity=dict(),
            public_network_access=pip.public_network_access,
        )
        if pip.identity:
            result['identity']['principal_id'] = pip.identity.principal_id
            result['identity']['tenant_id'] = pip.identity.tenant_id
        if pip.repo_configuration:
            result['repo_configuration']['type'] = pip.repo_configuration.type
            result['repo_configuration']['account_name'] = pip.repo_configuration.account_name
            result['repo_configuration']['repository_name'] = pip.repo_configuration.repository_name
            result['repo_configuration']['collaboration_branch'] = pip.repo_configuration.collaboration_branch
            result['repo_configuration']['root_folder'] = pip.repo_configuration.root_folder
            if pip.repo_configuration.type == "FactoryVSTSConfiguration":
                result['repo_configuration']['project_name'] = pip.repo_configuration.project_name
        return result

    def get_item(self):
        response = None
        self.log('Get properties for {0}'.format(self.name))
        try:
            response = self.datafactory_client.factories.get(self.resource_group, self.name, self.if_none_match)
        except ResourceNotFoundError:
            pass
        return [response] if response else []

    def list_by_resourcegroup(self):
        self.log("Get GitHub Access Token Response")
        try:
            response = self.datafactory_client.factories.list_by_resource_group(self.resource_group)
        except Exception:
            pass
        return response if response else []

    def list_all(self):
        self.log("Get GitHub Access Token Response")
        try:
            response = self.datafactory_client.factories.list()
        except Exception:
            pass
        return response if response else []


def main():
    AzureRMDataFactoryInfo()


if __name__ == '__main__':
    main()
