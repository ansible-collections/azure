#!/usr/bin/python
#
# Copyright (c) 2019 Yunge Zhu, <yungez@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_keyvault_info
version_added: "0.1.2"
short_description: Get Azure Key Vault facts
description:
    - Get facts of Azure Key Vault.

options:
    resource_group:
        description:
            - The name of the resource group to which the key vault belongs.
        type: str
    name:
        description:
            - The name of the key vault.
        type: str
    hsm_name:
        description:
            - The name of the HSM.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Yunge Zhu (@yungezz)

'''

EXAMPLES = '''
- name: Get Key Vault by name
  azure_rm_keyvault_info:
    resource_group: myResourceGroup
    name: myVault

- name: List Key Vaults in specific resource group
  azure_rm_keyvault_info:
    resource_group: myResourceGroup

- name: List Key Vaults in current subscription
  azure_rm_keyvault_info:
'''

RETURN = '''
keyvaults:
    description: List of Azure Key Vaults.
    returned: always
    type: list
    contains:
        name:
            description:
                - Name of the vault.
            returned: always
            type: str
            sample: myVault
        id:
            description:
                - Resource Id of the vault.
            returned: always
            type: str
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.KeyVault/vaults/myVault
        vault_uri:
            description:
                - Vault uri.
            returned: always
            type: str
            sample: https://myVault.vault.azure.net/
        location:
            description:
                - Location of the vault.
            returned: always
            type: str
            sample: eastus
        enabled_for_deployments:
            description:
                - Whether Azure Virtual Machines are permitted to retrieve certificates stored as secrets from the key vault.
            returned: always
            type: bool
            sample: False
        enabled_for_disk_encryption:
            description:
                - Whether Azure Disk Encryption is permitted to retrieve secrets from the vault and unwrap keys.
            returned: always
            type: bool
            sample: False
        enabled_for_template_deployment:
            description:
                - Whether Azure Resource Manager is permitted to retrieve secrets from the key vault.
            returned: always
            type: bool
            sample: False
        enable_rbac_authorization:
            description:
                - Property that controls how data actions are authorized.
            returned: always
            type: bool
            sample: False
        enable_soft_delete:
            description:
                - Property to specify whether Azure Resource Manager is permitted to retrieve secrets from the key vault.
            type: bool
            returned: always
            sample: True
        enable_purge_protection:
            description:
                - Property specifying whether protection against purge is enabled for this vault.
            type: bool
            returned: always
            sample: False
        soft_delete_retention_in_days:
            description:
                - Property specifying the number of days to retain deleted vaults.
            type: int
            returned: always
            sample: 90
        tags:
            description:
                - List of tags.
            type: list
            sample:
                - foo
        sku:
            description:
                - Sku of the vault.
            returned: always
            type: dict
            contains:
                family:
                    description: Sku family name.
                    type: str
                    returned: always
                    sample: A
                name:
                    description: Sku name.
                    type: str
                    returned: always
                    sample: standard
        public_network_access:
            description:
                - Property to specify whether the vault will accept traffic from public internet.
            type: str
            returned: always
            sample: Disabled
        network_acls:
            description:
                - A collection of rules governing the accessibility of the vault from specific network locations.
            returned: always
            type: complex
            contains:
                bypass:
                    description:
                        - Tells what traffic can bypass network rules.
                    type: str
                    returned: always
                    sample: AzureServices
                default_action:
                    description:
                        - The default action when no rule from ipRules and from virtualNetworkRules match.
                    type: str
                    returned: always
                    sample: Allow
                ip_rules:
                    description:
                        - The list of IP address rules.
                    type: list
                    returned: always
                    sample: [{'value': '124.56.78.91/32'}]
                virtual_network_rules:
                    description:
                        - The list of virtual network rules.
                    type: list
                    returned: always
                    sample: [{'id': "/subscriptions/**/resourcegroups/**/providers/microsoft.network/virtualnetworks/**/subnets/subnet01",
                            'ignore_missing_vnet_service_endpoint': True}]
        access_policies:
            description:
                - List of policies.
            returned: always
            type: complex
            contains:
                object_id:
                    description: The object if of a user, service principal or security group in AAD for the vault.
                    type: str
                    returned: always
                    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                tenant_id:
                    description: The AAD tenant iD that should be used for authenticating requests to the key vault.
                    type: str
                    returned: always
                    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                permissions:
                    description: Permissions the identity has for keys, secrets and certificates.
                    type: complex
                    returned: always
                    contains:
                        key_permissions:
                            description:
                                Permissions to keys.
                            type: list
                            returned: always
                            sample:
                                - get
                                - create
                        keys:
                            description:
                                - Permissions to keys.
                                - This return value has been deprecated and will be removed in a
                                  release after 2027-05-01. Use C(key_permissions) instead.
                            type: list
                            returned: always
                            sample:
                                - get
                                - create
                        secrets:
                            description:
                                Permissions to secrets.
                            type: list
                            returned: always
                            sample:
                                - list
                                - set
                        certificates:
                            description:
                                Permissions to secrets.
                            type: list
                            returned: always
                            sample:
                                - get
                                - import
'''


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.mgmt.keyvault import KeyVaultManagementClient
    from azure.core.exceptions import ResourceNotFoundError
    from azure.mgmt.core.tools import parse_resource_id
except ImportError:
    # This is handled in azure_rm_common
    pass

KEYVAULT_RESOURCE_FILTER = "resourceType eq 'Microsoft.KeyVault/vaults'"
MANAGED_HSM_RESOURCE_FILTER = "resourceType eq 'Microsoft.KeyVault/managedHSMs'"


def _permission_value_lower(value):
    return value.lower() if isinstance(value, str) else str(value).lower()


def _get_permission_attr(permissions, *names):
    '''
    Read a permission list from SDK model or dict.

    Do not use getattr(permissions, 'keys') on a dict: that returns dict.keys (method).
    azure-mgmt-keyvault >= 13 exposes key permissions as keys_property on models.
    '''
    if not permissions:
        return None
    if isinstance(permissions, dict):
        for name in names:
            value = permissions.get(name)
            if value:
                return value
        return None
    for name in names:
        value = getattr(permissions, name, None)
        if value is None:
            continue
        if callable(value) and not isinstance(value, (list, tuple)):
            continue
        return value
    return None


def _get_keys_permissions(permissions):
    key_perms = _get_permission_attr(permissions, 'keys_property', 'key_permissions', 'keys')
    if not key_perms:
        return None
    return [_permission_value_lower(kp) for kp in key_perms]


def _permission_list_to_lower(perm_list):
    if perm_list is None:
        return None
    return [_permission_value_lower(p) for p in perm_list]


def _permissions_to_dict(permissions):
    if not permissions:
        return None
    key_perms = _get_keys_permissions(permissions)
    return dict(
        key_permissions=key_perms,
        keys=key_perms,
        secrets=_permission_list_to_lower(_get_permission_attr(permissions, 'secrets')),
        certificates=_permission_list_to_lower(_get_permission_attr(permissions, 'certificates')),
        storage=_permission_list_to_lower(_get_permission_attr(permissions, 'storage')),
    )


def keyvault_to_dict(vault):
    return dict(
        id=vault.id,
        name=vault.name,
        location=vault.location,
        tags=vault.tags,
        vault_uri=vault.properties.vault_uri,
        enabled_for_deployment=vault.properties.enabled_for_deployment,
        enabled_for_disk_encryption=vault.properties.enabled_for_disk_encryption,
        enabled_for_template_deployment=vault.properties.enabled_for_template_deployment,
        enable_soft_delete=vault.properties.enable_soft_delete,
        enable_rbac_authorization=vault.properties.enable_rbac_authorization,
        soft_delete_retention_in_days=vault.properties.soft_delete_retention_in_days
        if vault.properties.soft_delete_retention_in_days else 90,
        enable_purge_protection=vault.properties.enable_purge_protection
        if vault.properties.enable_purge_protection else False,
        access_policies=[dict(
            tenant_id=policy.tenant_id,
            object_id=policy.object_id,
            permissions=_permissions_to_dict(policy.permissions),
        ) for policy in vault.properties.access_policies] if vault.properties.access_policies else None,
        sku=dict(
            family=vault.properties.sku.family,
            name=vault.properties.sku.name
        ) if vault.properties.sku else None,
        public_network_access=vault.properties.public_network_access,
        network_acls=dict(
            bypass=vault.properties.network_acls.bypass,
            default_action=vault.properties.network_acls.default_action,
            ip_rules=[dict(
                value=item.value
            ) for item in vault.properties.network_acls.ip_rules] if vault.properties.network_acls.ip_rules else None,
            virtual_network_rules=[dict(
                id=item.id,
                ignore_missing_vnet_service_endpoint=item.ignore_missing_vnet_service_endpoint
            ) for item in vault.properties.network_acls.virtual_network_rules] if vault.properties.network_acls.virtual_network_rules else None
        ) if vault.properties.network_acls else None
    )


def hsm_to_dict(hsm):
    return dict(
        id=hsm.id,
        name=hsm.name,
        hsm_uri=hsm.properties.hsm_uri,
        location=hsm.location,
        tags=hsm.tags,
        identity=hsm.identity and hsm.identity.as_dict() or None,
        enable_soft_delete=hsm.properties.enable_soft_delete,
        soft_delete_retention_in_days=hsm.properties.soft_delete_retention_in_days
        if hsm.properties.soft_delete_retention_in_days else 90,
        enable_purge_protection=hsm.properties.enable_purge_protection
        if hsm.properties.enable_purge_protection else False,
        sku=dict(
            family=hsm.sku.family,
            name=hsm.sku.name
        )
    )


class AzureRMKeyVaultInfo(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            hsm_name=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.resource_group = None
        self.name = None
        self.hsm_name = None
        self.tags = None

        self.results = dict(changed=False)
        self._client = None

        super(AzureRMKeyVaultInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False,
                                                  facts_module=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        self.module.deprecate(
            "The 'keys' return key in 'permissions' is deprecated. Use 'key_permissions' instead.",
            date="2027-05-01",
            collection_name="azure.azcollection",
        )

        self._client = self.get_mgmt_svc_client(KeyVaultManagementClient,
                                                base_url=self._cloud_environment.endpoints.resource_manager,
                                                api_version="2026-02-01")

        if self.name:
            if self.resource_group:
                self.results['keyvaults'] = self.get_by_vault_name()
            else:
                self.fail("resource_group is required when filtering by name")
        elif self.hsm_name:
            if self.resource_group:
                self.results['hsms'] = self.get_by_hsm_name()
            else:
                self.fail("resource_group is required when filtering by hsm_name")
        elif self.resource_group:
            self.results['keyvaults'] = self.list_vault_by_resource_group()
            self.results['hsms'] = self.list_hsm_by_resource_group()
        else:
            self.results['keyvaults'] = self.list_vault()
            self.results['hsms'] = self.list_hsm()

        return self.results

    def get_by_hsm_name(self):
        '''
        Gets the properties of this specified hsm.

        :return: deserialized hsm state dictionary
        '''
        self.log("Get the hsm {0}".format(self.hsm_name))
        results = []
        try:
            response = self._client.managed_hsms.get(resource_group_name=self.resource_group, name=self.hsm_name)
            self.log("Response : {0}".format(response))
            if response and self.has_tags(response.tags, self.tags):
                results.append(hsm_to_dict(response))
        except ResourceNotFoundError as e:
            self.log("Did not find the hsm {0}: {1}".format(self.hsm_name, str(e)))
        return results

    def get_by_vault_name(self):
        '''
        Gets the properties of this specified key vault.

        :return: deserialized key vault state dictionary
        '''
        self.log("Get the key vault {0}".format(self.name))
        results = []
        try:
            response = self._client.vaults.get(resource_group_name=self.resource_group, vault_name=self.name)
            self.log("Response : {0}".format(response))
            if response and self.has_tags(response.tags, self.tags):
                results.append(keyvault_to_dict(response))
        except ResourceNotFoundError as e:
            self.log("Did not find the key vault {0}: {1}".format(self.name, str(e)))
        return results

    def _get_vault(self, resource_group_name, vault_name):
        return keyvault_to_dict(self._client.vaults.get(resource_group_name, vault_name))

    def _get_vault_from_resource_id(self, resource_id):
        parsed = parse_resource_id(resource_id)
        resource_group = parsed.get('resource_group')
        vault_name = parsed.get('name')
        if not resource_group or not vault_name:
            raise ValueError("Could not parse resource group or vault name from id: {0}".format(resource_id))
        return self._get_vault(resource_group, vault_name)

    def _iter_keyvault_resources(self, resource_group_name=None):
        '''
        Discover Key Vaults via ARM (supplemental inventory source).
        '''
        if resource_group_name:
            return self.rm_client.resources.list_by_resource_group(
                resource_group_name, filter=KEYVAULT_RESOURCE_FILTER)
        return self.rm_client.resources.list(filter=KEYVAULT_RESOURCE_FILTER)

    def _collect_vault_from_keyvault_api(self, resource_group_name, vaults_by_id):
        '''
        Same API path as "az keyvault list --resource-group".
        '''
        self.log("Listing key vaults via Key Vault API in {0}".format(resource_group_name))
        try:
            response = self._client.vaults.list_by_resource_group(resource_group_name=resource_group_name)
        except Exception as e:
            self.log("Key Vault API list failed for {0}: {1}".format(resource_group_name, str(e)))
            return

        try:
            for item in response:
                if not self.has_tags(getattr(item, 'tags', None), self.tags):
                    continue
                if item.id in vaults_by_id:
                    continue
                try:
                    vaults_by_id[item.id] = keyvault_to_dict(item)
                except Exception as e:
                    self.log("Failed to serialize key vault {0}: {1}".format(item.name, str(e)))
                    try:
                        vaults_by_id[item.id] = self._get_vault(resource_group_name, item.name)
                    except Exception as e2:
                        self.module.warn(
                            "Unable to read key vault '{0}' in resource group '{1}': {2}".format(
                                item.name, resource_group_name, str(e2)))
        except Exception as e:
            self.module.warn(
                "Key Vault API list iteration stopped early in '{0}' after {1} vault(s): {2}".format(
                    resource_group_name, len(vaults_by_id), str(e)))

    def _collect_vault_from_arm(self, resource_group_name, vaults_by_id):
        self.log("Listing key vault resources via ARM in {0}".format(
            resource_group_name or 'subscription'))
        try:
            resources = self._iter_keyvault_resources(resource_group_name)
        except Exception as e:
            self.log("Failed to list key vault resources via ARM: {0}".format(str(e)))
            return

        try:
            for resource in resources:
                if not self.has_tags(getattr(resource, 'tags', None), self.tags):
                    continue
                if resource.id in vaults_by_id:
                    continue
                try:
                    vaults_by_id[resource.id] = self._get_vault_from_resource_id(resource.id)
                except Exception as e:
                    parsed = parse_resource_id(resource.id)
                    self.module.warn(
                        "Unable to read key vault '{0}' in resource group '{1}': {2}".format(
                            parsed.get('name'), parsed.get('resource_group'), str(e)))
        except Exception as e:
            self.module.warn(
                "ARM key vault list iteration stopped early in '{0}' after {1} vault(s): {2}".format(
                    resource_group_name or 'subscription', len(vaults_by_id), str(e)))

    def _collect_keyvaults(self, resource_group_name=None):
        vaults_by_id = {}
        if resource_group_name:
            self._collect_vault_from_keyvault_api(resource_group_name, vaults_by_id)
            self._collect_vault_from_arm(resource_group_name, vaults_by_id)
        else:
            try:
                resource_groups = self.rm_client.resource_groups.list()
            except Exception as e:
                self.fail("Failed to list resource groups in subscription: {0}".format(str(e)))
            for resource_group in resource_groups:
                self._collect_vault_from_keyvault_api(resource_group.name, vaults_by_id)
            self._collect_vault_from_arm(None, vaults_by_id)
        return list(vaults_by_id.values())

    def list_vault_by_resource_group_name(self, resource_group_name):
        '''
        Lists the properties of key vaults in a resource group.

        :return: deserialized key vaults state dictionary
        '''
        self.log("Get the key vaults in resource group {0}".format(resource_group_name))
        return self._collect_keyvaults(resource_group_name=resource_group_name)

    def list_vault_by_resource_group(self):
        return self.list_vault_by_resource_group_name(self.resource_group)

    def list_vault(self):
        '''
        Lists the properties of key vaults in the subscription.

        Uses Key Vault list_by_resource_group (same as az keyvault list) plus ARM
        resource discovery to include any vaults missed by API pagination issues.

        :return: deserialized key vaults state dictionary
        '''
        self.log("Get the key vaults in current subscription")
        return self._collect_keyvaults()

    def _get_hsm_from_resource_id(self, resource_id):
        parsed = parse_resource_id(resource_id)
        resource_group = parsed.get('resource_group')
        hsm_name = parsed.get('name')
        if not resource_group or not hsm_name:
            raise ValueError("Could not parse resource group or HSM name from id: {0}".format(resource_id))
        return hsm_to_dict(self._client.managed_hsms.get(resource_group, hsm_name))

    def _iter_hsm_resources(self, resource_group_name=None):
        if resource_group_name:
            return self.rm_client.resources.list_by_resource_group(
                resource_group_name, filter=MANAGED_HSM_RESOURCE_FILTER)
        return self.rm_client.resources.list(filter=MANAGED_HSM_RESOURCE_FILTER)

    def list_hsm_by_resource_group_name(self, resource_group_name):
        '''
        Lists the properties of hsms in a resource group.

        :return: deserialized hsm state dictionary
        '''
        self.log("Get the hsms in resource group {0}".format(resource_group_name))

        results = []
        try:
            resources = self._iter_hsm_resources(resource_group_name)
        except Exception as e:
            self.log("Did not find HSM resources in resource group {0}: {1}.".format(resource_group_name, str(e)))
            return results

        for resource in resources:
            if self.has_tags(getattr(resource, 'tags', None), self.tags):
                try:
                    results.append(self._get_hsm_from_resource_id(resource.id))
                except Exception as e:
                    self.log("Failed to get HSM {0} in {1}: {2}.".format(
                        getattr(resource, 'name', resource.id), resource_group_name, str(e)))
        return results

    def list_hsm_by_resource_group(self):
        return self.list_hsm_by_resource_group_name(self.resource_group)

    def list_hsm(self):
        '''
        Lists the properties of hsms in the subscription.

        :return: deserialized hsms state dictionary
        '''
        self.log("Get the hsms in current subscription")

        results = []
        try:
            resources = self._iter_hsm_resources()
        except Exception as e:
            self.fail("Failed to list HSM resources in subscription: {0}".format(str(e)))

        for resource in resources:
            if self.has_tags(getattr(resource, 'tags', None), self.tags):
                try:
                    results.append(self._get_hsm_from_resource_id(resource.id))
                except Exception as e:
                    self.log("Failed to get HSM {0}: {1}.".format(
                        getattr(resource, 'name', resource.id), str(e)))
        return results


def main():
    """Main execution"""
    AzureRMKeyVaultInfo()


if __name__ == '__main__':
    main()
