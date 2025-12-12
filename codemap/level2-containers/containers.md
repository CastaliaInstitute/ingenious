# Level 2: Containers

<!-- Last updated: 2025-12-12 -->

The Container diagram shows the high-level shape of the software architecture and how responsibilities are distributed.

## Diagram

Source: [containers.puml](./containers.puml)

## Container Details

| Container | Technology | Purpose |
|-----------|------------|---------|
| **FastAPI REST API** | Python FastAPI + Uvicorn | REST API server, request routing, HTTP/HTTPS |
| **CLI Application** | Python Typer | Command-line interface, workflow management |
| **Multi-Agent Service** | Python AutoGen | Agent orchestration, conversation flows |
| **Chat Service** | Python | Chat request/response handler, streaming |
| **Auth Middleware** | JWT/Basic Auth | Authentication, authorization, security headers |
| **Knowledge Base** | ChromaDB (optional) | Vector embeddings, document retrieval |
| **Memory Manager** | Python In-Memory | Conversation history, context management |

## Database Options

| Database | Technology | Use Case |
|----------|------------|----------|
| **SQLite** | SQLite 3 | Local development, file-based |
| **Azure SQL** | SQL Server | Production, cloud-native |
| **Azure Cosmos DB** | NoSQL | Distributed, high availability |

## External Services

| Service | Technology | Purpose |
|---------|------------|---------|
| **Azure OpenAI** | REST API | GPT-4/GPT-3.5, embeddings |
| **Azure AI Search** | REST API | Semantic search, vector search |
| **Azure Blob Storage** | REST API | Document storage |
| **Document Intelligence** | REST API | PDF extraction, OCR |

## Communication Patterns

### Internal Communication
- **API -> Chat Service**: Sync/async Python calls
- **Chat Service -> Multi-Agent**: Python delegation
- **Multi-Agent -> Memory Manager**: In-memory state

### External Communication
- **Multi-Agent -> Azure OpenAI**: REST/OpenAI SDK
- **Multi-Agent -> Azure AI Search**: REST API
- **Memory Manager -> Database**: SQL/ODBC/REST

## Deployment Configurations

### Minimal (Development)
- FastAPI + SQLite + Azure OpenAI
- Single container, local execution

### Standard Production
- FastAPI + Azure SQL + Azure OpenAI + Azure AI Search
- Azure Container Instances or App Service

### Full Cloud-Native
- FastAPI + Cosmos DB + Azure OpenAI + Azure AI Search + Blob Storage
- AKS with auto-scaling, multi-region
