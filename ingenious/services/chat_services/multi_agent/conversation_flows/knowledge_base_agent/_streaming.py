"""Streaming response handling for knowledge base conversation flow.

This module handles streaming responses including state management,
message processing, and content chunking.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, AsyncIterator, Callable, Dict, List, Optional

from ._helpers import to_text

if TYPE_CHECKING:
    from ingenious.config.config import Config


@dataclass
class StreamingState:
    """Tracks the state of a streaming conversation response.

    Attributes:
        accumulated_text: Complete text accumulated so far
        current_position: Current position in the accumulated text
        tool_events: List of tool call events detected
        is_complete: Whether streaming is complete
        error: Any error that occurred during streaming
    """

    accumulated_text: str = ""
    current_position: int = 0
    tool_events: List[Dict[str, Any]] = field(default_factory=list)
    is_complete: bool = False
    error: Optional[Exception] = None


class StreamingMixin:
    """Mixin class providing streaming response functionality.

    This mixin extracts streaming-related methods from the main ConversationFlow
    class for better organization and maintainability.
    """

    if TYPE_CHECKING:
        _config: Config

    def _create_streaming_state(self) -> StreamingState:
        """Create a new streaming state instance."""
        return StreamingState()

    def _update_streaming_state(
        self,
        state: StreamingState,
        new_text: str,
    ) -> str:
        """Update streaming state and return newly added text.

        Args:
            state: The streaming state to update
            new_text: The complete accumulated text so far

        Returns:
            The delta (new text added since last update)
        """
        if len(new_text) > len(state.accumulated_text):
            delta = new_text[state.current_position :]
            state.accumulated_text = new_text
            state.current_position = len(new_text)
            return delta
        return ""

    def _detect_tool_event(
        self,
        message: Any,
        state: StreamingState,
    ) -> Optional[Dict[str, Any]]:
        """Detect and extract tool call events from messages.

        Args:
            message: The message to check for tool events
            state: The streaming state for tracking

        Returns:
            Tool event dictionary if detected, None otherwise
        """
        if not hasattr(message, "content"):
            return None

        content = message.content
        if isinstance(content, list):
            for item in content:
                if hasattr(item, "type") and item.type == "tool_use":
                    event = {
                        "type": "tool_use",
                        "name": getattr(item, "name", "unknown"),
                        "input": getattr(item, "input", {}),
                        "id": getattr(item, "id", None),
                    }
                    state.tool_events.append(event)
                    return event
        return None

    def _filter_streaming_content(
        self,
        content: str,
        filters: Optional[List[Callable[[str], str]]] = None,
    ) -> str:
        """Apply content filters to streaming output.

        Args:
            content: The content to filter
            filters: Optional list of filter functions

        Returns:
            Filtered content
        """
        if not filters:
            return content

        result = content
        for filter_fn in filters:
            try:
                result = filter_fn(result)
            except Exception:
                pass  # nosec B110 - intentionally ignoring filter errors
        return result

    def _process_stream_message(
        self,
        message: Any,
        state: StreamingState,
        logger: Optional[logging.Logger] = None,
    ) -> Optional[str]:
        """Process a single streaming message and extract content.

        Args:
            message: The message to process
            state: The streaming state
            logger: Optional logger

        Returns:
            Extracted text content or None
        """
        # Check for tool events first
        tool_event = self._detect_tool_event(message, state)
        if tool_event and logger:
            logger.debug("Tool event detected: %s", tool_event.get("name"))

        # Extract text content
        if hasattr(message, "content"):
            content = message.content
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                return self._extract_text_from_content_list(content)
        return None

    def _extract_text_from_content_list(self, content: List[Any]) -> str:
        """Extract text from a content list (mixed text/tool_use blocks).

        Args:
            content: List of content items

        Returns:
            Concatenated text content
        """
        parts: List[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif hasattr(item, "type"):
                if item.type == "text":
                    parts.append(getattr(item, "text", ""))
        return "".join(parts)

    async def _stream_with_chunking(
        self,
        text: str,
        chunk_size: int = 100,
        delay_ms: int = 0,
    ) -> AsyncIterator[str]:
        """Stream text content with chunking for non-streaming sources.

        This provides a streaming-like experience for content that isn't
        natively streamed (e.g., direct mode responses).

        Args:
            text: The text to stream
            chunk_size: Size of each chunk
            delay_ms: Optional delay between chunks in milliseconds

        Yields:
            Text chunks
        """
        import asyncio

        if not text:
            return

        for i in range(0, len(text), chunk_size):
            chunk = text[i : i + chunk_size]
            yield chunk
            if delay_ms > 0:
                await asyncio.sleep(delay_ms / 1000)

    def _finalize_streaming_state(
        self,
        state: StreamingState,
        final_text: Optional[str] = None,
    ) -> str:
        """Finalize streaming state and return complete response.

        Args:
            state: The streaming state to finalize
            final_text: Optional final text override

        Returns:
            The complete response text
        """
        state.is_complete = True
        if final_text is not None:
            state.accumulated_text = final_text
        return state.accumulated_text

    def _handle_streaming_error(
        self,
        state: StreamingState,
        error: Exception,
        logger: Optional[logging.Logger] = None,
    ) -> str:
        """Handle streaming errors and update state.

        Args:
            state: The streaming state
            error: The error that occurred
            logger: Optional logger

        Returns:
            Error message for the user
        """
        state.error = error
        state.is_complete = True

        if logger:
            logger.error("Streaming error: %s", error, exc_info=True)

        return f"An error occurred during streaming: {str(error)}"

    def _get_streaming_stats(self, state: StreamingState) -> Dict[str, Any]:
        """Get statistics about the streaming session.

        Args:
            state: The streaming state

        Returns:
            Dictionary of streaming statistics
        """
        return {
            "total_length": len(state.accumulated_text),
            "tool_events_count": len(state.tool_events),
            "is_complete": state.is_complete,
            "has_error": state.error is not None,
        }


def process_task_result(result: Any) -> str:
    """Process an AutoGen TaskResult into a text response.

    Args:
        result: The TaskResult from AutoGen

    Returns:
        Extracted text response
    """
    if result is None:
        return ""

    # Handle TaskResult objects
    if hasattr(result, "messages") and result.messages:
        return _extract_text_from_messages(result.messages)

    # Handle string results
    if isinstance(result, str):
        return result

    # Handle dict results
    if isinstance(result, dict):
        content = result.get("content", result.get("message", ""))
        return to_text(content)

    return to_text(result)


def _extract_text_from_messages(messages: List[Any]) -> str:
    """Extract text from a list of messages.

    Args:
        messages: List of message objects

    Returns:
        Concatenated text content
    """
    parts: List[str] = []

    for msg in messages:
        if hasattr(msg, "content"):
            content = msg.content
            if isinstance(content, str):
                parts.append(content)
            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, str):
                        parts.append(item)
                    elif hasattr(item, "text"):
                        parts.append(item.text)
        elif isinstance(msg, str):
            parts.append(msg)
        elif isinstance(msg, dict):
            parts.append(to_text(msg.get("content", "")))

    return "\n".join(parts)
