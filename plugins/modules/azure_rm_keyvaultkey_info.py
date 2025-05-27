#!/usr/bin/python
#
# Copyright (c) 2019 Yunge Zhu, <yungez@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_keyvaultkey_info
version_added: "0.1.2"
short_description: Get Azure Key Vault key facts
description:
    - Get facts of Azure Key Vault key.

options:
    vault_uri:
        description:
            - Vault uri where the key stored in.
        required: True
        type: str
    name:
        description:
            - Key name. If not set, will list all keys in I(vault_uri).
        type: str
    version:
        description:
            - Key version.
            - Set it to C(current) to show latest version of a key.
            - Set it to C(all) to list all versions of a key.
            - Set it to specific version to list specific version of a key. eg. fd2682392a504455b79c90dd04a1bf46.
        default: current
        type: str
    show_deleted_key:
        description:
            - Set to C(true) to show deleted keys. Set to C(false) to show not deleted keys.
        type: bool
        default: false
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Yunge Zhu (@yungezz)

'''

EXAMPLES = '''
- name: Get latest version of specific key
  azure_rm_keyvaultkey_info:
    vault_uri: "https://myVault.vault.azure.net"
    name: myKey

- name: List all versions of specific key
  azure_rm_keyvaultkey_info:
    vault_uri: "https://myVault.vault.azure.net"
    name: myKey
    version: all

- name: List specific version of specific key
  azure_rm_keyvaultkey_info:
    vault_uri: "https://myVault.vault.azure.net"
    name: myKey
    version: fd2682392a504455b79c90dd04a1bf46

- name: List all keys in specific key vault
  azure_rm_keyvaultkey_info:
    vault_uri: "https://myVault.vault.azure.net"

- name: List deleted keys in specific key vault
  azure_rm_keyvaultkey_info:
    vault_uri: "https://myVault.vault.azure.net"
    show_deleted_key: true
'''

RETURN = '''
keyvaults:
    description:
        - List of keys in Azure Key Vault.
    returned: always
    type: complex
    contains:
        kid:
            description:
                - Key identifier.
            returned: always
            type: str
            sample: "https://myVault.vault.azure.net/keys/key1/fd2682392a504455b79c90dd04a1bf46"
        permitted_operations:
            description:
                - Permitted operations on the key.
            type: list
            returned: always
            sample: encrypt
        type:
            description:
                - Key type.
            type: str
            returned: always
            sample: RSA
        version:
            description:
                - Key version.
            type: str
            returned: always
            sample: fd2682392a504455b79c90dd04a1bf46
        key:
            description:
                - public part of a key.
            type: dict
            contains:
                n:
                    description:
                        - RSA modules.
                    type: str
                e:
                    description:
                        - RSA public exponent.
                    type: str
                crv:
                    description:
                        - Elliptic curve name.
                    type: str
                x:
                    description:
                        - X component of an EC public key.
                    type: str
                y:
                    description:
                        - Y component of an EC public key.
                    type: str
        managed:
            description:
                - C(True) if the key's lifetime is managed by key vault.
            type: bool
            sample: True
        tags:
            description:
                - Tags of the key.
            returned: always
            type: list
            sample: [foo, ]
        attributes:
            description:
                - Key attributes.
            type: dict
            contains:
                created:
                    description:
                        - Creation datetime.
                    returned: always
                    type: str
                    sample: "2019-04-25T07:26:49+00:00"
                not_before:
                    description:
                        - Not before datetime.
                    type: str
                    sample: "2019-04-25T07:26:49+00:00"
                expires:
                    description:
                        - Expiration datetime.
                    type: str
                    sample: "2019-04-25T07:26:49+00:00"
                updated:
                    description:
                        - Update datetime.
                    returned: always
                    type: str
                    sample: "2019-04-25T07:26:49+00:00"
                enabled:
                    description:
                        - Indicate whether the key is enabled.
                    returned: always
                    type: str
                    sample: true
                recovery_level:
                    description:
                        - Reflects the deletion recovery level currently in effect for keys in the current vault.
                        - If it contains C(Purgeable) the key can be permanently deleted by a privileged user.
                        - Otherwise, only the system can purge the key, at the end of the retention interval.
                    returned: always
                    type: str
                    sample: Purgable
'''


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
import base64

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.keyvault.keys import KeyClient
except ImportError:
    # This is handled in azure_rm_common
    pass


def keybundle_to_dict(bundle):
    return dict(
        tags=bundle.properties.tags,
        managed=bundle.properties.managed,
        attributes=dict(
            enabled=bundle.properties.enabled,
            not_before=bundle.properties.not_before,
            expires=bundle.properties.expires_on,
            created=bundle.properties.created_on,
            updated=bundle.properties.updated_on,
            recovery_level=bundle.properties.recovery_level
        ),
        kid=bundle.id,
        version=bundle.properties.version,
        type=bundle.key_type,
        permitted_operations=bundle.key_operations,
        key=dict(
            n=base64.b64encode(bundle.key.n) if hasattr(bundle.key, 'n') and bundle.key.n else None,
            e=base64.b64encode(bundle.key.e) if hasattr(bundle.key, 'e') and bundle.key.e else None,
            crv=base64.b64encode(bundle.key.crv) if hasattr(bundle.key, 'crv') and bundle.key.crv else None,
            x=base64.b64encode(bundle.key.x) if hasattr(bundle.key, 'x') and bundle.key.x else None,
            y=base64.b64encode(bundle.key.y) if hasattr(bundle.key, 'y') and bundle.key.y else None
        )
    )


def delete_keybundle_to_dict(bundle):
    return dict(
        tags=bundle._tags,
        managed=bundle._managed,
        attributes=dict(
            enabled=bundle.enabled,
            not_before=bundle.not_before,
            expires=bundle.expires_on,
            created=bundle.created_on,
            updated=bundle.updated_on,
            recovery_level=bundle.recovery_level
        ),
        kid=bundle._id,
        version=bundle.version,
    )


def delete_properties_to_dict(bundle):
    return dict(
        tags=bundle.tags,
        managed=bundle.managed,
        attributes=dict(
            enabled=bundle.enabled,
            not_before=bundle.not_before,
            expires=bundle.expires_on,
            created=bundle.created_on,
            updated=bundle.updated_on,
            recovery_level=bundle.recovery_level
        ),
        kid=bundle.id,
        version=bundle.version,
    )


def deletedkeybundle_to_dict(bundle):
    keybundle = delete_properties_to_dict(bundle.properties)
    keybundle['type'] = bundle.key_type
    keybundle['permitted_operations'] = bundle.key_operations
    keybundle['recovery_id'] = bundle.recovery_id
    keybundle['scheduled_purge_date'] = bundle.scheduled_purge_date
    keybundle['deleted_date'] = bundle.deleted_date
    keybundle['key'] = dict(n=bundle.key.n if hasattr(bundle.key, 'n') else None,
                            e=bundle.key.e if hasattr(bundle.key, 'e') else None,
                            crv=bundle.key.crv if hasattr(bundle.key, 'crv') else None,
                            x=bundle.key.x if hasattr(bundle.key, 'x') else None,
                            y=bundle.key.y if hasattr(bundle.key, 'y') else None)
    keybundle['id'] = bundle.id
    return keybundle


def keyitem_to_dict(keyitem):
    return dict(
        kid=keyitem._id,
        version=keyitem.version,
        tags=keyitem._tags,
        managed=keyitem._managed,
        attributes=dict(
            enabled=keyitem.enabled,
            not_before=keyitem.not_before,
            expires=keyitem.expires_on,
            created=keyitem.created_on,
            updated=keyitem.updated_on,
            recovery_level=keyitem.recovery_level
        )
    )


def delete_item_to_dict(bundle):
    return dict(
        tags=bundle.properties._tags,
        kid=bundle.properties.id,
        version=bundle.properties.version,
        managed=bundle.properties.managed,
        attributes=dict(
            enabled=bundle.properties.enabled,
            not_before=bundle.properties.not_before,
            expires=bundle.properties.expires_on,
            created=bundle.properties.created_on,
            updated=bundle.properties.updated_on,
            recovery_level=bundle.properties.recovery_level


        )
    )


def deletedkeyitem_to_dict(keyitem):
    item = delete_item_to_dict(keyitem)
    item['recovery_id'] = keyitem.recovery_id
    item['scheduled_purge_date'] = keyitem.scheduled_purge_date
    item['deleted_date'] = keyitem.deleted_date
    return item


class AzureRMKeyVaultKeyInfo(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            version=dict(type='str', default='current'),
            name=dict(type='str'),
            vault_uri=dict(type='str', required=True),
            show_deleted_key=dict(type='bool', default=False),
            tags=dict(type='list', elements='str')
        )

        self.vault_uri = None
        self.name = None
        self.version = None
        self.show_deleted_key = False
        self.tags = None

        self.results = dict(changed=False)
        self._client = None

        super(AzureRMKeyVaultKeyInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=False,
                                                     facts_module=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        self._client = self.get_keyvault_client()

        if self.name:
            if self.show_deleted_key:
                self.results['keys'] = self.get_deleted_key()
            else:
                if self.version == 'all':
                    self.results['keys'] = self.get_key_versions()
                else:
                    self.results['keys'] = self.get_key()
        else:
            if self.show_deleted_key:
                self.results['keys'] = self.list_deleted_keys()
            else:
                self.results['keys'] = self.list_keys()

        return self.results

    def get_keyvault_client(self):

        return KeyClient(vault_url=self.vault_uri, credential=self.azure_auth.azure_credential_track2)

    def get_key(self):
        '''
        Gets the properties of the specified key in key vault.

        :return: deserialized key state dictionary
        '''
        self.log("Get the key {0}".format(self.name))

        results = []
        try:
            if self.version == 'current':
                response = self._client.get_key(name=self.name,
                                                version=None)
            else:
                response = self._client.get_key(name=self.name,
                                                version=self.version)

            if response:
                response = keybundle_to_dict(response)
                if self.has_tags(response['tags'], self.tags):
                    self.log("Response : {0}".format(response))
                    results.append(response)

        except ResourceNotFoundError as e:
            self.log("Did not find the key vault key {0}: {1}".format(self.name, str(e)))
        except Exception as ec:
            self.fail("Find the key vault key got a exception as {0}".format(ec))
        return results

    def get_key_versions(self):
        '''
        Lists keys versions.

        :return: deserialized versions of key, includes key identifier, attributes and tags
        '''
        self.log("Get the key versions {0}".format(self.name))

        results = []
        try:
            response = self._client.list_properties_of_key_versions(name=self.name)
            self.log("Response : {0}".format(response))

            if response:
                for item in response:
                    item = keyitem_to_dict(item)
                    if self.has_tags(item['tags'], self.tags):
                        results.append(item)
        except Exception as e:
            self.fail("Did not find key versions {0} : {1}.".format(self.name, str(e)))
        return results

    def list_keys(self):
        '''
        Lists keys in specific key vault.

        :return: deserialized keys, includes key identifier, attributes and tags.
        '''
        self.log("Get the key vaults in current subscription")

        results = []
        try:
            response = self._client.list_properties_of_keys()
            self.log("Response : {0}".format(response))

            if response:
                for item in response:
                    item = keyitem_to_dict(item)
                    if self.has_tags(item['tags'], self.tags):
                        results.append(item)
        except Exception as e:
            self.fail("Did not find key vault in current subscription {0}.".format(str(e)))
        return results

    def get_deleted_key(self):
        '''
        Gets the properties of the specified deleted key in key vault.

        :return: deserialized key state dictionary
        '''
        self.log("Get the key {0}".format(self.name))

        results = []
        try:
            response = self._client.get_deleted_key(name=self.name)

            if response:
                response = deletedkeybundle_to_dict(response)
                if self.has_tags(response['tags'], self.tags):
                    self.log("Response : {0}".format(response))
                    results.append(response)

        except ResourceNotFoundError as ec:
            self.log("Did not find the key vault key {0}: {1}".format(self.name, str(ec)))
        except Exception as ec:
            self.fail("Find the key vault key got a exception {0}".format(str(ec)))

        return results

    def list_deleted_keys(self):
        '''
        Lists deleted keys in specific key vault.

        :return: deserialized keys, includes key identifier, attributes and tags.
        '''
        self.log("Get the key vaults in current subscription")

        results = []
        try:
            response = self._client.list_deleted_keys()
            self.log("Response : {0}".format(response))

            if response:
                for item in response:
                    item = deletedkeyitem_to_dict(item)
                    if self.has_tags(item['tags'], self.tags):
                        results.append(item)
        except Exception as e:
            self.fail("Did not find key vault in current subscription {0}.".format(str(e)))
        return results


def main():
    """Main execution"""
    AzureRMKeyVaultKeyInfo()


if __name__ == '__main__':
    main()
