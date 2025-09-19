#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitordatacollectionendpoint
version_added: "3.9.0"
short_description: Managed Data Collection Endpoints
description:
    - Create, update or delete the Data Collection Rules Endpoints.

options:
    name:
        description:
            - The name of the data collection endpoint.
            - The name is case insensitive.
        type: str
        required: true
    resource_group:
        description:
            - The name of the resource group in which the data collection endpoint is (if you use name)
        type: str
        required: true
    location:
        description:
            - The geo-location where the resource lives.
            - Default is resource group's location.
        type: str
    kind:
        description:
            - The kind of the resource.
        type: str
        choices:
            - Linux
            - Windows
    description:
        description:
            - Description of the data collection endpoint.
        type: str
    network_acls:
        description:
            - Network access control rules for the endpoints.
        type: dict
        suboptions:
            public_network_access:
                description:
                    - The configuration to set whether network access from public internet to the endpoints are allowed.
                type: str
                choices:
                    - Enabled
                    - Disabled
                    - SecuredByPerimeter
    state:
        description:
            - State of the data colleciton endpoint.
            - Set to C(present) to create a new endpoint.
            - Set to C(absent) to remove a endpoint.
        default: present
        type: str
        choices:
            - absent
            - present

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
    type: complex
    returned: always
    contains:
        configuration_access:
            description:
                - The endpoint used by clients to access their configuration.
            type: dict
            returned: always
            sample: {"endpoint": "https://fredendpoint-q7lu.eastus-1.handler.control.monitor.azure.com"}
        description:
            description:
                - Description of the data collection endpoint.
            type: str
            returned: always
            sample: Created
        etag:
            description:
                - Resource entity tag (ETag).
            type: str
            returned: always
            sample: "3d001f14-0000-0100-0000-68ca270a0000"
        id:
            description:
                - Fully qualified ID of the resource.
            type: str
            returned: always
            sample: "/subscriptions/xxx-xxx/resourceGroups/v-xisuRG/providers/Microsoft.Insights/dataCollectionEndpoints/fredendpoint"
        immutable_id:
            description:
                - The immutable ID of this data collection endpoint resource.
                - This property is READ-ONLY.
            type: str
            returned: always
            sample: dce-9897a7cde9b54676a1c07ab3ea222768
        kind:
            description:
                - The kind of the resource.
            type: str
            returned: always
            sample: Linux
        location:
            description:
                - The geo-location where the resource lives.
            type: str
            returned: always
            sample: eastus
        logs_ingestion:
            description:
                - The endpoint used by clients to ingest logs.
            type: dict
            returned: always
            sample: {"endpoint": "https://fredendpoint-q7lu.eastus-1.ingest.monitor.azure.com"}
        metrics_ingestion:
            description:
                - The endpoint used by clients to ingest metrics.
            type: dict
            returned: always
            sample: {"endpoint": "https://fredendpoint-q7lu.eastus-1.metrics.ingest.monitor.azure.com"}
        name:
            description:
                - The name of the resource.
            type: str
            returned: always
            sample: testendpoint
        network_acls:
            description:
                - Network access control rules for the endpoints.
            type: dict
            returned: always
            sample: {"public_network_access": "Enabled"}
        provisioning_state:
            description:
                - The resource provisioning state. This property is READ-ONLY.
            type: str
            returned: always
            sample: Succeeded
        system_data:
            description:
                - Metadata pertaining to creation and last modification of the resource.
            type: dict
            returned: always
            sample: {
                "created_at": "2025-09-17T03:12:08.743499Z",
                "created_by": "00867800-0fa3-4d02-8bc8-35edac3a0d32",
                "created_by_type": "Application",
                "last_modified_at": "2025-09-17T03:12:08.743499Z",
                "last_modified_by": "00867800-0fa3-4d02-8bc8-35edac3a0d32",
                "last_modified_by_type": "Application"
            }
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: {'key1': 'value1'}
        type:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: "Microsoft.Insights/dataCollectionEndpoints"
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


network_acls_spec = dict(
    public_network_access=dict(
        type='str',
        choices=["Enabled", "Disabled", "SecuredByPerimeter"]
    )
)


class AzureRMDataCollectionRuleEndpoint(AzureRMModuleBaseExt):
    """Information class for an Azure RM Data Collection Rules"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            location=dict(type='str'),
            kind=dict(type='str', choices=['Linux', 'Windows']),
            description=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            network_acls=dict(
                type='dict',
                options=network_acls_spec
            )
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.kind = None
        self.description = None
        self.network_acls = None
        self.tags = None
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
                                                                facts_module=True)

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

        self.tags = self.body.get('tags')
        response = self.get_endpoint()
        changed = False
        if self.state == 'present':
            if response:
                self.log("The monitor data collection endpoint already exist")
                update_tags, self.body['tags'] = self.update_tags(response.get('tags', dict()))
                if update_tags:
                    changed = True
                if self.body.get('description') and self.body['description'] != response.get('description'):
                    changed = True
                else:
                    self.body['description'] = response.get('description')
                if self.body.get('kind') and self.body.get('kind') != response.get('kind'):
                    changed = True
                else:
                    self.body['kind'] = response.get('kind')
                if self.body.get('network_acls') and self.body['network_acls'] != response.get('network_acls'):
                    changed = True
                else:
                    self.body['network_acls'] = response.get('network_acls')
            else:
                changed = True
                self.log("There is no monitor data collection endpoint, will create a new")

            if self.check_mode:
                self.log("Check mode test")
            elif changed:
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
            self.log("Could not find data collection endpoint {0} in resource group {1}, Exception as {2}".format(self.name, self.resource_group, ex))
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
