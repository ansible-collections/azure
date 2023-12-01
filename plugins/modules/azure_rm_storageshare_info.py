#!/usr/bin/python
#
# Copyright (c) 2021 Andrii Bilorus <andrii.bilorus@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_storageshare_info
version_added: "1.8.0"
short_description: Get Azure storage file share info
description:
    - Get facts for storage file share.
options:
    resource_group:
        description:
            - Name of the resource group to use.
        required: true
        type: str
    name:
        description:
            - Name of the storage file share.
        type: str
        required: false
    account_name:
        description:
            - Name of the parent storage account for the storage file share.
        required: true
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Andrii Bilorus (@ewscat)
'''

EXAMPLES = '''
---
- name: Get storage share details
  azure_rm_storageshare_info:
    name: testShare
    resource_group: myResourceGroup
    account_name: testStorageAccount


- name: Get all storage file shares in storage account
  azure_rm_storageshare:
    resource_group: myResourceGroup
    account_name: testStorageAccount
'''

RETURN = '''
state:
    description:
        - Facts about the current state of the storage file share
    returned: always
    type: complex
    contains:
            id:
                description:
                    - Resource ID of the storage file share
                sample: "/subscriptions/9e700857-1631-4d8a-aed5-908520ede375/resourceGroups/myResourceGroup/providers/Microsoft.Storage/
                         storageAccounts/mystorageaccount/fileServices/default/shares/myshare"
                returned: always
                type: str
            name:
                description:
                    - Name of the file share
                sample: myshare
                returned: always
                type: str
            type:
                description:
                    - The type of the resource
                sample: "Microsoft.Storage/storageAccounts/fileServices/shares"
                returned: always
                type: str
            etag:
                description:
                    - Resource Etag
                sample: "0x8D75E4BA3E275F1"
                returned: always
                type: str
            last_modified_time:
                description:
                    - Returns the date and time the file share was last modified
                sample: "2021-08-23T08:17:35+00:00"
                returned: always
                type: str
            metadata:
                description:
                    - A name-value pair to associate with the file share as metadata
                sample: '{"key1": "value1"}'
                returned: always
                type: dict
            share_quota:
                description:
                    - The maximum size of the file share, in gigabytes
                sample: 102400
                returned: always
                type: int
            access_tier:
                description:
                    - Access tier for specific file share
                sample: 'TransactionOptimized'
                returned: always
                type: str
            access_tier_change_time:
                description:
                    - Indicates the last modification time for file share access tier
                sample: "2021-08-23T08:17:35+00:00"
                returned: always
                type: str
            enabled_protocols:
                description:
                    - The authentication protocol that is used for the file share.
                sample: 'SMB'
                returned: always
                type: str
            root_squash:
                description:
                    - The property is for NFS share only. The default is NoRootSquash.
                sample: 'NoRootSquash'
                returned: always
                type: str
            version:
                description:
                    - The version of the file share
                returned: always
                type: str
            deleted:
                description:
                    - Indicates whether the share was deleted
                returned: always
                type: str
            deleted_time:
                description:
                    - The deleted time if the share was deleted
                returned: always
                type: str
            remaining_retention_days:
                description:
                    - Remaining retention days for share that
                returned: always
                type: str
            access_tier_status:
                description:
                    - Indicates if there is a pending transition for access tier
                returned: always
                type: str
            share_usage_bytes:
                description:
                    - The approximate size of the data stored on the share. Note that this value may not include
                      all recently created or recently resized files.
                returned: always
                type: int
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMStorageShareInfo(AzureRMModuleBase):
    '''
    Info class for an Azure RM Storage share resource
    '''

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str'),
            account_name=dict(type='str', required=True),
        )
        self.results = dict(
            changed=False,
            storageshares=list()
        )

        self.resource_group = None
        self.name = None
        self.account_name = None

        super(AzureRMStorageShareInfo, self).__init__(self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False,
                                                      facts_module=True)

    def exec_module(self, **kwargs):
        '''
        Main module execution method
        '''

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            self.results['storageshares'] = self.get_share()
        else:
            self.results['storageshares'] = self.list_all()

        return self.results

    def get_share(self):
        '''
        Get the properties of the specified Azure Storage file share.
        :return: dict with properties of the storage file share
        '''
        storage_share = None
        try:
            storage_share = self.storage_client.file_shares.get(resource_group_name=self.resource_group,
                                                                account_name=self.account_name,
                                                                share_name=self.name)
            self.log("Response : {0}".format(storage_share))
        except ResourceNotFoundError as e:
            self.log("Did not find the storage share with name {0} : {1}".format(self.name, str(e)))
        return self.storage_share_to_dict(storage_share)

    def storage_share_to_dict(self, storage_share):
        '''
        Transform Azure RM Storage share object to dictionary
        :param storage_share: contains information about storage file share
        :type storage_share: FileShare
        :return: dict generated from storage_share
        '''
        return dict(
            id=storage_share.id,
            name=storage_share.name,
            type=storage_share.type,
            etag=storage_share.etag.replace('"', ''),
            last_modified_time=storage_share.last_modified_time,
            metadata=storage_share.metadata,
            share_quota=storage_share.share_quota,
            access_tier=storage_share.access_tier,
            access_tier_change_time=storage_share.access_tier_change_time,
            enabled_protocols=storage_share.enabled_protocols,
            root_squash=storage_share.root_squash,
            version=storage_share.version,
            deleted=storage_share.deleted,
            deleted_time=storage_share.deleted_time,
            remaining_retention_days=storage_share.remaining_retention_days,
            access_tier_status=storage_share.access_tier_status,
            share_usage_bytes=storage_share.share_usage_bytes
        ) if storage_share else None

    def list_all(self):
        '''
        Method calling the Azure SDK to create storage file share.
        :return: dict with description of the new storage file share
        '''
        '''
        Get the properties of the specified Azure Storage file share.
        :return: dict with properties of the storage file share
        '''
        all_items = None
        try:
            storage_shares = self.storage_client.file_shares.list(resource_group_name=self.resource_group,
                                                                  account_name=self.account_name)
            self.log("Response : {0}".format(storage_shares))
            all_items = [self.storage_share_to_dict(share) for share in storage_shares]
        except Exception as e:
            self.log("Did not find the storage file share : {0}".format(str(e)))
        return all_items


def main():
    AzureRMStorageShareInfo()


if __name__ == '__main__':
    main()
