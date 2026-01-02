# Prompt Tuner - User Stories Specification

## Overview

Prompt Tuner is a visual interface for inspecting, editing, and testing AI agent prompts within the Ingenious framework. It provides conversation tracing, prompt editing with syntax highlighting, and revision management.

---

## CRITICAL: Ingenious Library Integration

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

---

## Epic 5: Revision Management

### US-5.1: Create New Revision
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

### US-5.2: Copy Prompts to New Revision
**As a** user
**I want to** copy existing prompts to a new revision
**So that** I can start from the current state

**Acceptance Criteria:**
- [ ] Checkbox: "Copy prompts from current revision"
- [ ] When checked, all prompts duplicated to new revision
- [ ] Original revision unchanged
- [ ] New revision selected after creation

### US-5.3: View Revision Metadata
**As a** user
**I want to** see revision details
**So that** I can understand its history

**Acceptance Criteria:**
- [ ] Hovering revision in dropdown shows tooltip
- [ ] Tooltip displays: created date, prompt count, creator (if available)
- [ ] Click to select revision

---

## Epic 6: Conversation Trace Viewing

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

### US-6.8: View Token Usage
**As a** user
**I want to** see token usage per agent
**So that** I can optimize prompt efficiency

**Acceptance Criteria:**
- [ ] Token count displayed per agent in I/O panel
- [ ] Total tokens shown on trace card
- [ ] Format: "1,234 tokens" (with commas)

---

## Epic 7: Search & Navigation

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

## Epic 8: Error Handling & Edge Cases

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

## Epic 9: Performance & Optimization

### US-9.1: Lazy Load Traces
**As a** user
**I want to** efficiently browse many traces
**So that** the app remains responsive

**Acceptance Criteria:**
- [ ] Initial load: 20 traces
- [ ] "Load More" button or infinite scroll
- [ ] Smooth loading experience
- [ ] Total count displayed

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
| **Revision** | A versioned snapshot of prompts |
| **Trace** | A recorded conversation including all agent I/O |
| **Agent** | An AI component in the Ingenious orchestration pipeline |
| **Workflow** | A named sequence of agents (e.g., "bike-insights") |
| **Ingenious** | The AI agent orchestration library this tool manages |
| **Variable** | A Jinja2 placeholder like `{{ name }}` |
