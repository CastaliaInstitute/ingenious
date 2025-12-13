# Component: Builder Base

<!-- Last updated: 2025-12-13 -->

**Parent:** [Azure Client Builders](../../container.md)
**System:** [System Context](../../../../context.md)

Abstract base class providing authentication and credential management for all Azure service client builders with support for multiple authentication methods.

## Diagram

![Component](./component.png)

## Responsibility

The Builder Base component:
- Provides abstract base class for all Azure builders
- Manages Azure authentication credentials (DEFAULT_CREDENTIAL, MSI, CLIENT_ID_AND_SECRET, TOKEN)
- Handles credential lazy-loading and caching
- Supports multiple credential types (TokenCredential, AzureKeyCredential)
- Validates authentication configuration

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| AzureClientBuilder | Abstract base class | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- None (provides foundation)

### Cross-Container
- Configuration System: Azure authentication configuration

## Source Files

| File | Description |
|------|-------------|
| `ingenious/client/azure/builder/base.py` | Abstract base class |
