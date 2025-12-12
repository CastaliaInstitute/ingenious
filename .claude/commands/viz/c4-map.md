# C4 Architecture Mapping

Map the codebase architecture using the C4 model (Context, Container, Component, Code).

## Instructions

Use the Task tool to spawn 4 parallel Explore subagents in a single message. Each subagent analyzes one C4 level.

### Subagent Invocations

Invoke all 4 subagents in parallel using the Task tool:

**Subagent 1: System Context**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Map C4 system context"
  prompt: |
    TASK: Map the SYSTEM CONTEXT level (C4 Level 1) of this codebase.

    EXPLORATION GOALS:
    1. Identify the system boundary - determine what this software system is and does
    2. Find all users/actors by searching for:
       - Authentication/authorization code
       - User role definitions
       - API consumers
    3. Map external systems by searching for:
       - HTTP client configurations (requests, httpx, axios, fetch)
       - SDK imports (azure, aws, stripe, twilio, etc.)
       - Environment variables referencing external URLs/keys
       - Database connection strings for external DBs
    4. Document data flows in and out of the system

    SEARCH STRATEGY:
    - Glob for config files: **/*.env*, **/config.*, **/settings.*
    - Grep for HTTP clients: "requests\.", "httpx\.", "axios", "fetch("
    - Grep for SDK patterns: "import.*azure", "import.*aws", "from stripe"
    - Check docker-compose.yml for external service dependencies

    OUTPUT FORMAT:
    Return a C4-PlantUML Context diagram:
    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

    title System Context diagram for [System Name]

    Person(user, "User", "Description")
    System(system, "System Name", "Description")
    System_Ext(ext, "External System", "Description")

    Rel(user, system, "Uses")
    Rel(system, ext, "Calls")
    @enduml
    ```

    Also return:
    - List of external integrations found with file paths
    - List of user types/actors identified
```

**Subagent 2: Container Level**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Map C4 containers"
  prompt: |
    TASK: Map the CONTAINER level (C4 Level 2) of this codebase.

    EXPLORATION GOALS:
    1. Identify all deployable units:
       - Frontend applications (web, mobile)
       - Backend services/APIs
       - Background workers/jobs
       - Databases (type and purpose)
       - Message queues
       - Cache layers
    2. Document technology stack per container
    3. Map inter-container communication patterns
    4. Identify entry points and protocols

    SEARCH STRATEGY:
    - Glob for package manifests: **/package.json, **/requirements.txt, **/pyproject.toml, **/go.mod
    - Glob for deployment configs: **/Dockerfile, **/docker-compose.yml, **/k8s/**
    - Find main entry points: main.py, app.py, index.ts, server.ts
    - Grep for server setup: "FastAPI", "Express", "Flask", "createServer"
    - Grep for queue consumers: "celery", "bull", "rabbitmq", "kafka"

    OUTPUT FORMAT:
    Return a C4-PlantUML Container diagram:
    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

    title Container diagram for [System Name]

    Container(web, "Web App", "React", "User interface")
    Container(api, "API", "Node.js", "Business logic")
    ContainerDb(db, "Database", "PostgreSQL", "Data storage")

    Rel(web, api, "REST/JSON")
    Rel(api, db, "SQL")
    @enduml
    ```

    Also return:
    - Technology stack summary table
    - Key configuration files found with paths
    - Inter-container communication protocols
```

**Subagent 3: Component Level**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Map C4 components"
  prompt: |
    TASK: Map the COMPONENT level (C4 Level 3) of this codebase.

    EXPLORATION GOALS:
    For each container, analyze:
    1. Major modules/packages (top-level directories)
    2. Component responsibilities (one sentence each)
    3. Internal dependencies between components
    4. Key interfaces/contracts between components
    5. Shared utilities and their consumers

    SEARCH STRATEGY:
    - List top-level directories under src/ or equivalent
    - Read __init__.py or index.ts files for module exports
    - Grep for import patterns to map dependencies
    - Find interface/protocol definitions
    - Identify shared utility modules

    OUTPUT FORMAT:
    Return C4-PlantUML Component diagrams (one per container):
    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

    title Component diagram for [Container Name]

    Component(auth, "Auth Module", "Handles authentication")
    Component(users, "Users Module", "User management")
    Component(api, "API Layer", "Route handlers")

    Rel(api, auth, "Uses")
    Rel(api, users, "Uses")
    @enduml
    ```

    Also return:
    - Module dependency matrix
    - Interface files found with paths
    - Shared utility consumers list
```

**Subagent 4: Code Level**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Map C4 code structure"
  prompt: |
    TASK: Map the CODE level (C4 Level 4) of this codebase.

    EXPLORATION GOALS:
    For key components, analyze:
    1. Key classes/modules and their purposes
    2. Design patterns in use (Repository, Factory, Observer, etc.)
    3. Class relationships and hierarchies
    4. Critical code paths (request handling, data processing)
    5. Shared base classes or interfaces

    SEARCH STRATEGY:
    - Grep for class definitions: "class \w+", "interface \w+"
    - Find base classes: "class.*ABC", "class.*Base", "extends"
    - Identify patterns: "Repository", "Factory", "Service", "Handler"
    - Trace request flow from routes to data layer
    - Find abstract methods and implementations

    OUTPUT FORMAT:
    Return PlantUML class diagrams for key components:
    ```plantuml
    @startuml
    class UserService {
      +getUser(id)
      +createUser(data)
    }
    class UserRepository {
      +findById(id)
      +save(user)
    }
    UserService --> UserRepository
    @enduml
    ```

    Also return:
    - List of key classes with file paths
    - Design patterns identified with locations
    - Class hierarchy summary
```

## After All Subagents Complete

Create the `codemap/` folder and write each level to a separate file.

### Step 1: Create folder
```bash
mkdir -p codemap
```

### Step 2: Write files

**codemap/README.md**
```markdown
# C4 Architecture Map

<!-- Last updated: YYYY-MM-DD -->

Overview of [Project Name] architecture using the C4 model.

## Contents

- [context.md](./context.md) - System context and external integrations
- [containers.md](./containers.md) - Deployable units and technology stack
- [components.md](./components.md) - Internal modules and dependencies
- [code.md](./code.md) - Key classes and design patterns

## Quick Navigation

| Level | Scope | File |
|-------|-------|------|
| 1 | System Context | context.md |
| 2 | Containers | containers.md |
| 3 | Components | components.md |
| 4 | Code | code.md |

## Technology Stack
[Summary from Subagent 2]

## Key Files
[Combined file path list from all subagents]
```

**codemap/context.md**
```markdown
# Level 1: System Context

<!-- Last updated: YYYY-MM-DD -->

[Subagent 1 output: description]

## Diagram

[Subagent 1 C4-PlantUML Context diagram]

## External Systems

| System | Type | Integration Point |
|--------|------|-------------------|
| ... | ... | ... |

## Data Flows

[Description of data entering/leaving the system]
```

**codemap/containers.md**
```markdown
# Level 2: Containers

<!-- Last updated: YYYY-MM-DD -->

[Subagent 2 output: description]

## Diagram

[Subagent 2 C4-PlantUML Container diagram]

## Container Details

| Container | Technology | Purpose |
|-----------|------------|---------|
| ... | ... | ... |

## Communication

[Inter-container protocols and patterns]
```

**codemap/components.md**
```markdown
# Level 3: Components

<!-- Last updated: YYYY-MM-DD -->

[Subagent 3 output: description]

## Diagrams

[Subagent 3 C4-PlantUML Component diagrams - one per container]

## Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| ... | ... |

## Dependencies

[Internal dependency map]
```

**codemap/code.md**
```markdown
# Level 4: Code

<!-- Last updated: YYYY-MM-DD -->

[Subagent 4 output: description]

## Class Diagrams

[Subagent 4 PlantUML class diagrams]

## Design Patterns

| Pattern | Location | Purpose |
|---------|----------|---------|
| ... | ... | ... |

## Key Classes

| Class | File | Purpose |
|-------|------|---------|
| ... | ... | ... |
```

### Step 3: Confirm output

After writing all files, list the codemap folder:
```bash
ls -la codemap/
```

Output confirmation message with file locations.
