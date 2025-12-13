# Component: Local Storage

<!-- Last updated: 2025-12-13 -->

**Parent:** [File Storage Service](../../container.md)
**System:** [System Context](../../../../context.md)

Local filesystem implementation of the file storage interface, providing asynchronous file operations for development and on-premise deployments.

## Diagram

![Component](./component.png)

## Responsibility

The Local Storage component:
- Implements file operations using local filesystem
- Provides async I/O operations via aiofiles library
- Automatically creates parent directories when writing
- Lists files and directories from filesystem
- Checks file existence with error handling

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| local_FileStorageRepository | Local filesystem implementation | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- File Storage Interface (IFileStorage)

### Cross-Container
- Configuration System: FileStorageContainerSettings

## Source Files

| File | Description |
|------|-------------|
| `ingenious/files/local/__init__.py` | Local filesystem implementation |
