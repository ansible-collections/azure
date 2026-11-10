# Databricks data-plane integration test

This target uses an existing Azure Databricks workspace to avoid creating
expensive workspace infrastructure. Supply these variables through
`tests/integration/integration_config.yml` or `-e @/path/to/private-vars.yml`:

- `databricks_test_resource_group`, `databricks_test_workspace`
- `databricks_test_spark_version` and `databricks_test_node_type` (optional; defaults are in tasks)

The Azure principal must be a workspace user allowed to create clusters and
notebooks.

Run with:

```bash
ansible-test integration azure_rm_databrickscluster --docker --allow-destructive \
  --python 3.12 -e @/path/to/private-vars.yml
```

The target creates a uniquely named cluster and notebook, removes them with
`state: absent` (which terminates and permanently deletes the cluster), and
asserts both are gone. It does not delete the workspace.
