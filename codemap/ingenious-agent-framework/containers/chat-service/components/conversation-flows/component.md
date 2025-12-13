# Component: Conversation Flows

<!-- Last updated: 2025-12-13 -->

**Parent:** [Chat Service / Multi-Agent Orchestrator](../../container.md)
**System:** [System Context](../../../../context.md)

Pluggable workflow patterns implementing domain-specific conversation logic. Extensible architecture supporting dynamic discovery and instantiation of conversation flows.

## Diagram

![Component](./component.png)

## Responsibility

The Conversation Flows component:
- Provides abstract flow interface (IConversationFlow)
- Implements pluggable workflow pattern discovery
- Integrates with chat history and memory management
- Supports streaming and non-streaming response generation
- Handles template rendering and prompt management

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| IConversationFlow | Abstract base class | [View](./code/classes.md) |
| ClassificationFlow | Text classification | [View](./code/classes.md) |
| KnowledgeBaseFlow | Document QA | [View](./code/classes.md) |
| SQLManipulationFlow | SQL generation | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Agents: Agent definitions
- KB Backends: Knowledge base search

### Cross-Container
- Chat History DB: Message persistence
- File Storage: Template storage
- External LLM Service: Model access

## Source Files

| File | Description |
|------|-------------|
| `ingenious/services/chat_services/multi_agent/service.py` | IConversationFlow base |
| `conversation_flows/classification_agent/` | Classification flow |
| `conversation_flows/knowledge_base_agent/` | KB flow |
| `conversation_flows/sql_manipulation_agent/` | SQL flow |
