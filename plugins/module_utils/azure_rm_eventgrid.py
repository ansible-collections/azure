# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# Copyright (c) 2025 Bill Peck, (@p3ck) - Additional changes to make it work for ansible
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import re
try:
    from dateutil.parser import parse
    from azure.mgmt.eventgrid.models import (
        EventSubscription,
        EventSubscriptionUpdateParameters,
        WebHookEventSubscriptionDestination,
        RetryPolicy,
        EventHubEventSubscriptionDestination,
        HybridConnectionEventSubscriptionDestination,
        ServiceBusQueueEventSubscriptionDestination,
        ServiceBusTopicEventSubscriptionDestination,
        AzureFunctionEventSubscriptionDestination,
        StorageBlobDeadLetterDestination,
        EventSubscriptionFilter,
        EventSubscriptionIdentity,
        DeliveryWithResourceIdentity,
        DeadLetterWithResourceIdentity,
        StorageQueueEventSubscriptionDestination)
except ImportError:
    # This is handled in azure_rm_common
    pass


IDENTITY_NO_IDENTITY = "NoIdentity"
IDENTITY_NONE = "None"
IDENTITY_SYSTEM_ASSIGNED = "SystemAssigned"
IDENTITY_USER_ASSIGNED = "UserAssigned"
IDENTITY_MIXED_MODE = "SystemAssigned, UserAssigned"

WEBHOOK_DESTINATION = "webhook"
EVENTHUB_DESTINATION = "eventhub"
STORAGEQUEUE_DESTINATION = "storagequeue"
HYBRIDCONNECTION_DESTINATION = "hybridconnection"
SERVICEBUSQUEUE_DESTINATION = "servicebusqueue"
SERVICEBUSTOPIC_DESTINATION = "servicebustopic"
AZUREFUNCTION_DESTINATION = "azurefunction"


class ConfigError(Exception):
    def __init__(self, message, **kwargs):
        self.__dict__.update(kwargs)
        super(ConfigError, self).__init__(message)


eventgrid_subscription_module_arg_spec = dict(
    azure_active_directory_application_id_or_uri=dict(
        type='str',
        required=False,
    ),
    azure_active_directory_tenant_id=dict(
        type='str',
        required=False,
    ),
    deadletter_endpoint=dict(
        type='str',
        required=False,
    ),
    delivery_attribute_mapping=dict(
        type='list',
        elements='str',
        required=False,
    ),
    endpoint=dict(
        type='str',
        required=False,
    ),
    endpoint_type=dict(
        type='str',
        choices=['azurefunction',
                 'eventhub',
                 'hybridconnection',
                 'servicebusqueue',
                 'servicebustopic',
                 'storagequeue',
                 'webhook'],
        default='webhook',
    ),
    event_delivery_schema=dict(
        type='str',
        choices=['CloudEventSchemaV1_0', 'CustomInputSchema', 'EventGridSchema'],
        required=False,
    ),
    event_ttl=dict(
        type='int',
        default=1440,
    ),
    expiration_date=dict(
        type='str',
        required=False,
    ),
    labels=dict(
        type='list',
        elements='str',
        required=False,
    ),
    max_delivery_attempts=dict(
        type='int',
        default=30,
        required=False,
    ),
    max_events_per_batch=dict(
        type='int',
        required=False,
    ),
    preferred_batch_size_in_kilobytes=dict(
        type='int',
        required=False,
    ),
    storage_queue_msg_ttl=dict(
        type='int',
        required=False,
    ),
    advanced_filter=dict(
        type='list',
        elements='str',
        required=False,
    ),
    enable_advanced_filtering_on_arrays=dict(
        type='bool',
        required=False,
    ),
    included_event_types=dict(
        type='list',
        elements='str',
        required=False,
    ),
    subject_begins_with=dict(
        type='str',
        required=False,
    ),
    subject_case_sensitive=dict(
        type='bool',
        required=False,
    ),
    subject_ends_with=dict(
        type='str',
        required=False,
    ),
)


def _validate_retry_policy(max_delivery_attempts, event_ttl):
    if max_delivery_attempts < 1 or max_delivery_attempts > 30:
        raise ConfigError('max_delivery_attempts should be a number between 1 and 30.')

    if event_ttl < 1 or event_ttl > 1440:
        raise ConfigError('event_ttl should be a number between 1 and 1440.')


def _validate_destination_attribute(endpoint_type, storage_queue_msg_ttl=None, delivery_attribute_mapping=None):
    isStorageQueueDestination = endpoint_type is not None and endpoint_type.lower() == STORAGEQUEUE_DESTINATION.lower()

    if not isStorageQueueDestination and storage_queue_msg_ttl is not None:
        raise ConfigError('usage error: storage_queue_msg_ttl is only applicable for endpoint type StorageQueue.')

    if isStorageQueueDestination and delivery_attribute_mapping is not None:
        raise ConfigError('usage error: delivery_attribute_mapping is not applicable for endpoint type StorageQueue.')


def _get_storage_queue_destination(endpoint, storage_queue_msg_ttl):
    # Supplied endpoint would be in the following format:
    # /subscriptions/.../storageAccounts/sa1/queueServices/default/queues/{queueName}))
    # and we need to break it up into:
    # /subscriptions/.../storageAccounts/sa1 and queueName
    queue_items = re.split(
        "/queueServices/default/queues/", endpoint, flags=re.IGNORECASE)

    if len(queue_items) != 2 or queue_items[0] is None or queue_items[1] is None:
        raise ConfigError('Argument Error: Expected format of endpoint for storage queue is:' +
                          '/subscriptions/id/resourceGroups/rg/providers/Microsoft.Storage/' +
                          'storageAccounts/sa1/queueServices/default/queues/queueName')

    if storage_queue_msg_ttl is not None:
        destination = StorageQueueEventSubscriptionDestination(
            resource_id=queue_items[0],
            queue_name=queue_items[1],
            queue_message_time_to_live_in_seconds=storage_queue_msg_ttl)
    else:
        destination = StorageQueueEventSubscriptionDestination(
            resource_id=queue_items[0],
            queue_name=queue_items[1])
    return destination


def _get_endpoint_destination(
        endpoint_type,
        endpoint,
        max_events_per_batch,
        preferred_batch_size_in_kilobytes,
        azure_active_directory_tenant_id,
        azure_active_directory_application_id_or_uri,
        storage_queue_msg_ttl,
        delivery_attribute_mapping):

    if endpoint_type.lower() == WEBHOOK_DESTINATION.lower():
        destination = WebHookEventSubscriptionDestination(
            endpoint_url=endpoint,
            max_events_per_batch=max_events_per_batch,
            preferred_batch_size_in_kilobytes=preferred_batch_size_in_kilobytes,
            azure_active_directory_tenant_id=azure_active_directory_tenant_id,
            azure_active_directory_application_id_or_uri=azure_active_directory_application_id_or_uri,
            delivery_attribute_mappings=delivery_attribute_mapping)
    elif endpoint_type.lower() == EVENTHUB_DESTINATION.lower():
        destination = EventHubEventSubscriptionDestination(
            resource_id=endpoint,
            delivery_attribute_mappings=delivery_attribute_mapping)
    elif endpoint_type.lower() == HYBRIDCONNECTION_DESTINATION.lower():
        destination = HybridConnectionEventSubscriptionDestination(
            resource_id=endpoint,
            delivery_attribute_mappings=delivery_attribute_mapping)
    elif endpoint_type.lower() == STORAGEQUEUE_DESTINATION.lower():
        destination = _get_storage_queue_destination(endpoint, storage_queue_msg_ttl)
    elif endpoint_type.lower() == SERVICEBUSQUEUE_DESTINATION.lower():
        destination = ServiceBusQueueEventSubscriptionDestination(
            resource_id=endpoint,
            delivery_attribute_mappings=delivery_attribute_mapping)
    elif endpoint_type.lower() == SERVICEBUSTOPIC_DESTINATION.lower():
        destination = ServiceBusTopicEventSubscriptionDestination(
            resource_id=endpoint,
            delivery_attribute_mappings=delivery_attribute_mapping)
    elif endpoint_type.lower() == AZUREFUNCTION_DESTINATION.lower():
        destination = AzureFunctionEventSubscriptionDestination(
            resource_id=endpoint,
            max_events_per_batch=max_events_per_batch,
            preferred_batch_size_in_kilobytes=preferred_batch_size_in_kilobytes,
            delivery_attribute_mappings=delivery_attribute_mapping)
    return destination


def _get_event_subscription_identity_type(identity_type_name):
    result = None
    if identity_type_name.lower() == IDENTITY_SYSTEM_ASSIGNED.lower():
        result = IDENTITY_SYSTEM_ASSIGNED

    return result


def _get_deadletter_destination(deadletter_endpoint):
    blob_items = re.split(
        "/blobServices/default/containers/", deadletter_endpoint, flags=re.IGNORECASE)

    if len(blob_items) != 2 or blob_items[0] is None or blob_items[1] is None:
        raise ConfigError('Argument Error: Expected format of deadletter_endpoint is:' +
                          '/subscriptions/id/resourceGroups/rg/providers/Microsoft.Storage/' +
                          'storageAccounts/sa1/blobServices/default/containers/containerName')

    return StorageBlobDeadLetterDestination(resource_id=blob_items[0], blob_container_name=blob_items[1])


def _get_tenant_id(destination, destination_with_resource_identity):
    tenant_id = None

    if destination is not None and hasattr(destination, 'azure_active_directory_tenant_id'):
        tenant_id = destination.azure_active_directory_tenant_id
    elif destination_with_resource_identity is not None and hasattr(destination_with_resource_identity, 'azure_active_directory_tenant_id'):  # nopep8: E501
        tenant_id = destination_with_resource_identity.azure_active_directory_tenant_id

    return tenant_id


def _get_application_id(destination, destination_with_resource_identity):
    application_id = None

    if destination is not None and hasattr(destination, 'azure_active_directory_application_id_or_uri'):
        application_id = destination.azure_active_directory_application_id_or_uri
    elif destination_with_resource_identity is not None and hasattr(destination_with_resource_identity, 'azure_active_directory_application_id_or_uri'):  # nopep8: E501
        application_id = destination_with_resource_identity.azure_active_directory_application_id_or_uri
    return application_id


def _set_event_subscription_destination(
        destination,
        storage_queue_msg_ttl=None,
        delivery_attribute_mapping=None):

    endpoint_type = destination.endpoint_type
    if endpoint_type.lower() == WEBHOOK_DESTINATION.lower():
        if delivery_attribute_mapping is not None:
            destination.delivery_attribute_mappings = delivery_attribute_mapping
    elif endpoint_type.lower() == EVENTHUB_DESTINATION.lower():
        if delivery_attribute_mapping is not None:
            destination.delivery_attribute_mappings = delivery_attribute_mapping
    elif endpoint_type.lower() == HYBRIDCONNECTION_DESTINATION.lower():
        if delivery_attribute_mapping is not None:
            destination.delivery_attribute_mappings = delivery_attribute_mapping
    elif endpoint_type.lower() == STORAGEQUEUE_DESTINATION.lower():
        if storage_queue_msg_ttl is not None:
            destination.queue_message_time_to_live_in_seconds = storage_queue_msg_ttl
    elif endpoint_type.lower() == SERVICEBUSQUEUE_DESTINATION.lower():
        if delivery_attribute_mapping is not None:
            destination.delivery_attribute_mappings = delivery_attribute_mapping
    elif endpoint_type.lower() == SERVICEBUSTOPIC_DESTINATION.lower():
        if delivery_attribute_mapping is not None:
            destination.delivery_attribute_mappings = delivery_attribute_mapping
    elif endpoint_type.lower() == AZUREFUNCTION_DESTINATION.lower():
        if delivery_attribute_mapping is not None:
            destination.delivery_attribute_mappings = delivery_attribute_mapping
    return destination


def _validate_and_update_destination(endpoint_type, destination, storage_queue_msg_ttl, delivery_attribute_mapping):
    _validate_destination_attribute(
        endpoint_type,
        storage_queue_msg_ttl,
        delivery_attribute_mapping)

    _set_event_subscription_destination(
        destination,
        storage_queue_msg_ttl,
        delivery_attribute_mapping)


def _update_event_subscription_filter(
        event_subscription_filter,
        subject_begins_with=None,
        subject_ends_with=None,
        included_event_types=None,
        enable_advanced_filtering_on_arrays=None,
        advanced_filter=None):

    if subject_begins_with is not None:
        event_subscription_filter.subject_begins_with = subject_begins_with

    if subject_ends_with is not None:
        event_subscription_filter.subject_ends_with = subject_ends_with

    if included_event_types is not None:
        event_subscription_filter.included_event_types = included_event_types

    if enable_advanced_filtering_on_arrays is not None:
        event_subscription_filter.enable_advanced_filtering_on_arrays = enable_advanced_filtering_on_arrays

    if advanced_filter is not None:
        event_subscription_filter.advanced_filters = advanced_filter


def get_event_subscription_info(endpoint=None,
                                endpoint_type=WEBHOOK_DESTINATION,
                                included_event_types=None,
                                subject_begins_with=None,
                                subject_ends_with=None,
                                is_subject_case_sensitive=False,
                                max_delivery_attempts=30,
                                event_ttl=1440,
                                max_events_per_batch=None,
                                preferred_batch_size_in_kilobytes=None,
                                event_delivery_schema=None,
                                deadletter_endpoint=None,
                                labels=None,
                                expiration_date=None,
                                advanced_filter=None,
                                azure_active_directory_tenant_id=None,
                                azure_active_directory_application_id_or_uri=None,
                                delivery_identity=None,
                                delivery_identity_endpoint=None,
                                delivery_identity_endpoint_type=None,
                                deadletter_identity=None,
                                deadletter_identity_endpoint=None,
                                storage_queue_msg_ttl=None,
                                enable_advanced_filtering_on_arrays=None,
                                delivery_attribute_mapping=None):

    normalized_endpoint_type = endpoint_type.lower()
    normalized_webhook_destination = WEBHOOK_DESTINATION.lower()
    normalized_azure_function_destination = AZUREFUNCTION_DESTINATION.lower()

    if deadletter_endpoint is not None and deadletter_identity_endpoint is not None:
        raise ConfigError('usage error: either deadletter_endpoint or deadletter_identity_endpoint '
                          'should be specified at one time, not both')

    if included_event_types is not None and len(included_event_types) == 1 and included_event_types[0].lower() == 'all':
        raise ConfigError('The usage of \"All\" for included_event_types is not allowed starting from Azure Event Grid'
                          ' API Version 2019-02-01-preview.')

    # Construct RetryPolicy based on max_delivery_attempts and event_ttl
    _validate_retry_policy(max_delivery_attempts, event_ttl)
    retry_policy = RetryPolicy(max_delivery_attempts=max_delivery_attempts, event_time_to_live_in_minutes=event_ttl)

    if max_events_per_batch is not None:
        if normalized_endpoint_type not in (normalized_webhook_destination, normalized_azure_function_destination):
            raise ConfigError('usage error: max_events_per_batch is applicable only for '
                              'endpoint types WebHook and AzureFunction.')
        if max_events_per_batch > 5000:
            raise ConfigError('usage error: max_events_per_batch must be a number between 1 and 5000.')

    if preferred_batch_size_in_kilobytes is not None:
        if normalized_endpoint_type not in (normalized_webhook_destination, normalized_azure_function_destination):
            raise ConfigError('usage error: preferred_batch_size_in_kilobytes is applicable only for '
                              'endpoint types WebHook and AzureFunction.')
        if preferred_batch_size_in_kilobytes > 1024:
            raise ConfigError('usage error: preferred_batch_size_in_kilobytes must be a number '
                              'between 1 and 1024.')

    if azure_active_directory_tenant_id is not None:
        if normalized_endpoint_type != normalized_webhook_destination:
            raise ConfigError('usage error: azure_active_directory_tenant_id is applicable only for '
                              'endpoint types WebHook.')
        if azure_active_directory_application_id_or_uri is None:
            raise ConfigError('usage error: azure_active_directory_application_id_or_uri is missing. '
                              'It should include an Azure Active Directory Application Id or Uri.')

    if azure_active_directory_application_id_or_uri is not None:
        if normalized_endpoint_type != normalized_webhook_destination:
            raise ConfigError('usage error: azure_active_directory_application_id_or_uri is applicable only for '
                              'endpoint types WebHook.')
        if azure_active_directory_tenant_id is None:
            raise ConfigError('usage error: azure_active_directory_tenant_id is missing. '
                              'It should include an Azure Active Directory Tenant Id.')

    condition1 = deadletter_identity is not None and deadletter_identity_endpoint is None
    condition2 = deadletter_identity is None and deadletter_identity_endpoint is not None
    if condition1 or condition2:
        raise ConfigError('usage error: one or more deadletter identity information is missing. If '
                          'deadletter_identity is specified, deadletter_identity_endpoint should be specified.')

    tennant_id = None
    application_id = None

    condition1 = endpoint_type is not None and normalized_endpoint_type == normalized_webhook_destination
    condition2 = delivery_identity_endpoint_type is not None and \
        delivery_identity_endpoint_type.lower() == normalized_webhook_destination
    if condition1 or condition2:
        tennant_id = azure_active_directory_tenant_id
        application_id = azure_active_directory_application_id_or_uri

    destination = None
    delivery_with_resource_identity = None
    if endpoint is not None:
        _validate_destination_attribute(endpoint_type, storage_queue_msg_ttl, delivery_attribute_mapping)
        destination = _get_endpoint_destination(
            endpoint_type,
            endpoint,
            max_events_per_batch,
            preferred_batch_size_in_kilobytes,
            tennant_id,
            application_id,
            storage_queue_msg_ttl,
            delivery_attribute_mapping)
    elif delivery_identity_endpoint is not None:
        identity_type_name = _get_event_subscription_identity_type(delivery_identity)
        delivery_identity_info = EventSubscriptionIdentity(type=identity_type_name)
        _validate_destination_attribute(
            delivery_identity_endpoint_type,
            storage_queue_msg_ttl,
            delivery_attribute_mapping)
        destination_with_identity = _get_endpoint_destination(
            delivery_identity_endpoint_type,
            delivery_identity_endpoint,
            max_events_per_batch,
            preferred_batch_size_in_kilobytes,
            tennant_id,
            application_id,
            storage_queue_msg_ttl,
            delivery_attribute_mapping)
        delivery_with_resource_identity = DeliveryWithResourceIdentity(
            identity=delivery_identity_info,
            destination=destination_with_identity)

    event_subscription_filter = EventSubscriptionFilter(
        subject_begins_with=subject_begins_with,
        subject_ends_with=subject_ends_with,
        included_event_types=included_event_types,
        is_subject_case_sensitive=is_subject_case_sensitive,
        enable_advanced_filtering_on_arrays=enable_advanced_filtering_on_arrays,
        advanced_filters=advanced_filter)

    deadletter_destination = None
    if deadletter_endpoint is not None:
        deadletter_destination = _get_deadletter_destination(deadletter_endpoint)

    deadletter_with_resource_identity = None

    if deadletter_identity_endpoint is not None:
        deadletter_destination_with_identity = _get_deadletter_destination(deadletter_identity_endpoint)
        deadletter_identity_type_name = _get_event_subscription_identity_type(deadletter_identity)
        deadletter_delivery_identity_info = EventSubscriptionIdentity(type=deadletter_identity_type_name)
        deadletter_with_resource_identity = DeadLetterWithResourceIdentity(
            identity=deadletter_delivery_identity_info,
            dead_letter_destination=deadletter_destination_with_identity)

    if expiration_date is not None:
        expiration_date = parse(expiration_date)

    event_subscription_info = EventSubscription(
        destination=destination,
        filter=event_subscription_filter,
        labels=labels,
        event_delivery_schema=event_delivery_schema,
        retry_policy=retry_policy,
        expiration_time_utc=expiration_date,
        dead_letter_destination=deadletter_destination,
        delivery_with_resource_identity=delivery_with_resource_identity,
        dead_letter_with_resource_identity=deadletter_with_resource_identity)

    return event_subscription_info


def update_event_subscription_internal(instance,
                                       endpoint=None,
                                       endpoint_type=WEBHOOK_DESTINATION,
                                       subject_begins_with=None,
                                       subject_ends_with=None,
                                       included_event_types=None,
                                       advanced_filter=None,
                                       labels=None,
                                       deadletter_endpoint=None,
                                       delivery_identity=None,
                                       delivery_identity_endpoint=None,
                                       delivery_identity_endpoint_type=None,
                                       deadletter_identity=None,
                                       deadletter_identity_endpoint=None,
                                       storage_queue_msg_ttl=None,
                                       enable_advanced_filtering_on_arrays=None,
                                       delivery_attribute_mapping=None):

    if (endpoint_type is not None and
            endpoint_type.lower() != WEBHOOK_DESTINATION.lower() and
            endpoint is None):
        raise ConfigError('Invalid usage: Since endpoint_type is specified, a valid endpoint must also be specified.')

    current_destination = instance.destination
    current_filter = instance.filter
    current_event_delivery_schema = instance.event_delivery_schema
    current_retry_policy = instance.retry_policy
    current_destination_with_resource_identity = None
    current_destination2 = None

    if instance.delivery_with_resource_identity is not None:
        current_destination2 = instance.delivery_with_resource_identity
        current_destination_with_resource_identity = instance.delivery_with_resource_identity.destination

    tenant_id = _get_tenant_id(current_destination, current_destination_with_resource_identity)
    application_id = _get_application_id(current_destination, current_destination_with_resource_identity)

    # for the update path, endpoint_type can be None but it does not mean that this is webhook,
    # as it can be other types too.
    current_max_events_per_batch = 0
    current_preferred_batch_size_in_kilobytes = 0

    if current_destination is not None and (current_destination.endpoint_type.lower() == WEBHOOK_DESTINATION.lower() or current_destination.endpoint_type.lower() == AZUREFUNCTION_DESTINATION.lower()):  # nopep8: E501
        current_max_events_per_batch = current_destination.max_events_per_batch
        current_preferred_batch_size_in_kilobytes = current_destination.preferred_batch_size_in_kilobytes
    elif current_destination_with_resource_identity is not None and (current_destination_with_resource_identity.endpoint_type.lower() == WEBHOOK_DESTINATION.lower() or current_destination_with_resource_identity.endpoint_type.lower() == AZUREFUNCTION_DESTINATION.lower()):  # nopep8: E501
        current_max_events_per_batch = current_destination_with_resource_identity.max_events_per_batch
        current_preferred_batch_size_in_kilobytes = current_destination_with_resource_identity.preferred_batch_size_in_kilobytes  # nopep8: E501

    updated_destination = None
    updated_delivery_with_resource_identity = None

    # if endpoint and delivery_identity_endpoint is not specified then use the instance value
    if endpoint is None and delivery_identity_endpoint is None:
        if current_destination is not None:
            _validate_and_update_destination(
                current_destination.endpoint_type,
                current_destination,
                storage_queue_msg_ttl,
                delivery_attribute_mapping)
            updated_destination = current_destination
        elif current_destination_with_resource_identity is not None:
            _validate_and_update_destination(
                current_destination_with_resource_identity.endpoint_type,
                current_destination_with_resource_identity,
                storage_queue_msg_ttl,
                delivery_attribute_mapping)
            updated_delivery_with_resource_identity = current_destination2
    elif endpoint is not None:
        # If this is the update path, the user does not
        # have to specify the endpoint type so it might
        # be None
        if endpoint_type is None:
            endpoint_type = current_destination.endpoint_type

        _validate_destination_attribute(
            endpoint_type,
            storage_queue_msg_ttl,
            delivery_attribute_mapping)
        updated_destination = _get_endpoint_destination(
            endpoint_type,
            endpoint,
            current_max_events_per_batch,
            current_preferred_batch_size_in_kilobytes,
            tenant_id,
            application_id,
            storage_queue_msg_ttl,
            delivery_attribute_mapping)
    elif delivery_identity_endpoint is not None:
        destination_with_identity = _get_endpoint_destination(
            delivery_identity_endpoint_type,
            delivery_identity_endpoint,
            0,
            0,
            tenant_id,
            application_id,
            storage_queue_msg_ttl,
            delivery_attribute_mapping)

        identity_type_name = _get_event_subscription_identity_type(delivery_identity)
        delivery_identity_info = EventSubscriptionIdentity(type=identity_type_name)

        updated_delivery_with_resource_identity = DeliveryWithResourceIdentity(
            identity=delivery_identity_info,
            destination=destination_with_identity)

    updated_deadletter_destination = None
    if deadletter_endpoint is not None:
        updated_deadletter_destination = _get_deadletter_destination(deadletter_endpoint)

    updated_deadletter_with_resource_identity = None
    if deadletter_identity_endpoint is not None:
        deadletter_destination_with_identity = _get_deadletter_destination(deadletter_identity_endpoint)
        deadletter_identity_type_name = _get_event_subscription_identity_type(deadletter_identity)
        deadletter_delivery_identity_info = EventSubscriptionIdentity(type=deadletter_identity_type_name)
        updated_deadletter_with_resource_identity = DeadLetterWithResourceIdentity(
            identity=deadletter_delivery_identity_info,
            dead_letter_destination=deadletter_destination_with_identity)

    _update_event_subscription_filter(
        current_filter,
        subject_begins_with,
        subject_ends_with,
        included_event_types,
        enable_advanced_filtering_on_arrays,
        advanced_filter)
    updated_filter = current_filter

    updated_labels = None
    if labels is not None:
        updated_labels = labels

    params = EventSubscriptionUpdateParameters(
        destination=updated_destination,
        filter=updated_filter,
        labels=updated_labels,
        retry_policy=current_retry_policy,
        dead_letter_destination=updated_deadletter_destination,
        event_delivery_schema=current_event_delivery_schema,
        delivery_with_resource_identity=updated_delivery_with_resource_identity,
        dead_letter_with_resource_identity=updated_deadletter_with_resource_identity)

    return params
