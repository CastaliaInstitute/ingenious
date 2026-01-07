# SoCa (Submission over Criteria) - Technical Specification

## Overview

SoCa is a standalone application for evaluating submissions against weighted criteria using AI-powered analysis. Users upload documents (PDF, text, or other formats), define evaluation criteria with weights and scoring scales, and receive detailed scores with narrative justifications for each submission.

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     SoCa Frontend                           │
│                   (Vue 3 + Tailwind)                        │
│                     Port: 5173                              │
└─────────────────────────┬───────────────────────────────────┘
                          │ REST API
┌─────────────────────────▼───────────────────────────────────┐
│                     SoCa Backend                            │
│                   (FastAPI + Python)                        │
│                     Port: 8001                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Auth Service│  │ Eval Service│  │ Storage Service     │  │
│  └─────────────┘  └──────┬──────┘  └─────────────────────┘  │
└──────────────────────────┼──────────────────────────────────┘
                           │ REST API Call
                           │ /api/v1/chat
┌──────────────────────────▼──────────────────────────────────┐
│              Ingen Prompt Tuner Backend                      │
│           (Hosts Ingenious Agent Orchestration)              │
│                     Port: 8002                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  INGENIOUS LIBRARY (from PyPI)                          ││
│  │  - Multi-agent orchestration                            ││
│  │  - Conversation flows (e.g., soca-evaluator)            ││
│  │  - Prompt template management                           ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐
│  Azure Blob     │ │ Cosmos DB   │ │ Azure OpenAI    │
│  (Submissions)  │ │ (SoCa Data) │ │ (LLM)           │
└─────────────────┘ └─────────────┘ └─────────────────┘
```

### Deployment Model

- **Frontend**: Vue 3 SPA served on port 5173
- **Backend**: FastAPI application on port 8001
- **AI Orchestration**: Calls Ingen Prompt Tuner backend (port 8002) for AI evaluation
- **Data Storage**: Cosmos DB (separate database from Ingen Prompt Tuner)
- **File Storage**: Azure Blob Storage (dedicated container)
- **Deployment**: Local development + Azure Container Apps ready

### Why SoCa Does NOT Use Ingenious Directly

SoCa delegates all AI operations to Ingen Prompt Tuner because:

1. **Centralized Prompt Management**: Prompts are managed in Ingen Prompt Tuner, so agent flows should execute there
2. **Trace Visibility**: All traces appear in Ingen Prompt Tuner UI for debugging
3. **Single AI Configuration**: Azure OpenAI credentials only configured once
4. **Separation of Concerns**: SoCa focuses on document/criteria management

### Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend Framework | Vue 3 + Composition API |
| Language | TypeScript (strict mode) |
| Styling | Tailwind CSS |
| State Management | Pinia |
| Backend Framework | FastAPI (Python) |
| Database | Azure Cosmos DB (separate from Ingenious) |
| File Storage | Azure Blob Storage |
| Agent Backend | Ingenious API |
| Build Tool | Vite (frontend), uv (backend) |

## Navigation Structure

The application uses a simple 3-tab navigation:

| Tab | Purpose |
|-----|---------|
| **Evaluations** | List and manage evaluation sessions |
| **Submissions** | Upload and manage documents |
| **Criteria** | Define and manage evaluation criteria |

## Core Features

### 1. Evaluations Tab (Main View)

List and manage evaluation sessions.

**Content**:
- Stats cards: Completed, In Progress, Total Submissions
- List of evaluations with status badges
- Click to view evaluation results
- "New Evaluation" button

**Evaluation List Item**:
- Evaluation name
- Submission count and criteria set name
- Status badge (Completed/In Progress)
- Timestamp

### 2. Evaluation Results View

Display ranked results with expandable details.

**Layout**:
```
+--------------------------------------------------+
|  [Back] Evaluation Name                  [Export] |
|  5 submissions · Grant Proposal Criteria          |
+--------------------------------------------------+
|  +------------------+  +------------------+       |
|  | 78.4 Avg Score   |  | 92.5 Highest    |       |
|  +------------------+  +------------------+       |
+--------------------------------------------------+
|  Results List                                     |
|  +----------------------------------------------+|
|  | [1] Quantum Computing for Drug Discovery     ||
|  |     Dr. Sarah Chen et al.           92.5/100 ||
|  |                                          [v] ||
|  +----------------------------------------------+|
|  | Criteria Breakdown (expanded)                ||
|  | Scientific: 4.8  Innovation: 4.7  Method: 4.5||
|  | Summary: Exceptional proposal...             ||
|  +----------------------------------------------+|
+--------------------------------------------------+
```

**Features**:
- Click row to expand/collapse criteria breakdown
- Scores per criterion with labels
- AI-generated summary narrative
- Export button (PDF, CSV, JSON)

### 3. Submissions Tab

Upload and manage documents for evaluation.

**Supported Formats**:
- PDF, TXT, MD, DOCX, RTF

**Features**:
- Drag-and-drop upload
- Batch upload (multiple files)
- List of submissions with metadata
- Delete submissions

### 4. Criteria Tab

Define evaluation criteria sets.

**Features**:
- List of saved criteria sets
- Pre-built templates gallery
- Criteria builder with:
  - Criterion name and description
  - Weight slider (0-100%)
  - Scoring scale (1-5 or 1-10)

## Data Models

### Submission

```typescript
interface Submission {
  id: string;
  name: string;
  description?: string;
  fileUrl: string;
  fileName: string;
  fileType: string;
  fileSize: number;
  extractedText: string;
  uploadedAt: string;
}
```

### Criteria Set

```typescript
interface CriteriaSet {
  id: string;
  name: string;
  description?: string;
  criteria: Criterion[];
  createdAt: string;
}

interface Criterion {
  id: string;
  name: string;
  description: string;
  weight: number;        // 0-100, all should sum to 100
  maxScore: number;      // e.g., 5 or 10
}
```

### Evaluation

```typescript
interface Evaluation {
  id: string;
  name: string;
  status: 'draft' | 'running' | 'completed' | 'failed';
  submissionIds: string[];
  criteriaSetId: string;
  results: EvaluationResult[];
  createdAt: string;
  completedAt?: string;
}

interface EvaluationResult {
  submissionId: string;
  overallScore: number;
  criterionResults: CriterionResult[];
  summary: string;
}

interface CriterionResult {
  criterionId: string;
  score: number;
  narrative: string;
}
```

## Pre-built Criteria Templates

1. **Grant Proposal Evaluation**
   - Scientific Merit (25%)
   - Innovation (20%)
   - Methodology (20%)
   - Team Qualifications (15%)
   - Budget Justification (10%)
   - Broader Impact (10%)

2. **RFP Response Evaluation**
   - Technical Approach (30%)
   - Relevant Experience (25%)
   - Cost Effectiveness (20%)
   - Timeline Feasibility (15%)
   - Risk Mitigation (10%)

3. **Code Review Criteria**
   - Correctness (30%)
   - Code Quality (25%)
   - Performance (20%)
   - Documentation (15%)
   - Test Coverage (10%)

4. **Academic Paper Review**
   - Originality (25%)
   - Significance (20%)
   - Technical Quality (25%)
   - Clarity (15%)
   - References (15%)

## API Design

### SoCa Backend API

```
# Authentication
POST /api/auth/login
GET  /api/auth/me

# Submissions
GET    /api/submissions
POST   /api/submissions
DELETE /api/submissions/{id}

# Criteria
GET    /api/criteria-sets
POST   /api/criteria-sets
GET    /api/criteria-templates

# Evaluations
GET    /api/evaluations
POST   /api/evaluations
GET    /api/evaluations/{id}
POST   /api/evaluations/{id}/run
GET    /api/evaluations/{id}/export/{format}
```

### Integration with Ingen Prompt Tuner

SoCa backend calls **Ingen Prompt Tuner API** for AI-powered evaluation (NOT the Ingenious library directly):

```python
import httpx
from uuid import uuid4

INGEN_PROMPT_TUNER_API_URL = os.getenv("INGEN_PROMPT_TUNER_API_URL", "http://localhost:8002")

async def evaluate_submission(
    submission: Submission,
    criteria: CriteriaSet
) -> EvaluationResult:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{INGEN_PROMPT_TUNER_API_URL}/api/v1/chat",
            json={
                "user_prompt": build_evaluation_prompt(submission, criteria),
                "conversation_flow": "soca-evaluator",
                "thread_id": str(uuid4()),
            },
            headers={"Authorization": f"Bearer {ingen_prompt_tuner_token}"}
        )
        return parse_evaluation_response(response.json())
```

## Authentication

SoCa has its own authentication, independent from Ingenious.

**Configuration**:
```env
SOCA_AUTH_ENABLED=true
SOCA_JWT_SECRET=<secret>
SOCA_ADMIN_USER=admin
SOCA_ADMIN_PASSWORD=<hashed>
```

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
|  [Logo] SoCa   [Evaluations] [Submissions] [Criteria]
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
- **Status Badges**:
  - Completed: Green background
  - In Progress: Amber background
- **Score Colors**:
  - High (80+): Green
  - Medium (60-79): Amber
  - Low (<60): Orange

## Component Hierarchy

```
App
├── AuthGuard
│   └── MainLayout
│       ├── AppHeader
│       │   ├── Logo
│       │   ├── TabNavigation (Evaluations, Submissions, Criteria)
│       │   └── UserEmail
│       └── TabContent
│           ├── EvaluationsPage
│           │   ├── StatsGrid
│           │   ├── EvaluationList
│           │   │   └── EvaluationCard
│           │   └── NewEvaluationButton
│           ├── EvaluationResultsPage
│           │   ├── SummaryStats
│           │   ├── ResultsList
│           │   │   └── ResultCard (expandable)
│           │   └── ExportButton
│           ├── SubmissionsPage
│           │   ├── UploadDropzone
│           │   └── SubmissionList
│           └── CriteriaPage
│               ├── CriteriaSetList
│               ├── TemplateGallery
│               └── CriteriaBuilder
└── LoginPage
```

## State Management (Pinia)

```typescript
// stores/auth.ts
interface AuthState {
  user: User | null;
  token: string | null;
}

// stores/evaluations.ts
interface EvaluationsState {
  evaluations: Evaluation[];
  activeEvaluation: Evaluation | null;
  loading: boolean;
}

// stores/submissions.ts
interface SubmissionsState {
  submissions: Submission[];
  uploadProgress: number | null;
}

// stores/criteria.ts
interface CriteriaState {
  criteriaSets: CriteriaSet[];
  templates: CriteriaSet[];
}

// stores/ui.ts
interface UIState {
  activeTab: 'evaluations' | 'submissions' | 'criteria';
  expandedResultId: string | null;
}
```

## File Structure

### Frontend

```
soca/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── layout/
│   │   │   ├── evaluations/
│   │   │   ├── submissions/
│   │   │   └── criteria/
│   │   ├── stores/
│   │   ├── services/
│   │   ├── types/
│   │   ├── App.vue
│   │   └── main.ts
│   ├── package.json
│   ├── tailwind.config.js
│   └── Dockerfile
└── backend/
    ├── src/
    │   └── soca/
    │       ├── main.py
    │       ├── auth/
    │       ├── submissions/
    │       ├── criteria/
    │       ├── evaluations/
    │       └── db/
    ├── pyproject.toml
    └── Dockerfile
```

## Tailwind Configuration

```javascript
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

### Frontend
```dockerfile
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Backend
```dockerfile
FROM python:3.13-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml .
RUN uv sync --frozen
COPY src/ src/
EXPOSE 8001
CMD ["uv", "run", "uvicorn", "soca.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

## Environment Configuration

### Frontend
```env
VITE_API_BASE_URL=http://localhost:8001
VITE_AUTH_ENABLED=true
```

### Backend
```env
# SoCa Server Configuration
SOCA_PORT=8001
SOCA_AUTH_ENABLED=true
SOCA_JWT_SECRET=<secret>

# Database (Cosmos DB)
SOCA_COSMOS_URI=https://soca-cosmos.documents.azure.com:443/
SOCA_COSMOS_KEY=<key>
SOCA_COSMOS_DATABASE=soca

# File Storage (Azure Blob)
AZURE_STORAGE_CONNECTION_STRING=<connection-string>

# Ingen Prompt Tuner Integration (REQUIRED for AI evaluation)
INGEN_PROMPT_TUNER_API_URL=http://localhost:8002
INGEN_PROMPT_TUNER_API_KEY=<shared-api-key>
```

## Export Formats

- **PDF Report**: Formatted document with rankings and narratives
- **CSV/Excel**: Spreadsheet with all scores
- **JSON**: Machine-readable complete export

## Testing Strategy

- **Unit Tests**: Vitest (frontend), pytest (backend)
- **E2E Tests**: Playwright
- **Coverage Target**: 80%
