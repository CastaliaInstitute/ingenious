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
