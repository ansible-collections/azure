# Ansible collection for Azure

This collection provides a series of Ansible modules and plugins for interacting with the [Azure](https://azure.microsoft.com).

## Requirements

- ansible version >=2.9

## Installation

```
ansible-galaxy collection install azure.azcollection
```

## Usage

To use a module from Azure collection, please reference the full namespace, collection name, and modules name that you want to use:

```yaml
---
- name: Using Azure collection
  hosts: localhost
  tasks:
    - azure.azcollection.azure_rm_storageaccount:
        resource_group: myResourceGroup
        name: myStorageAccount
        account_type: Standard_LRS
```

Or you can add full namepsace and collecton name in the `collections` element:

```yaml
---
- name: Using Azure collection
  hosts: localhost
  collections:
    - azure.azcollection
  tasks:
    - azure_rm_storageaccount:
        resource_group: myResourceGroup
        name: myStorageAccount
        account_type: Standard_LRS
```

## Resource Supported

- azure_rm_deployment - Create or destroy Azure Resource Manager template deployments
- azure_rm_dnsrecordset - Create, delete and update DNS record sets and records
- azure_rm_dnsrecordset_facts - Get DNS Record Set facts
- azure_rm_dnszone - Manage Azure DNS zones
- azure_rm_dnszone_facts - Get DNS zone facts
- azure_rm_networkinterface - Manage Azure network interfaces
- azure_rm_networkinterface_facts - Get network interface facts
- azure_rm_publicipaddress - Manage Azure Public IP Addresses
- azure_rm_publicipaddress_facts - Get public IP facts
- azure_rm_securitygroup - Manage Azure network security groups
- azure_rm_securitygroup_facts - Get security group facts
- azure_rm_storageaccount - Manage Azure storage accounts
- azure_rm_storageaccount_facts - Get storage account facts
- azure_rm_subnet - Manage Azure subnets
- azure_rm_virtualmachine - Manage Azure virtual machines
- azure_rm_virtualmachine_facts - Get virtual machine facts
- azure_rm_virtualnetwork - Manage Azure virtual networks
- azure_rm_virtualnetwork_facts - Get virtual network facts