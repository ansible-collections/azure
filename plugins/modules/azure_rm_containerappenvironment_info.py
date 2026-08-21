#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_containerappenvironment_info
version_added: "4.0.0"
short_description: Get facts about Azure Container Apps Managed Environments
description:
    - Get facts about one or many Azure Container Apps Managed Environments.

options:
    resource_group:
        description:
            - Name of the resource group.
            - Required when I(name) is used.
        type: str
    name:
        description:
            - Name of the managed environment. When omitted, all environments in scope are returned.
        type: str
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
- name: Get a single managed environment
  azure.azcollection.azure_rm_containerappenvironment_info:
    resource_group: myResourceGroup
    name: myenv

- name: List all environments in a resource group
  azure.azcollection.azure_rm_containerappenvironment_info:
    resource_group: myResourceGroup

- name: List all environments in the subscription
  azure.azcollection.azure_rm_containerappenvironment_info:
'''

RETURN = '''
managed_environments:
    description:
        - List of managed environments matching the filter.
    returned: always
    type: list
    elements: dict
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


def _normalize(obj):
    """
    Return a snake_case flat dict for an ``azure-mgmt-appcontainers`` model
    via the Azure SDK's official ``as_attribute_dict`` backcompat helper.
    """
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj
    return as_attribute_dict(obj, exclude_readonly=False)


class AzureRMContainerAppEnvironmentInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            tags=dict(type='list', elements='str'),
        )

        self.resource_group = None
        self.name = None
        self.tags = None

        self.results = dict(changed=False, managed_environments=[])

        super(AzureRMContainerAppEnvironmentInfo, self).__init__(
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

        self.results['managed_environments'] = [self._format(i) for i in items if self._match_tags(i)]
        return self.results

    def _get(self):
        try:
            return [self.containerapps_client.managed_environments.get(
                resource_group_name=self.resource_group,
                environment_name=self.name,
            )]
        except ResourceNotFoundError:
            return []
        except Exception as exc:
            self.fail("Error retrieving managed environment {0}: {1}".format(self.name, str(exc)))

    def _list_by_rg(self):
        try:
            return list(self.containerapps_client.managed_environments.list_by_resource_group(
                resource_group_name=self.resource_group,
            ))
        except Exception as exc:
            self.fail("Error listing managed environments in {0}: {1}".format(self.resource_group, str(exc)))

    def _list_by_sub(self):
        try:
            return list(self.containerapps_client.managed_environments.list_by_subscription())
        except Exception as exc:
            self.fail("Error listing managed environments: {0}".format(str(exc)))

    def _format(self, item):
        return _normalize(item)

    def _match_tags(self, item):
        if not self.tags:
            return True
        tags = getattr(item, 'tags', None) or {}
        return self.has_tags(tags, self.tags)


def main():
    AzureRMContainerAppEnvironmentInfo()


if __name__ == '__main__':
    main()
