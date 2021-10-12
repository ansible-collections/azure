#!/usr/bin/python
#
# Copyright (c) 2020 David Duque Hernández, (@next-davidduquehernandez)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
module: azure_rm_cognitivesearch_info
version_added: "1.4.0"
short_description: Get Azure Cognitive Search service info
description:
    - Get info for a specific Azure Cognitive Search service or all Azure Cognitive Search service within a resource group.

options:
    resource_group:
        description:
            - The name of the Azure resource group.
        type: str
    name:
        description:
            - The name of the Azure Cognitive Search service.
        type: str
    show_keys:
        description:
            - Retrieve admin and query keys.
        type: bool
        default: False

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - David Duque Hernández (@next-davidduquehernandez)
'''

EXAMPLES = '''
  - name: Get Azure Cognitive Search info from resource group 'myResourceGroup' and name 'myAzureSearch'
    azure_rm_cognitivesearch_info:
      resource_group: myResourceGroup
      name: myAzureSearch

  - name: Get Azure Cognitive Search info from resource group 'myResourceGroup'
    azure_rm_cognitivesearch_info:
      resource_group: myResourceGroup

  - name: Get all Azure Cognitive Search info
    azure_rm_cognitivesearch_info:
'''

RETURN = '''
search:
    description:
        - Info for Azure Cognitive Search.
    returned: always
    type: list
    contains:
        hosting_mode:
            description:
                - Type of hosting mode selected.
            returned: always
            type: str
            sample: default
        id:
            description:
                - The unique identifier associated with this Azure Cognitive Search.
            returned: always
            type: str
            sample: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        identity:
            description:
                - The identity of the Azure Cognitive Search Service.
            returned: always
            type: dict
            contains:
                principal_id:
                    description:
                        - Identifier assigned.
                    type: str
                    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                type:
                    description:
                        - Identity type.
                    returned: always
                    type: str
                    sample: SystemAssigned
            sample:
                principal_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                type: SystemAssigned
        keys:
            description:
                - Admin and query keys for Azure Cognitive Search Service.
            type: dict
            contains:
                admin_primary:
                    description:
                        - Primary admin key for Azure Cognitive Search Service.
                    type: str
                    sample: 12345ABCDE67890FGHIJ123ABC456DEF
                admin_secondary:
                    description:
                        - Secondary admin key for Azure Cognitive Search Service.
                    type: str
                    sample: 12345ABCDE67890FGHIJ123ABC456DEF
                query:
                    description:
                        - List of query keys for Azure Cognitive Search Service.
                    type: list
                    sample: [{'key': '12345ABCDE67890FGHIJ123ABC456DEF', 'name': 'Query key'}]
        location:
            description:
                - The geo-location where the Azure Cognitive Search Service lives.
            returned: always
            type: str
            sample: West Europe
        name:
            description:
                - The name of the Azure Cognitive Search Service.
            returned: always
            type: str
            sample: myazuresearch
        network_rule_set:
            description:
                - Network specific rules that determine how the Azure Cognitive Search service may be reached.
            returned: always
            type: list
            sample: ['1.1.1.1', '8.8.8.8/31']
        partition_count:
            description:
                - The number of partitions in the Azure Cognitive Search Service.
            returned: always
            type: int
            sample: 3
        provisioning_state:
            description:
                - The state of the provisioning state of Azure Cognitive Search Service.
            returned: always
            type: str
            sample: succeeded
        public_network_access:
            description:
                - If it's allowed traffic over public interface.
            returned: always
            type: str
            sample: enabled
        replica_count:
            description:
                - The number of replicas in the Azure Cognitive Search Service.
            returned: always
            type: int
            sample: 3
        sku:
            description:
                - The SKU of the Azure Cognitive Search Service.
            returned: always
            type: str
            sample: standard
        status:
            description:
                - The state of the Azure Cognitive Search.
            returned: always
            type: str
            sample: Active running
        tags:
            description:
                - The resource tags.
            returned: always
            type: dict
            sample: { "tag1":"abc" }
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
            resource_group=dict(type='str'),
            show_keys=dict(type='bool', default=False)
        )

        self.results = dict(
            changed=False,
            search=[]
        )

        self.name = None
        self.resource_group = None
        self.show_keys = False

        super(AzureRMSearchInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
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
            identity=dict(type=search_obj.identity.type if search_obj.identity else 'None'),
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

        if search_obj.identity and search_obj.identity.principal_id:
            account_dict['identity']['principal_id'] = search_obj.identity.principal_id

        for rule in search_obj.network_rule_set.ip_rules:
            account_dict['network_rule_set'].append(rule.value)

        if self.show_keys:
            account_dict['keys'] = dict()

            admin_keys = self.search_client.admin_keys.get(self.resource_group, self.name)
            account_dict['keys']['admin_primary'] = admin_keys.primary_key
            account_dict['keys']['admin_secondary'] = admin_keys.secondary_key

            query_keys = self.search_client.query_keys.list_by_search_service(self.resource_group, self.name)
            account_dict['keys']['query'] = list()
            for key in query_keys:
                account_dict['keys']['query'].append(dict(name=key.name, key=key.key))

        return account_dict


def main():
    AzureRMSearchInfo()


if __name__ == '__main__':
    main()
