```markdown
Follow `@master-prompt.xml` for both `@soca/` and `@prompt-tuner/`.

## Environment

- Run the apps locally
- Use Azure resources for tests only

## Azure Constraints

- Use Azure CLI (`az cli`) for all operations
- **Resource Group:** Use `ingen-test` exclusively—do not create or modify resources outside this RG
- **Tagging:** Apply the tag `prompt-tuner` or `soca` to all resources based on which app they support
- **Provisioning:** Only create resources if they do not already exist in the `ingen-test` resource group
- **Cost:** Provision the cheapest viable SKUs/tiers needed to run tests
```
