#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


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
        type: str
    content_type:
        description:
            - Type of the secret value such as a password.
        type: str
    secret_name:
        description:
            - Name of the keyvault secret.
        required: true
        type: str
    secret_value:
        description:
            - Secret to be secured by keyvault.
            - This parameter must be configured at creation time.
        type: str
    secret_expiry:
        description:
            - Optional expiry datetime for secret
        type: str
    secret_valid_from:
        description:
            - Optional valid-from datetime for secret
        type: str
    recover_if_need:
        description:
            - Whether to permanently recover delete secrets.
        type: bool
    purge_if_need:
        description:
            - Whether to permanently delete secrets.
        type: bool
    state:
        description:
            - Assert the state of the subnet. Use C(present) to create or update a secret and C(absent) to delete a secret .
        type: str
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

- name: Recover a delete secret
  azure_rm_keyvaultsecret:
    secret_name: MySecret
    keyvault_uri: https://contoso.vault.azure.net/
    recover_if_need: true

- name: Purge a delete secret
  azure_rm_keyvaultsecret:
    secret_name: MySecret
    keyvault_uri: https://contoso.vault.azure.net/
    purge_if_need: true
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
    from azure.keyvault.secrets import SecretClient
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.exceptions import HttpResponseError
    import dateutil.parser
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMKeyVaultSecret(AzureRMModuleBase):
    ''' Module that creates or deletes secrets in Azure KeyVault '''

    def __init__(self):

        self.module_arg_spec = dict(
            secret_name=dict(type='str', required=True),
            secret_value=dict(type='str', no_log=True),
            secret_valid_from=dict(type='str', no_log=True),
            secret_expiry=dict(type='str', no_log=True),
            keyvault_uri=dict(type='str', no_log=True, required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            recover_if_need=dict(type='bool'),
            purge_if_need=dict(type='bool'),
            content_type=dict(type='str')
        )

        self.results = dict(
            changed=False,
            state=dict()
        )

        self.secret_name = None
        self.secret_value = None
        self.secret_valid_from = None
        self.secret_expiry = None
        self.keyvault_uri = None
        self.state = None
        self.data_creds = None
        self.client = None
        self.tags = None
        self.recover_if_need = None
        self.purge_if_need = None
        self.content_type = None

        super(AzureRMKeyVaultSecret, self).__init__(self.module_arg_spec,
                                                    supports_check_mode=True,
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

        except ResourceNotFoundError as ec:
            # Secret doesn't exist
            if self.state == 'present':
                changed = True
        except Exception as ec2:
            self.fail("Find the key vault secret got exception, exception as {0}".format(str(ec2)))

        self.results['changed'] = changed
        self.results['state'] = results

        valid_from = self.secret_valid_from
        if isinstance(valid_from, str) and len(valid_from) > 0:
            valid_from = dateutil.parser.parse(valid_from)

        expiry = self.secret_expiry
        if isinstance(expiry, str) and len(expiry) > 0:
            expiry = dateutil.parser.parse(expiry)

        if not self.check_mode:
            # Create secret
            if self.state == 'present' and changed:
                status = 'Created'
                if self.get_delete_secret(self.secret_name):
                    if self.recover_if_need:
                        results['secret_id'] = self.recover_delete_secret(self.secret_name)
                        status = 'Recover'
                    elif self.purge_if_need:
                        self.purge_deleted_secret(self.secret_name)
                        status = 'Purged'
                    else:
                        self.fail("Secret {0} is currently in a deleted but recoverable state, and its name cannot be reused; in this state,\
                                  the secret can only be recovered or purged.".format(self.secret_name))
                else:
                    results['secret_id'] = self.create_update_secret(self.secret_name, self.secret_value, self.tags, self.content_type, valid_from, expiry)
                    status = 'Created'
                self.results['state'] = results
                self.results['state']['status'] = status
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

        return SecretClient(vault_url=self.keyvault_uri, credential=self.azure_auth.azure_credential_track2)

    def get_secret(self, name, version=''):
        ''' Gets an existing secret '''
        secret_bundle = self.client.get_secret(name=name, version=version)

        if secret_bundle:
            return dict(secret_id=secret_bundle.id, secret_value=secret_bundle.value)
        return None

    def create_update_secret(self, name, secret, tags, content_type, valid_from, expiry):
        ''' Creates/Updates a secret '''
        secret_bundle = self.client.set_secret(name=name,
                                               value=secret,
                                               tags=tags,
                                               content_type=content_type,
                                               expires_on=expiry,
                                               not_before=valid_from)
        return secret_bundle._properties._id

    def delete_secret(self, name):
        ''' Deletes a secret '''
        deleted_secret = self.client.begin_delete_secret(name)
        result = self.get_poller_result(deleted_secret)
        return result.properties._id

    def recover_delete_secret(self, name):
        ''' Recover a delete secret '''
        try:
            recover_delete_secret = self.client.begin_recover_deleted_secret(name)
            result = self.get_poller_result(recover_delete_secret)
            return result._id
        except HttpResponseError as ec:
            self.fail("Recover the delete secret fail, detail info {0}".format(ec))

    def purge_deleted_secret(self, name):
        ''' Purge delete secret '''
        try:
            purge_deleted_secret = self.client.purge_deleted_secret(name)
            return purge_deleted_secret
        except HttpResponseError as ec:
            self.fail("Purge delete secret fail, detail info {0}".format(ec))

    def get_delete_secret(self, name):
        ''' Get delete secret '''
        try:
            self.client.get_deleted_secret(name=name)
        except ResourceNotFoundError:
            return False
        return True


def main():
    AzureRMKeyVaultSecret()


if __name__ == '__main__':
    main()
