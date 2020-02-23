#!/usr/bin/python
#
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: azure_rm_keyvaultkey_info
version_added: "2.9"
short_description: Get Azure Key Vault secret facts.
description:
    - Get facts of Azure Key Vault secret.

options:
    vault_uri:
        description:
            - Vault uri where the secret stored in.
        required: True
        type: str
    name:
        description:
            - secret name.
        required: True
        type: str
    version:
        description:
            - secret version.
        default: current (latest)
        type: str


extends_documentation_fragment:
    - azure

'''

EXAMPLES = '''
  - name: Get latest version of specific key
    azure_rm_keyvaultsecret_info::
      vault_uri: "https://myVault.vault.azure.net"
      name: mysecret

  - name: List all versions of specific key
    azure_rm_keyvaultsecret_info:
      vault_uri: "https://myVault.vault.azure.net"
      name: mysecret
      version: 12345
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.keyvault import KeyVaultClient, KeyVaultId, KeyVaultAuthentication, KeyId
    from azure.keyvault.models import KeyAttributes, JsonWebKey
    from azure.common.credentials import ServicePrincipalCredentials
    from azure.keyvault.models.key_vault_error import KeyVaultErrorException
    from msrestazure.azure_active_directory import MSIAuthentication
except ImportError:
    # This is handled in azure_rm_common
    pass


def keyitem_to_dict(keyitem):
    return dict(
        id=keyitem.id,
        value=keyitem.value,
        version=KeyVaultId.parse_secret_id(keyitem.id).version,
        manged=keyitem.managed,
        attributes=dict(
            enabled=keyitem.attributes.enabled,
            not_before=keyitem.attributes.not_before,
            expires=keyitem.attributes.expires,
            created=keyitem.attributes.created,
            updated=keyitem.attributes.updated,
            recovery_level=keyitem.attributes.recovery_level
        )
    )


class AzureRMKeyVaultSecretInfo(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            version=dict(type='str', default='current'),
            name=dict(type='str', required=True),
            vault_uri=dict(type='str', required=True),
            tags=dict(type='list')
        )

        self.vault_uri = None
        self.name = None
        self.version = None
        self.tags = None

        self.results = dict(changed=False)
        self._client = None

        super(AzureRMKeyVaultSecretInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=False,
                                                        supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        self._client = self.get_keyvault_client()

        versions = self.get_secret_versions()
        # self.results['versions'] = versions

        if self.version == 'current':
            self.version = versions[-1]

        secret = self.get_secret()
        self.results['secret'] = keyitem_to_dict(secret)
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

    def get_secret(self):
        '''
        Gets the properties of the specified key in key vault.

        :return: deserialized key state dictionary
        '''
        self.log("Get the key {0}".format(self.name))

        response = None
        try:
            response = self._client.get_secret(vault_base_url=self.vault_uri, secret_name=self.name,
                                               secret_version=self.version)
        except KeyVaultErrorException as e:
            self.log("Did not find the key vault secret {0}: {1}".format(self.name, str(e)))
        return response

    def get_secret_versions(self):
        '''
        Lists secret versions.

        :return: deserialized versions of secrets, includes key identifier, attributes and tags
        '''
        self.log("Get the secret versions {0}".format(self.name))

        versions = []
        try:
            response = self._client.get_secret_versions(vault_base_url=self.vault_uri, secret_name=self.name)

            self.log("Response : {0}".format(response))

            if response:
                for item in response:
                    version = KeyVaultId.parse_secret_id(item.id).version
                    versions.append(version)
        except KeyVaultErrorException as e:
            self.log("Did not find secret versions {0} : {1}.".format(self.name, str(e)))
        return versions


def main():
    """Main execution"""
    AzureRMKeyVaultSecretInfo()


if __name__ == '__main__':
    main()
