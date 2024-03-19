#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_keyvaultkey
version_added: "0.1.2"
short_description: Use Azure KeyVault keys
description:
    - Create or delete a key within a given keyvault.
    - By using Key Vault, you can encrypt keys and secrets.
    - Such as authentication keys, storage account keys, data encryption keys, .PFX files, and passwords.
options:
    keyvault_uri:
        description:
            - URI of the keyvault endpoint.
        required: true
        type: str
    key_name:
        description:
            - Name of the keyvault key.
        required: true
        type: str
    key_type:
        description:
            - The type of key to create. For valid values, see JsonWebKeyType. Possible values include EC, EC-HSM, RSA, RSA-HSM, oct
        default: 'RSA'
        type: str
    key_size:
        description:
            - The key size in bits. For example 2048, 3072, or 4096 for RSA.
        type: int
    key_attributes:
        description:
            - The attributes of a key managed by the key vault service.
        type: dict
        suboptions:
            enabled:
                description:
                    - Whether the key is enabled.
                type: bool
            not_before:
                description:
                    - not valid before date in UTC ISO format without the Z at the end
                type: str
            expires:
                description:
                    - not valid after date in UTC ISO format without the Z at the end
                type: str
    curve:
        description:
            - Elliptic curve name. For valid values, see JsonWebKeyCurveName. Possible values include P-256, P-384, P-521, P-256K.
        type: str
    byok_file:
        description:
            - BYOK file.
        type: str
    pem_file:
        description:
            - PEM file.
        type: str
    pem_password:
        description:
            - PEM password.
        type: str
    state:
        description:
            - Assert the state of the key. Use C(present) to create a key and C(absent) to delete a key.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Ian Philpot (@iphilpot)

'''

EXAMPLES = '''
- name: Create a key
  azure_rm_keyvaultkey:
    key_name: MyKey
    keyvault_uri: https://contoso.vault.azure.net/

- name: Delete a key
  azure_rm_keyvaultkey:
    key_name: MyKey
    keyvault_uri: https://contoso.vault.azure.net/
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the key.
    returned: success
    type: complex
    contains:
        key_id:
          description:
              - key resource path.
          type: str
          example: https://contoso.vault.azure.net/keys/hello/e924f053839f4431b35bc54393f98423
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.keyvault.keys import KeyClient
    from azure.core.exceptions import ResourceNotFoundError
    from datetime import datetime
except ImportError:
    # This is handled in azure_rm_common
    pass

key_addribute_spec = dict(
    enabled=dict(type='bool', required=False),
    not_before=dict(type='str', no_log=True, required=False),
    expires=dict(type='str', no_log=True, required=False)
)


class AzureRMKeyVaultKey(AzureRMModuleBase):
    ''' Module that creates or deletes keys in Azure KeyVault '''

    def __init__(self):

        self.module_arg_spec = dict(
            key_name=dict(type='str', required=True),
            keyvault_uri=dict(type='str', no_log=True, required=True),
            key_type=dict(type='str', default='RSA'),
            key_size=dict(type='int'),
            key_attributes=dict(type='dict', no_log=True, options=key_addribute_spec),
            curve=dict(type='str'),
            pem_file=dict(type='str'),
            pem_password=dict(type='str', no_log=True),
            byok_file=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent'])
        )

        self.results = dict(
            changed=False,
            state=dict()
        )

        self.key_name = None
        self.keyvault_uri = None
        self.key_type = None
        self.key_size = None
        self.key_attributes = None
        self.curve = None
        self.pem_file = None
        self.pem_password = None
        self.state = None
        self.client = None
        self.tags = None

        required_if = [
            ('pem_password', 'present', ['pem_file'])
        ]

        super(AzureRMKeyVaultKey, self).__init__(self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 required_if=required_if,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        # Create KeyVaultClient
        self.client = self.get_keyvault_client()

        results = dict()
        changed = False

        try:
            results['key_id'] = self.get_key(self.key_name)

            # Key exists and will be deleted
            if self.state == 'absent':
                changed = True

        except ResourceNotFoundError as ec:
            # Key doesn't exist
            if self.state == 'present':
                changed = True
        except Exception as ec:
            self.fail("Find the key vault secret got exception, exception as {0}".format(ec))

        self.results['changed'] = changed
        self.results['state'] = results

        if not self.check_mode:

            # Create key
            if self.state == 'present' and changed:
                results['key_id'] = self.create_key(self.key_name)
                self.results['state'] = results
                self.results['state']['status'] = 'Created'
            # Delete key
            elif self.state == 'absent' and changed:
                results['key_id'] = self.delete_key(self.key_name)
                self.results['state'] = results
                self.results['state']['status'] = 'Deleted'
        else:
            if self.state == 'present' and changed:
                self.results['state']['status'] = 'Created'
            elif self.state == 'absent' and changed:
                self.results['state']['status'] = 'Deleted'

        return self.results

    def get_keyvault_client(self):

        return KeyClient(vault_url=self.keyvault_uri, credential=self.azure_auth.azure_credential_track2)

    def get_key(self, name, version=''):
        ''' Gets an existing key '''
        key_bundle = self.client.get_key(name, version)

        if key_bundle:
            return key_bundle.id

    def create_key(self, name):
        ''' Creates a key '''

        if self.key_attributes is not None:
            k_enabled = self.key_attributes.get('enabled', True)
            k_not_before = self.key_attributes.get('not_before', None)
            k_expires = self.key_attributes.get('expires', None)
            if k_not_before:
                k_not_before = datetime.fromisoformat(k_not_before.replace('Z', '+00:00'))
            if k_expires:
                k_expires = datetime.fromisoformat(k_expires.replace('Z', '+00:00'))
        else:
            k_enabled = True
            k_not_before = None
            k_expires = None

        key_bundle = self.client.create_key(name=name,
                                            key_type=self.key_type,
                                            size=self.key_size,
                                            curve=self.curve,
                                            tags=self.tags,
                                            enabled=k_enabled,
                                            not_before=k_not_before,
                                            expires_on=k_expires)
        return key_bundle._properties._id

    def delete_key(self, name):
        ''' Deletes a key '''
        deleted_key = self.client.begin_delete_key(name)
        result = self.get_poller_result(deleted_key)
        return result.properties._id


def main():
    AzureRMKeyVaultKey()


if __name__ == '__main__':
    main()
