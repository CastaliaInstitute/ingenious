# C4 Architecture Map

<!-- Last updated: 2025-12-12 -->
<!-- Last verified: 2025-12-12 (see VERIFICATION.md) -->

Overview of Ingenious Multi-Agent AI Framework architecture using the C4 model.

## Folder Structure

```
codemap/
├── README.md
├── level1-context/
│   ├── context.puml
│   ├── context.png
│   └── context.md
├── level2-containers/
│   ├── containers.puml
│   ├── containers.png
│   └── containers.md
├── level3-components/
│   ├── components-api.puml
│   ├── components-services.puml
│   ├── components-data.puml
│   ├── components-infrastructure.puml
│   ├── components-external.puml
│   └── components.md
└── level4-code/
    ├── code-chat-service.puml
    ├── code-database.puml
    ├── code-azure-builders.puml
    ├── code-errors.puml
    ├── code-models.puml
    └── code.md
```

## Contents

| Level | Scope | Documentation | Diagrams |
|-------|-------|---------------|----------|
| 1 | System Context | [context.md](./level1-context/context.md) | [context.puml](./level1-context/context.puml) |
| 2 | Containers | [containers.md](./level2-containers/containers.md) | [containers.puml](./level2-containers/containers.puml) |
| 3 | Components | [components.md](./level3-components/components.md) | level3-components/*.puml |
| 4 | Code | [code.md](./level4-code/code.md) | level4-code/*.puml |
| - | Verification | [VERIFICATION.md](./VERIFICATION.md) | - |

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Web Framework | FastAPI 0.115.9 + Uvicorn 0.35.0 | REST API server |
| CLI | Typer 0.16.0 + Rich 13.7.1 | Command-line interface |
| Agent Orchestration | AutoGen 0.5.7 | Multi-agent conversation flows |
| Authentication | python-jose 3.5.0 + passlib 1.7.4 | JWT/Basic auth |
| Configuration | Pydantic Settings | Environment-based config |
| Local DB | SQLite + aiosqlite 0.21.0 | Development database |
| Cloud DB | Azure SQL (pyodbc 5.2.0) | Production database |
| NoSQL | Azure Cosmos DB 4.9.0 | Distributed storage |
| LLM | Azure OpenAI (openai 1.82.0) | Chat completions |
| Vector Search | Azure AI Search 11.5.2 | Knowledge base retrieval |
| Local Vector DB | ChromaDB 1.0.11 | Local embeddings |
| Blob Storage | Azure Blob Storage 12.25.1 | Document storage |
| Logging | structlog 25.4.0 | Structured logging |

## Key Files

| Path | Purpose |
|------|---------|
| `ingenious/main/app_factory.py` | FastAPI application factory |
| `ingenious/main/routing.py` | Route registration |
| `ingenious/services/chat_service.py` | Chat service facade |
| `ingenious/services/chat_services/multi_agent/service.py` | Multi-agent orchestration |
| `ingenious/db/chat_history_repository.py` | Repository factory |
| `ingenious/config/main_settings.py` | Configuration loader |
| `ingenious/client/azure/builder/` | Azure client builders |
| `ingenious/api/routes/` | API route handlers |
| `ingenious/errors/` | Error class hierarchy |

## Rendering Diagrams

PlantUML diagrams can be rendered using:

- **VS Code PlantUML extension** - Preview diagrams directly in editor
- **Online**: https://www.plantuml.com/plantuml/uml/
- **CLI**: `plantuml -tpng codemap/**/*.puml`

## Regenerating PNG Exports

```bash
# Generate PNGs for all levels
plantuml -tpng codemap/level1-context/*.puml
plantuml -tpng codemap/level2-containers/*.puml
plantuml -tpng codemap/level3-components/*.puml
plantuml -tpng codemap/level4-code/*.puml
```

## Installation

If PlantUML CLI is not available:

- **macOS**: `brew install plantuml`
- **Linux**: `apt install plantuml`
- **Manual**: Download from https://plantuml.com/download
