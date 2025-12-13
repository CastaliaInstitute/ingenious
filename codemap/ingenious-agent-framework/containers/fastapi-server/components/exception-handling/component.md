# Component: Exception Handling

<!-- Last updated: 2025-12-13 -->

**Parent:** [FastAPI REST API Server](../../container.md)
**System:** [System Context](../../../../context.md)

Provides centralized exception handling with structured error responses, proper HTTP status code mapping, and user-friendly error messages with recovery suggestions.

## Diagram

![Component](./component.png)

## Responsibility

The Exception Handling component:
- Converts domain errors (IngeniousError) to HTTP responses
- Handles validation errors with field-level error details
- Provides user-friendly error messages with recovery suggestions
- Logs all exceptions with structured context information
- Maps HTTP status codes for different error types

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| ExceptionHandlers | Exception handler registration | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- None (pure error handling layer)

### Cross-Container
- Error System: IngeniousError and domain-specific errors
- Structured Logging: Error logging with context

## Source Files

| File | Description |
|------|-------------|
| `ingenious/main/exception_handlers.py` | Exception handlers |
