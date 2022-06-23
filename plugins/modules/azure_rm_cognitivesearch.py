#!/usr/bin/python
#
# Copyright (c) 2020 David Duque Hernández, (@next-davidduquehernandez)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_cognitivesearch
version_added: "1.4.0"
short_description: Manage Azure Cognitive Search service
description:
    - Create, update or delete Azure Cognitive Search service.
options:
    name:
        description:
            - The name of the Azure Cognitive Search service.
            - Search service names must only contain lowercase letters, digits or dashes.
            - Cannot use dash as the first two or last one characters.
            - Cannot contain consecutive dashes.
            - Must be between 2 and 60 characters in length.
            - Search service names must be globally unique.
            - You cannot change the service name after the service is created.
        type: str
        required: true
    resource_group:
        description:
            - The name of the resource group within the current subscription.
        type: str
        required: true
    location:
        description:
            - Valid azure location. Defaults to location of the resource group.
        type: str
    hosting_mode:
        description:
            - Applicable only for the standard3 SKU.
            - You can set this property to enable up to 3 high density partitions that allow up to 1000 indexes.
            - For the standard3 SKU, the value is either 'default' or 'highDensity'.
            - For all other SKUs, this value must be 'default'.
        choices:
            - default
            - highDensity
        type: str
        default: 'default'
    identity:
        description:
            - The identity for the resource.
        choices:
            - None
            - SystemAssigned
        type: str
        default: 'None'
    network_rule_set:
        description:
            - Network specific rules that determine how the Azure Cognitive Search service may be reached.
        type: list
        elements: str
    partition_count:
        description:
            - The number of partitions in the search service.
            - It can be C(1), C(2), C(3), C(4), C(6), or C(12).
            - Values greater than 1 are only valid for standard SKUs.
            - For 'standard3' services with hostingMode set to 'highDensity', the allowed values are between 1 and 3.
        type: int
        default: 1
    public_network_access:
        description:
            - This value can be set to C(enabled) to avoid breaking changes on existing customer resources and templates.
            - If set to C(enabled), traffic over public interface is not allowed, and private endpoint connections would be the exclusive access method.
        choices:
            - enabled
            - disabled
        type: str
        default: 'enabled'
    replica_count:
        description:
            - The number of replicas in the search service.
            - It must be a value between 1 and 12 inclusive for I(sku=standard).
            - It must be a value between 1 and 3 inclusive for I(sku=basic).
        type: int
        default: 1
    sku:
        description:
            - The SKU of the Search Service, which determines price tier and capacity limits.
            - This property is required when creating a new Search Service.
        choices:
            - free
            - basic
            - standard
            - standard2
            - standard3
            - storage_optimized_l1
            - storage_optimized_l2
        type: str
        default: 'basic'
    state:
        description:
            - Assert the state of the search instance. Set to C(present) to create or update a search instance. Set to C(absent) to remove a search instance.
        type: str
        default: present
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - David Duque Hernández (@next-davidduquehernandez)
'''

EXAMPLES = '''
  - name: Create Azure Cognitive Search
    azure_rm_cognitivesearch:
      resource_group: myResourceGroup
      name: myAzureSearch
'''

RETURN = '''
state:
    description:
        - Info for Azure Cognitive Search.
    returned: always
    type: dict
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
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSearch(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            hosting_mode=dict(type='str', default='default', choices=['default', 'highDensity']),
            identity=dict(type='str', default='None', choices=['None', 'SystemAssigned']),
            location=dict(type='str'),
            name=dict(type='str', required=True),
            network_rule_set=dict(type='list', elements='str'),
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
        self.identity = None
        self.location = None
        self.name = None
        self.network_rule_set = list()
        self.partition_count = None
        self.public_network_access = None
        self.replica_count = None
        self.resource_group = None
        self.sku = None
        self.tags = None

        self.results = dict(changed=False)
        self.account_dict = None
        self.firewall_list = list()

        super(AzureRMSearch, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=False,
                                            supports_tags=True)

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
        except ResourceNotFoundError:
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

        if self.network_rule_set:
            for rule in self.network_rule_set:
                self.firewall_list.append(self.search_client.services.models.IpRule(value=rule))

        search_model = self.search_client.services.models.SearchService(
            hosting_mode=self.hosting_mode,
            identity=self.search_client.services.models.Identity(type=self.identity),
            location=self.location,
            network_rule_set=dict(ip_rules=self.firewall_list) if len(self.firewall_list) > 0 else None,
            partition_count=self.partition_count,
            public_network_access=self.public_network_access,
            replica_count=self.replica_count,
            sku=self.search_client.services.models.Sku(name=self.sku),
            tags=self.tags
        )

        try:
            poller = self.search_client.services.begin_create_or_update(self.resource_group, self.name, search_model)
            self.get_poller_result(poller)
        except Exception as e:
            self.log('Error creating Azure Search.')
            self.fail("Failed to create Azure Search: {0}".format(str(e)))

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
            location=self.location,
            hosting_mode=None,
            partition_count=None,
            public_network_access=None,
            replica_count=None,
            sku=self.search_client.services.models.Sku(name=self.account_dict.get('sku'))
        )

        if self.hosting_mode and self.account_dict.get('hosting_mode') != self.hosting_mode:
            self.fail("Updating hosting_mode of an existing search service is not allowed.")

        if self.identity and self.account_dict.get('identity').get('type') != self.identity:
            self.results['changed'] = True
            search_update_model.identity = self.search_client.services.models.Identity(type=self.identity)

        if self.network_rule_set:
            for rule in self.network_rule_set:
                if len(self.network_rule_set) != len(self.account_dict.get('network_rule_set')) or rule not in self.account_dict.get('network_rule_set'):
                    self.results['changed'] = True
                self.firewall_list.append(self.search_client.services.models.IpRule(value=rule))
                search_update_model.network_rule_set = dict(ip_rules=self.firewall_list)

        if self.partition_count and self.account_dict.get('partition_count') != self.partition_count:
            self.results['changed'] = True
            search_update_model.partition_count = self.partition_count

        if self.public_network_access and self.account_dict.get('public_network_access').lower() != self.public_network_access.lower():
            self.results['changed'] = True
            search_update_model.public_network_access = self.public_network_access

        if self.replica_count and self.account_dict.get('replica_count') != self.replica_count:
            self.results['changed'] = True
            search_update_model.replica_count = self.replica_count

        if self.sku and self.account_dict.get('sku') != self.sku:
            self.fail("Updating sku of an existing search service is not allowed.")

        if self.tags and self.account_dict.get('tags') != self.tags:
            self.results['changed'] = True
            search_update_model.tags = self.tags

        self.log('Updating search {0}'.format(self.name))

        try:
            if self.results['changed']:
                poller = self.search_client.services.begin_create_or_update(self.resource_group, self.name, search_update_model)
                self.get_poller_result(poller)
        except Exception as e:
            self.fail("Failed to update the search: {0}".format(str(e)))

        return self.get_search()

    def delete_search(self):
        self.log('Delete search {0}'.format(self.name))

        try:
            if self.account_dict is not None:
                self.results['changed'] = True
                self.search_client.services.delete(self.resource_group, self.name)
        except Exception as e:
            self.fail("Failed to delete the search: {0}".format(str(e)))

    def check_name_availability(self):
        self.log('Checking name availability for {0}'.format(self.name))
        try:
            response = self.search_client.services.check_name_availability(self.name)
        except Exception as e:
            self.log('Error attempting to validate name.')
            self.fail("Error checking name availability: {0}".format(str(e)))
        if not response.is_name_available:
            self.log('Error name not available.')
            self.fail("{0} - {1}".format(response.message, response.reason))

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

        return account_dict


def main():
    AzureRMSearch()


if __name__ == '__main__':
    main()
