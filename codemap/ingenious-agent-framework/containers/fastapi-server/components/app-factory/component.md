# Component: FastAPI Application Factory

<!-- Last updated: 2025-12-13 -->

**Parent:** [FastAPI REST API Server](../../container.md)
**System:** [System Context](../../../../context.md)

Bootstraps and configures the FastAPI application instance with middleware, routes, exception handlers, and all initialization logic.

## Diagram

![Component](./component.png)

## Responsibility

The App Factory is the central orchestrator for application initialization. It:
- Creates the FastAPI application instance
- Configures middleware stack in correct order
- Registers all API routes (built-in and custom)
- Sets up exception handlers
- Configures dependency injection
- Initializes optional services

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| FastAgentAPI | Main factory class | [View](./code/classes.md) |
| create_app | Factory function | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Routing: Route registration
- Middleware: Middleware configuration
- Exception Handlers: Error handling setup
- Dependency Injection: Service instantiation

### Cross-Container
- Configuration System: IngeniousSettings loading

## Source Files

| File | Description |
|------|-------------|
| `ingenious/main/app_factory.py` | Main factory implementation |
