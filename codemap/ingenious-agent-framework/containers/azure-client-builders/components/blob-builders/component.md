# Component: Blob Builders

<!-- Last updated: 2025-12-13 -->

**Parent:** [Azure Client Builders](../../container.md)
**System:** [System Context](../../../../context.md)

Specialized builders for creating Azure Blob Storage clients at both service and blob levels with support for connection strings, SAS tokens, and Azure AD authentication.

## Diagram

![Component](./component.png)

## Responsibility

The Blob Builders component:
- Provides builders for Azure Blob Service clients
- Provides builders for individual Blob clients
- Handles file storage configuration extraction
- Manages account URL resolution
- Supports connection strings and SAS token authentication

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| BlobServiceClientBuilder | Service-level builder | [View](./code/classes.md) |
| BlobClientBuilder | Individual blob builder | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Builder Base: Abstract base class

### Cross-Container
- Configuration System: File storage settings

## Source Files

| File | Description |
|------|-------------|
| `ingenious/client/azure/builder/blob_client.py` | Blob client builders |
