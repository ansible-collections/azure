#!/usr/bin/python
#
# Copyright (c) 2022 Ross Bender (@l3ender)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_containerregistrytag_info
version_added: "1.12.0"
short_description: Get Azure Container Registry tag facts
description:
    - Get facts for Container Registry tags.

options:
    registry:
        description:
            - The name of the container registry.
        type: str
        required: true
    repository_name:
        description:
            - Filter results for repository within the registry. If omitted, all repositories will be retrieved.
        type: str
    name:
        description:
            - Filter results by tags with a desired name.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Ross Bender (@l3ender)
'''

EXAMPLES = '''
- name: Get tags for all repositories in registry
  azure_rm_containerregistrytag_info:
    registry: myRegistry

- name: List tags for a specific repository
  azure_rm_containerregistrytag_info:
    registry: myRegistry
    repository_name: myRepository

- name: List tags matching a name for a specific repository
  azure_rm_containerregistrytag_info:
    registry: myRegistry
    repository_name: myRepository
    name: myTag
'''

RETURN = '''
repositories:
    description:
        - A list of dictionaries containing facts for repositories.
    returned: always
    type: complex
    contains:
        name:
            description:
                - The name of the repository.
            returned: always
            type: str
            sample: my-app
        tags:
            description:
                - A list of dictionaries for the tags in the repository.
            returned: always
            type: complex
            contains:
                name:
                    description:
                        - Name of the tag.
                    type: str
                    returned: always
                    sample: my-tag
                digest:
                    description:
                        - Digest of the tag.
                    type: str
                    returned: always
                    sample: sha256:7bd8fcb425afc34a7865f85868126e9c4fef5b2d6291986524687d289ab3a64a
                created_on:
                    description:
                        - Datetime of when the tag was created.
                    type: str
                    returned: always
                    sample: "2022-02-02T18:18:57.145778+00:00"
                last_updated_on:
                    description:
                        - Datetime of when the tag was last updated.
                    type: str
                    returned: always
                    sample: "2022-02-02T18:18:57.145778+00:00"
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.containerregistry import ContainerRegistryClient
    from azure.core.exceptions import ResourceNotFoundError
except ImportError as exc:
    # This is handled in azure_rm_common
    pass


class AzureRMContainerRegistryTagInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            registry=dict(
                type="str",
                required=True,
            ),
            repository_name=dict(
                type="str",
            ),
            name=dict(
                type="str",
            ),
        )

        self.results = dict(
            changed=False
        )

        self.registry = None
        self.repository_name = None
        self.name = None

        self._client = None

        super(AzureRMContainerRegistryTagInfo, self).__init__(self.module_arg_spec,
                                                              supports_check_mode=True,
                                                              supports_tags=False,
                                                              facts_module=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self._client = self.get_client()

        if self.repository_name and self.name:
            self.results["repositories"] = [self.get_tag(self.repository_name, self.name)]
        elif self.repository_name:
            tags = self.list_by_repository(self.repository_name, self.name)
            self.results["repositories"] = [] if not tags else [tags]
        else:
            self.results["repositories"] = self.list_all_repositories(self.name)

        return self.results

    def get_client(self):
        registry_endpoint = self.registry if self.registry.endswith(".azurecr.io") else self.registry + ".azurecr.io"
        return ContainerRegistryClient(
            endpoint=registry_endpoint,
            credential=self.azure_auth.azure_credential_track2,
            audience="https://management.azure.com",
        )

    def get_tag(self, repository_name, tag_name):
        response = None
        try:
            response = self._client.get_tag_properties(repository=repository_name, tag=tag_name)
            self.log(f"Response : {response}")
        except Exception as e:
            self.log(f"Could not get ACR tag for {repository_name}:{tag_name} - {str(e)}")

        tags = []
        if response is not None:
            tags.append(format_tag(response))

        return {
            "name": repository_name,
            "tags": tags,
        }

    def list_by_repository(self, repository_name, tag_name):
        try:
            response = self._client.list_tag_properties(repository=repository_name)
            self.log(f"Response : {response}")
            tags = []
            for tag in response:
                if not tag_name or tag.name == tag_name:
                    tags.append(format_tag(tag))

            return {
                "name": repository_name,
                "tags": tags
            }
        except ResourceNotFoundError as e:
            self.log(f"Could not get ACR tags for {repository_name} - {str(e)}")

        return None

    def list_all_repositories(self, tag_name):
        response = None
        try:
            response = self._client.list_repository_names()
            self.log(f"Response : {response}")
        except Exception as e:
            self.fail(f"Could not get ACR repositories - {str(e)}")

        if response is not None:
            results = []
            for repo_name in response:
                tags = self.list_by_repository(repo_name, tag_name)
                if tags:
                    results.append(tags)

            return results

        return None


def format_tag(tag):
    return {
        "name": tag.name,
        "digest": tag.digest,
        "created_on": tag.created_on,
        "last_updated_on": tag.last_updated_on,
    }


def main():
    AzureRMContainerRegistryTagInfo()


if __name__ == "__main__":
    main()
