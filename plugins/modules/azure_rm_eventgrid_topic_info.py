#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_eventgrid_topic_info
version_added: "3.13.0"
short_description: List Eventgrid Topics
description:
    - List Eventgrid Topics.
options:
    name:
        description:
            - Specify the name of the Eventgrid topic.
        required: false
        type: str
    resource_group:
        description:
            - Name of a resource group to limit topics from.  If not specified the subscription
              will be searched.
        required: false
        type: str
    odata_query:
        description:
            - The query used to filter the search results using OData syntax.
        required: false
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get info on a Topic
  azure.azcollection.azure_rm_eventgrid_topic_info:
    resource_group: rg1
    odata_query: "contains(name, 'PATTERN')"
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: true
eventgrid_topics:
    description:
        - List of Eventgrid Topics.
    returned: always
    type: complex
    contains:
        data_residency_boundary:
            description:
                - Residncy boundary
            returned: always
            type: str
            sample: WithinGeopair
        disable_local_auth:
            description:
                - Whether local auth is disabled
            returned: always
            type: bool
            sample: false
        endpoint:
            description:
                - Rest API endpoint to use to post events
            returned: always
            type: str
            sample: https://myTopic-20070.westus3-1.eventgrid.azure.net/api/events
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.EventGrid/topics/myTopic
        inbound_ip_rules:
            description:
                - Rules for network access
            type: complex
            returned: when-enabled
            contains:
                action:
                    description:
                        - What action will be taken, Allow or Disallow
                    returned: always
                    type: str
                    sample: Allow
                ip_mask:
                    description:
                        - CIDR notation of the network to act on.
                    returned: always
                    type: str
                    sample: 10.0.0.0/8
        input_schema:
            description:
                - The input schema assigned to this Topic
            returned: always
            type: str
            sample: EventGridSchema
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: westus3
        metric_resource_id:
            description:
                - Metric Resource ID.
            returned: always
            type: str
            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        minimum_tls_version_allowed:
            description:
                - The minimum TLS version allowed
            returned: always
            type: str
            sample: 1.0
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: myTopic
        provisioning_state:
            description:
                - The provisioning state.
            returned: always
            type: str
            sample: Succeeded
        public_network_access:
            description:
                - Indicates if boot diagnostics are enabled.
            returned: always
            type: bool
            sample: true
        topic_keys:
            description:
                - Shared access keys to a topic
            type: complex
            returned: always
            contains:
                key1:
                    description:
                        - Shared access key 1
                    type: str
                    returned: always
                    sample: FYKuIOq0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxZEGV3gr
                key2:
                    description:
                        - Shared access key 2
                    type: str
                    returned: always
                    sample: D8QRdfVrxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxZEGdMMc
        type:
            description:
                - Type of Eventgrid
            type: str
            returned: always
            sample: Microsoft.EventGrid/topics
'''


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.mgmt.eventgrid import EventGridManagementClient
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMEventgridTopic(AzureRMModuleBase):

    @property
    def client(self):
        self.log('Getting client')
        if not self._client:
            self._client = self.get_mgmt_svc_client(EventGridManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)
        return self._client

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=False
            ),
            odata_query=dict(
                type='str',
                required=False
            ),
            resource_group=dict(
                type='str',
                required=False
            ),
            tags=dict(
                type='list',
                elements='str'
            ),
        )

        mutually_exclusive = [('name', 'odata_query')]

        self._client = None

        self.name = None
        self.tags = None

        self.results = dict(
            changed=False,
            eventgrid_topics=[]
        )

        super(AzureRMEventgridTopic, self).__init__(self.module_arg_spec,
                                                    supports_tags=False,
                                                    supports_check_mode=True,
                                                    mutually_exclusive=mutually_exclusive,
                                                    facts_module=True,
                                                    )

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None and self.resource_group is not None:
            self.results['eventgrid_topics'] = self.get_item(self.resource_group,
                                                             self.name)
        elif self.resource_group is not None:
            self.results['eventgrid_topics'] = self.list_by_resourcegroup(self.resource_group,
                                                                          self.odata_query)
        else:
            self.results['eventgrid_topics'] = self.list_items(self.odata_query)

        return self.results

    def list_by_resourcegroup(self, resource_group, odata_query=None):
        self.log('List all items by resource group')
        try:
            items = self.client.topics.list_by_resource_group(resource_group, odata_query)
        except ResourceNotFoundError as exc:
            self.fail("Failed to list all items in resource group - {0}".format(str(exc)))

        return self.filter_results(items)

    def list_items(self, odata_query=None):
        self.log('List all items by resource group')
        try:
            items = self.client.topics.list_by_subscription(odata_query)
        except ResourceNotFoundError as exc:
            self.fail("Failed to list all items in resource group - {0}".format(str(exc)))

        return self.filter_results(items)

    def get_item(self, resource_group, topic_name):
        '''
        Get the eventgrid topic

        :return: eventgrid topic dict
        '''
        try:
            response = self.client.topics.get(resource_group, topic_name)
            return self.filter_results([response])
        except ResourceNotFoundError:
            self.log('Did not find the eventgrid_topic.')
            return []
        except Exception as exc:
            self.fail('Error when get eventgrid_topic got Excetion as {0}'.format(str(exc)))

    def filter_results(self, items):
        results = []
        for item in items:
            topic = self.format_eventgrid_topic(item)
            if topic and self.has_tags(topic.get('tags', {}), self.tags):
                resource_group = self.parse_resource_to_dict(topic.get('id')).get('resource_group')
                topic_keys = self.client.topics.list_shared_access_keys(resource_group, topic.get('name'))
                topic['topic_keys'] = topic_keys and topic_keys.as_dict() or {}
                results.append(topic)
        return results

    def format_eventgrid_topic(self, topic_data):
        results = topic_data and topic_data.as_dict() or {}
        return results


def main():
    AzureRMEventgridTopic()


if __name__ == '__main__':
    main()
