"""Ansible-rulebook event source plugin for Azure Service Bus.

This module provides asynchronous consumers for Azure Service Bus to feed
events into Ansible EDA rulebooks.
"""

import asyncio
import contextlib
import json
import logging
from typing import Any

from azure.servicebus.aio import ServiceBusClient

DOCUMENTATION = r"""
---
short_description: Receive events from an Azure service bus.
description:
  - An ansible-rulebook event source module for receiving events from an Azure service bus.
  - In order to get the service bus and the connection string, refer to
    https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-python-how-to-use-queues?tabs=passwordless
options:
  conn_str:
    description:
      - The connection string to connect to the Azure service bus.
    type: str
    required: true
  queue_name:
    description:
      - The name of the queue to pull messages from.
    type: str
    required: true
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
- azure.azcollection.azure_service_bus:
    conn_str: "{{connection_str}}"
    queue_name: "{{queue_name}}"
"""

DEFAULT_FEEDBACK_TIMEOUT = 120

logger = logging.getLogger()


async def receive_events(
    queue: asyncio.Queue[Any],
    args: dict[str, Any],  # pylint: disable=W0621
) -> None:
    """Receive events from service bus asynchronously."""
    feedback_enabled = args.get("feedback", False)
    eda_feedback_queue = args.get("eda_feedback_queue")
    feedback_timeout = int(args.get("feedback_timeout", DEFAULT_FEEDBACK_TIMEOUT))

    if feedback_enabled and eda_feedback_queue is None:
        msg = (
            "feedback: true was set but no feedback queue was provided. "
            "This requires a compatible version of ansible-rulebook that "
            "supports the feedback mechanism."
        )
        raise ValueError(msg)
    servicebus_client = ServiceBusClient.from_connection_string(
        conn_str=args["conn_str"],
        logging_enable=bool(args.get("logging_enable", True)),
    )

    async with servicebus_client:
        receiver = servicebus_client.get_queue_receiver(queue_name=args["queue_name"])
        async with receiver:
            async for msg in receiver:
                meta = {"message_id": msg.message_id, "event": {}}
                meta["event"]["uuid"] = msg.message_id
                if msg.enqueued_time_utc:
                    meta["event"]["produced_at"] = msg.enqueued_time_utc.isoformat()

                body = str(msg)
                with contextlib.suppress(json.JSONDecodeError):
                    body = json.loads(body)

                await queue.put({"body": body, "meta": meta})

                if feedback_enabled and eda_feedback_queue:
                    try:
                        await asyncio.wait_for(
                            eda_feedback_queue.get(),
                            timeout=feedback_timeout,
                        )
                        await receiver.complete_message(msg)
                    except asyncio.TimeoutError:
                        logger.exception("Timed out waiting for feedback")
                        raise
                else:
                    await receiver.complete_message(msg)


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

    args = {
        "conn_str": "Endpoint=sb://foo.servicebus.windows.net/",
        "queue_name": "eda-queue",
    }
    asyncio.run(main(MockQueue(), args))
