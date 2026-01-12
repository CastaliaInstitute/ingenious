# SoCa (Submission over Criteria) - User Stories Specification

## Overview

SoCa is a document evaluation application that uses AI to score submissions against weighted criteria. This specification defines all user stories required for a complete implementation.

---

## CRITICAL: Ingen Prompt Tuner Integration

**SoCa MUST call the Ingen Prompt Tuner backend for all AI-powered evaluation functionality.**

### Architecture Overview

SoCa does NOT directly use the Ingenious library. Instead, it calls the **Ingen Prompt Tuner backend**, which hosts the Ingenious agent flow.

```
┌─────────────────────┐       ┌──────────────────────────────┐
│   SoCa Frontend     │       │  Ingen Prompt Tuner Backend  │
│   (Vue 3)           │       │  (Hosts Ingenious Agent Flow)│
└─────────┬───────────┘       │  Port: 8002                  │
          │                   └──────────────┬───────────────┘
          ▼                                  │
┌─────────────────────┐                      ▼
│   SoCa Backend      │  ─────────────►  Azure OpenAI
│   (FastAPI)         │  REST API Call   (via Ingenious)
│   Port: 8001        │  /api/v1/chat
└─────────────────────┘
```

### Why SoCa Calls Ingen Prompt Tuner

- **Centralized AI Orchestration**: All AI logic lives in one service
- **Prompt Management**: Ingen Prompt Tuner manages prompts used for evaluation
- **Trace Visibility**: All evaluation traces visible in Ingen Prompt Tuner UI
- **Separation of Concerns**: SoCa focuses on submission/criteria management, not AI

### Integration Requirements

1. **API Communication**: SoCa backend calls Ingen Prompt Tuner API (`/api/v1/chat`)
2. **Conversation Flow**: Use `soca-evaluator` conversation flow for structured evaluation
3. **Environment Variables**: Configure `INGEN_PROMPT_TUNER_API_URL`
4. **Error Handling**: Gracefully handle API failures with user-friendly messages

### Example Integration Pattern

```python
# SoCa backend calling Ingen Prompt Tuner for AI evaluation
import httpx
from uuid import uuid4

INGEN_PROMPT_TUNER_API_URL = "http://localhost:8002"

async def evaluate_with_ai(submission: Submission, criteria: CriteriaSet) -> EvaluationResult:
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
        return parse_structured_response(response.json())
```

### Required Configuration

```env
# SoCa Backend
SOCA_PORT=8001

# Ingen Prompt Tuner API (where SoCa sends AI requests)
INGEN_PROMPT_TUNER_API_URL=http://localhost:8002
INGEN_PROMPT_TUNER_API_KEY=<shared-api-key>
```

---

## Epic 1: Authentication & Authorization

### US-1.1: User Login
**As a** user
**I want to** log in with my email and password
**So that** I can access the application securely

**Acceptance Criteria:**
- [ ] Login page displays email and password fields
- [ ] Submit button is disabled when fields are empty
- [ ] Invalid credentials show error message "Invalid email or password"
- [ ] Successful login redirects to Evaluations tab
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
- [ ] All tabs require authentication
- [ ] Direct URL access without token redirects to login
- [ ] API calls without valid token return 401

---

## Epic 2: Submissions Management

### US-2.1: View Submissions List
**As a** user
**I want to** see all my uploaded submissions
**So that** I can manage my documents

**Acceptance Criteria:**
- [ ] Submissions tab shows list of all uploaded documents
- [ ] Each submission displays: name, file type icon, file size, upload date
- [ ] List is sorted by upload date (newest first)
- [ ] Empty state shows "No submissions yet" with upload prompt

### US-2.2: Upload Single Submission
**As a** user
**I want to** upload a document for evaluation
**So that** it can be scored against criteria

**Acceptance Criteria:**
- [ ] Drag-and-drop zone accepts files
- [ ] Click to browse files works
- [ ] Supported formats: PDF, TXT, MD, DOCX, RTF
- [ ] Unsupported formats show error message
- [ ] Upload progress indicator displays
- [ ] Success message confirms upload completion
- [ ] New submission appears in list immediately

### US-2.3: Batch Upload Submissions
**As a** user
**I want to** upload multiple documents at once
**So that** I can efficiently add many submissions

**Acceptance Criteria:**
- [ ] Multiple files can be selected or dropped
- [ ] Each file shows individual progress
- [ ] Failed uploads don't block successful ones
- [ ] Summary shows success/failure count after batch completes

### US-2.4: Delete Submission
**As a** user
**I want to** delete a submission
**So that** I can remove unwanted documents

**Acceptance Criteria:**
- [ ] Delete button visible on each submission item
- [ ] Confirmation dialog asks "Delete [filename]?"
- [ ] Successful deletion removes item from list
- [ ] Cannot delete submissions used in running evaluations

### US-2.5: View Submission Details
**As a** user
**I want to** view details of a submission
**So that** I can verify its content

**Acceptance Criteria:**
- [ ] Click submission to see detail panel
- [ ] Shows: filename, description, file type, size, upload date
- [ ] Displays extracted text preview (first 500 characters)
- [ ] Download original file button works

### US-2.6: Edit Submission Metadata
**As a** user
**I want to** edit the name and description of a submission
**So that** I can organize my documents better

**Acceptance Criteria:**
- [ ] Edit button opens inline edit mode
- [ ] Can modify name and description fields
- [ ] Save commits changes
- [ ] Cancel discards changes
- [ ] Validation prevents empty name

---

## Epic 3: Criteria Management

### US-3.1: View Criteria Sets
**As a** user
**I want to** see my saved criteria sets
**So that** I can reuse evaluation criteria

**Acceptance Criteria:**
- [ ] Criteria tab shows list of saved criteria sets
- [ ] Each set displays: name, description, number of criteria, created date
- [ ] Empty state shows templates gallery prominently

### US-3.2: View Criteria Templates
**As a** user
**I want to** browse pre-built criteria templates
**So that** I can quickly start evaluating

**Acceptance Criteria:**
- [ ] Templates section shows 4 pre-built templates:
  - Grant Proposal Evaluation
  - RFP Response Evaluation
  - Code Review Criteria
  - Academic Paper Review
- [ ] Each template shows name and brief description
- [ ] Clicking template shows full criteria breakdown

### US-3.3: Use Template as Starting Point
**As a** user
**I want to** create a criteria set from a template
**So that** I can customize it for my needs

**Acceptance Criteria:**
- [ ] "Use Template" button on each template
- [ ] Opens criteria builder pre-filled with template values
- [ ] User can modify before saving
- [ ] Saved as new criteria set (template unchanged)

### US-3.4: Create Custom Criteria Set
**As a** user
**I want to** create my own criteria set from scratch
**So that** I can define custom evaluation criteria

**Acceptance Criteria:**
- [ ] "New Criteria Set" button opens builder modal
- [ ] Name field (required)
- [ ] Description field (optional)
- [ ] Add criterion button creates new criterion row
- [ ] Each criterion has: name, description, weight (0-100%), max score (1-5 or 1-10)
- [ ] Weight sliders show real-time percentage
- [ ] Total weight must equal 100% to save
- [ ] Validation error if weights don't sum to 100%

### US-3.5: Edit Criteria Set
**As a** user
**I want to** modify an existing criteria set
**So that** I can refine my evaluation criteria

**Acceptance Criteria:**
- [ ] Edit button opens builder with existing values
- [ ] All fields editable
- [ ] Can add/remove criteria
- [ ] Changes saved on submit
- [ ] Cannot edit criteria sets used in running evaluations

### US-3.6: Delete Criteria Set
**As a** user
**I want to** delete a criteria set
**So that** I can remove unused criteria

**Acceptance Criteria:**
- [ ] Delete button with confirmation dialog
- [ ] Cannot delete criteria sets used in any evaluation
- [ ] Error message explains if deletion blocked

### US-3.7: Reorder Criteria
**As a** user
**I want to** reorder criteria within a set
**So that** I can control display priority

**Acceptance Criteria:**
- [ ] Drag handles on each criterion row
- [ ] Drag-and-drop reorders criteria
- [ ] Order persists on save

### US-3.8: Generate Criteria from Document
**As a** user
**I want to** generate evaluation criteria from an unstructured document
**So that** I can quickly create relevant criteria without manual definition

**Acceptance Criteria:**
- [ ] "Generate from Document" button visible on Criteria page
- [ ] Modal supports file upload (PDF, DOCX, TXT)
- [ ] Modal supports text paste as alternative input
- [ ] Name field required before generation
- [ ] Loading state shown during AI processing
- [ ] Generated criteria saved directly to criteria sets
- [ ] New criteria set appears in list after generation
- [ ] User can edit generated criteria via normal edit flow
- [ ] Error message shown if generation fails

### US-3.9: Configurable Criteria Generation Prompts
**As a** administrator
**I want to** customize the AI criteria generation prompt via Prompt Tuner
**So that** I can fine-tune how criteria are extracted from documents

**Acceptance Criteria:**
- [ ] SoCa fetches criteria generator template from Prompt Tuner API
- [ ] Template uses Jinja2 variable: `document_text`
- [ ] Template can be edited in Prompt Tuner UI
- [ ] Falls back to default template if Prompt Tuner unavailable
- [ ] Template changes take effect on next generation request

---

## Epic 4: Evaluation Workflow

### US-4.1: View Evaluations Dashboard
**As a** user
**I want to** see an overview of all my evaluations
**So that** I can track their status

**Acceptance Criteria:**
- [ ] Evaluations tab is the default landing page
- [ ] Stats cards show: Completed count, In Progress count, Total Submissions
- [ ] List shows all evaluations with: name, submission count, criteria set name, status badge, timestamp
- [ ] Status badges: Draft (gray), Running (amber), Completed (green), Failed (red)
- [ ] Sorted by created date (newest first)

### US-4.2: Create New Evaluation
**As a** user
**I want to** create a new evaluation
**So that** I can score submissions against criteria

**Acceptance Criteria:**
- [ ] "New Evaluation" button opens modal
- [ ] Name field (required)
- [ ] Submission multi-select (at least 1 required)
- [ ] Criteria set dropdown (required)
- [ ] Create button saves evaluation in Draft status
- [ ] Cancel closes modal without saving

### US-4.3: Run Evaluation
**As a** user
**I want to** run an evaluation
**So that** the AI can score my submissions

**Acceptance Criteria:**
- [ ] "Run" button visible on Draft evaluations
- [ ] Clicking Run changes status to "Running"
- [ ] Progress indicator shows during processing
- [ ] **CRITICAL**: Backend calls Ingenious API for each submission
- [ ] Each submission evaluated against all criteria
- [ ] AI generates score (1-5 or 1-10) per criterion
- [ ] AI generates narrative justification per criterion
- [ ] AI generates overall summary per submission
- [ ] Overall score calculated as weighted average
- [ ] Status changes to "Completed" when done
- [ ] Status changes to "Failed" if Ingenious API errors

### US-4.3.1: Configurable Evaluation Prompts
**As a** administrator
**I want to** customize the AI evaluation prompt via Prompt Tuner
**So that** I can fine-tune how submissions are evaluated without code changes

**Acceptance Criteria:**
- [ ] SoCa fetches user prompt template from Prompt Tuner API
- [ ] Template uses Jinja2 variables: `submission_name`, `submission_content`, `criteria_text`
- [ ] Template can be edited in Prompt Tuner UI
- [ ] Falls back to default template if Prompt Tuner unavailable
- [ ] Template changes take effect on next evaluation run

### US-4.4: View Evaluation Results
**As a** user
**I want to** view the results of a completed evaluation
**So that** I can see how submissions ranked

**Acceptance Criteria:**
- [ ] Click completed evaluation to view results
- [ ] Header shows: evaluation name, submission count, criteria set name
- [ ] Stats cards show: Average Score, Highest Score
- [ ] Results list shows submissions ranked by overall score
- [ ] Each result displays: rank badge, submission name, overall score
- [ ] Color coding: 80+ green, 60-79 amber, <60 orange

### US-4.5: Expand Result Details
**As a** user
**I want to** see detailed breakdown for each result
**So that** I can understand the scoring

**Acceptance Criteria:**
- [ ] Click result row to expand/collapse details
- [ ] Expanded view shows score per criterion
- [ ] Each criterion displays: name, score, narrative justification
- [ ] Overall AI-generated summary at bottom
- [ ] Only one result expanded at a time

### US-4.5.1: Multi-Submission Evaluation Test Cases
**As a** tester
**I want to** verify evaluations work correctly with multiple submissions
**So that** I can ensure the ranking and comparison features work as expected

**Test Cases:**

**TC-4.5.1-A: Create Evaluation with 3+ Submissions**
- [x] Upload at least 3 distinct submission files with varying content quality
- [x] Create a new evaluation selecting all 3+ submissions
- [x] Select a criteria set with multiple weighted criteria
- [x] Run the evaluation successfully
- [x] Verify all submissions are evaluated and ranked

**TC-4.5.1-B: Ranking Accuracy**
- [x] Results should be sorted by overall score (highest first)
- [x] Rank badges should show correct position (1, 2, 3, etc.)
- [x] Submissions with similar scores should have distinct rankings
- [x] Score distribution should reflect content quality differences

**TC-4.5.1-C: Comparative Analysis**
- [x] Each submission should have individual criterion scores
- [x] AI narratives should reference submission-specific content
- [x] Overall summaries should differentiate between submissions
- [x] Export should include all submissions with complete data

**TC-4.5.1-D: Large Batch Evaluation**
- [x] System should handle evaluation of 5+ submissions
- [x] Progress indicator should update during batch processing
- [x] All submissions should complete without timeout
- [x] Results should be consistent across multiple runs

**TC-4.5.1-E: PDF Document Submission**
- [x] Upload a PDF file as submission
- [x] PDF text content is extracted correctly
- [x] AI evaluation references PDF content appropriately
- [x] Results include meaningful scores and narratives

**TC-4.5.1-F: DOCX Document Submission**
- [x] Upload a DOCX file as submission
- [x] DOCX text content is extracted correctly
- [x] AI evaluation references DOCX content appropriately
- [x] Results include meaningful scores and narratives

### US-4.6: Delete Evaluation
**As a** user
**I want to** delete an evaluation
**So that** I can remove unwanted evaluations

**Acceptance Criteria:**
- [ ] Delete button on evaluation list items
- [ ] Confirmation dialog required
- [ ] Cannot delete running evaluations
- [ ] Successful deletion removes from list

---

## Epic 5: Export & Reporting

### US-5.1: Export to JSON
**As a** user
**I want to** export evaluation results to JSON
**So that** I can integrate with other systems

**Acceptance Criteria:**
- [ ] Export dropdown on results page
- [ ] "Export as JSON" option
- [ ] Downloads file named `[evaluation-name].json`
- [ ] JSON contains: evaluation metadata, all results with scores and narratives

### US-5.2: Export to CSV
**As a** user
**I want to** export evaluation results to CSV
**So that** I can analyze in spreadsheet software

**Acceptance Criteria:**
- [ ] "Export as CSV" option in dropdown
- [ ] Downloads file named `[evaluation-name].csv`
- [ ] Columns: Rank, Submission, Overall Score, [each criterion], Summary
- [ ] One row per submission

### US-5.3: Export to PDF (Future)
**As a** user
**I want to** export evaluation results to PDF
**So that** I can share formatted reports

**Acceptance Criteria:**
- [ ] "Export as PDF" option in dropdown
- [ ] Generates formatted PDF with:
  - Header with evaluation name and date
  - Summary statistics
  - Ranked results with full narratives
  - Page breaks between submissions

---

## Epic 6: Error Handling & Edge Cases

### US-6.1: Handle Ingenious API Unavailable
**As a** user
**I want to** see a clear error when AI service is unavailable
**So that** I understand why evaluation failed

**Acceptance Criteria:**
- [ ] If Ingenious API unreachable, evaluation status = "Failed"
- [ ] Error message: "AI evaluation service unavailable. Please try again later."
- [ ] User can retry evaluation

### US-6.2: Handle Large Documents
**As a** user
**I want to** upload large documents without issues
**So that** I can evaluate comprehensive submissions

**Acceptance Criteria:**
- [ ] Maximum file size: 10MB
- [ ] Documents over limit show clear error
- [ ] Text extraction truncates at 50,000 characters with warning

### US-6.3: Handle Empty Submissions
**As a** user
**I want to** receive feedback if document has no extractable text
**So that** I know evaluation may be limited

**Acceptance Criteria:**
- [ ] Warning shown if extracted text is empty
- [ ] AI evaluation still runs with filename/metadata
- [ ] Results may be lower quality (noted in summary)

### US-6.4: Handle Concurrent Access
**As a** system
**I want to** prevent conflicts when same evaluation accessed concurrently
**So that** data integrity is maintained

**Acceptance Criteria:**
- [ ] Running evaluation cannot be modified
- [ ] Stale data detected and user prompted to refresh

---

## Epic 7: Performance & Optimization

### US-7.1: Paginated Lists
**As a** user
**I want to** efficiently browse large lists
**So that** the application remains responsive

**Acceptance Criteria:**
- [ ] Submissions list paginated (20 per page)
- [ ] Evaluations list paginated (20 per page)
- [ ] Load more / pagination controls visible

### US-7.2: Optimistic UI Updates
**As a** user
**I want to** see immediate feedback on actions
**So that** the app feels responsive

**Acceptance Criteria:**
- [ ] Uploads show in list immediately (with loading state)
- [ ] Deletes remove from list immediately
- [ ] Errors revert optimistic changes

### US-7.3: Timestamp Display Format
**As a** user
**I want to** see timestamps with time (x:xx AM/PM) in addition to dates
**So that** I can understand exactly when events occurred

**Acceptance Criteria:**
- [x] Evaluation list shows date and time (e.g., "Jan 12, 2026 3:45 PM")
- [x] Submission list shows date and time
- [x] Relative times ("Just now", "2 min ago") still used for recent items
- [x] Consistent format across all timestamp displays

---

## Non-Functional Requirements

### Security
- All API endpoints require JWT authentication
- Passwords hashed with bcrypt
- CORS configured for frontend origin only
- HTTPS required in production

### Performance
- API response time < 500ms (excluding AI calls)
- Frontend bundle < 500KB gzipped
- Lighthouse score > 90

### Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatible

### Browser Support
- Chrome (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Edge (last 2 versions)

---

## Glossary

| Term | Definition |
|------|------------|
| **Submission** | A document uploaded for evaluation |
| **Criteria Set** | A collection of weighted evaluation criteria |
| **Criterion** | A single evaluation dimension with weight and max score |
| **Evaluation** | A scoring session matching submissions to a criteria set |
| **Ingenious** | The AI agent orchestration library powering evaluations |
