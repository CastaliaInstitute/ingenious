# Component: OpenAI Service

<!-- Last updated: 2025-12-13 -->

**Parent:** [External LLM Services Adapter](../../container.md)
**System:** [System Context](../../../../context.md)

Azure OpenAI wrapper service providing asynchronous chat completions with support for streaming, tool calling, JSON mode, and comprehensive error handling including content filtering and token limit detection.

## Diagram

![Component](./component.png)

## Responsibility

The OpenAI Service component:
- Wraps Azure OpenAI Chat Completions API with async support
- Manages authentication via AzureClientFactory
- Provides non-streaming response generation with configurable tools
- Implements streaming response generation with chunk-by-chunk delivery
- Handles BadRequestError exceptions and converts to domain-specific errors
- Detects ContentFilterError when content filtering is triggered
- Detects TokenLimitExceededError when context length is exceeded

## Drill Down - Code

| Class | Purpose | Details |
|-------|---------|---------|
| OpenAIService | Azure OpenAI wrapper | [View](./code/classes.md) |

## Dependencies

### Internal (same container)
- None

### Cross-Container
- Azure Client Builders: OpenAI client factory creation
- Logging System: Structured logging
- Error Handling: Custom exceptions

## Source Files

| File | Description |
|------|-------------|
| `ingenious/external_services/openai_service.py` | OpenAI service implementation |
