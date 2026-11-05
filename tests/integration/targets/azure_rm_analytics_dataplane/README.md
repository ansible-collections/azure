# Databricks and Synapse data-plane integration test

This target uses existing Azure Databricks and Synapse workspaces to avoid
creating expensive workspace infrastructure. Supply these variables through
`tests/integration/integration_config.yml` or `-e @/path/to/private-vars.yml`:

- `databricks_test_resource_group`, `databricks_test_workspace`
- `synapse_test_resource_group`, `synapse_test_workspace`
- `azure_sql_server`, `azure_sql_database`, `azure_sql_user`, `azure_sql_password`
- `databricks_test_spark_version` and `databricks_test_node_type` (optional; defaults are in tasks)

The Azure principal must be a workspace user allowed to create clusters and
notebooks, and have permission to manage linked services in the Synapse
workspace. The SQL credentials are stored as an Ansible `no_log` parameter.

Run with:

```bash
ansible-test integration azure_rm_analytics_dataplane --docker --allow-destructive \
  --python 3.12 -e @/path/to/private-vars.yml
```

The target creates uniquely named compute and linked-service resources and
removes them in an `always` block. It does not delete either workspace.
