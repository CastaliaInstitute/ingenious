# Component: MultiAgent Orchestration

<!-- Last updated: 2025-12-13 -->

**Parent:** [Chat Service](../../container.md)
**System:** [System Context](../../../../context.md)

AutoGen-based multi-agent orchestration engine with conversation flow management, streaming support, and response generation.

## Diagram

![Component](./component.png)

## Responsibility

The Multi-Agent Service is the core orchestration engine that:
- Manages multi-agent conversations using AutoGen framework
- Loads and executes conversation flows dynamically
- Handles streaming and non-streaming responses
- Coordinates agent lifecycle and communication
- Integrates with chat history for persistence

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| MultiAgentChatService | Core orchestration | [View](./code/classes.md) |
| IConversationFlow | Flow interface | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Conversation Flows: Flow implementations
- Agents: Agent definitions

### Cross-Container
- Chat History DB: Message persistence
- File Storage: Artifact storage
- Logging System: Event logging
- Configuration System: Settings

## Source Files

| File | Description |
|------|-------------|
| `ingenious/services/chat_services/multi_agent/service.py` | Main service |
