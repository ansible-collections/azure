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

# using host filters
ansible-playbook playbooks/empty_inventory_config.yml "$@"
ansible-playbook playbooks/create_inventory_config.yml "$@"  --extra-vars "template=filter.yml"
ansible-playbook playbooks/test_inventory_filter.yml "$@"

# using cache
ansible-playbook playbooks/empty_inventory_config.yml "$@"
ansible-playbook playbooks/create_inventory_config.yml "$@"  --extra-vars "template=cache.yml"
ansible-playbook playbooks/test_inventory_cache.yml "$@"
ansible-playbook playbooks/test_inventory_flush_part_1.yml "$@"
ansible-playbook playbooks/test_inventory_flush_part_2.yml "$@"
ansible-playbook --flush-cache playbooks/test_inventory_flush_part_3.yml "$@"
ansible-playbook playbooks/test_inventory_flush_part_3.yml "$@"


# teardown
ansible-playbook playbooks/teardown.yml "$@"
