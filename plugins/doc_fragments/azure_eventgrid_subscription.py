# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Bill Peck, <@p3ck>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):

    # Azure doc fragment
    DOCUMENTATION = r'''
options:
    azure_active_directory_application_id_or_uri:
        description:
            - The Azure Active Directory Application Id or Uri to get the access token
              that will be included as the bearer token in delivery requests. Applicable
              only for webhook as a destination.
        required: false
        type: str
    azure_active_directory_tenant_id:
        description:
            - The Azure Active Directory Tenant Id to get the access token that will be
              included as the bearer token in delivery requests. Applicable only for
              webhook as a destination.
        required: false
        type: str
    deadletter_endpoint:
        description:
            - The Azure resource ID of an Azure Storage blob container destination where
              EventGrid should deadletter undeliverable events for this event subscription.
        required: false
        type: str
    delivery_attribute_mapping:
        description:
            - Add delivery attribute mapping to send additional information via HTTP headers
              when delivering events. This attribute is valid for all destination types except
              StorageQueue.
            - Format attribute-name attribute-type attribute-value [attribute-is-secret]
            - somename dynamic somevalue true
            - somename2 static somevalue
        type: list
        elements: str
    endpoint:
        description:
            - Endpoint where EventGrid should deliver events matching this event subscription.
              For webhook endpoint type, this should be the corresponding webhook URL. For
              other endpoint types, this should be the Azure resource identifier of the endpoint.
              It is expected that the destination endpoint to be already created and available
              for use before executing any Event Grid command.
        required: false
        type: str
    endpoint_type:
        description:
            - The type of the destination endpoint.
        type: str
        choices:
            - azurefunction
            - eventhub
            - hybridconnection
            - servicebusqueue
            - servicebustopic
            - storagequeue
            - webhook
        default: webhook
    event_delivery_schema:
        description:
            - The schema in which events should be delivered for this event subscription.
              By default, events will be delivered in the same schema in which they are
              published (based on the corresponding topic's input schema).
        type: str
        choices:
            - CloudEventSchemaV1_0
            - CustomInputSchema
            - EventGridSchema
    event_ttl:
        description:
            - Event time to live (in minutes). Must be a number between 1 and 1440.
        type: int
        default: 1440
    expiration_date:
        description:
            - Date or datetime (in UTC, e.g. '2018-11-30T11:59:59+00:00' or '2018-11-30')
              after which the event subscription would expire. By default, there is no expiration
              for the event subscription.
        type: str
    labels:
        description:
            - A list of labels to associate with this event subscription.
        type: list
        elements: str
    max_delivery_attempts:
        description:
            - Maximum number of delivery attempts. Must be a number between 1 and 30.
        type: int
        default: 30
    max_events_per_batch:
        description:
            - Maximum number of events in a batch. Must be a number between 1 and 5000.
        type: int
    preferred_batch_size_in_kilobytes:
        description:
            - Preferred batch size in kilobytes. Must be a number between 1 and 1024.
        type: int
    storage_queue_msg_ttl:
        description:
            - Storage queue message time to live in seconds.
        type: int
    advanced_filter:
        description:
            - An advanced filter enables filtering of events based on a specific event property.
            - KEY[.INNERKEY] FILTEROPERATOR VALUE [VALUE ...]
            - Examples
            - data.Color StringIn Blue Red Orange Yellow
            - data.Color StringNotIn Blue Red Orange Yellow
            - subject StringContains Blue Red
            - subject StringNotContains Blue Red
            - subject StringBeginsWith Blue Red
            - subject StringNotBeginsWith Blue Red
            - subject StringEndsWith img png jpg
            - subject StringNotEndsWith img png jpg
            - data.property1 NumberIn 5 10 20
            - data.property1 NumberInRange 5,10 20,30 40,50
            - data.property2 NumberNotIn 100 200 300
            - data.property2 NumberNotInRange 100,110 200,210 300,310
            - data.property3 NumberLessThan 100
            - data.property2 NumberLessThanOrEquals 100
            - data.property3 NumberGreaterThan 100
            - data.property2 NumberGreaterThanOrEquals 100
            - data.property3 BoolEquals true
            - data.property3 IsNullOrUndefined
            - data.property3 IsNotNull
        type: list
        elements: str
    enable_advanced_filtering_on_arrays:
        description:
            - Allows advanced filters to be evaluated against an array of values
              instead of expecting a singular value.
        type: bool
    included_event_types:
        description:
            - A list of event types (e.g., Microsoft.Storage.BlobCreated and
              Microsoft.Storage.BlobDeleted). In order to subscribe to all default event types,
              do not specify any value for this argument. For event grid topics, event types are
              customer defined. For Azure events, e.g., Storage Accounts, IoT Hub, etc.,
              you can query their event types using this CLI command
              'az eventgrid topic-type list-event-types'.
        type: list
        elements: str
    subject_begins_with:
        description:
            - An optional string to filter events for an event subscription based on a prefix.
              Wildcard characters are not supported.
        type: str
    subject_case_sensitive:
        description:
            - Specify to indicate whether the subject fields should be compared in a case sensitive
              manner. True if flag present.
        type: bool
    subject_ends_with:
        description:
            - An optional string to filter events for an event subscription based on a suffix.
              Wildcard characters are not supported.
        type: str
'''
