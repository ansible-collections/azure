#!/usr/bin/python
#
# Copyright (c) 2022 Ross Bender (@l3ender)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_containerregistry_tag
version_added: "1.12.0"
short_description: Delete tags in Azure Container Registry
description:
    - Delete tags in Azure Container Registry.

options:
    registry:
        description:
            - The name or URL of the container registry.
        type: str
        required: true
    repository_name:
        description:
            - The name of the repository within the registry.
        type: str
        required: true
    name:
        description:
            - The name of the tag. If omitted, the whole repository will be updated.
        type: str
    state:
        description:
            - Assert the state of the tag. Only deleting (state = C(absent)) is supported.
        type: str
        choices:
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Ross Bender (@l3ender)
'''

EXAMPLES = '''
  - name: Delete all tags in repository
    azure_rm_containerregistry_tag:
      registry: myRegistry.azurecr.io
      repository_name: myRepository
      state: absent

  - name: Delete specific tag in repository
    azure_rm_containerregistry_tag:
      registry: myRegistry.azurecr.io
      repository_name: myRepository
      name: myTag
      state: absent
'''

RETURN = '''
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.containerregistry import ContainerRegistryClient
except ImportError as exc:
    # This is handled in azure_rm_common
    pass


class AzureRMContainerRegistryTag(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            registry=dict(
                type="str",
                required=True,
            ),
            repository_name=dict(
                type="str",
                required=True,
            ),
            name=dict(
                type="str",
            ),
            state=dict(
                type="str",
                required=True,
                choices=["absent"],
            )
        )

        self.results = dict(
            changed=False
        )

        self.registry = None
        self.repository_name = None
        self.name = None
        self.state = None

        self._client = None

        super(AzureRMContainerRegistryTag, self).__init__(self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=False,
                                                          facts_module=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self._client = self.get_client()

        repository = self.get_repository(self.repository_name)
        tag = None

        if self.name:
            tag = self.get_tag(self.repository_name, self.name)

        if self.state == "absent":
            if repository and tag:
                self.log("deleting tag {0}:{1}".format(self.repository_name, self.name))
                self.results["changed"] = True

                if self.check_mode:
                    return self.results

                self.delete_tag(self.repository_name, self.name)
            elif repository:
                self.log("deleting repository {0}".format(self.repository_name))
                self.results["changed"] = True

                if self.check_mode:
                    return self.results

                self.delete_repository(self.repository_name)

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
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.log("Could not get ACR repository for {0} - {1}".format(repository_name, str(e)))

        if response is not None:
            return response.name

        return None

    def get_tag(self, repository_name, tag_name):
        response = None
        try:
            response = self._client.get_tag_properties(repository=repository_name, tag=tag_name)
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.log("Could not get ACR tag for {0}:{1} - {2}".format(repository_name, tag_name, str(e)))

        return response

    def delete_repository(self, repository_name):
        try:
            self._client.delete_repository(repository=repository_name)
        except Exception as e:
            self.fail("Could not delete repository {0} - {1}".format(repository_name, str(e)))

    def delete_tag(self, repository_name, tag_name):
        try:
            self._client.delete_tag(repository=repository_name, tag=tag_name)
        except Exception as e:
            self.fail("Could not delete tag {0}:{1} - {2}".format(repository_name, tag_name, str(e)))


def main():
    AzureRMContainerRegistryTag()


if __name__ == "__main__":
    main()
