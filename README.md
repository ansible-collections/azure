# Ansible collection for Azure
[![Doc](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://docs.ansible.com/ansible/latest/collections/azure/azcollection/index.html)
[![Code of conduct](https://img.shields.io/badge/code%20of%20conduct-Ansible-silver.svg)](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)
[![License](https://img.shields.io/badge/license-GPL%20v3.0-brightgreen.svg)](LICENSE)

This collection provides a series of Ansible modules and plugins for interacting with the [Azure](https://azure.microsoft.com).

Documentation of individual modules is [available in the Ansible docs site](https://docs.ansible.com/ansible/latest/collections/azure/azcollection/index.html#plugins-in-azure-azcollection)

## Included content

See the complete list of collection content in the [Plugin Index](https://docs.ansible.com/ansible/latest/collections/azure/azcollection/index.html#plugins-in-azure-azcollection).

## Communication

* Join the Ansible forum:
  * [Get Help](https://forum.ansible.com/c/help/6): get help or help others. Please use appropriate tags, for example `cloud`.
  * [Social Spaces](https://forum.ansible.com/c/chat/4): gather and interact with fellow enthusiasts.
  * [News & Announcements](https://forum.ansible.com/c/news/5): track project-wide announcements including social events.

* The Ansible [Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn): used to announce releases and important changes.

For more information about communication, see the [Ansible communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).


## Installation

It is recommended to run ansible in [Virtualenv](https://virtualenv.pypa.io/en/latest/)

## Requirements

- ansible version >= 2.16

To install Azure collection hosted in Galaxy:

```bash
ansible-galaxy collection install azure.azcollection
```

Install dependencies required by the collection (adjust path to collection if necessary):

```bash
pip3 install -r ~/.ansible/collections/ansible_collections/azure/azcollection/requirements.txt
```

Or, if you can't use pip, e.g. when you are on Ubuntu/Debian:

```bash
pipx runpip ansible install -r ~/.ansible/collections/ansible_collections/azure/azcollection/requirements.txt
```

To upgrade to the latest version of Azure collection:

```bash
ansible-galaxy collection install azure.azcollection --force
```

## Usage

### Playbooks

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

### Roles

For existing Ansible roles, please also reference the full namespace, collection name, and modules name which used in tasks instead of just modules name.

### Plugins

To use a plugin from Azure collection, please reference the full namespace, collection name, and plugins name that you want to use:

```yaml
---
plugin: azure.azcollection.azure_rm
include_vm_resource_groups:
  - ansible-inventory-test-rg
auth_source: auto
```

## Contributing

There are many ways in which you can participate in the project, for example:

- Submit bugs and feature requests, and help us verify as they are checked in
- Review source code changes
- Review the documentation and make pull requests for anything from typos to new content
- If you are interested in fixing issues and contributing directly to the code base, please see the [CONTRIBUTING](https://github.com/ansible-collections/azure/blob/dev/CONTRIBUTING.md) document

## Release notes

See the [Changelog](https://github.com/ansible-collections/azure/blob/dev/CHANGELOG.md)

## License

GNU General Public License v3.0

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
