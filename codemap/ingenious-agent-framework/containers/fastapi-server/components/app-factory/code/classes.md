# Code: App Factory Classes

<!-- Last updated: 2025-12-13 -->

**Parent:** [App Factory](../component.md)
**Container:** [FastAPI REST API Server](../../../container.md)
**System:** [System Context](../../../../../context.md)

## Class Diagram

![Classes](./classes.png)

## Classes

| Class | File | Purpose | Pattern |
|-------|------|---------|---------|
| FastAgentAPI | app_factory.py:22 | Main application factory | Factory, Builder |
| create_app | app_factory.py:116 | Factory function | Factory Function |

## FastAgentAPI

Main factory class that creates and configures the FastAPI application.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| config | IngeniousSettings | Application configuration |
| app | FastAPI | FastAPI application instance |

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `__init__` | `(config: IngeniousSettings)` | Initialize with configuration |
| `_create_app` | `() -> FastAPI` | Create FastAPI instance |
| `_configure_app` | `() -> None` | Run all configuration steps |
| `_setup_dependency_injection` | `() -> None` | Configure DI container |
| `_setup_working_directory` | `() -> None` | Set working directory |
| `_setup_middleware` | `() -> None` | Configure middleware stack |
| `_setup_routes` | `() -> None` | Register API routes |
| `_setup_exception_handlers` | `() -> None` | Register exception handlers |
| `_setup_optional_services` | `() -> None` | Initialize optional services |
| `_setup_root_redirect` | `() -> None` | Configure root redirect |
| `redirect_to_docs` | `() -> RedirectResponse` | Redirect to /docs |

## Design Patterns

| Pattern | Implementation | Description |
|---------|----------------|-------------|
| Factory | FastAgentAPI | Creates configured FastAPI instance |
| Builder | Configuration methods | Step-by-step application setup |
| Facade | FastAgentAPI | Hides complexity of initialization |

## Initialization Order

1. Create FastAPI instance
2. Setup working directory
3. Configure dependency injection
4. Setup middleware stack
5. Register routes
6. Register exception handlers
7. Setup optional services
8. Configure root redirect

## Usage

```python
from ingenious.config import get_config
from ingenious.main.app_factory import create_app

config = get_config()
app = create_app(config)
```
