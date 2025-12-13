# Component: Service Implementation

<!-- Last updated: 2025-12-13 -->

**Parent:** [Chat Service / Multi-Agent Orchestrator](../../container.md)
**System:** [System Context](../../../../context.md)

Facade implementation that dynamically loads and delegates to specific chat service types. Handles service discovery and instantiation with fallback mechanisms.

## Diagram

![Component](./component.png)

## Responsibility

The Service Implementation component:
- Provides facade pattern for service type delegation
- Dynamically loads service class based on configuration
- Handles configuration-driven service instantiation
- Implements transparent delegation to underlying implementations
- Provides fallback handling for streaming responses

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| ChatService | Facade implementation | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Service Interface: IChatService contract
- Multi-Agent Service: Default implementation

### Cross-Container
- Configuration System: Service type settings
- Error Handling: ChatServiceError

## Source Files

| File | Description |
|------|-------------|
| `ingenious/services/chat_service.py` | ChatService facade |
