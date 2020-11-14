#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import datetime

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''

'''

EXAMPLES = '''
'''

RETURN = '''

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDatalakeStore(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            default_group=dict(type='str'),
            encryption_config=dict(
                type='dict',
                options=dict(
                    type=dict(type='str', choices=['UserManaged', 'ServiceManaged']),
                    key_vault_meta_info=dict(
                        type='dict', 
                        options=dict(
                            key_vault_resource_id=dict(type='str',required=True),
                            encryption_key_name=dict(type='str',required=True),
                            encryption_key_version=dict(type='str')
                        )
                    ),
                )
            ),
            encryption_state=dict(type='str', choices=['Enabled', 'Disabled']),
            firewall_allow_azure_ips=dict(type='str', choices=['Enabled', 'Disabled']),
            firewall_rules=dict(
                type='list',
                options=dict(
                    name=dict(type='str',required=True),
                    start_ip_address=dict(type='str',required=True),
                    end_ip_address=dict(type='str',required=True)
                )
            ),
            firewall_state=dict(type='str', choices=['Enabled', 'Disabled']),
            location=dict(type='str'),
            name=dict(type='str',required=True),
            new_tier=dict(type='str', choices=['Consumption', 'Commitment_1TB', 'Commitment_10TB', 'Commitment_100TB', 'Commitment_500TB', 'Commitment_1PB', 'Commitment_5PB']),
            resource_group=dict(type='str',required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            tags=dict(type='dict'),
            virtual_network_rules=dict(
                type='list',
                options=dict(
                    name=dict(type='str',required=True),
                    subnet_id=dict(type='str',required=True)
                )
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

        self.results = dict(changed=False)
        self.account_dict = None

        super(AzureRMDatalakeStore, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=False,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        if self.encryption_config:
            # TODO: Revisar todo lo referente a Key Vault Meta Info y hacer pruebas
            self.encryption_config_model=self.datalake_store_models.EncryptionConfig(type=self.encryption_config.get('type'),
                                                                                     key_vault_meta_info=self.encryption_config.get('key_vault_meta_info'))

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
            response = self.datalake_store_client.accounts.check_name_availability(self.location, self.name)
        except CloudError as e:
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
            location=self.location,
            new_tier=self.new_tier,
            tags=self.tags,
            virtual_network_rules=self.virtual_network_rules_model
        )

        self.log(str(parameters))
        try:
            poller = self.datalake_store_client.accounts.create(self.resource_group, self.name, parameters)
            self.get_poller_result(poller)
        except CloudError as e:
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
                parameters.tags=self.account_dict['tags']

        if self.new_tier and self.account_dict.get('new_tier') != self.new_tier:
            self.results['changed'] = True
            parameters.new_tier=self.new_tier

        if self.default_group and self.account_dict.get('default_group') != self.default_group:
            self.results['changed'] = True
            parameters.default_group=self.default_group

        if self.encryption_state and self.account_dict.get('encryption_state') != self.encryption_state:
            self.fail("Encryption type cannot be updated.")

        if self.encryption_config and self.account_dict.get('encryption_config').get('type') != self.encryption_config.get('type'):
            self.fail("Encryption type cannot be updated.")

        if self.firewall_state and self.account_dict.get('firewall_state') != self.firewall_state:
            self.results['changed'] = True
            parameters.firewall_state=self.firewall_state

        if self.firewall_allow_azure_ips and self.account_dict.get('firewall_allow_azure_ips') != self.firewall_allow_azure_ips:
            self.results['changed'] = True
            parameters.firewall_allow_azure_ips=self.firewall_allow_azure_ips
        
        if self.firewall_rules is not None:
            self.firewall_rules_model = list()
            for rule in self.firewall_rules:
                rule_model = self.datalake_store_models.UpdateFirewallRuleWithAccountParameters(
                    name=rule.get('name'),
                    start_ip_address=rule.get('start_ip_address'),
                    end_ip_address=rule.get('end_ip_address'))
                self.firewall_rules_model.append(rule_model)
            self.results['changed'] = True
            parameters.firewall_rules=self.firewall_rules_model
        
        if self.virtual_network_rules is not None:
            self.virtual_network_rules_model = list()
            for vnet_rule in self.virtual_network_rules:
                vnet_rule_model = self.datalake_store_models.UpdateVirtualNetworkRuleWithAccountParameters(
                    name=vnet_rule.get('name'),
                    subnet_id=vnet_rule.get('subnet_id'))
                self.virtual_network_rules_model.append(vnet_rule_model)
            self.results['changed'] = True
            parameters.virtual_network_rules=self.virtual_network_rules_model

        self.log(str(parameters))
        try:
            poller = self.datalake_store_client.accounts.update(self.resource_group, self.name, parameters)
            self.get_poller_result(poller)
        except CloudError as e:
            self.log('Error creating datalake store.')
            self.fail("Failed to create datalake store: {0}".format(str(e)))
            
        return self.get_datalake_store()

    def delete_datalake_store(self):
        self.log('Delete datalake store {0}'.format(self.name))

        self.results['changed'] = True if self.account_dict is not None else False
        if not self.check_mode and self.account_dict is not None:
            try:
                status = self.datalake_store_client.accounts.delete(self.resource_group, self.name)
                self.log("delete status: ")
                self.log(str(status))
            except CloudError as e:
                self.fail("Failed to delete datalake store: {0}".format(str(e)))

        return True

    def get_datalake_store(self):
        self.log('Get properties for datalake store {0}'.format(self.name))
        datalake_store_obj = None
        account_dict = None

        try:
            datalake_store_obj = self.datalake_store_client.accounts.get(self.resource_group, self.name)
        except CloudError:
            pass

        if datalake_store_obj:
            account_dict = self.account_obj_to_dict(datalake_store_obj)

        return account_dict

    def account_obj_to_dict(self, datalake_store_obj):
        account_dict = dict(
            id=datalake_store_obj.id,
            name=datalake_store_obj.name,
            type=datalake_store_obj.type,
            location=datalake_store_obj.location,
            tags=datalake_store_obj.tags,
            identity=datalake_store_obj.identity,
            account_id=datalake_store_obj.account_id,
            provisioning_state=datalake_store_obj.provisioning_state,
            state=datalake_store_obj.state,
            creation_time=datalake_store_obj.creation_time,
            last_modified_time=datalake_store_obj.last_modified_time,
            endpoint=datalake_store_obj.endpoint,
            default_group=datalake_store_obj.default_group,
            encryption_config=dict(type=datalake_store_obj.encryption_config.type,
                                   key_vault_meta_info=datalake_store_obj.encryption_config.key_vault_meta_info),
            encryption_state=datalake_store_obj.encryption_state,
            encryption_provisioning_state=datalake_store_obj.encryption_provisioning_state,
            firewall_state=datalake_store_obj.firewall_state,
            firewall_allow_azure_ips=datalake_store_obj.firewall_allow_azure_ips,
            trusted_id_providers=datalake_store_obj.trusted_id_providers,
            trusted_id_provider_state=datalake_store_obj.trusted_id_provider_state,
            new_tier=datalake_store_obj.new_tier,
            current_tier=datalake_store_obj.current_tier
        )

        account_dict['firewall_rules']=list()
        for rule in datalake_store_obj.firewall_rules:
            rule_item = dict(
                name=rule.name,
                start_ip_address=rule.start_ip_address,
                end_ip_address=rule.end_ip_address
            )
            account_dict['firewall_rules'].append(rule_item)

        account_dict['virtual_network_rules']=list()
        for vnet_rule in datalake_store_obj.virtual_network_rules:
            vnet_rule_item = dict(
                name=vnet_rule.name,
                subnet_id=vnet_rule.subnet_id
            )
            account_dict['virtual_network_rules'].append(vnet_rule_item)
        
        return account_dict

def main():
    AzureRMDatalakeStore()


if __name__ == '__main__':
    main()
