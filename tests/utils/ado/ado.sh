#!/usr/bin/env bash

set -o pipefail -e

group="$1"

echo '--------------------------------------------'
echo "Install Python"
echo '--------------------------------------------'
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install -y \
    python"$2" \
    python3-dateutil \
    python3-pip

echo '--------------------------------------------'
echo "Setup venv"
echo '--------------------------------------------'
python$2 -m venv ~/ansible-venv
. ~/ansible-venv/bin/activate

echo '--------------------------------------------'
echo "Clone and setup ansible hacking env"
echo '--------------------------------------------'
git clone https://github.com/ansible/ansible.git ~/ansible
pushd ~/ansible > /dev/null
    if [ "$3" = "devel" ]
    then
        echo "The branch is devel"
    else
        git checkout "stable-$3"
    fi
    source hacking/env-setup
    pip install paramiko PyYAML Jinja2 httplib2 six
popd > /dev/null

echo '--------------------------------------------'
echo 'Copy and install our collection to a test directory'
echo '--------------------------------------------'
TEST_DIR="${HOME}/.ansible/ansible_collections/azure/azcollection"
mkdir -p "${TEST_DIR}"
cp -aT "${SHIPPABLE_BUILD_DIR}" "${TEST_DIR}"
cd "${TEST_DIR}"
mkdir -p shippable/testresults
pip install  -I -r "${TEST_DIR}/requirements.txt"
pip install  -I -r "${TEST_DIR}/sanity-requirements.txt"
pip install ansible-lint

timeout=180

# See: https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/integration-aliases.html
echo '--------------------------------------------'
echo "Disable non-chosen target"
echo '--------------------------------------------'
if [ "$4" = "all" ]
then
    echo "All module need test"
else
    path_dir="${TEST_DIR}/tests/integration/targets/"
    for item in "$path_dir"*
    do
        if [ "${item}" != "$path_dir""$4" ]
            echo " " >> "${item}"/aliases
            echo "disabled" >> "${item}"/aliases
        fi
    done
fi

echo '--------------------------------------------'
echo "List dependencies and ansible version"
echo '--------------------------------------------'
pip list
ansible --version

echo '--------------------------------------------'
echo 'Test'
echo '--------------------------------------------'
ansible-test env --dump --show --timeout "${timeout}" --color -v
if [ "sanity" = "${group}" ]
then
    ansible-lint --exclude "tests/integration/targets/inventory_azure/playbooks/vars.yml" --force-color -c "tests/lint/ignore-lint.txt"
    ansible-test sanity --color -v --junit
else
    ansible-test integration --color -v --retry-on-error "shippable/azure/group${group}/" --allow-destructive
fi
