# Component: Settings Root

<!-- Last updated: 2025-12-13 -->

**Parent:** [Configuration Management](../../container.md)
**System:** [System Context](../../../../context.md)

Root settings class that loads and validates all configuration from environment variables, .env files, and provides the main configuration interface for the entire application.

## Diagram

![Component](./component.png)

## Responsibility

The Settings Root component:
- Loads configuration from INGENIOUS_* environment variables
- Loads configuration from .env files (.env, .env.local, .env.dev, .env.prod)
- Combines all configuration models through composition
- Validates complete configuration and provides helpful error messages
- Parses JSON and nested environment variable formats
- Ensures at least one AI model is configured
- Provides factory methods for creating minimal or custom configurations

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| IngeniousSettings | Root configuration class | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Settings Models: All individual configuration models

### Cross-Container
- None (foundational container)

## Source Files

| File | Description |
|------|-------------|
| `ingenious/config/main_settings.py` | Main IngeniousSettings class |
| `ingenious/config/environment.py` | Environment variable handling |
