#!/usr/bin/env bash

set -eux

# make sure inventory is empty at the begining of the tests
ansible-playbook playbooks/empty_inventory_config.yml "$@"

# create vm
ansible-playbook playbooks/setup.yml "$@"

export ANSIBLE_INVENTORY=test.azure_rm.yml

# using fully qualified name
ansible-playbook playbooks/create_inventory_config.yml "$@"  
ansible-playbook playbooks/test_inventory.yml "$@"

# using short name
ansible-playbook playbooks/empty_inventory_config.yml "$@"
ansible-playbook playbooks/create_inventory_config.yml "$@"  --extra-vars "template=basic2.yml"
ansible-playbook playbooks/test_inventory.yml "$@"


# teardown
ansible-playbook playbooks/teardown.yml "$@"
