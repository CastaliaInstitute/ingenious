# Ingen Prompt Tuner - User Stories Specification

## Overview

Ingen Prompt Tuner is a visual interface for inspecting, editing, and testing AI agent prompts within the Ingenious framework. It provides conversation tracing, prompt editing with syntax highlighting, and revision management.

---

## CRITICAL: Ingenious Agent Flow Hosting

**Ingen Prompt Tuner backend is the central AI orchestration hub that hosts the Ingenious agent flow.**

### Architecture Role

The Ingen Prompt Tuner backend serves two primary purposes:

1. **Prompt Management UI Backend**: Serves the frontend for editing and testing prompts
2. **Ingenious Agent Flow Host**: Runs the actual AI agent orchestration using the `ingenious` library from PyPI

### Why Prompt Tuner Hosts Ingenious

- **Single Point of AI Logic**: All AI agent orchestration runs through one service
- **Prompt-Execution Alignment**: The same service that manages prompts also executes them
- **Consistent Configuration**: Agent flows use prompts from the same revision system they manage
- **Simplified Debugging**: Trace viewing and prompt editing in one place

### Integration Pattern for Other Applications

**All applications requiring AI agent responses (e.g., SoCa) must call the Ingen Prompt Tuner backend API.**

```python
# Example: SoCa backend calling Ingen Prompt Tuner for AI evaluation
async def evaluate_with_ai(submission: Submission, criteria: CriteriaSet) -> EvaluationResult:
    response = await httpx.AsyncClient().post(
        f"{INGEN_PROMPT_TUNER_API_URL}/api/v1/chat",
        json={
            "user_prompt": build_evaluation_prompt(submission, criteria),
            "conversation_flow": "soca-evaluator",
            "thread_id": str(uuid4()),
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    return parse_evaluation_response(response.json())
```

### Required Configuration

```env
# Ingen Prompt Tuner Backend
PT_HOST=0.0.0.0
PT_PORT=8002

# Authentication
PT_AUTH_ENABLED=true
PT_JWT_SECRET=<jwt-signing-key>
PT_JWT_EXPIRE_MINUTES=1440  # 24 hours default
PT_ADMIN_EMAIL=admin@prompt-tuner.local
PT_ADMIN_PASSWORD=********

# Azure Cosmos DB (for trace persistence)
PT_COSMOS_ENDPOINT=<cosmos-endpoint>
PT_COSMOS_KEY=<cosmos-key>
PT_COSMOS_DATABASE=soca
PT_COSMOS_CONTAINER=traces

# Azure OpenAI (via Ingenious)
INGENIOUS_MODELS__0__API_KEY=<api-key>
INGENIOUS_MODELS__0__BASE_URL=https://eastus.api.cognitive.microsoft.com/
INGENIOUS_MODELS__0__MODEL=gpt-4o-mini
INGENIOUS_MODELS__0__DEPLOYMENT=gpt-4o-mini-deployment
INGENIOUS_MODELS__0__API_VERSION=2024-12-01-preview
INGENIOUS_MODELS__0__ROLE=chat

# SoCa Backend must point to Ingen Prompt Tuner
SOCA_INGENIOUS_API_URL=http://localhost:8002
```

### Trace Persistence

**Azure Cosmos DB**: All conversation traces are persisted to Cosmos DB
- One document per conversation trace
- Queryable by revision, workflow, timestamp
- Full agent chain stored with system/user prompts
- Large prompts truncated at 5000 characters
- Token usage tracked per agent

### Pre-built Prompts

The following prompt files are included by default. The SoCa evaluator uses a **6-agent pipeline** with parallel execution in Phase 1:

| Filename | Type | Agent | Jinja2 Variables |
|----------|------|-------|------------------|
| `submission_evaluator_system.md` | System | Submission Evaluator | None |
| `submission_evaluator_user.md` | User | Submission Evaluator | `submission_name`, `submission_content` |
| `criteria_evaluator_system.md` | System | Criteria Evaluator | None |
| `criteria_evaluator_user.md` | User | Criteria Evaluator | `criteria_text` |
| `next_steps_system.md` | System | Next Steps Agent | None |
| `next_steps_user.md` | User | Next Steps Agent | `submission_name`, `submission_content` |
| `scoring_agent_system.md` | System | Scoring Agent | None |
| `scoring_agent_user.md` | User | Scoring Agent | `submission_analysis`, `criteria_analysis`, `next_steps`, `criteria_text` |
| `summarizer_agent_system.md` | System | Summarizer Agent | None |
| `summarizer_agent_user.md` | User | Summarizer Agent | `scores`, `submission_name` |
| `sanity_check_system.md` | System | Sanity Check Agent | None |
| `sanity_check_user.md` | User | Sanity Check Agent | `summary`, `scores`, `criteria_text` |
| `criteria_generator_system.md` | System | Criteria Generator | None |
| `criteria_generator_user.md` | User | Criteria Generator | `document_text` |

---

## Ingenious Library Integration

**Prompt Tuner is deeply integrated with the Ingenious library and serves as its prompt management UI.**

The Ingenious library (`/ingenious/`) provides:
- Prompt template storage and versioning
- Conversation trace logging for all agent interactions
- Revision management for prompt iterations
- Agent orchestration metadata (inputs, outputs, token usage)

### Integration Requirements

1. **Prompt Storage**: Prompts are stored in Ingenious revision system
2. **Trace API**: Conversation traces retrieved via Ingenious trace endpoints
3. **Revision API**: Prompt revisions managed through Ingenious revision API
4. **Real-time Data**: Traces reflect actual Ingenious agent executions

### Required Ingenious Endpoints

```
# Trace Endpoints (NEW - must be added to Ingenious)
GET  /api/v1/traces/list           # List conversation traces
GET  /api/v1/traces/{traceId}      # Get full trace details

# Revision Endpoints (EXISTING in Ingenious)
GET  /api/v1/revisions/list        # List all revisions
POST /api/v1/revisions/create      # Create new revision
GET  /api/v1/prompts/list/{rev}    # List prompts in revision
GET  /api/v1/prompts/view/{rev}/{file}   # Get prompt content
POST /api/v1/prompts/update/{rev}/{file} # Update prompt
```

### Trace Data Structure

Ingenious must log traces in this format:
```typescript
interface ConversationTrace {
  traceId: string;
  threadId: string;
  workflow: string;        // e.g., "bike-insights", "knowledge-base"
  revision: string;        // prompt revision used
  userQuery: string;       // original user input
  timestamp: string;
  agents: AgentTrace[];    // ordered list of agent executions
  totalTokens: number;
}
```

---

## Epic 1: Authentication & Authorization

### US-1.1: User Login
**As a** user
**I want to** log in with my email and password
**So that** I can access prompt management features

**Acceptance Criteria:**
- [ ] Login page displays email and password fields
- [ ] Submit button is disabled when fields are empty
- [ ] Invalid credentials show error message "Invalid email or password"
- [ ] Successful login redirects to Home tab
- [ ] JWT token is stored in localStorage
- [ ] Token expires after configured duration (default: 24 hours)

### US-1.2: User Logout
**As a** logged-in user
**I want to** log out of the application
**So that** I can secure my session

**Acceptance Criteria:**
- [ ] Logout button visible in header when authenticated
- [ ] Clicking logout clears localStorage token
- [ ] User is redirected to login page
- [ ] All protected API calls fail after logout

### US-1.3: Session Persistence
**As a** user
**I want to** remain logged in when I refresh the page
**So that** I don't have to re-authenticate constantly

**Acceptance Criteria:**
- [ ] Valid token in localStorage auto-authenticates on page load
- [ ] Expired tokens redirect to login page
- [ ] Invalid tokens are cleared and user sees login page

### US-1.4: Protected Routes
**As a** system
**I want to** protect all application routes
**So that** unauthenticated users cannot access functionality

**Acceptance Criteria:**
- [ ] All tabs (Home, Prompts, Test) require authentication
- [ ] Direct URL access without token redirects to login
- [ ] API calls without valid token return 401

---

## Epic 2: Home Dashboard

### US-2.1: View Dashboard Statistics
**As a** user
**I want to** see an overview of prompt tuning activity
**So that** I can understand the current state

**Acceptance Criteria:**
- [ ] Stats cards display:
  - Total Revisions count
  - Total Prompt Files count
  - Test Runs count (traces)
  - Workflows count (unique workflow names)
- [ ] Stats update on page load
- [ ] Loading state shown while fetching

### US-2.2: Quick Action Links
**As a** user
**I want to** quickly navigate to common actions
**So that** I can be more productive

**Acceptance Criteria:**
- [ ] "Browse Prompts" button links to Prompts tab
- [ ] "View Traces" button links to Test tab
- [ ] Buttons styled as prominent action cards

### US-2.2.1: Workflow Visualization
**As a** user
**I want to** see a visual representation of available AI workflows
**So that** I can understand how the system processes requests

**Acceptance Criteria:**
- [ ] WorkflowDag component displays on Home page
- [ ] Shows two available workflows: SoCa Evaluator (6-agent) and Criteria Generator
- [ ] SoCa Evaluator shows detailed 6-agent pipeline visualization:
  - **Phase 1 (Parallel)**: Three agents running concurrently
    - Submission Evaluator: Analyzes submission content
    - Criteria Evaluator: Parses criteria into rubrics
    - Next Steps Agent: Identifies improvement areas
  - **Phase 2**: Scoring Agent combines Phase 1 outputs
  - **Phase 3**: Summarizer Agent creates executive summary
  - **Phase 4**: Sanity Check Agent validates consistency
- [ ] Visual representation shows:
  ```
  Input ──┬──► Submission Evaluator ──┐
          │                           │
          ├──► Criteria Evaluator ────┼──► Scoring ──► Summarizer ──► Sanity Check ──► Output
          │                           │
          └──► Next Steps Agent ──────┘
  ```
- [ ] Visual indicators for parallel execution (Phase 1) vs sequential (Phases 2-4)
- [ ] Color coding distinguishes different workflows (shiraz, taupe)
- [ ] Displays `/api/v1/chat` endpoint explanation
- [ ] Interactive hover states for workflow nodes
- [ ] Agent count badge shows "6 agents" for SoCa Evaluator
- [ ] Each agent node shows brief description on hover

### US-2.3: Recent Activity Feed
**As a** user
**I want to** see recent activity
**So that** I can track changes and tests

**Acceptance Criteria:**
- [ ] Activity feed shows last 10 activities
- [ ] Activity types: prompt edits, new revisions, test runs
- [ ] Each item shows: action, target, timestamp, user
- [ ] Clicking activity navigates to relevant item
- [ ] "View All" links to appropriate tab

---

## Epic 3: Prompt Browsing & Selection

### US-3.1: View Revisions List
**As a** user
**I want to** see all available prompt revisions
**So that** I can select which version to work with

**Acceptance Criteria:**
- [ ] Revision dropdown in Prompts tab header
- [ ] Shows all revisions from Ingenious API
- [ ] Each revision shows: name, created date, prompt count
- [ ] Sorted by created date (newest first)
- [ ] Default selection: latest revision

### US-3.2: Switch Active Revision
**As a** user
**I want to** switch between revisions
**So that** I can view and edit different prompt versions

**Acceptance Criteria:**
- [ ] Selecting revision in dropdown updates prompt grid
- [ ] Previously selected prompt is cleared
- [ ] Editor panel resets
- [ ] URL reflects selected revision (for bookmarking)

### US-3.3: View Prompt Grid
**As a** user
**I want to** see all prompts in a revision
**So that** I can choose which one to edit

**Acceptance Criteria:**
- [ ] Grid displays all prompt files in selected revision
- [ ] Each card shows: filename, description (if any), file size
- [ ] Cards styled with consistent sizing
- [ ] Empty state: "No prompts in this revision"

### US-3.4: Select Prompt for Editing
**As a** user
**I want to** click a prompt to edit it
**So that** I can modify its content

**Acceptance Criteria:**
- [ ] Clicking prompt card highlights it as selected
- [ ] Editor panel opens below grid (or side panel)
- [ ] Prompt content loaded into editor
- [ ] Only one prompt selected at a time

### US-3.5: Filter Prompts
**As a** user
**I want to** filter prompts by name or tag
**So that** I can find specific prompts quickly

**Acceptance Criteria:**
- [ ] Search input above prompt grid
- [ ] Filters by filename (partial match)
- [ ] Filters by tags (if prompts have tags)
- [ ] Results update as user types
- [ ] Clear button resets filter

---

## Epic 4: Prompt Editing

### US-4.1: View Prompt in Code Editor
**As a** user
**I want to** see the prompt content in a code editor
**So that** I can read and modify it easily

**Acceptance Criteria:**
- [ ] CodeMirror/Monaco editor displays prompt content
- [ ] Line numbers visible
- [ ] Dark theme (mine-shaft background)
- [ ] Monospace font
- [ ] Minimum height: 400px
- [ ] Resizable editor panel

### US-4.2: Jinja2 Syntax Highlighting
**As a** user
**I want to** see Jinja2 syntax highlighted
**So that** I can easily identify template elements

**Acceptance Criteria:**
- [ ] `{{ variable }}` highlighted in distinct color (yellow)
- [ ] `{% block %}` highlighted in distinct color (purple)
- [ ] `{# comment #}` highlighted in gray/italic
- [ ] Regular text in default color
- [ ] Nested syntax correctly highlighted

### US-4.3: View Extracted Variables
**As a** user
**I want to** see all variables used in a prompt
**So that** I can understand required inputs

**Acceptance Criteria:**
- [ ] Variables panel below editor
- [ ] Lists all `{{ variable }}` names found in prompt
- [ ] Variables displayed as tags/chips
- [ ] Color coding: variables vs control structures
- [ ] Clicking variable scrolls to first occurrence
- [ ] Variables update dynamically as prompt content is edited

### US-4.4: Edit Prompt Content
**As a** user
**I want to** modify the prompt text
**So that** I can improve agent behavior

**Acceptance Criteria:**
- [ ] Editor is fully editable
- [ ] Standard keyboard shortcuts work (Ctrl+Z, Ctrl+C, etc.)
- [ ] Changes tracked (hasChanges state)
- [ ] Unsaved changes indicator visible
- [ ] Tab indentation supported

### US-4.5: Save Prompt Changes
**As a** user
**I want to** save my prompt edits
**So that** they persist and can be used by agents

**Acceptance Criteria:**
- [ ] "Save" button enabled when changes exist
- [ ] Clicking Save calls Ingenious update API
- [ ] Success notification: "Prompt saved"
- [ ] hasChanges resets to false
- [ ] Error handling: "Failed to save. Please try again."

### US-4.6: Discard Prompt Changes
**As a** user
**I want to** discard my unsaved edits
**So that** I can revert to the original content

**Acceptance Criteria:**
- [ ] "Discard" button enabled when changes exist
- [ ] Confirmation dialog: "Discard unsaved changes?"
- [ ] Confirm reverts editor to original content
- [ ] Cancel keeps current edits
- [ ] hasChanges resets to false after discard

### US-4.7: Unsaved Changes Warning
**As a** user
**I want to** be warned about unsaved changes
**So that** I don't accidentally lose work

**Acceptance Criteria:**
- [ ] Switching prompts with unsaved changes shows warning
- [ ] Switching revisions with unsaved changes shows warning
- [ ] Browser tab close shows native beforeunload warning
- [ ] Warning offers: Save, Discard, Cancel

### US-4.8: Export Prompt to File
**As a** user
**I want to** export a prompt to a file
**So that** I can share or backup prompt content

**Acceptance Criteria:**
- [x] "Export" button visible when prompt is selected
- [x] Clicking export downloads prompt as .md or .jinja file
- [x] Filename matches prompt filename
- [x] Content includes current editor content (including unsaved changes)

---

## Epic 5: Configurable AI Prompts

### US-5.1: View System Prompts
**As a** user
**I want to** see all system prompts used by AI agents
**So that** I can understand how agents are configured

**Acceptance Criteria:**
- [ ] System prompts listed in the Prompts grid (tagged as "system")
- [ ] SoCa evaluator system prompt visible as `soca_evaluator_system.md`
- [ ] System prompts displayed with special "system" tag styling
- [ ] Description explains what the prompt controls

### US-5.2: Edit System Prompts
**As a** user
**I want to** edit the system prompt used by AI agents
**So that** I can customize agent behavior

**Acceptance Criteria:**
- [ ] System prompts editable in the code editor
- [ ] Changes can be saved and persisted
- [ ] Changes take effect immediately for subsequent AI calls
- [ ] Warning message explains impact of system prompt changes

### US-5.3: Preview Prompt Changes
**As a** user
**I want to** preview how my prompt changes affect AI behavior
**So that** I can validate changes before deploying

**Acceptance Criteria:**
- [ ] Test tab shows traces from both old and new prompts
- [ ] User can compare responses from different prompt versions
- [ ] Revision filter helps identify which prompt version produced each trace

### US-5.4: Structured Output Enforcement
**As a** system
**I want to** enforce JSON schema for AI responses
**So that** downstream applications receive consistent data formats

**Acceptance Criteria:**
- [ ] Chat endpoint uses OpenAI structured outputs feature
- [ ] Pydantic models define expected response schema
- [ ] AI responses guaranteed to match schema
- [ ] Error handling for edge cases

### US-5.5: Criteria Generation Flow
**As a** client application
**I want to** call a criteria-generator conversation flow
**So that** I can extract evaluation criteria from documents

**Acceptance Criteria:**
- [ ] `/api/v1/chat` accepts `conversation_flow: "criteria-generator"`
- [ ] Flow analyzes document text and extracts 3-7 criteria
- [ ] Response includes: name, description, criteria array
- [ ] Each criterion has: id, name, description, weight, maxScore
- [ ] Weights automatically sum to 100%
- [ ] Response matches CriteriaGenerationResponseSchema
- [ ] Trace recorded for criteria generation calls
- [ ] Error handling returns structured error response

### US-5.6: User Prompt Templates
**As a** administrator
**I want to** view and edit user prompt templates for SoCa
**So that** I can customize AI behavior without modifying code

**Acceptance Criteria:**
- [ ] User prompt templates appear in Prompts grid with "user" tag
- [ ] `soca_evaluator_user.md` template is editable
- [ ] `criteria_generator_user.md` template is editable
- [ ] Templates display required Jinja2 variables
- [ ] Changes are saved and take effect immediately for SoCa
- [ ] Visual distinction between system and user prompts

### US-5.7: Multi-Agent Prompt Configuration
**As a** administrator
**I want to** view and edit prompts for all 6 agents in the evaluation pipeline
**So that** I can customize each agent's behavior independently

**Acceptance Criteria:**
- [ ] 12 prompt files visible in Prompts grid (system + user for each of 6 agents)
- [ ] Each prompt tagged with agent role: `submission`, `criteria`, `nextsteps`, `scoring`, `summarizer`, `sanity`
- [ ] Tags styled distinctively for easy identification
- [ ] Variables panel shows agent-specific variables:
  - Submission Evaluator: `submission_name`, `submission_content`
  - Criteria Evaluator: `criteria_text`
  - Next Steps Agent: `submission_name`, `submission_content`
  - Scoring Agent: `submission_analysis`, `criteria_analysis`, `next_steps`, `criteria_text`
  - Summarizer Agent: `scores`, `submission_name`
  - Sanity Check Agent: `summary`, `scores`, `criteria_text`
- [ ] Changes to any agent prompt take effect immediately
- [ ] Prompt grouping/filtering by agent type available

---

## Epic 6: Revision Management

### US-6.1: Create New Revision
**As a** user
**I want to** create a new revision
**So that** I can iterate on prompts safely

**Acceptance Criteria:**
- [ ] "Create New Revision" button in Prompts tab header
- [ ] Modal prompts for revision name
- [ ] Name validation: required, alphanumeric + hyphens
- [ ] Creates revision via Ingenious API
- [ ] New revision appears in dropdown
- [ ] User automatically switched to new revision

### US-6.2: Copy Prompts to New Revision
**As a** user
**I want to** copy existing prompts to a new revision
**So that** I can start from the current state

**Acceptance Criteria:**
- [x] Checkbox: "Copy prompts from current revision"
- [x] When checked, all prompts duplicated to new revision
- [x] Original revision unchanged
- [x] New revision selected after creation

### US-6.3: View Revision Metadata
**As a** user
**I want to** see revision details
**So that** I can understand its history

**Acceptance Criteria:**
- [ ] Hovering revision in dropdown shows tooltip
- [ ] Tooltip displays: created date, prompt count, creator (if available)
- [ ] Click to select revision

---

## Epic 7: Conversation Trace Viewing

### US-6.1: View Traces List
**As a** user
**I want to** see all conversation traces
**So that** I can inspect agent behavior

**Acceptance Criteria:**
- [ ] Test tab displays list of conversation traces
- [ ] Revision dropdown filters traces by revision used
- [ ] Each trace card shows:
  - User query text (truncated if long)
  - Workflow name
  - Relative timestamp ("2m ago", "1h ago")
  - Total token count
  - Agent buttons (one per agent in trace)
- [ ] Sorted by timestamp (newest first)

### US-6.2: Filter Traces by Revision
**As a** user
**I want to** filter traces by prompt revision
**So that** I can see results for specific prompt versions

**Acceptance Criteria:**
- [ ] Revision dropdown in Test tab header
- [ ] Selecting revision filters trace list
- [ ] Option: "All Revisions" to see everything
- [ ] Empty state: "No traces for this revision"

### US-6.3: Filter Traces by Workflow
**As a** user
**I want to** filter traces by workflow name
**So that** I can focus on specific agent pipelines

**Acceptance Criteria:**
- [ ] Workflow filter dropdown (or search)
- [ ] Shows unique workflow names from traces
- [ ] Selecting workflow filters trace list
- [ ] Can combine with revision filter

### US-6.4: View Agent Buttons
**As a** user
**I want to** see which agents participated in a trace
**So that** I can understand the execution flow

**Acceptance Criteria:**
- [ ] Agent buttons displayed in upper-right of trace card
- [ ] Button labels: agent names (e.g., "Router", "SQL", "Analyst")
- [ ] Buttons styled with neutral background
- [ ] Order reflects execution order

### US-6.5: Expand Agent I/O Panel
**As a** user
**I want to** see input and output for a specific agent
**So that** I can debug agent behavior

**Acceptance Criteria:**
- [ ] Clicking agent button expands I/O panel below trace
- [ ] Clicking same button collapses panel
- [ ] Clicking different agent switches to that agent's data
- [ ] Only one agent expanded per trace at a time
- [ ] Selected agent button highlighted with accent color

### US-6.6: View Agent Input
**As a** user
**I want to** see what input an agent received
**So that** I can understand its context

**Acceptance Criteria:**
- [ ] Input panel shows full input text
- [ ] Formatted as code/preformatted text
- [ ] Scrollable if content is long
- [ ] Copy to clipboard button

### US-6.7: View Agent Output
**As a** user
**I want to** see what an agent produced
**So that** I can evaluate its response

**Acceptance Criteria:**
- [ ] Output panel shows full output text
- [ ] Formatted as code/preformatted text
- [ ] Scrollable if content is long
- [ ] Copy to clipboard button

### US-6.7.1: JSON Viewer Component
**As a** user
**I want to** view JSON data in a structured, interactive format
**So that** I can easily navigate complex nested data

**Acceptance Criteria:**
- [ ] Recursive tree view for nested objects/arrays
- [ ] Collapsible nodes for objects and arrays
- [ ] Syntax coloring for different value types (strings, numbers, booleans)
- [ ] Copy to clipboard button for any node
- [ ] Truncation for long strings (200 char limit with expand)
- [ ] Collapsed preview showing item count for arrays/objects
- [ ] Automatic JSON parsing when content is valid JSON

### US-6.7.2: Collapsible Prompt Sections
**As a** user
**I want to** expand/collapse system and user prompts in trace details
**So that** I can focus on relevant information

**Acceptance Criteria:**
- [ ] System prompt section is collapsible
- [ ] User prompt section is collapsible
- [ ] Sections default to collapsed state
- [ ] Clear visual indicator of expanded/collapsed state
- [ ] Smooth transition animation on toggle

### US-6.8: View Token Usage
**As a** user
**I want to** see token usage per agent
**So that** I can optimize prompt efficiency

**Acceptance Criteria:**
- [ ] Token count displayed per agent in I/O panel
- [ ] Total tokens shown on trace card
- [ ] Format: "1,234 tokens" (with commas)

### US-6.9: Multi-Agent Trace Visualization
**As a** user
**I want to** see all 6 agents in the trace view for SoCa evaluations
**So that** I can understand and debug the full evaluation pipeline

**Acceptance Criteria:**
- [ ] Trace card shows 6 agent buttons in execution order:
  1. Submission Evaluator
  2. Criteria Evaluator
  3. Next Steps Agent
  4. Scoring Agent
  5. Summarizer Agent
  6. Sanity Check Agent
- [ ] Phase 1 agents (Submission, Criteria, Next Steps) visually grouped or marked as parallel
- [ ] Parallel execution indicator (e.g., icon or badge) on Phase 1 agents
- [ ] Similar timestamps visible for Phase 1 agents (parallel execution evidence)
- [ ] Each agent's I/O viewable independently via button click
- [ ] Token breakdown shows per-agent usage and total
- [ ] Execution timeline visualization shows 4-phase pipeline:
  - Phase 1: Parallel input processing (3 agents)
  - Phase 2: Scoring
  - Phase 3: Summarization
  - Phase 4: Sanity Check
- [ ] Hover on agent button shows agent role description

### US-6.10: Multi-Agent Trace Storage
**As a** system
**I want to** store all 6 agent traces when an evaluation runs
**So that** the Test tab can display complete pipeline information

**Acceptance Criteria:**
- [ ] Backend stores trace with all 6 agents (not just single "SoCa Evaluator")
- [ ] Each agent trace includes: name, phase, input, output, tokens, system/user prompts
- [ ] Trace API returns full agent array for each conversation trace
- [ ] Agent order reflects execution sequence (1-6)
- [ ] Total tokens is sum of all agent tokens

---

## Epic 8: Search & Navigation

### US-7.1: Search Prompts by Content
**As a** user
**I want to** search within prompt content
**So that** I can find prompts containing specific text

**Acceptance Criteria:**
- [ ] Search input in Prompts tab
- [ ] Searches prompt content (not just filename)
- [ ] Results highlight matching prompts
- [ ] Search across current revision only

### US-7.2: Search Traces by Query
**As a** user
**I want to** search traces by user query text
**So that** I can find specific conversations

**Acceptance Criteria:**
- [ ] Search input in Test tab
- [ ] Searches userQuery field
- [ ] Partial matching supported
- [ ] Results update as user types

### US-7.3: Navigate via URL
**As a** user
**I want to** bookmark and share specific views
**So that** I can return to them later

**Acceptance Criteria:**
- [ ] URL reflects: active tab, selected revision, selected prompt
- [ ] Direct URL access loads correct state
- [ ] Browser back/forward works correctly

---

## Epic 9: Error Handling & Edge Cases

### US-8.1: Handle Ingenious API Unavailable
**As a** user
**I want to** see a clear error when Ingenious is unavailable
**So that** I understand the issue

**Acceptance Criteria:**
- [ ] Error banner: "Cannot connect to Ingenious API"
- [ ] Retry button available
- [ ] Cached data (if any) still displayed
- [ ] New operations disabled until connection restored

### US-8.2: Handle Empty Revisions
**As a** user
**I want to** see appropriate UI when a revision has no prompts
**So that** I know what to do

**Acceptance Criteria:**
- [ ] Empty state message: "No prompts in this revision"
- [ ] Suggestion to create prompts or switch revision

### US-8.3: Handle No Traces
**As a** user
**I want to** see appropriate UI when no traces exist
**So that** I know the feature is working

**Acceptance Criteria:**
- [ ] Empty state: "No conversation traces yet"
- [ ] Explanation: "Run workflows in Ingenious to see traces here"

### US-8.4: Handle Large Prompts
**As a** user
**I want to** edit large prompts without performance issues
**So that** I can work with complex templates

**Acceptance Criteria:**
- [ ] Editor handles prompts up to 100KB
- [ ] Syntax highlighting performs well
- [ ] Line numbers render correctly
- [ ] No UI freezing during edits

---

## Epic 10: Performance & Optimization

### US-9.1: Lazy Load Traces
**As a** user
**I want to** efficiently browse many traces
**So that** the app remains responsive

**Acceptance Criteria:**
- [] Initial load: 10 traces per page
- [] Pagination controls with page navigation
- [] Page size selector available (10, 25, 50)
- [] Total count displayed
- [] Smooth loading experience

### US-9.2: Cache Prompt Content
**As a** user
**I want to** quickly switch between prompts
**So that** I can compare and edit efficiently

**Acceptance Criteria:**
- [ ] Previously loaded prompts cached in memory
- [ ] Switching prompts is instant (if cached)
- [ ] Cache invalidated on save
- [ ] Cache cleared on revision change

### US-9.3: Debounced Save Indicator
**As a** user
**I want to** know when I have unsaved changes
**So that** I don't lose work

**Acceptance Criteria:**
- [ ] "Unsaved changes" indicator appears after typing
- [ ] Debounced (500ms) to avoid flicker
- [ ] Clears immediately on save/discard

---

## Non-Functional Requirements

### Security
- All API endpoints require JWT authentication
- Passwords hashed with bcrypt
- CORS configured for frontend origin only
- HTTPS required in production

### Performance
- API response time < 500ms
- Frontend bundle < 500KB gzipped (excluding CodeMirror)
- Editor responsive for files up to 100KB
- Lighthouse score > 85

### Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatible (where possible with code editor)

### Browser Support
- Chrome (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Edge (last 2 versions)

---

## Glossary

| Term | Definition |
|------|------------|
| **Prompt** | A Jinja2 template file used by Ingenious agents |
| **System Prompt** | Instructions that define AI agent behavior and constraints |
| **User Prompt** | Template for the actual request sent to the AI, with variable placeholders |
| **Revision** | A versioned snapshot of prompts for iteration and rollback |
| **Trace** | A recorded conversation including all agent I/O, prompts, and token usage |
| **Agent** | An AI component in the Ingenious orchestration pipeline |
| **Workflow** | A named sequence of agents (e.g., "soca-evaluator", "criteria-generator") |
| **Conversation Flow** | Python implementation of a workflow with agent configuration |
| **Ingenious** | The AI agent orchestration library (PyPI package) hosted by this backend |
| **Variable** | A Jinja2 placeholder like `{{ name }}` rendered at runtime |
| **Structured Output** | JSON schema enforcement for AI responses using Pydantic models |
| **Ingen Prompt Tuner** | The central AI orchestration backend that hosts Ingenious agent flows |
| **SoCa** | Submission over Criteria - an application that uses Ingen Prompt Tuner for AI evaluation |
| **CodeMirror** | The code editor component used for prompt editing with syntax highlighting |
| **JsonViewer** | Interactive tree view component for displaying JSON data |
| **Multi-Agent Pipeline** | A 6-agent orchestration flow with parallel and sequential execution phases |
| **Submission Evaluator** | Agent that analyzes submission content and extracts key claims/evidence |
| **Criteria Evaluator** | Agent that parses and interprets evaluation criteria into scoring rubrics |
| **Next Steps Agent** | Agent that identifies improvement areas and recommendations |
| **Scoring Agent** | Agent that scores submissions against criteria using outputs from Phase 1 agents |
| **Summarizer Agent** | Agent that creates executive summaries from scoring output |
| **Sanity Check Agent** | Validation agent that ensures score consistency and completeness |
| **Phase 1 (Parallel)** | First pipeline phase where Submission, Criteria, and Next Steps agents run concurrently |
| **Phase 2-4 (Sequential)** | Sequential phases: Scoring -> Summarization -> Sanity Check |
