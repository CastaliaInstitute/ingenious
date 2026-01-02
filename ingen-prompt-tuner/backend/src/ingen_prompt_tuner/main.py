"""Ingen Prompt Tuner FastAPI application.

This backend hosts the Ingenious agent flow and serves as the central AI orchestration hub.
Other applications (e.g., SoCa) call the /api/v1/chat endpoint for AI agent responses.

Uses the Ingenious framework for agent definition and orchestration.
"""

import logging
import uuid
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ingen_prompt_tuner.auth import authenticate_user, create_access_token, get_current_user
from ingen_prompt_tuner.config import settings
from ingen_prompt_tuner.conversation_flows.soca_evaluator import ConversationFlow
from ingen_prompt_tuner.models import (
    ChatRequest,
    ChatResponseModel,
    LoginRequest,
    LoginResponse,
    Prompt,
    Revision,
    UpdatePromptRequest,
    User,
)
from ingen_prompt_tuner.prompts import (
    get_prompt,
    get_prompts,
    get_revisions,
    update_prompt,
)
from ingen_prompt_tuner.traces import create_trace_from_chat, get_trace, get_traces

logger = logging.getLogger(__name__)

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


# AI Chat endpoint - used by SoCa for evaluations
@app.post("/api/v1/chat", response_model=ChatResponseModel)
async def chat(request: ChatRequest) -> ChatResponseModel:
    """Process AI chat requests using Ingenious framework agents.

    This endpoint uses the Ingenious framework's ConversationFlow pattern
    to evaluate submissions against criteria using AutoGen agents.
    SoCa calls this endpoint to evaluate submissions against criteria.
    """
    message_id = str(uuid.uuid4())

    try:
        # Use the Ingenious-based conversation flow for evaluation
        result, memory_summary, token_count = await ConversationFlow.get_conversation_response(
            message=request.user_prompt,
            topics=request.topic,
            revision="active",
        )

        logger.info(
            f"Chat request processed with Ingenious agent: {message_id}, tokens: {token_count}"
        )

        # Log trace for this AI call
        workflow = request.conversation_flow or "soca-evaluator"
        create_trace_from_chat(
            trace_id=message_id,
            thread_id=request.thread_id,
            user_query=request.user_prompt,
            agent_response=result,
            token_count=token_count,
            revision="active",
            workflow=workflow,
        )

        return ChatResponseModel(
            thread_id=request.thread_id,
            message_id=message_id,
            agent_response=result,
            token_count=token_count,
            memory_summary=memory_summary,
        )

    except Exception as e:
        logger.error(f"Chat request failed: {e}")
        import json

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
