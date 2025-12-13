# Component: Error Handling

<!-- Last updated: 2025-12-13 -->

**Parent:** [Structured Logging](../../container.md)
**System:** [System Context](../../../../context.md)

Comprehensive error handling system providing context managers for common operations with automatic error mapping, retry decorators with exponential backoff, and recovery strategies.

## Diagram

![Component](./component.png)

## Responsibility

The Error Handling component:
- Wrap operations in context managers with automatic error mapping
- Catch and convert exceptions to typed Ingenious errors
- Track operation state, metadata, and execution duration
- Implement exponential backoff retry logic
- Provide recovery strategies (fallback, circuit breaker)
- Manage correlation IDs for error tracking
- Support both sync and async operation patterns

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| operation_context | Generic operation wrapper | [View](./code/classes.md) |
| database_operation | Database ops with retry | [View](./code/classes.md) |
| retry_on_error | Retry decorator | [View](./code/classes.md) |
| CircuitBreakerRecoveryStrategy | Circuit breaker pattern | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Structured Logging: Uses get_logger() for logging

### Cross-Container
- None

## Source Files

| File | Description |
|------|-------------|
| `ingenious/core/error_handling/context_managers.py` | Sync context managers |
| `ingenious/core/error_handling/decorators.py` | Retry decorators |
| `ingenious/core/error_handling/recovery.py` | Recovery strategies |
