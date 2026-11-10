# Synapse workspace integration test

This target uses an existing Azure Synapse workspace to avoid creating
expensive workspace infrastructure. Supply these variables through
`tests/integration/integration_config.yml` or `-e @/path/to/private-vars.yml`:

- `synapse_test_resource_group`, `synapse_test_workspace`

The Azure principal must be allowed to read Synapse workspaces.

Run with:

```bash
ansible-test integration azure_rm_synapseworkspace --docker --allow-destructive \
  --python 3.12 -e @/path/to/private-vars.yml
```

The target reconciles the pre-existing workspace, reads it through the info
module, and asserts idempotency and check-mode behavior. It does not create
or delete the workspace.
