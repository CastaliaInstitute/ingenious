# Component: Structured Logging

<!-- Last updated: 2025-12-13 -->

**Parent:** [Structured Logging](../../container.md)
**System:** [System Context](../../../../context.md)

Configurable structured logging system using structlog with context variable-based correlation tracking for request IDs, user IDs, and session IDs.

## Diagram

![Component](./component.png)

## Responsibility

The Structured Logging component:
- Initialize and configure structlog with customizable processors
- Track request correlation across async contexts using ContextVar
- Generate and manage unique request IDs
- Enrich log entries with correlation IDs, timestamps, and system metrics
- Provide typed logger factory and bound logger instances
- Log API calls with method, URL, status code, and duration
- Log database operations with table, operation type, and affected rows

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| setup_structured_logging | Configure structlog | [View](./code/classes.md) |
| get_logger | Get bound logger instance | [View](./code/classes.md) |
| PerformanceLogger | Context manager for timing | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- None

### Cross-Container
- None (cross-cutting concern)

## Source Files

| File | Description |
|------|-------------|
| `ingenious/core/structured_logging.py` | Logger factory and processors |
