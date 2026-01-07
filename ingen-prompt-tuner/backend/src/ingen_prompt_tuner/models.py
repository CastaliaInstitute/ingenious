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
    system_prompt: str = Field(default="", alias="systemPrompt")
    user_prompt: str = Field(default="", alias="userPrompt")

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


class ChatRequest(BaseModel):
    """Chat request for AI agent invocation."""

    user_prompt: str
    thread_id: str
    conversation_flow: str = "soca-evaluator"
    topic: Optional[list[str]] = None


class ChatResponseModel(BaseModel):
    """Chat response from AI agent."""

    thread_id: str
    message_id: str
    agent_response: str
    token_count: int = 0
    memory_summary: Optional[str] = None


# Structured output models for AI evaluation (enforced JSON schema)
class CriterionResultSchema(BaseModel):
    """Individual criterion evaluation result with enforced schema."""

    criterionId: str = Field(description="The unique identifier of the criterion being evaluated")
    score: float = Field(description="The score given for this criterion (1 to max_score)")
    narrative: str = Field(description="A 1-2 sentence justification for the score")


class EvaluationResponseSchema(BaseModel):
    """Evaluation response schema enforced by structured outputs."""

    criterionResults: list[CriterionResultSchema] = Field(
        description="List of evaluation results for each criterion"
    )
    overallScore: float = Field(description="Weighted average score from 0-100")
    summary: str = Field(description="A 2-3 sentence summary of the overall evaluation")


# Structured output models for criteria generation
class GeneratedCriterionSchema(BaseModel):
    """Individual criterion generated from document analysis."""

    id: str = Field(description="Unique identifier in format 'criterion-N'")
    name: str = Field(description="Short name for the criterion (2-5 words)")
    description: str = Field(description="Evaluation guidance (1-2 sentences)")
    weight: int = Field(ge=0, le=100, description="Weight as percentage (0-100)")
    maxScore: int = Field(description="Maximum score for this criterion (5 or 10)")


class CriteriaGenerationResponseSchema(BaseModel):
    """Response schema for criteria generation from document analysis."""

    name: str = Field(description="Descriptive name for the criteria set")
    description: str = Field(
        default="Auto-generated criteria based on document analysis",
        description="Brief description of the criteria set",
    )
    criteria: list[GeneratedCriterionSchema] = Field(
        description="List of extracted evaluation criteria (3-7 items)"
    )
