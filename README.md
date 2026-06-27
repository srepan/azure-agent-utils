# azure-agent-utils

Utility scripts for Azure AI Foundry agent operations.

## List agents in a project

Run:

```bash
python list_agents.py \
  --endpoint "https://<resource>.services.ai.azure.com/api/projects/<project-name>" \
  --token "<access-token>"
```

Output is tab-separated columns:

- `id`
- `name`
- `model`
