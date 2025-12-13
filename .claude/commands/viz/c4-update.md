# C4 Architecture Update

Update the existing hierarchical C4 model based on code changes since it was last generated.

## Prerequisites

Hierarchical C4 model must exist in `codemap/<system-id>/` folder. If not, run `/viz/c4-map` first.

The expected structure is:
```
codemap/
└── <system-id>/
    ├── context.puml/md
    └── containers/
        └── <container-id>/
            ├── container.puml/md
            └── components/
                └── <component-id>/
                    ├── component.puml/md
                    └── code/
                        └── classes.puml/md
```

## Instructions

### Step 1: Identify the System and Changes

First, identify the system ID and what changed:

```bash
# Find the system folder
ls codemap/

# Get last modified date of C4 model
find codemap -type f \( -name "*.puml" -o -name "*.md" \) | head -20

# Find files changed since C4 model was created (use context.md as reference)
SYSTEM_ID=$(ls codemap/ | head -1)
find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" \) -newer codemap/$SYSTEM_ID/context.md 2>/dev/null | grep -v node_modules | grep -v __pycache__
```

Also check git history:
```bash
# Get commit hash when codemap was last updated
git log -1 --format="%H" -- codemap/

# Show all changes since then
git diff --name-status <commit_hash>..HEAD -- . ':!codemap'
```

### Step 2: Categorize Changes by Hierarchy Level

Group the changed files by their impact on the C4 hierarchy:

**Context-level changes** (affects `codemap/<system-id>/context.*`):
- New external integrations added
- External services removed
- New user types or actors
- New containers added to the system

**Container-level changes** (affects `codemap/<system-id>/containers/<container-id>/`):
- New services/applications added -> create new container folder
- Services removed -> remove container folder
- Technology stack changes
- New inter-container communication
- New components added to container

**Component-level changes** (affects `.../components/<component-id>/`):
- New modules/packages added -> create new component folder
- Modules removed -> remove component folder
- Component responsibility changes
- New dependencies between components
- New key classes added to component

**Code-level changes** (affects `.../components/<component-id>/code/`):
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

    SYSTEM_ID: <system-id>
    CHANGED FILES: [insert list from Step 1]

    EXPLORATION GOALS:
    1. Read codemap/<system-id>/context.md to understand existing state
    2. Analyze changed files for:
       - New external service integrations
       - Removed external dependencies
       - New user types or authentication methods
       - New containers that need to be added
    3. Identify what needs to be added/removed/modified

    HIERARCHICAL UPDATES:
    - If new containers detected, list them with IDs for folder creation
    - Update the "Drill Down - Containers" navigation table

    OUTPUT FORMAT:
    Return:
    - Updated C4-PlantUML Context diagram (full replacement)
    - NEW_CONTAINERS: Array of new container IDs to create folders for
    - REMOVED_CONTAINERS: Array of container IDs to remove
    - Change summary: what was added/removed/modified
```

**If container-level changes detected:**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Update C4 container level"
  prompt: |
    TASK: Update the CONTAINER level based on recent code changes.

    SYSTEM_ID: <system-id>
    CONTAINER_ID: <container-id>  # If specific container, otherwise "all"
    CHANGED FILES: [insert list from Step 1]

    EXPLORATION GOALS:
    1. Read codemap/<system-id>/containers/<container-id>/container.md
    2. Analyze changed files for:
       - Technology stack updates
       - New inter-container communication
       - New components within this container
       - Removed components
    3. Identify what needs to be added/removed/modified

    HIERARCHICAL UPDATES:
    - If new components detected, list them with IDs for folder creation
    - Update the "Drill Down - Components" navigation table
    - Update parent link if container moved

    OUTPUT FORMAT:
    Return:
    - Updated C4-PlantUML Container diagram (full replacement)
    - NEW_COMPONENTS: Array of {container_id, component_id} for folder creation
    - REMOVED_COMPONENTS: Array of {container_id, component_id} to remove
    - Updated technology stack table
    - Change summary
```

**If component-level changes detected:**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Update C4 component level"
  prompt: |
    TASK: Update the COMPONENT level based on recent code changes.

    SYSTEM_ID: <system-id>
    CONTAINER_ID: <container-id>
    COMPONENT_ID: <component-id>  # If specific component, otherwise "all"
    CHANGED FILES: [insert list from Step 1]

    EXPLORATION GOALS:
    1. Read codemap/<system-id>/containers/<container-id>/components/<component-id>/component.md
    2. Analyze changed files for:
       - Changed responsibilities
       - New inter-component dependencies
       - New key classes for code level
       - Removed classes
    3. Identify what needs to be added/removed/modified

    HIERARCHICAL UPDATES:
    - Update the "Drill Down - Code" navigation table
    - Update parent/sibling navigation links
    - If new classes, they go in ./code/ folder

    OUTPUT FORMAT:
    Return:
    - Updated C4-PlantUML Component diagram (full replacement)
    - CLASSES_CHANGED: true/false (whether code level needs update)
    - Updated dependency matrix
    - Change summary
```

**If code-level changes detected:**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Update C4 code level"
  prompt: |
    TASK: Update the CODE level based on recent code changes.

    SYSTEM_ID: <system-id>
    CONTAINER_ID: <container-id>
    COMPONENT_ID: <component-id>
    CHANGED FILES: [insert list from Step 1]

    EXPLORATION GOALS:
    1. Read codemap/<system-id>/containers/<container-id>/components/<component-id>/code/classes.md
    2. Analyze changed files for:
       - New key classes or interfaces
       - Changed class hierarchies
       - New design patterns
       - Significant method changes
    3. Identify what needs to be added/removed/modified

    HIERARCHICAL UPDATES:
    - Update navigation links to parent component

    OUTPUT FORMAT:
    Return:
    - Updated PlantUML class diagram (full replacement)
    - Updated design patterns table
    - Change summary
```

### Step 4: Apply Updates

For each subagent that returns updates:

**Create new folders if needed:**
```bash
SYSTEM_ID="<system-id>"

# For new containers
for CONTAINER_ID in <new-container-ids>; do
  mkdir -p codemap/$SYSTEM_ID/containers/$CONTAINER_ID/components
done

# For new components
for path in <new-component-paths>; do
  mkdir -p codemap/$SYSTEM_ID/containers/$CONTAINER_ID/components/$COMPONENT_ID/code
done
```

**Remove folders if containers/components were removed:**
```bash
# Remove entire container subtree
rm -rf codemap/$SYSTEM_ID/containers/<removed-container-id>

# Remove component subtree
rm -rf codemap/$SYSTEM_ID/containers/<container-id>/components/<removed-component-id>
```

**Update files in hierarchical locations:**

Context level:
- `codemap/<system-id>/context.puml` - Context diagram
- `codemap/<system-id>/context.md` - Documentation with updated navigation

Container level:
- `codemap/<system-id>/containers/<container-id>/container.puml` - Container diagram
- `codemap/<system-id>/containers/<container-id>/container.md` - Documentation

Component level:
- `codemap/<system-id>/containers/<container-id>/components/<component-id>/component.puml`
- `codemap/<system-id>/containers/<container-id>/components/<component-id>/component.md`

Code level:
- `codemap/<system-id>/containers/<container-id>/components/<component-id>/code/classes.puml`
- `codemap/<system-id>/containers/<container-id>/components/<component-id>/code/classes.md`

Update format for markdown files:
```markdown
<!-- Last updated: YYYY-MM-DD -->
<!-- Changes: brief summary of what changed -->
```

### Step 5: Update Navigation Links

After structural changes, ensure all navigation links are correct:

1. **Parent links** - Each level links UP to its parent
2. **Child links** - Each level has a "Drill Down" section linking to children
3. **Sibling links** - Optional, list other items at same level

Example navigation check:
```bash
# Find all markdown files and verify links
find codemap -name "*.md" -exec grep -l "Parent:" {} \;
```

### Step 6: Regenerate PNG Exports

After updating .puml files, regenerate the PNG exports:

```bash
SYSTEM_ID="<system-id>"

# Regenerate context PNG
plantuml -tpng codemap/$SYSTEM_ID/context.puml

# Regenerate affected container PNGs
plantuml -tpng codemap/$SYSTEM_ID/containers/<container-id>/container.puml

# Regenerate affected component PNGs
plantuml -tpng codemap/$SYSTEM_ID/containers/<container-id>/components/<component-id>/component.puml

# Regenerate affected code PNGs
plantuml -tpng codemap/$SYSTEM_ID/containers/<container-id>/components/<component-id>/code/classes.puml

# Or regenerate all
find codemap -name "*.puml" -exec plantuml -tpng {} \;
```

### Step 7: Update README

Update `codemap/README.md` with:
- New last-updated timestamp
- Summary of changes made
- Updated entry point link if system ID changed

## Output

After updates are applied, output:

```markdown
# C4 Update Summary

## Structural Changes
- [ ] New containers created: [list]
- [ ] Containers removed: [list]
- [ ] New components created: [list]
- [ ] Components removed: [list]

## Files Modified

### Context Level
- [ ] codemap/<system-id>/context.puml - [changes or "no changes"]
- [ ] codemap/<system-id>/context.png - [regenerated or "no changes"]
- [ ] codemap/<system-id>/context.md - [changes or "no changes"]

### Container Level
- [ ] codemap/<system-id>/containers/<container-id>/container.puml - [changes]
- [ ] codemap/<system-id>/containers/<container-id>/container.png - [regenerated]
- [ ] codemap/<system-id>/containers/<container-id>/container.md - [changes]

### Component Level
- [ ] .../components/<component-id>/component.puml - [changes]
- [ ] .../components/<component-id>/component.png - [regenerated]
- [ ] .../components/<component-id>/component.md - [changes]

### Code Level
- [ ] .../components/<component-id>/code/classes.puml - [changes]
- [ ] .../components/<component-id>/code/classes.png - [regenerated]
- [ ] .../components/<component-id>/code/classes.md - [changes]

## Changes Applied
[Summary of architectural changes detected and applied]

## Navigation Verified
- [ ] All parent links valid
- [ ] All child links valid
- [ ] Entry point in README.md updated

## Files Analyzed
[List of source files that triggered updates]

## Render Diagrams
```bash
find codemap -name "*.puml" -exec plantuml -tpng {} \;
```
```
