# Level 2: Containers

<!-- Last updated: 2025-12-12 -->

The Container diagram shows the major deployable units and their interactions within the Ingenious framework.

## Diagram

See [containers.puml](./containers.puml) for the C4-PlantUML diagram.

## Container Details

| Container | Technology | Purpose |
|-----------|------------|---------|
| **CLI Tool** | Python/Typer | Command-line interface for project init, validation, server management |
| **FastAPI Server** | Python/FastAPI | REST API for chat interactions, conversation management |
| **Documentation** | HTML/CSS | Swagger UI and interactive API docs |
| **Chat Service** | Python/AutoGen | Multi-agent orchestration with configurable conversation flows |
| **Conversation Flows** | Python | Pluggable workflow patterns (KB Agent, SQL Agent, Classification) |
| **Authentication** | Python/PyJWT | JWT and Basic auth with role-based access control |
| **Configuration System** | Python/Pydantic | Environment-based configuration management |
| **Chat History Database** | SQLite/Azure SQL/Cosmos | Persistent storage for conversations and feedback |
| **File Storage** | Local/Azure Blob | Document and file management |
| **Azure AI Search** | Azure Cognitive Search | Vector search and semantic ranking for RAG |
| **Azure OpenAI API** | REST API | LLM service for chat completions and embeddings |
| **ChromaDB** | Vector Database | Local vector embeddings for development |
| **Document Processor** | Python/Azure Doc Intel | PDF and document text extraction |
| **Chunking Service** | Python/LangChain | Semantic chunking for document ingestion |

## Communication

### Synchronous (REST/HTTP)
- **User -> FastAPI Server**: Chat requests, workflow invocations
- **FastAPI Server -> Azure OpenAI**: Chat completions, embeddings
- **FastAPI Server -> Azure AI Search**: Vector and semantic queries
- **Conversation Flows -> Azure SQL**: Direct SQL execution

### Asynchronous
- **FastAPI Server -> Chat History DB**: Non-blocking persistence via aiosqlite
- **Document Processor -> Chunking Service**: Async document pipeline

### In-Process
- **CLI Tool -> FastAPI Server**: Server startup via uvicorn
- **Chat Service -> AutoGen**: Multi-agent coordination
- **Chat Service -> Conversation Flows**: Workflow execution

### File-based
- **File Storage -> Document Processor**: Document ingestion
- **SQLite**: Local chat history via file I/O

## Entry Points

| Container | Entry Point | Protocol |
|-----------|-------------|----------|
| CLI Tool | `ingen` command | Command-line |
| FastAPI Server | `POST /chat`, `/chat/stream` | HTTP REST |
| Custom Workflows | `POST /custom-workflows` | HTTP REST |
| Authentication | `POST /auth/token` | HTTP REST |
| Swagger UI | `GET /docs` | HTTP |

## Deployment Configuration

```yaml
# Environment variables for container configuration
INGENIOUS_WEB_CONFIGURATION__PORT=8000
INGENIOUS_WEB_CONFIGURATION__IP_ADDRESS=0.0.0.0
INGENIOUS_CHAT_HISTORY__DATABASE_TYPE=sqlite  # or azuresql, cosmos
INGENIOUS_CHAT_SERVICE__TYPE=multi_agent
KB_POLICY=local_only  # or azure_only, prefer_azure, prefer_local
```

## Container Dependencies

```
CLI Tool
  |
  +-> Configuration System
  +-> FastAPI Server
        |
        +-> Authentication
        +-> Chat Service
              |
              +-> Conversation Flows
              |     |
              |     +-> Azure OpenAI API
              |     +-> Azure AI Search / ChromaDB
              |     +-> Azure SQL (for SQL workflows)
              |
              +-> Chat History Database
              +-> File Storage
```
