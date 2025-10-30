import asyncio
import json
import logging
from typing import Any

from azure.eventhub.aio import EventHubConsumerClient
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


class AzureHubConsumer:
    def __init__(self, queue: asyncio.Queue[Any], args: dict[str, Any]) -> None:
        self.queue = queue
        tenant_id = args.get("azure_tenant_id")
        client_id = args.get("azure_client_id")
        client_secret = args.get("azure_client_secret")

        self.event_hub_namespace = args.get("azure_namespace")
        self.event_hub_name = args.get("azure_event_hub_name")

        self.consumer_group = args.get("azure_consumer_group", "$Default")
        self.starting_position = int(args.get("azure_starting_position", "-1"))

        self.credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        )

    async def on_event(self, partition_context, event):
        if event:
            await partition_context.update_checkpoint(event)
            meta = {}
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

        await asyncio.sleep(0)

    async def start_receiving(self):
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
    asyncio.run(main())
