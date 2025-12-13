# Component: Agents

<!-- Last updated: 2025-12-13 -->

**Parent:** [Chat Service / Multi-Agent Orchestrator](../../container.md)
**System:** [System Context](../../../../context.md)

Agent definitions, markdown-based configuration parsing, and agent metadata management. Supports definition of agent behavior, responsibilities, and associated tasks.

## Diagram

![Component](./component.png)

## Responsibility

The Agents component:
- Provides agent configuration and definition parsing
- Implements markdown-to-object conversion for agent specs
- Handles agent metadata extraction from markdown files
- Manages task definition and organization
- Provides agent prompt and instruction management

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| parse_markdown_to_object | Markdown parsing | [View](./code/classes.md) |
| GetAgent | Agent definition loader | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- None (agent definitions are self-contained)

### Cross-Container
- Configuration System: Default agent settings
- File Storage: Agent definition files

## Source Files

| File | Description |
|------|-------------|
| `ingenious/services/chat_services/multi_agent/agents/agents.py` | Agent utilities |
