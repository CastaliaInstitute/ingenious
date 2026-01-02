"""Traces module for storing and retrieving conversation traces.

This module stores real traces from AI agent executions. Traces are logged
when the /api/v1/chat endpoint is called for AI evaluations.
"""

from datetime import datetime, timezone
from typing import Optional

from ingen_prompt_tuner.models import AgentTrace, ConversationTrace

# In-memory trace storage (for local development)
# In production, this should be backed by Cosmos DB
_traces: dict[str, ConversationTrace] = {}


def add_trace(trace: ConversationTrace) -> None:
    """Add a new conversation trace to storage."""
    _traces[trace.trace_id] = trace


def get_traces(revision: str | None = None, limit: int = 10) -> list[ConversationTrace]:
    """Get conversation traces, optionally filtered by revision."""
    all_traces = list(_traces.values())

    # Sort by timestamp (newest first)
    all_traces.sort(key=lambda t: t.timestamp, reverse=True)

    if revision:
        all_traces = [t for t in all_traces if t.revision == revision]

    return all_traces[:limit]


def get_trace(trace_id: str) -> Optional[ConversationTrace]:
    """Get a specific trace by ID."""
    return _traces.get(trace_id)


def create_trace_from_chat(
    trace_id: str,
    thread_id: str,
    user_query: str,
    agent_response: str,
    token_count: int,
    revision: str = "active",
    workflow: str = "soca-evaluator",
) -> ConversationTrace:
    """Create and store a trace from a chat API call."""
    timestamp = datetime.now(timezone.utc).isoformat()

    trace = ConversationTrace(
        trace_id=trace_id,
        thread_id=thread_id,
        workflow=workflow,
        revision=revision,
        user_query=user_query[:200] + "..." if len(user_query) > 200 else user_query,
        timestamp=timestamp,
        total_tokens=token_count,
        agents=[
            AgentTrace(
                agent_name="SoCa Evaluator",
                order=1,
                input=user_query[:1000] + "..." if len(user_query) > 1000 else user_query,
                output=agent_response[:2000] + "..."
                if len(agent_response) > 2000
                else agent_response,
                token_usage=token_count,
            )
        ],
    )

    add_trace(trace)
    return trace
