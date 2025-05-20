# Copyright (c) 2022 Hai Cao, <t-haicao@microsoft.com>, Marcin Slowikowski (@msl0)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
name: azure_keyvault_secret
author:
    - Hai Cao (@tk5eq) <t-haicao@microsoft.com>
    - Marcin Slowikowski (@msl0)
version_added: '1.12.0'
requirements:
    - requests
    - azure
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
    use_msi:
        description: MSI token autodiscover, default is true.
    use_cli:
        description: When I(use_cli=True), get the 'az lgin' credential authentication, default if false.
    cloud_type:
        description: Specify which cloud, such as C(azure), C(usgovcloudapi).
notes:
    - If version is not provided, this plugin will return the latest version of the secret.
    - If ansible is running on Azure Virtual Machine with MSI enabled, client_id, secret and tenant isn't required.
    - For enabling MSI on Azure VM, please refer to this doc https://docs.microsoft.com/en-us/azure/active-directory/managed-service-identity/
    - After enabling MSI on Azure VM, remember to grant access of the Key Vault to the VM by adding a new Acess Policy in Azure Portal.
    - If MSI is not enabled on ansible host, it's required to provide a valid service principal which has access to the key vault.
    - To authenticate via service principal, pass client_id, secret and tenant_id or set environment variables
      AZURE_CLIENT_ID, AZURE_CLIENT_SECRET and AZURE_TENANT_ID.
    - Authentication via C(az login) is also supported.
    - To use a plugin from a collection, please reference the full namespace, collection name, and lookup plugin name that you want to use.
"""

EXAMPLE = """
- name: Look up secret when azure cli login
  debug:
    msg: msg: "{{ lookup('azure.azcollection.azure_keyvault_secret', 'testsecret', vault_url=key_vault_uri)}}"

- name: Look up secret with cloud type
  debug:
    msg: msg: "{{ lookup('azure.azcollection.azure_keyvault_secret', 'testsecret', cloud_type='usgovcloudapi', vault_url=key_vault_uri)}}"

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
          tenant_id=tenant,
          use_msi=false
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
        offer: 0001-com-ubuntu-server-focal
        publisher: Canonical
        sku: 20_04-lts
        version: latest
"""

RETURN = """
  _raw:
    description: secret content string
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
try:
    import logging
    import requests
    from azure.keyvault.secrets import SecretClient
    from azure.identity import DefaultAzureCredential, ClientSecretCredential, AzureCliCredential
    from azure.keyvault.secrets import SecretClient

except ImportError:
    pass

display = Display()

TOKEN_ACQUIRED = False

logger = logging.getLogger("azure.identity").setLevel(logging.ERROR)


def lookup_secret_non_msi(terms, vault_url, kwargs):

    client_id = kwargs['client_id'] if kwargs.get('client_id') else None
    secret = kwargs['secret'] if kwargs.get('secret') else None
    tenant_id = kwargs['tenant_id'] if kwargs.get('tenant_id') else None

    if all(v is not None for v in [client_id, secret, tenant_id]):
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=secret,
        )
    else:
        if kwargs.get('use_cli'):
            credential = AzureCliCredential()
        else:
            credential = DefaultAzureCredential()
    client = SecretClient(vault_url, credential)

    ret = []
    for term in terms:
        try:
            secret_val = client.get_secret(term).value
            ret.append(secret_val)
        except Exception:
            raise AnsibleError('Failed to fetch secret ' + term + ' from ' + vault_url + '.')
    return ret


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):
        ret = []
        vault_url = kwargs.pop('vault_url', None)
        use_msi = kwargs.pop('use_msi', True)
        TOKEN_ACQUIRED = False
        token = None

        token_params = {
            'api-version': '2018-02-01',
            'resource': 'https://vault.{0}.net'.format(kwargs.get('cloud_type', 'azure'))
        }

        token_headers = {
            'Metadata': 'true'
        }

        if use_msi:
            try:
                token_res = requests.get('http://169.254.169.254/metadata/identity/oauth2/token',
                                         params=token_params,
                                         headers=token_headers,
                                         timeout=(3.05, 27))
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
                    raise AnsibleError('Failed to fetch secret ' + term + ' from ' + vault_url + '.')
                except Exception:
                    raise AnsibleError('Failed to fetch secret ' + term + ' from ' + vault_url + ' via MSI endpoint.')
            return ret
        else:
            return lookup_secret_non_msi(terms, vault_url, kwargs)
