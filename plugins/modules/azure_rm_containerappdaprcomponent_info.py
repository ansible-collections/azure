#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_containerappdaprcomponent_info
version_added: "4.2.0"
short_description: Get Dapr components in an Azure Container Apps managed environment
description:
    - Get details of a single Dapr component, or list all Dapr components in
      an Azure Container Apps managed environment.
options:
    resource_group:
        description:
            - Name of the resource group containing the managed environment.
        required: true
        type: str
    environment_name:
        description:
            - Name of the managed environment that hosts the Dapr components.
        required: true
        type: str
    name:
        description:
            - Name of a specific Dapr component to fetch. If omitted, all
              Dapr components in the environment are listed.
        type: str
    show_secrets:
        description:
            - Retrieve the secret values of the requested Dapr component with
              the C(listSecrets) operation.
            - Only valid when I(name) is set.
            - The retrieved values are registered with Ansible's redaction
              pool, so they never appear in module results or logs - the
              returned secret entries carry Ansible's no-log placeholder
              instead of the clear text values.
        type: bool
        default: false
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get a specific Dapr component
  azure.azcollection.azure_rm_containerappdaprcomponent_info:
    resource_group: myResourceGroup
    environment_name: myenvironment
    name: statestore
  register: component

- name: Get a Dapr component including its secret values
  azure.azcollection.azure_rm_containerappdaprcomponent_info:
    resource_group: myResourceGroup
    environment_name: myenvironment
    name: statestore
    show_secrets: true
  register: component

- name: List all Dapr components in the environment
  azure.azcollection.azure_rm_containerappdaprcomponent_info:
    resource_group: myResourceGroup
    environment_name: myenvironment
  register: components
'''

RETURN = '''
daprcomponents:
    description:
        - List of Dapr components.
        - Secret values are only included when I(show_secrets) is enabled;
          otherwise only the secret names are returned.
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "name": "statestore",
            "component_type": "state.azure.blobstorage",
            "version": "v1",
            "metadata": [{"name": "accountName", "value": "mystorageaccount"}],
            "secrets": [{"name": "storage-account-key"}],
            "scopes": ["mycontainerapp"]
        }
    ]
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


class AzureRMContainerAppDaprComponentInfo(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            environment_name=dict(type='str', required=True),
            name=dict(type='str'),
            show_secrets=dict(type='bool', default=False),
        )

        self.resource_group = None
        self.environment_name = None
        self.name = None
        self.show_secrets = False

        self.results = dict(
            changed=False,
            daprcomponents=[],
        )

        super(AzureRMContainerAppDaprComponentInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
        )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.show_secrets and not self.name:
            self.fail("show_secrets requires name to be set")

        if self.name:
            items = self._get()
        else:
            items = self._list()

        formatted = []
        for item in items:
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

        self.results['daprcomponents'] = formatted
        return self.results

    def _get(self):
        try:
            return [self.containerapps_client.dapr_components.get(
                resource_group_name=self.resource_group,
                environment_name=self.environment_name,
                component_name=self.name,
            )]
        except ResourceNotFoundError:
            return []
        except Exception as exc:
            self.fail("Error retrieving dapr component {0}: {1}".format(self.name, str(exc)))

    def _list(self):
        try:
            return list(self.containerapps_client.dapr_components.list(
                resource_group_name=self.resource_group,
                environment_name=self.environment_name,
            ))
        except Exception as exc:
            self.fail("Error listing dapr components in environment {0}: {1}".format(self.environment_name, str(exc)))

    def _list_secrets(self):
        try:
            response = self.containerapps_client.dapr_components.list_secrets(
                resource_group_name=self.resource_group,
                environment_name=self.environment_name,
                component_name=self.name,
            )
        except Exception as exc:
            self.fail("Error listing secrets for dapr component {0}: {1}".format(self.name, str(exc)))
        raw = as_attribute_dict(response, exclude_readonly=False) if response else None
        return raw.get('value', []) if raw else []

    def _format(self, item):
        normalized = as_attribute_dict(item, exclude_readonly=False) if item else None
        if normalized is None:
            return None
        # Secret values are never returned by the plain GET; strip any empty
        # placeholders so only the secret names show up.
        for secret in (normalized.get('secrets') or []):
            secret.pop('value', None)
        return normalized


def main():
    AzureRMContainerAppDaprComponentInfo()


if __name__ == '__main__':
    main()
