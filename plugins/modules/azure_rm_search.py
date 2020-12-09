#!/usr/bin/python
#
# Copyright (c) 2020 David Duque Hernández, (@next-davidduquehernandez)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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


class AzureRMSearch(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            hosting_mode=dict(type='str', default='default', choices=['default', 'highDensity']),
            location=dict(type='str'),
            name=dict(type='str', required=True),
            network_rule_set=dict(type='list'),
            partition_count=dict(type='int', default=1),
            public_network_access=dict(type='str', default='enabled', choices=['enabled', 'disabled']),
            replica_count=dict(type='int', default=1),
            resource_group=dict(type='str', required=True),
            sku=dict(type='str', default='basic', choices=['free', 'basic', 'standard', 'standard2', 'standard3',
                                                           'storage_optimized_l1', 'storage_optimized_l2']),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            tags=dict(type='dict')
        )

        self.hosting_mode = None
        self.location = None
        self.name = None
        self.network_rule_set = None
        self.partition_count = None
        self.public_network_access = None
        self.replica_count = None
        self.resource_group = None
        self.sku = None
        self.tags = None

        self.results = dict(changed=False)
        self.account_dict = None

        super(AzureRMSearch, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=False,
                                            supports_tags=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        self.account_dict = self.get_search()

        if self.account_dict is not None:
            self.results['state'] = self.account_dict
        else:
            self.results['state'] = dict()

        if self.state == 'present':
            if not self.account_dict:
                self.results['state'] = self.create_search()
            else:
                self.results['state'] = self.update_search()
        else:
            self.delete_search()
            self.results['state'] = dict(state='Deleted')

        return self.results

    def get_search(self):
        self.log('Get properties for azure search {0}'.format(self.name))
        search_obj = None
        account_dict = None

        try:
            search_obj = self.search_client.services.get(self.resource_group, self.name)
        except CloudError:
            pass

        if search_obj:
            account_dict = self.account_obj_to_dict(search_obj)

        return account_dict

    def check_values(self, hosting_mode, sku, partition_count, replica_count):
        if (
            hosting_mode == 'highDensity' and
            sku != 'standard3'
        ):
            self.fail("Hosting mode could not be 'highDensity' if sku is not 'standard3'.")

        if (
            sku == 'standard3' and
            hosting_mode == 'highDensity'
            and partition_count not in [1, 2, 3]
        ):
            self.fail("Partition count must be 1, 2 or 3 if hosting mode is 'highDensity' and sku 'standard3'.")

        if partition_count not in [1, 2, 3, 4, 6, 12]:
            self.fail("Partition count must be 1, 2, 3, 4, 6 or 12.")

        if sku == 'basic':
            if replica_count not in [1, 2, 3]:
                self.fail("Replica count must be between 1 and 3.")
        else:
            if replica_count < 1 or replica_count > 12:
                self.fail("Replica count must be between 1 and 12.")

    def create_search(self):
        self.log("Creating search {0}".format(self.name))

        self.check_values(self.hosting_mode, self.sku, self.partition_count, self.replica_count)

        self.check_name_availability()
        self.results['changed'] = True

        search_model = self.search_client.services.models.SearchService(
            hosting_mode=self.hosting_mode,
            location=self.location,
            network_rule_set=self.network_rule_set,
            partition_count=self.partition_count,
            public_network_access=self.public_network_access,
            replica_count=self.replica_count,
            sku=self.search_client.services.models.Sku(name='basic'),
            tags=self.tags
        )

        self.search_client.services.create_or_update(self.resource_group, self.name, search_model)

        return self.get_search()

    def update_search(self):
        self.log("Updating search {0}".format(self.name))

        self.check_values(
            self.hosting_mode or self.account_dict.get('hosting_mode'),
            self.sku or self.account_dict.get('sku'),
            self.partition_count or self.account_dict.get('partition_count'),
            self.replica_count or self.account_dict.get('replica_count')
        )

        search_update_model = self.search_client.services.models.SearchServiceUpdate(
            location=self.location
        )

        if self.hosting_mode and self.account_dict.get('hosting_mode') != self.hosting_mode:
            self.results['changed'] = True
            search_update_model.hosting_mode = self.hosting_mode

        # if self.network_rule_set and self.account_dict.get('network_rule_set') != self.network_rule_set:
        #     self.results['changed'] = True
        #     search_update_model.network_rule_set = self.network_rule_set

        if self.partition_count and self.account_dict.get('partition_count') != self.partition_count:
            self.results['changed'] = True
            search_update_model.partition_count = self.partition_count

        if self.public_network_access and self.account_dict.get('public_network_access') != self.public_network_access:
            self.results['changed'] = True
            search_update_model.public_network_access = self.public_network_access

        if self.replica_count and self.account_dict.get('replica_count') != self.replica_count:
            self.results['changed'] = True
            search_update_model.replica_count = self.replica_count

        if self.sku and self.account_dict.get('sku') != self.sku:
            self.results['changed'] = True
            search_update_model.sku = self.sku

        if self.tags and self.account_dict.get('tags') != self.tags:
            self.results['changed'] = True
            search_update_model.tags = self.tags

        self.log('Updating search {0}'.format(self.name))

        try:
            if self.results['changed']:
                self.search_client.services.update(self.resource_group, self.name, search_update_model)
        except CloudError as e:
            self.fail("Failed to update the search: {0}".format(str(e)))

        return self.get_search()

    def delete_search(self):
        self.log('Delete search {0}'.format(self.name))

        try:
            if self.account_dict is not None:
                self.results['changed'] = True
                self.search_client.services.delete(self.resource_group, self.name)
        except CloudError as e:
            self.fail("Failed to delete the search: {0}".format(str(e)))

    def check_name_availability(self):
        self.log('Checking name availability for {0}'.format(self.name))
        try:
            response = self.search_client.services.check_name_availability(self.name)
        except CloudError as e:
            self.log('Error attempting to validate name.')
            self.fail("Error checking name availability: {0}".format(str(e)))
        if not response.is_name_available:
            self.log('Error name not available.')
            self.fail("{0} - {1}".format(response.message, response.reason))

    def account_obj_to_dict(self, search_obj):
        account_dict = dict(
            id=search_obj.id,
            location=search_obj.location,
            name=search_obj.name,
            partition_count=search_obj.partition_count,
            provisioning_state=search_obj.provisioning_state,
            replica_count=search_obj.replica_count,
            sku=search_obj.sku.name,
            status=search_obj.status,
            tags=search_obj.tags
        )

        return account_dict


def main():
    AzureRMSearch()


if __name__ == '__main__':
    main()
