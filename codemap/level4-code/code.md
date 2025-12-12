# Level 4: Code

<!-- Last updated: 2025-12-12 -->

The Code level shows key class hierarchies and design patterns used in the codebase.

## Class Diagrams

Class diagrams are split by component area:

### Chat Service Hierarchy
Source: [code-chat-service.puml](./code-chat-service.puml)

### Database Repository Hierarchy
Source: [code-database.puml](./code-database.puml)

### Azure Client Builders
Source: [code-azure-builders.puml](./code-azure-builders.puml)

### Error Hierarchy
Source: [code-errors.puml](./code-errors.puml)

### Request/Response Models
Source: [code-models.puml](./code-models.puml)

## Design Patterns

| Pattern | Location | Purpose |
|---------|----------|---------|
| **Factory** | `ChatHistoryRepository`, `RepositoryFactory`, `AzureClientFactory` | Dynamic backend selection |
| **Strategy** | `KBBackend`, `Dialect` | Swappable algorithms |
| **Repository** | `IChatHistoryRepository`, `BaseSQLRepository` | Data access abstraction |
| **Builder** | `AzureClientBuilder` and subclasses | Flexible client construction |
| **Facade** | `ChatService`, `AzureSearchProvider` | Simplified interfaces |
| **Dependency Injection** | `Container`, FastAPI dependencies | Loosely coupled services |
| **Middleware** | `RequestContextMiddleware`, `SecurityHeadersMiddleware` | Cross-cutting concerns |
| **Template Method** | `BaseSQLRepository` | Algorithm skeleton reuse |

## Key Classes

### Chat Service

| Class | File | Purpose |
|-------|------|---------|
| `IChatService` | `services/chat_service.py` | Abstract chat service interface |
| `ChatService` | `services/chat_service.py` | Chat service facade |
| `MultiAgentChatService` | `services/chat_services/multi_agent/service.py` | AutoGen orchestration |
| `OpenAIService` | `external_services/openai_service.py` | Azure OpenAI client |

### Database

| Class | File | Purpose |
|-------|------|---------|
| `IChatHistoryRepository` | `db/chat_history_interface.py` | Repository interface |
| `ChatHistoryRepository` | `db/chat_history_repository.py` | Repository factory |
| `BaseSQLRepository` | `db/base_sql.py` | Base SQL implementation |
| `SQLiteChatHistoryRepository` | `db/sqlite/` | SQLite implementation |
| `AzureSQLChatHistoryRepository` | `db/azuresql/` | Azure SQL implementation |
| `QueryBuilder` | `db/query_builder/builder.py` | SQL query builder |
| `Dialect` | `db/query_builder/base.py` | SQL dialect abstraction |

### Azure Integration

| Class | File | Purpose |
|-------|------|---------|
| `AzureClientBuilder` | `client/azure/builder/base.py` | Abstract builder |
| `AzureSearchClientBuilder` | `client/azure/builder/search_client.py` | Search client builder |
| `AzureSqlClientBuilder` | `client/azure/builder/sql_client.py` | SQL client builder |
| `AzureOpenAIClientBuilder` | `client/azure/builder/openai_client.py` | OpenAI client builder |
| `AzureClientFactory` | `client/azure/azure_client_builder_factory.py` | Builder factory |

### Configuration

| Class | File | Purpose |
|-------|------|---------|
| `IngeniousSettings` | `config/main_settings.py` | Root configuration |
| `ModelSettings` | `config/models.py` | LLM model settings |
| `ChatHistorySettings` | `config/models.py` | Database settings |
| `WebSettings` | `config/models.py` | Web server settings |

### Errors

| Class | File | Purpose |
|-------|------|---------|
| `IngeniousError` | `errors/base_error.py` | Base error class |
| `ChatServiceError` | `errors/service.py` | Service errors |
| `DatabaseError` | `errors/database.py` | Database errors |
| `ConfigurationError` | `errors/configuration.py` | Config errors |
| `ContentFilterError` | `errors/content_filter_error.py` | Content filter errors |

## Critical Code Paths

### Chat Request Processing
```
POST /api/v1/chat
  -> chat() route handler
  -> ChatService.get_chat_response()
  -> MultiAgentChatService.get_chat_response()
  -> _build_thread_memory()
  -> ChatHistoryRepository.get_thread_messages()
  -> Database query
  -> ChatResponse
```

### Streaming Chat Response
```
POST /api/v1/chat/stream
  -> chat_stream() route handler
  -> ChatService.get_streaming_chat_response()
  -> MultiAgentChatService.get_streaming_chat_response()
  -> stream_response_as_chunks()
  -> StreamingResponse (SSE)
```

### Knowledge Base Query
```
ChatRequest with KB query
  -> ConversationFlow (KnowledgeBaseAgent)
  -> KB policy resolution
  -> AzureKBBackend.search() or ChromaKBBackend.search()
  -> KBSearchResult
  -> Agent response generation
```

## Shared Base Classes

| Interface | Implementations | Purpose |
|-----------|-----------------|---------|
| `IChatService` | `ChatService`, `MultiAgentChatService` | Chat operation contract |
| `IChatHistoryRepository` | SQLite, AzureSQL, Cosmos repos | Unified data access |
| `KBBackend` | `AzureKBBackend`, `ChromaKBBackend` | KB search abstraction |
| `AzureClientBuilder` | 4+ specialized builders | Azure client construction |
| `Dialect` | `SQLiteDialect`, `AzureSQLDialect` | SQL generation |
| `IngeniousError` | 10+ error subclasses | Structured error handling |
