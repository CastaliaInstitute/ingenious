# CLAUDE.md - Ingen Prompt Tuner

This file provides guidance to Claude Code when working with the Ingen Prompt Tuner codebase.

## Project Overview

**Ingen Prompt Tuner** is a visual interface for inspecting, editing, and testing AI agent prompts within the Ingenious framework. It serves dual purposes:

1. **Prompt Management UI**: Browse, edit, and version AI prompts with Jinja2 template support
2. **Central AI Orchestration Hub**: Hosts the Ingenious agent flow that other applications call for AI responses

**Critical**: The backend's `/api/v1/chat` endpoint is the single entry point for AI agent execution. Client applications (e.g., SoCa) call this endpoint rather than hosting their own AI logic.

## Communication Style

- **NEVER use emojis** in code, comments, or documentation
- Maintain concise, professional tone in all interactions
- Focus on technical accuracy over conversational language

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **Package Manager**: uv
- **AI Orchestration**: Ingenious (v0.2.8+) with AutoGen agents
- **Authentication**: JWT (python-jose + bcrypt)
- **Database**: Azure Cosmos DB (for trace persistence)
- **LLM Provider**: Azure OpenAI

### Frontend
- **Framework**: Vue 3 + Composition API
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **State Management**: Pinia
- **HTTP Client**: Axios
- **Code Editor**: CodeMirror 6
- **Build Tool**: Vite

## Directory Structure

```
ingen-prompt-tuner/
├── backend/
│   ├── src/ingen_prompt_tuner/
│   │   ├── main.py              # FastAPI app + all endpoints
│   │   ├── config.py            # Settings + Ingenious config
│   │   ├── models.py            # Pydantic data models
│   │   ├── auth/                # JWT authentication
│   │   ├── prompts/             # Prompt management (in-memory)
│   │   ├── traces/              # Cosmos DB trace storage
│   │   └── conversation_flows/  # Ingenious agent pipelines
│   │       └── soca_evaluator/  # SoCa evaluation agent
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.vue              # Root component
│   │   ├── main.ts              # Vue 3 entry point
│   │   ├── components/          # Vue components by feature
│   │   ├── stores/              # Pinia state stores
│   │   ├── services/            # API service layer
│   │   └── types/               # TypeScript interfaces
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── spec.md                      # User stories specification
└── tech-specs.md                # Technical specification
```

## Development Commands

### Backend

```bash
cd backend

# Install dependencies
uv sync

# Run development server (port 8002)
uv run uvicorn ingen_prompt_tuner.main:app --host 0.0.0.0 --port 8002 --reload

# Type checking
uv run mypy src/

# Run tests
uv run pytest
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server (port 5174, proxies /api to :8002)
npm run dev

# Production build
npm run build

# Linting and formatting
npm run lint
npm run typecheck
npm run format
```

### Full Stack Local Development

```bash
# Terminal 1: Backend
cd backend && uv run uvicorn ingen_prompt_tuner.main:app --host 0.0.0.0 --port 8002 --reload

# Terminal 2: Frontend
cd frontend && npm run dev

# Access: http://localhost:5174
# Login credentials: see CREDENTIALS.md at repository root
```

## Backend API Endpoints

### Authentication
- `POST /api/auth/login` - Login with email/password, returns JWT
- `GET /api/auth/me` - Get current user info (requires auth)

### Revisions
- `GET /api/revisions` - List all prompt revisions

### Prompts
- `GET /api/prompts/{revision}` - List prompts for a revision
- `GET /api/prompts/{revision}/{filename}` - Get specific prompt
- `PUT /api/prompts/{revision}/{filename}` - Update prompt content

### Traces
- `GET /api/traces` - List conversation traces (optional `revision` filter)
- `GET /api/traces/{trace_id}` - Get specific trace

### Statistics
- `GET /api/stats` - Dashboard statistics

### AI Chat (Core Feature)
- `POST /api/v1/chat` - Process AI chat requests via Ingenious agents
  - Request: `{ user_prompt, thread_id, conversation_flow, topic? }`
  - Response: `{ thread_id, message_id, agent_response, token_count, memory_summary }`

## Configuration

### Backend Environment Variables

```bash
# Server
PT_HOST=0.0.0.0
PT_PORT=8002

# Authentication
PT_AUTH_ENABLED=true
PT_JWT_SECRET=<production-secret>
PT_JWT_EXPIRE_MINUTES=1440
PT_ADMIN_EMAIL=admin@prompttuner.local
PT_ADMIN_PASSWORD=<secure-password>

# Ingenious Framework (alternative to PT_AZURE_OPENAI_* vars)
INGENIOUS_MODELS__0__API_KEY=<azure-openai-key>
INGENIOUS_MODELS__0__BASE_URL=https://eastus.api.cognitive.microsoft.com/
INGENIOUS_MODELS__0__MODEL=gpt-4o-mini
INGENIOUS_MODELS__0__DEPLOYMENT=gpt-4o-mini-deployment
INGENIOUS_MODELS__0__API_VERSION=2024-12-01-preview
INGENIOUS_MODELS__0__API_TYPE=rest
INGENIOUS_MODELS__0__ROLE=chat

# Cosmos DB (for trace persistence)
PT_COSMOS_ENDPOINT=https://your-cosmos.documents.azure.com:443/
PT_COSMOS_KEY=<cosmos-key>
PT_COSMOS_DATABASE=soca
PT_COSMOS_CONTAINER=traces
```

**Legacy PT_* to INGENIOUS_* mapping**: The config module automatically maps `PT_AZURE_OPENAI_*` variables to the Ingenious format for backward compatibility.

### Frontend Environment Variables

```bash
VITE_API_BASE_URL=http://localhost:8002
```

## Key Architectural Patterns

### Conversation Flow Pattern

The backend uses the Ingenious `ConversationFlow` pattern for AI agent orchestration:

```python
# backend/src/ingen_prompt_tuner/conversation_flows/soca_evaluator/soca_evaluator.py
class ConversationFlow:
    @staticmethod
    async def get_conversation_response(
        message: str,
        topics: Optional[list[str]] = None,
        revision: str = "active",
        ...
    ) -> tuple[str, str, int]:  # (result_json, memory_summary, token_count)
        # 1. Get configurable system prompt
        # 2. Create Azure OpenAI client via AzureOpenAIChatCompletionClientBuilder
        # 3. Initialize AutoGen AssistantAgent
        # 4. Send message and get response
        # 5. Validate against EvaluationResponseSchema
        # 6. Return structured result
```

### Frontend State Management

Pinia stores organize state by domain:

- `auth.ts` - Authentication state and JWT token
- `revisions.ts` - Revisions and prompts data
- `traces.ts` - Conversation traces
- `editor.ts` - Prompt editor state with change tracking
- `ui.ts` - UI state (active tab, expanded items)

### API Service Layer

All API calls go through typed service modules:

```typescript
// frontend/src/services/prompts.service.ts
export const promptsService = {
  list: (revision: string): Promise<Prompt[]> => api.get(`/prompts/${revision}`),
  update: (revision: string, filename: string, content: string): Promise<void> =>
    api.put(`/prompts/${revision}/${filename}`, { content }),
}
```

## Code Conventions

### Backend (Python)

- Use type hints for all function signatures
- Pydantic models for request/response validation
- FastAPI dependency injection for auth
- Async functions for I/O operations
- Structured logging with context

### Frontend (TypeScript/Vue)

- Composition API with `<script setup lang="ts">`
- Define props/emits with TypeScript types
- Use Pinia stores for shared state
- Services handle API calls, components handle UI
- Tailwind CSS for styling (no custom CSS unless necessary)

### Jinja2 Template Variables

The editor extracts variables from prompts using regex:
- `{{ variable }}` - Simple variable
- `{{ object.property }}` - Nested access
- `{% for item in items %}` - Loop variables

## Testing Artifacts

All testing artifacts, temporary files, and development scripts must go in `/tmp` folder.

## Pre-commit Checks

Do NOT circumvent pre-commit checks. When commits fail:
- Fix the underlying issue properly
- Do not use `# type: ignore`, `# noqa`, or `# nosec` to suppress errors
- Exception: `# nosec B110` is acceptable for intentional try/except/pass patterns

## Key Files Reference

### Backend
- `main.py:169` - `/api/v1/chat` endpoint (AI orchestration entry point)
- `config.py:42` - `configure_ingenious_from_env()` function
- `conversation_flows/soca_evaluator/soca_evaluator.py` - Agent implementation
- `models.py:113` - `EvaluationResponseSchema` for structured outputs
- `traces/__init__.py` - Cosmos DB trace persistence

### Frontend
- `App.vue` - Root component with auth routing
- `stores/editor.ts` - Prompt editor with variable extraction
- `components/prompts/CodeEditor.vue` - CodeMirror with Jinja2 highlighting
- `services/api.ts` - Axios instance with auth interceptors

## Integration with Client Applications

Client applications (e.g., SoCa) integrate via the chat API:

```python
# Example: SoCa backend calling Prompt Tuner
async def evaluate_submission(prompt: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://prompt-tuner:8002/api/v1/chat",
            json={
                "user_prompt": prompt,
                "thread_id": str(uuid4()),
                "conversation_flow": "soca-evaluator",
            },
        )
        return response.json()
```

## Brand Colors (Insight)

```css
--shiraz: #AE0A46;        /* Primary accent */
--mine-shaft: #222222;    /* Primary text */
--taupe: #3E332D;         /* Secondary text */
--desert-storm: #F7F6F5;  /* Light background */
```
