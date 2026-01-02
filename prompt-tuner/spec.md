# Prompt Tuner - Technical Specification

## Overview

Prompt Tuner is a Vue 3 application that provides a visual interface for inspecting, editing, and testing AI agent prompts within the Ingenious framework. It displays conversation traces showing inputs and outputs for each agent, with the ability to edit prompts and test changes.

## Architecture

### Deployment Model

- **Serving**: Static files served from Ingenious (e.g., `/prompt-tuner/*`)
- **Backend**: Ingenious API (existing endpoints + new trace endpoints)
- **Authentication**: Separate auth system (not shared with Ingenious core)
- **Deployment**: Local development + Azure Container Apps ready

### Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Vue 3 + Composition API |
| Language | TypeScript (strict mode) |
| Styling | Tailwind CSS |
| State Management | Pinia |
| HTTP Client | Axios or Fetch API |
| Code Editor | Monaco Editor or CodeMirror |
| Build Tool | Vite |

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
prompt-tuner/
├── public/
│   └── favicon.ico
├── src/
│   ├── assets/
│   │   └── styles/
│   │       └── tailwind.css
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.vue
│   │   │   ├── Card.vue
│   │   │   └── Dropdown.vue
│   │   ├── layout/
│   │   │   ├── AppHeader.vue
│   │   │   └── TabNavigation.vue
│   │   ├── home/
│   │   │   ├── StatsGrid.vue
│   │   │   └── ActivityFeed.vue
│   │   ├── prompts/
│   │   │   ├── PromptGrid.vue
│   │   │   ├── PromptCard.vue
│   │   │   └── EditorPanel.vue
│   │   └── test/
│   │       ├── TraceList.vue
│   │       ├── TraceCard.vue
│   │       └── AgentIOPanel.vue
│   ├── stores/
│   │   ├── auth.ts
│   │   ├── revisions.ts
│   │   ├── traces.ts
│   │   ├── editor.ts
│   │   └── ui.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.service.ts
│   │   ├── traces.service.ts
│   │   └── prompts.service.ts
│   ├── types/
│   │   └── index.ts
│   ├── App.vue
│   └── main.ts
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
└── Dockerfile
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

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_AUTH_ENABLED=true
```

## Development Workflow

```bash
cd prompt-tuner
npm install
npm run dev        # Start dev server on port 5173
npm run build      # Production build
npm run lint       # Run ESLint
npm run typecheck  # Run TypeScript checks
```

## Integration with Ingenious

Ingenious serves the built static files:

```python
# In Ingenious app_factory.py
from fastapi.staticfiles import StaticFiles

app.mount("/prompt-tuner", StaticFiles(
    directory="static/prompt-tuner",
    html=True
), name="prompt-tuner")
```

## Testing Strategy

- **Unit Tests**: Vitest + Vue Test Utils for components
- **E2E Tests**: Playwright for key flows
- **Coverage Target**: 80%

## Mock UI Files

The following HTML mockups demonstrate the UI design:

| File | Description |
|------|-------------|
| `home.html` | Home tab with stats and recent activity |
| `prompt-editor.html` | Prompts tab with file grid and code editor |
| `main-dashboard.html` | Test tab with revision selector and run list with agent buttons |

To view the mocks, open any HTML file in a browser:
```bash
open prompt-tuner/home.html
```

## Future Enhancements

1. **Regenerate testing**: Test modified prompts against historical inputs
2. **Prompt versioning**: Track changes over time
3. **Prompt comparison**: Diff view between revisions
4. **Analytics**: Aggregate metrics across traces
