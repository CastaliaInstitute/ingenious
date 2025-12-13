# Component: Database Builders

<!-- Last updated: 2025-12-13 -->

**Parent:** [Azure Client Builders](../../container.md)
**System:** [System Context](../../../../context.md)

Specialized builders for creating Azure database clients including SQL Database and Cosmos DB with flexible authentication and connection management.

## Diagram

![Component](./component.png)

## Responsibility

The Database Builders component:
- Provides builders for Azure SQL Database connections
- Provides builders for Azure Cosmos DB clients
- Handles database configuration extraction
- Manages connection string construction
- Supports SQL authentication and Azure AD authentication

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| AzureSqlClientBuilder | SQL connection builder | [View](./code/classes.md) |
| CosmosClientBuilder | Cosmos DB builder | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Builder Base: Abstract base class

### Cross-Container
- Configuration System: SQL and Cosmos settings

## Source Files

| File | Description |
|------|-------------|
| `ingenious/client/azure/builder/sql_client.py` | Azure SQL builders |
| `ingenious/client/azure/builder/cosmos_client.py` | Cosmos DB builder |
