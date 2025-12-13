# Component: Database Connection Pooling

<!-- Last updated: 2025-12-13 -->

**Parent:** [Chat History Database](../../container.md)
**System:** [System Context](../../../../context.md)

Connection pool management and async database access patterns with factory for creating connections.

## Diagram

![Component](./component.png)

## Responsibility

The Connection Pool component:
- Manages thread-safe connection pooling
- Provides abstract factory for database connections
- Implements health checks and retry logic
- Supports both sync and async access patterns

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| ConnectionPool | Thread-safe pool | [View](./code/classes.md) |
| ConnectionFactory | Abstract factory | [View](./code/classes.md) |
| SQLiteConnectionFactory | SQLite factory | [View](./code/classes.md) |
| AzureSQLConnectionFactory | Azure SQL factory | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- None

### Cross-Container
- None

## Source Files

| File | Description |
|------|-------------|
| `ingenious/db/connection_pool.py` | Pool implementation |

## Features

| Feature | Description |
|---------|-------------|
| Pre-population | Pool is pre-filled on initialization |
| Health Checks | Connections validated before use |
| Overflow | 2x pool_size overflow capacity |
| Retry Logic | Exponential backoff on failures |
| Thread Safety | Lock-based synchronization |
| Context Managers | Sync and async support |

## SQLite Optimizations

| Optimization | Description |
|--------------|-------------|
| WAL Mode | Write-ahead logging for concurrency |
| Normal Sync | Reduced fsync for performance |
| 10000 Page Cache | Large in-memory cache |
| Memory Temp Store | Temp tables in memory |
