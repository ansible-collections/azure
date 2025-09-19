#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitordatacollectionruleassociation
version_added: "3.9.0"
short_description: Managed Data Collection Rule Association
description:
    - Create, update or delete the Data Collection Rule Association.

options:
    data_collection_endpoint_id:
        description:
            - The ID of the data collection endpoint.
        type: str
    data_collection_rule_id:
        description:
            - The ID of the data collection rule.
        type: str
    resource_uri:
        description:
            - The identifier of the resource.
        type: str
        required: true
    association_name:
        description:
            - The name of the association.
            - The name is case insensitive.
            - An association of data collection endpoint must be named 'configurationAccessEndpoint.
        type: str
        required: true
    description:
        description:
            - Description of the association.
        type: str
    state:
        description:
            - State of the data colleciton rule association.
            - Set to C(present) to create a new association.
            - Set to C(absent) to remove a association.
        default: present
        type: str
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Create a new data collection rule association
  azure.azcollection.azure_rm_monitordatacollectionrulesassociation:
    resource_uri: "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG/providers/Microsoft.Compute/virtualMachines/fredVM"
    association_name: association01
    data_collection_rule_id: "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG02/providers/Microsoft.Insights/dataCollectionRules/fredrpfx001-DCR"
    description: fredtest

- name: Delete the data collection rule association
  azure.azcollection.azure_rm_monitordatacollectionrulesassociation:
    resource_uri: "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG/providers/Microsoft.Compute/virtualMachines/fredVM"
    association_name: association01
    state: absent
'''

RETURN = '''
datacollectionruleassociation:
    description:
        - The facts of the data collection rule association.
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


class AzureRMDataCollectionRuleAssociation(AzureRMModuleBase):
    """Information class for an Azure RM Data Collection Rules"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_uri=dict(type='str', required=True),
            association_name=dict(type='str', required=True),
            data_collection_endpoint_id=dict(type='str'),
            data_collection_rule_id=dict(type='str'),
            description=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent'])
        )

        self.resource_uri = None
        self.association_name = None
        self.data_collection_endpoint_id = None
        self.data_collection_rule_id = None
        self.state = None
        self.description = None
        self.log_path = None
        self.log_mode = None
        mutually_exclusive = [('data_collection_endpoint_id', 'data_collection_rule_id')]

        self.results = dict(
            changed=False,
            datacollectionruleassociation=None
        )

        super(AzureRMDataCollectionRuleAssociation, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                   supports_check_mode=True,
                                                                   supports_tags=False,
                                                                   mutually_exclusive=mutually_exclusive,
                                                                   facts_module=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        response = self.get_association()
        changed = False
        if self.state == 'present':
            if response:
                if self.description and self.description != response.get('description'):
                    changed = True
                else:
                    self.description = response.get('description')
                if self.data_collection_rule_id and self.data_collection_rule_id != response.get('data_collection_rule_id'):
                    self.fail("Already exist assciation with {0}. If need to udpate, please delete it and recreate it".format(self.data_collection_rule_id))
                else:
                    self.data_collection_rule_id = response.get('data_collection_rule_id')
                if self.data_collection_endpoint_id and self.data_collection_endpoint_id != response.get('data_collection_endpoint_id'):
                    self.fail("Already exist associat with {0}. If need to udpate, please delete it and recreate it".format(self.data_collection_endpoint_id))
                else:
                    self.data_collection_endpoint_id = response.get('data_collection_endpoint_id')
            else:
                changed = True

            if not self.check_mode and changed:
                response = self.create_association()
        else:
            if response:
                changed = True
                if self.check_mode:
                    self.log("The monitor data collection rule association already exist, will be delete")
                else:
                    response = self.delete_association()
            else:
                if self.check_mode:
                    self.log("There is no monitor data collection rule association.")

        self.results['datacollectionruleassociation'] = response
        self.results['changed'] = changed

        return self.results

    def get_association(self):
        '''
        Gets the specified association
        '''
        response = None
        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_rule_associations.get(resource_uri=self.resource_uri,
                                                                                                                  association_name=self.association_name)
        except Exception:
            self.log("Could not find data collection rule assoication {0} in resource uri {1}".format(self.association_name, self.resource_uri))
        if response:
            return response.as_dict()

    def create_association(self):
        '''
        Creates or updates an association.
        '''
        response = None
        try:
            body = dict(description=self.description,
                        data_collection_rule_id=self.data_collection_rule_id,
                        data_collection_endpoint_id=self.data_collection_endpoint_id)
            response = self.monitor_management_client_data_collection_rules.data_collection_rule_associations.create(resource_uri=self.resource_uri,
                                                                                                                     association_name=self.association_name,
                                                                                                                     body=body)
        except Exception as ex:
            self.fail("Creates or update the association occured exception, Exception as {0}".format(ex))
        return response.as_dict()

    def delete_association(self):
        '''
        Deletes an association
        '''
        try:
            self.monitor_management_client_data_collection_rules.data_collection_rule_associations.delete(resource_uri=self.resource_uri,
                                                                                                          association_name=self.association_name)
        except Exception as ex:
            self.fail("Deletes the association occured exception, Exception as {0}".format(ex))


def main():
    """Main execution"""
    AzureRMDataCollectionRuleAssociation()


if __name__ == '__main__':
    main()
