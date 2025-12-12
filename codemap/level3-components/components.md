# Level 3: Components

<!-- Last updated: 2025-12-12 -->

The Component diagrams show how the system is made up of components and their responsibilities.

## Diagrams

Component diagrams are split by area:

### API Layer
Source: [components-api.puml](./components-api.puml)

### Services Layer
Source: [components-services.puml](./components-services.puml)

### Data Layer
Source: [components-data.puml](./components-data.puml)

### Infrastructure
Source: [components-infrastructure.puml](./components-infrastructure.puml)

### External Clients
Source: [components-external.puml](./components-external.puml)

## Component Responsibilities

### API Layer

| Component | Responsibility |
|-----------|----------------|
| Route Manager | FastAPI route registration and dispatching |
| Auth Routes | JWT and authentication endpoints |
| Chat Routes | Chat and conversation endpoints |
| Conversation Routes | Conversation history management |
| Diagnostic Routes | System diagnostics and health checks |
| Prompts Routes | Prompt management endpoints |
| Custom Routes | Extensible custom route implementations |
| Feedback Routes | Message feedback collection |
| Workflows Routes | Custom workflow execution |

### Services Layer

| Component | Responsibility |
|-----------|----------------|
| Chat Service | Abstracts and delegates to specific chat service types |
| Multi-Agent Service | AutoGen-based multi-agent conversation flows |
| Message Feedback Service | Collects and stores user feedback on responses |
| Memory Manager | Manages conversation memory and context |
| FastAPI DI | FastAPI-native dependency resolution |
| Auth Dependencies | JWT and basic auth dependency provision |
| DI Container | Legacy dependency-injector container integration |
| OpenAI Service | Azure OpenAI API client wrapper |

### Data Layer

| Component | Responsibility |
|-----------|----------------|
| Chat History Repository | Multi-backend chat history persistence |
| Files Repository | File storage abstraction (local/Azure Blob) |
| Base SQL | Common SQL query building and execution |
| Connection Pool | Database connection pooling and lifecycle |
| Query Builder | Dialect-aware SQL query construction |
| SQLite Backend | SQLite-specific implementation |
| Azure SQL Backend | Azure SQL Database implementation |
| Cosmos Backend | Azure Cosmos DB implementation |
| Repository Factory | Creates appropriate repository implementations |

### Infrastructure Layer

| Component | Responsibility |
|-----------|----------------|
| Config Loader | Environment-based configuration loading |
| Models Config | AI model settings (Azure OpenAI, embeddings) |
| Auth Config | Authentication and authorization settings |
| Main Settings | Application-wide settings (Pydantic-based) |
| Validators | Configuration validators and transformers |
| Environment Resolver | Environment variable parsing and resolution |
| Structured Logger | Correlation ID and structured logging |
| App Factory | Creates and configures FastAPI application |
| Exception Handlers | Global exception to HTTP response conversion |
| CORS Middleware | Cross-Origin Resource Sharing configuration |
| Request Context | Injects correlation IDs into requests |

### External Clients & Agents

| Component | Responsibility |
|-----------|----------------|
| Azure Client Factory | Builds and caches Azure service clients |
| OpenAI Client | Azure OpenAI REST client |
| Azure Search Provider | Azure AI Search for knowledge base retrieval |
| Search Components | Pipeline stages (generation, fusion, etc.) |
| Retrieval Module | Abstract retrieval interface |
| Agent Factory | Creates and configures AutoGen agents |
| Knowledge Base Agent | Knowledge base retrieval and synthesis |
| SQL Manipulation Agent | SQL query generation and execution |
| Classification Agent | Intent and query classification |
| Conversation Flows | Pluggable conversation patterns |

## Internal Dependencies

| Component | Depends On | Used By |
|-----------|-----------|---------|
| Route Manager | All route modules | App Factory |
| Chat Service | Multi-Agent, Memory Manager | Chat Routes |
| Multi-Agent Service | Agents, OpenAI Service | Chat Service |
| Chat History Repository | Base SQL, Repository Factory | Memory Manager |
| Base SQL | Connection Pool, Query Builder | Chat History Repository |
| Config Loader | Environment Resolver, Validators | All services |

## Interface Files

| File | Purpose |
|------|---------|
| `ingenious/services/chat_service.py` | IChatService interface |
| `ingenious/models/api_routes.py` | IApiRoutes interface |
| `ingenious/db/chat_history_interface.py` | ChatHistory persistence interface |
| `ingenious/models/database_client.py` | DatabaseClientType enum |
| `ingenious/config/models.py` | Configuration Pydantic models |
