# Component: Base Repository

<!-- Last updated: 2025-12-13 -->

**Parent:** [Chat History Database](../../container.md)
**System:** [System Context](../../../../context.md)

Abstract SQL repository implementing the repository interface using composition with QueryBuilder for database-agnostic query generation.

## Diagram

![Component](./component.png)

## Responsibility

The Base Repository component:
- Implements IChatHistoryRepository interface for SQL backends
- Uses QueryBuilder for database-agnostic SQL generation
- Provides template methods for table and index creation
- Handles message and user operations with parameterized queries
- Converts database rows to domain models (Message, User)

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| BaseSQLRepository | Abstract SQL template | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Repository Interface: IChatHistoryRepository
- Data Models: ChatHistory, User
- Query Builders: SQL generation

### Cross-Container
- Configuration System: Database configuration
- Models: Message model

## Source Files

| File | Description |
|------|-------------|
| `ingenious/db/base_sql.py` | Base SQL repository |
