# Ingen Prompt Tuner - Technical Specification

## Overview

Ingen Prompt Tuner is a Vue 3 application with a FastAPI backend that provides a visual interface for inspecting, editing, and testing AI agent prompts within the Ingenious framework. It displays conversation traces showing inputs and outputs for each agent, with the ability to edit prompts and test changes.

**CRITICAL: The backend hosts the Ingenious agent flow and serves as the central AI orchestration hub for all dependent applications (e.g., SoCa).**

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│              Ingen Prompt Tuner Frontend                     │
│                   (Vue 3 + Tailwind)                         │
│                    Port: 5174                                │
└─────────────────────────┬───────────────────────────────────┘
                          │ REST API
┌─────────────────────────▼───────────────────────────────────┐
│              Ingen Prompt Tuner Backend                      │
│                  (FastAPI + Python)                          │
│                    Port: 8002                                │
│  ┌─────────────────────────────────────────────────────────┐│
│  │           INGENIOUS AGENT FLOW HOST                      ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  ││
│  │  │ Chat API    │  │ Agent Flows │  │ Prompt Revisions│  ││
│  │  │ /api/v1/chat│  │ (AutoGen)   │  │ (Templates)     │  ││
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────┬───────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐
│  Azure OpenAI   │ │ Cosmos DB   │ │  Azure Blob     │
│  (LLM)          │ │ (Traces)    │ │  (Prompts)      │
└─────────────────┘ └─────────────┘ └─────────────────┘
                          ▲
                          │ Calls Ingen Prompt Tuner API
┌─────────────────────────┴───────────────────────────────────┐
│                    SoCa Backend                              │
│               (and other applications)                       │
│                    Port: 8001                                │
└─────────────────────────────────────────────────────────────┘
```

### Deployment Model

- **Frontend**: Vue 3 SPA served on port 5174
- **Backend**: FastAPI application on port 8002 hosting Ingenious
- **AI Orchestration**: Ingenious library (PyPI) runs within the backend
- **Authentication**: Separate auth system (not shared with dependent apps)
- **Deployment**: Local development + Azure Container Apps ready

### Ingenious Agent Flow Hosting

The backend uses the `ingenious` library from PyPI to provide:

- **Chat API** (`/api/v1/chat`): Entry point for all AI agent requests
- **Conversation Flows**: Pre-configured agent pipelines (e.g., `soca-evaluator`)
- **Prompt Templates**: Jinja2 templates managed via the UI and used by agents
- **Trace Logging**: Records all agent I/O for debugging and analysis

```python
# Backend dependency (pyproject.toml)
dependencies = [
    "ingenious",  # AI agent orchestration from PyPI
    "fastapi",
    "uvicorn",
    ...
]
```

### Client Applications

Any application requiring AI responses (e.g., SoCa) calls this backend:

```python
# In SoCa backend or any client
INGEN_PROMPT_TUNER_API_URL = "http://localhost:8002"

async def call_ai_agent(prompt: str, flow: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{INGEN_PROMPT_TUNER_API_URL}/api/v1/chat",
            json={
                "user_prompt": prompt,
                "conversation_flow": flow,
                "thread_id": str(uuid4()),
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()["response"]
```

### Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | |
| Framework | Vue 3 + Composition API |
| Language | TypeScript (strict mode) |
| Styling | Tailwind CSS |
| State Management | Pinia |
| HTTP Client | Axios or Fetch API |
| Code Editor | Monaco Editor or CodeMirror |
| Build Tool | Vite |
| **Backend** | |
| Framework | FastAPI (Python) |
| AI Orchestration | Ingenious (PyPI) |
| Language | Python 3.13+ |
| Package Manager | uv |
| Database | Cosmos DB (traces, prompts) |
| LLM Provider | Azure OpenAI |

## Navigation Structure

The application uses a simple 3-tab navigation:

| Tab | Purpose |
|-----|---------|
| **Home** | Overview with stats and recent activity |
| **Prompts** | Browse and edit prompt files by revision |
| **Test** | View conversation traces with agent I/O details |

## Core Features

### 1. Home Tab

Dashboard overview of the prompt tuning environment.

**Content**:
- Stats cards: Revisions count, Prompt files count, Test runs count, Workflows count
- Quick action links to Prompts and Test tabs
- Recent activity feed (edits, new revisions, test runs)

### 2. Prompts Tab

Browse and edit prompt templates organized by revision.

**Features**:
- Revision dropdown selector
- Grid of prompt files with metadata (filename, description, size, tags)
- Click to select a prompt for editing
- Inline code editor with Jinja2 syntax highlighting
- Variable highlighting and inspector
- Save/Discard buttons
- Create New Revision button

**UI Layout**:
```
+--------------------------------------------------+
|  Revision: [dropdown]          [Create Revision] |
+--------------------------------------------------+
|  +----------------+  +----------------+          |
|  | prompt1.jinja  |  | prompt2.jinja  |          |
|  | description    |  | description    |          |
|  +----------------+  +----------------+          |
+--------------------------------------------------+
|  Editor Panel                                    |
|  +--------------------------------------------+  |
|  |  filename.jinja          [Discard] [Save]  |  |
|  +--------------------------------------------+  |
|  |  1  You are a data analyst...              |  |
|  |  2  {{ variable }}                         |  |
|  +--------------------------------------------+  |
|  |  Variables: domain, data, include_recs     |  |
|  +--------------------------------------------+  |
+--------------------------------------------------+
```

### 3. Test Tab

View conversation traces and inspect agent inputs/outputs.

**Features**:
- Revision dropdown selector
- List of conversation runs (most recent first)
- Each run displayed as a card showing:
  - User query text
  - Workflow name, timestamp, token count
  - Agent buttons in upper-right corner
- Clicking an agent button reveals input/output panel for that agent
- Only one agent can be expanded at a time per card

**UI Layout**:
```
+--------------------------------------------------+
|  Revision: [dropdown]                            |
+--------------------------------------------------+
|  +----------------------------------------------+|
|  | What are the top selling bikes?              ||
|  | bike-insights · 2m ago · 1,234 tokens        ||
|  |                    [Router] [SQL] [Analyst]  ||
|  +----------------------------------------------+|
|  | Input                    | Output            ||
|  | User query: "What are..." | Routing to SQL...||
|  +----------------------------------------------+|
|                                                  |
|  +----------------------------------------------+|
|  | How do I configure auth?                     ||
|  | knowledge-base · 15m ago · 892 tokens        ||
|  |                              [KB Agent]      ||
|  +----------------------------------------------+|
+--------------------------------------------------+
```

**Interaction**:
- Agent buttons are styled with neutral background by default
- Clicking a button highlights it with accent color and expands the I/O panel
- Clicking the same button again collapses the panel
- Clicking a different agent button switches to that agent's data

## Data Models

### Conversation Trace

```typescript
interface ConversationTrace {
  traceId: string;
  threadId: string;
  workflow: string;
  revision: string;
  userQuery: string;
  timestamp: string;
  agents: AgentTrace[];
  totalTokens: number;
}

interface AgentTrace {
  agentName: string;
  order: number;
  input: string;
  output: string;
  tokenUsage: number;
}
```

### Prompt

```typescript
interface Prompt {
  filename: string;
  description?: string;
  content: string;
  size: number;
  tags: string[];
  variables: string[];
}

interface Revision {
  id: string;
  name: string;
  createdAt: string;
  promptCount: number;
}
```

## API Requirements

### New Endpoints Needed in Ingenious

```
GET  /api/v1/traces/list
     Query: revision, workflow, limit, offset
     Returns: List of conversation traces

GET  /api/v1/traces/{traceId}
     Returns: Full trace with all agent details
```

### Existing Endpoints Used

```
GET  /api/v1/revisions/list
GET  /api/v1/prompts/list/{revision}
GET  /api/v1/prompts/view/{revision}/{filename}
POST /api/v1/revisions/create
POST /api/v1/prompts/update/{revision}/{filename}
```

## Authentication

Prompt Tuner uses its own authentication, independent from Ingenious core auth.

**Configuration**:
```env
PROMPT_TUNER_AUTH_ENABLED=true
PROMPT_TUNER_JWT_SECRET=<secret>
PROMPT_TUNER_USERS=admin:hashedpassword
```

**Implementation**:
- Login page with username/password form
- JWT stored in localStorage
- Auth guard on all routes

## UI/UX Design

### Design Principles

- **Minimalist**: Clean, uncluttered interface with focus on content
- **White-label**: Neutral branding, easily customizable
- **Responsive**: Support for desktop, tablet, and mobile

### Brand Colors (Insight)

```css
--shiraz: #AE0A46;      /* Accent/primary actions */
--mine-shaft: #222222;  /* Primary text */
--taupe: #3E332D;       /* Secondary text */
--desert-storm: #F7F6F5; /* Background */
--white: #FFFFFF;       /* Cards/panels */
```

### Typography

- **Font**: Inter (Google Fonts)
- **Weights**: 400 (regular), 500 (medium), 600 (semibold)

### Layout Structure

```
+--------------------------------------------------+
|  [Logo] Prompt Tuner   [Home] [Prompts] [Test]   |
|                                    user@email    |
+--------------------------------------------------+
|                                                  |
|  Main Content Area                               |
|  (Tab-specific content)                          |
|                                                  |
+--------------------------------------------------+
```

### Component Styling

- **Cards**: White background, 1px gray-200 border, rounded-lg
- **Buttons**:
  - Primary: Shiraz background, white text
  - Secondary: Desert-storm background, taupe text
- **Inputs**: White background, gray-200 border, rounded-md
- **Code editor**: Mine-shaft background, monospace font

## Component Hierarchy

```
App
├── AuthGuard
│   └── MainLayout
│       ├── AppHeader
│       │   ├── Logo
│       │   ├── TabNavigation (Home, Prompts, Test)
│       │   └── UserEmail
│       └── TabContent
│           ├── HomePage
│           │   ├── StatsGrid
│           │   ├── QuickActions
│           │   └── ActivityFeed
│           ├── PromptsPage
│           │   ├── RevisionSelector
│           │   ├── PromptGrid
│           │   │   └── PromptCard
│           │   └── EditorPanel
│           │       ├── CodeEditor
│           │       └── VariableInspector
│           └── TestPage
│               ├── RevisionSelector
│               └── TraceList
│                   └── TraceCard
│                       ├── AgentButtons
│                       └── AgentIOPanel
└── LoginPage
```

## State Management (Pinia)

### Stores

```typescript
// stores/auth.ts
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

// stores/revisions.ts
interface RevisionsState {
  revisions: Revision[];
  activeRevision: string | null;
  prompts: Prompt[];
}

// stores/traces.ts
interface TracesState {
  traces: ConversationTrace[];
  loading: boolean;
}

// stores/editor.ts
interface EditorState {
  selectedPrompt: Prompt | null;
  modifiedContent: string | null;
  hasChanges: boolean;
}

// stores/ui.ts
interface UIState {
  activeTab: 'home' | 'prompts' | 'test';
  expandedAgent: { traceId: string; agentName: string } | null;
}
```

## File Structure

```
ingen-prompt-tuner/
├── frontend/
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── assets/
│   │   │   └── styles/
│   │   │       └── tailwind.css
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Button.vue
│   │   │   │   ├── Card.vue
│   │   │   │   └── Dropdown.vue
│   │   │   ├── layout/
│   │   │   │   ├── AppHeader.vue
│   │   │   │   └── TabNavigation.vue
│   │   │   ├── home/
│   │   │   │   ├── StatsGrid.vue
│   │   │   │   └── ActivityFeed.vue
│   │   │   ├── prompts/
│   │   │   │   ├── PromptGrid.vue
│   │   │   │   ├── PromptCard.vue
│   │   │   │   └── EditorPanel.vue
│   │   │   └── test/
│   │   │       ├── TraceList.vue
│   │   │       ├── TraceCard.vue
│   │   │       └── AgentIOPanel.vue
│   │   ├── stores/
│   │   │   ├── auth.ts
│   │   │   ├── revisions.ts
│   │   │   ├── traces.ts
│   │   │   ├── editor.ts
│   │   │   └── ui.ts
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── traces.service.ts
│   │   │   └── prompts.service.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.vue
│   │   └── main.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── backend/
│   ├── src/
│   │   └── ingen_prompt_tuner/
│   │       ├── __init__.py
│   │       ├── main.py          # FastAPI app + Ingenious chat API
│   │       ├── config.py
│   │       ├── models.py
│   │       ├── auth/
│   │       ├── prompts/
│   │       └── traces/
│   ├── pyproject.toml           # Includes ingenious>=0.2.8
│   └── Dockerfile
├── spec.md
└── tech-specs.md
```

## Tailwind Configuration

```javascript
// tailwind.config.js
module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {
      colors: {
        shiraz: '#AE0A46',
        mine: '#222222',
        taupe: '#3E332D',
        desert: '#F7F6F5',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

## Docker Configuration

```dockerfile
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Environment Configuration

### Frontend
```env
VITE_API_BASE_URL=http://localhost:8002
VITE_AUTH_ENABLED=true
```

### Backend
```env
# Server Configuration
INGEN_PROMPT_TUNER_PORT=8002
INGEN_PROMPT_TUNER_JWT_SECRET=<secret>

# Ingenious Configuration (inherited from INGENIOUS_* env vars)
INGENIOUS_MODELS__0__API_KEY=<your-azure-openai-key>
INGENIOUS_MODELS__0__BASE_URL=https://eastus.api.cognitive.microsoft.com/
INGENIOUS_MODELS__0__MODEL=gpt-4o-mini
INGENIOUS_MODELS__0__API_VERSION=2024-12-01-preview
INGENIOUS_MODELS__0__DEPLOYMENT=gpt-4o-mini-deployment
INGENIOUS_MODELS__0__API_TYPE=rest
INGENIOUS_MODELS__0__ROLE=chat

# Database
COSMOS_URI=<cosmos-uri>
COSMOS_KEY=<cosmos-key>
COSMOS_DATABASE=ingen-prompt-tuner
```

## Development Workflow

### Frontend
```bash
cd ingen-prompt-tuner/frontend
npm install
npm run dev        # Start dev server on port 5174
npm run build      # Production build
npm run lint       # Run ESLint
npm run typecheck  # Run TypeScript checks
```

### Backend
```bash
cd ingen-prompt-tuner/backend
uv sync            # Install dependencies (including ingenious from PyPI)
uv run uvicorn ingen_prompt_tuner.main:app --host 0.0.0.0 --port 8002 --reload
```

## Backend API Endpoints

### Ingen Prompt Tuner API

```
# Authentication
POST /api/auth/login
GET  /api/auth/me

# Prompt Management
GET  /api/v1/revisions/list
POST /api/v1/revisions/create
GET  /api/v1/prompts/list/{revision}
GET  /api/v1/prompts/view/{revision}/{filename}
POST /api/v1/prompts/update/{revision}/{filename}

# Trace Management
GET  /api/v1/traces/list
GET  /api/v1/traces/{traceId}

# Ingenious Chat API (for client applications like SoCa)
POST /api/v1/chat   # Main entry point for AI agent requests
```

### Chat API Request Format

```python
# POST /api/v1/chat
{
    "user_prompt": "Evaluate this submission against the criteria...",
    "conversation_flow": "soca-evaluator",  # Or other configured flows
    "thread_id": "unique-conversation-id",
    "revision": "v1.0"  # Optional: specific prompt revision to use
}
```

### Chat API Response Format

```python
{
    "response": "Evaluation complete. The submission scores...",
    "trace_id": "trace-uuid",
    "tokens_used": 1234,
    "agents": ["Router", "Evaluator", "Summarizer"]
}
```

## Testing Strategy

- **Unit Tests**: Vitest + Vue Test Utils for components
- **E2E Tests**: Playwright for key flows
- **Coverage Target**: 80%

## Future Enhancements

1. **Regenerate testing**: Test modified prompts against historical inputs
2. **Prompt versioning**: Track changes over time
3. **Prompt comparison**: Diff view between revisions
4. **Analytics**: Aggregate metrics across traces
