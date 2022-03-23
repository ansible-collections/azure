#!/usr/bin/python
#
# Copyright (c) 2021 Aparna Patil(@techcon65)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_diskencryptionset

version_added: "1.9.0"

short_description: Create, delete and update Disk encryption set

description:
    - Creates, deletes, and updates Disk encryption set.

options:
    resource_group:
        description:
            - The name of resource group.
        required: true
        type: str
    name:
        description:
            - The name of the disk encryption set.
        required: true
        type: str
    location:
        description:
            - Location for Disk encryption set. Defaults to location of resource group if not specified.
        type: str
    source_vault:
        description:
            - The name of source key vault containing encryption key.
        type: str
    key_url:
        description:
            - The url pointing to the encryption key to be used for disk encryption set.
        type: str
    state:
        description:
            - Assert the state of the disk encryption set. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Aparna Patil (@techcon65)
'''

EXAMPLES = '''
- name: create disk encryption set
  azure_rm_diskencryptionset:
    resource_group: myResourceGroup
    name: mydiskencryptionset
    source_vault: myvault
    key_url: https://myvault.vault.azure.net/keys/Key1/e65090b268ec4c3ba1a0f7a473005768
    state: present

- name: Update disk encryption set
  azure_rm_diskencryptionset:
    resource_group: myResourceGroup
    name: mydiskencryptionset
    source_vault: myvault
    key_url: https://myvault.vault.azure.net/keys/Key1/e65090b268ec4c3ba1a0f7a473005768
    state: present
    tags:
      key1: "value1"

- name: Delete disk encryption set
  azure_rm_diskencryptionset:
    resource_group: myResourceGroup
    name: mydiskencryptionset
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the Disk Encryption Set.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The disk encryption set ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/
                     Microsoft.Compute/diskEncryptionSets/mydiskencryptionset"
        name:
            description:
                - Disk encryption name.
            returned: always
            type: str
            sample: 'mydiskencryptionset'
        location:
            description:
                - The Azure Region where the resource lives.
            returned: always
            type: str
            sample: eastus
        tags:
            description:
                - Resource tags.
            returned: always
            type: list
            sample: [{"key1": "value1"}]
        active_key:
            description:
                - Reference to Key vault and key used for disk encryption set.
            returned: always
            type: dict
            sample: {
                "key_url": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                "source_vault": {
                    "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/
                           Microsoft.KeyVault/vaults/myvault"
                }
            }
        identity:
            description:
                - The managed identity for the disk encryption set.
            returned: always
            type: dict
            sample: {
                "principal_id": "d3abec0a-5818-4bbd-8300-8014198124ca",
                "tenant_id": "7268bab5-aabd-44f9-915f-6bf864e879c6",
                "type": "SystemAssigned"
            }
        provisioning_state:
            description:
                - The provisioning state of the resource.
            returned: always
            type: str
            sample: Succeeded
        type:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: "Microsoft.Compute/diskEncryptionSets"
'''

from ansible.module_utils.basic import _load_params
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, HAS_AZURE, \
    format_resource_id, normalize_location_name

try:
    from azure.core.polling import LROPoller
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDiskEncryptionSet(AzureRMModuleBase):

    def __init__(self):

        _load_params()
        # define user inputs from playbook
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            source_vault=dict(type='str'),
            key_url=dict(type='str', no_log=True),
            state=dict(choices=['present', 'absent'], default='present', type='str')
        )

        required_if = [
            ('state', 'present', ['source_vault', 'key_url'])
        ]

        self.results = dict(
            changed=False,
            state=dict()
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.source_vault = None
        self.key_url = None
        self.state = None
        self.tags = None

        super(AzureRMDiskEncryptionSet, self).__init__(self.module_arg_spec,
                                                       required_if=required_if,
                                                       supports_check_mode=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False
        results = dict()
        disk_encryption_set = None

        # retrieve resource group to make sure it exists
        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        self.location = normalize_location_name(self.location)

        if self.source_vault:
            source_vault = self.parse_resource_to_dict(self.source_vault)
            self.source_vault = format_resource_id(val=source_vault['name'],
                                                   subscription_id=source_vault['subscription_id'],
                                                   namespace='Microsoft.KeyVault',
                                                   types='vaults',
                                                   resource_group=source_vault['resource_group'])

        try:
            self.log('Fetching Disk encryption set {0}'.format(self.name))
            disk_encryption_set_old = self.compute_client.disk_encryption_sets.get(self.resource_group,
                                                                                   self.name)
            # serialize object into a dictionary
            results = self.diskencryptionset_to_dict(disk_encryption_set_old)
            if self.state == 'present':
                changed = False
                update_tags, results['tags'] = self.update_tags(results['tags'])
                if update_tags:
                    changed = True
                self.tags = results['tags']
                if self.source_vault != results['active_key']['source_vault']['id']:
                    changed = True
                    results['active_key']['source_vault']['id'] = self.source_vault
                if self.key_url != results['active_key']['key_url']:
                    changed = True
                    results['active_key']['key_url'] = self.key_url
            elif self.state == 'absent':
                changed = True

        except ResourceNotFoundError:
            if self.state == 'present':
                changed = True
            else:
                changed = False

        self.results['changed'] = changed
        self.results['state'] = results

        if self.check_mode:
            return self.results

        if changed:
            if self.state == 'present':
                identity = self.compute_models.EncryptionSetIdentity(type="SystemAssigned")
                # create or update disk encryption set
                disk_encryption_set_new = \
                    self.compute_models.DiskEncryptionSet(location=self.location,
                                                          identity=identity)
                if self.source_vault:
                    source_vault = self.compute_models.SourceVault(id=self.source_vault)
                    disk_encryption_set_new.active_key = \
                        self.compute_models.KeyVaultAndKeyReference(source_vault=source_vault,
                                                                    key_url=self.key_url)
                if self.tags:
                    disk_encryption_set_new.tags = self.tags
                self.results['state'] = self.create_or_update_diskencryptionset(disk_encryption_set_new)

            elif self.state == 'absent':
                # delete disk encryption set
                self.delete_diskencryptionset()
                self.results['state'] = 'Deleted'

        return self.results

    def create_or_update_diskencryptionset(self, disk_encryption_set):
        try:
            # create the disk encryption set
            response = \
                self.compute_client.disk_encryption_sets.begin_create_or_update(resource_group_name=self.resource_group,
                                                                                disk_encryption_set_name=self.name,
                                                                                disk_encryption_set=disk_encryption_set)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error creating or updating disk encryption set {0} - {1}".format(self.name, str(exc)))
        return self.diskencryptionset_to_dict(response)

    def delete_diskencryptionset(self):
        try:
            # delete the disk encryption set
            response = self.compute_client.disk_encryption_sets.begin_delete(resource_group_name=self.resource_group,
                                                                             disk_encryption_set_name=self.name)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error deleting disk encryption set {0} - {1}".format(self.name, str(exc)))
        return response

    def diskencryptionset_to_dict(self, diskencryptionset):
        result = diskencryptionset.as_dict()
        result['tags'] = diskencryptionset.tags
        return result


def main():
    AzureRMDiskEncryptionSet()


if __name__ == '__main__':
    main()
