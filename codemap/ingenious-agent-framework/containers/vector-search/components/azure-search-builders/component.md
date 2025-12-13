# Component: Azure Search Builders

<!-- Last updated: 2025-12-13 -->

**Parent:** [Vector Search / Knowledge Base](../../container.md)
**System:** [System Context](../../../../context.md)

Configuration builders that validate and construct SearchConfig from application settings, handling field name aliasing and applying sensible defaults.

## Diagram

![Component](./component.png)

## Responsibility

The Azure Search Builders component:
- Parses application settings and constructs validated SearchConfig
- Handles field name aliases (key vs api_key, endpoint vs base_url)
- Selects and validates embedding and chat models from configuration
- Applies sensible defaults for optional parameters
- Validates URLs and enforces critical constraints
- Provides user-actionable error messages for configuration failures

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| ConfigError | Configuration exceptions | [View](./code/classes.md) |
| build_search_config_from_settings | Main builder entry point | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- SearchConfig: Configuration model

### Cross-Container
- Configuration System: IngeniousSettings
- Azure Client Factory: Credential builders

## Source Files

| File | Description |
|------|-------------|
| `ingenious/services/azure_search/builders.py` | Configuration builders |
