# Component: Authentication Middleware

<!-- Last updated: 2025-12-13 -->

**Parent:** [Authentication & Authorization](../../container.md)
**System:** [System Context](../../../../context.md)

Global authentication middleware that protects FastAPI endpoints with optional per-request authentication enforcement. Validates user credentials from JWT Bearer tokens or Basic Auth, enforces exemptions for public endpoints, and provides structured error handling.

## Diagram

![Component](./component.png)

## Responsibility

The Authentication Middleware component:
- Enforces global authentication when enabled
- Validates all incoming requests (except exempt paths)
- Supports JWT Bearer token authentication
- Supports HTTP Basic Auth credentials
- Exempts public paths from authentication
- Adds authenticated user information to request state
- Provides structured error responses for authentication failures
- Logs authentication events for audit trails

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| AuthenticationMiddleware | Global auth enforcement | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- JWT Service: Token verification

### Cross-Container
- Configuration System: Authentication enablement and exempt paths
- Logging System: Authentication event logging

## Source Files

| File | Description |
|------|-------------|
| `ingenious/auth/middleware.py` | Authentication middleware implementation |
