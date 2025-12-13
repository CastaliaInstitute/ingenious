# Component: Azure Search Provider

<!-- Last updated: 2025-12-13 -->

**Parent:** [Vector Search / Knowledge Base](../../container.md)
**System:** [System Context](../../../../context.md)

Thin facade for Azure Search pipeline operations that builds configuration, manages pipeline lifecycle, and delegates retrieval and generation operations.

## Diagram

![Component](./component.png)

## Responsibility

The Azure Search Provider component:
- Builds validated search configuration from settings
- Instantiates and manages the advanced search pipeline lifecycle
- Delegates retrieval and generation operations to the pipeline
- Handles preflight checks for generation and blank query validation
- Provides a thin, stable public API for search operations

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| AzureSearchProvider | Provider facade | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Azure Search Builders: Configuration construction
- Advanced Search Pipeline: Retrieval/generation orchestration

### Cross-Container
- Configuration System: IngeniousSettings, SearchConfig
- Azure Client Factory: Client creation

## Source Files

| File | Description |
|------|-------------|
| `ingenious/services/azure_search/provider.py` | Main provider facade |
