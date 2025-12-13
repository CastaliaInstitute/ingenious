# Component: Command Modules

<!-- Last updated: 2025-12-13 -->

**Parent:** [CLI Application](../../container.md)
**System:** [System Context](../../../../context.md)

Individual CLI command implementations organized by functional area including server management, project initialization, testing, workflow execution, and help utilities.

## Diagram

![Component](./component.png)

## Responsibility

The Command Modules component:
- Implements server commands (serve, run-rest-api-server, prompt-tuner)
- Implements project commands (init, initialize-new-project)
- Implements test commands (test, run-test-batch)
- Implements workflow commands (workflows, workflow-requirements)
- Implements help commands (help, status, version, validate)
- Implements search commands (azure-search)
- Provides BaseCommand abstract class for consistent error handling

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| InitCommand | Project initialization | [View](./code/classes.md) |
| HelpCommand | Help display | [View](./code/classes.md) |
| StatusCommand | Status checking | [View](./code/classes.md) |
| ValidateCommand | Configuration validation | [View](./code/classes.md) |
| BaseCommand | Abstract base class | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- CLI Main: Command registration

### Cross-Container
- Configuration System: Settings validation
- FastAPI Server: Server startup

## Source Files

| File | Description |
|------|-------------|
| `ingenious/cli/server_commands.py` | Server management commands |
| `ingenious/cli/project_commands.py` | Project initialization commands |
| `ingenious/cli/test_commands.py` | Test execution commands |
| `ingenious/cli/workflow_commands.py` | Workflow management commands |
| `ingenious/cli/help_commands.py` | Help and status commands |
| `ingenious/cli/search_commands.py` | Azure Search commands |
