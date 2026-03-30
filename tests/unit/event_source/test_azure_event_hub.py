import asyncio
from typing import Any, Dict, Optional, Type
from unittest.mock import AsyncMock, patch

import pytest

from extensions.eda.plugins.event_source.azure_event_hub import AzureHubConsumer, main


class MockEvent:
    def __init__(
        self,
        body: str,
        message_id: str | None = None,
        correlation_id: str | None = None,
        sequence_number: int = 0,
        enqueued_time: Any = None,
    ) -> None:
        self._body = body
        self.message_id = message_id
        self.correlation_id = correlation_id
        self.sequence_number = sequence_number
        self.enqueued_time = enqueued_time

    def body_as_str(self) -> str:
        return self._body


class MockPartitionContext:
    def __init__(self, partition_id: str = "0") -> None:
        self.partition_id = partition_id

    async def update_checkpoint(self, event: MockEvent) -> None:
        pass


class MockEventHubConsumerClient:
    def __init__(self, events: list[MockEvent]) -> None:
        self.events = events

    async def __aenter__(self) -> "MockEventHubConsumerClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Any,
    ) -> None:
        pass

    async def receive(self, on_event_callback) -> None:
        partition_context = MockPartitionContext()
        for event in self.events:
            await on_event_callback(partition_context, event)


@pytest.mark.asyncio
async def test_main_missing_required_args() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: Dict[str, Any] = {"azure_tenant_id": "test_tenant"}

    with pytest.raises(ValueError, match="Please provide azure_client_id"):
        await main(queue, args)


@pytest.mark.asyncio
async def test_main_with_all_required_args() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: Dict[str, Any] = {
        "azure_tenant_id": "test_tenant_id",
        "azure_client_id": "test_client_id",
        "azure_client_secret": "test_client_secret",
        "azure_namespace": "test.servicebus.windows.net",
        "azure_event_hub_name": "test_hub",
    }

    with patch(
        "extensions.eda.plugins.event_source.azure_event_hub.EventHubConsumerClient"
    ) as mock_client_class, patch(
        "extensions.eda.plugins.event_source.azure_event_hub.ClientSecretCredential"
    ) as mock_credential:

        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.receive = AsyncMock()

        await main(queue, args)

        mock_credential.assert_called_once_with(
            tenant_id="test_tenant_id",
            client_id="test_client_id",
            client_secret="test_client_secret",
        )
        mock_client_class.assert_called_once()
        mock_client.receive.assert_called_once()


@pytest.mark.asyncio
async def test_azure_hub_consumer_on_event_json() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: Dict[str, Any] = {
        "azure_tenant_id": "test_tenant_id",
        "azure_client_id": "test_client_id",
        "azure_client_secret": "test_client_secret",
        "azure_namespace": "test.servicebus.windows.net",
        "azure_event_hub_name": "test_hub",
    }

    with patch(
        "extensions.eda.plugins.event_source.azure_event_hub.ClientSecretCredential"
    ):
        consumer = AzureHubConsumer(queue, args)

        partition_context = MockPartitionContext()
        event = MockEvent('{"message": "Hello World"}')

        await consumer.on_event(partition_context, event)

        result = await queue.get()
        assert result == {
            "body": {"message": "Hello World"},
            "meta": {"event": {"uuid": "0:0"}},
        }


@pytest.mark.asyncio
async def test_azure_hub_consumer_on_event_raw_string() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: Dict[str, Any] = {
        "azure_tenant_id": "test_tenant_id",
        "azure_client_id": "test_client_id",
        "azure_client_secret": "test_client_secret",
        "azure_namespace": "test.servicebus.windows.net",
        "azure_event_hub_name": "test_hub",
    }

    with patch(
        "extensions.eda.plugins.event_source.azure_event_hub.ClientSecretCredential"
    ):
        consumer = AzureHubConsumer(queue, args)

        partition_context = MockPartitionContext()
        event = MockEvent("Hello World")

        await consumer.on_event(partition_context, event)

        result = await queue.get()
        assert result == {"body": "Hello World", "meta": {"event": {"uuid": "0:0"}}}


@pytest.mark.asyncio
async def test_azure_hub_consumer_on_event_unicode_error() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: Dict[str, Any] = {
        "azure_tenant_id": "test_tenant_id",
        "azure_client_id": "test_client_id",
        "azure_client_secret": "test_client_secret",
        "azure_namespace": "test.servicebus.windows.net",
        "azure_event_hub_name": "test_hub",
    }

    with patch(
        "extensions.eda.plugins.event_source.azure_event_hub.ClientSecretCredential"
    ):
        consumer = AzureHubConsumer(queue, args)

        partition_context = MockPartitionContext()
        event = MockEvent('{"message": "Hello World"}')

        with patch.object(
            event, "body_as_str", side_effect=UnicodeError("Unicode decode error")
        ):
            await consumer.on_event(partition_context, event)

        # Should not put anything in queue when there's a Unicode error
        assert queue.empty()


@pytest.mark.asyncio
async def test_azure_hub_consumer_on_event_no_event() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: Dict[str, Any] = {
        "azure_tenant_id": "test_tenant_id",
        "azure_client_id": "test_client_id",
        "azure_client_secret": "test_client_secret",
        "azure_namespace": "test.servicebus.windows.net",
        "azure_event_hub_name": "test_hub",
    }

    with patch(
        "extensions.eda.plugins.event_source.azure_event_hub.ClientSecretCredential"
    ):
        consumer = AzureHubConsumer(queue, args)

        partition_context = MockPartitionContext()

        await consumer.on_event(partition_context, None)

        # Should not put anything in queue when event is None
        assert queue.empty()


@pytest.mark.asyncio
async def test_azure_hub_consumer_initialization() -> None:
    args: Dict[str, Any] = {
        "azure_tenant_id": "test_tenant_id",
        "azure_client_id": "test_client_id",
        "azure_client_secret": "test_client_secret",
        "azure_namespace": "test.servicebus.windows.net",
        "azure_event_hub_name": "test_hub",
        "azure_consumer_group": "custom_group",
        "azure_starting_position": "5",
    }

    with patch(
        "extensions.eda.plugins.event_source.azure_event_hub.ClientSecretCredential"
    ) as mock_credential:
        queue: asyncio.Queue[Any] = asyncio.Queue()
        consumer = AzureHubConsumer(queue, args)

        assert consumer.event_hub_namespace == "test.servicebus.windows.net"
        assert consumer.event_hub_name == "test_hub"
        assert consumer.consumer_group == "custom_group"
        assert consumer.starting_position == 5

        mock_credential.assert_called_once_with(
            tenant_id="test_tenant_id",
            client_id="test_client_id",
            client_secret="test_client_secret",
        )


@pytest.mark.asyncio
async def test_azure_hub_consumer_defaults() -> None:
    args: Dict[str, Any] = {
        "azure_tenant_id": "test_tenant_id",
        "azure_client_id": "test_client_id",
        "azure_client_secret": "test_client_secret",
        "azure_namespace": "test.servicebus.windows.net",
        "azure_event_hub_name": "test_hub",
    }

    with patch(
        "extensions.eda.plugins.event_source.azure_event_hub.ClientSecretCredential"
    ):
        queue: asyncio.Queue[Any] = asyncio.Queue()
        consumer = AzureHubConsumer(queue, args)

        assert consumer.consumer_group == "$Default"
        assert consumer.starting_position == -1


@pytest.mark.asyncio
async def test_azure_hub_consumer_start_receiving() -> None:
    args: Dict[str, Any] = {
        "azure_tenant_id": "test_tenant_id",
        "azure_client_id": "test_client_id",
        "azure_client_secret": "test_client_secret",
        "azure_namespace": "test.servicebus.windows.net",
        "azure_event_hub_name": "test_hub",
    }

    events = [MockEvent('{"test": "data"}')]

    with patch(
        "extensions.eda.plugins.event_source.azure_event_hub.ClientSecretCredential"
    ), patch(
        "extensions.eda.plugins.event_source.azure_event_hub.EventHubConsumerClient",
        return_value=MockEventHubConsumerClient(events),
    ):

        queue: asyncio.Queue[Any] = asyncio.Queue()
        consumer = AzureHubConsumer(queue, args)

        await consumer.start_receiving()

        result = await queue.get()
        assert result == {"body": {"test": "data"}, "meta": {"event": {"uuid": "0:0"}}}


@pytest.mark.asyncio
async def test_azure_hub_consumer_feedback_enabled_without_queue() -> None:
    """Test that ValueError is raised when feedback is enabled but no queue is provided."""
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: Dict[str, Any] = {
        "azure_tenant_id": "test_tenant_id",
        "azure_client_id": "test_client_id",
        "azure_client_secret": "test_client_secret",
        "azure_namespace": "test.servicebus.windows.net",
        "azure_event_hub_name": "test_hub",
        "feedback": True,
    }

    with patch(
        "extensions.eda.plugins.event_source.azure_event_hub.ClientSecretCredential"
    ), pytest.raises(ValueError, match="feedback: true was set but no feedback queue"):
        AzureHubConsumer(queue, args)


@pytest.mark.asyncio
async def test_azure_hub_consumer_feedback_enabled_with_queue() -> None:
    """Test that consumer waits for feedback when enabled."""
    queue: asyncio.Queue[Any] = asyncio.Queue()
    feedback_queue: asyncio.Queue[Any] = asyncio.Queue()
    args: Dict[str, Any] = {
        "azure_tenant_id": "test_tenant_id",
        "azure_client_id": "test_client_id",
        "azure_client_secret": "test_client_secret",
        "azure_namespace": "test.servicebus.windows.net",
        "azure_event_hub_name": "test_hub",
        "feedback": True,
        "eda_feedback_queue": feedback_queue,
    }

    with patch(
        "extensions.eda.plugins.event_source.azure_event_hub.ClientSecretCredential"
    ):
        consumer = AzureHubConsumer(queue, args)
        partition_context = MockPartitionContext()
        event = MockEvent('{"message": "Hello World"}')

        # Put feedback in queue immediately so it doesn't block
        await feedback_queue.put("feedback_received")

        await consumer.on_event(partition_context, event)

        result = await queue.get()
        assert result["body"] == {"message": "Hello World"}
        # Verify feedback was consumed
        assert feedback_queue.empty()


@pytest.mark.asyncio
async def test_azure_hub_consumer_feedback_timeout() -> None:
    """Test that TimeoutError is raised when feedback timeout is exceeded."""
    queue: asyncio.Queue[Any] = asyncio.Queue()
    feedback_queue: asyncio.Queue[Any] = asyncio.Queue()
    args: Dict[str, Any] = {
        "azure_tenant_id": "test_tenant_id",
        "azure_client_id": "test_client_id",
        "azure_client_secret": "test_client_secret",
        "azure_namespace": "test.servicebus.windows.net",
        "azure_event_hub_name": "test_hub",
        "feedback": True,
        "eda_feedback_queue": feedback_queue,
        "feedback_timeout": 0.1,  # Short timeout for testing
    }

    with patch(
        "extensions.eda.plugins.event_source.azure_event_hub.ClientSecretCredential"
    ):
        consumer = AzureHubConsumer(queue, args)
        partition_context = MockPartitionContext()
        event = MockEvent('{"message": "Hello World"}')

        # Don't put anything in feedback queue, so it times out
        with pytest.raises(asyncio.TimeoutError):
            await consumer.on_event(partition_context, event)


@pytest.mark.asyncio
async def test_azure_hub_consumer_feedback_defaults() -> None:
    """Test that feedback defaults are set correctly."""
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: Dict[str, Any] = {
        "azure_tenant_id": "test_tenant_id",
        "azure_client_id": "test_client_id",
        "azure_client_secret": "test_client_secret",
        "azure_namespace": "test.servicebus.windows.net",
        "azure_event_hub_name": "test_hub",
    }

    with patch(
        "extensions.eda.plugins.event_source.azure_event_hub.ClientSecretCredential"
    ):
        consumer = AzureHubConsumer(queue, args)
        assert consumer.feedback is False
        assert consumer.feedback_timeout == 120
        assert consumer.eda_feedback_queue is None
