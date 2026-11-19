# Synapse workspace integration test

This target provisions everything it needs inside a dedicated resource group
(`{{ resource_group }}-synapseworkspace`): an ADLS Gen2 storage account, a
filesystem, and a Synapse workspace. It exercises workspace creation
(including the system-assigned managed identity), idempotent reconciliation,
tag updates and removal, the immutability of the create-only fields, the info
module (by name, by resource group, and across the subscription), check-mode
deletion, and deletion idempotency. The resource group is force-deleted in
the always block.

The Azure principal must be allowed to create Synapse workspaces and storage
accounts in the subscription.

Run with:

```bash
ansible-test integration azure_rm_synapseworkspace --docker --allow-destructive \
  --python 3.12
```
