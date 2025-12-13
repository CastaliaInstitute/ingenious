# Component: Query Builders

<!-- Last updated: 2025-12-13 -->

**Parent:** [Chat History Database](../../container.md)
**System:** [System Context](../../../../context.md)

Database-agnostic SQL query generation using builder pattern with pluggable dialect implementations for SQLite, Azure SQL, and extensible to other databases.

## Diagram

![Component](./component.png)

## Responsibility

The Query Builders component:
- Generates database-specific SQL statements
- Abstracts database syntax differences via dialects
- Builds CREATE TABLE statements with proper data types
- Generates parameterized INSERT, SELECT, UPDATE, DELETE queries
- Creates indexes for query optimization

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| QueryBuilder | Main builder | [View](./code/classes.md) |
| Dialect | Abstract dialect | [View](./code/classes.md) |
| SQLiteDialect | SQLite implementation | [View](./code/classes.md) |
| AzureSQLDialect | SQL Server implementation | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Data Models: Model definitions for table schema

### Cross-Container
- None

## Source Files

| File | Description |
|------|-------------|
| `ingenious/db/query_builder/builder.py` | QueryBuilder implementation |
| `ingenious/db/query_builder/sqlite.py` | SQLite dialect |
| `ingenious/db/query_builder/azuresql.py` | Azure SQL dialect |
