#!/usr/bin/env bash

set -o pipefail -eux

declare -a args
IFS='/:' read -ra args <<< "$1"

group="${args[0]}"

command -v python
python -V
if [ "$2" = "2.7" ]
then
    echo "The specified environment is Python2.7"
else
    alias pip='pip3'
    sudo apt update
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python"$2" -y
    sudo apt install python3-dateutil
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python"$2" 1
fi

command -v pip
pip --version
pip list --disable-pip-version-check

export PATH="${PWD}/bin:${PATH}"
export PYTHONIOENCODING="UTF-8"
export LC_ALL="en_US.utf-8"

pip install virtualenv
virtualenv --python /usr/bin/python"$2" ~/ansible-venv

set +ux
. ~/ansible-venv/bin/activate
set -ux

git clone https://github.com/ansible/ansible.git
cd "ansible"
if [ "$3" = "devel" ]
then
    echo "The branch is devel"
else
    git checkout "stable-$3"
fi
source hacking/env-setup
pip install paramiko PyYAML Jinja2  httplib2 six

TEST_DIR="${HOME}/.ansible/ansible_collections/azure/azcollection"
mkdir -p "${TEST_DIR}"
cp -aT "${SHIPPABLE_BUILD_DIR}" "${TEST_DIR}"
cd "${TEST_DIR}"
mkdir -p shippable/testresults

pip install  -I -r "${TEST_DIR}/requirements-azure.txt"
pip install  -I -r "${TEST_DIR}/sanity-requirements-azure.txt"

timeout=90

if [ "$4" = "all" ]
then
    echo "All module need test"
else
    path_dir="${TEST_DIR}/tests/integration/targets/"
    for item in "$path_dir"*
    do
        if [ "${item}" = "$path_dir""$4" ]
        then
            echo "PASS"
        else
            echo " " >> "${item}"/aliases
            echo "disabled" >> "${item}"/aliases
        fi
    done
fi
echo '--------------------------------------------'
pip list
ansible --version
echo '--------------------------------------------'

ansible-test env --dump --show --timeout "${timeout}" --color -v

cat <<EOF >> "${TEST_DIR}"/tests/integration/cloud-config-azure.ini
[default]
AZURE_CLIENT_ID:${AZURE_CLIENT_ID}
AZURE_SECRET:${AZURE_SECRET}
AZURE_SUBSCRIPTION_ID:${AZURE_SUBSCRIPTION_ID}
AZURE_SUBSCRIPTION_SEC_ID:${AZURE_SUBSCRIPTION_SEC_ID}
AZURE_TENANT:${AZURE_TENANT}
RESOURCE_GROUP:${RESOURCE_GROUP}
RESOURCE_GROUP_SECONDARY:${RESOURCE_GROUP_SECONDARY}
RESOURCE_GROUP_DATALAKE:${RESOURCE_GROUP_DATALAKE}
AZURE_PRINCIPAL_ID:${AZURE_PRINCIPAL_ID}
AZURE_MANAGED_BY_TENANT_ID:${AZURE_MANAGED_BY_TENANT_ID}
AZURE_ROLE_DEFINITION_ID:${AZURE_ROLE_DEFINITION_ID}
EOF

if [ "sanity" = "${group}" ]
then
    ansible-test sanity --color -v --junit
else
    ansible-test integration --color -v --retry-on-error "shippable/azure/group${group}/" --allow-destructive
fi
