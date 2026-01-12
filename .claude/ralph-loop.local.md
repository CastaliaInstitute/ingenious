---
active: true
iteration: 4
max_iterations: 5
completion_promise: null
started_at: "2026-01-12T06:30:09Z"
---

Follow the following prompt for both soca and ingen-prompt-tuner. You MUST confirm that all user stories are working as COMPLETELY expected or make fixes as needed so that they do:

# Master Prompt

## Environment

- Run the apps locally
- Use Azure resources for tests only

## Azure Constraints

- Use Azure CLI () for all operations
- **Resource Group:** Use  exclusively—do not create or modify resources outside this RG
- **Tagging:** Apply the tag  or  to all resources based on which app they support
- **Provisioning:** Only create resources if they do not already exist in the  resource group
- **Cost:** Provision the cheapest viable SKUs/tiers needed to run tests

---

## Definitions

| ID | Definition |
|---|---|
|  | All User Stories in spec.md |
|  |  |

---

## Primary Goal

Work autonomously to validate the application end-to-end per all User Stories. Most implementation is complete - resolve all remaining issues until fully functional.

> **⚠️ YOU CANNOT STOP UNTIL EVERYTHING IN spec.md IS IMPLEMENTED AND VALIDATED.**

---

## Autonomous Work Expectations

### Context Window Management

Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off.

### Completion Mandate ⚠️ ABSOLUTE

- **YOU CANNOT STOP** until EVERYTHING in spec.md is implemented and validated
- **DO NOT** stop early - work until EVERYTHING is FLESHED OUT COMPLETELY
- Do **NOT** stop tasks due to token budget concerns
- Complete tasks **FULLY**, even if end of budget is approaching
- **NEVER** artificially stop any task early regardless of context remaining

### Required Work Cycle

For **EACH and EVERY** feature in spec.md:

1. Validate using Playwright MCP
2. Debug any issues found
3. Code and implement fixes/features as needed
4. Work to unblock and resolve ALL problems
5. Re-validate until feature is fully functional
6. Move to next feature - repeat until ALL features complete

### Expectation

CONTINUE and DO NOT STOP until the entire app is finished and validated end-to-end. You are expected to work autonomously for a **VERY LONG PERIOD OF TIME** to complete this task.

The work is **NOT** complete until EVERY User Story in spec.md is:
- ✅ Fully implemented
- ✅ Thoroughly validated with Playwright MCP
- ✅ Debugged and working correctly
- ✅ Integrated and stable

### Planning Approach

Be ambitious with task lists and planning - context management allows for extensive work sessions. Break down ALL User Stories comprehensively and work through EVERY SINGLE ONE without stopping.

---

## Development Workflow

### Code Changes

**Trigger:** After ANY code modification

**Required Steps:**
1. Run  immediately
2. Confirm deployment successful
3. Re-test functionality
4. Proceed only after verifying stability

### Debugging

- **On Failure:** Debug → Fix →  → Confirm resolution
- **Persistence:** Continue debugging and fixing until issue is COMPLETELY resolved

---

## Validation & Testing

### Scope

| Aspect | Details |
|---|---|
| **Source** | ALL User Stories in spec.md - EVERY SINGLE ONE must be validated |
| **Aspects** | Functional correctness, data consistency, state transitions, error handling |

### Method

- **Tool:** Playwright MCP in integrated environment
- **Requirement:** Validate complete flows from start to expected result for EACH feature

**Workflow:**
1. Use Playwright MCP to test feature
2. If issues found: debug, code fixes, deploy with
3. Re-validate with Playwright MCP
4. Repeat until feature is FULLY functional
5. Move to next feature

### Page Requirements

- All functions fully implemented and data-driven (no hardcoded placeholders)
- Manual routes accessible via UI
- Document new components in  with behavior and state details
- Map UI elements to corresponding User Stories

### Completion Criteria

Work is **NOT** complete until:
- ✅ Every feature in spec.md is implemented
- ✅ Every feature passes Playwright MCP validation
- ✅ No bugs or blockers remain
- ✅ All flows work end-to-end

---

## Specifications Compliance

- **Source:** spec.md is the authoritative source - ALL items must be completed

### Refinement Guideline

If specifications are unclear, refine them to be:
- Explicit and structured
- Consistent and agent-friendly
- While preserving original intent

---

## Execution Plan

### Approach

Decompose ALL User Stories in spec.md into comprehensive, ambitious task list. Work through EVERY SINGLE task without stopping until complete. Context management supports extensive planning - be thorough and complete.

### Priorities

| Level | Priority |
|:---:|---|
| 1 | Complete EVERYTHING in spec.md - no exceptions |
| 2 | Validate each feature with Playwright MCP |
| 3 | Debug and fix all issues immediately |
| 4 | Run  after each update |
| 5 | DO NOT STOP until all User Stories are done |

### Work Style

**AUTONOMOUS** execution **WITHOUT STOPPING** until ALL User Stories are:
- Implemented completely
- Validated end-to-end with Playwright MCP
- Debugged and working correctly
- Integrated and stable

Work **PERSISTENTLY** for as long as needed. **DO NOT** stop early. **EVERYTHING** must be FLESHED OUT COMPLETELY before stopping.

---

## Final Mandate ⚠️ ABSOLUTE

**YOU CANNOT STOP WORKING UNTIL:**

- ✅ Every User Story in spec.md is implemented
- ✅ Every feature is validated with Playwright MCP
- ✅ Every bug is debugged and fixed
- ✅ The entire application works end-to-end
- ✅ EVERYTHING is FLESHED OUT COMPLETELY

> **🚨 DO NOT STOP EARLY. WORK CONTINUOUSLY UNTIL COMPLETE.**
