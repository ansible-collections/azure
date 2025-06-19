#!/usr/bin/env bash
set -e

# A number represents the group number, or "sanity"
GROUP_NO="$1"
PY_VER="$2"
ANSIBLE_VER="$3"
MODULE_NAME="$4"

die() {
    echo "$@" >&2
    exit 1
}

# Skip if running against a certain 
if [ "$GROUP_NO" != "sanity" ] && [ "$MODULE_NAME" != "all" ] ; then
    grep -w "shippable/azure/group${GROUP_NO}" "./tests/integration/targets/${MODULE_NAME}/aliases" > /dev/null || die "Module: $MODULE_NAME doesn't belong to this group ($GROUP_NO). Exit..."
fi

echo '--------------------------------------------'
echo "Setup venv (using the target python version)"
echo '--------------------------------------------'
python -m venv ~/ansible-venv
. ~/ansible-venv/bin/activate
python --version

echo '--------------------------------------------'
echo "Clone and setup ansible hacking env"
echo '--------------------------------------------'
git clone https://github.com/ansible/ansible.git ~/ansible
pushd ~/ansible > /dev/null
    if [ "$ANSIBLE_VER" = "devel" ]
    then
        echo "The branch is devel"
    else
        git checkout "stable-$ANSIBLE_VER"
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
if [ "$MODULE_NAME" = "all" ]
then
    echo "All module need test"
else
    path_dir="${TEST_DIR}/tests/integration/targets"
    for item in "$path_dir"/*
    do
        if [ "${item}" != "$path_dir/$MODULE_NAME" ]; then
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
if [ "sanity" = "${GROUP_NO}" ]
then
    ansible-lint --exclude "tests/integration/targets/inventory_azure/playbooks/vars.yml" --force-color -c "tests/lint/ignore-lint.txt"
    ansible-test sanity --color -v --junit
else
    # See: https://github.com/ansible/ansible/blob/23a84902cb9599fe958a86e7a95520837964726a/test/lib/ansible_test/config/cloud-config-azure.ini.template
    config_file="${TEST_DIR}"/tests/integration/cloud-config-azure.ini
    cat <<EOF >> "$config_file"
[default]
AZURE_CLIENT_ID:${AZURE_CLIENT_ID}
AZURE_SECRET:${AZURE_SECRET}
AZURE_SUBSCRIPTION_ID:${AZURE_SUBSCRIPTION_ID}
AZURE_SUBSCRIPTION_SEC_ID:${AZURE_SUBSCRIPTION_SEC_ID}
AZURE_TENANT:${AZURE_TENANT}
RESOURCE_GROUP:${RESOURCE_GROUP}
RESOURCE_GROUP_SECONDARY:${RESOURCE_GROUP_SECONDARY}
RESOURCE_GROUP_THIRD:${RESOURCE_GROUP_THIRD}
RESOURCE_GROUP_DATALAKE:${RESOURCE_GROUP_DATALAKE}
AZURE_PRINCIPAL_ID:${AZURE_PRINCIPAL_ID}
AZURE_MANAGED_BY_TENANT_ID:${AZURE_MANAGED_BY_TENANT_ID}
AZURE_ROLE_DEFINITION_ID:${AZURE_ROLE_DEFINITION_ID}
EOF
    ansible-test integration --color -v --retry-on-error "shippable/azure/group${GROUP_NO}/" --allow-destructive || { rm "$config_file"; die "failed to run integration test"; }
    rm "$config_file"
fi
