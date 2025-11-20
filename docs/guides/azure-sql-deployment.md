# Azure SQL Deployment Guide

This guide provides step-by-step instructions for using Azure SQL Database as an alternative to Cosmos DB for chat history persistence in **Ingenious**.

> **Note**: Cosmos DB is the recommended default for production deployments due to its serverless pricing model and automatic scaling. Use Azure SQL if you have specific requirements for relational database features or existing SQL infrastructure.

## Prerequisites

- Azure CLI installed and authenticated
- Azure OpenAI resource (required)
- Azure subscription with appropriate permissions

## When to Use Azure SQL

Consider Azure SQL over Cosmos DB when you need:
- Relational database features (complex joins, transactions)
- Existing SQL Server expertise or tooling
- Integration with other SQL-based systems
- T-SQL stored procedures or advanced SQL features

For most use cases, Cosmos DB (the default) is recommended due to lower cost and automatic scaling.

## Minimal Azure Provisioning

### 1. Create Azure SQL Server

```bash
# Register the SQL resource provider if needed
if [ "$(az provider show --namespace Microsoft.Sql --query "registrationState" -o tsv 2>/dev/null)" != "Registered" ]; then
  az provider register --namespace Microsoft.Sql
fi

# Check if SQL Server exists first
SQL_EXISTS=$(az sql server show --name your-sql-server --resource-group your-rg-name 2>/dev/null)
if [ -z "$SQL_EXISTS" ]; then
  # Create SQL Server only if it doesn't exist
  # Note: Use simple alphanumeric passwords (no special characters) to avoid ODBC connection issues
  az sql server create \
    --name your-sql-server \
    --resource-group your-rg-name \
    --location eastus2 \
    --admin-user adminuser \
    --admin-password YourPassword123
else
  echo "SQL Server already exists, skipping creation"
fi

# Allow Azure services access
az sql server firewall-rule create \
  --resource-group your-rg-name \
  --server your-sql-server \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Allow your IP
MY_IP=$(curl -s ipinfo.io/ip)
az sql server firewall-rule create \
  --resource-group your-rg-name \
  --server your-sql-server \
  --name AllowMyIP \
  --start-ip-address "$MY_IP" \
  --end-ip-address "$MY_IP"
```

### 2. Create Database (Basic SKU)

```bash
# Create Database (Basic SKU - cheapest option at ~$5/month)
az sql db create \
  --resource-group your-rg-name \
  --server your-sql-server \
  --name ingenious-db \
  --service-objective Basic
```

### 3. Get Connection Information

```bash
# Get SQL server FQDN for connection string
az sql server show \
  --name your-sql-server \
  --resource-group your-rg-name \
  --query 'fullyQualifiedDomainName' \
  --output tsv

# Verify admin username
az sql server show \
  --name your-sql-server \
  --resource-group your-rg-name \
  --query 'administratorLogin' \
  --output tsv
```

## Environment Configuration

### Update .env File

Change your chat history database configuration from Cosmos DB to Azure SQL:

| Variable | Description | Example |
|----------|-------------|---------|
| `INGENIOUS_CHAT_HISTORY__DATABASE_TYPE` | Database type | `azuresql` |
| `INGENIOUS_AZURE_SQL_SERVICES__DATABASE_CONNECTION_STRING` | SQL connection string | See below |
| `INGENIOUS_AZURE_SQL_SERVICES__DATABASE_NAME` | Database name | `ingenious-db` |
| `INGENIOUS_AZURE_SQL_SERVICES__TABLE_NAME` | Table name | `chat_history` |

### Complete .env Configuration

```bash
# Change database type from cosmos to azuresql
INGENIOUS_CHAT_HISTORY__DATABASE_TYPE=azuresql

# Azure SQL Configuration
INGENIOUS_AZURE_SQL_SERVICES__DATABASE_CONNECTION_STRING=Driver={ODBC Driver 18 for SQL Server};Server=tcp:your-sql-server.database.windows.net,1433;Database=ingenious-db;Uid=adminuser;Pwd=YourPassword123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
INGENIOUS_AZURE_SQL_SERVICES__DATABASE_NAME=ingenious-db
INGENIOUS_AZURE_SQL_SERVICES__TABLE_NAME=chat_history

# Optional: Keep memory path for temporary files
INGENIOUS_CHAT_HISTORY__MEMORY_PATH=./.tmp
```

**Important**: Use simple alphanumeric passwords (no special characters like `!@#$%`) to avoid ODBC connection string parsing issues.

## Automatic Table Creation

Ingenious automatically creates the required tables in Azure SQL:

- `chat_history` - Main chat messages
- `chat_history_summary` - Memory summaries
- `users` - User information
- `threads` - Thread metadata
- `steps` - Workflow steps
- `elements` - UI elements
- `feedbacks` - User feedback

No manual table creation is required.

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
  "timestamp": "2025-08-29T07:14:46.522450",
  "response_time_ms": 2.7,
  "components": {
    "configuration": "ok",
    "profile": "ok"
  },
  "version": "1.0.0",
  "uptime": "available"
}
```

### 4. Test Workflow with Azure SQL

```bash
# Test bike-insights workflow
echo '{
  "user_prompt": "{\"revision_id\": \"quickstart-1\", \"identifier\": \"test-001\", \"stores\": [{\"name\": \"Test Store\", \"location\": \"NSW\", \"bike_sales\": [{\"product_code\": \"MB-TREK-2021-XC\", \"quantity_sold\": 2, \"sale_date\": \"2023-04-01\", \"year\": 2023, \"month\": \"April\", \"customer_review\": {\"rating\": 4.5, \"comment\": \"Great bike\"}}], \"bike_stock\": []}]}",
  "conversation_flow": "bike-insights"
}' > test_sql.json

curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d @test_sql.json
```

### 5. Verify Data Persistence

```bash
# Connect and verify chat history rows
uv run python <<PY
import pyodbc
conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:your-sql-server.database.windows.net,1433;"
    "Database=ingenious-db;Uid=adminuser;Pwd=YourPassword123;"
    "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM chat_history")
print("chat_history rows:", cursor.fetchone()[0])
cursor.close()
conn.close()
PY
```

Successful response indicates:
- Azure SQL connection for chat history persistence
- Automatic table creation and data storage
- Multi-agent workflow execution

## Migration from Cosmos DB

To migrate from Cosmos DB to Azure SQL:

1. **Backup existing data** (optional):
   - Export Cosmos DB data if needed for archival

2. **Update configuration** as described above

3. **Restart application** - SQL tables will be created automatically

4. **Verify migration** by testing workflows

Note: Direct data migration tools are not currently provided. For production migrations, consider implementing custom migration scripts.

## Troubleshooting

### Connection Issues
- Verify SQL Server is provisioned and accessible
- Check firewall rules allow your IP
- Ensure connection string format is correct
- Verify password doesn't contain special characters

### ODBC Driver Issues
- Install ODBC Driver 18 for SQL Server
- On macOS: `brew install msodbcsql18`
- On Ubuntu: Follow [Microsoft's installation guide](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server)

### Authentication Issues
- Confirm admin username and password are correct
- Verify SQL Server firewall rules are configured
- Check that database exists

### Table Creation Issues
- Ensure SQL account has appropriate permissions
- Verify database exists before running workflows
- Check error logs for specific SQL errors

### Performance Considerations
- Basic tier (5 DTUs) suitable for development/testing
- Monitor DTU usage in Azure portal
- Consider upgrading to Standard tier for production workloads
- Add indexes for frequently queried columns

## Cost Optimization

- **Azure SQL Basic (5 DTUs)**: ~$5/month
- **Additional DTUs**: Scale based on usage
- **Storage**: Included in Basic tier (2GB max)

Total cost for minimal usage: ~$5/month for Basic tier.

**Comparison with Cosmos DB**:
- Cosmos DB Free Tier: First 1000 RU/s and 25GB free
- Cosmos DB Serverless: Pay only for what you use
- **Recommendation**: Use Cosmos DB for lower costs in most scenarios

For the default Cosmos DB deployment, see the [Complete Azure Deployment Guide](complete-azure-deployment.md).
