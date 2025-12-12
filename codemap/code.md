# Level 4: Code

<!-- Last updated: 2025-12-12 -->

The Code level diagrams show the detailed class structures, design patterns, and relationships within key components.

## Class Diagrams

Class diagrams are split by component area:
- [code-chat-service.puml](./code-chat-service.puml) - Chat service layer classes
- [code-database.puml](./code-database.puml) - Database and repository classes
- [code-azure-builders.puml](./code-azure-builders.puml) - Azure client builder pattern
- [code-errors.puml](./code-errors.puml) - Error handling hierarchy
- [code-models.puml](./code-models.puml) - Chat request/response models

## Design Patterns

| Pattern | Location | Purpose |
|---------|----------|---------|
| **Factory** | `db/connection_pool.py` | Abstract database connection creation |
| **Facade** | `services/chat_service.py`, `db/chat_history_repository.py` | Simplify complex subsystems |
| **Object Pool** | `db/connection_pool.py` | Reuse expensive database connections |
| **Registry** | `main/routing.py` | Centralized route registration |
| **Middleware** | `main/middleware.py`, `auth/middleware.py` | Cross-cutting concerns |
| **Builder** | `client/azure/builder/base.py` | Complex Azure client construction |
| **Strategy** | `services/chat_services/multi_agent/conversation_flows/` | Pluggable conversation flows |
| **Template Method** | `MultiAgentChatService._invoke_new_pattern()` | Skeleton of flow execution |
| **Dependency Injection** | `services/container.py`, `main/app_factory.py` | Loose coupling |
| **Abstract Base Class** | Throughout codebase | Define contracts for implementations |

## Key Classes

| Class | File | Purpose |
|-------|------|---------|
| FastAgentAPI | `main/app_factory.py` | FastAPI app factory with DI setup |
| RouteManager | `main/routing.py` | Route registration orchestrator |
| IChatService | `services/chat_service.py` | Chat service interface |
| ChatService | `services/chat_service.py` | Service facade with dynamic loading |
| MultiAgentChatService | `services/chat_services/multi_agent/service.py` | Multi-agent orchestration |
| IConversationFlow | `services/chat_services/multi_agent/service.py` | Conversation flow interface |
| ConnectionFactory | `db/connection_pool.py` | Abstract factory for DB connections |
| ConnectionPool | `db/connection_pool.py` | Connection pooling with health checks |
| ChatHistoryRepository | `db/chat_history_repository.py` | Chat history facade |
| IChatHistoryRepository | `db/chat_history_repository.py` | Chat history interface |
| IFileStorage | `files/files_repository.py` | File storage interface |
| FileStorage | `files/files_repository.py` | File storage facade |
| AzureClientBuilder | `client/azure/builder/base.py` | Azure client builder base |
| Container | `services/container.py` | Dependency injection container |
| IngeniousSettings | `config/main_settings.py` | Main configuration class |
| IngeniousError | `errors/base_error.py` | Base error class |
| OpenAIService | `external_services/openai_service.py` | Azure OpenAI integration |

## Class Hierarchies

### Error Hierarchy
```
Exception
  +-- IngeniousError
        +-- ServiceError
        |     +-- ChatServiceError
        +-- DatabaseError
        |     +-- DatabaseConnectionError
        |     +-- DatabaseQueryError
        |     +-- DatabaseTransactionError
        |     +-- DatabaseMigrationError
        +-- ConfigurationError
        |     +-- ConfigFileError
        |     +-- EnvironmentError
        |     +-- ValidationError
        +-- APIError
        |     +-- RequestValidationError
        |     +-- ResponseError
        |     +-- RateLimitError
        +-- ContentFilterError
        +-- TokenLimitExceededError
```

### Chat Service Hierarchy
```
IChatService (ABC)
  +-- ChatService (Facade)
        +-- MultiAgentChatService
              +-- IConversationFlow (ABC)
                    +-- ClassificationAgent
                    +-- SQLManipulationAgent
                    +-- KnowledgeBaseAgent
```

### Azure Builder Hierarchy
```
AzureClientBuilder (ABC)
  +-- AzureSearchClientBuilder
  +-- AzureOpenAIChatCompletionClientBuilder
  +-- AzureSqlClientBuilder
  +-- BlobServiceClientBuilder
  +-- CosmosClientBuilder
  +-- AzureSearchAsyncClientBuilder
```

### Repository Hierarchy
```
IChatHistoryRepository (ABC)
  +-- sqlite_ChatHistoryRepository
  +-- azuresql_ChatHistoryRepository
  +-- cosmos_ChatHistoryRepository
```

## Critical Code Paths

### Chat Request Flow
```
Request Handler (@router.post("/chat"))
  |
  v
ChatService.get_chat_response()
  |
  v
MultiAgentChatService.get_chat_response()
  |
  v
MultiAgentChatService._load_conversation_flow_class()
  |
  v
IConversationFlow subclass implementation
  |
  v
OpenAIService.get_chat_completion()
  |
  v
ChatHistoryRepository.add_message()
  |
  v
IChatHistoryRepository implementation (SQLite/AzureSQL/Cosmos)
```

### Streaming Response Flow
```
Request Handler (@router.post("/chat/stream"))
  |
  v
ChatService.get_streaming_chat_response()
  |
  v
MultiAgentChatService.get_streaming_chat_response()
  |
  v
stream_response_as_chunks() utility
  |
  v
FastAPI StreamingResponse
```

### Database Connection Flow
```
ChatHistoryRepository.__init__()
  |
  v
ConnectionFactory.create_connection()
  |
  v
ConnectionPool.get_connection()
  |
  v
Database Query Execution
```

## Component Interaction Patterns

### Dependency Injection
The FastAPI Dependencies module provides injectable services via `Depends()` annotation, supporting lazy loading and configuration-based selection.

### Factory Pattern
- `ChatHistoryRepository` selects DB backend based on config
- `FileStorage` selects file backend (local/Azure)
- `ChatService` dynamically loads service implementation

### Repository Pattern
- `IChatHistoryRepository` defines abstract interface
- Implementations for SQLite, Azure SQL, Cosmos DB
- `QueryBuilder` abstracts DB-specific queries

### Strategy Pattern
- Conversation flows implement `IConversationFlow` interface
- Agent patterns provide pluggable behaviors
- Database backends implement same interface

### Middleware Pattern
- Auth middleware validates requests
- Security headers middleware adds security headers
- CORS middleware handles cross-origin requests
