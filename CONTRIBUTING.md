# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, or any other method with the owners of this repository before making a change.

## Environment setup

1. Prepare the Azure configuration file at `tests/integration/cloud-config-azure.ini`, a template of which is available in [the Ansible repo](https://github.com/ansible/ansible/blob/23a84902cb9599fe958a86e7a95520837964726a/test/lib/ansible_test/config/cloud-config-azure.ini.template). Populate your appropriate credential and resource group information.
    - The account or service principal must have permission (typically Owner) on the resource groups.
1. Ensure the resource groups defined in your configuration file are already created. Recommended region: **East US** (not all regions support all Azure features).
1. Prepare testing directory (necessary until [ansible/ansible#68499](https://github.com/ansible/ansible/issues/68499) is resolved):
    ```bash
    git init ansible_collections
    ```
1. Unless you are running `ansible-test` inside a container (`--docker` flag), it is recommended you install Ansible and this repository's dependencies in a virtual environment:
    ```bash
    python3 -m venv venv
    . venv/bin/activate
    pip3 install -U pip
    pip3 install ansible
    pip3 install -r requirements.txt
    pip3 install -r sanity-requirements.txt
    ```

## Running tests

1. Build/install the collection:
    ```bash
    rm -f azure-azcollection-*.tar.gz && ansible-galaxy collection build . --force && ansible-galaxy collection install azure-azcollection-*.tar.gz --force
    ```
1. Switch to the test environment directory where the collection installed:
    ```bash
    cd ansible_collections/azure/azcollection/
    ```
1. Run tests for the desired module(s):
    ```bash
    ansible-test integration azure_rm_storageaccount --allow-destructive -v
    ansible-test sanity azure_rm_storageaccount --color --junit -v
    ```

Additional `ansible-test` resources:
* [Integration tests](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html).
* [Testing Sanity](https://docs.ansible.com/ansible/latest/dev_guide/testing_sanity.html).

## Pull Request Process

1. Fork this project into your account if you are a first-time contributor.
1. Create a branch based on the latest `dev` branch, commit your changes on this branch.
1. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## Tests / sanity checks

1. Please provide integration tests showing the changed behavior/functionality under `tests/integration/targets/<relevant-module>/tasks`. See [Integration test layout](#integration-test-layout) below.
1. Think about updating the documentation and examples for the changed module.
1. If you added a new module, register it in `action_groups.all` in [meta/runtime.yml](meta/runtime.yml), keeping the list alphabetically sorted and free of duplicates.
1. If you added a new test target, add its name to the `MODULE_NAME` `values` list in [pr-pipelines.yml](pr-pipelines.yml) so it can be selected in the pipeline.
1. Please run a sanity check. Install prerequisites `pip install -r sanity-requirements.txt`, run with `ansible-test sanity --color -v --junit`. Read more at https://docs.ansible.com/ansible/latest/dev_guide/testing_sanity.html.
1. There is a script `tests/utils/ado/ado.sh` for running tests inside an Azure DevOps pipeline. Unfortunately the pipeline and results are not visible for the public. You can perhaps adapt the parts of the script or use a small playbook to run the task list of the integration tests mentioned above.

### Integration test layout

```
tests/integration/targets/azure_rm_<name>/
├── aliases
├── meta/main.yml
└── tasks/main.yml
```

`aliases`:

```
cloud/azure
shippable/azure/group<N>
destructive
```

`meta/main.yml`:

```yaml
dependencies:
  - setup_azure
```

`tasks/main.yml` — create a dedicated resource group, run the tests inside a `block`, and always clean up:

```yaml
- name: Create a resource group for the test
  azure.azcollection.azure_rm_resourcegroup:
    name: "{{ resource_group }}-<name>"
    location: eastus

- name: Test azure_rm_<name>
  block:
    # Variables
    - name: Set variables
      ansible.builtin.set_fact:
        rg: "{{ resource_group }}-<name>"
        rpfx: "{{ resource_group | hash('md5') | truncate(8, True, '') }}"

    # Create
    - name: Create resource (check mode)
      azure.azcollection.azure_rm_<name>:
        resource_group: "{{ rg }}"
        name: "res{{ rpfx }}"
      check_mode: true
      register: output

    - name: Assert check mode reports a change
      ansible.builtin.assert:
        that: output.changed

    - name: Create resource
      azure.azcollection.azure_rm_<name>:
        resource_group: "{{ rg }}"
        name: "res{{ rpfx }}"
        tags:
          key1: value1
      register: output

    - name: Assert resource is created
      ansible.builtin.assert:
        that: output.changed

    # Idempotence
    - name: Create resource again (idempotent)
      azure.azcollection.azure_rm_<name>:
        resource_group: "{{ rg }}"
        name: "res{{ rpfx }}"
        tags:
          key1: value1
      register: output

    - name: Assert no change
      ansible.builtin.assert:
        that: not output.changed

    # Update (properties and tags)
    - name: Update resource
      azure.azcollection.azure_rm_<name>:
        resource_group: "{{ rg }}"
        name: "res{{ rpfx }}"
        tags:
          key2: value2
      register: output

    - name: Assert resource is updated
      ansible.builtin.assert:
        that: output.changed

    # Read
    - name: Get resource info
      azure.azcollection.azure_rm_<name>_info:
        resource_group: "{{ rg }}"
        name: "res{{ rpfx }}"
      register: output

    - name: Assert returned values
      ansible.builtin.assert:
        that:
          - output.<name>s | length == 1
          - output.<name>s[0].tags.key1 == 'value1'
          - output.<name>s[0].tags.key2 == 'value2'

    # Delete
    - name: Delete resource
      azure.azcollection.azure_rm_<name>:
        resource_group: "{{ rg }}"
        name: "res{{ rpfx }}"
        state: absent
      register: output

    - name: Assert resource is deleted
      ansible.builtin.assert:
        that: output.changed

    - name: Delete resource again (idempotent)
      azure.azcollection.azure_rm_<name>:
        resource_group: "{{ rg }}"
        name: "res{{ rpfx }}"
        state: absent
      register: output

    - name: Assert no change
      ansible.builtin.assert:
        that: not output.changed

  # Cleanup
  always:
    - name: Delete the test resource group
      azure.azcollection.azure_rm_resourcegroup:
        name: "{{ resource_group }}-<name>"
        force_delete_nonempty: true
        state: absent
```

### Common variables and shared tasks

Use these instead of hardcoding values:

| Name | Source | Use |
|---|---|---|
| `resource_group`, `resource_group_secondary` | `cloud-config-azure.ini` (injected by `ansible-test`) | Base resource group names. Create test resource groups as `"{{ resource_group }}-<suffix>"`. |
| `azure_subscription_id`, `azure_tenant`, `azure_client_id` | `cloud-config-azure.ini` (injected by `ansible-test`) | Building resource IDs and tenant-scoped settings. |
| `azure_test_vm_size`, `azure_test_vm_size_large` | [tests/integration/integration_config.yml](tests/integration/integration_config.yml) | VM, scale set, and AKS node sizes. Never hardcode a VM size; change it once in this file. |
| `managed_identity.yml` | [tests/integration_common_tasks/](tests/integration_common_tasks/managed_identity.yml) | Creates or deletes user-assigned managed identities. |

`integration_config.yml` is loaded automatically for role targets. Targets that use `runme.sh` must pass it explicitly:

```bash
ansible-playbook main.yml -e @../../integration_config.yml "$@"
```

To use the shared managed identity tasks, add `needs/file/tests/integration_common_tasks/managed_identity.yml` to `aliases`, then:

```yaml
- name: Create identities array
  ansible.builtin.set_fact:
    managed_identity_ids: []

- name: Create user managed identities
  ansible.builtin.include_tasks: "{{ role_path }}/../../../integration_common_tasks/managed_identity.yml"
  vars:
    managed_identity_test_unique: '<name>'
    managed_identity_unique: "{{ item }}"
    managed_identity_action: 'create'  # use 'delete' during cleanup
    managed_identity_location: eastus
    new_resource_group: "{{ rg }}"
  with_items:
    - '1'
    - '2'
```

The created identity IDs are appended to `managed_identity_ids`.

## Release Process

1. Create a release branch from the target commit on dev branch.
1. Update version in [galaxy.yml](galaxy.yml) and release logs in [CHANGELOG.md](CHANGELOG.md).
1. Make sure the release branch is ready to release, merge the release branch into master branch.
1. Tag the master branch with new version number like `v*.*.*`, push to origin.
1. Release pipleline will automatically release the new version to galaxy.
1. Merge released changes back to `dev` branch.

## Release status

For each release details, you can refer to the [CHANGELOG](CHANGELOG.md) which contains the dates and significant changes in each minor release.
