# Component: File Storage Facade

<!-- Last updated: 2025-12-13 -->

**Parent:** [File Storage Service](../../container.md)
**System:** [System Context](../../../../context.md)

Dynamic factory and facade that selects and initializes the appropriate storage backend based on configuration, providing a unified interface for file operations.

## Diagram

![Component](./component.png)

## Responsibility

The File Storage Facade component:
- Dynamically loads storage implementation based on configuration
- Selects between local and Azure backends
- Delegates file operations to appropriate backend
- Manages category-based storage configuration
- Provides helper methods for common paths (templates, data, output)

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| FileStorage | Factory and facade | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- File Storage Interface (IFileStorage)
- Local Storage (local_FileStorageRepository)
- Azure Storage (azure_FileStorageRepository)

### Cross-Container
- Configuration System: IngeniousSettings

## Source Files

| File | Description |
|------|-------------|
| `ingenious/files/files_repository.py` | Facade implementation |
