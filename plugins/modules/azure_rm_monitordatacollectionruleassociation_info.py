#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitordatacollectionrulesassociation_info
version_added: "3.9.0"
short_description: Get or list Data Collection Rule Association
description:
    - Get Data Collection Rule Association.

options:
    data_collection_endpoint_name:
        description:
            - The name of the data collection endpoint.
            - The name is case insensitive.
        type: str
    data_collection_rule_name:
        description:
            - The name of the data collection rule.
            - The name is case insensitive.
        type: str
    resource_uri:
        description:
            - The identifier of the resource.
        type: str
    association_name:
        description:
            - The name of the association.
            - The name is case insensitive.
        type: str
    resource_group:
        description:
            - The name of the resource group in which the data collection rule association is (if you use name)
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get data collection rule association details
  azure.azcollection.azure_rm_monitordatacollectionrulesassociation_info:
    association_name: 
    resource_group: Resource_Group_Name

- name: List all data collection rule associations with data_collection_endpoint_name
  azure.azcollection.azure_rm_monitordatacollectionrulesassociation_info:
    resource_group: Resource_Group_Name
    data_collection_endpoint_name:

- name: List all data collection rule associations with data_collection_rule_name
  azure.azcollection.azure_rm_monitordatacollectionrulesassociation_info:
    resource_group: Resource_Group_Name
    data_collection_rule_name:

- name: List all data collection rule associations with the resource_uri
  azure.azcollection.azure_rm_monitordatacollectionrulesassociation_info:
    resource_uri: pass
'''

RETURN = '''
datacollectionruleassociations:
    description:
        - List of data collection rule association.
        - Can be empty if listing data collection rule association.
    type: list
    returned: always
    sample:
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import HttpResponseError

except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDataCollectionRuleAssociationInfo(AzureRMModuleBase):
    """Information class for an Azure RM Data Collection Rules"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_uri=dict(type='str'),
            association_name=dict(type='str'),
            data_collection_endpoint_name=dict(type='str'),
            data_collection_rule_name=dict(type='str'),
            resource_group=dict(type='str')
        )

        self.required_by = {
            'data_collection_rule_name': 'resource_group',
            'data_collection_endpoint_name': 'resource_group',
            'association_name': 'resource_uri'
        }

        self.resource_uri = None
        self.resource_group = None
        self.association_name = None
        self.data_collection_endpoint_name = None
        self.data_collection_rule_name = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            datacollectionruleassociations=[]
        )

        super(AzureRMDataCollectionRuleAssociationInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                             supports_check_mode=True,
                                                             supports_tags=False,
                                                             facts_module=True,
                                                             required_by=self.required_by)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.association_name:
            result = self.get_association()
        elif self.data_collection_rule_name:
            result = self.list_by_rule()
        elif self.data_collection_endpoint_name:
            result = self.list_by_data_collection_endpoint()
        elif self.resource_uri:
            result = self.list_by_resource()
        else:
            self.fail("One of association_name, data_collection_rule_name, data_collection_endpoint_name and resource_uri must be configured")

        self.results['datacollectionruleassociations'] = result

        return self.results

    def get_association(self):
        '''
        Gets the specified association
        '''
        result = []
        response = None

        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_rule_associations.get(resource_uri=self.resource_uri,
                                                                                                                  association_name=self.association_name)
        except Exception as ex:
            self.log("Could not find data collection rule assoication {0} in resource uri {1}".format(self.association_name, self.resource_uri))
            return []
        if response:
            result = [response.as_dict()]

        return result

    def list_by_resource(self):
        '''
        Lists associations for the specified resource.
        '''
        result = []
        response = None

        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_rule_associations.list_by_resource(resource_uri=self.resource_uri)
        except Exception as ex:
            self.log("Could not list data collection rule assoication in resource uri {0}".format(self.resource_uri))
            return []
        if response:
            result.append(item.as_dict() for item in response)

        return result

    def list_by_rule(self):
        '''
        Lists associations for the specified data collection rule.
        '''
        result = []
        response = None

        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_rule_associations.list_by_rule(resource_group_name=self.resource_group,
                                                                                                                           data_collection_rule_name=self.data_collection_rule_name)
        except Exception as ex:
            self.log("Could not list assoication in data collection rule {0}".format(self.data_collection_rule_name))
            return []
        if response:
            result.append(item.as_dict() for item in response)

        return result

    def list_by_data_collection_endpoint(self):
        '''
        Lists associations for the specified data collection endpoint.
        '''
        result = []
        response = None

        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_rule_associations.list_by_data_collection_endpoint(resource_group_name=self.resource_group,
                                                                                                                                               data_collection_endpoint_name=self.data_collection_endpoint_name)
        except Exception as ex:
            self.log("Could not list associations for the data collection rule endpoint {0}".format(self.data_collection_endpoint_name))
            return []
        if response:
            result.append(item.as_dict() for item in response)

        return result


def main():
    """Main execution"""
    AzureRMDataCollectionRuleAssociationInfo()


if __name__ == '__main__':
    main()
