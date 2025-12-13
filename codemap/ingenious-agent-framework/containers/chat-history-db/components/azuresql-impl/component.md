# Component: Azure SQL Implementation

<!-- Last updated: 2025-12-13 -->

**Parent:** [Chat History Database](../../container.md)
**System:** [System Context](../../../../context.md)

Cloud Azure SQL Database implementation using pyodbc driver with retry logic, connection management, and MERGE-based UPSERT operations for production scenarios.

## Diagram

![Component](./component.png)

## Responsibility

The Azure SQL Implementation component:
- Provides cloud production database backend
- Initializes Azure SQL connection with retry logic
- Executes SQL queries using pyodbc driver
- Validates connection string from configuration
- Handles Azure SQL-specific MERGE syntax for UPSERT

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| azuresql_ChatHistoryRepository | Azure SQL adapter | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Base Repository: Extends BaseSQLRepository
- Query Builders: AzureSQLDialect

### Cross-Container
- Configuration System: Connection string settings
- Logging System: Structured logging

## Source Files

| File | Description |
|------|-------------|
| `ingenious/db/azuresql/__init__.py` | Azure SQL repository implementation |
