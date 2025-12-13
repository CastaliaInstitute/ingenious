# Component: Chat History Repository Interface

<!-- Last updated: 2025-12-13 -->

**Parent:** [Chat History Database](../../container.md)
**System:** [System Context](../../../../context.md)

Defines abstract repository interface and data models for multi-database compatibility (SQLite, Azure SQL, Cosmos).

## Diagram

![Component](./component.png)

## Responsibility

The Repository Interface component:
- Defines the IChatHistoryRepository abstract interface
- Specifies all operations for chat history storage
- Ensures database-agnostic API for all consumers
- Enables runtime backend selection

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| IChatHistoryRepository | Abstract interface | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- None

### Cross-Container
- None

## Source Files

| File | Description |
|------|-------------|
| `ingenious/db/chat_history_interface.py` | Interface definition |

## Interface Methods

| Method | Description |
|--------|-------------|
| `add_user(identifier)` | Create or get user |
| `get_user(identifier)` | Retrieve user by ID |
| `add_message(message)` | Store a message |
| `get_message(id, thread)` | Retrieve single message |
| `get_thread_messages(thread)` | Get all thread messages |
| `update_message_feedback` | Update feedback flag |
| `delete_thread(thread)` | Delete entire thread |
