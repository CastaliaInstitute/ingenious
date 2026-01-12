"""Traces module for storing and retrieving conversation traces from Cosmos DB.

This module stores traces from AI agent executions in Azure Cosmos DB.
Traces are logged when the /api/v1/chat endpoint is called for AI evaluations.

Environment variables required:
- PT_COSMOS_ENDPOINT: Cosmos DB endpoint URL
- PT_COSMOS_KEY: Cosmos DB primary key
- PT_COSMOS_DATABASE: Database name (default: soca)
- PT_COSMOS_CONTAINER: Container name (default: traces)
"""

import logging
import os
from datetime import datetime, timezone
from typing import Any, Optional

from azure.cosmos import CosmosClient, exceptions
from azure.cosmos.container import ContainerProxy

from ingen_prompt_tuner.models import AgentTrace, ConversationTrace

logger = logging.getLogger(__name__)

# Cosmos DB configuration from environment
COSMOS_ENDPOINT = os.getenv(
    "PT_COSMOS_ENDPOINT", "https://ingen-test-cosmos.documents.azure.com:443/"
)
COSMOS_KEY = os.getenv("PT_COSMOS_KEY", "")
COSMOS_DATABASE = os.getenv("PT_COSMOS_DATABASE", "soca")
COSMOS_CONTAINER = os.getenv("PT_COSMOS_CONTAINER", "traces")

_client: Optional[CosmosClient] = None
_container: Optional[ContainerProxy] = None


def _get_container() -> Optional[ContainerProxy]:
    """Get or create the Cosmos DB container client."""
    global _client, _container

    if _container is not None:
        return _container

    if not COSMOS_KEY:
        logger.warning("PT_COSMOS_KEY not set, traces will not be persisted")
        return None

    try:
        _client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
        database = _client.get_database_client(COSMOS_DATABASE)
        _container = database.get_container_client(COSMOS_CONTAINER)
        logger.info(f"Connected to Cosmos DB: {COSMOS_DATABASE}/{COSMOS_CONTAINER}")
        return _container
    except exceptions.CosmosHttpResponseError as e:
        logger.error(f"Failed to connect to Cosmos DB: {e}")
        return None


def add_trace(trace: ConversationTrace) -> None:
    """Add a new conversation trace to Cosmos DB."""
    container = _get_container()
    if container is None:
        logger.warning(f"Skipping trace storage (no Cosmos DB): {trace.trace_id}")
        return

    try:
        # Convert to dict for Cosmos DB, using trace_id as the document id
        doc = {
            "id": trace.trace_id,
            "trace_id": trace.trace_id,
            "thread_id": trace.thread_id,
            "workflow": trace.workflow,
            "revision": trace.revision,
            "user_query": trace.user_query,
            "timestamp": trace.timestamp,
            "total_tokens": trace.total_tokens,
            "agents": [
                {
                    "agent_name": agent.agent_name,
                    "order": agent.order,
                    "input": agent.input,
                    "output": agent.output,
                    "token_usage": agent.token_usage,
                    "system_prompt": agent.system_prompt,
                    "user_prompt": agent.user_prompt,
                }
                for agent in trace.agents
            ],
        }
        container.create_item(body=doc)
        logger.info(f"Stored trace: {trace.trace_id}")
    except exceptions.CosmosResourceExistsError:
        logger.warning(f"Trace already exists: {trace.trace_id}")
    except exceptions.CosmosHttpResponseError as e:
        logger.error(f"Failed to store trace: {e}")


def get_traces(revision: str | None = None, limit: int = 10) -> list[ConversationTrace]:
    """Get conversation traces from Cosmos DB, optionally filtered by revision."""
    container = _get_container()
    if container is None:
        return []

    try:
        if revision:
            query = (
                "SELECT * FROM c WHERE c.revision = @revision "
                "ORDER BY c.timestamp DESC OFFSET 0 LIMIT @limit"
            )
            params: list[dict[str, object]] = [
                {"name": "@revision", "value": revision},
                {"name": "@limit", "value": limit},
            ]
            items = container.query_items(
                query=query,
                parameters=params,
                partition_key=revision,
            )
        else:
            query = "SELECT * FROM c ORDER BY c.timestamp DESC OFFSET 0 LIMIT @limit"
            params = [{"name": "@limit", "value": limit}]
            items = container.query_items(
                query=query,
                parameters=params,
                enable_cross_partition_query=True,
            )

        traces = []
        for item in items:
            traces.append(_item_to_trace(item))
        return traces

    except exceptions.CosmosHttpResponseError as e:
        logger.error(f"Failed to query traces: {e}")
        return []


def get_trace(trace_id: str) -> Optional[ConversationTrace]:
    """Get a specific trace by ID from Cosmos DB."""
    container = _get_container()
    if container is None:
        return None

    try:
        # Need to query since we don't know the partition key (revision)
        query = "SELECT * FROM c WHERE c.trace_id = @trace_id"
        params: list[dict[str, object]] = [{"name": "@trace_id", "value": trace_id}]
        items = list(
            container.query_items(
                query=query,
                parameters=params,
                enable_cross_partition_query=True,
            )
        )
        if items:
            return _item_to_trace(items[0])
        return None

    except exceptions.CosmosHttpResponseError as e:
        logger.error(f"Failed to get trace {trace_id}: {e}")
        return None


def delete_traces_by_thread_id(thread_id: str) -> int:
    """Delete all traces matching a thread_id from Cosmos DB.

    Args:
        thread_id: The thread ID to match for deletion.

    Returns:
        Number of traces deleted.
    """
    container = _get_container()
    if container is None:
        logger.warning(f"Skipping trace deletion (no Cosmos DB): thread_id={thread_id}")
        return 0

    try:
        # Find all traces with matching thread_id
        query = "SELECT c.id, c.revision FROM c WHERE c.thread_id = @thread_id"
        params: list[dict[str, object]] = [{"name": "@thread_id", "value": thread_id}]
        items = list(
            container.query_items(
                query=query,
                parameters=params,
                enable_cross_partition_query=True,
            )
        )

        deleted_count = 0
        for item in items:
            try:
                container.delete_item(item["id"], partition_key=item["revision"])
                deleted_count += 1
                logger.info(f"Deleted trace: {item['id']}")
            except exceptions.CosmosHttpResponseError as e:
                logger.error(f"Failed to delete trace {item['id']}: {e}")

        logger.info(f"Deleted {deleted_count} traces for thread_id={thread_id}")
        return deleted_count

    except exceptions.CosmosHttpResponseError as e:
        logger.error(f"Failed to query traces for deletion: {e}")
        return 0


def _item_to_trace(item: dict[str, Any]) -> ConversationTrace:
    """Convert a Cosmos DB item to a ConversationTrace model."""
    return ConversationTrace(
        trace_id=item["trace_id"],
        thread_id=item["thread_id"],
        workflow=item["workflow"],
        revision=item["revision"],
        user_query=item["user_query"],
        timestamp=item["timestamp"],
        total_tokens=item["total_tokens"],
        agents=[
            AgentTrace(
                agent_name=agent["agent_name"],
                order=agent["order"],
                input=agent["input"],
                output=agent["output"],
                token_usage=agent["token_usage"],
                system_prompt=agent.get("system_prompt", ""),
                user_prompt=agent.get("user_prompt", ""),
            )
            for agent in item.get("agents", [])
        ],
    )


def create_trace_from_chat(
    trace_id: str,
    thread_id: str,
    user_query: str,
    agent_response: str,
    token_count: int,
    revision: str = "active",
    workflow: str = "soca-evaluator",
    system_prompt: str = "",
    user_prompt: str = "",
    agent_name: str = "SoCa Evaluator",
) -> ConversationTrace:
    """Create and store a trace from a chat API call."""
    timestamp = datetime.now(timezone.utc).isoformat()

    # Truncate prompts to reasonable sizes for storage
    truncated_system = system_prompt[:5000] + "..." if len(system_prompt) > 5000 else system_prompt
    truncated_user = user_prompt[:5000] + "..." if len(user_prompt) > 5000 else user_prompt

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
                agent_name=agent_name,
                order=1,
                input=user_query[:50000] + "..." if len(user_query) > 50000 else user_query,
                output=agent_response[:50000] + "..."
                if len(agent_response) > 50000
                else agent_response,
                token_usage=token_count,
                system_prompt=truncated_system,
                user_prompt=truncated_user,
            )
        ],
    )

    add_trace(trace)
    return trace


def create_multi_agent_trace(
    trace_id: str,
    thread_id: str,
    user_query: str,
    agents_data: list[dict[str, Any]],
    revision: str = "active",
    workflow: str = "soca-evaluator",
) -> ConversationTrace:
    """Create and store a trace with multiple agent executions.

    Args:
        trace_id: Unique trace identifier
        thread_id: Conversation thread ID
        user_query: Original user query
        agents_data: List of agent execution data, each containing:
            - agent_name: Name of the agent
            - order: Execution order (1-6)
            - input: Input received by agent
            - output: Output produced by agent
            - token_usage: Tokens used
            - system_prompt: System prompt used
            - user_prompt: User prompt used
        revision: Prompt revision used
        workflow: Workflow name

    Returns:
        Created ConversationTrace
    """
    timestamp = datetime.now(timezone.utc).isoformat()

    def truncate(text: str, max_len: int) -> str:
        """Truncate text to max_len characters, adding ellipsis if needed."""
        return text[:max_len] + "..." if len(text) > max_len else text

    agents: list[AgentTrace] = []
    total_tokens = 0

    for agent_data in agents_data:
        token_usage = agent_data.get("token_usage", 0)
        total_tokens += token_usage

        agents.append(
            AgentTrace(
                agent_name=agent_data.get("agent_name", "Unknown"),
                order=agent_data.get("order", len(agents) + 1),
                input=truncate(agent_data.get("input", ""), 50000),
                output=truncate(agent_data.get("output", ""), 50000),
                token_usage=token_usage,
                system_prompt=truncate(agent_data.get("system_prompt", ""), 5000),
                user_prompt=truncate(agent_data.get("user_prompt", ""), 5000),
            )
        )

    trace = ConversationTrace(
        trace_id=trace_id,
        thread_id=thread_id,
        workflow=workflow,
        revision=revision,
        user_query=truncate(user_query, 200),
        timestamp=timestamp,
        total_tokens=total_tokens,
        agents=agents,
    )

    add_trace(trace)
    return trace
