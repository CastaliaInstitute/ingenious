# C4 Architecture Mapping

Map the codebase architecture using a hierarchical C4 model (Context -> Containers -> Components -> Code).

## Hierarchical Structure

The C4 model is built as a navigable tree where each level drills down into more detail:

```
codemap/
└── <system-name>/                    # Level 1: System Context
    ├── context.puml                  # Context diagram
    ├── context.md                    # Context documentation
    └── containers/                   # Level 2: Containers
        ├── <container-1>/
        │   ├── container.puml        # Container details
        │   ├── container.md          # Container documentation
        │   └── components/           # Level 3: Components
        │       ├── <component-a>/
        │       │   ├── component.puml
        │       │   ├── component.md
        │       │   └── code/         # Level 4: Code
        │       │       ├── classes.puml
        │       │       └── classes.md
        │       └── <component-b>/
        │           └── ...
        └── <container-2>/
            └── ...
```

## Instructions

Use the Task tool to spawn 4 parallel Explore subagents in a single message. Each subagent analyzes one C4 level and produces output that references its parent level.

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

    This is the ROOT of the C4 hierarchy. All other levels will be nested under this system.

    EXPLORATION GOALS:
    1. Identify the system name and create a kebab-case identifier (e.g., "ingenious-agent-framework")
    2. Define the system boundary - what this software system is and does
    3. Find all users/actors by searching for:
       - Authentication/authorization code
       - User role definitions
       - API consumers
    4. Map external systems by searching for:
       - HTTP client configurations (requests, httpx, axios, fetch)
       - SDK imports (azure, aws, stripe, twilio, etc.)
       - Environment variables referencing external URLs/keys
       - Database connection strings for external DBs
    5. Document data flows in and out of the system
    6. List the CONTAINERS this system contains (for cross-referencing)

    SEARCH STRATEGY:
    - Glob for config files: **/*.env*, **/config.*, **/settings.*
    - Grep for HTTP clients: "requests\.", "httpx\.", "axios", "fetch("
    - Grep for SDK patterns: "import.*azure", "import.*aws", "from stripe"
    - Check docker-compose.yml for external service dependencies
    - Read pyproject.toml or package.json for project name

    OUTPUT FORMAT:
    Return:
    1. SYSTEM_ID: kebab-case identifier for folder naming (e.g., "ingenious-framework")
    2. SYSTEM_NAME: Human-readable name for diagram titles
    3. CONTAINERS_LIST: Array of container IDs that will be created under this system:
       [
         { "id": "api-server", "name": "API Server", "technology": "FastAPI" },
         { "id": "database", "name": "Database", "technology": "SQLite/PostgreSQL" },
         ...
       ]
    4. C4-PlantUML Context diagram:
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
    5. List of external integrations found with file paths
    6. List of user types/actors identified
```

**Subagent 2: Container Level**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Map C4 containers"
  prompt: |
    TASK: Map the CONTAINER level (C4 Level 2) of this codebase.

    Containers are deployable units WITHIN the system. Each container will become a subfolder
    that houses its own components.

    EXPLORATION GOALS:
    1. Identify all deployable units with unique IDs:
       - Frontend applications (web, mobile)
       - Backend services/APIs
       - Background workers/jobs
       - Databases (type and purpose)
       - Message queues
       - Cache layers
    2. For EACH container, document:
       - container_id: kebab-case identifier (e.g., "api-server", "chat-database")
       - container_name: Human-readable name
       - technology: Primary technology/framework
       - responsibility: One-sentence description
       - components: List of component IDs it contains
    3. Map inter-container communication patterns
    4. Identify entry points and protocols

    SEARCH STRATEGY:
    - Glob for package manifests: **/package.json, **/requirements.txt, **/pyproject.toml, **/go.mod
    - Glob for deployment configs: **/Dockerfile, **/docker-compose.yml, **/k8s/**
    - Find main entry points: main.py, app.py, index.ts, server.ts
    - Grep for server setup: "FastAPI", "Express", "Flask", "createServer"
    - Grep for queue consumers: "celery", "bull", "rabbitmq", "kafka"

    OUTPUT FORMAT:
    Return:
    1. CONTAINERS: Array of container definitions with nested components:
       [
         {
           "id": "api-server",
           "name": "API Server",
           "technology": "FastAPI",
           "responsibility": "Handles HTTP requests and orchestrates business logic",
           "components": [
             { "id": "auth", "name": "Authentication", "path": "ingenious/auth" },
             { "id": "chat-services", "name": "Chat Services", "path": "ingenious/services/chat_services" },
             ...
           ]
         },
         {
           "id": "chat-database",
           "name": "Chat Database",
           "technology": "SQLite/Azure SQL",
           "responsibility": "Stores conversation history",
           "components": []
         },
         ...
       ]
    2. C4-PlantUML Container diagram showing ALL containers:
       ```plantuml
       @startuml
       !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

       title Container diagram for [System Name]

       Container(api_server, "API Server", "FastAPI", "Handles HTTP requests")
       ContainerDb(db, "Database", "PostgreSQL", "Data storage")

       Rel(api_server, db, "Reads/Writes", "SQL")
       @enduml
       ```
    3. INDIVIDUAL container diagrams (one per container) showing that container's relationship to others
    4. Technology stack summary table
    5. Inter-container communication protocols
```

**Subagent 3: Component Level**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Map C4 components"
  prompt: |
    TASK: Map the COMPONENT level (C4 Level 3) of this codebase.

    Components are modules WITHIN containers. Each component will become a subfolder
    under its parent container.

    EXPLORATION GOALS:
    For each container, analyze:
    1. Major modules/packages with unique IDs:
       - component_id: kebab-case identifier (e.g., "auth-module", "chat-service")
       - component_name: Human-readable name
       - parent_container_id: Which container this belongs to
       - source_path: Actual path in codebase
       - responsibility: One-sentence description
       - key_classes: List of important classes for Level 4
    2. Internal dependencies between components (WITHIN same container)
    3. Cross-container dependencies (which external containers this component calls)
    4. Key interfaces/contracts between components

    SEARCH STRATEGY:
    - List top-level directories under src/ or equivalent
    - Read __init__.py or index.ts files for module exports
    - Grep for import patterns to map dependencies
    - Find interface/protocol definitions
    - Identify shared utility modules

    OUTPUT FORMAT:
    Return:
    1. COMPONENTS: Array grouped by parent container:
       {
         "api-server": [
           {
             "id": "auth-module",
             "name": "Authentication",
             "source_path": "ingenious/auth",
             "responsibility": "JWT and Basic auth handling",
             "key_classes": ["JWTHandler", "BasicAuthMiddleware"],
             "internal_deps": ["config", "logging"],
             "external_deps": ["chat-database"]
           },
           ...
         ],
         "chat-database": [
           ...
         ]
       }
    2. C4-PlantUML Component diagrams (one per container):
       ```plantuml
       @startuml
       !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

       title Component diagram for API Server

       Component(auth, "Auth Module", "JWT/Basic Auth handling")
       Component(chat, "Chat Services", "Multi-agent orchestration")
       Component(db_repo, "Database Repository", "Data access layer")

       Rel(chat, auth, "Authenticates via")
       Rel(chat, db_repo, "Persists to")
       @enduml
       ```
    3. Module dependency matrix
    4. Interface files found with paths
```

**Subagent 4: Code Level**
```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Map C4 code structure"
  prompt: |
    TASK: Map the CODE level (C4 Level 4) of this codebase.

    Code diagrams show classes WITHIN components. Each code diagram will be nested
    under its parent component folder.

    EXPLORATION GOALS:
    For key components, analyze:
    1. Key classes/modules with mapping to parent:
       - class_name: Name of the class
       - parent_component_id: Which component this belongs to
       - parent_container_id: Which container (grandparent)
       - file_path: Location in codebase
       - purpose: One-sentence description
       - key_methods: Important public methods
    2. Design patterns in use (Repository, Factory, Observer, etc.)
    3. Class relationships and hierarchies
    4. Critical code paths (request handling, data processing)

    SEARCH STRATEGY:
    - Grep for class definitions: "class \w+", "interface \w+"
    - Find base classes: "class.*ABC", "class.*Base", "extends"
    - Identify patterns: "Repository", "Factory", "Service", "Handler"
    - Trace request flow from routes to data layer
    - Find abstract methods and implementations

    OUTPUT FORMAT:
    Return:
    1. CODE_DIAGRAMS: Array grouped by component and container:
       {
         "api-server": {
           "auth-module": {
             "classes": [
               {
                 "name": "JWTHandler",
                 "file": "ingenious/auth/jwt.py:15",
                 "purpose": "Validates and creates JWT tokens",
                 "methods": ["validate_token", "create_token", "decode_token"]
               },
               ...
             ],
             "patterns": ["Factory"],
             "diagram": "```plantuml\n@startuml\nclass JWTHandler {...}\n@enduml\n```"
           },
           "chat-services": {
             ...
           }
         }
       }
    2. PlantUML class diagrams for each component:
       ```plantuml
       @startuml
       title Classes in Auth Module

       class JWTHandler {
         +validate_token(token)
         +create_token(payload)
       }
       class BasicAuthMiddleware {
         +authenticate(request)
       }
       JWTHandler <.. BasicAuthMiddleware : uses
       @enduml
       ```
    3. Design patterns identified with locations
    4. Class hierarchy summary
```

## After All Subagents Complete

Create the hierarchical `codemap/` folder structure and write PlantUML diagrams.

### Step 1: Create hierarchical folder structure

Using the SYSTEM_ID from Subagent 1 and CONTAINERS from Subagent 2:

```bash
# Create root system folder
SYSTEM_ID="<system-id-from-subagent-1>"
mkdir -p codemap/$SYSTEM_ID/containers

# For each container, create nested structure
for CONTAINER_ID in <container-ids-from-subagent-2>; do
  mkdir -p codemap/$SYSTEM_ID/containers/$CONTAINER_ID/components

  # For each component in this container
  for COMPONENT_ID in <component-ids-for-this-container>; do
    mkdir -p codemap/$SYSTEM_ID/containers/$CONTAINER_ID/components/$COMPONENT_ID/code
  done
done
```

Example structure:
```bash
mkdir -p codemap/ingenious-framework/containers
mkdir -p codemap/ingenious-framework/containers/api-server/components/auth-module/code
mkdir -p codemap/ingenious-framework/containers/api-server/components/chat-services/code
mkdir -p codemap/ingenious-framework/containers/api-server/components/data-layer/code
mkdir -p codemap/ingenious-framework/containers/chat-database/components
mkdir -p codemap/ingenious-framework/containers/knowledge-base/components
```

### Step 2: Write PlantUML files in hierarchical locations

**Level 1 - System Context:**
- `codemap/<system-id>/context.puml` - System context diagram
- `codemap/<system-id>/context.md` - Context documentation

**Level 2 - Containers (one folder per container):**
- `codemap/<system-id>/containers/<container-id>/container.puml` - This container's diagram
- `codemap/<system-id>/containers/<container-id>/container.md` - Container documentation

**Level 3 - Components (nested under containers):**
- `codemap/<system-id>/containers/<container-id>/components/<component-id>/component.puml`
- `codemap/<system-id>/containers/<container-id>/components/<component-id>/component.md`

**Level 4 - Code (nested under components):**
- `codemap/<system-id>/containers/<container-id>/components/<component-id>/code/classes.puml`
- `codemap/<system-id>/containers/<container-id>/components/<component-id>/code/classes.md`

### Step 3: Write navigation links in each level

Each markdown file should include navigation links to:
- Parent level (go up the hierarchy)
- Child levels (drill down into detail)
- Sibling levels (other items at same level)

**Example context.md:**
```markdown
# System Context: [System Name]

<!-- Last updated: YYYY-MM-DD -->

[Description]

## Diagram

![System Context](./context.png)

## Drill Down - Containers

Navigate to containers within this system:

| Container | Technology | Description | Details |
|-----------|------------|-------------|---------|
| API Server | FastAPI | Handles HTTP requests | [View](./containers/api-server/container.md) |
| Chat Database | SQLite | Stores conversations | [View](./containers/chat-database/container.md) |

## External Systems

[External system details]
```

**Example container.md:**
```markdown
# Container: API Server

<!-- Last updated: YYYY-MM-DD -->

**Parent:** [System Context](../../context.md)

[Description]

## Diagram

![Container](./container.png)

## Drill Down - Components

Navigate to components within this container:

| Component | Responsibility | Details |
|-----------|----------------|---------|
| Auth Module | JWT/Basic auth | [View](./components/auth-module/component.md) |
| Chat Services | Multi-agent chat | [View](./components/chat-services/component.md) |

## Communication

[Inter-container protocols]
```

**Example component.md:**
```markdown
# Component: Auth Module

<!-- Last updated: YYYY-MM-DD -->

**Parent:** [API Server Container](../../container.md)
**System:** [System Context](../../../../context.md)

[Description]

## Diagram

![Component](./component.png)

## Drill Down - Code

View class diagrams for this component:

| Class | Purpose | Details |
|-------|---------|---------|
| JWTHandler | Token validation | [View](./code/classes.md) |

## Dependencies

[Internal and external dependencies]
```

**Example code/classes.md:**
```markdown
# Code: Auth Module Classes

<!-- Last updated: YYYY-MM-DD -->

**Parent:** [Auth Module Component](../component.md)
**Container:** [API Server](../../../container.md)
**System:** [System Context](../../../../../context.md)

## Class Diagram

![Classes](./classes.png)

## Classes

| Class | File | Purpose |
|-------|------|---------|
| JWTHandler | ingenious/auth/jwt.py:15 | Token validation |

## Design Patterns

[Patterns identified]
```

### Step 4: Generate PNG exports

Generate PNG images from all PlantUML files:

```bash
SYSTEM_ID="<system-id>"

# Generate context PNG
plantuml -tpng codemap/$SYSTEM_ID/context.puml

# Generate container PNGs
for dir in codemap/$SYSTEM_ID/containers/*/; do
  plantuml -tpng "${dir}container.puml"
done

# Generate component PNGs
find codemap/$SYSTEM_ID/containers -name "component.puml" -exec plantuml -tpng {} \;

# Generate code PNGs
find codemap/$SYSTEM_ID/containers -path "*/code/classes.puml" -exec plantuml -tpng {} \;
```

If PlantUML CLI is not available, note this in the output.

### Step 5: Write README.md

**codemap/README.md**
```markdown
# C4 Architecture Map

<!-- Last updated: YYYY-MM-DD -->

Hierarchical C4 model for [Project Name].

## Structure

This C4 map is organized as a navigable tree:

```
codemap/
└── <system-name>/              <- Start here
    ├── context.puml/md/png     <- Level 1: System Context
    └── containers/
        └── <container>/
            ├── container.puml/md/png  <- Level 2: Container
            └── components/
                └── <component>/
                    ├── component.puml/md/png  <- Level 3: Component
                    └── code/
                        └── classes.puml/md/png  <- Level 4: Code
```

## Entry Point

Start exploring from the system context:
- [System Context](./<system-id>/context.md)

## Navigation

- Each level links DOWN to its children (drill into detail)
- Each level links UP to its parent (zoom out for context)
- Use the navigation links in each .md file to explore

## Rendering Diagrams

```bash
# Render all diagrams
find codemap -name "*.puml" -exec plantuml -tpng {} \;
```
```

### Step 6: Confirm output

List the hierarchical structure:
```bash
find codemap -type f | sort
```

Output confirmation with:
- Hierarchical file locations
- Navigation entry point
- Instructions for rendering diagrams
