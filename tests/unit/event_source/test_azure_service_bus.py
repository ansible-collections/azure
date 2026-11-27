import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any, Self
from unittest.mock import patch

import pytest

from extensions.eda.plugins.event_source.azure_service_bus import (
    _create_service_bus_client,
    _uuid_warning,
    receive_events,
)

VALID_UUID_1 = "8472ff2c-6045-4418-8d4e-46f6cffc8557"
VALID_UUID_2 = "a1b2c3d4-e5f6-4789-abcd-ef0123456789"
QUEUE_NAME = "queue"

PATCH_CREATE_CLIENT = (
    "extensions.eda.plugins.event_source.azure_service_bus._create_service_bus_client"
)
PATCH_CONN_STR = (
    "extensions.eda.plugins.event_source.azure_service_bus"
    ".ServiceBusClient.from_connection_string"
)


class MockMsg:
    def __init__(
        self,
        message_id: Any,
        body: str,
        enqueued_time_utc: Any = None,
        sequence_number: int = 0,
    ) -> None:
        self.message_id = message_id
        self._body = body
        self.enqueued_time_utc = enqueued_time_utc
        self.sequence_number = sequence_number

    def __str__(self) -> str:
        return self._body


class AsyncMsgIter:
    def __init__(self, msgs: list[MockMsg]) -> None:
        self._msgs = msgs
        self._idx = 0

    def __aiter__(self) -> "AsyncMsgIter":
        return self

    async def __anext__(self) -> MockMsg:
        if self._idx < len(self._msgs):
            msg = self._msgs[self._idx]
            self._idx += 1
            return msg
        raise StopAsyncIteration


class MockReceiver:
    def __init__(self, msgs: list[MockMsg]) -> None:
        self._msgs = msgs

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object,
    ) -> None:
        pass

    def __aiter__(self) -> AsyncMsgIter:
        return AsyncMsgIter(self._msgs)

    async def complete_message(self, msg: MockMsg) -> None:
        pass

    async def dead_letter_message(self, msg: MockMsg, **kwargs: Any) -> None:
        pass


class MockServiceBusClient:
    def __init__(self, msgs: list[MockMsg]) -> None:
        self._msgs = msgs

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object,
    ) -> None:
        pass

    def get_queue_receiver(self, queue_name: str | None = None) -> MockReceiver:
        return MockReceiver(self._msgs)

    def get_subscription_receiver(
        self,
        topic_name: str,
        subscription_name: str,
    ) -> MockReceiver:
        self.received_topic = topic_name
        self.received_subscription = subscription_name
        return MockReceiver(self._msgs)


@pytest.fixture(autouse=True)
def reset_uuid_warning():
    _uuid_warning["emitted"] = False
    yield
    _uuid_warning["emitted"] = False


async def _run(
    msgs: list[MockMsg], extra_args: dict[str, Any] | None = None
) -> asyncio.Queue:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: dict[str, Any] = {"conn_str": "fake", "queue_name": QUEUE_NAME}
    if extra_args:
        args.update(extra_args)
    with patch(PATCH_CREATE_CLIENT, return_value=MockServiceBusClient(msgs)):
        await receive_events(queue, args)
    return queue


def _expected_fallback_uuid(sequence_number: int = 0) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_OID, f"{QUEUE_NAME}:{sequence_number}"))


# ---------------------------------------------------------------------------
# UUID assignment
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_receive_events_valid_uuid_message_id() -> None:
    msg = MockMsg(VALID_UUID_1, '{"data": "test"}')

    queue = await _run([msg])

    result = await queue.get()
    assert result["meta"]["uuid"] == VALID_UUID_1
    assert result["meta"]["message_id"] == VALID_UUID_1


@pytest.mark.asyncio
async def test_receive_events_non_uuid_message_id_falls_back() -> None:
    msg1 = MockMsg(1, "Hello World", sequence_number=0)
    msg2 = MockMsg(2, '{"Say": "Hello World"}', sequence_number=1)

    queue = await _run([msg1, msg2])

    result1 = await queue.get()
    result2 = await queue.get()

    assert result1 == {
        "body": "Hello World",
        "meta": {"uuid": _expected_fallback_uuid(0), "message_id": "1"},
    }
    assert result2 == {
        "body": {"Say": "Hello World"},
        "meta": {"uuid": _expected_fallback_uuid(1), "message_id": "2"},
    }


@pytest.mark.asyncio
async def test_receive_events_invalid_uuid_falls_back() -> None:
    msg = MockMsg("not-a-valid-uuid", '{"data": "test"}', sequence_number=42)

    queue = await _run([msg])

    result = await queue.get()
    assert result["meta"]["uuid"] == _expected_fallback_uuid(42)
    assert result["meta"]["message_id"] == "not-a-valid-uuid"


@pytest.mark.asyncio
async def test_receive_events_message_id_always_preserved() -> None:
    msg_valid = MockMsg(VALID_UUID_1, '{"a": 1}')
    msg_invalid = MockMsg("not-a-uuid", '{"b": 2}')

    queue = await _run([msg_valid, msg_invalid])

    r_valid = await queue.get()
    r_invalid = await queue.get()

    assert r_valid["meta"]["message_id"] == VALID_UUID_1
    assert r_invalid["meta"]["message_id"] == "not-a-uuid"


@pytest.mark.asyncio
async def test_receive_events_uuid5_seed_includes_queue_name() -> None:
    msg = MockMsg("not-a-uuid", '{"data": "test"}', sequence_number=0)

    queue_a: asyncio.Queue[Any] = asyncio.Queue()
    queue_b: asyncio.Queue[Any] = asyncio.Queue()

    with patch(PATCH_CREATE_CLIENT, return_value=MockServiceBusClient([msg])):
        await receive_events(queue_a, {"conn_str": "fake", "queue_name": "queue-a"})
    with patch(PATCH_CREATE_CLIENT, return_value=MockServiceBusClient([msg])):
        await receive_events(queue_b, {"conn_str": "fake", "queue_name": "queue-b"})

    result_a = await queue_a.get()
    result_b = await queue_b.get()

    assert result_a["meta"]["uuid"] != result_b["meta"]["uuid"]


# ---------------------------------------------------------------------------
# meta structure
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_receive_events_produced_at() -> None:
    ts = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    msg = MockMsg(VALID_UUID_2, '{"x": 1}', enqueued_time_utc=ts)

    queue = await _run([msg])

    result = await queue.get()
    assert result["meta"]["produced_at"] == ts.isoformat()
    assert "event" not in result["meta"]


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_receive_events_feedback_enabled_without_queue() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: dict[str, Any] = {
        "conn_str": "fake",
        "queue_name": QUEUE_NAME,
        "feedback": True,
    }

    with pytest.raises(
        ValueError, match="feedback: true was set but no feedback queue"
    ):
        await receive_events(queue, args)


@pytest.mark.asyncio
async def test_receive_events_feedback_enabled_with_queue() -> None:
    msg = MockMsg(VALID_UUID_1, '{"message": "Test"}')
    feedback_queue: asyncio.Queue[Any] = asyncio.Queue()
    await feedback_queue.put("feedback_received")

    queue = await _run([msg], {"feedback": True, "eda_feedback_queue": feedback_queue})

    result = await queue.get()
    assert result["body"] == {"message": "Test"}
    assert feedback_queue.empty()


@pytest.mark.asyncio
async def test_receive_events_feedback_timeout() -> None:
    msg = MockMsg(VALID_UUID_1, '{"message": "Test"}')

    with pytest.raises(asyncio.TimeoutError):
        feedback_queue: asyncio.Queue[Any] = asyncio.Queue()
        await _run(
            [msg],
            {
                "feedback": True,
                "eda_feedback_queue": feedback_queue,
                "feedback_timeout": 0.1,
            },
        )


# ---------------------------------------------------------------------------
# _create_service_bus_client
# ---------------------------------------------------------------------------


def test_create_client_with_connection_string() -> None:
    args: dict[str, Any] = {"conn_str": "Endpoint=sb://fake.servicebus.windows.net/"}
    with patch(PATCH_CONN_STR) as mock_from_conn:
        mock_from_conn.return_value = "mock_client"
        result = _create_service_bus_client(args)
        mock_from_conn.assert_called_once_with(
            conn_str="Endpoint=sb://fake.servicebus.windows.net/",
            logging_enable=True,
        )
        assert result == "mock_client"


def test_create_client_with_service_principal() -> None:
    args: dict[str, Any] = {
        "azure_tenant_id": "tenant",
        "azure_client_id": "client",
        "azure_client_secret": "secret",
        "azure_namespace": "mybus.servicebus.windows.net",
    }
    with patch(
        "extensions.eda.plugins.event_source.azure_service_bus.ClientSecretCredential"
    ) as mock_cred, patch(
        "extensions.eda.plugins.event_source.azure_service_bus.ServiceBusClient"
    ) as mock_client_class:
        mock_cred.return_value = "mock_credential"
        mock_client_class.return_value = "mock_client"

        result = _create_service_bus_client(args)

        mock_cred.assert_called_once_with(
            tenant_id="tenant",
            client_id="client",
            client_secret="secret",
        )
        mock_client_class.assert_called_once_with(
            fully_qualified_namespace="mybus.servicebus.windows.net",
            credential="mock_credential",
            logging_enable=True,
        )
        assert result == "mock_client"


def test_create_client_no_credentials() -> None:
    with pytest.raises(ValueError, match="Either 'conn_str' OR"):
        _create_service_bus_client({})


def test_create_client_partial_service_principal() -> None:
    args: dict[str, Any] = {
        "azure_tenant_id": "tenant",
        "azure_client_id": "client",
    }
    with pytest.raises(ValueError, match="Either 'conn_str' OR"):
        _create_service_bus_client(args)


def test_create_client_logging_disable() -> None:
    args: dict[str, Any] = {"conn_str": "fake", "logging_enable": False}
    with patch(PATCH_CONN_STR) as mock_from_conn:
        _create_service_bus_client(args)
        mock_from_conn.assert_called_once_with(conn_str="fake", logging_enable=False)


# ---------------------------------------------------------------------------
# Queue vs topic/subscription validation
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_receive_events_both_queue_and_topic() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: dict[str, Any] = {
        "conn_str": "fake",
        "queue_name": "my-queue",
        "azure_topic_name": "my-topic",
        "azure_subscription_name": "my-sub",
    }

    with pytest.raises(
        ValueError, match="Cannot specify both queue_name and azure_topic_name"
    ):
        await receive_events(queue, args)


@pytest.mark.asyncio
async def test_receive_events_neither_queue_nor_topic() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: dict[str, Any] = {"conn_str": "fake"}

    with pytest.raises(ValueError, match="Either queue_name OR"):
        await receive_events(queue, args)


@pytest.mark.asyncio
async def test_receive_events_topic_without_subscription() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: dict[str, Any] = {
        "conn_str": "fake",
        "azure_topic_name": "my-topic",
    }

    with pytest.raises(ValueError, match="Either queue_name OR"):
        await receive_events(queue, args)


# ---------------------------------------------------------------------------
# Topic/subscription receiver
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_receive_events_with_topic_subscription() -> None:
    msg1 = MockMsg(VALID_UUID_1, '{"key": "value"}')
    mock_sb_client = MockServiceBusClient([msg1])

    with patch(PATCH_CREATE_CLIENT, return_value=mock_sb_client):
        queue: asyncio.Queue[Any] = asyncio.Queue()
        args: dict[str, Any] = {
            "conn_str": "fake",
            "azure_topic_name": "my-topic",
            "azure_subscription_name": "my-sub",
        }

        await receive_events(queue, args)

        result = await queue.get()
        assert result["body"] == {"key": "value"}
        assert mock_sb_client.received_topic == "my-topic"
        assert mock_sb_client.received_subscription == "my-sub"


# ---------------------------------------------------------------------------
# Service principal with receive_events
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_receive_events_with_service_principal() -> None:
    msg1 = MockMsg(VALID_UUID_1, '{"sp": "test"}')
    mock_sb_client = MockServiceBusClient([msg1])

    with patch(PATCH_CREATE_CLIENT, return_value=mock_sb_client) as mock_create:
        queue: asyncio.Queue[Any] = asyncio.Queue()
        args: dict[str, Any] = {
            "azure_tenant_id": "tenant",
            "azure_client_id": "client",
            "azure_client_secret": "secret",
            "azure_namespace": "mybus.servicebus.windows.net",
            "queue_name": "my-queue",
        }

        await receive_events(queue, args)

        mock_create.assert_called_once_with(args)
        result = await queue.get()
        assert result["body"] == {"sp": "test"}


# ---------------------------------------------------------------------------
# Dead-letter on feedback timeout
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_receive_events_dead_letter_on_feedback_timeout() -> None:
    msg1 = MockMsg(VALID_UUID_1, '{"msg": "test"}')
    dead_lettered: list[MockMsg] = []

    class DLQMockReceiver(MockReceiver):
        async def dead_letter_message(self, msg: MockMsg, **kwargs: Any) -> None:
            dead_lettered.append(msg)

    class DLQMockServiceBusClient(MockServiceBusClient):
        def get_queue_receiver(self, queue_name: str | None = None) -> DLQMockReceiver:
            return DLQMockReceiver(self._msgs)

    with patch(PATCH_CREATE_CLIENT, return_value=DLQMockServiceBusClient([msg1])):
        queue: asyncio.Queue[Any] = asyncio.Queue()
        feedback_queue: asyncio.Queue[Any] = asyncio.Queue()
        args: dict[str, Any] = {
            "conn_str": "fake",
            "queue_name": "queue",
            "feedback": True,
            "eda_feedback_queue": feedback_queue,
            "feedback_timeout": 0.1,
        }

        with pytest.raises(asyncio.TimeoutError):
            await receive_events(queue, args)

        assert len(dead_lettered) >= 1
        assert all(m.message_id == VALID_UUID_1 for m in dead_lettered)
