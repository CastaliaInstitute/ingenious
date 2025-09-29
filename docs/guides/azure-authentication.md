# Azure Authentication Options

Ingenious supports four Azure authentication methods for Azure OpenAI, Azure AI Search, Cosmos DB, and Azure Blob Storage. If no method is specified, the default is default_credential.

## Methods

- default_credential
  - Uses Azure DefaultAzureCredential chain (env vars, managed identity, Azure CLI sign-in, etc.).
  - No extra fields required.
- token
  - Uses a raw key/token string (API key, admin key, SAS token, or connection string).
  - Required field depends on service (see Service mapping below).
- msi
  - Uses ManagedIdentityCredential.
  - If client_id is set, uses user-assigned identity; otherwise uses system-assigned.
- client_id_and_secret
  - Uses ClientSecretCredential (service principal).
  - Requires client_id, client_secret, tenant_id.

## Service mapping and required settings

- Azure OpenAI
  - token: INGENIOUS_MODELS__N__API_KEY
  - default_credential/msi/client_id_and_secret: provide INGENIOUS_MODELS__N__BASE_URL and API_VERSION; identity is resolved automatically.
- Azure AI Search
  - token: INGENIOUS_AZURE_SEARCH_SERVICES__N__KEY
  - default_credential/msi/client_id_and_secret: supported by SDK when permissioned; set endpoint and index name.
- Cosmos DB
  - token: INGENIOUS_COSMOS_SERVICE__API_KEY
  - default_credential/msi/client_id_and_secret: requires proper RBAC on the account; set URI and database name.
- Azure Blob Storage
  - token: INGENIOUS_FILE_STORAGE__REVISIONS__TOKEN or INGENIOUS_FILE_STORAGE__DATA__TOKEN
    - Can be SAS token or full connection string; set corresponding URL when using SAS.
  - default_credential/msi/client_id_and_secret: set URL and ensure RBAC (e.g., Storage Blob Data Contributor).

## Choosing a method

- Omit authentication_method to use default_credential.
- Provide only a token/key to use token automatically.
- Provide only client_id to prefer msi (user-assigned). Without client_id, msi uses system-assigned.
- Provide client_id, client_secret, tenant_id to use client_id_and_secret.

## Examples by method

### default_credential (no auth env required)

- Do not set any authentication variables; omitting
  `AUTHENTICATION_METHOD` defaults to `default_credential`.
- Provide only the service-specific settings like endpoints and names.

- Azure OpenAI
  - INGENIOUS_MODELS__0__BASE_URL=https://`region`.api.cognitive.microsoft.com/
  - INGENIOUS_MODELS__0__API_VERSION=2024-12-01-preview

- Azure AI Search
  - INGENIOUS_AZURE_SEARCH_SERVICES__0__ENDPOINT=https://`service`.search.windows.net
  - INGENIOUS_AZURE_SEARCH_SERVICES__0__INDEX_NAME=knowledge-base

- Cosmos DB
  - INGENIOUS_CHAT_HISTORY__DATABASE_TYPE=cosmos
  - INGENIOUS_COSMOS_SERVICE__URI=https://`account`.documents.azure.com:443/
  - INGENIOUS_COSMOS_SERVICE__DATABASE_NAME=ingenious-db

- Azure Blob Storage
  - INGENIOUS_FILE_STORAGE__REVISIONS__STORAGE_TYPE=azure
  - INGENIOUS_FILE_STORAGE__REVISIONS__URL=https://`account`.blob.core.windows.net

### token (API/admin key, SAS, connection string)

- Azure OpenAI
  - INGENIOUS_MODELS__0__AUTHENTICATION_METHOD=token
  - INGENIOUS_MODELS__0__API_KEY=...
  - INGENIOUS_MODELS__0__BASE_URL=https://`region`.api.cognitive.microsoft.com/
  - INGENIOUS_MODELS__0__API_VERSION=2024-12-01-preview

- Azure AI Search
  - INGENIOUS_AZURE_SEARCH_SERVICES__0__AUTHENTICATION_METHOD=token
  - INGENIOUS_AZURE_SEARCH_SERVICES__0__KEY=...
  - INGENIOUS_AZURE_SEARCH_SERVICES__0__ENDPOINT=https://`service`.search.windows.net
  - INGENIOUS_AZURE_SEARCH_SERVICES__0__INDEX_NAME=knowledge-base

- Cosmos DB (account key)
  - INGENIOUS_CHAT_HISTORY__DATABASE_TYPE=cosmos
  - INGENIOUS_COSMOS_SERVICE__AUTHENTICATION_METHOD=token
  - INGENIOUS_COSMOS_SERVICE__URI=https://`account`.documents.azure.com:443/
  - INGENIOUS_COSMOS_SERVICE__DATABASE_NAME=ingenious-db
  - INGENIOUS_COSMOS_SERVICE__API_KEY=...

- Azure Blob Storage (SAS or connection string)
  - INGENIOUS_FILE_STORAGE__REVISIONS__AUTHENTICATION_METHOD=token
  - INGENIOUS_FILE_STORAGE__REVISIONS__TOKEN=...
  - INGENIOUS_FILE_STORAGE__REVISIONS__URL=https://`account`.blob.core.windows.net  # when using SAS

### msi (Managed Identity)

- System-assigned MI (no client_id)
  - Azure OpenAI
    - INGENIOUS_MODELS__0__AUTHENTICATION_METHOD=msi
    - INGENIOUS_MODELS__0__BASE_URL=https://`region`.api.cognitive.microsoft.com/
    - INGENIOUS_MODELS__0__API_VERSION=2024-12-01-preview
  - Azure AI Search
    - INGENIOUS_AZURE_SEARCH_SERVICES__0__AUTHENTICATION_METHOD=msi
    - INGENIOUS_AZURE_SEARCH_SERVICES__0__ENDPOINT=https://`service`.search.windows.net
    - INGENIOUS_AZURE_SEARCH_SERVICES__0__INDEX_NAME=knowledge-base
  - Cosmos DB
    - INGENIOUS_CHAT_HISTORY__DATABASE_TYPE=cosmos
    - INGENIOUS_COSMOS_SERVICE__AUTHENTICATION_METHOD=msi
    - INGENIOUS_COSMOS_SERVICE__URI=https://`account`.documents.azure.com:443/
    - INGENIOUS_COSMOS_SERVICE__DATABASE_NAME=ingenious-db
  - Azure Blob Storage
    - INGENIOUS_FILE_STORAGE__REVISIONS__STORAGE_TYPE=azure
    - INGENIOUS_FILE_STORAGE__REVISIONS__AUTHENTICATION_METHOD=msi
    - INGENIOUS_FILE_STORAGE__REVISIONS__URL=https://`account`.blob.core.windows.net

- User-assigned MI (add client_id)
  - Add: `...__CLIENT_ID=your-user-assigned-mi-client-id` to the lines above.

### client_id_and_secret (Service Principal)

- Azure OpenAI
  - INGENIOUS_MODELS__0__AUTHENTICATION_METHOD=client_id_and_secret
  - INGENIOUS_MODELS__0__CLIENT_ID=...
  - INGENIOUS_MODELS__0__CLIENT_SECRET=...
  - INGENIOUS_MODELS__0__TENANT_ID=...
  - INGENIOUS_MODELS__0__BASE_URL=https://`region`.api.cognitive.microsoft.com/
  - INGENIOUS_MODELS__0__API_VERSION=2024-12-01-preview

- Azure AI Search
  - INGENIOUS_AZURE_SEARCH_SERVICES__0__AUTHENTICATION_METHOD=client_id_and_secret
  - INGENIOUS_AZURE_SEARCH_SERVICES__0__CLIENT_ID=...
  - INGENIOUS_AZURE_SEARCH_SERVICES__0__CLIENT_SECRET=...
  - INGENIOUS_AZURE_SEARCH_SERVICES__0__TENANT_ID=...
  - INGENIOUS_AZURE_SEARCH_SERVICES__0__ENDPOINT=https://`service`.search.windows.net
  - INGENIOUS_AZURE_SEARCH_SERVICES__0__INDEX_NAME=knowledge-base

- Cosmos DB
  - INGENIOUS_CHAT_HISTORY__DATABASE_TYPE=cosmos
  - INGENIOUS_COSMOS_SERVICE__AUTHENTICATION_METHOD=client_id_and_secret
  - INGENIOUS_COSMOS_SERVICE__CLIENT_ID=...
  - INGENIOUS_COSMOS_SERVICE__CLIENT_SECRET=...
  - INGENIOUS_COSMOS_SERVICE__TENANT_ID=...
  - INGENIOUS_COSMOS_SERVICE__URI=https://`account`.documents.azure.com:443/
  - INGENIOUS_COSMOS_SERVICE__DATABASE_NAME=ingenious-db

- Azure Blob Storage
  - INGENIOUS_FILE_STORAGE__REVISIONS__STORAGE_TYPE=azure
  - INGENIOUS_FILE_STORAGE__REVISIONS__AUTHENTICATION_METHOD=client_id_and_secret
  - INGENIOUS_FILE_STORAGE__REVISIONS__CLIENT_ID=...
  - INGENIOUS_FILE_STORAGE__REVISIONS__CLIENT_SECRET=...
  - INGENIOUS_FILE_STORAGE__REVISIONS__TENANT_ID=...
  - INGENIOUS_FILE_STORAGE__REVISIONS__URL=https://`account`.blob.core.windows.net

Notes

- For AAD-based methods (msi, client_id_and_secret), ensure the identity has
  the correct RBAC on each resource.
