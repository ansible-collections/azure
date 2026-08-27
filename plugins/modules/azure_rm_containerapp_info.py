#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_containerapp_info
version_added: "4.0.0"
short_description: Get facts about Azure Container Apps
description:
    - Get facts about one or many Azure Container Apps.
    - Optionally include app secrets. Secret values are considered sensitive, so C(show_secrets) defaults to C(false).

options:
    resource_group:
        description:
            - Name of the resource group.
            - Required when I(name) is used.
        type: str
    name:
        description:
            - Name of the container app. When omitted, all container apps in scope are returned.
        type: str
    show_secrets:
        description:
            - When C(true) and I(name) is set, call C(list_secrets) and include the secret values in the returned payload.
        type: bool
        default: false
    tags:
        description:
            - Limit results by providing a list of tags formatted as C(key) or C(key:value).
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Get a single container app
  azure.azcollection.azure_rm_containerapp_info:
    resource_group: myResourceGroup
    name: hello

- name: Get a single container app with secrets
  azure.azcollection.azure_rm_containerapp_info:
    resource_group: myResourceGroup
    name: hello
    show_secrets: true

- name: List all container apps in a resource group
  azure.azcollection.azure_rm_containerapp_info:
    resource_group: myResourceGroup

- name: List all container apps in the subscription
  azure.azcollection.azure_rm_containerapp_info:
'''

RETURN = '''
container_apps:
    description:
        - List of container apps matching the filter.
    returned: always
    type: list
    elements: dict
    contains:
        secrets:
            description:
                - Container app secrets as returned by C(listSecrets).
                - Only present when I(show_secrets=true) and I(name) is set.
                - Values are added to Ansible's C(no_log_values) so they are
                  redacted from verbose and callback logs, but returned in the
                  module result for programmatic use.
            returned: when I(show_secrets=true) and I(name) is set
            type: list
            elements: dict
            contains:
                name:
                    description: Secret name.
                    type: str
                value:
                    description: Secret value.
                    type: str
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMContainerAppInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            show_secrets=dict(type='bool', default=False),
            tags=dict(type='list', elements='str'),
        )

        self.resource_group = None
        self.name = None
        self.show_secrets = False
        self.tags = None

        self.results = dict(changed=False, container_apps=[])

        super(AzureRMContainerAppInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True,
        )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name and not self.resource_group:
            self.fail("resource_group is required when name is specified")

        if self.name:
            items = self._get()
        elif self.resource_group:
            items = self._list_by_rg()
        else:
            items = self._list_by_sub()

        formatted = []
        for item in items:
            if self.tags and not self.has_tags(getattr(item, 'tags', None) or {}, self.tags):
                continue
            entry = self._format(item)
            if self.show_secrets and self.name:
                secrets = self._list_secrets()
                # Register secret values with Ansible's redaction pool so they
                # never appear in verbose (`-vvv`) or callback logs, even though
                # they are returned in the module result for programmatic use.
                for secret in secrets:
                    value = secret.get('value')
                    if value:
                        self.module.no_log_values.add(value)
                entry['secrets'] = secrets
            formatted.append(entry)

        self.results['container_apps'] = formatted
        return self.results

    def _get(self):
        try:
            return [self.containerapps_client.container_apps.get(
                resource_group_name=self.resource_group,
                container_app_name=self.name,
            )]
        except ResourceNotFoundError:
            return []
        except Exception as exc:
            self.fail("Error retrieving container app {0}: {1}".format(self.name, str(exc)))

    def _list_by_rg(self):
        try:
            return list(self.containerapps_client.container_apps.list_by_resource_group(
                resource_group_name=self.resource_group,
            ))
        except Exception as exc:
            self.fail("Error listing container apps in {0}: {1}".format(self.resource_group, str(exc)))

    def _list_by_sub(self):
        try:
            return list(self.containerapps_client.container_apps.list_by_subscription())
        except Exception as exc:
            self.fail("Error listing container apps: {0}".format(str(exc)))

    def _list_secrets(self):
        try:
            response = self.containerapps_client.container_apps.list_secrets(
                resource_group_name=self.resource_group,
                container_app_name=self.name,
            )
        except Exception as exc:
            self.fail("Error listing secrets for container app {0}: {1}".format(self.name, str(exc)))

        raw = as_attribute_dict(response, exclude_readonly=False) if response else None
        return raw.get('value', []) if raw else []

    def _format(self, item):
        return as_attribute_dict(item, exclude_readonly=False) if item else None


def main():
    AzureRMContainerAppInfo()


if __name__ == '__main__':
    main()
