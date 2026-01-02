"""Prompt Tuner FastAPI application."""

from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from prompt_tuner.auth import authenticate_user, create_access_token, get_current_user
from prompt_tuner.config import settings
from prompt_tuner.models import (
    LoginRequest,
    LoginResponse,
    Prompt,
    Revision,
    UpdatePromptRequest,
    User,
)
from prompt_tuner.prompts import get_prompt, get_prompts, get_revisions, update_prompt
from prompt_tuner.traces import get_trace, get_traces

app = FastAPI(title="Prompt Tuner API", version="0.1.0")

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
    return get_revisions()


# Prompts endpoints
@app.get("/api/prompts/{revision}", response_model=list[Prompt])
async def list_prompts(
    revision: str,
    current_user: User = Depends(get_current_user),
) -> list[Prompt]:
    """List prompts for a revision."""
    return get_prompts(revision)


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
    return trace.model_dump(by_alias=True)


# Stats endpoint
@app.get("/api/stats")
async def get_stats(
    current_user: User = Depends(get_current_user),
) -> dict[str, int]:
    """Get dashboard stats."""
    return {
        "revisions": len(get_revisions()),
        "promptFiles": 12,
        "testRuns": 47,
        "workflows": 4,
    }


# Health check
@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port)
