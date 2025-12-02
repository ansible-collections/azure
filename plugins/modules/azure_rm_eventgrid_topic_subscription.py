#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_eventgrid_topic_subscription
version_added: "3.13.0"
short_description: Manage Eventgrid Topic Subscriptions
description:
    - Create, update ,delete and replace Eventgrid Topic Subscriptions.
options:
    name:
        description:
            - Name of the subscription.
        required: true
        type: str
    topic_name:
        description:
            - Name of the topic.
        required: true
        type: str
    resource_group:
        description:
            - Name of a resource group where the topic exists or will be created.
        required: true
        type: str
    state:
        description:
            - State of the Eventgrid Topic Event Subscription. Use C(present) to create
              or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present


extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_eventgrid_subscription

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Subscribe to custom topic
  azure.azcollection.azure_rm_eventgrid_subscription:
    name: subscription-xxxxx20070
    topic_name: topic-xxxxx20070
    endpoint: https://event-grid-site-xxxxx20070.azurewebsites.net/api/updates
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: true
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


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_eventgrid import (
    eventgrid_subscription_module_arg_spec, get_event_subscription_info,
    update_event_subscription_internal, ConfigError)
try:
    from azure.mgmt.eventgrid import EventGridManagementClient
    from azure.core.polling import LROPoller
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMEventgridSubscription(AzureRMModuleBaseExt):

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
                required=True
            ),
            topic_name=dict(
                type='str',
                required=True,
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
        )
        self.module_arg_spec.update(eventgrid_subscription_module_arg_spec)

        self._client = None

        self.name = None
        self.topic_name = None
        self.resource_group = None
        self.state = None
        self.endpoint = None
        self.endpoint_type = None
        self.included_event_types = None
        self.subject_begins_with = None
        self.subject_ends_with = None
        self.is_subject_case_sensitive = None
        self.max_delivery_attempts = None
        self.event_ttl = None
        self.max_events_per_batch = None
        self.preferred_batch_size_in_kilobytes = None
        self.event_delivery_schema = None
        self.deadletter_endpoint = None
        self.labels = None
        self.expiration_date = None
        self.advanced_filter = None
        self.azure_active_directory_tenant_id = None
        self.azure_active_directory_application_id_or_uri = None
        self.storage_queue_msg_ttl = None
        self.enable_advanced_filtering_on_arrays = None
        self.delivery_attribute_mapping = None

        self.results = dict(
            changed=False,
            eventgrid_topic_event_subscription=dict()
        )

        required_together = None
        required_if = None
#        required_together = [['extended_location_name', 'extended_location_type']]
#        required_if = [
#            ("kind", "AzureArc", ["extended_location_name"]),
#        ]

        super(AzureRMEventgridSubscription, self).__init__(self.module_arg_spec,
                                                           supports_tags=False,
                                                           supports_check_mode=True,
                                                           required_together=required_together,
                                                           required_if=required_if)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        changed = False

        if self.state == 'present':
            event_subscription_info = self.get_event_subscription(self.resource_group,
                                                                  self.topic_name,
                                                                  self.name)
            if event_subscription_info:
                try:
                    params = update_event_subscription_internal(
                        instance=event_subscription_info,
                        endpoint=self.endpoint,
                        endpoint_type=self.update_endpoint_type,
                        subject_begins_with=self.subject_begins_with,
                        subject_ends_with=self.subject_ends_with,
                        included_event_types=self.included_event_types,
                        advanced_filter=self.advanced_filter,
                        labels=self.labels,
                        deadletter_endpoint=self.deadletter_endpoint,
                        delivery_identity=None,
                        delivery_identity_endpoint=None,
                        delivery_identity_endpoint_type=None,
                        deadletter_identity=None,
                        deadletter_identity_endpoint=None,
                        storage_queue_msg_ttl=self.storage_queue_msg_ttl,
                        enable_advanced_filtering_on_arrays=self.enable_advanced_filtering_on_arrays,
                        delivery_attribute_mapping=self.delivery_attribute_mapping)
                except ConfigError as exc:
                    self.fail(str(exc))

                self.results['compare'] = []
                changed = not self.default_compare({},
                                                   self.format_event_subscription(params),
                                                   self.format_event_subscription(event_subscription_info),
                                                   '',
                                                   self.results)
                if changed and not self.check_mode:
                    event_subscription_info = self.begin_update_event_subscription(self.resource_group,
                                                                                   self.topic_name,
                                                                                   self.name,
                                                                                   params)
                    response = self.format_subscription_info(event_subscription_info)

            else:
                changed = True

                try:
                    event_subscription_info = get_event_subscription_info(
                        endpoint=self.endpoint,
                        endpoint_type=self.endpoint_type,
                        included_event_types=self.included_event_types,
                        subject_begins_with=self.subject_begins_with,
                        subject_ends_with=self.subject_ends_with,
                        is_subject_case_sensitive=self.is_subject_case_sensitive,
                        max_delivery_attempts=self.max_delivery_attempts,
                        event_ttl=self.event_ttl,
                        max_events_per_batch=self.max_events_per_batch,
                        preferred_batch_size_in_kilobytes=self.preferred_batch_size_in_kilobytes,
                        event_delivery_schema=self.event_delivery_schema,
                        deadletter_endpoint=self.deadletter_endpoint,
                        labels=self.labels,
                        expiration_date=self.expiration_date,
                        advanced_filter=self.advanced_filter,
                        azure_active_directory_tenant_id=self.azure_active_directory_tenant_id,
                        azure_active_directory_application_id_or_uri=self.azure_active_directory_application_id_or_uri,
                        delivery_identity=None,
                        delivery_identity_endpoint=None,
                        delivery_identity_endpoint_type=None,
                        deadletter_identity=None,
                        deadletter_identity_endpoint=None,
                        storage_queue_msg_ttl=self.storage_queue_msg_ttl,
                        enable_advanced_filtering_on_arrays=self.enable_advanced_filtering_on_arrays,
                        delivery_attribute_mapping=self.delivery_attribute_mapping)
                except ConfigError as exc:
                    self.fail(str(exc))

                if not self.check_mode:
                    event_subscription_info = self.begin_create_or_update_event_subscription(self.resource_group,
                                                                                             self.topic_name,
                                                                                             self.name,
                                                                                             event_subscription_info)
                response = self.format_subscription_info(event_subscription_info)
        else:
            event_subscription_info = self.get_event_subscription(self.resource_group,
                                                                  self.topic_name,
                                                                  self.name)
            if event_subscription_info:
                changed = True
                if not self.check_mode:
                    response = self.delete_event_subscription(self.resource_group,
                                                              self.topic_name,
                                                              self.name)
                else:
                    response = self.format_event_subscription(event_subscription_info)

        self.results['changed'] = changed
        self.results['eventgrid_topic_event_subscription'] = response

        return self.results

    def begin_create_or_update_event_subscription(self,
                                                  resource_group,
                                                  topic_name,
                                                  event_subscription_name,
                                                  event_subscription_info):
        self.log('Creates or updates the Eventgrid Topic Event Subscription.')

        try:
            response = self.client.topic_event_subscriptions.begin_create_or_update(resource_group,
                                                                                    topic_name,
                                                                                    event_subscription_name,
                                                                                    event_subscription_info)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail('Creates or updates the Eventgrid Topic Event Subscription got Exception as as {0}'.format(exc.message or str(exc)))
        return response

    def begin_update_event_subscription(self,
                                        resource_group,
                                        topic_name,
                                        event_subscription_name,
                                        event_subscription_update_parameters):
        self.log('Selectively updates the Event Subscription.')

        try:
            response = self.client.topic_event_subscriptions.begin_update(resource_group,
                                                                          topic_name,
                                                                          event_subscription_name,
                                                                          event_subscription_update_parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail('Selectively update the Eventgrid Topic Event Subscription got Excption as {0}'.format(str(exc)))
        return response

    def delete_event_subscription(self, resource_group, topic_name, event_subsription_name):
        self.log('Deletes the entire Eventgrid Topic Event Subscription.')
        try:
            return self.client.topic_event_subscriptions.delete(resource_group, topic_name, event_subsription_name)
        except Exception as exc:
            self.fail('Delete Event Subscription got Excetion as {0}'.format(str(exc)))

    def get_event_subscription(self, resource_group, topic_name, event_subscription_name):
        self.log('Get properties for {0}'.format(topic_name))
        try:
            return self.client.topic_event_subscriptions.get(resource_group, topic_name, event_subscription_name)
        except ResourceNotFoundError:
            self.log('Did not find the event_subscription.')
            return False
        except Exception as exc:
            self.fail('Error trying to get event_subscription got Excetion as {0}'.format(str(exc)))

    def format_event_subscription(self, event_subscription_data):
        results = event_subscription_data and event_subscription_data.as_dict() or {}
        return results


def main():
    AzureRMEventgridSubscription()


if __name__ == '__main__':
    main()
