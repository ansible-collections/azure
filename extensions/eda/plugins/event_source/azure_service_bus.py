# Copyright (c) 2025 Red Hat, Inc.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Ansible-rulebook event source plugin for Azure Service Bus.

This module provides asynchronous consumers for Azure Service Bus to feed
events into Ansible EDA rulebooks.
"""

import asyncio
import contextlib
import dataclasses
import json
import logging
import uuid
from typing import Any

from azure.identity.aio import ClientSecretCredential
from azure.servicebus import ServiceBusReceivedMessage
from azure.servicebus.aio import ServiceBusClient, ServiceBusReceiver

DOCUMENTATION = r"""
---
short_description: Receive events from an Azure service bus.
description:
  - An ansible-rulebook event source module for receiving events from an Azure service bus.
  - Supports both connection string and service principal authentication.
  - Can receive from queues or topic subscriptions.
  - In order to get the service bus and the connection string, refer to
    https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-python-how-to-use-queues?tabs=passwordless
  - Each event is assigned a valid RFC 4122 UUID under meta.uuid.
  - If the message_id from Azure Service Bus is already a valid UUID it is used directly.
  - If the message_id is not a valid UUID, a deterministic UUID5 is generated from
    queue_name and sequence_number (broker-assigned, unique within the queue) to ensure
    uniqueness within the configured queue. The original value is always preserved under meta.message_id.
options:
  conn_str:
    description:
      - The connection string to connect to the Azure service bus.
      - Either conn_str OR (tenant_id, client_id, client_secret, namespace) must be provided.
    type: str
    required: false
  azure_tenant_id:
    description:
      - Azure Active Directory tenant ID for service principal authentication.
      - Required if conn_str is not provided.
    type: str
    required: false
  azure_client_id:
    description:
      - Azure service principal client ID (application ID).
      - Required if conn_str is not provided.
    type: str
    required: false
  azure_client_secret:
    description:
      - Azure service principal client secret.
      - Required if conn_str is not provided.
    type: str
    required: false
  azure_namespace:
    description:
      - Azure Service Bus namespace (e.g., 'myservicebus.servicebus.windows.net').
      - Required if conn_str is not provided.
    type: str
    required: false
  queue_name:
    description:
      - The name of the queue to pull messages from.
      - Either queue_name OR (azure_topic_name AND azure_subscription_name) must be provided.
    type: str
    required: false
  azure_topic_name:
    description:
      - The name of the topic to pull messages from.
      - Requires azure_subscription_name to be set.
    type: str
    required: false
  azure_subscription_name:
    description:
      - The name of the subscription under the topic.
      - Requires azure_topic_name to be set.
    type: str
    required: false
  logging_enable:
    description:
      - Whether to turn on logging.
    type: bool
    default: true
  feedback:
    type: bool
    default: false
    description:
      - Should the source plugin wait for feedback before
        processing the next event from the Azure Event Hub
        This flag allows ansible rulebook to pass in an asyncio
        queue which is passed in the args['eda_feedback_queue']
        The source plugin should wait for the response to come
        back on this queue before it picks the next event from
        Azure Event Hub.
  feedback_timeout:
    type: int
    default: 120
    description:
      - Timeout in seconds to wait for feedback from the rule engine
        before raising an exception. Only applies when feedback is enabled.
  eda_feedback_queue:
    description:
      - Provided automatically by ansible-rulebook when the feedback parameter
        is enabled, this parameter utilizes an asyncio.Queue. It allows the
        system to wait for confirmation that an event has been safely persisted
        in the database before removing it from the event bus. Users do not need
        to provide a value for this manually.
"""

EXAMPLES = r"""
# Using connection string with queue
- azure.azcollection.azure_service_bus:
    conn_str: "{{connection_str}}"
    queue_name: "{{queue_name}}"

# Using service principal with queue
- azure.azcollection.azure_service_bus:
    azure_tenant_id: "{{tenant_id}}"
    azure_client_id: "{{client_id}}"
    azure_client_secret: "{{client_secret}}"
    azure_namespace: "myservicebus.servicebus.windows.net"
    queue_name: "my-queue"
    feedback: true

# Using service principal with topic subscription
- azure.azcollection.azure_service_bus:
    azure_tenant_id: "{{tenant_id}}"
    azure_client_id: "{{client_id}}"
    azure_client_secret: "{{client_secret}}"
    azure_namespace: "myservicebus.servicebus.windows.net"
    azure_topic_name: "my-topic"
    azure_subscription_name: "my-subscription"
"""

DEFAULT_FEEDBACK_TIMEOUT = 120

logger = logging.getLogger()

_uuid_warning = {"emitted": False}


def is_valid_uuid(value: str) -> bool:
    """Check if a string is a valid RFC 4122 UUID.

    Accepts a str but handles non-string types defensively by catching
    TypeError, so callers do not need to guard against unexpected types.
    """
    try:
        uuid.UUID(value)
    except (ValueError, AttributeError, TypeError):
        return False
    else:
        return True


def _process_service_bus_uuid(
    msg: ServiceBusReceivedMessage,
    queue_name: str,
    meta: dict[str, Any],
) -> None:
    """Assign a valid UUID to meta["uuid"].

    Uses msg.message_id if it is a valid UUID, otherwise generates a
    deterministic UUID5 from queue_name and sequence_number to ensure
    uniqueness within the configured queue. The original message_id is
    always preserved under meta["message_id"] regardless of validity;
    it is set to None when message_id is absent.
    """
    raw_id = str(msg.message_id) if msg.message_id is not None else None
    meta["message_id"] = raw_id

    if raw_id and is_valid_uuid(raw_id):
        meta["uuid"] = raw_id
    else:
        meta["uuid"] = str(
            uuid.uuid5(uuid.NAMESPACE_OID, f"{queue_name}:{msg.sequence_number}"),
        )
        if raw_id and not _uuid_warning["emitted"]:
            _uuid_warning["emitted"] = True
            logger.warning(
                "Provided message_id is not a valid UUID,"
                " using generated UUID. The original value has been"
                " stored under event.meta.message_id for tracking.",
            )


@dataclasses.dataclass(frozen=True)
class _FeedbackConfig:
    enabled: bool
    queue: asyncio.Queue[Any] | None
    timeout: int


def _create_service_bus_client(args: dict[str, Any]) -> ServiceBusClient:
    """Create Service Bus client with connection string or service principal.

    Args:
        args: Configuration arguments containing either conn_str or service principal credentials.

    Returns:
        ServiceBusClient instance.

    Raises:
        ValueError: If neither connection string nor service principal credentials are provided.

    """
    logging_enable = bool(args.get("logging_enable", True))

    # Option 1: Connection string authentication (backward compatible)
    if "conn_str" in args:
        return ServiceBusClient.from_connection_string(
            conn_str=args["conn_str"],
            logging_enable=logging_enable,
        )

    # Option 2: Service principal authentication
    tenant_id = args.get("azure_tenant_id")
    client_id = args.get("azure_client_id")
    client_secret = args.get("azure_client_secret")
    namespace = args.get("azure_namespace")

    if all([tenant_id, client_id, client_secret, namespace]):
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        )
        return ServiceBusClient(
            fully_qualified_namespace=namespace,
            credential=credential,
            logging_enable=logging_enable,
        )

    # Neither method provided
    msg = (
        "Either 'conn_str' OR ('azure_tenant_id', 'azure_client_id', "
        "'azure_client_secret', 'azure_namespace') must be provided"
    )
    raise ValueError(msg)


def _validate_receive_args(args: dict[str, Any]) -> None:
    """Validate feedback and queue/topic configuration."""
    if args.get("feedback", False) and args.get("eda_feedback_queue") is None:
        msg = (
            "feedback: true was set but no feedback queue was provided. "
            "This requires a compatible version of ansible-rulebook that "
            "supports the feedback mechanism."
        )
        raise ValueError(msg)

    queue_name = args.get("queue_name")
    azure_topic_name = args.get("azure_topic_name")
    azure_subscription_name = args.get("azure_subscription_name")

    if queue_name and (azure_topic_name or azure_subscription_name):
        msg = "Cannot specify both queue_name and azure_topic_name/azure_subscription_name"
        raise ValueError(msg)

    if not queue_name and not (azure_topic_name and azure_subscription_name):
        msg = "Either queue_name OR (azure_topic_name AND azure_subscription_name) must be provided"
        raise ValueError(msg)


def _get_receiver(
    servicebus_client: ServiceBusClient,
    args: dict[str, Any],
) -> ServiceBusReceiver:
    """Get the appropriate receiver based on queue or topic/subscription config."""
    queue_name = args.get("queue_name")
    namespace = args.get("azure_namespace", "connection-string-based")

    if queue_name:
        logger.info(
            "Starting Azure Service Bus consumer - Namespace: '%s', Queue: '%s'",
            namespace,
            queue_name,
        )
        return servicebus_client.get_queue_receiver(queue_name=queue_name)

    azure_topic_name = args.get("azure_topic_name")
    azure_subscription_name = args.get("azure_subscription_name")
    logger.info(
        "Starting Azure Service Bus consumer - Namespace: '%s', Topic: '%s', Subscription: '%s'",
        namespace,
        azure_topic_name,
        azure_subscription_name,
    )
    return servicebus_client.get_subscription_receiver(
        topic_name=azure_topic_name,
        subscription_name=azure_subscription_name,
    )


async def _process_message(
    msg: ServiceBusReceivedMessage,
    receiver: ServiceBusReceiver,
    queue: asyncio.Queue[Any],
    feedback: _FeedbackConfig,
    destination_name: str,
) -> None:
    """Process a single Service Bus message."""
    meta: dict[str, Any] = {}
    if msg.enqueued_time_utc:
        meta["produced_at"] = msg.enqueued_time_utc.isoformat()
    _process_service_bus_uuid(msg, destination_name, meta)

    body = str(msg)
    with contextlib.suppress(json.JSONDecodeError):
        body = json.loads(body)

    await queue.put({"body": body, "meta": meta})

    if feedback.enabled and feedback.queue:
        try:
            await asyncio.wait_for(
                feedback.queue.get(),
                timeout=feedback.timeout,
            )
            await receiver.complete_message(msg)
            logger.debug("Message %s completed successfully", msg.message_id)
        except asyncio.TimeoutError:
            logger.exception(
                "Timed out waiting for feedback for message %s - dead lettering",
                msg.message_id,
            )
            await receiver.dead_letter_message(
                msg,
                reason="FeedbackTimeout",
                error_description=f"No acknowledgment received within {feedback.timeout}s",
            )
            raise
    else:
        await receiver.complete_message(msg)
        logger.debug("Message %s completed (no feedback)", msg.message_id)


async def receive_events(
    queue: asyncio.Queue[Any],
    args: dict[str, Any],  # pylint: disable=W0621
) -> None:
    """Receive events from service bus asynchronously."""
    _validate_receive_args(args)

    feedback = _FeedbackConfig(
        enabled=args.get("feedback", False),
        queue=args.get("eda_feedback_queue"),
        timeout=int(args.get("feedback_timeout", DEFAULT_FEEDBACK_TIMEOUT)),
    )

    servicebus_client = _create_service_bus_client(args)

    async with servicebus_client:
        receiver = _get_receiver(servicebus_client, args)
        async with receiver:
            destination_name = args.get("queue_name") or args.get(
                "azure_topic_name", "unknown",
            )
            async for msg in receiver:
                try:
                    await _process_message(
                        msg, receiver, queue, feedback, destination_name,
                    )
                except Exception as e:
                    logger.exception("Error processing message %s", msg.message_id)
                    try:
                        await receiver.dead_letter_message(
                            msg,
                            reason="ProcessingError",
                            error_description=str(e)[:4096],
                        )
                        logger.exception(
                            "Message %s dead-lettered due to error", msg.message_id,
                        )
                    except Exception:
                        logger.exception(
                            "Failed to dead-letter message %s", msg.message_id,
                        )
                    raise


async def main(
    queue: asyncio.Queue[Any],
    args: dict[str, Any],  # pylint: disable=W0621
) -> None:
    """Receive events from service bus in a loop."""
    await receive_events(queue, args)


if __name__ == "__main__":
    # MockQueue if running directly.

    class MockQueue(asyncio.Queue[Any]):
        """A fake queue."""

        async def put(self: "MockQueue", event: dict[str, Any]) -> None:
            """Print the event."""
            print(event)  # noqa: T201

    # Example 1: Using connection string with queue
    args_conn_str = {
        "conn_str": "Endpoint=sb://foo.servicebus.windows.net/",
        "queue_name": "eda-queue",
    }

    # Example 2: Using service principal with queue
    args_service_principal_queue = {
        "azure_tenant_id": "your_tenant_id",
        "azure_client_id": "your_client_id",
        "azure_client_secret": "your_client_secret",
        "azure_namespace": "myservicebus.servicebus.windows.net",
        "queue_name": "eda-queue",
    }

    # Example 3: Using service principal with topic subscription
    args_service_principal_topic = {
        "azure_tenant_id": "your_tenant_id",
        "azure_client_id": "your_client_id",
        "azure_client_secret": "your_client_secret",
        "azure_namespace": "myservicebus.servicebus.windows.net",
        "azure_topic_name": "my-topic",
        "azure_subscription_name": "my-subscription",
    }

    # Run with connection string example
    asyncio.run(main(MockQueue(), args_conn_str))
