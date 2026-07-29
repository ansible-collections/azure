# Copyright (c) 2025 Red Hat, Inc.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Ansible-rulebook event source plugin for Azure Event Hub.

This module provides asynchronous consumers for Azure Event Hub to feed
events into Ansible EDA rulebooks.
"""

import asyncio
import json
import logging
import uuid
from typing import Any

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubConsumerClient, PartitionContext
from azure.identity.aio import ClientSecretCredential

DOCUMENTATION = r"""
---
short_description: Receive events via a Azure Event Hub
description:
  - An ansible-rulebook event source plugin for receiving events
    via Azure Event Hub
  - Each event is assigned a valid RFC 4122 UUID under meta.uuid.
  - If message_id is a valid UUID it is used. Otherwise if correlation_id is a valid UUID
    it is used. Each is validated independently so an invalid message_id does not hide
    a valid correlation_id.
  - AMQP ID values of any type (str, bytes, uuid.UUID, int) are normalised to str
    before validation.
  - If neither is a valid UUID, a deterministic UUID5 is generated from
    partition_id:sequence_number. The original value is preserved under meta.message_id.
options:
  azure_tenant_id:
    description:
      - The azure tenant id
    type: str
    required: true
  azure_client_id:
    description:
      - The azure client id
    type: str
    required: true
  azure_client_secret:
    description:
      - The azure client secret
    type: str
    required: true
  azure_namespace:
    description:
      - The azure event hub namespace which includes the host name
    type: str
    example: "test.servicebus.windows.net"
    required: true
  azure_event_hub_name:
    description:
      - The azure event hub name
    type: str
    required: true
  azure_starting_position:
    description:
      - The starting position
    type: str
    default: "-1"
  azure_consumer_group:
    description:
      - The name of the consumer group
    type: str
    default: "$Default"
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
- azure.azcollection.azure_event_hub:
    "azure_tenant_id": "your_tenant_id"
    "azure_client_id": "your_client_id"
    "azure_client_secret": "your_client_secret"
    "azure_namespace": "example.servicebus.windows.net"
    "azure_event_hub_name": "your_hub_name"
    "azure_starting_position": "-1"
"""

logger = logging.getLogger()

_uuid_warning = {"emitted": False}


def is_valid_uuid(value: str) -> bool:
    """Check if a string is a valid RFC 4122 UUID.

    Accepts a str but handles non-string types defensively by catching
    TypeError, so callers do not need to guard against unexpected types.
    """
    try:
        uuid.UUID(value)
        return True  # noqa: TRY300
    except (ValueError, AttributeError, TypeError):
        return False


def _normalize_amqp_id(value: str | bytes | uuid.UUID | int | None) -> str | None:
    """Normalize an AMQP ID value to a string suitable for UUID validation.

    AMQP message-id and correlation-id may be str, bytes, uuid.UUID, or int (ulong).
    Returns None if value is None.
    """
    if value is None:
        return None
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8")
        except UnicodeDecodeError:
            return value.hex()
    return str(value)


def _process_event_hub_uuid(
    partition_context: PartitionContext,
    event: EventData,
    meta: dict[str, Any],
) -> None:
    """Assign a valid UUID to meta["uuid"].

    Priority: message_id > correlation_id > generated UUID5.
    Each candidate is validated independently so an invalid message_id does
    not hide a valid correlation_id. Generated UUID5 uses
    partition_id:sequence_number as coordinates. The original value is
    preserved under meta["message_id"] when the fallback is used.
    """
    coordinates = f"{partition_context.partition_id}:{event.sequence_number}"
    generated_uuid = str(uuid.uuid5(uuid.NAMESPACE_OID, coordinates))

    message_id = _normalize_amqp_id(event.message_id)
    correlation_id = _normalize_amqp_id(event.correlation_id)

    if message_id and is_valid_uuid(message_id):
        meta["uuid"] = message_id
    elif correlation_id and is_valid_uuid(correlation_id):
        meta["uuid"] = correlation_id
    else:
        meta["uuid"] = generated_uuid
        raw_id = message_id or correlation_id
        if raw_id:
            meta["message_id"] = raw_id
            if not _uuid_warning["emitted"]:
                _uuid_warning["emitted"] = True
                logger.warning(
                    "Provided message_id/correlation_id is not a valid UUID,"
                    " using generated UUID. The original value has been"
                    " stored under event.meta.message_id for tracking.",
                )


REQUIRED_ARGS = [
    "azure_tenant_id",
    "azure_client_id",
    "azure_client_secret",
    "azure_namespace",
    "azure_event_hub_name",
]

DEFAULT_FEEDBACK_TIMEOUT = 120


class AzureHubConsumer:
    """Azure Hub Consumer."""

    def __init__(self, queue: asyncio.Queue[Any], args: dict[str, Any]) -> None:
        """Initialize Hub Consumer."""
        self.queue = queue
        tenant_id = args.get("azure_tenant_id")
        client_id = args.get("azure_client_id")
        client_secret = args.get("azure_client_secret")

        self.event_hub_namespace = args.get("azure_namespace")
        self.event_hub_name = args.get("azure_event_hub_name")

        self.consumer_group = args.get("azure_consumer_group", "$Default")
        self.starting_position = int(args.get("azure_starting_position", "-1"))
        self.feedback_timeout = int(args.get("feedback_timeout", DEFAULT_FEEDBACK_TIMEOUT))
        self.feedback = args.get("feedback", False)
        self.eda_feedback_queue = args.get("eda_feedback_queue")

        if self.feedback and self.eda_feedback_queue is None:
            msg = (
                "feedback: true was set but no feedback queue was provided. "
                "This requires a compatible version of ansible-rulebook that "
                "supports the feedback mechanism."
            )
            raise ValueError(msg)

        self.credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        )

    async def on_event(
        self, partition_context: PartitionContext, event: EventData,
    ) -> None:
        """Receiving event data."""
        if event:
            meta: dict[str, Any] = {}
            if event.enqueued_time:
                meta["produced_at"] = event.enqueued_time.isoformat()
            _process_event_hub_uuid(partition_context, event, meta)
            # Process message body
            try:
                value = event.body_as_str()
                logger.debug(
                    "Received event from partition %s: %s",
                    str(partition_context.partition_id),
                    value,
                )
            except UnicodeError:
                logger.exception("Unicode error while decoding message body")
                data = None
            else:
                try:
                    data = json.loads(value)
                except json.decoder.JSONDecodeError:
                    logger.info("JSON decode error, storing raw value")
                    data = value

            # Add data to the event and put it into the queue
            if data:
                await self.queue.put({"body": data, "meta": meta})

            if self.feedback and self.eda_feedback_queue:
                try:
                    await asyncio.wait_for(
                        self.eda_feedback_queue.get(),
                        timeout=self.feedback_timeout,
                    )
                    await partition_context.update_checkpoint(event)
                except asyncio.TimeoutError:
                    logger.exception("Timed out waiting for feedback")
                    raise
            else:
                await partition_context.update_checkpoint(event)

        await asyncio.sleep(0)

    async def start_receiving(self) -> None:
        """Start receiving data."""
        client = EventHubConsumerClient(
            fully_qualified_namespace=self.event_hub_namespace,
            eventhub_name=self.event_hub_name,
            consumer_group=self.consumer_group,
            credential=self.credential,
        )
        async with client:
            await client.receive(self.on_event)


# Usage
async def main(  # pylint: disable=R0914
    queue: asyncio.Queue[Any],
    args: dict[str, Any],
) -> None:
    """Entry Point."""
    for key in REQUIRED_ARGS:
        if key not in args:
            msg = f"Please provide {key} it is a required argument."
            raise ValueError(msg)

    consumer = AzureHubConsumer(queue, args)
    await consumer.start_receiving()


if __name__ == "__main__":

    class MockQueue(asyncio.Queue[Any]):
        """A fake queue."""

        async def put(self: "MockQueue", event: dict[str, Any]) -> None:
            """Print the event."""
            print(event)  # noqa: T201

    test_args = {
        "azure_tenant_id": "your_tenant_id",
        "azure_client_id": "your_client_id",
        "azure_client_secret": "your_client_secret",
        "azure_namespace": "example.servicebus.windows.net",
        "azure_event_hub_name": "your_hub_name",
        "azure_starting_position": "-1",
    }

    asyncio.run(
        main(
            MockQueue(),
            test_args,
        ),
    )
