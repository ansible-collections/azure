# Copyright (c) 2022 Hai Cao, <t-haicao@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: azure_keyvault_secret
    author:
        - Hai Cao <t-haicao@microsoft.com>
    version_added: '1.12.0'
    requirements:
        - requests
        - azure
        - msrest
    short_description: Read secret from Azure Key Vault.
    description:
      - This lookup returns the content of secret saved in Azure Key Vault.
      - When ansible host is MSI enabled Azure VM, user don't need provide any credential to access to Azure Key Vault.
    options:
        _terms:
            description: Secret name, version can be included like secret_name/secret_version.
            required: True
        vault_url:
            description: Url of Azure Key Vault.
            required: True
        client_id:
            description: Client id of service principal that has access to the Azure Key Vault
        secret:
            description: Secret of the service principal.
        tenant_id:
            description: Tenant id of service principal.
    notes:
        - If version is not provided, this plugin will return the latest version of the secret.
        - If ansible is running on Azure Virtual Machine with MSI enabled, client_id, secret and tenant isn't required.
        - For enabling MSI on Azure VM, please refer to this doc https://docs.microsoft.com/en-us/azure/active-directory/managed-service-identity/
        - After enabling MSI on Azure VM, remember to grant access of the Key Vault to the VM by adding a new Acess Policy in Azure Portal.
        - If MSI is not enabled on ansible host, it's required to provide a valid service principal which has access to the key vault.
        - To use a plugin from a collection, please reference the full namespace, collection name, and lookup plugin name that you want to use.
"""

EXAMPLE = """
- name: Look up secret when ansible host is MSI enabled Azure VM
  debug:
    msg: "the value of this secret is {{
        lookup(
          'azure.azcollection.azure_keyvault_secret',
          'testSecret/version',
          vault_url='https://yourvault.vault.azure.net'
        )
      }}"

- name: Look up secret when ansible host is general VM
  vars:
    url: 'https://yourvault.vault.azure.net'
    secretname: 'testSecret/version'
    client_id: '123456789'
    secret: 'abcdefg'
    tenant: 'uvwxyz'
  debug:
    msg: "the value of this secret is {{
        lookup(
          'azure.azcollection.azure_keyvault_secret',
          secretname,
          vault_url=url,
          client_id=client_id,
          secret=secret,
          tenant_id=tenant
        )
      }}"

# Example below creates an Azure Virtual Machine with SSH public key from key vault using 'azure_keyvault_secret' lookup plugin.
- name: Create Azure VM
  hosts: localhost
  connection: local
  no_log: True
  vars:
    resource_group: myResourceGroup
    vm_name: testvm
    location: eastus
    ssh_key: "{{ lookup('azure.azcollection.azure_keyvault_secret','myssh_key') }}"
  - name: Create VM
    azure_rm_virtualmachine:
      resource_group: "{{ resource_group }}"
      name: "{{ vm_name }}"
      vm_size: Standard_DS1_v2
      admin_username: azureuser
      ssh_password_enabled: false
      ssh_public_keys:
        - path: /home/azureuser/.ssh/authorized_keys
          key_data: "{{ ssh_key }}"
      network_interfaces: "{{ vm_name }}"
      image:
        offer: UbuntuServer
        publisher: Canonical
        sku: 16.04-LTS
        version: latest
"""

RETURN = """
  _raw:
    description: secret content string
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
try:
    import requests
    import logging
    from azure.common.credentials import ServicePrincipalCredentials
    from azure.keyvault import KeyVaultClient
    from msrest.exceptions import AuthenticationError, ClientRequestError
    from azure.keyvault.models.key_vault_error import KeyVaultErrorException
except ImportError:
    pass

display = Display()

TOKEN_ACQUIRED = False

token_params = {
    'api-version': '2018-02-01',
    'resource': 'https://vault.azure.net'
}

token_headers = {
    'Metadata': 'true'
}

token = None

try:
    token_res = requests.get('http://169.254.169.254/metadata/identity/oauth2/token', params=token_params, headers=token_headers, timeout=(3.05, 27))
    if token_res.ok:
        token = token_res.json().get("access_token")
        if token is not None:
            TOKEN_ACQUIRED = True
        else:
            display.v('Successfully called MSI endpoint, but no token was available. Will use service principal if provided.')
    else:
        display.v("Unable to query MSI endpoint, Error Code %s. Will use service principal if provided" % token_res.status_code)
except Exception:
    display.v('Unable to fetch MSI token. Will use service principal if provided.')
    TOKEN_ACQUIRED = False


def lookup_secret_non_msi(terms, vault_url, kwargs):
    logging.getLogger('msrestazure.azure_active_directory').addHandler(logging.NullHandler())
    logging.getLogger('msrest.service_client').addHandler(logging.NullHandler())

    client_id = kwargs.pop('client_id', None)
    secret = kwargs.pop('secret', None)
    tenant_id = kwargs.pop('tenant_id', None)

    try:
        credentials = ServicePrincipalCredentials(
            client_id=client_id,
            secret=secret,
            tenant=tenant_id
        )
        client = KeyVaultClient(credentials)
    except AuthenticationError:
        raise AnsibleError('Invalid credentials provided.')

    ret = []
    for term in terms:
        try:
            secret_val = client.get_secret(vault_url, term, '').value
            ret.append(secret_val)
        except ClientRequestError:
            raise AnsibleError('Error occurred in request')
        except KeyVaultErrorException:
            raise AnsibleError('Failed to fetch secret ' + term + '.')
    return ret


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):
        ret = []
        vault_url = kwargs.pop('vault_url', None)
        if vault_url is None:
            raise AnsibleError('Failed to get valid vault url.')
        if TOKEN_ACQUIRED:
            secret_params = {'api-version': '2016-10-01'}
            secret_headers = {'Authorization': 'Bearer ' + token}
            for term in terms:
                try:
                    secret_res = requests.get(vault_url + '/secrets/' + term, params=secret_params, headers=secret_headers)
                    ret.append(secret_res.json()["value"])
                except KeyError:
                    raise AnsibleError('Failed to fetch secret ' + term + '.')
                except Exception:
                    raise AnsibleError('Failed to fetch secret: ' + term + ' via MSI endpoint.')
            return ret
        else:
            return lookup_secret_non_msi(terms, vault_url, kwargs)
