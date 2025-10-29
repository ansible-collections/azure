# Ansible collection for Azure
[![Doc](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://docs.ansible.com/ansible/latest/collections/azure/azcollection/index.html)
[![Code of conduct](https://img.shields.io/badge/code%20of%20conduct-Ansible-silver.svg)](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)
[![License](https://img.shields.io/badge/license-GPL%20v3.0-brightgreen.svg)](LICENSE)

## Description

This collection provides a series of Ansible modules and plugins for interacting with the [Azure](https://azure.microsoft.com).

Documentation of individual modules is [available at the Ansible Galaxy](https://galaxy.ansible.com/ui/repo/published/azure/azcollection/docs/)

## Requirements

- Python version >= 3.10
- Ansible version >= 2.16

## Installation

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:

```
ansible-galaxy collection install azure.azcollection
```

You can also include it in a requirements.yml file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
collections:
  - name: azure.azcollection
```

To upgrade the collection to the latest available version, run the following command:

```
ansible-galaxy collection install azure.azcollection --upgrade
```

You can also install a specific version of the collection. Use the following syntax to install version 1.0.0:

```
ansible-galaxy collection install azure.azcollection==1.0.0
```

See [using Ansible collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

---

After the collection is installed, please install the dependencies required by the collection (adjust path to collection if necessary):

```bash
pip install -r ~/.ansible/collections/ansible_collections/azure/azcollection/requirements.txt
```

## Use Cases

### Playbook

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

### Role

For existing Ansible roles, please also reference the full namespace, collection name, and modules name which used in tasks instead of just modules name.

### Plugin

To use a plugin from Azure collection, please reference the full namespace, collection name, and plugins name that you want to use:

```yaml
---
plugin: azure.azcollection.azure_rm
include_vm_resource_groups:
  - ansible-inventory-test-rg
auth_source: auto
```

## Testing

Test cases can be found under folder `tests`.

## Contributing

There are many ways in which you can participate in the project, for example:

- Submit bugs and feature requests, and help us verify as they are checked in
- Review source code changes
- Review the documentation and make pull requests for anything from typos to new content
- If you are interested in fixing issues and contributing directly to the code base, please see the [CONTRIBUTING](https://github.com/ansible-collections/azure/blob/dev/CONTRIBUTING.md) document

## Support

As Red Hat Ansible Certified Content, this collection is entitled to support through the Ansible Automation Platform (AAP) using the **Create issue** button on the top right corner. If a support case cannot be opened with Red Hat and the collection has been obtained either from Galaxy or GitHub, there may be community help available on the [Ansible Forum](https://forum.ansible.com/).

## Release Notes and Roadmap

See the [Changelog](https://github.com/ansible-collections/azure/blob/dev/CHANGELOG.md)


## Related Information

* [Ansible Official Documentation](https://docs.ansible.com/): A comprehensive Ansible user guide.
* [azure.azcolleciton Documentation](https://docs.ansible.com/ansible/latest/collections/azure/azcollection/index.html): Detailed information about the collection.
* [Azure Documentation](https://learn.microsoft.com/en-us/azure)

## License Information

GNU General Public License v3.0

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
