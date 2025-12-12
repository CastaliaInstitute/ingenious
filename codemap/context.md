# Level 1: System Context

<!-- Last updated: 2025-12-12 -->

The System Context diagram shows Ingenious as an AI Agent Framework that sits at the center of a complex ecosystem of users, external services, and data stores.

## Diagram

See [context.puml](./context.puml) for the C4-PlantUML diagram.

## System Overview

**Ingenious** is a FastAPI-based multi-agent AI framework with AutoGen orchestration, chat history persistence, and modular conversation flows. It provides:

- REST API (FastAPI + Uvicorn)
- JWT/Basic authentication
- Multi-agent conversations (AutoGen)
- Chat history persistence
- Custom workflow registration
- Prompt management
- RAG (Retrieval Augmented Generation)
- Streaming responses (SSE)

## Users/Actors

| Actor | Role | Interaction Method |
|-------|------|-------------------|
| **API Consumer** | End-user application | REST API: `POST /chat`, `GET /chat/stream` |
| **System Administrator** | Infrastructure/config | Environment variables: `INGENIOUS_*` prefix |
| **Workflow Developer** | Developer | REST API: `/custom-workflows` endpoints |
| **Knowledge Base Manager** | Data management | Configuration: `KB_POLICY`, Azure AI Search setup |

## External Systems

| System | Type | Integration Point |
|--------|------|-------------------|
| Azure OpenAI | Cloud LLM Service | `ingenious/external_services/openai_service.py` |
| Azure AI Search | Vector Database | `ingenious/services/azure_search/` |
| Azure SQL Database | Cloud Database | `ingenious/db/azuresql/` |
| Azure Cosmos DB | NoSQL Database | `ingenious/db/cosmos/` |
| Azure Blob Storage | File Storage | `ingenious/files/azure/` |
| ChromaDB | Local Vector DB | `ingenious/services/chat_services/multi_agent/conversation_flows/knowledge_base_agent/backends/` |
| SQLite | Local Database | `ingenious/db/` |
| Microsoft AutoGen | Agent Framework | `ingenious/services/chat_services/multi_agent/` |
| Scrapfly | Web Scraping | `ingenious/cli/commands/` |

## Data Flows

### Inbound
- **Chat Requests**: API consumers send chat messages via `POST /chat` with conversation context
- **Configuration**: Administrators configure models, auth, and services via environment variables
- **Custom Workflows**: Developers register custom conversation flows via API

### Outbound
- **LLM Calls**: Chat completions and embeddings requests to Azure OpenAI
- **Vector Search**: Knowledge retrieval queries to Azure AI Search or ChromaDB
- **Persistence**: Chat history and message feedback stored in SQL/Cosmos/SQLite
- **File Operations**: Document storage and retrieval via Azure Blob or local filesystem

## Authentication Methods

| Method | Configuration | Use Case |
|--------|--------------|----------|
| JWT Bearer Token | `INGENIOUS_WEB_CONFIGURATION__AUTHENTICATION__*` | API consumers |
| Basic Auth | `USERNAME`, `PASSWORD` in auth config | Simple deployments |
| Azure MSI | `authentication_method: msi` | Azure-hosted services |
| Service Principal | `client_id`, `tenant_id`, `client_secret` | Enterprise integrations |
| API Key | `api_key` in service configs | External service calls |
