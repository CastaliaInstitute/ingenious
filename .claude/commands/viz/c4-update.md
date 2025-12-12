# C4 Architecture Update

Update the existing C4 model based on code changes since it was last generated.

## Prerequisites

C4 model must exist in `codemap/` folder. If not, run `/viz/c4-map` first.

## Instructions

### Step 1: Identify Changes

Run these commands to identify what changed:

```bash
# Get last modified date of C4 model
ls -la codemap/

# Find files changed since C4 model was created
# Use the oldest codemap file's date as reference
find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" \) -newer codemap/context.md 2>/dev/null | grep -v node_modules | grep -v __pycache__
```

Also check git history:
```bash
# Get commit hash when codemap was last updated
git log -1 --format="%H" -- codemap/

# Show all changes since then
git diff --name-status <commit_hash>..HEAD -- . ':!codemap'
```

### Step 2: Categorize Changes

Group the changed files by impact level:

**Context-level changes** (affects `codemap/context.md`):
- New external integrations added
- External services removed
- New user types or actors

**Container-level changes** (affects `codemap/containers.md`):
- New services/applications added
- Services removed or merged
- Technology stack changes (new frameworks, databases)
- New inter-service communication

**Component-level changes** (affects `codemap/components.md`):
- New modules/packages added
- Modules removed or renamed
- Component responsibility changes
- New dependencies between components

**Code-level changes** (affects `codemap/code.md`):
- New key classes added
- Class hierarchy changes
- New design patterns introduced
- Interface changes

### Step 3: Spawn Update Subagents

Based on the categorized changes, spawn parallel Explore subagents ONLY for affected levels.

**If context-level changes detected:**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Update C4 context level"
  prompt: |
    TASK: Update the SYSTEM CONTEXT level based on recent code changes.

    CHANGED FILES: [insert list from Step 1]

    EXPLORATION GOALS:
    1. Read the current codemap/context.md to understand existing state
    2. Analyze the changed files for:
       - New external service integrations (HTTP clients, SDKs)
       - Removed external dependencies
       - New user types or authentication methods
    3. Identify what needs to be added/removed/modified in the diagram

    SEARCH STRATEGY:
    - Read each changed file to understand the change
    - Grep for new import statements related to external services
    - Check for new environment variable references
    - Compare against existing external systems in context.md

    OUTPUT FORMAT:
    Return:
    - Updated C4-PlantUML Context diagram (full replacement)
    - Change summary: what was added/removed/modified
    - List of files that triggered each change
```

**If container-level changes detected:**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Update C4 container level"
  prompt: |
    TASK: Update the CONTAINER level based on recent code changes.

    CHANGED FILES: [insert list from Step 1]

    EXPLORATION GOALS:
    1. Read the current codemap/containers.md to understand existing state
    2. Analyze the changed files for:
       - New services or applications added
       - Services removed or consolidated
       - Technology stack updates (new dependencies in package files)
       - New inter-service communication patterns
    3. Identify what needs to be added/removed/modified in the diagram

    SEARCH STRATEGY:
    - Check if any new Dockerfile or docker-compose entries exist
    - Read changed package.json/requirements.txt for new major dependencies
    - Look for new main entry points or server configurations
    - Find new API routes or queue consumers

    OUTPUT FORMAT:
    Return:
    - Updated C4-PlantUML Container diagram (full replacement)
    - Change summary: what was added/removed/modified
    - Updated technology stack table
```

**If component-level changes detected:**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Update C4 component level"
  prompt: |
    TASK: Update the COMPONENT level based on recent code changes.

    CHANGED FILES: [insert list from Step 1]

    EXPLORATION GOALS:
    1. Read the current codemap/components.md to understand existing state
    2. Analyze the changed files for:
       - New modules or packages created
       - Modules removed or renamed
       - Changed responsibilities (significant refactoring)
       - New inter-component dependencies
    3. Identify what needs to be added/removed/modified in the diagrams

    SEARCH STRATEGY:
    - Check for new top-level directories
    - Analyze import statement changes
    - Look for new __init__.py or index.ts files
    - Identify moved or renamed modules

    OUTPUT FORMAT:
    Return:
    - Updated C4-PlantUML Component diagrams (full replacement for affected containers)
    - Change summary: what was added/removed/modified
    - Updated dependency matrix
```

**If code-level changes detected:**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Update C4 code level"
  prompt: |
    TASK: Update the CODE level based on recent code changes.

    CHANGED FILES: [insert list from Step 1]

    EXPLORATION GOALS:
    1. Read the current codemap/code.md to understand existing state
    2. Analyze the changed files for:
       - New key classes or interfaces
       - Changed class hierarchies
       - New design patterns introduced
       - Significant method signature changes
    3. Identify what needs to be added/removed/modified in the diagrams

    SEARCH STRATEGY:
    - Read the changed class definitions
    - Check for new inheritance relationships
    - Identify new pattern implementations
    - Look for new abstract base classes

    OUTPUT FORMAT:
    Return:
    - Updated PlantUML class diagrams (full replacement for affected components)
    - Change summary: what was added/removed/modified
    - Updated design patterns table
```

### Step 4: Apply Updates

For each subagent that returns updates:

1. Read the current file from `codemap/`
2. Apply the changes
3. Add update timestamp to the file header

Update format for each file:
```markdown
<!-- Last updated: YYYY-MM-DD -->
<!-- Changes: brief summary of what changed -->
```

### Step 5: Update Index

Update `codemap/README.md` with:
- New last-updated timestamp
- Summary of changes made
- List of files modified

## Output

After updates are applied, output:

```markdown
# C4 Update Summary

## Files Modified
- [ ] codemap/context.md - [changes or "no changes"]
- [ ] codemap/containers.md - [changes or "no changes"]
- [ ] codemap/components.md - [changes or "no changes"]
- [ ] codemap/code.md - [changes or "no changes"]

## Changes Applied
[Summary of architectural changes detected and applied]

## Files Analyzed
[List of source files that triggered updates]

## Recommendation
[Any manual review needed or follow-up actions]
```
