# Level 1: System Context

<!-- Last updated: 2025-12-12 -->

The System Context diagram shows how the Ingenious framework interacts with users and external systems.

## Diagram

Source: [context.puml](./context.puml)

## System Summary

**Ingenious** is a core AI agent framework library built on FastAPI that orchestrates multi-agent conversations using Microsoft's AutoGen framework. It provides a production-ready platform for building AI-powered APIs with flexible deployment options (local development to full Azure cloud).

## Users/Actors

| Actor | Description | Interaction |
|-------|-------------|-------------|
| **Developer** | Uses Ingenious CLI to configure and deploy | CLI commands: init, serve, validate |
| **API Client** | Applications calling Ingenious APIs | REST API calls: chat, workflows, auth |
| **End User** | Interacts with applications built on Ingenious | Through client applications |

## External Systems

| System | Type | Integration Point | Purpose |
|--------|------|-------------------|---------|
| Azure OpenAI | LLM Service | REST API | Chat completions, text embeddings |
| Azure AI Search | Search Service | REST API | Vector search, semantic search |
| Azure SQL Database | Cloud Database | ODBC | Production chat history |
| Azure Cosmos DB | NoSQL Database | REST/SDK | Distributed chat history |
| ChromaDB | Local Vector DB | Python SDK | Local embeddings storage |
| SQLite | Local Database | SQL | Development chat history |
| Azure Blob Storage | File Storage | REST/SDK | Document storage |
| Azure Identity | Authentication | SDK | AAD/MSI authentication |

## Data Flows

### Inbound
- **API Client -> Ingenious**: Chat requests with user prompts and conversation flow
- **Developer -> Ingenious**: CLI commands for configuration and server management

### Outbound
- **Ingenious -> Azure OpenAI**: Chat completion requests, streaming responses
- **Ingenious -> Azure AI Search**: Vector similarity search queries
- **Ingenious -> Azure SQL/Cosmos**: Chat history CRUD operations
- **Ingenious -> Azure Blob**: Document upload/download operations
- **Ingenious -> Azure Identity**: Token acquisition for AAD authentication

## Authentication Methods

| Method | Use Case |
|--------|----------|
| JWT Bearer Token | API authentication |
| Basic Auth | Simple username/password |
| Azure AD | Enterprise authentication |
| Managed Identity | Azure serverless deployments |
| Service Principal | Automated deployments |
