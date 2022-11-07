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
    key_name:
        description:
            - Name of the keyvault key.
        required: true
    key_type:
        description:
            - The type of key to create. For valid values, see JsonWebKeyType. Possible values include EC, EC-HSM, RSA, RSA-HSM, oct
        default: 'RSA'
    key_size:
        description:
            - The key size in bits. For example 2048, 3072, or 4096 for RSA.
    key_attributes:
        description:
            - The attributes of a key managed by the key vault service.
        suboptions:
            enabled:
                description: bool
            not_before:
                description:
                    - not valid before date in UTC ISO format without the Z at the end
            expires:
                description:
                    - not valid after date in UTC ISO format without the Z at the end
    curve:
        description:
            - Elliptic curve name. For valid values, see JsonWebKeyCurveName. Possible values include P-256, P-384, P-521, P-256K.
    byok_file:
        description:
            - BYOK file.
    pem_file:
        description:
            - PEM file.
    pem_password:
        description:
            - PEM password.
    state:
        description:
            - Assert the state of the key. Use C(present) to create a key and C(absent) to delete a key.
        default: present
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
    import re
    import codecs
    from azure.keyvault import KeyVaultClient, KeyVaultId, KeyVaultAuthentication
    from azure.keyvault.models import KeyAttributes, JsonWebKey
    from azure.common.credentials import ServicePrincipalCredentials, get_cli_profile
    from datetime import datetime
    from msrestazure.azure_active_directory import MSIAuthentication
    from OpenSSL import crypto
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

        except Exception:
            # Key doesn't exist
            if self.state == 'present':
                changed = True

        self.results['changed'] = changed
        self.results['state'] = results

        if not self.check_mode:

            # Create key
            if self.state == 'present' and changed:
                results['key_id'] = self.create_key(self.key_name, self.key_type, self.key_size, self.key_attributes,
                                                    self.curve, self.tags)
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
        kv_url = self.azure_auth._cloud_environment.suffixes.keyvault_dns.split('.', 1).pop()
        # Don't use MSI credentials if the auth_source isn't set to MSI.  The below will Always result in credentials when running on an Azure VM.
        if self.module.params['auth_source'] == 'msi':
            try:
                self.log("Get KeyVaultClient from MSI")
                credentials = MSIAuthentication(resource="https://{0}".format(kv_url))
                return KeyVaultClient(credentials)
            except Exception:
                self.log("Get KeyVaultClient from service principal")
        elif self.module.params['auth_source'] in ['auto', 'cli']:
            try:
                profile = get_cli_profile()
                credentials, subscription_id, tenant = profile.get_login_credentials(
                    subscription_id=self.credentials['subscription_id'], resource="https://{0}".format(kv_url))
                return KeyVaultClient(credentials)
            except Exception as exc:
                self.log("Get KeyVaultClient from service principal")
                # self.fail("Failed to load CLI profile {0}.".format(str(exc)))

        # Create KeyVault Client using KeyVault auth class and auth_callback
        def auth_callback(server, resource, scope):
            if self.credentials['client_id'] is None or self.credentials['secret'] is None:
                self.fail('Please specify client_id, secret and tenant to access azure Key Vault.')

            tenant = self.credentials.get('tenant')
            if not self.credentials['tenant']:
                tenant = "common"

            authcredential = ServicePrincipalCredentials(
                client_id=self.credentials['client_id'],
                secret=self.credentials['secret'],
                tenant=tenant,
                cloud_environment=self._cloud_environment,
                resource="https://{0}".format(kv_url))

            token = authcredential.token
            return token['token_type'], token['access_token']

        return KeyVaultClient(KeyVaultAuthentication(auth_callback))

    def get_key(self, name, version=''):
        ''' Gets an existing key '''
        key_bundle = self.client.get_key(self.keyvault_uri, name, version)
        if key_bundle:
            key_id = KeyVaultId.parse_key_id(key_bundle.key.kid)
        return key_id.id

    def create_key(self, name, key_type, key_size, key_attributes, curve, tags):
        ''' Creates a key '''

        if key_attributes is not None:
            k_enabled = key_attributes.get('enabled', True)
            k_not_before = key_attributes.get('not_before', None)
            k_expires = key_attributes.get('expires', None)
            if k_not_before:
                k_not_before = datetime.fromisoformat(k_not_before.replace('Z', '+00:00'))
            if k_expires:
                k_expires = datetime.fromisoformat(k_expires.replace('Z', '+00:00'))

            key_attributes = KeyAttributes(enabled=k_enabled, not_before=k_not_before, expires=k_expires)

        key_bundle = self.client.create_key(vault_base_url=self.keyvault_uri, key_name=name, kty=key_type, key_size=key_size,
                                            key_attributes=key_attributes, curve=curve, tags=tags)
        key_id = KeyVaultId.parse_key_id(key_bundle.key.kid)
        return key_id.id

    def delete_key(self, name):
        ''' Deletes a key '''
        deleted_key = self.client.delete_key(self.keyvault_uri, name)
        key_id = KeyVaultId.parse_key_id(deleted_key.key.kid)
        return key_id.id

    def import_key(self, key_name, destination=None, key_ops=None, disabled=False, expires=None,
                   not_before=None, tags=None, pem_file=None, pem_password=None, byok_file=None):
        """ Import a private key. Supports importing base64 encoded private keys from PEM files.
            Supports importing BYOK keys into HSM for premium KeyVaults. """

        def _to_bytes(hex_string):
            # zero pads and decodes a hex string
            if len(hex_string) % 2:
                hex_string = '{0}'.format(hex_string)
            return codecs.decode(hex_string, 'hex_codec')

        def _set_rsa_parameters(dest, src):
            # map OpenSSL parameter names to JsonWebKey property names
            conversion_dict = {
                'modulus': 'n',
                'publicExponent': 'e',
                'privateExponent': 'd',
                'prime1': 'p',
                'prime2': 'q',
                'exponent1': 'dp',
                'exponent2': 'dq',
                'coefficient': 'qi'
            }
            # regex: looks for matches that fit the following patterns:
            #   integerPattern: 65537 (0x10001)
            #   hexPattern:
            #      00:a0:91:4d:00:23:4a:c6:83:b2:1b:4c:15:d5:be:
            #      d8:87:bd:c9:59:c2:e5:7a:f5:4a:e7:34:e8:f0:07:
            # The desired match should always be the first component of the match
            regex = re.compile(r'([^:\s]*(:[^\:)]+\))|([^:\s]*(:\s*[0-9A-Fa-f]{2})+))')
            # regex2: extracts the hex string from a format like: 65537 (0x10001)
            regex2 = re.compile(r'(?<=\(0x{1})([0-9A-Fa-f]*)(?=\))')

            key_params = crypto.dump_privatekey(crypto.FILETYPE_TEXT, src).decode('utf-8')
            for match in regex.findall(key_params):
                comps = match[0].split(':', 1)
                name = conversion_dict.get(comps[0], None)
                if name:
                    value = comps[1].replace(' ', '').replace('\n', '').replace(':', '')
                    try:
                        value = _to_bytes(value)
                    except Exception:  # pylint:disable=broad-except
                        # if decoding fails it is because of an integer pattern. Extract the hex
                        # string and retry
                        value = _to_bytes(regex2.findall(value)[0])
                    setattr(dest, name, value)

        key_attrs = KeyAttributes(not disabled, not_before, expires)
        key_obj = JsonWebKey(key_ops=key_ops)
        if pem_file:
            key_obj.kty = 'RSA'
            with open(pem_file, 'r') as f:
                pem_data = f.read()
            # load private key and prompt for password if encrypted
            try:
                pem_password = str(pem_password).encode() if pem_password else None
                # despite documentation saying password should be a string, it needs to actually
                # be UTF-8 encoded bytes
                pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, pem_data, pem_password)
            except crypto.Error:
                pass  # wrong password
            except TypeError:
                pass  # no pass provided
            _set_rsa_parameters(key_obj, pkey)
        elif byok_file:
            with open(byok_file, 'rb') as f:
                byok_data = f.read()
            key_obj.kty = 'RSA-HSM'
            key_obj.t = byok_data

        return self.client.import_key(
            self.keyvault_uri, key_name, key_obj, destination == 'hsm', key_attrs, tags)


def main():
    AzureRMKeyVaultKey()


if __name__ == '__main__':
    main()
