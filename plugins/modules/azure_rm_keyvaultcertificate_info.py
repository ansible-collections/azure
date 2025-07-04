#!/usr/bin/python
#
# Copyright (c) 2025 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_keyvaultcertificate_info
version_added: "3.1.0"
short_description: Get Azure Key Vault certificate facts
description:
    - Get or list facts of Azure Key Vault certificate(deleted).

options:
    vault_uri:
        description:
            - Vault uri where the certificate stored in.
        required: True
        type: str
    name:
        description:
            - Certificate name. If not set, will list all certificates in vault_uri.
        type: str
    version:
        description:
            - The version of the certificate.
        type: str
    show_deleted_certificate:
        description:
            - Set to I(show_delete_certificate=true) to show deleted certificates. Set to I(show_deleted_certificate=false) to show not deleted certificates.
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
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Get certificate facts
  azure_rm_keyvaultcertificate_info:
    vault_uri: "https://myVault.vault.azure.net"
    name: myCertificate

- name: Get specific versions of certificate
  azure_rm_keyvaultcertificate_info:
    vault_uri: "https://myVault.vault.azure.net"
    name: mySecret
    version: 2809225bcb674ff380f330471b3c3eb0

- name: Get deleted certificate
  azure_rm_keyvaultcertificate_info:
    vault_uri: "https://myVault.vault.azure.net"
    name: mySecret
    show_deleted_certificate: true

- name: List deleted certificate
  azure_rm_keyvaultcertificate_info:
    vault_uri: "https://myVault.vault.azure.net"
    show_deleted_certificate: true
'''

RETURN = '''
certificates:
    description:
        - The facts of certificates in Azure Key Vault.
    returned: always
    type: complex
    contains:
        cert_data:
            description:
                - CER contents of the X509 certificate.
            type: str
            returned: always
            sample: "MIID*****************0pRjXE"
        name:
            description:
                - The name of the certificate.
            type: str
            returned: always
            sample: testcert
        deleted_on:
            description:
                - The time when the certificate was deleted, in UTC.
            returned: always
            type: str
            sample: 2025-01-14T09
        recovery_id:
            description:
                - The url of the recovery object, used to identify and recover the deleted certificate.
            type: str
            returned: always
            sample: "https://vaultrfred01.vault.azure.net/deletedcertificates/cert02"
        scheduled_purge_date:
            description:
                - The time when the certificate is scheduled to be purged, in UTC.
            returned: always
            type: dict
            sample: 2025-02-14T09
        policy:
            description:
                - The management policy of the deleted certificate.
            returned: always
            type: complex
            contains:
                attributes:
                    description:
                        - Certificate attributes.
                    type: complex
                    returned: always
                    contains:
                        created:
                            description:
                                - Creation datetime.
                            returned: always
                            type: str
                            sample: "2025-01-14T09:41:20+00:00"
                        not_before:
                            description:
                                - Not before datetime.
                            type: str
                            sample: None
                        expires:
                            description:
                                - Expiration datetime.
                            type: str
                            sample: None
                        updated:
                            description:
                                - Update datetime.
                            returned: always
                            type: str
                            sample: "2025-01-15T09:41:20+00:00"
                        enabled:
                            description:
                                - Indicate whether the certificate is enabled.
                            returned: always
                            type: str
                            sample: true
                        recovery_level:
                            description:
                                - Reflects the deletion recovery level currently in effect for certificates in the current vault.
                                - If it contains 'Purgeable' the certificate can be permanently deleted by a privileged user,
                                - Otherwise, only the system can purge the certificate, at the end of the retention interval.
                            returned: always
                            type: str
                            sample: None
                        recoverable_days:
                            description:
                                - Reflects the deletion recovery days.
                            type: int
                            returned: always
                            sample: None
                issuer_name:
                    description:
                        - Name of the referenced issuer object or reserved names.
                    type: str
                    returned: always
                    sample: Self
                subject:
                    description:
                        - The subject name of the certificate.
                        - Should be a valid X509 distinguished name.
                        - Either subject or one of the subject alternative name parameters are required for creating a certificate.
                        - This will be ignored when importing a certificate; the subject will be parsed from the imported certificate.
                    type: str
                    returned: always
                    sample: CN=anhui.com
                san_emails:
                    description:
                        - Subject alternative emails of the X509 object.
                        - Either subject or one of the subject alternative name parameters are required for creating a certificate.
                    type: str
                    returned: always
                    sample: None
                san_dns_names:
                    description:
                        - Subject alternative DNS names of the X509 object.
                        - Either subject or one of the subject alternative name parameters are required for creating a certificate.
                    type: str
                    returned: always
                    sample: None
                san_user_principal_names:
                    description:
                        - Subject alternative user principal names of the X509 object.
                        - Either subject or one of the subject alternative name parameters are required for creating a certificate.
                    type: str
                    returned: always
                    sample: None
                exportable:
                    description:
                        - Indicates if the private key can be exported.
                    type: bool
                    returned: always
                    sample: true
                key_type:
                    description:
                        - The type of key pair to be used for the certificate.
                    type: str
                    returned: always
                    sample: RSA
                key_size:
                    description:
                        - The key size in bits.
                    type: int
                    returned: always
                    sample: 2048
                reuse_key:
                    description:
                        - Indicates if the same key pair will be used on certificate renewal.
                    type: bool
                    returned: always
                    sample: false
                key_curve_name:
                    description:
                        - Elliptic curve name. For valid values, see KeyCurveName.
                    type: str
                    returned: always
                    sample: None
                enhanced_key_usage:
                    description:
                        - The extended ways the key of the certificate can be used.
                    type: list
                    returned: always
                    sample: ['1.3.6.1.5.5.7.3.1', '1.3.6.1.5.5.7.3.2']
                key_usage:
                    description:
                        - List of key usages.
                    type: list
                    returned: always
                    sample: ["digitalSignature", "keyEncipherment"]
                content_type:
                    description:
                        - If not specified, the media type (MIME type) of the secret backing the certificate.
                    type: str
                    returned: always
                    sample: application/x-pkcs12
                validity_in_months:
                    description:
                        - The duration that the certificate is valid in months.
                    type: int
                    returned: always
                    sample: 12
                lifetime_actions:
                    description:
                        - Actions that will be performed by Key Vault over the lifetime of a certificate.
                    type: list
                    returned: always
                    sample: [{'action': 'AutoRenew', 'days_before_expiry': None, 'lifetime_percentage': 80}]
                certificate_type:
                    description:
                        - Type of certificate to be requested from the issuer provider.
                    type: str
                    returned: str
                    sample: None
                certificate_transparency:
                    description:
                        - Indicates if the certificates generated under this policy should be published to certificate transparency logs.
                    type: bool
                    returned: always
                    sample: None
        properties:
            description:
                - The certificate's properties.
            type: complex
            returned: always
            contains:
                id:
                    description:
                        - Id of the certificate. If specified all other 'Id' arguments should be omitted.
                    type: str
                    returned: always
                    sample: "https://vaultrfred01.vault.azure.net/certificates/cert02/62409e6304c642f193209729b8360d2c"
                vault_id:
                    description:
                        - ID of the Key Vault.
                    type: str
                    returned: always
                    sample: "https://vaultrfred01.vault.azure.net"
                x509_thumbprint:
                    description:
                        - The X509 Thumbprint of the Key Vault Certificate represented as a hexadecimal string.
                    type: str
                    returned: always
                    sample: 1blAnHN9ddng0qh1pYoUDY2lp1E=
                tags:
                    description:
                        - List of the certificate tags.
                    type: dict
                    returned: always
                    sample: {'key': 'value'}
                attributes:
                    description:
                        - Certificate attributes.
                    type: complex
                    returned: always
                    contains:
                        created:
                            description:
                                - Creation datetime.
                            returned: always
                            type: str
                            sample: "2025-01-14T09"
                        not_before:
                            description:
                                - Not before datetime.
                            type: str
                            sample: "2025-02-14T09"
                        expires:
                            description:
                                - Expiration datetime.
                            type: str
                            sample: "2025-03-14T09"
                        updated:
                            description:
                                - Update datetime.
                            returned: always
                            type: str
                            sample: "2025-01-15T09"
                        enabled:
                            description:
                                - Indicate whether the certificate is enabled.
                            returned: always
                            type: str
                            sample: true
                        recovery_level:
                            description:
                                - Reflects the deletion recovery level currently in effect for certificates in the current vault.
                                - If it contains 'Purgeable' the certificate can be permanently deleted by a privileged user,
                                - Otherwise, only the system can purge the certificate, at the end of the retention interval.
                            returned: always
                            type: str
                            sample: Recoverable+Purgeable
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.keyvault.certificates import CertificateClient
    from azure.core.exceptions import ResourceNotFoundError
    import base64
except ImportError:
    # This is handled in azure_rm_common
    pass


def certificatebundle_to_dict(certificate):
    response = dict(policy=dict(), properties=dict(), cert_data=None)
    if certificate.cer is not None:
        response['cert_data'] = base64.b64encode(certificate.cer).decode('utf-8')
    response['name'] = certificate.name
    if certificate.policy is not None:
        response['policy']['issuer_name'] = certificate.policy._issuer_name
        response['policy']['subject'] = certificate.policy._subject
        response['policy']['exportable'] = certificate.policy._exportable
        response['policy']['key_type'] = certificate.policy._key_type
        response['policy']['reuse_key'] = certificate.policy._reuse_key
        response['policy']['key_size'] = certificate.policy._key_size
        response['policy']['key_curve_name'] = certificate.policy._key_curve_name
        response['policy']['enhanced_key_usage'] = certificate.policy._enhanced_key_usage
        response['policy']['key_usage'] = certificate.policy._key_usage
        response['policy']['content_type'] = certificate.policy._content_type
        response['policy']['validity_in_months'] = certificate.policy._validity_in_months
        response['policy']['certificate_type'] = certificate.policy._certificate_type
        response['policy']['certificate_transparency'] = certificate.policy._certificate_transparency
        response['policy']['san_emails'] = certificate.policy._san_emails
        response['policy']['san_dns_names'] = certificate.policy._san_dns_names
        response['policy']['san_user_principal_names'] = certificate.policy._san_user_principal_names
        response['policy']['attributes'] = dict()
        if certificate.policy._attributes is not None:
            response['policy']['attributes']['enabled'] = certificate.policy._attributes.enabled
            response['policy']['attributes']['not_before'] = certificate.policy._attributes.not_before
            response['policy']['attributes']['expires'] = certificate.policy._attributes.expires
            response['policy']['attributes']['created'] = certificate.policy._attributes.created
            response['policy']['attributes']['updated'] = certificate.policy._attributes.updated
            response['policy']['attributes']['recoverable_days'] = certificate.policy._attributes.recoverable_days
            response['policy']['attributes']['recovery_level'] = certificate.policy._attributes.recovery_level
        else:
            response['policy']['attributes'] = None
        if certificate.policy._lifetime_actions is not None:
            response['policy']['lifetime_actions'] = []
            for item in certificate.policy._lifetime_actions:
                response['policy']['lifetime_actions'].append(dict(action=item.action,
                                                                   lifetime_percentage=item.lifetime_percentage,
                                                                   days_before_expiry=item.days_before_expiry))
        else:
            response['policy']['lifetime_actions'] = None
    else:
        response['policy'] = None

    if certificate.properties is not None:
        response['properties']['attributes'] = dict(enabled=certificate.properties._attributes.enabled,
                                                    not_before=certificate.properties._attributes.not_before,
                                                    expires=certificate.properties._attributes.expires,
                                                    created=certificate.properties._attributes.created,
                                                    updated=certificate.properties._attributes.updated,
                                                    recovery_level=certificate.properties._attributes.recovery_level)
        response['properties']['id'] = certificate.properties._id
        response['properties']['vault_id'] = certificate.properties._vault_id.vault_url if certificate.properties._vault_id is not None else None
        response['properties']['x509_thumbprint'] = base64.b64encode(certificate.properties._x509_thumbprint).decode('utf-8')
        response['properties']['tags'] = certificate.properties._tags
    else:
        response['properties'] = None

    return response


def deleted_certificatebundle_to_dict(certificate):
    response = dict(policy=dict(), properties=dict(), cert_data=None)
    if certificate.cer is not None:
        response['cert_data'] = str(certificate.cer)
    response['name'] = certificate.name
    response['recovery_id'] = certificate._recovery_id
    response['scheduled_purge_date'] = certificate._scheduled_purge_date
    response['deleted_on'] = certificate._deleted_on
    if certificate.policy is not None:
        response['policy']['issuer_name'] = certificate.policy._issuer_name
        response['policy']['subject'] = certificate.policy._subject
        response['policy']['exportable'] = certificate.policy._exportable
        response['policy']['key_type'] = certificate.policy._key_type
        response['policy']['key_size'] = certificate.policy._key_size
        response['policy']['reuse_key'] = certificate.policy._reuse_key
        response['policy']['key_curve_name'] = certificate.policy._key_curve_name
        response['policy']['enhanced_key_usage'] = certificate.policy._enhanced_key_usage
        response['policy']['key_usage'] = certificate.policy._key_usage
        response['policy']['content_type'] = certificate.policy._content_type
        response['policy']['validity_in_months'] = certificate.policy._validity_in_months
        response['policy']['certificate_type'] = certificate.policy._certificate_type
        response['policy']['certificate_transparency'] = certificate.policy._certificate_transparency
        response['policy']['san_emails'] = certificate.policy._san_emails
        response['policy']['san_dns_names'] = certificate.policy._san_dns_names
        response['policy']['san_user_principal_names'] = certificate.policy._san_user_principal_names
        response['policy']['attributes'] = dict()
        if certificate.policy._attributes is not None:
            response['policy']['attributes']['enabled'] = certificate.policy._attributes.enabled
            response['policy']['attributes']['not_before'] = certificate.policy._attributes.not_before
            response['policy']['attributes']['expires'] = certificate.policy._attributes.expires
            response['policy']['attributes']['created'] = certificate.policy._attributes.created
            response['policy']['attributes']['updated'] = certificate.policy._attributes.updated
            response['policy']['attributes']['recoverable_days'] = certificate.policy._attributes.recoverable_days
            response['policy']['attributes']['recovery_level'] = certificate.policy._attributes.recovery_level
        else:
            response['policy']['attributes'] = None
        if certificate.policy._lifetime_actions is not None:
            response['policy']['lifetime_actions'] = []
            for item in certificate.policy._lifetime_actions:
                response['policy']['lifetime_actions'].append(dict(action=item.action,
                                                                   lifetime_percentage=item.lifetime_percentage,
                                                                   days_before_expiry=item.days_before_expiry))
        else:
            response['policy']['lifetime_actions'] = None
    else:
        response['policy'] = None

    if certificate.properties is not None:
        response['properties']['attributes'] = dict(enabled=certificate.properties._attributes.enabled,
                                                    not_before=certificate.properties._attributes.not_before,
                                                    expires=certificate.properties._attributes.expires,
                                                    created=certificate.properties._attributes.created,
                                                    updated=certificate.properties._attributes.updated,
                                                    recovery_level=certificate.properties._attributes.recovery_level)
        response['properties']['id'] = certificate.properties._id
        response['properties']['vault_id'] = certificate.properties._vault_id.vault_url if certificate.properties._vault_id is not None else None
        response['properties']['x509_thumbprint'] = base64.b64encode(certificate.properties._x509_thumbprint).decode('utf-8')
        response['properties']['tags'] = certificate.properties._tags
    else:
        response['properties'] = None
    return response


class AzureRMKeyVaultCertificateInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(version=dict(type='str'),
                                    name=dict(type='str'),
                                    vault_uri=dict(type='str', required=True),
                                    show_deleted_certificate=dict(type='bool', default=False),
                                    tags=dict(type='list', elements='str'))

        self.vault_uri = None
        self.name = None
        self.version = None
        self.show_deleted_certificate = False
        self.tags = None

        self.results = dict(changed=False)
        self._client = None

        super(AzureRMKeyVaultCertificateInfo,
              self).__init__(derived_arg_spec=self.module_arg_spec,
                             supports_check_mode=True,
                             supports_tags=False,
                             facts_module=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for certificate in list(self.module_arg_spec.keys()):
            if hasattr(self, certificate):
                setattr(self, certificate, kwargs[certificate])

        self._client = self.get_keyvault_client()

        if self.name:
            if self.show_deleted_certificate:
                self.results['certificates'] = self.get_deleted_certificate()
            else:
                if self.version is not None:
                    self.results['certificates'] = self.get_certificate_version()
                else:
                    self.results['certificates'] = self.get_certificate()
        else:
            if self.show_deleted_certificate:
                self.results['certificates'] = self.list_deleted_certificates()

        return self.results

    def get_keyvault_client(self):

        return CertificateClient(vault_url=self.vault_uri, credential=self.azure_auth.azure_credential_track2)

    def get_certificate(self):
        '''
        Gets the certificate fact of the specified certificate in key vault.

        :return: deserialized certificate state dictionary
        '''
        self.log("Get the certificate {0}".format(self.name))

        results = []
        try:
            response = self._client.get_certificate(certificate_name=self.name)

            if response:
                response = certificatebundle_to_dict(response)
                if self.has_tags(response['properties']['tags'], self.tags):
                    self.log("Response : {0}".format(response))
                    results.append(response)

        except ResourceNotFoundError as ec:
            self.log("Did not find the key vault certificate {0}: {1}".format(
                self.name, str(ec)))
        except Exception as ec2:
            self.fail("Find the key vault certificate got exception, exception as {0}".format(str(ec2)))
        return results

    def get_deleted_certificate(self):
        '''
        Gets the deleted certificate facts in key vault.

        :return: deserialized certificate state dictionary
        '''
        self.log("Get the certificate {0}".format(self.name))

        results = []
        try:
            response = self._client.get_deleted_certificate(certificate_name=self.name)
            if response:
                response = deleted_certificatebundle_to_dict(response)
                if self.has_tags(response['properties'].get('tags'), self.tags):
                    self.log("Response : {0}".format(response))
                    results.append(response)

        except ResourceNotFoundError as ec:
            self.log("Did not find the key vault certificate {0}: {1}".format(self.name, str(ec)))
        except Exception as ec2:
            self.fail("Find the key vault certificate got exception, exception as {0}".format(str(ec2)))
        return results

    def get_certificate_version(self):
        '''
        Lists certificates versions.

        :return: deserialized versions of certificate, includes certificate identifier, attributes and tags
        '''
        self.log("Get the certificate versions {0}".format(self.name))

        try:
            response = self._client.get_certificate_version(certificate_name=self.name, version=self.version)
            self.log("Response : {0}".format(response))

            if response:
                res = certificatebundle_to_dict(response)
                if self.has_tags(res['properties'].get('tags'), self.tags):
                    return res
        except Exception as e:
            self.fail("Did not find certificate versions {0} : {1}.".format(
                self.name, str(e)))

    def list_deleted_certificates(self):
        '''
        Lists deleted certificates in specific key vault.

        :return: deserialized certificates, includes certificate identifier, attributes and tags.
        '''
        self.log("Get the key vaults in current subscription")

        results = []
        try:
            response = self._client.list_deleted_certificates()
            self.log("Response : {0}".format(response))

            if response:
                for item in response:
                    item = deleted_certificatebundle_to_dict(item)
                    if self.has_tags(item['properties'].get('tags'), self.tags):
                        results.append(item)
        except Exception as e:
            self.fail("Did not find certificate in current key vault {0}.".format(str(e)))
        return results


def main():
    """Main execution"""
    AzureRMKeyVaultCertificateInfo()


if __name__ == '__main__':
    main()
