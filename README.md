# Ansible collection: azure.azcollection
[![Doc](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://docs.ansible.com/ansible/latest/collections/azure/azcollection/index.html)
[![Code of conduct](https://img.shields.io/badge/code%20of%20conduct-Ansible-silver.svg)](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)
[![License](https://img.shields.io/badge/license-GPL%20v3.0-brightgreen.svg)](LICENSE)

This collection provides a series of Ansible modules and plugins for interacting with the [Azure](https://azure.microsoft.com).

Documentation of individual modules is [available in the Ansible docs site](https://docs.ansible.com/ansible/latest/collections/azure/azcollection/index.html#plugins-in-azure-azcollection)

## Description
Azure.azcollection is an Ansible collection designed to help users automate and manage their resources on the Microsoft Azure cloud platform. It offers a powerful set of modules for managing Azure's infrastructure services, such as virtual machines, storage accounts, network interfaces, resource groups, etc. As one of the Azure collections officially supported by Ansible, Azure.azCollection enables DevOps engineers, system administrators, and cloud architects to use Ansible to simplify the creation, configuration, management, and monitoring of azure resources.

## Included content
The azure.azcollection collection contains a series of modules, plugins, and support tools.
See the complete list of collection content in the [Plugin Index](https://docs.ansible.com/ansible/latest/collections/azure/azcollection/index.html#plugins-in-azure-azcollection).

* Module:
  * Resource Group Management (azure_rm_resourcegroup) : Used for creating, deleting, and updating Azure resource groups.
  * Virtual Machine Management (azure_rm_virtualmachine) : Manage the lifecycle of Azure virtual machines, including starting, stopping, creating, and deleting virtual machines.
  * Storage Account Management (azure_rm_storageaccount) : Create and manage Azure storage accounts.
  * Network Interface Management (azure_rm_networkinterface) : Manage the lifecycle of networkinterface cards (NICs).
  * Virtual Network Management (azure_rm_virtualnetwork) : Used for managing virtual networks and subnets.
  * Azure Authentication and Authorization: Supports authentication through service entities, Azure CLI, or environment variables.
  * Advanced resource management: such as Azure Kubernetes Service (AKS), Azure Front Door, Web applications, etc.

* Inventory Plugin:
  * azure_rm inventory – Azure Resource Manager inventory plugin
  * azure_kql inventory - Query VM details from Azure Resource Manager using Graph QL

* Lookup Plugins:
  * azure_keyvault_secret lookup – Read secret from Azure Key Vault.
  * azure_service_principal_attribute lookup – Look up Azure service principal attributes.

* Roles:
  This is a structured approach in Ansible for organizing and reusing automated tasks. Each character has its own directory structure, and related tasks, processors, templates, variables, etc. are separated, making the Playbook more modular and easier to maintain.

## Communication

* Join the Ansible forum:
  * [Get Help](https://forum.ansible.com/c/help/6): get help or help others. Please use appropriate tags, for example `cloud`.
  * [Social Spaces](https://forum.ansible.com/c/chat/4): gather and interact with fellow enthusiasts.
  * [News & Announcements](https://forum.ansible.com/c/news/5): track project-wide announcements including social events.

* The Ansible [Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn): used to announce releases and important changes.

For more information about communication, see the [Ansible communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Requirements

- ansible version >= 2.17
- python version >= 3.7

* Certification requirements
  * Service Principal (Service Principal Authentication): It is usually necessary to provide the Azure service principal credentials(subscription_id, tenant_id, client_id and secret).
  * Azure CLI: Users can log in through Azure CLI, and azure.azCollection will use this authentication for resource management.
  * Environment variables: Authentication can also be achieved by setting the environment variables related to Azure credentials.
    * export AZURE_SUBSCRIPTION_ID=<your-subscription-id>
    * export AZURE_CLIENT_ID=<your-client-id>
    * export AZURE_TENANT_ID=<your-tenant-id>
    * export AZURE_CLIENT_SECRET=<your-client-secret>

## Installation

Before using this collection, you need to install it with the Ansible Galaxy command-line tool.
It is recommended to run ansible in [Virtualenv](https://virtualenv.pypa.io/en/latest/)

To install Azure collection hosted in Galaxy:

```bash
ansible-galaxy collection install azure.azcollection
```

Install dependencies required by the collection (adjust path to collection if necessary):

```bash
pip3 install -r ~/.ansible/collections/ansible_collections/azure/azcollection/requirements.txt
```

Install the specified azure.azcollection version of the azure.azcollection. Use the following syntax to install version 3.7.0:

```bash
ansible-galaxy collection install azure.azcolleciton:==3.7.0
```

To upgrade to the latest version of Azure collection:

```bash
ansible-galaxy collection install azure.azcollection --upgrade
```

Check the installation version of azure.azcollection

```bash
ansible-galaxy collection list azure.azcollection
```

Or, if you can't use pip, e.g. when you are on Ubuntu/Debian:

```bash
pipx runpip ansible install -r ~/.ansible/collections/ansible_collections/azure/azcollection/requirements.txt
```

## Usage
Azure.azcollection provides multiple modules for managing Azure resources. Users can automate the creation, configuration, and management of various resources in Azure through Ansible Playbook. Through modular design, users can operate the Azure environment efficiently, reduce manual operations and enhance the degree of automation.

You can use this collection to manage all Azure resources ranging from infrastructure (such as virtual machines, networks, and storage) to more advanced services (such as Kubernetes and Azure Web applications).

### Use Cases

To use a module from Azure collection, please reference the full namespace, collection name, and modules name that you want to use:

```yaml
---
- name: Using Azure collection
  hosts: localhost
  tasks:
    - azure.azcollection.azure_rm_storageaccount:
        resource_group: myResourceGroup
        name: mystorageaccount
        account_type: Standard_LRS
```

Or you can add full namespace and collection name in the `collections` element:

```yaml
---
- name: Using Azure collection
  hosts: localhost
  collections:
    - azure.azcollection
  tasks:
    - azure_rm_storageaccount:
        resource_group: myResourceGroup
        name: mystorageaccount
        account_type: Standard_LRS
```

Testing:

Create a virtual machine
```yaml
- name: Using Azure collection
  hosts: localhost
  collections:
    - azure.azcollection
  vars:
    resource_group: myResourceGroup
    subnet_name: mySubnet
    network_name: myVirtualNetwork
    network: 10.42.8.0/24
    subnet: 10.42.8.0/28
  tasks:
    - name: Create a new resource group
      azure_rm_resourcegroup:
        name: "{{ resource_group }}"
        location: eastus

    - name: Create virtual network
      azure_rm_virtualnetwork:
        resource_group: "{{ resource_group }}"
        name: "{{ network_name }}"
        address_prefixes: "{{ network }}"

    - name: Create subnet
      azure_rm_subnet:
        resource_group: "{{ resource_group }}"
        name: "{{ subnet_name }}"
        address_prefix: "{{ subnet }}"
        virtual_network: "{{ network_name }}"

    - name: Create VM
      azure_rm_virtualmachine:
        resource_group: "{{ resource_group }}"
        name: "{{ vm_name }}"
        admin_username: "testuser"
        ssh_password_enabled: false
        open_ports:
          - 33
        ssh_public_keys:
          - path: /home/testuser/.ssh/authorized_keys
            key_data: "ssh-rsa AAAA ********* email@domain.com"
        vm_size: Standard_B1ms
        managed_disk_type: Standard_LRS
        image:
          offer: 0001-com-ubuntu-server-focal
          publisher: Canonical
          sku: 20_04-lts
          version: latest
      register: vm_output

    - name: Get VM facts
      azure_rm_virtualmachine_info:
        resource_group: "{{ resource_group }}"
        name: "{{ vm_name }}"
```

## Contributing

There are many ways in which you can participate in the project, for example:

- Submit bugs and feature requests, and help us verify as they are checked in
- Review source code changes
- Review the documentation and make pull requests for anything from typos to new content
- If you are interested in fixing issues and contributing directly to the code base, please see the [CONTRIBUTING](https://github.com/ansible-collections/azure/blob/dev/CONTRIBUTING.md) document

# Support
 Submit your questions or feature request on https://github.com/ansible-collections/azure.

## Release notes and Roadmap

See the [Changelog](https://github.com/ansible-collections/azure/blob/dev/CHANGELOG.md)


## Related Information
* Ansible official documentation
  * Relate link https://docs.ansible.com/. Provides a comprehensive Ansible user guide, including how to write Playbooks, manage variables, and use modules, etc.
* Azure.azcolleciton official documentation
  * Relate link https://docs.ansible.com/ansible/latest/collections/azure/azcollection/index.html. Provides detailed information about the collection module, including the functions, usage examples, parameter descriptions, etc. of each module.
* Azure official documentation
  * Relate link https://learn.microsoft.com/en-us/azure/?product=popular. Provided by Microsoft about the Azure platform, including how to create and manage Azure resources, configure security, and other contents.

## License Information

GNU General Public License v3.0

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
