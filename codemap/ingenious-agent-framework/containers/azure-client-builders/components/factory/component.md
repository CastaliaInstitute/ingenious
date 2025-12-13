# Component: Azure Client Factory

<!-- Last updated: 2025-12-13 -->

**Parent:** [Azure Service Client Factory](../../container.md)
**System:** [System Context](../../../../context.md)

Centralized factory for creating all Azure service clients with proper authentication.

## Diagram

![Component](./component.png)

## Responsibility

The Azure Client Factory:
- Provides unified interface for all Azure client creation
- Delegates to specialized builders for each service
- Handles authentication method selection
- Manages client lifecycle

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| AzureClientFactory | Unified factory | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- OpenAI Builders: OpenAI client creation
- Search Builder: Search client creation
- Database Builders: SQL/Cosmos creation
- Blob Builders: Blob client creation

### Cross-Container
- Configuration System: Service credentials

## Source Files

| File | Description |
|------|-------------|
| `ingenious/client/azure/azure_client_builder_factory.py` | Factory implementation |

## Factory Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `create_openai_client` | AzureOpenAI | Sync OpenAI client |
| `create_async_openai_client` | AsyncAzureOpenAI | Async OpenAI client |
| `create_chat_completion_client` | AzureOpenAIChatCompletionClient | AutoGen client |
| `create_search_client` | SearchClient | Azure Search client |
| `create_sql_client` | pyodbc.Connection | SQL connection |
| `create_cosmos_client` | CosmosClient | Cosmos DB client |
| `create_blob_service_client` | BlobServiceClient | Blob service client |
| `create_blob_client` | BlobClient | Individual blob client |
