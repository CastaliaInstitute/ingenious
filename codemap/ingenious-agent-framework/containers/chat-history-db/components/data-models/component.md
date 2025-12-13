# Component: Data Models

<!-- Last updated: 2025-12-13 -->

**Parent:** [Chat History Database](../../container.md)
**System:** [System Context](../../../../context.md)

Dataclasses and TypedDict definitions for chat history entities providing type-safe data structures for users, threads, messages, steps, elements, and feedback.

## Diagram

![Component](./component.png)

## Responsibility

The Data Models component:
- Defines dataclasses for domain entities
- Provides TypedDicts for flexible data transfer
- Specifies type definitions for enums and unions
- Ensures type safety across the codebase
- Supports serialization/deserialization

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| ChatHistory | Denormalized history record | [View](./code/classes.md) |
| User | User identity entity | [View](./code/classes.md) |
| Thread | Conversation thread | [View](./code/classes.md) |
| Step | Conversation step/turn | [View](./code/classes.md) |
| Feedback | User feedback entity | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- None

### Cross-Container
- None

## Source Files

| File | Description |
|------|-------------|
| `ingenious/db/chat_history_models.py` | Data model definitions |
