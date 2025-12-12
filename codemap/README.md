# C4 Architecture Map

<!-- Last updated: 2025-12-12 -->

Overview of Ingenious AI Agent Framework architecture using the C4 model.

## Contents

| Level | Scope | Documentation | Diagram |
|-------|-------|---------------|---------|
| 1 | System Context | [context.md](./context.md) | [context.puml](./context.puml) |
| 2 | Containers | [containers.md](./containers.md) | [containers.puml](./containers.puml) |
| 3 | Components | [components.md](./components.md) | components-*.puml |
| 4 | Code | [code.md](./code.md) | code-*.puml |

## Technology Stack

| Container | Technology | Language | Purpose |
|-----------|-----------|----------|---------|
| CLI Tool | Typer, Rich, Python-dotenv | Python 3.13+ | Command-line interface and project scaffolding |
| FastAPI Server | FastAPI, Uvicorn, Pydantic | Python 3.13+ | REST API server and request routing |
| Chat Service | AutoGen, AutoGen-ext, OpenAI SDK | Python 3.13+ | Multi-agent orchestration and LLM coordination |
| Conversation Flows | AutoGen, Python | Python 3.13+ | Task-specific agent workflows |
| Authentication | PyJWT, PassLib, BCrypt, python-jose | Python 3.13+ | Token-based and credential authentication |
| Configuration | Pydantic-settings, Python-dotenv | Python 3.13+ | Environment-driven settings management |
| Chat History DB | aiosqlite, pyodbc, Azure SDK | Python/SQLite/SQL | Conversation and message persistence |
| File Storage | aiofiles, Azure Storage SDK | Python | Local/cloud file management |
| Azure OpenAI | OpenAI SDK, tiktoken | Python/REST API | LLM inference and embeddings |
| Azure AI Search | Azure Search SDK | Python/REST API | Vector and semantic search |
| ChromaDB | chromadb SDK | Python | Local vector embeddings |

## Key Files

| Category | File Path | Purpose |
|----------|-----------|---------|
| App Factory | `ingenious/main/app_factory.py` | FastAPI application factory with DI setup |
| Routing | `ingenious/main/routing.py` | API route registration and management |
| Chat Service | `ingenious/services/chat_service.py` | Chat service interface and facade |
| Multi-Agent | `ingenious/services/chat_services/multi_agent/service.py` | AutoGen multi-agent orchestration |
| Database | `ingenious/db/chat_history_repository.py` | Chat history repository factory |
| Connection Pool | `ingenious/db/connection_pool.py` | Database connection pooling |
| Configuration | `ingenious/config/main_settings.py` | Main settings class |
| Auth Config | `ingenious/config/auth_config.py` | Azure authentication configuration |
| Azure Builders | `ingenious/client/azure/builder/` | Azure client builder pattern |
| File Storage | `ingenious/files/files_repository.py` | File storage abstraction |
| Errors | `ingenious/errors/base_error.py` | Base error class hierarchy |
| API Routes | `ingenious/api/routes/` | REST API endpoint definitions |
| CLI | `ingenious/cli/main.py` | CLI application entry point |

## Rendering Diagrams

PlantUML diagrams can be rendered using:

### VS Code Extension
Install the PlantUML extension and open any `.puml` file, then use `Alt+D` to preview.

### Online Editor
Visit https://www.plantuml.com/plantuml/uml/ and paste diagram contents.

### Command Line
```bash
# Install PlantUML (macOS)
brew install plantuml

# Render all diagrams to PNG
plantuml codemap/*.puml

# Render to SVG
plantuml -tsvg codemap/*.puml
```

### Docker
```bash
docker run -v $(pwd)/codemap:/data plantuml/plantuml -tpng /data/*.puml
```

## External Integrations

| System | Purpose | Configuration |
|--------|---------|---------------|
| Azure OpenAI | LLM chat completions and embeddings | `INGENIOUS_MODELS__N__*` |
| Azure AI Search | Vector search and RAG retrieval | `INGENIOUS_AZURE_SEARCH_SERVICES__N__*` |
| Azure SQL | Chat history (cloud) | `INGENIOUS_AZURE_SQL_SERVICES__*` |
| Azure Cosmos DB | Chat history (NoSQL) | `INGENIOUS_COSMOS_SERVICE__*` |
| Azure Blob Storage | File/prompt revisions | `INGENIOUS_FILE_STORAGE__REVISIONS__*` |
| ChromaDB | Local vector embeddings | `KB_POLICY=local_only` |
| SQLite | Local chat history | `INGENIOUS_CHAT_HISTORY__DATABASE_PATH` |
