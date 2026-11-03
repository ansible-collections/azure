#!/usr/bin/python
#
# Copyright (c) 2020 Suyeb Ansari (@suyeb786)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = \
    '''
---
module: azure_rm_recoveryservicesvault_info
version_added: '1.1.0'
short_description: Get or list the Azure Recovery Services vault Details
description:
    - Get or list the Azure Recovery Services vault Details.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - If this parameter is not configured, all Vaults in the resource group are listed.
            - The name of the Azure Recovery Service Vault.
            - Azure only returns the security and redundancy settings of a vault when it is requested by name.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Suyeb Ansari (@suyeb786)
'''

EXAMPLES = '''
- name: List all Azure Recovery Services Vault in same resource group
  azure_rm_recoveryservicesvault_info:
    resource_group: 'myResourceGroup'

- name: Get Azure Recovery Services Vault Details.
  azure_rm_recoveryservicesvault_info:
    resource_group: 'myResourceGroup'
    name: 'testVault'
  register: vault_info

- name: Reuse the soft delete settings of a vault on another vault
  azure_rm_recoveryservicesvault:
    resource_group: 'myResourceGroup'
    name: 'otherVault'
    location: 'eastus'
    security_settings:
      soft_delete_settings: "{{ vault_info.recoveryservicesvaults[0].properties.security_settings.soft_delete_settings }}"
'''

RETURN = '''
response:
    description:
        - The response about the current state of the recovery services vault.
        - Deprecated, will be removed in version 5.0.0. Use RV(recoveryservicesvaults) instead, which returns the same
          information in snake_case.
    returned: always
    type: complex
    contains:
        etag:
            description:
                - A unique read-only string that changes whenever the resource create.
            returned: always
            type: str
            sample: "datetime'2020-09-16T02%3A44%3A27.834293Z'"
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample:  "/subscriptions/xxxxxxx/resourceGroups/resourcegroup_name/ \
            providers/Microsoft.RecoveryServices/vaults/rev_name"
        location:
            description:
                - The location of the resource.
            returned: always
            type: str
            sample: "eastus"
        name:
            description:
                - Name of the recovery services vault name.
            returned: always
            type: str
            sample: revault_name
        properties:
            description:
                - The recovery service vault properties.
            returned: always
            type: dict
            sample: {
                    "privateEndpointStateForBackup": "None",
                    "privateEndpointStateForSiteRecovery": "None",
                    "provisioningState": "Succeeded"
                    }
        sku:
            description:
                - The sku type of the recovery service vault.
            returned: always
            type: str
            sample: Standard
        type:
            description:
                - The type of the recovery service vault.
            returned: always
            type: str
            sample: "Microsoft.RecoveryServices/vaults"
        tags:
            description:
                - The resource tags.
            returned: when-used
            type: dict
            sample: {'key1': 'value'}
recoveryservicesvaults:
    description:
        - List of recovery services vaults, with snake_case keys.
    returned: always
    type: list
    elements: dict
    version_added: '4.2.0'
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.RecoveryServices/vaults/testVault"
        name:
            description:
                - Name of the recovery services vault.
            returned: always
            type: str
            sample: testVault
        type:
            description:
                - The type of the recovery services vault.
            returned: always
            type: str
            sample: "Microsoft.RecoveryServices/vaults"
        location:
            description:
                - The location of the resource.
            returned: always
            type: str
            sample: "eastus"
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: "W/datetime'2026-10-22T02%3A44%3A27.834293Z'"
        sku:
            description:
                - The SKU of the recovery services vault.
            returned: always
            type: dict
            sample: {"name": "Standard"}
        identity:
            description:
                - The managed identity of the recovery services vault.
            returned: when-used
            type: dict
            sample: {"type": "SystemAssigned", "principal_id": "xxxxxxx", "tenant_id": "xxxxxxx"}
        tags:
            description:
                - The resource tags.
            returned: when-used
            type: dict
            sample: {'key1': 'value'}
        properties:
            description:
                - The recovery services vault properties.
                - The settings managed by M(azure.azcollection.azure_rm_recoveryservicesvault) use the same names as its
                  options, for example C(properties.security_settings.soft_delete_settings).
            returned: always
            type: dict
            sample: {
                    "provisioning_state": "Succeeded",
                    "public_network_access": "Enabled",
                    "security_settings": {
                        "soft_delete_settings": {
                            "soft_delete_state": "AlwaysON",
                            "soft_delete_retention_period_in_days": 30,
                            "enhanced_security_state": "Enabled"
                        }
                    }
                    }
'''

try:
    from azure.core.serialization import as_attribute_dict
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


class AzureRMRecoveryServicesVaultInfo(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str'),
        )

        self.resource_group = None
        self.name = None

        self.results = dict(changed=False, recoveryservicesvaults=[])

        super(AzureRMRecoveryServicesVaultInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                               supports_check_mode=True,
                                                               supports_tags=True
                                                               )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            items = self._get()
            self.results['response'] = self._format_response(items[0])
        else:
            items = self._list_by_rg()
            self.results['response'] = dict(value=[self._format_response(i) for i in items])

        self.results['recoveryservicesvaults'] = [self._format(i) for i in items]
        self.module.deprecate("The 'response' return value is deprecated, use 'recoveryservicesvaults' instead which "
                              "returns the same information in snake_case.", version='5.0.0', collection_name='azure.azcollection')
        return self.results

    def _get(self):
        try:
            return [self.recovery_services_client.vaults.get(
                resource_group_name=self.resource_group,
                vault_name=self.name,
            )]
        except Exception as exc:
            self.fail("Error retrieving Recovery Service Vault {0}: {1}".format(self.name, str(exc)))

    def _list_by_rg(self):
        try:
            return list(self.recovery_services_client.vaults.list_by_resource_group(
                resource_group_name=self.resource_group,
            ))
        except Exception as exc:
            self.fail("Error listing Recovery Service Vaults in {0}: {1}".format(self.resource_group, str(exc)))

    def _format_response(self, item):
        return item.as_dict(exclude_readonly=False)

    def _format(self, item):
        return as_attribute_dict(item, exclude_readonly=False)


def main():
    AzureRMRecoveryServicesVaultInfo()


if __name__ == '__main__':
    main()
