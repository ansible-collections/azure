azure_arc
==================

A role to Configure an Azure ARC Machine.  Once the agent is installed and run
it will register the host in the **azure_arc_resource_group** requested.

Setting **azure_arc_state** to `absent` offboards the host instead: the agent is
disconnected from Azure (deleting the server resource) and removed from the
host.

Requirements
------------

* Azure User Account with valid permission

Role Variables
--------------

* **azure_arc_state**: Whether the Azure Arc host should be `present` (onboard, default) or `absent` (disconnect and remove the agent). `absent` requires the same Azure credentials as onboarding, with permission to delete the Azure Arc-enabled server resource.
* **azure_arc_resource_group**: The resource group that the host will be registered in.
* **azure_arc_cloud**: The Azure cloud to use. Default `AzureCloud`
* **azure_arc_location**: The location to use. Default `The location of the resource_group`
* **azure_arc_tenant_id**: Azure tenant id.
* **azure_arc_subscription_id**: Azure subscription id.
* **azure_arc_tags**: Dictionary of tags to apply to the Arc Host entry in Azure. Default: `{archost: "true"}`
* **desired_version**: Desired version of the azcmagent. When set and the installed agent version differs, the role upgrades (or downgrades) the agent to this version while keeping the host connected. On Linux this can be a partial version (for example `1.56`) or a full version (for example `1.56.03167.593`). On Windows this must be the major.minor version (for example `1.56`) used by the versioned MSI download links in the Azure Arc agent release notes. When unset, the agent is only installed when absent and is never upgraded. When the desired version is older than the installed agent, Debian/Ubuntu hosts have the agent package removed before the older version is installed (apt cannot downgrade the azcmagent package non-interactively), Windows hosts have the agent uninstalled first (the MSI cannot install an older version over a newer one), and RPM based Linux hosts downgrade in place. The connection state is kept in all cases, so the host stays connected. The Debian/Ubuntu package removal runs the package's prerm, which also removes the Guest Configuration agent directories (`/opt/GC_Service` and `/opt/GC_Ext`); installing the older version restores and re-enables both agents from the package payload, and because the package is removed without purging, the extension payloads in `/var/lib/GuestConfig` are kept.
* **altdownload**: Alternative download URL for the azcmagent package. Takes precedence over the `desired_version` based download locations.
* **proxy**: Object used to provide details for proxy setup if needed.  Contains the following:
  - * **hostname**: The hostname of the proxy server.
  - * **port**: The port that the proxy server is listening on.
* **azure_arc_force_local_only**: When true and `azure_arc_state` is `absent`, pass `--force-local-only` to `azcmagent disconnect` so the local agent is reset without deleting the server resource in Azure. Useful when the resource was already deleted in Azure. Default `false`
* **azure_arc_log_enabled**: Log success / failure to Azure for assistance with debugging (true by default, set to false to disable)

Limitations
------------

- NA

Dependencies
------------

- NA

Example Playbook
----------------

    - name: Deploy arc agent on arc_hosts
      hosts: arc_hosts
      tasks:
        - name: Configure Arc Hosts
          ansible.builtin.include_role:
            name: azure.azcollection.azure_arc

    - name: Offboard arc agent from arc_hosts
      hosts: arc_hosts
      tasks:
        - name: Remove Arc Hosts
          ansible.builtin.include_role:
            name: azure.azcollection.azure_arc
          vars:
            azure_arc_state: absent

Example Inventory
-----------------

    [arc_hosts]
    arc-host-01 ansible_user=admin
    arc-host-02 ansible_user=admin
    arc-host-03 ansible_user=admin
    WIN-3B6PDJQPRS4 ansible_user=vagrant ansible_shell_type=powershell

    [all:vars]
    ansible_ssh_extra_args='-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
    azure_arc_resource_group=YOURRESOURCEGROUP
    azure_arc_subscription_id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    azure_arc_tenant_id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

License
-------

GNU General Public License v3.0 or later

See [LICENCE](https://github.com/ansible-collections/azure/blob/dev/LICENSE) to see the full text.

Author Information
------------------

- Ansible Cloud Content Team
- Klaas Demter
