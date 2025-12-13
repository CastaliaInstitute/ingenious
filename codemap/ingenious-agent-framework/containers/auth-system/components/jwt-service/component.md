# Component: JWT Service

<!-- Last updated: 2025-12-13 -->

**Parent:** [Authentication & Authorization](../../container.md)
**System:** [System Context](../../../../context.md)

JWT token creation and validation with support for access and refresh tokens. Manages token lifecycle including generation, verification, expiration validation, and secret key configuration from environment or settings.

## Diagram

![Component](./component.png)

## Responsibility

The JWT Service component:
- Creates short-lived access tokens (default 24 hours)
- Creates long-lived refresh tokens (default 7 days)
- Verifies and decodes tokens with expiration validation
- Extracts user identity from tokens
- Manages JWT configuration from environment variables or application settings
- Handles token type validation (access vs refresh)
- Provides secure error handling with structured logging

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| JWTConfigurationError | Configuration exception | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- None

### Cross-Container
- Configuration System: JWT secret key and expiration settings
- Logging System: Structured logging for authentication events

## Source Files

| File | Description |
|------|-------------|
| `ingenious/auth/jwt.py` | JWT token management implementation |
