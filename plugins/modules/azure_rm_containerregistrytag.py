#!/usr/bin/python
#
# Copyright (c) 2022 Ross Bender (@l3ender)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_containerregistrytag
version_added: "1.12.0"
short_description: Import or delete tags in Azure Container Registry
description:
    - Import or delete tags in Azure Container Registry.

options:
    resource_group:
        description:
            - The resource group of the registry.
        type: str
    registry:
        description:
            - The name of the container registry.
        type: str
        required: true
    repository_name:
        description:
            - The name of the repository within the registry.
            - Required when state = C(absent).
            - If omitted when I(state=present), the name of the source repository will be used.
        type: str
    name:
        description:
            - The name of the tag.
            - If omitted when I(state=present), the name of the source tag will be used.
            - If omitted when I(state=absent), the whole repository will be deleted.
        type: str
    source_image:
        description:
            - The source image detail. Required when I(state=present).
        type: dict
        suboptions:
            registry_uri:
                description:
                    - The address of the source registry.
                type: str
            repository:
                description:
                    - Repository name of the source image.
                type: str
                required: true
            name:
                description:
                    - Name of the tag.
                type: str
                default: latest
            credentials:
                description:
                    - Credentials for the source registry.
                type: dict
                suboptions:
                    username:
                        description:
                            - Username for the source registry.
                        type: str
                    password:
                        description:
                            - Password for the source registry.
                        type: str
    state:
        description:
            - State of the container registry tag.
            - Use C(present) to create or update a  container registry tag and use C(absent) to delete an  container registry tag.
        type: str
        default: present
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Ross Bender (@l3ender)
'''

EXAMPLES = '''
- name: Import a tag
  azure_rm_containerregistrytag:
    registry: myRegistry
    source_image:
      registry_uri: docker.io
      repository: library/hello-world
      name: latest

- name: Import a tag to a different name
  azure_rm_containerregistrytag:
    registry: myRegistry
    repository_name: app1
    name: v1
    source_image:
      registry_uri: docker.io
      repository: library/hello-world
      name: latest

- name: Delete all tags in repository
  azure_rm_containerregistrytag:
    registry: myRegistry
    repository_name: myRepository
    state: absent

- name: Delete specific tag in repository
  azure_rm_containerregistrytag:
    registry: myRegistry
    repository_name: myRepository
    name: myTag
    state: absent
'''

RETURN = '''
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, azure_id_to_dict

try:
    from azure.mgmt.containerregistry.models import ImportImageParameters, ImportSource, ImportSourceCredentials
    from azure.containerregistry import ContainerRegistryClient
except ImportError as exc:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Import, DeleteRepo, DeleteTag = range(4)


class AzureRMContainerRegistryTag(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type="str",
            ),
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
            source_image=dict(
                type="dict",
                options=dict(
                    registry_uri=dict(
                        type="str",
                    ),
                    repository=dict(
                        type="str",
                        required=True,
                    ),
                    name=dict(
                        type="str",
                        default="latest",
                    ),
                    credentials=dict(
                        type="dict",
                        options=dict(
                            username=dict(type="str"),
                            password=dict(type="str", no_log=True),
                        )
                    ),
                ),
            ),
            state=dict(
                type="str",
                default="present",
                choices=["present", "absent"],
            )
        )

        required_if = [
            ("state", "present", ["source_image"]),
            ("state", "absent", ["repository_name"]),
        ]

        self.results = dict(
            changed=True
        )

        self.resource_group = None
        self.registry = None
        self.repository_name = None
        self.name = None
        self.source_image = None
        self.state = None

        self._client = None
        self._todo = Actions.NoAction

        super(AzureRMContainerRegistryTag, self).__init__(self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=False,
                                                          facts_module=False,
                                                          required_if=required_if)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self._client = self.get_client()

        if self.state == "present":
            repo_name = self.repository_name if self.repository_name else self.source_image["repository"]
            tag_name = self.name if self.name else self.source_image["name"]
            tag = self.get_tag(repo_name, tag_name)
            if not tag:
                self._todo = Actions.Import
        elif self.state == "absent":
            if self.repository_name and self.name:
                tag = self.get_tag(self.repository_name, self.name)
                if tag:
                    self._todo = Actions.DeleteTag
            else:
                repository = self.get_repository(self.repository_name)
                if repository:
                    self._todo = Actions.DeleteRepo

        if self._todo == Actions.Import:
            self.log("importing image into registry")
            if not self.check_mode:
                self.import_tag(self.repository_name, self.name, self.resource_group, self.registry, self.source_image)
        elif self._todo == Actions.DeleteTag:
            self.log(f"deleting tag {self.repository_name}:{self.name}")
            if not self.check_mode:
                self.delete_tag(self.repository_name, self.name)
        elif self._todo == Actions.DeleteRepo:
            self.log(f"deleting repository {self.repository_name}")
            if not self.check_mode:
                self.delete_repository(self.repository_name)
        else:
            self.log("no action")
            self.results["changed"] = False

        return self.results

    def get_client(self):
        registry_endpoint = self.registry if self.registry.endswith(".azurecr.io") else self.registry + ".azurecr.io"
        return ContainerRegistryClient(
            endpoint=registry_endpoint,
            credential=self.azure_auth.azure_credential_track2,
            audience="https://management.azure.com",
        )

    def get_repository(self, repository_name):
        response = None
        try:
            response = self._client.get_repository_properties(repository=repository_name)
            self.log(f"Response : {response}")
        except Exception as e:
            self.log(f"Could not get ACR repository for {repository_name} - {str(e)}")

        if response is not None:
            return response.name

        return None

    def get_tag(self, repository_name, tag_name):
        response = None
        try:
            self.log(f"Getting tag for {repository_name}:{tag_name}")
            response = self._client.get_tag_properties(repository=repository_name, tag=tag_name)
            self.log(f"Response : {response}")
        except Exception as e:
            self.log(f"Could not get ACR tag for {repository_name}:{tag_name} - {str(e)}")

        return response

    def import_tag(self, repository, tag, resource_group, registry, source_image):
        source_tag = get_tag(source_image["repository"], source_image["name"])
        dest_repo_name = repository if repository else source_image["repository"]
        dest_tag_name = tag if tag else source_image["name"]
        dest_tag = get_tag(dest_repo_name, dest_tag_name)
        creds = None if not source_image["credentials"] else ImportSourceCredentials(
            username=source_image["credentials"]["username"],
            password=source_image["credentials"]["password"],
        )
        params = ImportImageParameters(
            target_tags=[dest_tag],
            source=ImportSource(
                registry_uri=source_image["registry_uri"],
                source_image=source_tag,
                credentials=creds,
            )
        )
        try:
            if not resource_group:
                resource_group = self.get_registry_resource_group(registry)

            self.log(f"Importing {source_tag} as {dest_tag} to {registry} in {resource_group}")
            poller = self.containerregistry_client.registries.begin_import_image(resource_group_name=resource_group,
                                                                                 registry_name=registry,
                                                                                 parameters=params)
            self.get_poller_result(poller)
        except Exception as e:
            self.fail(f"Could not import {source_tag} as {dest_tag} to {registry} in {resource_group} - {str(e)}")

    def get_registry_resource_group(self, registry_name):
        response = None
        try:
            response = self.containerregistry_client.registries.list()
        except Exception as e:
            self.fail(f"Could not load resource group for registry {registry_name} - {str(e)}")

        if response is not None:
            for item in response:
                item_dict = item.as_dict()
                if item_dict["name"] == registry_name:
                    return azure_id_to_dict(item_dict["id"]).get("resourceGroups")

        return None

    def delete_repository(self, repository_name):
        try:
            self._client.delete_repository(repository=repository_name)
        except Exception as e:
            self.fail(f"Could not delete repository {repository_name} - {str(e)}")

    def delete_tag(self, repository_name, tag_name):
        try:
            self._client.delete_tag(repository=repository_name, tag=tag_name)
        except Exception as e:
            self.fail(f"Could not delete tag {repository_name}:{tag_name} - {str(e)}")


def get_tag(repository, tag):
    return repository if not tag else repository + ":" + tag


def main():
    AzureRMContainerRegistryTag()


if __name__ == "__main__":
    main()
