# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, or any other method with the owners of this repository before making a change.

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
