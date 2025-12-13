# Component: Routing

<!-- Last updated: 2025-12-13 -->

**Parent:** [FastAPI REST API Server](../../container.md)
**System:** [System Context](../../../../context.md)

Manages route registration for all API endpoints, including built-in routes (authentication, chat, conversations, diagnostics, prompts, message feedback) and custom extension routes.

## Diagram

![Component](./component.png)

## Responsibility

The Routing component:
- Registers built-in API routes with their respective routers
- Discovers and registers custom routes from extensions
- Organizes routes by feature area with versioned API prefixes
- Provides route tagging for OpenAPI documentation
- Supports custom route implementations via extensible interface

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| RouteManager | Route registration orchestrator | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- App Factory: Route registration during initialization

### Cross-Container
- Auth Routes: `/api/v1/auth` endpoints
- Chat Routes: `/api/v1/chat` endpoints
- Conversation Routes: `/api/v1/conversations` endpoints
- Diagnostic Routes: `/api/v1/diagnostic` endpoints

## Source Files

| File | Description |
|------|-------------|
| `ingenious/main/routing.py` | Route manager |
| `ingenious/api/routes/auth.py` | Authentication routes |
| `ingenious/api/routes/chat.py` | Chat routes |
| `ingenious/api/routes/conversation.py` | Conversation routes |
| `ingenious/api/routes/diagnostic.py` | Diagnostic routes |
