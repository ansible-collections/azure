#!/usr/bin/env bash

set -o pipefail -eux

declare -a args
IFS='/:' read -ra args <<< "$1"

group="${args[0]}"

command -v python
python -V

if [ "$2" = "2.7" ]
then
    command -v pip
    pip --version
    pip list --disable-pip-version-check
else
    command -v pip3
    pip3 --version
    pip3 list --disable-pip-version-check
fi

export PATH="${PWD}/bin:${PATH}"
export PYTHONIOENCODING="UTF-8"
export LC_ALL="en_US.utf-8"

if [ "$2" = "2.7" ]
then
    pip install virtualenv
    virtualenv --python /usr/bin/python2.7 ~/ansible-venv
else
    pip3 install virtualenv
    virtualenv --python /usr/bin/python"$2" ~/ansible-venv
fi

set +ux
. ~/ansible-venv/bin/activate
set -ux

if [ "$2" = "2.7" ]
then
    if [ "$3" = "devel" ]
    then
        pip install git+https://github.com/ansible/ansible.git@devel  --disable-pip-version-check
    else
	git clone https://github.com/ansible/ansible.git
	cd "ansible"
	git checkout "stable-$3"
	source hacking/env-setup
	pip install paramiko PyYAML Jinja2  httplib2 six
    fi
else
    if [ "$3" = "devel" ]
    then
        pip3 install git+https://github.com/ansible/ansible.git@devel  --disable-pip-version-check
    else
	git clone https://github.com/ansible/ansible.git
	cd "ansible"
	git checkout "stable-$3"
	source hacking/env-setup
	pip3 install paramiko PyYAML Jinja2  httplib2 six
    fi
fi

TEST_DIR="${HOME}/.ansible/ansible_collections/azure/azcollection"
mkdir -p "${TEST_DIR}"
cp -aT "${SHIPPABLE_BUILD_DIR}" "${TEST_DIR}"
cd "${TEST_DIR}"
mkdir -p shippable/testresults

if [ "$2" = "2.7" ]
then
    pip install --upgrade pip
    pip install  -I -r "${TEST_DIR}/requirements-azure.txt"
    pip3 install setuptools
    pip3 install  -I -r "${TEST_DIR}/sanity-requirements-azure.txt"
    pip3 list
else
    pip3 install  -I -r "${TEST_DIR}/requirements-azure.txt"
    pip3 install  -I -r "${TEST_DIR}/sanity-requirements-azure.txt"
    pip3 list
fi

timeout=60

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
ansible --version
echo '--------------------------------------------'

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
    ansible-test sanity --color -v --junit
else
    ansible-test integration --color -v --retry-on-error "shippable/azure/group${group}/" --allow-destructive
fi
