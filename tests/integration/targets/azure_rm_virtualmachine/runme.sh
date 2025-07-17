#!/usr/bin/env bash

set -eux

# Create a resource group for VM test
ansible-playbook -i inventory.yml create_rg.yml "$@"

ansible-playbook -i inventory.yml main.yml "$@"

# Force delete the resource group
ansible-playbook -i inventory.yml delete_rg.yml "$@"
