import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any, Self
from unittest.mock import AsyncMock, patch

import pytest

from extensions.eda.plugins.event_source.azure_event_hub import (
    AzureHubConsumer,
    _uuid_warning,
    main,
)

VALID_UUID_1 = "8472ff2c-6045-4418-8d4e-46f6cffc8557"
VALID_UUID_2 = "a1b2c3d4-e5f6-4789-abcd-ef0123456789"

PATCH_CREDENTIAL = (
    "extensions.eda.plugins.event_source.azure_event_hub.ClientSecretCredential"
)
PATCH_CLIENT = (
    "extensions.eda.plugins.event_source.azure_event_hub.EventHubConsumerClient"
)
PATCH_BLOB_STORE = (
    "extensions.eda.plugins.event_source.azure_event_hub.BlobCheckpointStore"
)

BASE_ARGS: dict[str, Any] = {
    "azure_tenant_id": "test_tenant_id",
    "azure_client_id": "test_client_id",
    "azure_client_secret": "test_client_secret",
    "azure_namespace": "test.servicebus.windows.net",
    "azure_event_hub_name": "test_hub",
}


class MockEvent:
    def __init__(
        self,
        body: str,
        message_id: Any = None,
        correlation_id: Any = None,
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
        self.receive_kwargs: dict[str, Any] = {}

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object,
    ) -> None:
        pass

    async def receive(self, **kwargs: Any) -> None:
        self.receive_kwargs = kwargs
        on_event_callback = kwargs["on_event"]
        partition_context = MockPartitionContext()
        for event in self.events:
            await on_event_callback(partition_context, event)


@pytest.fixture(autouse=True)
def reset_uuid_warning():
    _uuid_warning["emitted"] = False
    yield
    _uuid_warning["emitted"] = False


def _make_consumer(
    queue: asyncio.Queue, extra_args: dict[str, Any] | None = None
) -> AzureHubConsumer:
    args = {**BASE_ARGS, **(extra_args or {})}
    with patch(PATCH_CREDENTIAL):
        return AzureHubConsumer(queue, args)


# ---------------------------------------------------------------------------
# main() / required args
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_main_missing_required_args() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: dict[str, Any] = {"azure_tenant_id": "test_tenant"}

    with pytest.raises(ValueError, match="Please provide azure_client_id"):
        await main(queue, args)


@pytest.mark.asyncio
async def test_main_with_all_required_args() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()

    with patch(PATCH_CLIENT) as mock_client_class, patch(
        PATCH_CREDENTIAL
    ) as mock_credential:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.receive = AsyncMock()

        await main(queue, BASE_ARGS)

        mock_credential.assert_called_once_with(
            tenant_id="test_tenant_id",
            client_id="test_client_id",
            client_secret="test_client_secret",
        )
        mock_client_class.assert_called_once()
        mock_client.receive.assert_called_once()


# ---------------------------------------------------------------------------
# UUID assignment — string IDs
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_on_event_no_message_id_generates_uuid5() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    event = MockEvent('{"message": "Hello World"}')

    await consumer.on_event(MockPartitionContext("0"), event)

    result = await queue.get()
    expected_uuid = str(uuid.uuid5(uuid.NAMESPACE_OID, "0:0"))
    assert result["meta"]["uuid"] == expected_uuid
    assert "event" not in result["meta"]


@pytest.mark.asyncio
async def test_on_event_valid_uuid_message_id() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    event = MockEvent('{"data": "test"}', message_id=VALID_UUID_1)

    await consumer.on_event(MockPartitionContext(), event)

    result = await queue.get()
    assert result["meta"]["uuid"] == VALID_UUID_1
    assert "message_id" not in result["meta"]


@pytest.mark.asyncio
async def test_on_event_valid_uuid_correlation_id() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    event = MockEvent('{"data": "test"}', correlation_id=VALID_UUID_2)

    await consumer.on_event(MockPartitionContext(), event)

    result = await queue.get()
    assert result["meta"]["uuid"] == VALID_UUID_2
    assert "message_id" not in result["meta"]


@pytest.mark.asyncio
async def test_on_event_message_id_takes_precedence_over_correlation_id() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    event = MockEvent(
        '{"data": "test"}', message_id=VALID_UUID_1, correlation_id=VALID_UUID_2
    )

    await consumer.on_event(MockPartitionContext(), event)

    result = await queue.get()
    assert result["meta"]["uuid"] == VALID_UUID_1


@pytest.mark.asyncio
async def test_on_event_invalid_message_id_falls_through_to_valid_correlation_id() -> (
    None
):
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    event = MockEvent(
        '{"data": "test"}', message_id="not-a-valid-uuid", correlation_id=VALID_UUID_2
    )

    await consumer.on_event(MockPartitionContext(), event)

    result = await queue.get()
    assert result["meta"]["uuid"] == VALID_UUID_2
    assert "message_id" not in result["meta"]


@pytest.mark.asyncio
async def test_on_event_invalid_uuid_falls_back_to_generated() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    event = MockEvent(
        '{"data": "test"}', message_id="not-a-valid-uuid", sequence_number=42
    )

    await consumer.on_event(MockPartitionContext("1"), event)

    result = await queue.get()
    expected_uuid = str(uuid.uuid5(uuid.NAMESPACE_OID, "1:42"))
    assert result["meta"]["uuid"] == expected_uuid
    assert result["meta"]["message_id"] == "not-a-valid-uuid"


# ---------------------------------------------------------------------------
# UUID assignment — AMQP non-string types
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_on_event_bytes_message_id_valid_uuid() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    event = MockEvent('{"data": "test"}', message_id=VALID_UUID_1.encode("utf-8"))

    await consumer.on_event(MockPartitionContext(), event)

    result = await queue.get()
    assert result["meta"]["uuid"] == VALID_UUID_1


@pytest.mark.asyncio
async def test_on_event_uuid_object_message_id() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    uuid_obj = uuid.UUID(VALID_UUID_1)
    event = MockEvent('{"data": "test"}', message_id=uuid_obj)

    await consumer.on_event(MockPartitionContext(), event)

    result = await queue.get()
    assert result["meta"]["uuid"] == VALID_UUID_1


@pytest.mark.asyncio
async def test_on_event_integer_message_id_falls_back() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    event = MockEvent('{"data": "test"}', message_id=12345, sequence_number=7)

    await consumer.on_event(MockPartitionContext("0"), event)

    result = await queue.get()
    expected_uuid = str(uuid.uuid5(uuid.NAMESPACE_OID, "0:7"))
    assert result["meta"]["uuid"] == expected_uuid
    assert result["meta"]["message_id"] == "12345"


@pytest.mark.asyncio
async def test_on_event_non_utf8_bytes_message_id_falls_back() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    raw_bytes = b"\xff\xfe"
    event = MockEvent('{"data": "test"}', message_id=raw_bytes, sequence_number=3)

    await consumer.on_event(MockPartitionContext("0"), event)

    result = await queue.get()
    expected_uuid = str(uuid.uuid5(uuid.NAMESPACE_OID, "0:3"))
    assert result["meta"]["uuid"] == expected_uuid
    assert result["meta"]["message_id"] == raw_bytes.hex()


# ---------------------------------------------------------------------------
# meta structure
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_on_event_produced_at_flat_on_meta() -> None:
    ts = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    event = MockEvent('{"x": 1}', message_id=VALID_UUID_1, enqueued_time=ts)

    await consumer.on_event(MockPartitionContext(), event)

    result = await queue.get()
    assert result["meta"]["produced_at"] == ts.isoformat()
    assert "event" not in result["meta"]


@pytest.mark.asyncio
async def test_on_event_raw_string_body() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    event = MockEvent("Hello World")

    await consumer.on_event(MockPartitionContext(), event)

    result = await queue.get()
    assert result["body"] == "Hello World"
    assert "uuid" in result["meta"]
    assert "event" not in result["meta"]


@pytest.mark.asyncio
async def test_on_event_unicode_error_does_not_enqueue() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    event = MockEvent('{"message": "Hello World"}')

    with patch.object(event, "body_as_str", side_effect=UnicodeError("error")):
        await consumer.on_event(MockPartitionContext(), event)

    assert queue.empty()


@pytest.mark.asyncio
async def test_on_event_none_event_does_not_enqueue() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)

    await consumer.on_event(MockPartitionContext(), None)

    assert queue.empty()


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_azure_hub_consumer_initialization() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args = {
        **BASE_ARGS,
        "azure_consumer_group": "custom_group",
        "azure_starting_position": "5",
    }

    with patch(PATCH_CREDENTIAL) as mock_credential:
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
    queue: asyncio.Queue[Any] = asyncio.Queue()

    with patch(PATCH_CREDENTIAL):
        consumer = AzureHubConsumer(queue, BASE_ARGS)

        assert consumer.consumer_group == "$Default"
        assert consumer.starting_position == "@latest"


# ---------------------------------------------------------------------------
# start_receiving / end-to-end
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_azure_hub_consumer_start_receiving() -> None:
    events = [MockEvent('{"test": "data"}')]
    queue: asyncio.Queue[Any] = asyncio.Queue()

    with patch(PATCH_CREDENTIAL), patch(
        PATCH_CLIENT, return_value=MockEventHubConsumerClient(events)
    ):
        consumer = AzureHubConsumer(queue, BASE_ARGS)
        await consumer.start_receiving()

    result = await queue.get()
    expected_uuid = str(uuid.uuid5(uuid.NAMESPACE_OID, "0:0"))
    assert result["body"] == {"test": "data"}
    assert result["meta"]["uuid"] == expected_uuid
    assert "event" not in result["meta"]


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_azure_hub_consumer_feedback_enabled_without_queue() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args = {**BASE_ARGS, "feedback": True}

    with patch(PATCH_CREDENTIAL), pytest.raises(
        ValueError, match="feedback: true was set but no feedback queue"
    ):
        AzureHubConsumer(queue, args)


@pytest.mark.asyncio
async def test_azure_hub_consumer_feedback_enabled_with_queue() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    feedback_queue: asyncio.Queue[Any] = asyncio.Queue()
    args = {**BASE_ARGS, "feedback": True, "eda_feedback_queue": feedback_queue}

    with patch(PATCH_CREDENTIAL):
        consumer = AzureHubConsumer(queue, args)
        event = MockEvent('{"message": "Hello World"}', message_id=VALID_UUID_1)

        await feedback_queue.put("feedback_received")
        await consumer.on_event(MockPartitionContext(), event)

        result = await queue.get()
        assert result["body"] == {"message": "Hello World"}
        assert feedback_queue.empty()


@pytest.mark.asyncio
async def test_azure_hub_consumer_feedback_timeout() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    feedback_queue: asyncio.Queue[Any] = asyncio.Queue()
    args = {
        **BASE_ARGS,
        "feedback": True,
        "eda_feedback_queue": feedback_queue,
        "feedback_timeout": 0.1,
    }

    with patch(PATCH_CREDENTIAL):
        consumer = AzureHubConsumer(queue, args)
        event = MockEvent('{"message": "Hello World"}', message_id=VALID_UUID_1)

        with pytest.raises(asyncio.TimeoutError):
            await consumer.on_event(MockPartitionContext(), event)


@pytest.mark.asyncio
async def test_azure_hub_consumer_feedback_defaults() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()

    with patch(PATCH_CREDENTIAL):
        consumer = AzureHubConsumer(queue, BASE_ARGS)
        assert consumer.feedback is False
        assert consumer.feedback_timeout == 120
        assert consumer.eda_feedback_queue is None


# ---------------------------------------------------------------------------
# Checkpoint store
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_azure_hub_consumer_checkpoint_store_validation() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args = {**BASE_ARGS, "azure_storage_account_name": "mystorageaccount"}

    with patch(PATCH_CREDENTIAL), pytest.raises(
        ValueError, match="azure_checkpoint_container_name is required"
    ):
        AzureHubConsumer(queue, args)


@pytest.mark.asyncio
async def test_azure_hub_consumer_checkpoint_store_init() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(
        queue,
        {
            "azure_storage_account_name": "mystorageaccount",
            "azure_checkpoint_container_name": "checkpoints",
        },
    )
    assert consumer.storage_account_name == "mystorageaccount"
    assert consumer.checkpoint_container_name == "checkpoints"


@pytest.mark.asyncio
async def test_azure_hub_consumer_max_wait_time_default() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    assert consumer.max_wait_time == 60


@pytest.mark.asyncio
async def test_azure_hub_consumer_max_wait_time_custom() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue, {"azure_max_wait_time": 30})
    assert consumer.max_wait_time == 30


@pytest.mark.asyncio
async def test_azure_hub_consumer_starting_position_numeric_string() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue, {"azure_starting_position": "-1"})
    assert consumer.starting_position == -1
    assert isinstance(consumer.starting_position, int)


@pytest.mark.asyncio
async def test_azure_hub_consumer_starting_position_string_preserved() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue, {"azure_starting_position": "@latest"})
    assert consumer.starting_position == "@latest"
    assert isinstance(consumer.starting_position, str)


@pytest.mark.asyncio
async def test_start_receiving_without_checkpoint_store() -> None:
    mock_client = MockEventHubConsumerClient([])

    with patch(PATCH_CREDENTIAL), patch(PATCH_CLIENT, return_value=mock_client):
        queue: asyncio.Queue[Any] = asyncio.Queue()
        consumer = _make_consumer(queue, {"azure_starting_position": "@latest"})
        await consumer.start_receiving()

        assert mock_client.receive_kwargs["starting_position"] == "@latest"
        assert mock_client.receive_kwargs["max_wait_time"] == 60


@pytest.mark.asyncio
async def test_start_receiving_with_checkpoint_store() -> None:
    mock_client = MockEventHubConsumerClient([])

    with patch(PATCH_CREDENTIAL), patch(
        PATCH_CLIENT,
        return_value=mock_client,
    ) as mock_client_class, patch(PATCH_BLOB_STORE) as mock_blob_store:
        mock_blob_store.return_value = mock_blob_store

        queue: asyncio.Queue[Any] = asyncio.Queue()
        consumer = _make_consumer(
            queue,
            {
                "azure_storage_account_name": "mystorageaccount",
                "azure_checkpoint_container_name": "checkpoints",
            },
        )

        await consumer.start_receiving()

        assert "starting_position" not in mock_client.receive_kwargs
        assert mock_client.receive_kwargs["max_wait_time"] == 60
        mock_blob_store.assert_called_once_with(
            blob_account_url="https://mystorageaccount.blob.core.windows.net",
            container_name="checkpoints",
            credential=consumer.credential,
        )
        mock_client_class.assert_called_once_with(
            fully_qualified_namespace="test.servicebus.windows.net",
            eventhub_name="test_hub",
            consumer_group="$Default",
            credential=consumer.credential,
            checkpoint_store=mock_blob_store,
        )


@pytest.mark.asyncio
async def test_start_receiving_no_storage_defaults() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    consumer = _make_consumer(queue)
    assert consumer.storage_account_name is None
    assert consumer.checkpoint_container_name is None
