"""Ingen Prompt Tuner FastAPI application.

This backend hosts the Ingenious agent flow and serves as the central AI orchestration hub.
Other applications (e.g., SoCa) call the /api/v1/chat endpoint for AI agent responses.

Uses the Ingenious framework for agent definition and orchestration.
"""

import logging
import uuid
from typing import Any, Optional, Protocol

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ingen_prompt_tuner.auth import authenticate_user, create_access_token, get_current_user
from ingen_prompt_tuner.config import settings
from ingen_prompt_tuner.conversation_flows.criteria_generator import (
    ConversationFlow as CriteriaGeneratorFlow,
)
from ingen_prompt_tuner.conversation_flows.soca_evaluator import (
    ConversationFlow as SocaEvaluatorFlow,
)
from ingen_prompt_tuner.models import (
    ChatRequest,
    ChatResponseModel,
    CreateRevisionRequest,
    LoginRequest,
    LoginResponse,
    Prompt,
    Revision,
    UpdatePromptRequest,
    User,
)
from ingen_prompt_tuner.prompts import (
    create_revision,
    get_prompt,
    get_prompts,
    get_revisions,
    update_prompt,
)
from ingen_prompt_tuner.traces import (
    create_multi_agent_trace,
    create_trace_from_chat,
    get_trace,
    get_traces,
)

logger = logging.getLogger(__name__)


class ConversationFlowProtocol(Protocol):
    """Protocol defining the interface for conversation flows."""

    @staticmethod
    async def get_conversation_response(
        message: str,
        topics: Optional[list[str]] = None,
        revision: str = "active",
        **kwargs: Any,
    ) -> tuple[str, str, int, str]:
        """Process a conversation message and return AI response.

        Args:
            message: The user's input message to process.
            topics: Optional list of topic tags for the conversation.
            revision: Prompt revision to use (default: "active").
            **kwargs: Additional flow-specific arguments.

        Returns:
            Tuple of (result_json, memory_summary, token_count, system_prompt).
        """
        ...


# Map conversation flow names to their implementations
# Using Any for values since the flow classes use static methods which don't match Protocol typing perfectly
CONVERSATION_FLOWS: dict[str, Any] = {
    "soca-evaluator": SocaEvaluatorFlow,
    "criteria-generator": CriteriaGeneratorFlow,
}

app = FastAPI(title="Ingen Prompt Tuner API", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Auth endpoints
@app.post("/api/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest) -> LoginResponse:
    """Login with email and password."""
    user = authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.id, "email": user.email})
    return LoginResponse(token=token, user=user)


@app.get("/api/auth/me")
async def get_me(current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    """Get current user info."""
    return {"user": current_user}


# Revisions endpoints
@app.get("/api/revisions", response_model=list[Revision])
async def list_revisions(
    current_user: User = Depends(get_current_user),
) -> list[Revision]:
    """List all revisions."""
    revisions: list[Revision] = get_revisions()
    return revisions


@app.post("/api/revisions", response_model=Revision)
async def create_revision_endpoint(
    request: CreateRevisionRequest,
    current_user: User = Depends(get_current_user),
) -> Revision:
    """Create a new revision, optionally copying prompts from an existing revision."""
    try:
        revision = create_revision(request.name, request.copy_from)
        return revision
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Prompts endpoints
@app.get("/api/prompts/{revision}", response_model=list[Prompt])
async def list_prompts(
    revision: str,
    current_user: User = Depends(get_current_user),
) -> list[Prompt]:
    """List prompts for a revision."""
    prompts: list[Prompt] = get_prompts(revision)
    return prompts


@app.get("/api/prompts/{revision}/{filename}", response_model=Prompt)
async def view_prompt(
    revision: str,
    filename: str,
    current_user: User = Depends(get_current_user),
) -> Prompt:
    """View a specific prompt."""
    prompt = get_prompt(revision, filename)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.put("/api/prompts/{revision}/{filename}")
async def update_prompt_endpoint(
    revision: str,
    filename: str,
    request: UpdatePromptRequest,
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """Update a prompt's content."""
    success = update_prompt(revision, filename, request.content)
    if not success:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return {"status": "updated"}


# Traces endpoints
@app.get("/api/traces")
async def list_traces(
    revision: str | None = None,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
) -> list[dict[str, Any]]:
    """List conversation traces."""
    traces = get_traces(revision, limit)
    return [t.model_dump(by_alias=True) for t in traces]


@app.get("/api/traces/{trace_id}")
async def view_trace(
    trace_id: str,
    current_user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """View a specific trace."""
    trace = get_trace(trace_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Trace not found")
    result: dict[str, Any] = trace.model_dump(by_alias=True)
    return result


# Stats endpoint
@app.get("/api/stats")
async def get_stats(
    current_user: User = Depends(get_current_user),
) -> dict[str, int]:
    """Get dashboard stats from real data."""
    revisions = get_revisions()
    prompts = get_prompts(revisions[0].name) if revisions else []
    traces = get_traces(limit=1000)  # Get all traces for counting
    workflows = set(t.workflow for t in traces)

    return {
        "revisions": len(revisions),
        "promptFiles": len(prompts),
        "testRuns": len(traces),
        "workflows": len(workflows),
    }


# Health check
@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


# AI Chat endpoint - used by SoCa for evaluations and criteria generation
@app.post("/api/v1/chat", response_model=ChatResponseModel)
async def chat(request: ChatRequest) -> ChatResponseModel:
    """Process AI chat requests using Ingenious framework agents.

    Supports multiple conversation flows:
    - soca-evaluator: Evaluate submissions against criteria
    - criteria-generator: Extract criteria from document text
    """
    message_id = str(uuid.uuid4())
    workflow = request.conversation_flow or "soca-evaluator"

    # Get the appropriate conversation flow
    flow_class = CONVERSATION_FLOWS.get(workflow)
    if not flow_class:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown conversation_flow: {workflow}. "
            f"Supported flows: {list(CONVERSATION_FLOWS.keys())}",
        )

    # Determine agent name based on workflow
    agent_names = {
        "soca-evaluator": "SoCa Evaluator",
        "criteria-generator": "Criteria Generator",
    }
    agent_name = agent_names.get(workflow, workflow)

    try:
        # Use the selected conversation flow
        (
            result,
            memory_summary,
            token_count,
            agents_info,
        ) = await flow_class.get_conversation_response(
            message=request.user_prompt,
            topics=request.topic,
            revision="active",
        )

        logger.info(f"Chat request processed with {workflow}: {message_id}, tokens: {token_count}")

        # Parse agents_info to check for multi-agent trace data
        try:
            import json as json_module

            agents_info_parsed = json_module.loads(agents_info)
            agents_trace_data = agents_info_parsed.get("agents_trace_data", [])

            if agents_trace_data and len(agents_trace_data) > 1:
                # Multi-agent trace (soca-evaluator with 6 agents)
                create_multi_agent_trace(
                    trace_id=message_id,
                    thread_id=request.thread_id,
                    user_query=request.user_prompt,
                    agents_data=agents_trace_data,
                    revision="active",
                    workflow=workflow,
                )
            else:
                # Single agent trace (criteria-generator or fallback)
                create_trace_from_chat(
                    trace_id=message_id,
                    thread_id=request.thread_id,
                    user_query=request.user_prompt,
                    agent_response=result,
                    token_count=token_count,
                    revision="active",
                    workflow=workflow,
                    system_prompt=agents_info,
                    user_prompt=request.user_prompt,
                    agent_name=agent_name,
                )
        except (json_module.JSONDecodeError, KeyError):
            # Fallback to single agent trace
            create_trace_from_chat(
                trace_id=message_id,
                thread_id=request.thread_id,
                user_query=request.user_prompt,
                agent_response=result,
                token_count=token_count,
                revision="active",
                workflow=workflow,
                system_prompt=agents_info,
                user_prompt=request.user_prompt,
                agent_name=agent_name,
            )

        return ChatResponseModel(
            thread_id=request.thread_id,
            message_id=message_id,
            agent_response=result,
            token_count=token_count,
            memory_summary=memory_summary,
        )

    except Exception as e:
        logger.error(f"Chat request failed for {workflow}: {e}")
        import json

        # Return error response appropriate to the flow type
        if workflow == "criteria-generator":
            error_response = json.dumps(
                {
                    "name": "Error",
                    "description": f"Generation failed: {str(e)}",
                    "criteria": [],
                }
            )
        else:
            error_response = json.dumps(
                {
                    "criterionResults": [],
                    "overallScore": 0,
                    "summary": f"Evaluation failed: {str(e)}",
                }
            )

        return ChatResponseModel(
            thread_id=request.thread_id,
            message_id=message_id,
            agent_response=error_response,
            token_count=0,
            memory_summary=f"Error: {str(e)}",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port)
