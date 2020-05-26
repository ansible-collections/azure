#!/usr/bin/env bash

set -o pip3efail -eux

declare -a args
IFS='/:' read -ra args <<< "$1"

group="${args[0]}"

command -v python
python -V

command -v pip3
pip3 --version
pip3 list --disable-pip3-version-check

export PATH="${PWD}/bin:${PATH}"
export PYTHONIOENCODING="UTF-8"
export LC_ALL="en_US.utf-8"

pip3 install virtualenv
virtualenv --python /usr/bin/python3.7 ~/ansible-venv
#virtualenv --python /usr/bin/python2.7 ~/ansible-venv
set +ux
. ~/ansible-venv/bin/activate
set -ux

pip3 install ansible==2.9.0 --disable-pip3-version-check

TEST_DIR="${HOME}/.ansible/ansible_collections/azure/azcollection"
mkdir -p "${TEST_DIR}"
cp -aT "${SHIPPABLE_BUILD_DIR}" "${TEST_DIR}"
cd "${TEST_DIR}"
mkdir -p shippable/testresults
pip3 install  -I -r "${TEST_DIR}/requirements-azure.txt"

timeout=60
ansible --version

ansible-test env --dump --show --timeout "${timeout}" --color -v

cat <<EOF >> "${TEST_DIR}"/tests/integration/cloud-config-azure.ini
[default]
AZURE_CLIENT_ID:${AZURE_CLIENT_ID}
AZURE_SECRET:${AZURE_SECRET}
AZURE_SUBSCRIPTION_ID:${AZURE_SUBSCRIPTION_ID}
AZURE_TENANT:${AZURE_TENANT}
RESOURCE_GROUP:${RESOURCE_GROUP}
RESOURCE_GROUP_SECONDARY:${RESOURCE_GROUP_SECONDARY}
EOF

if [ "sanity" = "${group}" ]
then
    ansible-test sanity --color -v --junit --docker
else
    ansible-test integration --color -v --retry-on-error "shippable/azure/group${group}/" --allow-destructive
fi
