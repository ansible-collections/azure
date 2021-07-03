# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, or any other method with the owners of this repository before making a change.

## Environment setup

It is recommended you install Ansible and this repository's dependencies in a virtual environment:
```bash
python3 -m venv venv
. venv/bin/activate
pip3 install -U pip
pip3 install ansible
pip3 install -r requirements-azure.txt
pip3 install -r sanity-requirements-azure.txt
```

## Development and running tests

Being able to run tests requires an account or service principal with permission (typically Owner) in your Azure subscription.

1. Prepare the Azure configuration file at `tests/integration/cloud-config-azure.ini`, a template of which is available in [the Ansible repo](https://github.com/ansible/ansible/blob/23a84902cb9599fe958a86e7a95520837964726a/test/lib/ansible_test/config/cloud-config-azure.ini.template). Populate your appropriate credential and resource group name information.
1. Make the desired change(s) and then build/install the collection:
    ```bash
    rm azure-azcollection-*.tar.gz && ansible-galaxy collection build . --force && ansible-galaxy collection install azure-azcollection-*.tar.gz -p tests/staging --force
    ```
1. Switch to the directory where the collection installed.
    ```bash
    cd tests/staging/ansible_collections/azure/azcollection/
    ```
1. Run tests for the desired module(s):
    ```bash
    ansible-test integration azure_rm_storageaccount -v
    ```

## Pull Request Process

1. Fork this project into your account if you are a first-time contributor.
1. Create a branch based on the latest `dev` branch, commit your changes on this branch.
1. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## Release Process

1. Create a release branch from the target commit on dev branch.
1. Update version in [galaxy.yml](galaxy.yml) and release logs in [CHANGELOG.md](CHANGELOG.md).
1. Make sure the release branch is ready to release, merge the release branch into master branch.
1. Tag the master branch with new version number like `v*.*.*`, push to origin.
1. Release pipleline will automatically release the new version to galaxy.
1. Merge released changes back to `dev` branch.

## Release status

For each release details, you can refer to the [CHANGELOG](CHANGELOG.md) which contains the dates and significant changes in each minor release.
