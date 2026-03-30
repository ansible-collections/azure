import asyncio
from typing import Any, Dict, Optional, Type
from unittest.mock import patch

import pytest

from extensions.eda.plugins.event_source.azure_service_bus import receive_events


class MockMsg:
    def __init__(
        self, message_id: int, body: str, enqueued_time_utc: Any = None
    ) -> None:
        self.message_id = message_id
        self._body = body
        self.enqueued_time_utc = enqueued_time_utc

    def __str__(self) -> str:
        return self._body


@pytest.mark.asyncio
async def test_receive_events() -> None:
    msg1 = MockMsg(1, "Hello World")
    msg2 = MockMsg(2, '{"Say": "Hello World"}')

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
            return AsyncMsgIter([msg1, msg2])

        async def complete_message(self, msg: MockMsg) -> None:
            pass

    class MockServiceBusClient:
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
            return MockReceiver()

    with patch(
        "extensions.eda.plugins.event_source.azure_service_bus.ServiceBusClient.from_connection_string",
        return_value=MockServiceBusClient(),
    ):
        queue: asyncio.Queue[Any] = asyncio.Queue()
        args: Dict[str, Any] = {"conn_str": "fake", "queue_name": "queue"}
        await receive_events(queue, args)

        result1 = await queue.get()
        result2 = await queue.get()
        assert result1 == {
            "body": "Hello World",
            "meta": {"message_id": 1, "event": {"uuid": 1}},
        }
        assert result2 == {
            "body": {"Say": "Hello World"},
            "meta": {"message_id": 2, "event": {"uuid": 2}},
        }


@pytest.mark.asyncio
async def test_receive_events_feedback_enabled_without_queue() -> None:
    """Test that ValueError is raised when feedback is enabled but no queue is provided."""
    queue: asyncio.Queue[Any] = asyncio.Queue()
    args: Dict[str, Any] = {
        "conn_str": "fake",
        "queue_name": "queue",
        "feedback": True,
    }

    with pytest.raises(
        ValueError, match="feedback: true was set but no feedback queue"
    ):
        await receive_events(queue, args)


@pytest.mark.asyncio
async def test_receive_events_feedback_enabled_with_queue() -> None:
    """Test that consumer waits for feedback when enabled."""
    msg1 = MockMsg(1, '{"message": "Test"}')

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
            return AsyncMsgIter([msg1])

        async def complete_message(self, msg: MockMsg) -> None:
            pass

    class MockServiceBusClient:
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
            return MockReceiver()

    with patch(
        "extensions.eda.plugins.event_source.azure_service_bus.ServiceBusClient.from_connection_string",
        return_value=MockServiceBusClient(),
    ):
        queue: asyncio.Queue[Any] = asyncio.Queue()
        feedback_queue: asyncio.Queue[Any] = asyncio.Queue()
        args: Dict[str, Any] = {
            "conn_str": "fake",
            "queue_name": "queue",
            "feedback": True,
            "eda_feedback_queue": feedback_queue,
        }

        # Put feedback in queue immediately so it doesn't block
        await feedback_queue.put("feedback_received")

        await receive_events(queue, args)

        result = await queue.get()
        assert result["body"] == {"message": "Test"}
        # Verify feedback was consumed
        assert feedback_queue.empty()


@pytest.mark.asyncio
async def test_receive_events_feedback_timeout() -> None:
    """Test that TimeoutError is raised when feedback timeout is exceeded."""
    msg1 = MockMsg(1, '{"message": "Test"}')

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
            return AsyncMsgIter([msg1])

        async def complete_message(self, msg: MockMsg) -> None:
            pass

    class MockServiceBusClient:
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
            return MockReceiver()

    with patch(
        "extensions.eda.plugins.event_source.azure_service_bus.ServiceBusClient.from_connection_string",
        return_value=MockServiceBusClient(),
    ):
        queue: asyncio.Queue[Any] = asyncio.Queue()
        feedback_queue: asyncio.Queue[Any] = asyncio.Queue()
        args: Dict[str, Any] = {
            "conn_str": "fake",
            "queue_name": "queue",
            "feedback": True,
            "eda_feedback_queue": feedback_queue,
            "feedback_timeout": 0.1,  # Short timeout for testing
        }

        # Don't put anything in feedback queue, so it times out
        with pytest.raises(asyncio.TimeoutError):
            await receive_events(queue, args)
