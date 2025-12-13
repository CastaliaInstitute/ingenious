# Component: Azure Storage

<!-- Last updated: 2025-12-13 -->

**Parent:** [File Storage Service](../../container.md)
**System:** [System Context](../../../../context.md)

Azure Blob Storage implementation of the file storage interface, supporting multiple authentication methods and providing complete file operation capabilities.

## Diagram

![Component](./component.png)

## Responsibility

The Azure Storage component:
- Implements file operations using Azure Blob Storage
- Manages multiple authentication methods (token, connection string, MSI)
- Handles blob path construction with proper formatting
- Lists files and directories with virtual directory support
- Checks blob existence and manages container lifecycle

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| azure_FileStorageRepository | Azure Blob implementation | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- File Storage Interface (IFileStorage)

### Cross-Container
- Azure Client Builders: BlobServiceClient creation
- Configuration System: FileStorageContainerSettings

## Source Files

| File | Description |
|------|-------------|
| `ingenious/files/azure/__init__.py` | Azure Blob implementation |
