#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_eventgrid_subscription_info
version_added: "3.13.0"
short_description: List Eventgrid Event Subscriptions
description:
    - List Eventgrid Event Subscriptions.
options:
    source_resource_id:
        description:
            - Fully qualified identifier of the Azure resource whose event subscription
              needs to be listed.
        type: str
        required: false
    location:
        description:
            - List by region.
        type: str
        required: false
    resource_group:
        description:
            - Name of a resource group to limit event subscriptions from.  If not specified the subscription
              will be searched.
        required: false
        type: str
    odata_query:
        description:
            - The query used to filter the search results using OData syntax.
        required: false
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get info on an event subscription
  azure.azcollection.azure_rm_eventgrid_subscription_info:
    location: westus3
    odata_query: "contains(name, 'PATTERN')"
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
eventgrid_subscriptions:
    description:
        - List of Eventgrid subscriptions.
    returned: always
    type: complex
    contains:
        destination:
            description:
                - Details of the destination
            returned: always
            type: complex
            contains:
                delivery_attribute_mappings:
                    description:
                        - Mapping attributes for delivery
                    returned: always
                    type: str
                endpoint_base_url:
                    description:
                        - The base URL of the endpoint
                    returned: always
                    type: str
                    sample: https://event-grid-site-xxxxx20070.azurewebsites.net/api/updates
                endpoint_type:
                    description:
                        - The type of the endpoint
                    returned: always
                    type: str
                    sample: WebHook
                endpoint_url:
                    description:
                        - The URL of the endpoint
                    returned: always
                    type: str
                    sample: https://event-grid-site-xxxxx20070.azurewebsites.net/api/updates
                max_events_per_batch:
                    description:
                        - How many events will be batched
                    returned: always
                    type: int
                    sample: 1
                preferred_batch_size_in_kilobytes:
                    description:
                        - The preferred batch size in kilobytes
                    returned: always
                    type: int
                    sample: 64
        event_delivery_schema:
            description:
                - The type of Eventgrid Schema
            returned: always
            type: str
            sample: EventGridSchema
        filter:
            description:
                - Filter settings for which events to publish to endpoint
            returned: always
            type: complex
            contains:
                subject_begins_with:
                    description:
                        - Filter on Subject beginning with this value
                    returned: always
                    type: str
                subject_ends_with:
                    description:
                        - Filter on Subject ending with this value
                    returned: always
                    type: str
        id:
            description:
                - The ID of the Eventgrid Subscription
            returned: always
            type: str
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/MyResourceGroup/providers/Microsoft.EventGrid/topics/topic-xxxxx20070/providers/Microsoft.EventGrid/eventSubscriptions/subscription-xxxxx20070 # nopep8: E501
        name:
            description:
                - The name of the Eventgrid Subscription
            returned: always
            type: str
            sample: subscription-xxxxx20070
        provisioning_state:
            description:
                - The provisioning state of this Eventgrid Subscription
            returned: always
            type: str
            sample: Succeeded
        retry_policy:
            description:
                - Retry policy for this Eventgrid Subscription
            returned: always
            type: complex
            contains:
                event_time_to_live_in_minutes:
                    description:
                        - Event time to live in minutes
                    returned: always
                    type: int
                    sample: 1440
                max_delivery_attempts:
                    description:
                        - Max attempts to deliver to endpoint
                    returned: always
                    type: int
                    sample: 30
        topic:
            description:
                - The source resource id that the Eventgrid Subscription is subscribed to
            returned: always
            type: str
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/MyResourceGroup/providers/microsoft.eventgrid/topics/topic-xxxxx20070
        type:
            description:
                - The type of Eventgrid Subscription
            returned: always
            type: str
            sample: Microsoft.EventGrid/eventSubscriptions
'''

DEFAULT_TOP = 100
EVENTGRID_NAMESPACE = "Microsoft.EventGrid"
EVENTGRID_DOMAINS = "domains"
EVENTGRID_TOPICS = "topics"

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.mgmt.core.tools import parse_resource_id
    from azure.mgmt.eventgrid import EventGridManagementClient
    from azure.mgmt.eventgrid.models import (
        WebHookEventSubscriptionDestination,
        StorageQueueEventSubscriptionDestination,
    )
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMEventgridSubscriptionInfo(AzureRMModuleBase):

    @property
    def client(self):
        self.log('Getting client')
        if not self._client:
            self._client = self.get_mgmt_svc_client(EventGridManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)
        return self._client

    def __init__(self):

        self.module_arg_spec = dict(
            source_resource_id=dict(
                type='str',
                required=False
            ),
            location=dict(
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
        )

        mutually_exclusive = [('source_resource_id', 'location')]
        required_one_of = [['source_resource_id', 'location']]

        self._client = None

        self.results = dict(
            changed=False,
            eventgrid_subscriptions=[]
        )

        super(AzureRMEventgridSubscriptionInfo, self).__init__(self.module_arg_spec,
                                                               supports_tags=False,
                                                               supports_check_mode=True,
                                                               mutually_exclusive=mutually_exclusive,
                                                               required_one_of=required_one_of,
                                                               facts_module=True,
                                                               )

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.source_resource_id is not None:
            self.results['eventgrid_subscriptions'] = self.list_by_resource_id(self.source_resource_id,
                                                                               self.odata_query,
                                                                               DEFAULT_TOP)
        else:
            self.results['eventgrid_subscriptions'] = self.list_by_location(self.resource_group,
                                                                            self.location,
                                                                            self.odata_query,
                                                                            DEFAULT_TOP)

        return self.results

    def list_by_resource_id(self, source_resource_id, odata_query, top):
        self.log('List all items by resource id')
        try:
            items = self._list_event_subscriptions_by_resource_id(self.source_resource_id,
                                                                  self.odata_query,
                                                                  top)
        except ResourceNotFoundError as exc:
            self.fail("Failed to list all items in resource group - {0}".format(str(exc)))

        return self.filter_results(items)

    def list_by_location(self, resource_group_name, location, odata_query, top):
        self.log('List all items by location')
        try:
            if resource_group_name:
                items = self.client.event_subscriptions.list_regional_by_resource_group(resource_group_name,
                                                                                        location,
                                                                                        odata_query,
                                                                                        top)
            else:
                items = self.client.event_subscriptions.list_regional_by_subscription(location,
                                                                                      odata_query,
                                                                                      top)
        except ResourceNotFoundError as exc:
            self.fail("Failed to list all items - {0}".format(str(exc)))

        return self.filter_results(items)

    def filter_results(self, items):
        results = []
        for item in items:
            subscription = self.format_eventgrid_subscription(item)
            destination = item.destination
            if isinstance(destination, WebHookEventSubscriptionDestination):
                full_endpoint_url = self.client.event_subscriptions.get_full_url(item.topic, item.name)
                subscription["destination"]["endpoint_url"] = full_endpoint_url.endpoint_url

            if not isinstance(destination, StorageQueueEventSubscriptionDestination):
                delivery_attributes = self.client.event_subscriptions.get_delivery_attributes(item.topic, item.name)
                subscription["destination"]["delivery_attribute_mappings"] = delivery_attributes.as_dict()
            results.append(subscription)
        return results

    def format_eventgrid_subscription(self, event_subscription_data):
        results = event_subscription_data and event_subscription_data.as_dict() or {}
        return results

    def _list_event_subscriptions_by_resource_id(self, resource_id, oDataQuery, top):
        # parse_resource_id doesn't handle resource_ids for Azure subscriptions and RGs
        # so, first try to look for those two patterns.
        if resource_id is not None:
            id_parts = list(filter(None, resource_id.split('/')))
            if len(id_parts) < 5:
                # Azure subscriptions or Resource group
                if id_parts[0].lower() != "subscriptions":
                    self.fail('The specified value for source_resource_id is not in the'
                              ' expected format. It should start with /subscriptions.')

                subscription_id = id_parts[1]

                if len(id_parts) == 2:
                    return self.client.event_subscriptions.list_global_by_subscription_for_topic_type(
                        "Microsoft.Resources.Subscriptions",
                        oDataQuery,
                        top)

            if len(id_parts) == 4 and id_parts[2].lower() == "resourcegroups":
                resource_group_name = id_parts[3]
                if resource_group_name is None:
                    self.fail('The specified value for source_resource_id is not'
                              ' in the expected format. A valid value for'
                              ' resource group must be provided.')
                return self.client.event_subscriptions.list_global_by_resource_group_for_topic_type(
                    resource_group_name,
                    "Microsoft.Resources.ResourceGroups",
                    oDataQuery,
                    top)

        id_parts = parse_resource_id(resource_id)
        subscription_id = id_parts.get('subscription')

        rg_name = id_parts.get('resource_group')
        resource_name = id_parts.get('name')
        namespace = id_parts.get('namespace')
        resource_type = id_parts.get('type')

        if (subscription_id is None or rg_name is None or resource_name is None or
                namespace is None or resource_type is None):
            self.fail('The specified value for source_resource_id is not in the expected format.')

        # If this is for a domain topic, invoke the appropriate operation
        if (namespace.lower() == EVENTGRID_NAMESPACE.lower() and resource_type.lower() == EVENTGRID_DOMAINS.lower()):
            child_resource_type = id_parts.get('child_type_1')
            child_resource_name = id_parts.get('child_name_1')

            if (child_resource_type is not None and child_resource_type.lower() == EVENTGRID_TOPICS.lower() and
                    child_resource_name is not None):
                return self.client.event_subscriptions.list_by_domain_topic(rg_name, resource_name, child_resource_name, oDataQuery, top)

        # Not a domain topic, invoke the standard list_by_resource
        return self.client.event_subscriptions.list_by_resource(
            rg_name,
            namespace,
            resource_type,
            resource_name,
            oDataQuery,
            top)


def main():
    AzureRMEventgridSubscriptionInfo()


if __name__ == '__main__':
    main()
