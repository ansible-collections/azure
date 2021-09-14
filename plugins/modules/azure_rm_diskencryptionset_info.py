#!/usr/bin/python
#
# Copyright (c) 2021 Aparna Patil(@techcon65)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_diskencryptionset_info

version_added: "1.9.0"

short_description: Get disk encryption set facts

description:
    - Get facts for specific disk encryption set or all sets in a given resource group.

options:
    resource_group:
        description:
            - Name of the resource group.
        type: str
    name:
        description:
            - Name of the disk encryption set.
        type: str
    tags:
        description:
            - Limit the results by providing resource tags.
        type: dict

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Aparna Patil (@techcon65)

'''

EXAMPLES = '''
- name: Get facts for one disk encryption set
  azure_rm_diskencryptionset_info:
    resource_group: myResourceGroup
    name: mydiskencryptionset

- name: Get facts for all disk encryption sets in resource group
  azure_rm_diskencryptionset_info:
    resource_group: myResourceGroup
'''

RETURN = '''
diskencryptionsets:
    description:
        - Gets a list of disk encryption sets.
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "active_key": {
                "key_url": "https://myvault.vault.azure.net/keys/Key1/e65090b268ec4c3ba1a0f7a473005768",
                "source_vault": {
                    "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/
                           Microsoft.KeyVault/vaults/myvault"
                }
            },
            "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/
                   Microsoft.Compute/diskEncryptionSets/mydiskencryptionset",
            "identity": {
                "principal_id": "d3abec0a-5818-4bbd-8300-8014198124ca",
                "tenant_id": "7268bab5-aabd-44f9-915f-6bf864e879c6",
                "type": "SystemAssigned"
            },
            "location": "eastus",
            "name": "mydiskencryptionset",
            "provisioning_state": "Succeeded",
            "tags": {
                "key1": "value1"
            },
            "type": "Microsoft.Compute/diskEncryptionSets"
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.common import AzureMissingResourceHttpError, AzureHttpError
except Exception:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'DiskEncryptionSet'


class AzureRMDiskEncryptionSetInfo(AzureRMModuleBase):

    def __init__(self):

        # define user inputs into argument
        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            tags=dict(type='dict')
        )

        # store the results of the module operation
        self.results = dict(
            changed=False
        )

        self.name = None
        self.resource_group = None
        self.tags = None

        super(AzureRMDiskEncryptionSetInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        results = []
        # list the conditions and results to return based on user input
        if self.name is not None:
            # if there is set name is provided, return facts about that specific disk encryption set
            results = self.get_item()
        elif self.resource_group:
            # all the disk encryption sets listed in specific resource group
            results = self.list_resource_group()
        else:
            # all the disk encryption sets in a subscription
            results = self.list_items()

        self.results['diskencryptionsets'] = self.curated_items(results)

        return self.results

    def get_item(self):
        self.log('Get properties for {0}'.format(self.name))
        item = None
        results = []
        # get specific disk encryption set
        try:
            item = self.compute_client.disk_encryption_sets.get(self.resource_group, self.name)
        except CloudError:
            pass

        # serialize result
        if item and self.has_tags(item.tags, self.tags):
            results = [item]
        return results

    def list_resource_group(self):
        self.log('List all disk encryption sets for resource group - {0}'.format(self.resource_group))
        try:
            response = self.compute_client.disk_encryption_sets.list_by_resource_group(self.resource_group)
        except AzureHttpError as exc:
            self.fail("Failed to list for resource group {0} - {1}".format(self.resource_group, str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def list_items(self):
        self.log('List all disk encryption sets for a subscription ')
        try:
            response = self.compute_client.disk_encryption_sets.list()
        except AzureHttpError as exc:
            self.fail("Failed to list all items - {0}".format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def curated_items(self, raws):
        return [self.diskencryptionset_to_dict(item) for item in raws] if raws else []

    def diskencryptionset_to_dict(self, diskencryptionset):
        result = dict(
            id=diskencryptionset.id,
            name=diskencryptionset.name,
            location=diskencryptionset.location,
            tags=diskencryptionset.tags,
            active_key=diskencryptionset.active_key.as_dict(),
            provisioning_state=diskencryptionset.provisioning_state,
            identity=diskencryptionset.identity.as_dict(),
            type=diskencryptionset.type
        )
        return result


def main():
    AzureRMDiskEncryptionSetInfo()


if __name__ == '__main__':
    main()
