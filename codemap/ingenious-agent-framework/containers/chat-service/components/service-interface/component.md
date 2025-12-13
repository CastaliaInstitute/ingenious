# Component: Service Interface

<!-- Last updated: 2025-12-13 -->

**Parent:** [Chat Service / Multi-Agent Orchestrator](../../container.md)
**System:** [System Context](../../../../context.md)

Abstract interface contract defining the core chat service operations. Provides protocol for message processing and response streaming.

## Diagram

![Component](./component.png)

## Responsibility

The Service Interface component:
- Defines abstract interface for all chat service implementations
- Provides contract for synchronous and asynchronous message processing
- Specifies streaming response protocol for real-time delivery
- Establishes standard error handling and response formatting
- Defines chat request and response data models

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| IChatService | Abstract base interface | [View](./code/classes.md) |
| ChatRequest | Request data model | [View](./code/classes.md) |
| ChatResponse | Response data model | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- None (pure interface definition)

### Cross-Container
- Configuration System: Settings models
- Chat Models: Data transfer objects

## Source Files

| File | Description |
|------|-------------|
| `ingenious/services/chat_service.py` | Chat service interface |
| `ingenious/models/chat.py` | Request/response data models |
