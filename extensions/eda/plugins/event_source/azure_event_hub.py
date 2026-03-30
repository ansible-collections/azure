"""Ansible-rulebook event source plugin for Azure Event Hub.

This module provides asynchronous consumers for Azure Event Hub to feed
events into Ansible EDA rulebooks.
"""

import asyncio
import json
import logging
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
            meta = {}
            msg_id = (
                event.message_id
                or event.correlation_id
                or f"{partition_context.partition_id}:{event.sequence_number}"
            )

            meta["event"] = {"uuid": msg_id}
            if event.enqueued_time:
                meta["event"]["produced_at"] = event.enqueued_time.isoformat()
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
