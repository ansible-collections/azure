import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Type
from unittest.mock import patch

import pytest

from extensions.eda.plugins.event_source.azure_service_bus import (
    _uuid_warning,
    receive_events,
)

VALID_UUID_1 = "8472ff2c-6045-4418-8d4e-46f6cffc8557"
VALID_UUID_2 = "a1b2c3d4-e5f6-4789-abcd-ef0123456789"
QUEUE_NAME = "queue"

PATCH_TARGET = (
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

    async def __aenter__(self) -> "MockReceiver":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Any,
    ) -> None:
        pass

    def __aiter__(self) -> AsyncMsgIter:
        return AsyncMsgIter(self._msgs)

    async def complete_message(self, msg: MockMsg) -> None:
        pass


class MockServiceBusClient:
    def __init__(self, msgs: list[MockMsg]) -> None:
        self._msgs = msgs

    async def __aenter__(self) -> "MockServiceBusClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Any,
    ) -> None:
        pass

    def get_queue_receiver(self, queue_name: Optional[str] = None) -> MockReceiver:
        return MockReceiver(self._msgs)


@pytest.fixture(autouse=True)
def reset_uuid_warning():
    _uuid_warning["emitted"] = False
    yield
    _uuid_warning["emitted"] = False


async def _run(msgs: list[MockMsg], extra_args: Dict[str, Any] | None = None) -> asyncio.Queue:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: Dict[str, Any] = {"conn_str": "fake", "queue_name": QUEUE_NAME}
    if extra_args:
        args.update(extra_args)
    with patch(PATCH_TARGET, return_value=MockServiceBusClient(msgs)):
        await receive_events(queue, args)
    return queue


def _expected_fallback_uuid(sequence_number: int = 0) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_OID, f"{QUEUE_NAME}:{sequence_number}"))


# ---------------------------------------------------------------------------
# UUID assignment
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_receive_events_valid_uuid_message_id() -> None:
    """Valid UUID message_id is used directly as meta.uuid."""
    msg = MockMsg(VALID_UUID_1, '{"data": "test"}')

    queue = await _run([msg])

    result = await queue.get()
    assert result["meta"]["uuid"] == VALID_UUID_1
    assert result["meta"]["message_id"] == VALID_UUID_1


@pytest.mark.asyncio
async def test_receive_events_non_uuid_message_id_falls_back() -> None:
    """Non-UUID message_ids fall back to UUID5 seeded on queue_name:sequence_number."""
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
    """Invalid UUID message_id falls back to UUID5 of queue_name:sequence_number; original preserved."""
    msg = MockMsg("not-a-valid-uuid", '{"data": "test"}', sequence_number=42)

    queue = await _run([msg])

    result = await queue.get()
    assert result["meta"]["uuid"] == _expected_fallback_uuid(42)
    assert result["meta"]["message_id"] == "not-a-valid-uuid"


@pytest.mark.asyncio
async def test_receive_events_message_id_always_preserved() -> None:
    """meta.message_id is present regardless of whether the UUID was valid."""
    msg_valid = MockMsg(VALID_UUID_1, '{"a": 1}')
    msg_invalid = MockMsg("not-a-uuid", '{"b": 2}')

    queue = await _run([msg_valid, msg_invalid])

    r_valid = await queue.get()
    r_invalid = await queue.get()

    assert r_valid["meta"]["message_id"] == VALID_UUID_1
    assert r_invalid["meta"]["message_id"] == "not-a-uuid"


@pytest.mark.asyncio
async def test_receive_events_uuid5_seed_includes_queue_name() -> None:
    """UUID5 fallback seed includes queue_name, so the same sequence_number on different
    queues produces distinct UUIDs."""
    msg = MockMsg("not-a-uuid", '{"data": "test"}', sequence_number=0)

    queue_a: asyncio.Queue[Any] = asyncio.Queue()
    queue_b: asyncio.Queue[Any] = asyncio.Queue()

    with patch(PATCH_TARGET, return_value=MockServiceBusClient([msg])):
        await receive_events(queue_a, {"conn_str": "fake", "queue_name": "queue-a"})
    with patch(PATCH_TARGET, return_value=MockServiceBusClient([msg])):
        await receive_events(queue_b, {"conn_str": "fake", "queue_name": "queue-b"})

    result_a = await queue_a.get()
    result_b = await queue_b.get()

    assert result_a["meta"]["uuid"] != result_b["meta"]["uuid"]


# ---------------------------------------------------------------------------
# meta structure
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_receive_events_produced_at() -> None:
    """enqueued_time_utc is surfaced as meta.produced_at (flat on meta)."""
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
    """ValueError is raised when feedback is enabled but no queue is provided."""
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: Dict[str, Any] = {
        "conn_str": "fake",
        "queue_name": QUEUE_NAME,
        "feedback": True,
    }

    with pytest.raises(ValueError, match="feedback: true was set but no feedback queue"):
        await receive_events(queue, args)


@pytest.mark.asyncio
async def test_receive_events_feedback_enabled_with_queue() -> None:
    """Consumer waits for feedback when enabled."""
    msg = MockMsg(VALID_UUID_1, '{"message": "Test"}')
    feedback_queue: asyncio.Queue[Any] = asyncio.Queue()
    await feedback_queue.put("feedback_received")

    queue = await _run([msg], {"feedback": True, "eda_feedback_queue": feedback_queue})

    result = await queue.get()
    assert result["body"] == {"message": "Test"}
    assert feedback_queue.empty()


@pytest.mark.asyncio
async def test_receive_events_feedback_timeout() -> None:
    """TimeoutError is raised when feedback timeout is exceeded."""
    msg = MockMsg(VALID_UUID_1, '{"message": "Test"}')

    with pytest.raises(asyncio.TimeoutError):
        feedback_queue: asyncio.Queue[Any] = asyncio.Queue()
        await _run(
            [msg],
            {"feedback": True, "eda_feedback_queue": feedback_queue, "feedback_timeout": 0.1},
        )
