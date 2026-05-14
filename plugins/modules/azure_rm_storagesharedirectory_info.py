#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang Chin, (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_storagesharedirectory_info
version_added: "3.19.0"
short_description: Get information about directories inside an Azure file share
description:
    - Get properties for a specific directory inside an Azure Storage file share, or list the
      directories at a given path (default the share root).
options:
    resource_group:
        description:
            - Name of the resource group that contains the storage account.
        required: true
        type: str
    account_name:
        description:
            - Name of the parent storage account hosting the file share.
        required: true
        type: str
    share_name:
        description:
            - Name of the existing file share.
        required: true
        type: str
    name:
        description:
            - Path of the directory to return properties for, for example C(foo/bar).
            - If omitted, the module lists directories under C(path) (defaults to the share root).
        type: str
        aliases:
            - path
    recursive:
        description:
            - When listing directories, walk the tree and return every directory under the start path.
            - Ignored when C(name) is specified.
        type: bool
        default: false

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang Chin (@zunyangc)
'''

EXAMPLES = '''
---
- name: Get a single directory's properties
  azure.azcollection.azure_rm_storagesharedirectory_info:
    resource_group: myResourceGroup
    account_name: myStorageAccount
    share_name: myshare
    name: parent/child

- name: List directories at the share root
  azure.azcollection.azure_rm_storagesharedirectory_info:
    resource_group: myResourceGroup
    account_name: myStorageAccount
    share_name: myshare

- name: List every directory in the share recursively
  azure.azcollection.azure_rm_storagesharedirectory_info:
    resource_group: myResourceGroup
    account_name: myStorageAccount
    share_name: myshare
    recursive: true
'''

RETURN = '''
storagesharedirectories:
    description:
        - List of directories matching the request. Always a list, even for a single C(name) lookup.
    returned: always
    type: list
    elements: dict
    contains:
        name:
            description:
                - Leaf name of the directory.
            returned: always
            type: str
            sample: child
        path:
            description:
                - Full path of the directory within the file share.
            returned: always
            type: str
            sample: parent/child
        share:
            description:
                - Name of the parent file share.
            returned: always
            type: str
            sample: myshare
        account:
            description:
                - Name of the parent storage account.
            returned: always
            type: str
            sample: myStorageAccount
        etag:
            description:
                - The directory entity tag.
            returned: when properties are available
            type: str
        last_modified:
            description:
                - Time the directory was last modified.
            returned: when properties are available
            type: str
        metadata:
            description:
                - Metadata associated with the directory.
            returned: when properties are available
            type: dict
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMStorageShareDirectoryInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            account_name=dict(type='str', required=True),
            share_name=dict(type='str', required=True),
            name=dict(type='str', aliases=['path']),
            recursive=dict(type='bool', default=False),
        )
        self.results = dict(
            changed=False,
            storagesharedirectories=[],
        )

        self.resource_group = None
        self.account_name = None
        self.share_name = None
        self.name = None
        self.recursive = False

        super(AzureRMStorageShareDirectoryInfo, self).__init__(
            self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.name = self.name.strip('/').strip()

        if self.name:
            self.results['storagesharedirectories'] = self._get_one(self.name)
        else:
            self.results['storagesharedirectories'] = self._list('', recursive=self.recursive)

        return self.results

    def _get_one(self, path):
        client = self.get_share_directory_client(
            resource_group_name=self.resource_group,
            storage_account_name=self.account_name,
            share_name=self.share_name,
            directory_path=path,
        )
        try:
            props = client.get_directory_properties()
        except ResourceNotFoundError:
            return []
        except Exception as exc:
            self.fail("Error retrieving directory '{0}': {1}".format(path, str(exc)))
        return [self._props_to_dict(path, props)]

    def _list(self, base_path, recursive):
        share_client = self.get_share_client(
            resource_group_name=self.resource_group,
            storage_account_name=self.account_name,
            share_name=self.share_name,
        )
        if base_path:
            iterable = share_client.get_directory_client(base_path).list_directories_and_files()
        else:
            iterable = share_client.list_directories_and_files()

        results = []
        try:
            entries = list(iterable)
        except Exception as exc:
            self.fail("Error listing share '{0}': {1}".format(self.share_name, str(exc)))

        for entry in entries:
            if not entry.get('is_directory'):
                continue
            child_path = entry['name'] if not base_path else base_path + '/' + entry['name']
            child_client = self.get_share_directory_client(
                resource_group_name=self.resource_group,
                storage_account_name=self.account_name,
                share_name=self.share_name,
                directory_path=child_path,
            )
            try:
                props = child_client.get_directory_properties()
            except Exception:
                props = None
            results.append(self._props_to_dict(child_path, props))
            if recursive:
                results.extend(self._list(child_path, recursive=True))
        return results

    def _props_to_dict(self, path, props):
        leaf = path.split('/')[-1] if path else ''
        result = dict(
            name=leaf,
            path=path,
            share=self.share_name,
            account=self.account_name,
        )
        if props is not None:
            etag = getattr(props, 'etag', None)
            last_modified = getattr(props, 'last_modified', None)
            result.update(dict(
                etag=etag.replace('"', '') if isinstance(etag, str) else etag,
                last_modified=str(last_modified) if last_modified is not None else None,
                metadata=getattr(props, 'metadata', None) or {},
            ))
        return result


def main():
    AzureRMStorageShareDirectoryInfo()


if __name__ == '__main__':
    main()
