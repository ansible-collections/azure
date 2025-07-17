#!/usr/bin/env bash

set -eux

ansible-playbook create_rg.yml
ansible-playbook -i inventory.yml main.yml  "$@"
ansible-playbook delete_rg.yml
