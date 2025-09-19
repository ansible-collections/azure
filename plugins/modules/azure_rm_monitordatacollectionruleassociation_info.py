#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitordatacollectionruleassociation_info
version_added: "3.9.0"
short_description: Get or list Data Collection Rule Association
description:
    - Get or list Data Collection Rule Association.

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
    association_name: association01
    resource_uri: "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG/providers/Microsoft.Compute/virtualMachines/fredVM"

- name: List all data collection rule associations with data_collection_endpoint_name
  azure.azcollection.azure_rm_monitordatacollectionrulesassociation_info:
    resource_group: Resource_Group_Name
    data_collection_endpoint_name: fredrpfx001-DCE

- name: List all data collection rule associations with data_collection_rule_name
  azure.azcollection.azure_rm_monitordatacollectionrulesassociation_info:
    resource_group: Resource_Group_Name
    data_collection_rule_name: fredrpfx001-DCR

- name: List all data collection rule associations with the resource_uri
  azure.azcollection.azure_rm_monitordatacollectionrulesassociation_info:
    resource_uri: "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG/providers/Microsoft.Compute/virtualMachines/fredVM"
'''

RETURN = '''
datacollectionruleassociations:
    description:
        - List of data collection rule association.
        - Can be empty if listing data collection rule association.
    type: complex
    returned: always
    contains:
        data_collection_rule_id:
            description:
                - The resource ID of the data collection endpoint that is to be associated.
            type: str
            returned: when-used
            sample: "/subscriptions/xxxxx/resourceGroups/v-xisuRG02/providers/Microsoft.Insights/dataCollectionRules/fredrpfx001-DCR"
        data_collection_endpoint_id:
            description:
                - The resource ID of the data collection endpoint that is to be associated.
            type: str
            returned: when-used
            sample: "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG/providers/Microsoft.Insights/dataCollectionEndpoints/fredendpoint"
        description:
            description:
                - Description of the association.
            type: str
            returned: always
            sample: Create
        etag:
            description:
                - Description of the association.
            returned: always
            type: str
            sample: "0c00c2b5-0000-0800-0000-68ca0de80000"
        id:
            description:
                - Fully qualified ID of the resource.
            type: str
            returned: always
            sample: "/subscriptions/xxxxxxxxxx/resourceGroups/v-xisuRG/providers/Microsoft.Compute/virtualMachines/\
                     fredVM/providers/Microsoft.Insights/dataCollectionRuleAssociations/association01"
        name:
            description:
                - Description of the association.
            type: str
            returned: always
            sample: associationname
        system_data:
            description:
                - Metadata pertaining to creation and last modification of the resource.
            type: dict
            returned: always
            sample: {
                "created_at": "2025-09-17T01:24:56.450551Z",
                "created_by": "00867800-0fa3-4d02-8bc8-35edac3a0d32",
                "created_by_type": "Application",
                "last_modified_at": "2025-09-17T01:24:56.450551Z",
                "last_modified_by": "00867800-0fa3-4d02-8bc8-35edac3a0d32",
                "last_modified_by_type": "Application"
            }
        type:
            description:
                - The type of the resource.
            type: str
            returned: always
            sample: "Microsoft.Insights/dataCollectionRuleAssociations"
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


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

        result = []
        if self.association_name:
            result = self.get_association(self.resource_uri, self.association_name)
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

    def get_association(self, resource_uri, association_name):
        '''
        Gets the specified association
        '''
        result = []
        response = None

        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_rule_associations.get(resource_uri=resource_uri,
                                                                                                                  association_name=association_name)
        except Exception:
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
            self.log("Could not list data collection rule assoication in resource uri {0}, Exception as {1}".format(self.resource_uri, ex))
            return []
        if response:
            for item in response:
                result.append(item.as_dict())

        return result

    def list_by_rule(self):
        '''
        Lists associations for the specified data collection rule.
        '''
        result = []
        response = None
        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_rule_associations.list_by_rule(
                resource_group_name=self.resource_group,
                data_collection_rule_name=self.data_collection_rule_name)
        except Exception as ex:
            self.log("Could not list assoication in data collection rule {0}, Exception as {1}".format(self.data_collection_rule_name, ex))
            return []
        if response:
            for item in response:
                association = item.as_dict()
                result += self.get_association(association['id'].split('providers/microsoft.insights')[0], association['name'])

        return result

    def list_by_data_collection_endpoint(self):
        '''
        Lists associations for the specified data collection endpoint.
        '''
        result = []
        response = None

        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_rule_associations.list_by_data_collection_endpoint(
                resource_group_name=self.resource_group,
                data_collection_endpoint_name=self.data_collection_endpoint_name)
        except Exception as ex:
            self.log("Could not list associations for the data collection rule endpoint {0}, Exception as {1}".format(self.data_collection_endpoint_name, ex))
            return []
        if response:
            for item in response:
                result.append(item.as_dict())

        return result


def main():
    """Main execution"""
    AzureRMDataCollectionRuleAssociationInfo()


if __name__ == '__main__':
    main()
