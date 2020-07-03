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
        pip install ansible=="$3" --disable-pip-version-check
    fi
else
    if [ "$3" = "devel" ]
    then
        pip3 install git+https://github.com/ansible/ansible.git@devel  --disable-pip-version-check
    else
        pip3 install ansible=="$3" --disable-pip-version-check
    fi
fi

TEST_DIR="${HOME}/.ansible/ansible_collections/azure/azcollection"
mkdir -p "${TEST_DIR}"
cp -aT "${SHIPPABLE_BUILD_DIR}" "${TEST_DIR}"
cd "${TEST_DIR}"
mkdir -p shippable/testresults

if [ "$2" = "2.7" ]
then
    pip install  -I -r "${TEST_DIR}/requirements-azure.txt"
else
    pip3 install  -I -r "${TEST_DIR}/requirements-azure.txt"
fi

timeout=60

test_list=("azure_rm_acs" "azure_rm_aks" "azure_rm_appgateway" "azure_rm_appserviceplan" "azure_rm_automationaccount" "azure_rm_autoscale" "azure_rm_availabilityset" "azure_rm_azurefirewall" "azure_rm_batchaccount" "azure_rm_cdnprofile" "azure_rm_containerinstance" "azure_rm_containerregistry" "azure_rm_cosmosdbaccount" "azure_rm_deployment" "azure_rm_dnsrecordset" "azure_rm_dnszone" "azure_rm_functionapp" "azure_rm_gallery" "azure_rm_hdinsightcluster" "azure_rm_image" "azure_rm_iothub" "azure_rm_keyvault" "azure_rm_keyvaultkey" "azure_rm_keyvaultsecret" "azure_rm_loadbalancer" "azure_rm_manageddisk" "azure_rm_mariadbserver" "azure_rm_monitorlogprofile" "azure_rm_mysqlserver" "azure_rm_networkinterface" "azure_rm_postgresqlserver" "azure_rm_publicipaddress" "azure_rm_rediscache" "azure_rm_resource" "azure_rm_resourcegroup" "azure_rm_routetable" "azure_rm_securitygroup" "azure_rm_servicebus" "azure_rm_sqlserver" "azure_rm_storageaccount" "azure_rm_storageblob" "azure_rm_subnet" "azure_rm_trafficmanagerprofile" "azure_rm_virtualmachine" "azure_rm_virtualmachineextension" "azure_rm_virtualmachineimage_info" "azure_rm_virtualmachinescaleset" "azure_rm_virtualnetwork" "azure_rm_virtualnetworkgateway" "azure_rm_virtualnetworkpeering" "azure_rm_webapp" "azure_rm_workspace" "inventory_azure" "setup_azure" "azure_rm_acs" "azure_rm_aks" "azure_rm_appgateway" "azure_rm_appserviceplan" "azure_rm_automationaccount" "azure_rm_autoscale" "azure_rm_availabilityset" "azure_rm_azurefirewall" "azure_rm_batchaccount" "azure_rm_cdnprofile" "azure_rm_containerinstance" "azure_rm_containerregistry" "azure_rm_cosmosdbaccount" "azure_rm_deployment" "azure_rm_dnsrecordset" "azure_rm_dnszone" "azure_rm_functionapp" "azure_rm_gallery" "azure_rm_hdinsightcluster" "azure_rm_image" "azure_rm_iothub" "azure_rm_keyvault" "azure_rm_keyvaultkey" "azure_rm_keyvaultsecret" "azure_rm_loadbalancer" "azure_rm_manageddisk" "azure_rm_mariadbserver" "azure_rm_monitorlogprofile" "azure_rm_mysqlserver" "azure_rm_networkinterface" "azure_rm_postgresqlserver" "azure_rm_publicipaddress" "azure_rm_rediscache" "azure_rm_resource" "azure_rm_resourcegroup" "azure_rm_routetable" "azure_rm_securitygroup" "azure_rm_servicebus" "azure_rm_sqlserver" "azure_rm_storageaccount" "azure_rm_storageblob" "azure_rm_subnet" "azure_rm_trafficmanagerprofile" "azure_rm_virtualmachine" "azure_rm_virtualmachineextension" "azure_rm_virtualmachineimage_info" "azure_rm_virtualmachinescaleset" "azure_rm_virtualnetwork" "azure_rm_virtualnetworkgateway" "azure_rm_virtualnetworkpeering" "azure_rm_webapp" "azure_rm_workspace" "inventory_azure" "setup_azure")
if [ "$4" = "all" ]
then
    echo "All module need test"
else
    for item in ${test_list[*]}
    do
        if [ "${item}" = "$4" ]
        then
            echo "PASS"
        else
            echo "disabled" >> "${TEST_DIR}"/tests/integration/targets/"${item}"/aliases
        fi
    done
fi

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
