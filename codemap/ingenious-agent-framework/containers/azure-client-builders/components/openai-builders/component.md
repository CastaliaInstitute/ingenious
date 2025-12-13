# Component: OpenAI Builders

<!-- Last updated: 2025-12-13 -->

**Parent:** [Azure Client Builders](../../container.md)
**System:** [System Context](../../../../context.md)

Specialized builders for creating Azure OpenAI clients in both sync and async variants, supporting multiple authentication methods and AutoGen integration.

## Diagram

![Component](./component.png)

## Responsibility

The OpenAI Builders component:
- Provides builders for sync Azure OpenAI clients
- Provides builders for async Azure OpenAI clients
- Provides builder for AutoGen Chat Completion clients
- Handles model configuration extraction
- Supports API key and Azure AD authentication

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| AzureOpenAIClientBuilder | Sync client builder | [View](./code/classes.md) |
| AsyncAzureOpenAIClientBuilder | Async client builder | [View](./code/classes.md) |
| AzureOpenAIChatCompletionClientBuilder | AutoGen builder | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- Builder Base: Abstract base class

### Cross-Container
- Configuration System: Model settings

## Source Files

| File | Description |
|------|-------------|
| `ingenious/client/azure/builder/openai_client.py` | Sync builder |
| `ingenious/client/azure/builder/openai_client_async.py` | Async builder |
| `ingenious/client/azure/builder/openai_chat_completions_client.py` | AutoGen builder |
