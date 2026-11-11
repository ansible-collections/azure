# Databricks data-plane integration test

This target is self-contained: it creates a Premium Databricks workspace in
`{{ resource_group }}` with `azure_rm_databricksworkspace`, runs the cluster
and notebook checks against it, and removes the workspace afterwards. No
extra variables are required, but workspace creation and deletion each take
a few minutes.

Optional variables (through `tests/integration/integration_config.yml` or
`-e`):

- `databricks_test_spark_version` and `databricks_test_node_type` (defaults are in tasks)

The Azure principal must be allowed to create Databricks workspaces in the
resource group; the principal that creates the workspace automatically has
data-plane access to it.

Run with:

```bash
ansible-test integration azure_rm_databrickscluster --docker --allow-destructive \
  --python 3.12
```

The target creates a uniquely named cluster and notebook, exports the
notebook to a temporary directory, removes the cluster with `state: absent`
(which permanently deletes it), and asserts both are gone before deleting
the workspace.
