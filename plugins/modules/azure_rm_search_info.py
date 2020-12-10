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


class AzureRMSearchInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str')
        )

        self.results = dict(
            changed=False,
            search=[]
        )

        self.name = None
        self.resource_group = None

        super(AzureRMSearchInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name and not self.resource_group:
            self.fail("Parameter error: resource group required when filtering by name.")

        results = []
        if self.name:
            results = self.get_search()
        elif self.resource_group:
            results = self.list_resource_group()
        else:
            results = self.list_all()

        self.results['search'] = results
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

    def list_resource_group(self):
        self.log('Get basic properties for azure search in resource group {0}'.format(self.resource_group))
        search_obj = None
        results = list()

        try:
            search_obj = self.search_client.services.list_by_resource_group(self.resource_group)
        except CloudError:
            pass

        if search_obj:
            for seach_item in search_obj:
                results.append(self.account_obj_to_dict(seach_item))
            return results

        return list()

    def list_all(self):
        self.log('Get basic properties for all azure search')
        search_obj = None
        results = list()

        try:
            search_obj = self.search_client.services.list_by_subscription()
        except CloudError:
            pass

        if search_obj:
            for search_item in search_obj:
                results.append(self.account_obj_to_dict(search_item))
            return results

        return list()

    def account_obj_to_dict(self, search_obj):
        account_dict = dict(
            hosting_mode=search_obj.hosting_mode,
            id=search_obj.id,
            identity=dict(type=search_obj.identity.type),
            location=search_obj.location,
            name=search_obj.name,
            network_rule_set=list(),
            partition_count=search_obj.partition_count,
            provisioning_state=search_obj.provisioning_state,
            public_network_access=search_obj.public_network_access,
            replica_count=search_obj.replica_count,
            sku=search_obj.sku.name,
            status=search_obj.status,
            tags=search_obj.tags
        )

        if search_obj.identity.principal_id is not None:
            account_dict['identity']['principal_id'] = search_obj.identity.principal_id

        for rule in search_obj.network_rule_set.ip_rules:
            account_dict['network_rule_set'].append(rule.value)

        return account_dict


def main():
    AzureRMSearchInfo()


if __name__ == '__main__':
    main()
