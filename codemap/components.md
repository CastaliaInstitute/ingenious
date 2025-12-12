# Level 3: Components

<!-- Last updated: 2025-12-12 -->

The Component diagrams show the internal structure of each major container in the Ingenious framework.

## Diagrams

Component diagrams are split by area:
- [components-api.puml](./components-api.puml) - API routes and handlers
- [components-services.puml](./components-services.puml) - Business logic services
- [components-data.puml](./components-data.puml) - Data access layer
- [components-infrastructure.puml](./components-infrastructure.puml) - Core infrastructure
- [components-external.puml](./components-external.puml) - External service clients

## Component Responsibilities

### API Components
| Component | Responsibility |
|-----------|----------------|
| Auth Routes | JWT token generation, login, refresh |
| Chat Routes | Chat endpoint, streaming responses |
| Conversation Routes | Thread history retrieval |
| Custom Workflows Routes | Workflow invocation, introspection |
| Message Feedback Routes | Feedback collection, submission |
| Diagnostic Routes | Health checks, system diagnostics |
| Prompts Routes | Prompt management endpoints |
| Route Manager | Route registration and configuration |

### Service Components
| Component | Responsibility |
|-----------|----------------|
| ChatService | Facade for dynamic chat service loading |
| MultiAgentChatService | AutoGen-based multi-agent orchestration |
| Knowledge Base Agent | RAG conversation flow |
| SQL Manipulation Agent | SQL query generation flow |
| Classification Agent | Intent classification flow |
| Memory Manager | Conversation memory handling |
| FastAPI Dependencies | Dependency injection container |
| Message Feedback Service | Feedback recording and retrieval |
| Azure Search Provider | Retrieval-augmented generation |

### Database Components
| Component | Responsibility |
|-----------|----------------|
| ChatHistoryRepository | Factory for dynamic backend selection |
| SQLite Repository | SQLite chat history implementation |
| Azure SQL Repository | Azure SQL implementation |
| Cosmos Repository | Cosmos DB implementation |
| IChatHistoryRepository | Abstract repository interface |
| Query Builder | Abstraction for DB-specific queries |
| Connection Pool | Connection management and pooling |
| Chat History Models | Data structures (User, Message, etc) |

### Infrastructure Components
| Component | Responsibility |
|-----------|----------------|
| IngeniousSettings | Pydantic-based config root |
| Config Parser | Environment variable parsing |
| AuthConfig | Authentication settings |
| Validators | Configuration validation rules |
| Structured Logging | Correlation ID tracking, log formatting |
| Error Handling | Operation context manager |

### External Service Components
| Component | Responsibility |
|-----------|----------------|
| AzureClientBuilder | Abstract base for Azure client construction |
| AzureSearchClientBuilder | Azure AI Search client builder |
| AzureOpenAIChatCompletionClientBuilder | Azure OpenAI client builder |
| AzureSqlClientBuilder | Azure SQL client builder |
| BlobServiceClientBuilder | Azure Blob Storage client builder |
| CosmosClientBuilder | Cosmos DB client builder |
| OpenAIService | Azure OpenAI integration service |
| FileStorage | File storage facade |

## Dependencies

### API Layer Dependencies
```
API Routes
  +-- ChatService (for chat endpoint)
  +-- ChatHistoryRepository (for conversation endpoints)
  +-- MessageFeedbackService (for feedback endpoints)
  +-- Auth Middleware (security)
  +-- Models (ChatRequest, ChatResponse)
```

### Service Layer Dependencies
```
ChatService
  +-- Config (configuration)
  +-- ChatHistoryRepository (persistence)
  +-- MultiAgentChatService (implementation)
  +-- Models (chat models)

MultiAgentChatService
  +-- OpenAIService (LLM)
  +-- MemoryManager (conversation state)
  +-- ConversationFlows (workflow patterns)
  +-- AgentOrchestrator (agent coordination)
  +-- Azure Search Provider (retrieval)
```

### Database Layer Dependencies
```
ChatHistoryRepository (Factory)
  +-- sqlite_ChatHistoryRepository (backend)
  +-- azuresql_ChatHistoryRepository (backend)
  +-- cosmos_ChatHistoryRepository (backend)
  +-- QueryBuilder (query abstraction)

BaseSQLRepository
  +-- ConnectionPool (connections)
  +-- QueryBuilder (SQL generation)
```

## Key Interfaces

| Interface | Location | Purpose |
|-----------|----------|---------|
| IChatService | `services/chat_service.py` | Chat service contract |
| IChatHistoryRepository | `db/chat_history_interface.py` | Repository pattern for chat history |
| IFileStorage | `files/files_repository.py` | File storage abstraction |
| IApiRoutes | `models/api_routes.py` | Route registration contract |
| IConversationFlow | `services/chat_services/multi_agent/service.py` | Conversation flow contract |

## Shared Utilities

| Utility | Location | Consumers |
|---------|----------|-----------|
| Token Counter | `utils/token_counter.py` | MultiAgentChatService, LLM Usage Tracker |
| Structured Logging | `core/structured_logging.py` | All modules (global logger) |
| Import Utils | `utils/imports.py` | ChatService, RouteManager, Config |
| Model Utils | `utils/model_utils.py` | Chat Service, Message handlers |
| Stage Executor | `utils/stage_executor.py` | CLI commands, Workflows |
| Conversation Builder | `utils/conversation_builder.py` | Chat flows, Memory manager |
