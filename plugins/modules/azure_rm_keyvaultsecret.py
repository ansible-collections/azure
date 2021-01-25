#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_keyvaultsecret
version_added: "0.1.2"
short_description: Use Azure KeyVault Secrets
description:
    - Create or delete a secret within a given keyvault.
    - By using Key Vault, you can encrypt keys and secrets.
    - Such as authentication keys, storage account keys, data encryption keys, .PFX files, and passwords.
options:
    keyvault_uri:
            description:
                - URI of the keyvault endpoint.
            required: true
    content_type:
        description:
            - Type of the secret value such as a password.
        type: str
    secret_name:
        description:
            - Name of the keyvault secret.
        required: true
    secret_value:
        description:
            - Secret to be secured by keyvault.
    state:
        description:
            - Assert the state of the subnet. Use C(present) to create or update a secret and C(absent) to delete a secret .
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
    - name: Create a secret
      azure_rm_keyvaultsecret:
        secret_name: MySecret
        secret_value: My_Pass_Sec
        keyvault_uri: https://contoso.vault.azure.net/
        tags:
            testing: testing
            delete: never

    - name: Delete a secret
      azure_rm_keyvaultsecret:
        secret_name: MySecret
        keyvault_uri: https://contoso.vault.azure.net/
        state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the secret.
    returned: success
    type: complex
    contains:
        secret_id:
          description:
              - Secret resource path.
          type: str
          example: https://contoso.vault.azure.net/secrets/hello/e924f053839f4431b35bc54393f98423
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.keyvault import KeyVaultClient, KeyVaultAuthentication, KeyVaultId
    from azure.common.credentials import ServicePrincipalCredentials
    from azure.keyvault.models.key_vault_error import KeyVaultErrorException
    from msrestazure.azure_active_directory import MSIAuthentication
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMKeyVaultSecret(AzureRMModuleBase):
    ''' Module that creates or deletes secrets in Azure KeyVault '''

    def __init__(self):

        self.module_arg_spec = dict(
            secret_name=dict(type='str', required=True),
            secret_value=dict(type='str', no_log=True),
            keyvault_uri=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            content_type=dict(type='str')
        )

        required_if = [
            ('state', 'present', ['secret_value'])
        ]

        self.results = dict(
            changed=False,
            state=dict()
        )

        self.secret_name = None
        self.secret_value = None
        self.keyvault_uri = None
        self.state = None
        self.data_creds = None
        self.client = None
        self.tags = None
        self.content_type = None

        super(AzureRMKeyVaultSecret, self).__init__(self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    required_if=required_if,
                                                    supports_tags=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        # Create KeyVault Client
        self.client = self.get_keyvault_client()

        results = dict()
        changed = False

        try:
            results = self.get_secret(self.secret_name)

            # Secret exists and will be deleted
            if self.state == 'absent':
                changed = True
            elif self.secret_value and results['secret_value'] != self.secret_value:
                changed = True

        except KeyVaultErrorException:
            # Secret doesn't exist
            if self.state == 'present':
                changed = True

        self.results['changed'] = changed
        self.results['state'] = results

        if not self.check_mode:
            # Create secret
            if self.state == 'present' and changed:
                results['secret_id'] = self.create_update_secret(self.secret_name, self.secret_value, self.tags, self.content_type)
                self.results['state'] = results
                self.results['state']['status'] = 'Created'
            # Delete secret
            elif self.state == 'absent' and changed:
                results['secret_id'] = self.delete_secret(self.secret_name)
                self.results['state'] = results
                self.results['state']['status'] = 'Deleted'
        else:
            if self.state == 'present' and changed:
                self.results['state']['status'] = 'Created'
            elif self.state == 'absent' and changed:
                self.results['state']['status'] = 'Deleted'

        return self.results

    def get_keyvault_client(self):
        try:
            self.log("Get KeyVaultClient from MSI")
            credentials = MSIAuthentication(resource='https://vault.azure.net')
            return KeyVaultClient(credentials)
        except Exception:
            self.log("Get KeyVaultClient from service principal")

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
                resource="https://vault.azure.net")

            token = authcredential.token
            return token['token_type'], token['access_token']

        return KeyVaultClient(KeyVaultAuthentication(auth_callback))

    def get_secret(self, name, version=''):
        ''' Gets an existing secret '''
        secret_bundle = self.client.get_secret(self.keyvault_uri, name, version)
        if secret_bundle:
            secret_id = KeyVaultId.parse_secret_id(secret_bundle.id)
            return dict(secret_id=secret_id.id, secret_value=secret_bundle.value)
        return None

    def create_update_secret(self, name, secret, tags, content_type):
        ''' Creates/Updates a secret '''
        secret_bundle = self.client.set_secret(self.keyvault_uri, name, secret, tags=tags, content_type=content_type)
        secret_id = KeyVaultId.parse_secret_id(secret_bundle.id)
        return secret_id.id

    def delete_secret(self, name):
        ''' Deletes a secret '''
        deleted_secret = self.client.delete_secret(self.keyvault_uri, name)
        secret_id = KeyVaultId.parse_secret_id(deleted_secret.id)
        return secret_id.id


def main():
    AzureRMKeyVaultSecret()


if __name__ == '__main__':
    main()
