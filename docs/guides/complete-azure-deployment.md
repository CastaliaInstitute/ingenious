# Complete Azure Deployment Guide

This guide provides step-by-step instructions for moving from local development to production Azure deployment with **Cosmos DB** and **Azure Blob Storage**.

## Prerequisites

- Azure CLI installed and authenticated
- Azure OpenAI resource (required)
- Azure subscription with appropriate permissions

## Architecture Overview

This guide uses the recommended Azure architecture for Ingenious:
- **Azure Cosmos DB** (Serverless) - Chat history persistence with automatic scaling
- **Azure Blob Storage** - Prompt template storage
- **Azure OpenAI** - AI model hosting

> **Note**: For relational database requirements, see the [Azure SQL Deployment Guide](azure-sql-deployment.md) as an alternative to Cosmos DB.

## Quick Deploy with Bicep (Optional)

If you want to recreate the core Azure resources from this guide in a single step, use the Bicep template located at `infra/main.bicep`. The defaults match the resource names used throughout the documentation; override parameters as needed to avoid name collisions.

```bash
# Deploy (or update) resources into your resource group
az deployment group create \
  --resource-group your-rg-name \
  --template-file infra/main.bicep \
  --parameters clientIpAddress=$(curl -s ipinfo.io/ip)

# Preview changes without applying
az deployment group what-if \
  --resource-group your-rg-name \
  --template-file infra/main.bicep
```

## Minimal Azure Provisioning

### 1. Create Resource Group

```bash
# Check if resource group exists first
az group show --name your-rg-name 2>/dev/null ||
az group create --name your-rg-name --location eastus
```

### 2. Provision Cosmos DB (Serverless - Free Tier)

```bash
# Check if Cosmos DB account exists first
COSMOS_EXISTS=$(az cosmosdb show --name your-cosmos-account --resource-group your-rg-name 2>/dev/null)
if [ -z "$COSMOS_EXISTS" ]; then
  # Create Cosmos DB account with serverless and free tier (cheapest option)
  az cosmosdb create \
    --name your-cosmos-account \
    --resource-group your-rg-name \
    --default-consistency-level Session \
    --locations regionName=eastus2 failoverPriority=0 isZoneRedundant=false \
    --kind GlobalDocumentDB \
    --capabilities EnableServerless \
    --enable-free-tier true
else
  echo "Cosmos DB account already exists, skipping creation"
fi

# Create SQL API database
az cosmosdb sql database create \
  --account-name your-cosmos-account \
  --resource-group your-rg-name \
  --name ingenious-db
```

### 3. Provision Azure Blob Storage

```bash
# Check if storage account exists first
STORAGE_EXISTS=$(az storage account show --name yourblobstorage --resource-group your-rg-name 2>/dev/null)
if [ -z "$STORAGE_EXISTS" ]; then
  # Create storage account (Standard_LRS - cheapest option)
  az storage account create \
    --name yourblobstorage \
    --resource-group your-rg-name \
    --location eastus2 \
    --sku Standard_LRS \
    --kind StorageV2
else
  echo "Storage account already exists, skipping creation"
fi

# Create prompts container
az storage container create \
  --account-name yourblobstorage \
  --name prompts \
  --auth-mode login
```

## Environment Configuration

### Transition from Local to Azure

When moving from local development to Azure, update your `.env` file with the following changes:

#### Local Development Configuration (Starting Point)
```bash
# Local SQLite database
INGENIOUS_CHAT_HISTORY__DATABASE_TYPE=sqlite
INGENIOUS_CHAT_HISTORY__DATABASE_PATH=./.tmp/chat_history.db

# Local file storage
INGENIOUS_FILE_STORAGE__REVISIONS__ENABLE=true
INGENIOUS_FILE_STORAGE__REVISIONS__STORAGE_TYPE=local
```

#### Azure Production Configuration (Target)
```bash
# Cosmos DB for Chat History
INGENIOUS_CHAT_HISTORY__DATABASE_TYPE=cosmos

# Cosmos DB Configuration
INGENIOUS_COSMOS_SERVICE__URI=https://your-cosmos-account.documents.azure.com:443/
INGENIOUS_COSMOS_SERVICE__DATABASE_NAME=ingenious-db
INGENIOUS_COSMOS_SERVICE__API_KEY=your-primary-master-key-here
INGENIOUS_COSMOS_SERVICE__AUTHENTICATION_METHOD=token

# Azure Blob Storage for prompt templates (Method 1: Simplified)
INGENIOUS_PROMPT_TEMPLATE_PATH=azure://yourblobstorage/prompts
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=yourblobstorage;AccountKey=YOUR_KEY;BlobEndpoint=https://yourblobstorage.blob.core.windows.net/;...

# Alternative Method 2: Detailed file storage configuration
# INGENIOUS_FILE_STORAGE__REVISIONS__ENABLE=true
# INGENIOUS_FILE_STORAGE__REVISIONS__STORAGE_TYPE=azure
# INGENIOUS_FILE_STORAGE__REVISIONS__CONTAINER_NAME=prompts
# INGENIOUS_FILE_STORAGE__REVISIONS__PATH=./
# INGENIOUS_FILE_STORAGE__REVISIONS__URL=https://yourblobstorage.blob.core.windows.net
# INGENIOUS_FILE_STORAGE__REVISIONS__TOKEN=DefaultEndpointsProtocol=https;AccountName=yourblobstorage;AccountKey=YOUR_KEY;EndpointSuffix=core.windows.net

# Production Security: Disable built-in workflows
INGENIOUS_CHAT_SERVICE__ENABLE_BUILTIN_WORKFLOWS=false
```

### Complete Environment Variable Reference

| Variable | Local Value | Azure Value | Description |
|----------|-------------|-------------|-------------|
| `INGENIOUS_CHAT_HISTORY__DATABASE_TYPE` | `sqlite` | `cosmos` | Database backend type |
| `INGENIOUS_CHAT_HISTORY__DATABASE_PATH` | `./.tmp/chat_history.db` | (remove) | Local SQLite path |
| `INGENIOUS_COSMOS_SERVICE__URI` | (not needed) | `https://...documents.azure.com:443/` | Cosmos DB endpoint |
| `INGENIOUS_COSMOS_SERVICE__DATABASE_NAME` | (not needed) | `ingenious-db` | Cosmos DB database name |
| `INGENIOUS_COSMOS_SERVICE__API_KEY` | (not needed) | `your-key` | Cosmos DB primary master key |
| `INGENIOUS_COSMOS_SERVICE__AUTHENTICATION_METHOD` | (not needed) | `token` | Authentication method |
| `INGENIOUS_FILE_STORAGE__REVISIONS__ENABLE` | `false` | `true` | Enable cloud file storage |
| `INGENIOUS_FILE_STORAGE__REVISIONS__STORAGE_TYPE` | `local` | `azure` | Storage backend type |
| `INGENIOUS_FILE_STORAGE__REVISIONS__CONTAINER_NAME` | (not needed) | `prompts` | Blob container name |
| `INGENIOUS_FILE_STORAGE__REVISIONS__PATH` | `./` | `./` | Blob prefix (keeps templates under templates/) |
| `INGENIOUS_FILE_STORAGE__REVISIONS__URL` | (not needed) | `https://...` | Storage account URL |
| `INGENIOUS_FILE_STORAGE__REVISIONS__TOKEN` | (not needed) | `DefaultEndpoints...` | Storage connection string |
| `INGENIOUS_CHAT_SERVICE__ENABLE_BUILTIN_WORKFLOWS` | `true` | `false` | Production security setting |

### Get Azure Resource Information

```bash
# Get Cosmos DB keys
az cosmosdb keys list \
  --name your-cosmos-account \
  --resource-group your-rg-name \
  --type keys \
  --query "primaryMasterKey" -o tsv

# Get Cosmos DB endpoint URL
az cosmosdb show \
  --name your-cosmos-account \
  --resource-group your-rg-name \
  --query "documentEndpoint" \
  --output tsv

# Get storage account key
az storage account keys list \
  --account-name yourblobstorage \
  --resource-group your-rg-name \
  --query "[0].value" \
  --output tsv
```

## Upload Prompt Templates

Upload your prompt templates to the correct blob path:

```bash
# Upload templates for revision "quickstart-1"
for file in templates/prompts/quickstart-1/*.jinja; do
  filename=$(basename "$file")
  az storage blob upload \
    --account-name yourblobstorage \
    --container-name prompts \
    --name "templates/prompts/quickstart-1/$filename" \
    --file "$file" \
    --auth-mode key \
    --overwrite
done

# Alternative: upload the entire templates tree in one command while preserving folder structure
az storage blob upload-batch \
  --account-name yourblobstorage \
  --account-key "$(az storage account keys list --account-name yourblobstorage --resource-group your-rg-name --query '[0].value' -o tsv)" \
  --destination prompts \
  --destination-path templates \
  --source templates
```

## Azure Integration Verification

Once configuration is in place, validate that Cosmos DB and Blob Storage are wired up end-to-end.

```bash
# 1. Start the server with authentication enabled
export PYTHONPATH=$(pwd):$PYTHONPATH
KB_POLICY=prefer_azure uv run ingen serve --port 8000

# 2. Health check (no auth required)
curl http://localhost:8000/api/v1/health

# 3. Exercise a workflow with Basic Auth (replace credentials with your own values)
AUTH_HEADER=$(echo -n 'admin:SuperSecurePassword!' | base64)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $AUTH_HEADER" \
  -d @test_bike_insights.json

# 4. Verify prompts are being served from Azure Blob Storage
curl -H "Authorization: Basic $AUTH_HEADER" \
  http://localhost:8000/api/v1/prompts/list/quickstart-1
```

If the workflow succeeds and the prompt listing returns template filenames, the Cosmos DB and Blob integrations are working.

## Automatic Container Creation

Ingenious automatically creates the following containers in Cosmos DB:

- `chat_history` - Main chat messages
- `chat_history_summary` - Memory summaries
- `users` - User information
- `threads` - Thread metadata
- `steps` - Workflow steps
- `elements` - UI elements
- `feedbacks` - User feedback

No manual container creation is required.

## Production Security Configuration

### Disable Built-in Workflows (Recommended for Production)

For production deployments, you can disable the built-in workflows (`classification-agent`, `knowledge-base-agent`, `sql-manipulation-agent`) to expose only your custom workflows from `ingenious_extensions`:

```bash
# Add to your .env file for production security
INGENIOUS_CHAT_SERVICE__ENABLE_BUILTIN_WORKFLOWS=false
```

**Testing the Security Setting:**

```bash
# Test that built-in workflows are blocked (should return error)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'username:password' | base64)" \
  -d '{"user_prompt": "Test", "conversation_flow": "classification-agent", "thread_id": "test"}'

# Expected error response:
# {"detail":"Built-in workflow 'classification-agent' is disabled. Set INGENIOUS_CHAT_SERVICE__ENABLE_BUILTIN_WORKFLOWS=true to enable built-in workflows, or use a custom workflow from ingenious_extensions."}

# Custom workflows still work:
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'username:password' | base64)" \
  -d '{"user_prompt": "Test", "conversation_flow": "your-custom-workflow", "thread_id": "test"}'
```

## Verification

### 1. Validate Configuration

```bash
uv run ingen validate
```

Expected output: `All validations passed! Your Ingenious setup is ready.`

### 2. Start Server

```bash
uv run ingen serve --port 8000
```

### 3. Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-08-29T06:06:02.916027",
  "response_time_ms": 2.06,
  "components": {
    "configuration": "ok",
    "profile": "ok"
  },
  "version": "1.0.0",
  "uptime": "available"
}
```

### 4. Test Workflow with Azure Integrations

```bash
# Test bike-insights workflow (requires prompt templates uploaded)
echo '{
  "user_prompt": "{\"revision_id\": \"quickstart-1\", \"identifier\": \"test-001\", \"stores\": [{\"name\": \"Test Store\", \"location\": \"NSW\", \"bike_sales\": [{\"product_code\": \"MB-TREK-2021-XC\", \"quantity_sold\": 2, \"sale_date\": \"2023-04-01\", \"year\": 2023, \"month\": \"April\", \"customer_review\": {\"rating\": 4.5, \"comment\": \"Great bike\"}}], \"bike_stock\": []}]}",
  "conversation_flow": "bike-insights"
}' > test_azure.json

curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d @test_azure.json
```

Successful response indicates:
- Cosmos DB connection for chat history persistence
- Azure Blob prompt template loading
- Multi-agent workflow execution

## Troubleshooting

### Cosmos DB Connection Issues
- Verify Cosmos DB account is provisioned and accessible
- Check API key is correct (primary master key)
- Ensure endpoint URL format is correct: `https://account.documents.azure.com:443/`
- Verify network connectivity to Azure
- Confirm `AUTHENTICATION_METHOD=token` for API key auth

### Blob Storage Issues
- Verify storage account key is correct
- Ensure prompt templates uploaded to correct path: `templates/prompts/{revision_id}/`
- Check container permissions
- Verify connection string format

### Container Creation Issues
- Ensure Cosmos DB account has sufficient permissions
- Verify free tier limits are not exceeded
- Check that database exists before running workflows

### Performance Considerations
- Cosmos DB serverless mode: Pay only for what you use
- Cosmos DB free tier includes 1000 RU/s and 25GB storage
- Monitor RU consumption in Azure portal
- For high-throughput workloads, consider provisioned throughput mode

### Rate Limiting
Azure OpenAI free tier (S0) has token limits. Consider upgrading to Pay-as-you-go for production use.

## Cost Optimization

- **Cosmos DB Free Tier**: First 1000 RU/s and 25GB free per month
- **Cosmos DB Serverless (beyond free tier)**: ~$0.25 per million RUs + $0.25/GB storage/month
- **Storage Account (Standard_LRS)**: ~$0.02/GB/month
- **Azure OpenAI**: Pay per token usage

**Total minimal cost: $0-5/month for light usage** (often free with Cosmos DB free tier)

**Cost Comparison**:
- Cosmos DB Serverless: $0-5/month (recommended)
- Azure SQL Basic: ~$5/month (see [Azure SQL Deployment Guide](azure-sql-deployment.md))

For detailed local setup, see the [Getting Started Guide](../getting-started.md).

## Alternative Deployment Options

### Using Azure SQL Instead of Cosmos DB

If you require relational database features or have existing SQL infrastructure, see the [Azure SQL Deployment Guide](azure-sql-deployment.md) for instructions on using Azure SQL Database instead of Cosmos DB.

Key differences:
- **Cosmos DB** (recommended): Serverless pricing, automatic scaling, NoSQL flexibility, free tier available
- **Azure SQL**: Fixed monthly cost (~$5), relational features, T-SQL support, better for complex queries

## Next Steps

- [Configure Azure AI Search](azure-ai-search-deployment.md) for knowledge base workflows
- [Set up Authentication](azure-authentication.md) for production security
- [Create Custom Workflows](custom-workflows.md) for your specific use cases
