# Component: Dependency Injection

<!-- Last updated: 2025-12-13 -->

**Parent:** [FastAPI REST API Server](../../container.md)
**System:** [System Context](../../../../context.md)

Provides FastAPI dependency injection using native FastAPI Depends mechanism. Manages service instantiation, configuration caching, and injection of services into route handlers.

## Diagram

![Component](./component.png)

## Responsibility

The Dependency Injection component:
- Provides configuration caching with LRU cache
- Instantiates OpenAI service with Azure credentials
- Resolves database type from configuration
- Creates chat history repository with database abstraction
- Instantiates chat service with proper configuration
- Creates file storage for data and revisions
- Handles conditional security (authenticated vs anonymous)

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| get_config | Configuration factory | [View](./code/classes.md) |
| get_chat_service | Chat service factory | [View](./code/classes.md) |
| get_chat_history_repository | Repository factory | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- App Factory: DI setup during initialization

### Cross-Container
- Configuration System: IngeniousSettings loading
- Chat History Repository: Database abstraction
- Chat Service: Multi-agent orchestration
- Auth System: User authentication context

## Source Files

| File | Description |
|------|-------------|
| `ingenious/services/fastapi_dependencies.py` | Dependency injection functions |
