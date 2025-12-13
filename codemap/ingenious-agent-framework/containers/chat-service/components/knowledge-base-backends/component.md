# Component: Knowledge Base Backends

<!-- Last updated: 2025-12-13 -->

**Parent:** [Chat Service](../../container.md)
**System:** [System Context](../../../../context.md)

Pluggable knowledge base search backends with policy-based selection. Supports Azure Cognitive Search and ChromaDB.

## Diagram

![Component](./component.png)

## Responsibility

The KB Backends component provides:
- Abstract interface for knowledge base search
- Azure AI Search backend for enterprise use
- ChromaDB backend for local development
- Policy-based backend selection (KB_POLICY)
- Search result normalization

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| KBBackend | Abstract base | [View](./code/classes.md) |
| KBSearchResult | Result DTO | [View](./code/classes.md) |
| AzureKBBackend | Azure implementation | [View](./code/classes.md) |
| ChromaKBBackend | Local implementation | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- None

### Cross-Container
- Vector Search: Azure Search provider
- Configuration System: Backend settings

## Source Files

| File | Description |
|------|-------------|
| `conversation_flows/knowledge_base_agent/backends/base.py` | Abstract base |
| `conversation_flows/knowledge_base_agent/backends/azure.py` | Azure impl |
| `conversation_flows/knowledge_base_agent/backends/chroma.py` | Chroma impl |

## Backend Selection

Controlled by `KB_POLICY` environment variable:

| Policy | Behavior |
|--------|----------|
| `local_only` | ChromaDB only |
| `azure_only` | Azure Search only |
| `prefer_azure` | Azure with Chroma fallback |
| `prefer_local` | Chroma with Azure fallback |
