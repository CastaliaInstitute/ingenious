"""Data models for chat history storage.

This module contains dataclasses for representing chat history entities:
users, threads, and messages.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID


@dataclass
class ChatHistory:
    """Dataclass representing a complete chat history record."""

    user_id: str
    thread_id: str
    message_id: str
    positive_feedback: Optional[bool]
    timestamp: str
    role: str
    content: str
    content_filter_results: Optional[str]
    tool_calls: Optional[str]
    tool_call_id: Optional[str]
    tool_call_function: Optional[str]


@dataclass
class User:
    """Dataclass representing a user entity."""

    id: UUID
    identifier: str
    metadata: dict[str, object]
    createdAt: Optional[str]


@dataclass
class Thread:
    """Dataclass representing a conversation thread."""

    id: UUID
    createdAt: Optional[str]
    name: Optional[str]
    userId: UUID
    userIdentifier: Optional[str]
    tags: Optional[List[str]]
    metadata: Optional[dict[str, object]]


def get_now() -> datetime:
    """Get the current UTC datetime.

    Returns:
        Current datetime object in UTC timezone.
    """
    return datetime.now(timezone.utc)


def get_now_as_string() -> str:
    """Get the current UTC datetime as a formatted string.

    Returns:
        ISO-formatted datetime string with microseconds and timezone.
    """
    return get_now().strftime("%Y-%m-%d %H:%M:%S.%f%z")
