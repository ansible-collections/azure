#!/usr/bin/python
#
# Copyright (c) 2020 David Duque Hernández, (@next-davidduquehernandez)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_datalakestore_info
version_added: "1.4.0"
short_description: Get Azure Data Lake Store info
description:
    - Get Azure Data Lake Store info.

options:
    resource_group:
        description:
            - The name of the Azure resource group.
        type: str
        aliases:
            - resource_group_name
    name:
        description:
            - The name of the Data Lake Store account.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - David Duque Hernández (@next-davidduquehernandez)

'''

EXAMPLES = '''
  - name: Get Azure Data Lake Store info from resource group 'myResourceGroup' and name 'myDataLakeStore'
    azure_rm_datalakestore_info:
      resource_group: myResourceGroup
      name: myDataLakeStore

  - name: Get Azure Data Lake Store info from resource group 'myResourceGroup'
    azure_rm_datalakestore_info:
      resource_group: myResourceGroup

  - name: Get Azure Data Lake Store info
    azure_rm_datalakestore_info:
'''

RETURN = '''
datalake:
    description:
        - A list of dictionaries containing facts for Azure Data Lake Store.
    returned: always
    type: complex
    contains:
        account_id:
            description:
                - The unique identifier associated with this Data Lake Store account.
            returned: always
            type: str
            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        creation_time:
            description:
                - The account creation time.
            returned: always
            type: str
            sample: '2020-01-01T00:00:00.000000+00:00'
        current_tier:
            description:
                - The commitment tier in use for the current month.
            type: str
            sample: Consumption
        default_group:
            description:
                -  The default owner group for all new folders and files created in the Data Lake Store account.
            type: str
            sample: null
        encryption_config:
            description:
                - The Key Vault encryption configuration.
            type: complex
            contains:
                type:
                    description:
                        - The type of encryption configuration being used.
                    type: str
                    returned: always
                    sample: ServiceManaged
                key_vault_meta_info:
                    description:
                        - The Key Vault information for connecting to user managed encryption keys.
                    type: complex
                    contains:
                        key_vault_resource_id:
                            description:
                                - The resource identifier for the user managed Key Vault being used to encrypt.
                            type: str
                            returned: always
                            sample: /subscriptions/{subscriptionId}/resourceGroups/myRG/providers/Microsoft.KeyVault/vaults/testkv
                        encryption_key_name:
                            description:
                                - The name of the user managed encryption key.
                            type: str
                            returned: always
                            sample: KeyName
                        encryption_key_version:
                            description:
                                - The version of the user managed encryption key.
                            type: str
                            returned: always
                            sample: 86a1e3b7406f45afa0d54e21eff47e39
        encryption_provisioning_state:
            description:
                - The current state of encryption provisioning for this Data Lake Store account.
            type: str
            sample: Succeeded
        encryption_state:
            description:
                - The current state of encryption for this Data Lake Store account.
            type: str
            sample: Enabled
        endpoint:
            description:
                - The full CName endpoint for this account.
            returned: always
            type: str
            sample: testaccount.azuredatalakestore.net
        firewall_allow_azure_ips:
            description:
                - The current state of allowing or disallowing IPs originating within Azure through the firewall.
            type: str
            sample: Disabled
        firewall_rules:
            description:
                - The list of firewall rules associated with this Data Lake Store account.
            type: list
            contains:
                name:
                    description:
                        - The resource name.
                    type: str
                    returned: always
                    sample: Example Name
                start_ip_address:
                    description:
                        - The start IP address for the firewall rule.
                        - This can be either ipv4 or ipv6.
                        - Start and End should be in the same protocol.
                    type: str
                    returned: always
                    sample: 192.168.1.1
                end_ip_address:
                    description:
                        - The end IP address for the firewall rule.
                        - This can be either ipv4 or ipv6.
                        - Start and End should be in the same protocol.
                    type: str
                    returned: always
                    sample: 192.168.1.254
        firewall_state:
            description:
                - The current state of the IP address firewall for this Data Lake Store account.
            type: str
            sample: Enabled
        id:
            description:
                - The resource identifier.
            returned: always
            type: str
            sample: /subscriptions/{subscriptionId}/resourceGroups/myResourceGroup/providers/Microsoft.DataLakeStore/accounts/testaccount
        identity:
            description:
                - The Key Vault encryption identity, if any.
            type: complex
            contains:
                type:
                    description:
                        - The type of encryption being used.
                    type: str
                    sample: SystemAssigned
                principal_id:
                    description:
                        - The principal identifier associated with the encryption.
                    type: str
                    sample: 00000000-0000-0000-0000-000000000000
                tenant_id:
                    description:
                        - The tenant identifier associated with the encryption.
                    type: str
                    sample: 00000000-0000-0000-0000-000000000000
        last_modified_time:
            description:
                - The account last modified time.
            returned: always
            type: str
            sample: '2020-01-01T00:00:00.000000+00:00'
        location:
            description:
                - The resource location.
            returned: always
            type: str
            sample: westeurope
        name:
            description:
                - The resource name.
            returned: always
            type: str
            sample: testaccount
        new_tier:
            description:
                - The commitment tier to use for next month.
            type: str
            sample: Consumption
        provisioning_state:
            description:
                - The provisioning status of the Data Lake Store account.
            returned: always
            type: str
            sample: Succeeded
        state:
            description:
                - The state of the Data Lake Store account.
            returned: always
            type: str
            sample: Active
        tags:
            description:
                - The resource tags.
            returned: always
            type: dict
            sample: { "tag1":"abc" }
        trusted_id_providers:
            description:
                - The current state of the trusted identity provider feature for this Data Lake Store account.
            type: list
            contains:
                id:
                    description:
                        - The resource identifier.
                    type: str
                name:
                    description:
                        - The resource name.
                    type: str
                type:
                    description:
                        - The resource type.
                    type: str
                id_provider:
                    description:
                        - The URL of this trusted identity provider.
                    type: str
        trusted_id_provider_state:
            description:
                - The list of trusted identity providers associated with this Data Lake Store account.
            type: str
            sample: Enabled
        type:
            description:
                - The resource type.
            returned: always
            type: str
            sample: Microsoft.DataLakeStore/accounts
        virtual_network_rules:
            description:
                - The list of virtual network rules associated with this Data Lake Store account.
            type: list
            contains:
                name:
                    description:
                        - The resource name.
                    type: str
                    sample: Rule Name
                subnet_id:
                    description:
                        - The resource identifier for the subnet.
                    type: str
                    sample: /subscriptions/{subscriptionId}/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/vnet/subnets/default
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMDatalakeStoreInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str', aliases=['resource_group_name'])
        )

        self.results = dict(
            changed=False,
            datalake=[]
        )

        self.name = None
        self.resource_group = None

        super(AzureRMDatalakeStoreInfo, self).__init__(self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name and not self.resource_group:
            self.fail("Parameter error: resource group required when filtering by name.")

        results = []
        if self.name:
            results = self.get_datalake_store()
        elif self.resource_group:
            results = self.list_resource_group()
        else:
            results = self.list_all()

        self.results['datalake'] = results
        return self.results

    def get_datalake_store(self):
        self.log('Get properties for datalake store {0}'.format(self.name))
        datalake_store_obj = None

        try:
            datalake_store_obj = self.datalake_store_client.accounts.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            pass

        if datalake_store_obj:
            return [self.account_obj_to_dict(datalake_store_obj)]

        return list()

    def list_resource_group(self):
        self.log('Get basic properties for datalake store in resource group {0}'.format(self.resource_group))
        datalake_store_obj = None
        results = list()

        try:
            datalake_store_obj = self.datalake_store_client.accounts.list_by_resource_group(self.resource_group)
        except Exception:
            pass

        if datalake_store_obj:
            for datalake_item in datalake_store_obj:
                results.append(self.account_obj_to_dict_basic(datalake_item))
            return results

        return list()

    def list_all(self):
        self.log('Get basic properties for all datalake store')
        datalake_store_obj = None
        results = list()

        try:
            datalake_store_obj = self.datalake_store_client.accounts.list()
        except Exception:
            pass

        if datalake_store_obj:
            for datalake_item in datalake_store_obj:
                results.append(self.account_obj_to_dict_basic(datalake_item))
            return results

        return list()

    def account_obj_to_dict(self, datalake_store_obj):
        account_dict = dict(
            account_id=datalake_store_obj.account_id,
            creation_time=datalake_store_obj.creation_time,
            current_tier=datalake_store_obj.current_tier,
            default_group=datalake_store_obj.default_group,
            encryption_config=dict(type=datalake_store_obj.encryption_config.type,
                                   key_vault_meta_info=None),
            encryption_provisioning_state=datalake_store_obj.encryption_provisioning_state,
            encryption_state=datalake_store_obj.encryption_state,
            endpoint=datalake_store_obj.endpoint,
            firewall_allow_azure_ips=datalake_store_obj.firewall_allow_azure_ips,
            firewall_rules=None,
            firewall_state=datalake_store_obj.firewall_state,
            id=datalake_store_obj.id,
            identity=None,
            last_modified_time=datalake_store_obj.last_modified_time,
            location=datalake_store_obj.location,
            name=datalake_store_obj.name,
            new_tier=datalake_store_obj.new_tier,
            provisioning_state=datalake_store_obj.provisioning_state,
            state=datalake_store_obj.state,
            tags=datalake_store_obj.tags,
            trusted_id_providers=datalake_store_obj.trusted_id_providers,
            trusted_id_provider_state=datalake_store_obj.trusted_id_provider_state,
            type=datalake_store_obj.type,
            virtual_network_rules=None
        )

        account_dict['firewall_rules'] = list()
        for rule in datalake_store_obj.firewall_rules:
            rule_item = dict(
                name=rule.name,
                start_ip_address=rule.start_ip_address,
                end_ip_address=rule.end_ip_address
            )
            account_dict['firewall_rules'].append(rule_item)

        account_dict['virtual_network_rules'] = list()
        for vnet_rule in datalake_store_obj.virtual_network_rules:
            vnet_rule_item = dict(
                name=vnet_rule.name,
                subnet_id=vnet_rule.subnet_id
            )
            account_dict['virtual_network_rules'].append(vnet_rule_item)

        if datalake_store_obj.identity:
            account_dict['identity'] = dict(
                type=datalake_store_obj.identity.type,
                principal_id=datalake_store_obj.identity.principal_id,
                tenant_id=datalake_store_obj.identity.tenant_id
            )

        if datalake_store_obj.encryption_config.key_vault_meta_info:
            account_dict['encryption_config'] = dict(
                key_vault_meta_info=dict(
                    key_vault_resource_id=datalake_store_obj.encryption_config.key_vault_meta_info.key_vault_resource_id,
                    encryption_key_name=datalake_store_obj.encryption_config.key_vault_meta_info.encryption_key_name,
                    encryption_key_version=datalake_store_obj.encryption_config.key_vault_meta_info.encryption_key_version
                )
            )

        return account_dict

    def account_obj_to_dict_basic(self, datalake_store_obj):
        account_dict = dict(
            account_id=datalake_store_obj.account_id,
            creation_time=datalake_store_obj.creation_time,
            endpoint=datalake_store_obj.endpoint,
            id=datalake_store_obj.id,
            last_modified_time=datalake_store_obj.last_modified_time,
            location=datalake_store_obj.location,
            name=datalake_store_obj.name,
            provisioning_state=datalake_store_obj.provisioning_state,
            state=datalake_store_obj.state,
            tags=datalake_store_obj.tags,
            type=datalake_store_obj.type
        )

        return account_dict


def main():
    AzureRMDatalakeStoreInfo()


if __name__ == '__main__':
    main()
