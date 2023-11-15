#!/usr/bin/python
#
# Copyright (c) 2021 Andrii Bilorus <andrii.bilorus@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_storageshare
version_added: "1.8.0"
short_description: Manage Azure storage file share
description:
    - Create, update or delete a storage file share in existing storage account.
options:
    resource_group:
        description:
            - Name of the resource group to use.
        required: true
        type: str
    name:
        description:
            - Name of the storage file share to delete or create.
        type: str
        required: true
    account_name:
        description:
            - Name of the parent storage account for the storage file share.
        required: true
        type: str
    access_tier:
        description:
            - The access tier determines the price and in some cases also the performance of a file share. TransactionOptimized if not set.
        type: str
        choices:
            - TransactionOptimized
            - Hot
            - Cool
            - Premium
    metadata:
        description:
            - A name-value pair to associate with the container as metadata.
        type: dict
    state:
        description:
            - State of the storage file share. Use 'present' to create or update a storage file share and use 'absent' to delete a file share.
        default: present
        type: str
        choices:
            - absent
            - present
    quota:
        description:
            - The maximum size of the file share, in gigabytes. Must be greater than 0, and less than or equal to 5TB (5120).
              For large file shares, the maximum size is 102400. By default 102400
        type: int
    enabled_protocols:
        description:
            - The authentication protocol that is used for the file share.
            - Can only be specified when creating a share.
        type: str
        choices:
            - SMB
            - NFS
    root_squash:
        description:
            - The property is for NFS share only.
            - The default is C(NoRootSquash).
        type: str
        choices:
            - NoRootSquash
            - RootSquash
            - AllSquash

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Andrii Bilorus (@ewscat)
'''

EXAMPLES = '''
---
- name: Create storage share
  azure_rm_storageshare:
    name: testShare
    resource_group: myResourceGroup
    account_name: testStorageAccount
    state: present
    access_tier: Cool
    quota: 2048
    metadata:
      key1: value1
      key2: value2

- name: Create share with enalbed protocols
  azure_rm_storageshare:
    name: "{{ share_name }}"
    resource_group: "{{ resource_group }}"
    account_name: "{{ storage_account }}"
    access_tier: "{{ access_tier }}"
    root_squash: RootSquash
    enabled_protocols: NFS

- name: Delete storage share
  azure_rm_storageshare:
    name: testShare
    resource_group: myResourceGroup
    account_name: testStorageAccount
    state: absent
'''

RETURN = '''
state:
    description:
        - Facts about the current state of the storage file file share.
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
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class Actions:
    '''
    Action list that can be executed with storage file share
    '''
    NoAction, Create, Update, Delete = range(4)


class AzureRMStorageShare(AzureRMModuleBase):
    '''
    Configuration class for an Azure RM Storage file share resource
    '''

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            account_name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            access_tier=dict(type='str', default=None,
                             choices=['TransactionOptimized', 'Hot', 'Cool', 'Premium']),
            quota=dict(type='int', default=None),
            metadata=dict(type='dict', default=None),
            root_squash=dict(type='str', choices=['NoRootSquash', 'RootSquash', 'AllSquash']),
            enabled_protocols=dict(type='str', choices=['SMB', 'NFS']),
        )
        self.results = dict(
            changed=False,
            state=dict()
        )

        self.resource_group = None
        self.name = None
        self.account_name = None
        self.state = None
        self.quota = None
        self.metadata = None
        self.root_squash = None
        self.enabled_protocols = None

        self.to_do = Actions.NoAction

        super(AzureRMStorageShare, self).__init__(self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        '''
        Main module execution method
        '''

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self.log('Fetching storage file share {0}'.format(self.name))
        response = None
        old_response = self.get_share()

        if old_response is None:
            if self.state == "present":
                self.to_do = Actions.Create
        else:
            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                self.to_do = Actions.Update

        if self.to_do == Actions.Create:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.create_storage_share()
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.delete_storage_share()
        elif self.to_do == Actions.Update:
            if self.update_needed(old_response):
                self.results['changed'] = True
                if self.check_mode:
                    return self.results
                response = self.update_storage_share(old_response)
            else:
                self.results['changed'] = False
                response = old_response

        if response is not None:
            self.results['state'] = response
        else:
            self.results['state'] = dict()

        return self.results

    def update_needed(self, old_response):
        '''
        Define if storage file share update needed.
        :param old_response: dict with properties of the storage file share
        :return: True if update needed, else False
        '''
        return ((self.access_tier is not None) and (self.access_tier != old_response.get('access_tier')) or
                (self.quota is not None) and (self.quota != old_response.get('share_quota')) or
                (self.metadata is not None) and (self.metadata != old_response.get('metadata')) or
                (self.root_squash is not None) and (self.root_squash != old_response.get('root_squash')) or
                (self.enabled_protocols is not None) and (self.enabled_protocols != old_response.get('enabled_protocols')))

    def get_share(self):
        '''
        Get the properties of the specified Azure Storage file share.
        :return: dict with properties of the storage file share
        '''
        found = False
        try:
            storage_share = self.storage_client.file_shares.get(resource_group_name=self.resource_group,
                                                                account_name=self.account_name,
                                                                share_name=self.name)
            found = True
            self.log("Response : {0}".format(storage_share))
        except ResourceNotFoundError as e:
            self.log("Did not find the storage file share with name {0} : {1}".format(self.name, str(e)))
        return self.storage_share_to_dict(storage_share) if found else None

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
            root_squash=storage_share.root_squash,
            enabled_protocols=storage_share.enabled_protocols
        )

    def create_storage_share(self):
        '''
        Method calling the Azure SDK to create storage file share.
        :return: dict with description of the new storage file share
        '''
        self.log("Creating fileshare {0}".format(self.name))
        try:
            self.storage_client.file_shares.create(resource_group_name=self.resource_group,
                                                   account_name=self.account_name,
                                                   share_name=self.name,
                                                   file_share=dict(access_tier=self.access_tier,
                                                                   share_quota=self.quota,
                                                                   metadata=self.metadata,
                                                                   root_squash=self.root_squash,
                                                                   enabled_protocols=self.enabled_protocols))
        except Exception as e:
            self.fail("Error creating file share {0} : {1}".format(self.name, str(e)))
        return self.get_share()

    def update_storage_share(self, old_responce):
        '''
        Method calling the Azure SDK to update storage file share.
        :param old_response: dict with properties of the storage file share
        :return: dict with description of the new storage file share
        '''
        self.log("Creating file share {0}".format(self.name))
        file_share_details = dict(
            access_tier=self.access_tier if self.access_tier else old_responce.get('access_tier'),
            share_quota=self.quota if self.quota else old_responce.get('share_quota'),
            metadata=self.metadata if self.metadata else old_responce.get('metadata'),
            enabled_protocols=self.enabled_protocols if self.enabled_protocols else old_responce.get('enabled_protocols'),
            root_squash=self.root_squash if self.root_squash else old_responce.get('self.root_squash')
        )
        try:
            self.storage_client.file_shares.update(resource_group_name=self.resource_group,
                                                   account_name=self.account_name,
                                                   share_name=self.name,
                                                   file_share=file_share_details)
        except Exception as e:
            self.fail("Error updating file share {0} : {1}".format(self.name, str(e)))
        return self.get_share()

    def delete_storage_share(self):
        '''
        Method calling the Azure SDK to delete storage share.
        :return: object resulting from the original request
        '''
        try:
            self.storage_client.file_shares.delete(resource_group_name=self.resource_group,
                                                   account_name=self.account_name,
                                                   share_name=self.name)
        except Exception as e:
            self.fail("Error deleting file share {0} : {1}".format(self.name, str(e)))
        return self.get_share()


def main():
    AzureRMStorageShare()


if __name__ == '__main__':
    main()
