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
            resource_group=dict(type='str',required=True),
            name=dict(type='str',required=True),
            location=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.state = None
        self.name = None
        self.resource_group = None
        self.location = None
        self.results = dict(changed=False)
        self.account_dict = None

        super(AzureRMDatalakeStore, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=False,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

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

        parameters = self.datalake_store_models.CreateDataLakeStoreAccountParameters(
            location=self.location
        )

        self.log(str(parameters))
        try:
            poller = self.datalake_store_client.accounts.create(self.resource_group, self.name, parameters)
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
            firewall_rules=datalake_store_obj.firewall_rules,
            virtual_network_rules=datalake_store_obj.virtual_network_rules,
            firewall_state=datalake_store_obj.firewall_state,
            firewall_allow_azure_ips=datalake_store_obj.firewall_allow_azure_ips,
            trusted_id_providers=datalake_store_obj.trusted_id_providers,
            trusted_id_provider_state=datalake_store_obj.trusted_id_provider_state,
            new_tier=datalake_store_obj.new_tier,
            current_tier=datalake_store_obj.current_tier
        )
        return account_dict

def main():
    AzureRMDatalakeStore()


if __name__ == '__main__':
    main()
