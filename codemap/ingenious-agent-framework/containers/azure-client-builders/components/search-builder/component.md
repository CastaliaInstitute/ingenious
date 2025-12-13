# Component: Search Builder

<!-- Last updated: 2025-12-13 -->

**Parent:** [Azure Client Builders](../../container.md)
**System:** [System Context](../../../../context.md)

Specialized builders for creating Azure AI Search clients in both sync and async variants with comprehensive authentication support.

## Diagram

![Component](./component.png)

## Responsibility

The Search Builder component:
- Provides builders for sync Azure Search clients
- Provides builders for async Azure Search clients
- Handles search configuration extraction
- Manages Azure Search index name resolution
- Supports multiple authentication methods (keys, tokens, MSI)

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| AzureSearchClientBuilder | Sync search builder | [View](./code/classes.md) |
| AzureSearchAsyncClientBuilder | Async search builder | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Builder Base: Abstract base class

### Cross-Container
- Configuration System: Search settings

## Source Files

| File | Description |
|------|-------------|
| `ingenious/client/azure/builder/search_client.py` | Sync builder |
| `ingenious/client/azure/builder/search_client_async.py` | Async builder |
