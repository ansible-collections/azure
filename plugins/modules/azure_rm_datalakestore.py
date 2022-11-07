#!/usr/bin/python
#
# Copyright (c) 2020 David Duque Hernández, (@next-davidduquehernandez)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
module: azure_rm_datalakestore
version_added: "1.4.0"
short_description: Manage Azure data lake store
description:
    - Create, update or delete a data lake store.
options:
    default_group:
        description:
            - The default owner group for all new folders and files created in the Data Lake Store account.
        type: str
    encryption_config:
        description:
            - The Key Vault encryption configuration.
        type: dict
        suboptions:
            type:
                description:
                    - The type of encryption configuration being used.
                choices:
                    - UserManaged
                    - ServiceManaged
                required: true
                type: str
            key_vault_meta_info:
                description:
                    - The Key Vault information for connecting to user managed encryption keys.
                type: dict
                suboptions:
                    key_vault_resource_id:
                        description:
                            - The resource identifier for the user managed Key Vault being used to encrypt.
                        type: str
                        required: true
                    encryption_key_name:
                        description:
                            - The name of the user managed encryption key.
                        type: str
                        required: true
                    encryption_key_version:
                        description:
                            - The version of the user managed encryption key.
                        type: str
                        required: true
    encryption_state:
        description:
            - The current state of encryption for this Data Lake Store account.
        choices:
            - Enabled
            - Disabled
        type: str
    firewall_allow_azure_ips:
        description:
            - The current state of allowing or disallowing IPs originating within Azure through the firewall.
            - If the firewall is disabled, this is not enforced.
        choices:
            - Enabled
            - Disabled
        type: str
    firewall_rules:
        description:
            - The list of firewall rules associated with this Data Lake Store account.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The unique name of the firewall rule to create.
                type: str
                required: true
            start_ip_address:
                description:
                    - The start IP address for the firewall rule.
                    - This can be either ipv4 or ipv6.
                    - Start and End should be in the same protocol.
                type: str
                required: true
            end_ip_address:
                description:
                    - The end IP address for the firewall rule.
                    - This can be either ipv4 or ipv6.
                    - Start and End should be in the same protocol.
                type: str
                required: true
    firewall_state:
        description:
            - The current state of the IP address firewall for this Data Lake Store account.
        choices:
            - Enabled
            - Disabled
        type: str
    identity:
        description:
            - The Key Vault encryption identity, if any.
        choices:
            - SystemAssigned
        type: str
    location:
        description:
            - The resource location.
        type: str
    name:
        description:
            - The name of the Data Lake Store account.
        type: str
        required: true
    new_tier:
        description:
            - The commitment tier to use for next month.
        choices:
            - Consumption
            - Commitment_1TB
            - Commitment_10TB
            - Commitment_100TB
            - Commitment_500TB
            - Commitment_1PB
            - Commitment_5PB
        type: str
    resource_group:
        description:
            - The name of the Azure resource group to use.
        required: true
        type: str
        aliases:
            - resource_group_name
    state:
        description:
            - State of the data lake store. Use C(present) to create or update a data lake store and use C(absent) to delete it.
        default: present
        choices:
            - absent
            - present
        type: str
    virtual_network_rules:
        description:
            - The list of virtual network rules associated with this Data Lake Store account.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The unique name of the virtual network rule to create.
                type: str
                required: true
            subnet_id:
                description:
                    - The resource identifier for the subnet.
                type: str
                required: true

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - David Duque Hernández (@next-davidduquehernandez)
'''

EXAMPLES = '''
  - name: Create Azure Data Lake Store
    azure_rm_datalakestore:
      resource_group: myResourceGroup
      name: myDataLakeStore
'''

RETURN = '''
state:
    description:
        - Facts for Azure Data Lake Store created/updated.
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
            returned: always
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
                            sample: /subscriptions/{subscriptionId}/resourceGroups/myResourceGroup/providers/Microsoft.KeyVault/vaults/tstkv
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
            returned: always
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
                - If the firewall is disabled, this is not enforced.
            type: str
            returned: always
            sample: Disabled
        firewall_rules:
            description:
                - The list of firewall rules associated with this Data Lake Store account.
            type: list
            returned: always
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
            returned: always
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
            returned: always
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
            returned: always
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
            returned: always
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
            returned: always
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
                    sample: /subscriptions/{subscriptionId}/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/vnet/subnets/default

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
import datetime

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass

firewall_rules_item = dict(
    name=dict(type='str', required=True),
    start_ip_address=dict(type='str', required=True),
    end_ip_address=dict(type='str', required=True)
)

virtual_network_rules_item = dict(
    name=dict(type='str', required=True),
    subnet_id=dict(type='str', required=True)
)


class AzureRMDatalakeStore(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            default_group=dict(type='str'),
            encryption_config=dict(
                type='dict',
                options=dict(
                    type=dict(type='str', choices=['UserManaged', 'ServiceManaged'], required=True),
                    key_vault_meta_info=dict(
                        type='dict',
                        no_log=True,
                        options=dict(
                            key_vault_resource_id=dict(type='str', required=True),
                            encryption_key_name=dict(type='str', required=True),
                            encryption_key_version=dict(type='str', no_log=True, required=True)
                        )
                    ),
                )
            ),
            encryption_state=dict(type='str', choices=['Enabled', 'Disabled']),
            firewall_allow_azure_ips=dict(type='str', choices=['Enabled', 'Disabled']),
            firewall_rules=dict(
                type='list',
                elements='dict',
                options=firewall_rules_item
            ),
            firewall_state=dict(type='str', choices=['Enabled', 'Disabled']),
            identity=dict(type='str', choices=['SystemAssigned']),
            location=dict(type='str'),
            name=dict(type='str', required=True),
            new_tier=dict(type='str', choices=['Consumption', 'Commitment_1TB', 'Commitment_10TB', 'Commitment_100TB',
                                               'Commitment_500TB', 'Commitment_1PB', 'Commitment_5PB']),
            resource_group=dict(type='str', required=True, aliases=['resource_group_name']),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            tags=dict(type='dict'),
            virtual_network_rules=dict(
                type='list',
                elements='dict',
                options=virtual_network_rules_item
            ),
        )

        self.state = None
        self.name = None
        self.resource_group = None
        self.location = None
        self.tags = None
        self.new_tier = None
        self.default_group = None
        self.encryption_config = dict()
        self.encryption_config_model = None
        self.encryption_state = None
        self.firewall_state = None
        self.firewall_allow_azure_ips = None
        self.firewall_rules = None
        self.firewall_rules_model = None
        self.virtual_network_rules = None
        self.virtual_network_rules_model = None
        self.identity = None
        self.identity_model = None

        self.results = dict(changed=False)
        self.account_dict = None

        super(AzureRMDatalakeStore, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=False,
                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        if self.encryption_config:
            key_vault_meta_info_model = None
            if self.encryption_config.get('key_vault_meta_info'):
                key_vault_meta_info_model = self.datalake_store_models.KeyVaultMetaInfo(
                    key_vault_resource_id=self.encryption_config.get('key_vault_meta_info').get('key_vault_resource_id'),
                    encryption_key_name=self.encryption_config.get('key_vault_meta_info').get('encryption_key_name'),
                    encryption_key_version=self.encryption_config.get('key_vault_meta_info').get('encryption_key_version')
                )
            self.encryption_config_model = self.datalake_store_models.EncryptionConfig(type=self.encryption_config.get('type'),
                                                                                       key_vault_meta_info=key_vault_meta_info_model)

        if self.identity is not None:
            self.identity_model = self.datalake_store_models.EncryptionIdentity(
                type=self.identity
            )

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        self.account_dict = self.get_datalake_store()

        if self.account_dict is not None:
            self.results['state'] = self.account_dict
        else:
            self.results['state'] = dict()

        if self.state == 'present':
            if not self.account_dict:
                self.results['state'] = self.create_datalake_store()
            else:
                self.results['state'] = self.update_datalake_store()
        else:
            self.delete_datalake_store()
            self.results['state'] = dict(state='Deleted')

        return self.results

    def check_name_availability(self):
        self.log('Checking name availability for {0}'.format(self.name))
        try:
            response = self.datalake_store_client.accounts.check_name_availability(self.location, parameters={'name': self.name})
        except Exception as e:
            self.log('Error attempting to validate name.')
            self.fail("Error checking name availability: {0}".format(str(e)))
        if not response.name_available:
            self.log('Error name not available.')
            self.fail("{0} - {1}".format(response.message, response.reason))

    def create_datalake_store(self):
        self.log("Creating datalake store {0}".format(self.name))

        if not self.location:
            self.fail('Parameter error: location required when creating a datalake store account.')

        self.check_name_availability()
        self.results['changed'] = True

        if self.check_mode:
            account_dict = dict(
                name=self.name,
                resource_group=self.resource_group,
                location=self.location
            )
            return account_dict

        if self.firewall_rules is not None:
            self.firewall_rules_model = list()
            for rule in self.firewall_rules:
                rule_model = self.datalake_store_models.CreateFirewallRuleWithAccountParameters(
                    name=rule.get('name'),
                    start_ip_address=rule.get('start_ip_address'),
                    end_ip_address=rule.get('end_ip_address'))
                self.firewall_rules_model.append(rule_model)

        if self.virtual_network_rules is not None:
            self.virtual_network_rules_model = list()
            for vnet_rule in self.virtual_network_rules:
                vnet_rule_model = self.datalake_store_models.CreateVirtualNetworkRuleWithAccountParameters(
                    name=vnet_rule.get('name'),
                    subnet_id=vnet_rule.get('subnet_id'))
                self.virtual_network_rules_model.append(vnet_rule_model)

        parameters = self.datalake_store_models.CreateDataLakeStoreAccountParameters(
            default_group=self.default_group,
            encryption_config=self.encryption_config_model,
            encryption_state=self.encryption_state,
            firewall_allow_azure_ips=self.firewall_allow_azure_ips,
            firewall_rules=self.firewall_rules_model,
            firewall_state=self.firewall_state,
            identity=self.identity_model,
            location=self.location,
            new_tier=self.new_tier,
            tags=self.tags,
            virtual_network_rules=self.virtual_network_rules_model
        )

        self.log(str(parameters))
        try:
            poller = self.datalake_store_client.accounts.begin_create(self.resource_group, self.name, parameters)
            self.get_poller_result(poller)
        except Exception as e:
            self.log('Error creating datalake store.')
            self.fail("Failed to create datalake store: {0}".format(str(e)))

        return self.get_datalake_store()

    def update_datalake_store(self):
        self.log("Updating datalake store {0}".format(self.name))

        parameters = self.datalake_store_models.UpdateDataLakeStoreAccountParameters()

        if self.tags:
            update_tags, self.account_dict['tags'] = self.update_tags(self.account_dict['tags'])
            if update_tags:
                self.results['changed'] = True
                parameters.tags = self.account_dict['tags']

        if self.new_tier and self.account_dict.get('new_tier') != self.new_tier:
            self.results['changed'] = True
            parameters.new_tier = self.new_tier

        if self.default_group and self.account_dict.get('default_group') != self.default_group:
            self.results['changed'] = True
            parameters.default_group = self.default_group

        if self.encryption_state and self.account_dict.get('encryption_state') != self.encryption_state:
            self.fail("Encryption type cannot be updated.")

        if self.encryption_config:
            if (
                self.encryption_config.get('type') == 'UserManaged'
                and self.encryption_config.get('key_vault_meta_info') != self.account_dict.get('encryption_config').get('key_vault_meta_info')
            ):
                self.results['changed'] = True
                key_vault_meta_info_model = self.datalake_store_models.UpdateKeyVaultMetaInfo(
                    encryption_key_version=self.encryption_config.get('key_vault_meta_info').get('encryption_key_version')
                )
                encryption_config_model = self.datalake_store_models.UpdateEncryptionConfig = key_vault_meta_info_model
                parameters.encryption_config = encryption_config_model

        if self.firewall_state and self.account_dict.get('firewall_state') != self.firewall_state:
            self.results['changed'] = True
            parameters.firewall_state = self.firewall_state

        if self.firewall_allow_azure_ips and self.account_dict.get('firewall_allow_azure_ips') != self.firewall_allow_azure_ips:
            self.results['changed'] = True
            parameters.firewall_allow_azure_ips = self.firewall_allow_azure_ips

        if self.firewall_rules is not None:
            if not self.compare_lists(self.firewall_rules, self.account_dict.get('firewall_rules')):
                self.firewall_rules_model = list()
                for rule in self.firewall_rules:
                    rule_model = self.datalake_store_models.UpdateFirewallRuleWithAccountParameters(
                        name=rule.get('name'),
                        start_ip_address=rule.get('start_ip_address'),
                        end_ip_address=rule.get('end_ip_address'))
                    self.firewall_rules_model.append(rule_model)
                self.results['changed'] = True
                parameters.firewall_rules = self.firewall_rules_model

        if self.virtual_network_rules is not None:
            if not self.compare_lists(self.virtual_network_rules, self.account_dict.get('virtual_network_rules')):
                self.virtual_network_rules_model = list()
                for vnet_rule in self.virtual_network_rules:
                    vnet_rule_model = self.datalake_store_models.UpdateVirtualNetworkRuleWithAccountParameters(
                        name=vnet_rule.get('name'),
                        subnet_id=vnet_rule.get('subnet_id'))
                    self.virtual_network_rules_model.append(vnet_rule_model)
                self.results['changed'] = True
                parameters.virtual_network_rules = self.virtual_network_rules_model

        if self.identity_model is not None:
            self.results['changed'] = True
            parameters.identity = self.identity_model

        self.log(str(parameters))
        if self.results['changed']:
            try:
                poller = self.datalake_store_client.accounts.begin_update(self.resource_group, self.name, parameters)
                self.get_poller_result(poller)
            except Exception as e:
                self.log('Error creating datalake store.')
                self.fail("Failed to create datalake store: {0}".format(str(e)))

        return self.get_datalake_store()

    def delete_datalake_store(self):
        self.log('Delete datalake store {0}'.format(self.name))

        self.results['changed'] = True if self.account_dict is not None else False
        if not self.check_mode and self.account_dict is not None:
            try:
                status = self.datalake_store_client.accounts.begin_delete(self.resource_group, self.name)
                self.log("delete status: ")
                self.log(str(status))
            except Exception as e:
                self.fail("Failed to delete datalake store: {0}".format(str(e)))

        return True

    def get_datalake_store(self):
        self.log('Get properties for datalake store {0}'.format(self.name))
        datalake_store_obj = None
        account_dict = None

        try:
            datalake_store_obj = self.datalake_store_client.accounts.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            pass

        if datalake_store_obj:
            account_dict = self.account_obj_to_dict(datalake_store_obj)

        return account_dict

    def account_obj_to_dict(self, datalake_store_obj):
        account_dict = dict(
            account_id=datalake_store_obj.account_id,
            creation_time=datalake_store_obj.creation_time,
            current_tier=datalake_store_obj.current_tier,
            default_group=datalake_store_obj.default_group,
            encryption_config=None,
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
        if datalake_store_obj.firewall_rules:
            for rule in datalake_store_obj.firewall_rules:
                rule_item = dict(
                    name=rule.name,
                    start_ip_address=rule.start_ip_address,
                    end_ip_address=rule.end_ip_address
                )
                account_dict['firewall_rules'].append(rule_item)

        account_dict['virtual_network_rules'] = list()
        if datalake_store_obj.virtual_network_rules:
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

        if datalake_store_obj.encryption_config:
            if datalake_store_obj.encryption_config.key_vault_meta_info:
                account_dict['encryption_config'] = dict(
                    key_vault_meta_info=dict(
                        key_vault_resource_id=datalake_store_obj.encryption_config.key_vault_meta_info.key_vault_resource_id,
                        encryption_key_name=datalake_store_obj.encryption_config.key_vault_meta_info.encryption_key_name,
                        encryption_key_version=datalake_store_obj.encryption_config.key_vault_meta_info.encryption_key_version
                    )
                )

        return account_dict

    def compare_lists(self, list1, list2):
        if len(list1) != len(list2):
            return False
        for element in list1:
            if element not in list2:
                return False
        return True


def main():
    AzureRMDatalakeStore()


if __name__ == '__main__':
    main()
