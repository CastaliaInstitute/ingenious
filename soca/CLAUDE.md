# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SoCa (Submission over Criteria)** is a full-stack document evaluation application. Users upload submissions (documents), define weighted evaluation criteria, and receive AI-generated scores via the Ingenious framework.

## Development Commands

### Frontend (Vue 3 + Vite)

```bash
cd frontend

# Development server (port 5173, proxies /api to backend)
npm run dev

# Build for production
npm run build

# Type checking
npm run typecheck

# Linting
npm run lint
npm run lint:fix

# Formatting
npm run format
npm run format:check
```

### Backend (FastAPI + uv)

```bash
cd backend

# Install dependencies
uv sync
uv sync --dev  # Include dev dependencies

# Run development server (port 8001)
uv run uvicorn soca.main:app --reload --port 8001

# Run tests
uv run pytest

# Type checking
uv run mypy src

# Linting and formatting
uv run ruff check src
uv run ruff format src
```

## Architecture

### System Integration

```
Frontend (Vue 3)     Backend (FastAPI)     Ingen Prompt Tuner
    :5173        -->      :8001        -->      :8002
                          |                        |
                    Cosmos DB              Azure OpenAI
                    Blob Storage
```

SoCa delegates all AI evaluation to Ingen Prompt Tuner (separate service on port 8002). The backend calls `/api/v1/chat` with `conversation_flow: "soca-evaluator"`.

### Frontend Structure (`frontend/src/`)

- **`components/`** - Vue components organized by feature (auth, criteria, evaluations, submissions, layout)
- **`stores/`** - Pinia stores for state management (auth, criteria, evaluations, submissions, ui)
- **`services/`** - Axios-based API clients (`api.ts` configures base instance with JWT interceptor)
- **`types/`** - TypeScript interfaces

### Backend Structure (`backend/src/soca/`)

- **`main.py`** - FastAPI application with all route handlers
- **`models.py`** - Pydantic models for request/response validation
- **`config.py`** - Settings class using pydantic-settings
- **`auth/`** - JWT authentication (HS256, 24-hour expiration)
- **`db/`** - Cosmos DB repository with in-memory fallback
- **`submissions/`** - Azure Blob Storage file handling
- **`evaluations/`** - AI integration via Prompt Tuner API

### Key Patterns

- Frontend uses Composition API with `<script setup>` syntax
- Vite dev server proxies `/api/*` requests to backend automatically
- Backend uses async/await throughout (FastAPI, httpx, Azure SDKs)
- In-memory storage fallback when Cosmos DB unavailable (development)

## Configuration

Environment variables use `SOCA_` prefix:

```bash
# Backend server
SOCA_PORT=8001
SOCA_HOST=0.0.0.0
SOCA_JWT_SECRET=<secret>

# Azure services
SOCA_COSMOS_URI=<azure-cosmos-uri>
SOCA_COSMOS_KEY=<azure-key>
SOCA_STORAGE_CONNECTION_STRING=<azure-blob-string>

# Ingen Prompt Tuner integration
SOCA_INGENIOUS_API_URL=http://localhost:8002
SOCA_INGENIOUS_API_KEY=<api-key>
```

Admin credentials are stored in the gitignored `CREDENTIALS.md` file at the repository root.

## Data Models

Core entities: Submission, Criterion, CriteriaSet, Evaluation, EvaluationResult. All stored in Cosmos DB (or in-memory for development). Submission files stored in Azure Blob Storage.

## API Endpoints

- `POST /api/auth/login` - Authentication
- `GET/POST/PATCH/DELETE /api/submissions` - Document management
- `GET/POST/PATCH/DELETE /api/criteria-sets` - Criteria management
- `GET /api/criteria-templates` - Predefined templates
- `GET/POST /api/evaluations` - Evaluation CRUD
- `POST /api/evaluations/{id}/run` - Execute AI evaluation
- `GET /api/evaluations/{id}/export/{format}` - Export results (json/csv)
