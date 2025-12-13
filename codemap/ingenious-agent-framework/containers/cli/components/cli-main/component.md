# Component: CLI Main

<!-- Last updated: 2025-12-13 -->

**Parent:** [CLI Application](../../container.md)
**System:** [System Context](../../../../context.md)

Main CLI application entry point using Typer framework with Rich console for formatted output. Implements lazy command loading and command registry for extensibility.

## Diagram

![Component](./component.png)

## Responsibility

The CLI Main component:
- Initializes Typer application with custom theming
- Sets up Rich console for formatted terminal output
- Implements lazy loading of command groups
- Registers command modules (server, project, test, workflow, help, search)
- Provides root command callback handler
- Uses CommandRegistry for dynamic command discovery

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| app | Typer application instance | [View](./code/classes.md) |
| LazyGroup | Lazy command loading | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Command Modules: Individual command implementations

### Cross-Container
- Configuration System: Settings loading
- Logging System: CLI operation logging

## Source Files

| File | Description |
|------|-------------|
| `ingenious/cli/main.py` | CLI application entry point |
