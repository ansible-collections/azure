#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang Chin, (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_storagesharedirectory
version_added: "3.19.0"
short_description: Manage directories inside an Azure file share
description:
    - Create, update or delete a directory (folder) inside an Azure Storage file share.
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
            - Path of the directory to manage inside the file share, for example C(foo) or C(foo/bar/baz).
            - When I(parents=false), the default, the parent path must already exist.
        required: true
        type: str
        aliases:
            - path
    metadata:
        description:
            - A name-value pair to associate with the directory as metadata.
            - All existing metadata will be replaced on each update.
        type: dict
    parents:
        description:
            - When C(true) and C(state=present), missing intermediate directories in C(name) are
              created.
            - When C(false), the default, the module fails if any parent segment does not exist.
        type: bool
        default: false
    force:
        description:
            - When C(true) and C(state=absent), recursively delete the contents of the directory
              before deleting the directory itself.
            - When C(false), the default, the module fails if the directory is not empty.
        type: bool
        default: false
    state:
        description:
            - State of the directory. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang Chin (@zunyangc)
'''

EXAMPLES = '''
---
- name: Create a directory at the share root
  azure.azcollection.azure_rm_storagesharedirectory:
    resource_group: myResourceGroup
    account_name: myStorageAccount
    share_name: myshare
    name: parent

- name: Create a nested directory tree (mkdir -p semantics)
  azure.azcollection.azure_rm_storagesharedirectory:
    resource_group: myResourceGroup
    account_name: myStorageAccount
    share_name: myshare
    name: parent/child/grandchild
    parents: true
    metadata:
      owner: ansible

- name: Update metadata on an existing directory
  azure.azcollection.azure_rm_storagesharedirectory:
    resource_group: myResourceGroup
    account_name: myStorageAccount
    share_name: myshare
    name: parent
    metadata:
      owner: ansible
      env: prod

- name: Delete an empty directory
  azure.azcollection.azure_rm_storagesharedirectory:
    resource_group: myResourceGroup
    account_name: myStorageAccount
    share_name: myshare
    name: parent/child/grandchild
    state: absent

- name: Delete a directory recursively (including children)
  azure.azcollection.azure_rm_storagesharedirectory:
    resource_group: myResourceGroup
    account_name: myStorageAccount
    share_name: myshare
    name: parent
    state: absent
    force: true
'''

RETURN = '''
state:
    description:
        - Facts about the current state of the directory.
    returned: always
    type: complex
    contains:
        name:
            description:
                - Name of the directory (the leaf segment of the path).
            returned: always
            type: str
            sample: grandchild
        path:
            description:
                - Full path of the directory within the file share.
            returned: always
            type: str
            sample: parent/child/grandchild
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
            returned: when the directory exists
            type: str
            sample: '"0x8D75E4BA3E275F1"'
        last_modified:
            description:
                - The time the directory was last modified.
            returned: when the directory exists
            type: str
            sample: '2026-05-14T03:11:22+00:00'
        metadata:
            description:
                - Name-value pairs associated with the directory as metadata.
            returned: when the directory exists
            type: dict
            sample: {"owner": "ansible"}
'''

try:
    from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError
except ImportError:
    # Handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMStorageShareDirectory(AzureRMModuleBase):
    '''
    Manage a directory inside an Azure Storage file share via the data plane.
    '''

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            account_name=dict(type='str', required=True),
            share_name=dict(type='str', required=True),
            name=dict(type='str', required=True, aliases=['path']),
            metadata=dict(type='dict'),
            parents=dict(type='bool', default=False),
            force=dict(type='bool', default=False),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )
        self.results = dict(
            changed=False,
            state=dict(),
        )

        self.resource_group = None
        self.account_name = None
        self.share_name = None
        self.name = None
        self.metadata = None
        self.parents = False
        self.force = False
        self.state = None

        super(AzureRMStorageShareDirectory, self).__init__(
            self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        # Normalise the path (no leading/trailing slashes).
        self.name = self.name.strip('/').strip()
        if not self.name:
            self.fail("The directory 'name' must not be empty.")

        directory_client = self._get_directory_client(self.name)
        existing = self._get_directory(directory_client)

        if self.state == 'present':
            if existing is None:
                self.results['changed'] = True
                if not self.check_mode:
                    self._create_directory(directory_client)
                    if self.metadata is not None:
                        directory_client.set_directory_metadata(metadata=self.metadata)
                    self.results['state'] = self._build_state(self._get_directory(directory_client))
                else:
                    self.results['state'] = self._build_state(None)
            else:
                if self.metadata is not None and (existing.get('metadata') or {}) != self.metadata:
                    self.results['changed'] = True
                    if not self.check_mode:
                        directory_client.set_directory_metadata(metadata=self.metadata)
                        existing = self._get_directory(directory_client)
                self.results['state'] = self._build_state(existing)
        else:
            if existing is not None:
                self.results['changed'] = True
                if not self.check_mode:
                    self._delete_directory(directory_client)
                self.results['state'] = self._build_state(None)
            else:
                self.results['state'] = self._build_state(None)

        return self.results

    def _get_directory_client(self, directory_path):
        return self.get_share_directory_client(resource_group_name=self.resource_group,
                                               storage_account_name=self.account_name,
                                               share_name=self.share_name,
                                               directory_path=directory_path)

    def _get_file_client(self, file_path):
        return self.get_share_file_client(resource_group_name=self.resource_group,
                                          storage_account_name=self.account_name,
                                          share_name=self.share_name,
                                          file_path=file_path)

    def _get_directory(self, directory_client):
        try:
            props = directory_client.get_directory_properties()
        except ResourceNotFoundError:
            return None
        except Exception as exc:
            self.fail("Error retrieving directory '{0}' on share '{1}': {2}".format(
                directory_client.directory_path, self.share_name, str(exc)))

        etag = getattr(props, 'etag', None)
        last_modified = getattr(props, 'last_modified', None)
        return dict(
            metadata=getattr(props, 'metadata', None) or {},
            etag=etag.replace('"', '') if isinstance(etag, str) else etag,
            last_modified=str(last_modified) if last_modified is not None else None,
        )

    def _create_directory(self, directory_client):
        if self.parents:
            self._create_parents(self.name)
        try:
            directory_client.create_directory()
        except ResourceExistsError:
            # Race or pre-existing — treat as no-op.
            pass
        except Exception as exc:
            self.fail("Error creating directory '{0}' on share '{1}': {2}".format(
                self.name, self.share_name, str(exc)))

    def _create_parents(self, full_path):
        segments = full_path.split('/')
        accumulated = ''
        for segment in segments[:-1]:
            if not segment:
                continue
            accumulated = segment if not accumulated else accumulated + '/' + segment
            parent_client = self._get_directory_client(accumulated)
            try:
                parent_client.create_directory()
            except ResourceExistsError:
                continue
            except Exception as exc:
                self.fail("Error creating parent directory '{0}': {1}".format(accumulated, str(exc)))

    def _delete_directory(self, directory_client):
        if self.force:
            self._recursive_delete(directory_client)
            return
        try:
            directory_client.delete_directory()
        except Exception as exc:
            self.fail("Error deleting directory '{0}' on share '{1}': {2}".format(
                self.name, self.share_name, str(exc)))

    def _recursive_delete(self, directory_client):
        '''
        Walk the directory client-side, deleting every file and subdirectory before
        deleting the target directory itself. The REST API has no recursive delete.
        '''
        try:
            entries = list(directory_client.list_directories_and_files())
        except Exception as exc:
            self.fail("Error listing contents of directory '{0}': {1}".format(
                directory_client.directory_path, str(exc)))

        for entry in entries:
            child_path = directory_client.directory_path + '/' + entry['name']
            if entry.get('is_directory'):
                child_client = self._get_directory_client(child_path)
                self._recursive_delete(child_client)
            else:
                file_client = self._get_file_client(child_path)
                try:
                    file_client.delete_file()
                except Exception as exc:
                    self.fail("Error deleting file '{0}': {1}".format(child_path, str(exc)))

        try:
            directory_client.delete_directory()
        except Exception as exc:
            self.fail("Error deleting directory '{0}' on share '{1}': {2}".format(
                directory_client.directory_path, self.share_name, str(exc)))

    def _build_state(self, props):
        leaf = self.name.split('/')[-1]
        state = dict(
            name=leaf,
            path=self.name,
            share=self.share_name,
            account=self.account_name,
        )
        if props is not None:
            state.update(dict(
                etag=props.get('etag'),
                last_modified=props.get('last_modified'),
                metadata=props.get('metadata') or {},
            ))
        return state


def main():
    AzureRMStorageShareDirectory()


if __name__ == '__main__':
    main()
