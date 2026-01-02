"""Pydantic models for Prompt Tuner."""

from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    """User model."""

    id: str
    email: str


class Revision(BaseModel):
    """Revision model."""

    id: str
    name: str
    created_at: str = Field(alias="createdAt")
    prompt_count: int = Field(alias="promptCount")

    model_config = {"populate_by_name": True}


class Prompt(BaseModel):
    """Prompt model."""

    filename: str
    description: Optional[str] = None
    content: str
    size: int
    tags: list[str]
    variables: list[str]


class AgentTrace(BaseModel):
    """Agent trace model."""

    agent_name: str = Field(alias="agentName")
    order: int
    input: str
    output: str
    token_usage: int = Field(alias="tokenUsage")

    model_config = {"populate_by_name": True}


class ConversationTrace(BaseModel):
    """Conversation trace model."""

    trace_id: str = Field(alias="traceId")
    thread_id: str = Field(alias="threadId")
    workflow: str
    revision: str
    user_query: str = Field(alias="userQuery")
    timestamp: str
    agents: list[AgentTrace]
    total_tokens: int = Field(alias="totalTokens")

    model_config = {"populate_by_name": True}


# Request/Response models
class LoginRequest(BaseModel):
    """Login request."""

    email: str
    password: str


class LoginResponse(BaseModel):
    """Login response."""

    token: str
    user: User


class UpdatePromptRequest(BaseModel):
    """Update prompt request."""

    content: str
