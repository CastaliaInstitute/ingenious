# Deploy to ingen-test Resource Group

Deploy SoCa or Prompt Tuner applications to Azure using the ingen-test resource group.

## Arguments

- `$ARGUMENTS` - Application to deploy: `soca`, `prompt-tuner`, or `all` (required)

## Instructions

1. **Determine which application to deploy** from `$ARGUMENTS`:
   - `soca` - Deploy SoCa application only
   - `prompt-tuner` - Deploy Prompt Tuner application only
   - `all` - Deploy both applications

2. **Resource Group**: Always use `ingen-test`. Do NOT create or use any other resource group.

3. **Resource Tagging**: Apply appropriate tags to all resources:
   - For SoCa: `app=soca`
   - For Prompt Tuner: `app=prompt-tuner`

4. **Provisioning Rules**:
   - Only provision resources if they don't already exist
   - Use the CHEAPEST tier available for all resources:
     - Static Web Apps: Free tier
     - Container Apps: Consumption plan (minReplicas=1, maxReplicas=3)
     - Container Apps Environment: Consumption workload profile
     - Container Registry: Basic tier

5. **Deployment Steps**:

### For SoCa:

```bash
# Check if resources exist
az staticwebapp show --name soca-frontend --resource-group ingen-test 2>/dev/null || \
  az staticwebapp create --name soca-frontend --resource-group ingen-test --location "Australia East" --sku Free --tags app=soca

# Build and deploy frontend
cd soca/frontend
npm run build
SOCA_TOKEN=$(az staticwebapp secrets list --name soca-frontend --resource-group ingen-test --query "properties.apiKey" -o tsv)
npx @azure/static-web-apps-cli deploy ./dist --deployment-token "$SOCA_TOKEN" --env production

# Deploy backend to Container Apps
cd ../backend
az containerapp up --name soca-backend --resource-group ingen-test --environment soca-env --source . --tags app=soca
az containerapp update --name soca-backend --resource-group ingen-test --min-replicas 1 --max-replicas 3
```

### For Prompt Tuner:

```bash
# Check if resources exist
az staticwebapp show --name prompt-tuner-frontend --resource-group ingen-test 2>/dev/null || \
  az staticwebapp create --name prompt-tuner-frontend --resource-group ingen-test --location "Australia East" --sku Free --tags app=prompt-tuner

# Build and deploy frontend
cd prompt-tuner/frontend
npm run build
PT_TOKEN=$(az staticwebapp secrets list --name prompt-tuner-frontend --resource-group ingen-test --query "properties.apiKey" -o tsv)
npx @azure/static-web-apps-cli deploy ./dist --deployment-token "$PT_TOKEN" --env production

# Deploy backend to Container Apps
cd ../backend
az containerapp up --name prompttuner-backend --resource-group ingen-test --environment soca-env --source . --tags app=prompt-tuner
az containerapp update --name prompttuner-backend --resource-group ingen-test --min-replicas 1 --max-replicas 3
```

6. **Verification**:
   After deployment, verify the applications are running:
   ```bash
   # Check frontend URLs
   az staticwebapp show --name soca-frontend --resource-group ingen-test --query defaultHostname -o tsv
   az staticwebapp show --name prompt-tuner-frontend --resource-group ingen-test --query defaultHostname -o tsv

   # Check backend health
   curl https://soca-backend.kindsea-9799773a.australiaeast.azurecontainerapps.io/health
   curl https://prompttuner-backend.kindsea-9799773a.australiaeast.azurecontainerapps.io/health
   ```

## Cost Optimization

- Static Web Apps Free tier: $0/month
- Container Apps Consumption: Pay only for active use (first 2M requests free)
- Container Registry Basic: ~$5/month
- Total estimated cost: <$10/month for light usage

## Usage

```
/deploy-ingen-test soca          # Deploy SoCa only
/deploy-ingen-test prompt-tuner  # Deploy Prompt Tuner only
/deploy-ingen-test all           # Deploy both applications
```
