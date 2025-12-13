# Component: Knowledge Base Agent

<!-- Last updated: 2025-12-13 -->

**Parent:** [Vector Search / Knowledge Base](../../container.md)
**System:** [System Context](../../../../context.md)

Production-ready knowledge base conversation flow implementing deterministic "direct" mode and optional LLM-composed "assist" mode with Azure AI Search and local ChromaDB support.

## Diagram

![Component](./component.png)

## Responsibility

The Knowledge Base Agent component:
- Implements IConversationFlow interface for KB-based conversations
- Handles policy-aware backend selection (azure_only, prefer_azure, prefer_local, local_only)
- Executes deterministic "direct" mode (direct KB search) by default
- Provides optional "assist" mode using AssistantAgent for LLM summarization
- Supports both streaming and non-streaming responses
- Performs robust preflight validation for Azure dependencies

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| ConversationFlow | KB conversation flow | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Azure Search Provider: Azure search operations

### Cross-Container
- Chat Service: IConversationFlow interface
- Chat History DB: Conversation persistence
- Configuration System: KB settings

## Source Files

| File | Description |
|------|-------------|
| `ingenious/services/chat_services/multi_agent/conversation_flows/knowledge_base_agent/knowledge_base_agent.py` | KB agent implementation |
