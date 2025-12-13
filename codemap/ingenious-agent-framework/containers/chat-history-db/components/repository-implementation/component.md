# Component: Repository Implementation

<!-- Last updated: 2025-12-13 -->

**Parent:** [Chat History Database](../../container.md)
**System:** [System Context](../../../../context.md)

Factory-based repository with dynamic backend selection using runtime module loading and instantiation based on configured database type.

## Diagram

![Component](./component.png)

## Responsibility

The Repository Implementation component:
- Dynamically loads backend-specific repository modules
- Instantiates the correct repository class based on database type
- Delegates all operations to the backend implementation
- Provides unified interface through ChatHistoryRepository wrapper

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| ChatHistoryRepository | Factory wrapper | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Repository Interface: IChatHistoryRepository
- SQLite Impl: Local database backend
- Azure SQL Impl: Cloud database backend
- Cosmos Impl: NoSQL backend

### Cross-Container
- Configuration System: Database type settings

## Source Files

| File | Description |
|------|-------------|
| `ingenious/db/chat_history_repository.py` | Factory implementation |
