# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, or any other method with the owners of this repository before making a change.

## Environment setup

1. Prepare the Azure configuration file at `tests/integration/cloud-config-azure.ini`, a template of which is available in [the Ansible repo](https://github.com/ansible/ansible/blob/23a84902cb9599fe958a86e7a95520837964726a/test/lib/ansible_test/config/cloud-config-azure.ini.template). Populate your appropriate credential and resource group information.
    - The account or service principal must have permission (typically Owner) on the resource groups.
1. Ensure the resource groups defined in your configuration file are already created. Recommended region: **East US** (not all regions support all Azure features).
1. Prepare testing directory (necessary until [ansible/ansible#68499](https://github.com/ansible/ansible/issues/68499) is resolved):
    ```bash
    git init tests/staging
    ```
1. Unless you are running `ansible-test` inside a container (`--docker` flag), it is recommended you install Ansible and this repository's dependencies in a virtual environment:
    ```bash
    python3 -m venv venv
    . venv/bin/activate
    pip3 install -U pip
    pip3 install ansible
    pip3 install -r requirements-azure.txt
    pip3 install -r sanity-requirements-azure.txt
    ```

## Running tests

1. Build/install the collection:
    ```bash
    rm azure-azcollection-*.tar.gz && ansible-galaxy collection build . --force && ansible-galaxy collection install azure-azcollection-*.tar.gz -p tests/staging --force
    ```
1. Switch to the test environment directory where the collection installed:
    ```bash
    cd tests/staging/ansible_collections/azure/azcollection/
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

1. Please provide integration tests showing the changed behavior/functionality under `tests/integration/targets/<relevant-module>/tasks`.
1. Think about updating the documentation and examples for the changed module.
1. Please run a sanity check. Install prerequisites `pip install -r sanity-requirements-azure.txt`, run with `ansible-test sanity --color -v --junit`. Read more at https://docs.ansible.com/ansible/latest/dev_guide/testing_sanity.html.
1. There is a script `tests/utils/ado/ado.sh` for running tests inside an Azure DevOps pipeline. Unfortunately the pipeline and results are not visible for the public. You can perhaps adapt the parts of the script or use a small playbook to run the task list of the integration tests mentioned above.

## Release Process

1. Create a release branch from the target commit on dev branch.
1. Update version in [galaxy.yml](galaxy.yml) and release logs in [CHANGELOG.md](CHANGELOG.md).
1. Make sure the release branch is ready to release, merge the release branch into master branch.
1. Tag the master branch with new version number like `v*.*.*`, push to origin.
1. Release pipleline will automatically release the new version to galaxy.
1. Merge released changes back to `dev` branch.

## Release status

For each release details, you can refer to the [CHANGELOG](CHANGELOG.md) which contains the dates and significant changes in each minor release.
