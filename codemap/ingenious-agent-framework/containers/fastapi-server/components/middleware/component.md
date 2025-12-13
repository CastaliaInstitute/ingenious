# Component: Middleware

<!-- Last updated: 2025-12-13 -->

**Parent:** [FastAPI REST API Server](../../container.md)
**System:** [System Context](../../../../context.md)

Provides cross-cutting concerns for HTTP request processing including security headers, request context tracking, structured logging, and tracing.

## Diagram

![Component](./component.png)

## Responsibility

The Middleware component:
- Injects security headers (HSTS, X-Content-Type-Options, X-Frame-Options, CSP)
- Sets up request context with correlation IDs for distributed tracing
- Provides structured logging of request start, completion, and errors
- Extracts user context from JWT Bearer tokens and Basic auth
- Measures request timing and performance tracking

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| SecurityHeadersMiddleware | Security header injection | [View](./code/classes.md) |
| RequestContextMiddleware | Request context and logging | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- None (pure middleware layer)

### Cross-Container
- Structured Logging: Correlation ID management
- Auth System: JWT token validation

## Source Files

| File | Description |
|------|-------------|
| `ingenious/main/middleware.py` | Middleware classes |
