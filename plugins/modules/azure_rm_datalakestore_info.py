#!/usr/bin/python

from __future__ import absolute_import, division, print_function
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

try:
    from msrestazure.azure_exceptions import CloudError
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
        except CloudError:
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
        except CloudError:
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
        except CloudError:
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

        if datalake_store_obj.identity:
            account_dict['identity']=dict(
                type=datalake_store_obj.identity.type,
                principal_id=datalake_store_obj.identity.principal_id,
                tenant_id=datalake_store_obj.identity.tenant_id
            )

        if datalake_store_obj.encryption_config.key_vault_meta_info:
            account_dict['encryption_config'] = dict(
                key_vault_meta_info = dict(
                    key_vault_resource_id = datalake_store_obj.encryption_config.key_vault_meta_info.key_vault_resource_id,
                    encryption_key_name = datalake_store_obj.encryption_config.key_vault_meta_info.encryption_key_name,
                    encryption_key_version = datalake_store_obj.encryption_config.key_vault_meta_info.encryption_key_version
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
