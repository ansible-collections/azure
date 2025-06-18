#!/usr/bin/python
#
# Copyright (c) 2024 Bill Peck, <bpeck@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_keyvaultsecuritydomain
version_added: "3.0.0"
short_description: Manage Key Vault security domain for HSM
description:
    - Create and delete instance of Key Vault Security Domain.

options:
    keyvault_uri:
        description:
            - URI of the keyvault endpoint.
        type: str
    hsm_name:
        description:
            - Name of the HSM.
        type: str
    sd_quorum:
        description:
            - The minimum number of shares required to decrypt the security domain for recovery.
            - The quorum of security domain should be in range [2, 10].
        required: True
        type: int
    sd_wrapping_keys:
        description:
            - List of wrapping keys containing public keys.
            - The number of wrapping keys should be in range [3, 10].
        required: True
        type: list
        elements: str
    no_wait:
        description:
            - Don't wait for the operation to finish
        type: bool
        default: False
    action:
        description:
            - Action to take on Security Domain. Use C(download) to download security domain file and C(upload) to restore the HSM.
        default: download
        type: str
        choices:
            - download
            - upload

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)

'''

EXAMPLES = '''
- name: Download Security domain file
  azure_rm_keyvaultsecuritydomain:
    keyvault_uri: https://samplehsmvault.managedhsm.azure.net
    sd_quorum: 2
    sd_wrapping_keys:
      - "{{ lookup('file', 'certfile1') }}"
      - "{{ lookup('file', 'certfile2') }}"
      - "{{ lookup('file', 'certfile3') }}"
    action: download

- name: Upload Security domain
  azure_rm_keyvaultsecuritydomain:
    keyvault_uri: https://samplehsmvault.managedhsm.azure.net
    action: upload
'''

RETURN = '''
security_domain:
    description:
        - JSON blob
    returned: always
    type: str
'''

import time
import codecs
import hashlib
import traceback
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible.module_utils.basic import missing_required_lib
from ansible_collections.azure.azcollection.plugins.module_utils.security_domain_utils import Utils


try:
    from cryptography.x509 import load_pem_x509_certificate
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.serialization import Encoding
    HAS_CRYPTO = True
    HAS_CRYPTO_EXC = None
except ImportError:
    load_pem_x509_certificate = None
    default_backend = None
    Encoding = None
    HAS_CRYPTO = False
    HAS_CRYPTO_EXC = traceback.format_exc()


try:
    from azure.keyvault.securitydomain import SecurityDomainClient
    from azure.keyvault.securitydomain.models import CertificateInfo, SecurityDomainJsonWebKey
    HAS_AZURE_CLI = True
    HAS_AZURE_CLI_EXC = None
except ImportError:
    CertificateInfo = None
    SecurityDomainJsonWebKey = None
    SecurityDomainClient = None
    HAS_AZURE_CLI = False
    HAS_AZURE_CLI_EXC = traceback.format_exc()


class AzureRMVaultSecurityDomain(AzureRMModuleBaseExt):
    """Configuration class for an Azure RM Vault Security Domain resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            keyvault_uri=dict(
                no_log=True,
                type='str'
            ),
            hsm_name=dict(
                type='str'
            ),
            sd_wrapping_keys=dict(
                type='list',
                required=True,
                no_log=True,
                elements='str'
            ),
            sd_quorum=dict(
                type='int',
                required=True
            ),
            no_wait=dict(
                type='bool',
                default='False'
            ),
            action=dict(
                type='str',
                default='download',
                choices=['download', 'upload']
            )
        )

        self.module_required_if = []

        self.keyvault_uri = None
        self.hsm_name = None

        self.results = dict(changed=False)
        self.client = None
        self.action = None
        self.sd_wrapping_keys = []
        self.sd_quorum = None
        self.no_wait = False

        required_one_of = [('keyvault_uri', 'hsm_name')]

        super(AzureRMVaultSecurityDomain, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                         supports_check_mode=False,
                                                         supports_tags=False,
                                                         required_one_of=required_one_of,
                                                         required_if=self.module_required_if)

        if not HAS_CRYPTO:
            self.fail(msg=missing_required_lib('cryptography'),
                      exception=HAS_CRYPTO_EXC)

        if not HAS_AZURE_CLI:
            self.fail(msg=missing_required_lib('azure-cli'),
                      exception=HAS_AZURE_CLI_EXC)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        # translate Ansible input to SDK-formatted dict in self.parameters
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        vault_base_url = self.hsm_name or self.keyvault_uri
        self.client = SecurityDomainClient(vault_base_url, credential=self.azure_auth.azure_credential_track2)

        response = None
        if self.action == 'download':
            response = self.security_domain_download()

            if response:
                self.results["security_domain"] = response.value

        return self.results

    def security_domain_download(self):

        N = len(self.sd_wrapping_keys)
        if N < 3 or N > 10:
            self.fail('The number of wrapping keys {0} should be in range [3, 10].'.format(N))
        if self.sd_quorum < 2 or self.sd_quorum > 10:
            self.fail('The quorum of security domain {0} should be in range [2, 10].'.format(self.sd_quorum))

        certificates = []
        for pem_string in self.sd_wrapping_keys:
            pem_data = pem_string.encode('UTF-8')

            cert = load_pem_x509_certificate(pem_data, backend=default_backend())
            public_key = cert.public_key()
            public_bytes = cert.public_bytes(Encoding.DER)
            x5c = [Utils.security_domain_b64_url_encode_for_x5c(public_bytes)]  # only one cert, not a chain
            x5t = Utils.security_domain_b64_url_encode(hashlib.sha1(public_bytes).digest())
            x5tS256 = Utils.security_domain_b64_url_encode(hashlib.sha256(public_bytes).digest())
            key_ops = ["verify", "encrypt", "wrapKey"]

            # populate key into jwk
            kty = "RSA"
            alg = "RSA-OAEP-256"
            n, e = _public_rsa_key_to_jwk(public_key, encoding=Utils.security_domain_b64_url_encode)

            certificates.append(
                SecurityDomainJsonWebKey(
                    kid=cert.subject.rfc4514_string(),
                    kty=kty,
                    key_ops=key_ops,
                    n=n,
                    e=e,
                    x5_c=x5c,
                    alg=alg,
                    x5_t=x5t,
                    x5_t_s256=x5tS256,
                )
            )

        certs_object = CertificateInfo(certificates=certificates, required=self.sd_quorum)

        poller = self.client.begin_download(certificate_info=certs_object, skip_activation_polling=True)
        security_domain = poller.result()

        if not self.no_wait:
            wait_second = 5
            time.sleep(wait_second)
            polling_ret = _wait_security_domain_operation(self.client,
                                                          'download')
            if polling_ret is None or getattr(polling_ret, 'status', None) == 'Failed':
                self.fail('Status: {0}'.format(polling_ret))

        return security_domain


def _int_to_bytes(i):
    h = hex(i)
    if len(h) > 1 and h[0:2] == '0x':
        h = h[2:]
    # need to strip L in python 2.x
    h = h.strip('L')
    if len(h) % 2:
        h = '0' + h
    return codecs.decode(h, 'hex')


def _public_rsa_key_to_jwk(rsa_key, encoding=None):
    public_numbers = rsa_key.public_numbers()
    n = _int_to_bytes(public_numbers.n)
    if encoding:
        n = encoding(n)
    e = _int_to_bytes(public_numbers.e)
    if encoding:
        e = encoding(e)
    return (n, e)


def _wait_security_domain_operation(client, target_operation='upload'):
    retries = 0
    max_retries = 30
    wait_second = 10
    while retries < max_retries:
        try:
            ret = None
            if target_operation == 'upload':
                ret = client.get_upload_status()
            elif target_operation == 'download':
                ret = client.get_download_status()

            # v7.2-preview and v7.2 will change the upload operation from Sync to Async
            # due to service defects, it returns 'Succeeded' before the change and 'Success' after the change
            if ret and getattr(ret, 'status', None) in ['Succeeded', 'Success', 'Failed']:
                return ret
        except Exception:
            pass
        time.sleep(wait_second)
        retries += 1

    return None


def main():
    """Main execution"""
    AzureRMVaultSecurityDomain()


if __name__ == '__main__':
    main()
