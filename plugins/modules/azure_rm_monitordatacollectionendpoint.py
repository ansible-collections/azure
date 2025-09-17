#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitordatacollectionendpoint
version_added: "3.9.0"
short_description: Get or list Data Collection Endpoints
description:
    - Get or list Data Collection Rules Endpoints.

options:
    endpoint_name:
        description:
            - The name of the data collection endpoint.
            - The name is case insensitive.
        type: str
    resource_group:
        description:
            - The name of the resource group in which the data collection endpoint is (if you use name)
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - magodo (@magodo)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Create a new data collection endpoint
  azure.azcollection.azure_rm_monitordatacollectionendpoint:
    resource_group: v-xisuRG
    name: fredendpoint1
    description: fredtestend
    kind: Linux
    network_acls:
      public_network_access: Enabled
    tags:
      key1: value1

- name: Delete the data collection endpoint
  azure.azcollection.azure_rm_monitordatacollectionendpoint:
    resource_group: v-xisuRG
    name: fredendpoint1
    state: absent
'''

RETURN = '''
datacollectionendpoint:
    description:
        - The facts of data collection rule association.
    type: dict
    returned: always
    sample: {
            "configuration_access": {
                "endpoint": "https://fredendpoint-q7lu.eastus-1.handler.control.monitor.azure.com"
            },
            "description": "fredtestend",
            "etag": "\"3d001f14-0000-0100-0000-68ca270a0000\"",
            "id": "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG/providers/Microsoft.Insights/dataCollectionEndpoints/fredendpoint",
            "immutable_id": "dce-9897a7cde9b54676a1c07ab3ea222768",
            "kind": "Linux",
            "location": "eastus",
            "logs_ingestion": {
                "endpoint": "https://fredendpoint-q7lu.eastus-1.ingest.monitor.azure.com"
            },
            "metrics_ingestion": {
                "endpoint": "https://fredendpoint-q7lu.eastus-1.metrics.ingest.monitor.azure.com"
            },
            "name": "fredendpoint",
            "network_acls": {
                "public_network_access": "Enabled"
            },
            "provisioning_state": "Succeeded",
            "system_data": {
                "created_at": "2025-09-17T03:12:08.743499Z",
                "created_by": "00867800-0fa3-4d02-8bc8-35edac3a0d32",
                "created_by_type": "Application",
                "last_modified_at": "2025-09-17T03:12:08.743499Z",
                "last_modified_by": "00867800-0fa3-4d02-8bc8-35edac3a0d32",
                "last_modified_by_type": "Application"
            },
            "tags": {
                "key1": "value1",
                "key2": "value2"
            },
            "type": "Microsoft.Insights/dataCollectionEndpoints"
        },
        "failed": false
    }
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import HttpResponseError
    import logging
    logging.basicConfig(filename='log.log', level=logging.INFO)

except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDataCollectionRuleEndpoint(AzureRMModuleBase):
    """Information class for an Azure RM Data Collection Rules"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            location=dict(type='str'),
            kind=dict(type='str', choices=['Linux', 'Windows']),
            identity=dict(type='dict',
                          options=dict(type=dict(type='str',  choices=["None", "SystemAssigned", "UserAssigned", "SystemAssigned,UserAssigned"]),
                                       user_assigned_identities=dict(type='str'))),
            description=dict(type='str'),
            network_acls=dict(type='dict',
                              options=dict(public_network_access=dict(type='str', choices=["Enabled", "Disabled", "SecuredByPerimeter"]))),
            state=dict(type='str', default='present', choices=['present', 'absent'])
        )

        self.required_by = {
            'endpoint_name': 'resource_group'
        }

        self.resource_group = None
        self.name = None
        self.location = None
        self.kind = None
        self.identity = None
        self.description = None
        self.network_acls = None
        self.state = None
        self.log_path = None
        self.log_mode = None
        self.body = dict()

        self.results = dict(
            changed=False,
            datacollectionendpoint=None
        )

        super(AzureRMDataCollectionRuleEndpoint, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                supports_check_mode=True,
                                                                supports_tags=True,
                                                                facts_module=True,
                                                                required_by=self.required_by)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if key in ['resource_group', 'state', 'name']:
                setattr(self, key, kwargs[key])
            else:
                self.body[key] = kwargs[key]

        resource_group = self.get_resource_group(self.resource_group)
        if not self.body.get('location'):
            # Set default location
            self.body['location'] = resource_group.location

        response = self.get_endpoint()
        changed = False
        if self.state == 'present':
            if response:
                pass
            else:
                changed = True
                if self.check_mode:
                    self.log("There is no monitor data collection endpoint, will create a new")
                else:
                    response = self.create_endpoint(self.body)
        else:
            if response:
                changed = True
                if self.check_mode:
                    self.log("The monitor data collection endpoint already exist, will be delete")
                else:
                    response = self.delete_endpoint()
            else:
                if self.check_mode:
                    self.log("There is no monitor data collection endpoint.")

        self.results['datacollectionruleendpoint'] = response
        self.results['changed'] = changed
        return self.results

    def get_endpoint(self):
        '''
        Gets the specified data collection rule endpoint
        '''
        response = None
        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_endpoints.get(resource_group_name=self.resource_group,
                                                                                                          data_collection_endpoint_name=self.name)
        except Exception as ex:
            self.log("Could not find data collection endpoint {0} in resource group {1}".format(self.name, self.resource_group))
        if response:
            return response.as_dict()

    def create_endpoint(self, body):
        '''
        Create a new Data Collection Endpoint
        '''
        response = None
        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_endpoints.create(resource_group_name=self.resource_group,
                                                                                                             data_collection_endpoint_name=self.name,
                                                                                                             body=body)
        except Exception as ex:
            self.fail("Create the data collection endponts occured exception, Exception as {0}".format(ex))

        if response:
            return response.as_dict()

    def update_endpoint(self):
        '''
        Update the Data Collection Endpoint
        '''
        body = dict()
        response = None
        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_endpoints.update(resource_group_name=self.resource_group,
                                                                                                             data_collection_endpoint_name=self.name,
                                                                                                             body=body)
        except Exception as ex:
            self.fail("Update the data collection endponts occured exception, Exception as {0}".format(ex))

        if response:
            return response.as_dict()

    def delete_endpoint(self):
        '''
        Delete the Data Collection Endpoint
        '''
        try:
            self.monitor_management_client_data_collection_rules.data_collection_endpoints.delete(resource_group_name=self.resource_group,
                                                                                                  data_collection_endpoint_name=self.name)
        except Exception as ex:
            self.fail("Delete the data collection endponts occured exception, Exception as {0}".format(ex))


def main():
    """Main execution"""
    AzureRMDataCollectionRuleEndpoint()


if __name__ == '__main__':
    main()
