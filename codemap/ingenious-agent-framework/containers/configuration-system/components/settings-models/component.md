# Component: Settings Models

<!-- Last updated: 2025-12-13 -->

**Parent:** [Configuration Management](../../container.md)
**System:** [System Context](../../../../context.md)

Collection of Pydantic BaseModel classes defining the structure, validation rules, and defaults for all configuration sections.

## Diagram

![Component](./component.png)

## Responsibility

The Settings Models component:
- Defines structure for chat history database configuration
- Defines structure for AI model configuration with Azure authentication
- Defines structure for chat service configuration
- Defines structure for web server configuration (CORS, authentication)
- Defines structure for external service integrations
- Provides field-level and model-level validators

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| ChatHistorySettings | Chat persistence configuration | [View](./code/classes.md) |
| ModelSettings | AI model configuration | [View](./code/classes.md) |
| WebSettings | Web server configuration | [View](./code/classes.md) |
| AzureSearchSettings | Azure Search configuration | [View](./code/classes.md) |
| FileStorageSettings | File storage configuration | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- None (foundational models)

### Cross-Container
- None (foundational container)

## Source Files

| File | Description |
|------|-------------|
| `ingenious/config/models.py` | All Pydantic configuration classes |
| `ingenious/config/validators.py` | Validation logic |
