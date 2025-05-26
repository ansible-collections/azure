#!/usr/bin/python
#
# Copyright (c) 2025 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_keyvaultcertificate
version_added: "3.4.0"
short_description: Managed keyvault certificate
description:
    - Managed keyvault certificate.

options:
    vault_uri:
        description:
            - Vault uri where the certificate stored in.
        required: True
        type: str
    name:
        description:
            - Certificate name.
        type: str
        required: True
    policy:
        description:
            - The management policy for the certificate.
            - When generating a new certificate, if no policy is set, the default policy will be used.
        type: dict
        suboptions:
            subject:
                description:
                    - The subject name of the certificate. Should be a valid X509 distinguished name.
                    - Either subject or one of the subject alternative name parameters are required for creating a certificate.
                    - This will be ignored when importing a certificate; the subject will be parsed from the imported certificate.
                type: str
            issuer_name:
                description:
                    - Name of the referenced issuer object or reserved names. For example C(self) and C(unknown).
                type: str
                choices:
                    - self
                    - unknown
            exportable:
                description:
                    - Indicates if the private key can be exported. For valid values, see KeyType.
                type: bool
            key_type:
                description:
                    - The type of key pair to be used for the certificate.
                type: str
                choices:
                    - EC
                    - EC-HSM
                    - RSA
                    - RSA-HSM
                    -  oct
                    - oct-HSM
            key_size:
                description:
                    - The key size in bits. For example C(2048), C(3072), or C(4096) for RSA.
                type: int
            reuse_key:
                description:
                    - Indicates if the same key pair will be used on certificate renewal.
                type: bool
            key_curve_name:
                description:
                    - Elliptic curve name. For valid values, see KeyCurveName.
                type: str
                choices:
                    - P-256
                    - P-384
                    - P-521
                    - P-256K
            enhanced_key_usage:
                description:
                    - The extended ways the key of the certificate can be used.
                type: list
                elements: str
            content_type:
                description:
                    - he media type (MIME type) of the secret backing the certificate.
                type: str
                default: application/x-pkcs12
                choices:
                    - application/x-pkcs12
                    - application/x-pem-file
            key_usage:
                description:
                    - The extended ways the key of the certificate can be used.
                type: list
                elements: str
                choices:
                    - digitalSignature
                    - nonRepudiation
                    - keyEncipherment
                    - dataEncipherment
                    - keyAgreement
                    - keyCertSign
                    - cRLSign
                    - encipherOnly
                    - decipherOnly
            validity_in_months:
                description:
                    - The duration that the certificate is valid in months.
                type: int
            lifetime_actions:
                description:
                    - Actions that will be performed by Key Vault over the lifetime of a certificate.
                type: list
                elements: dict
                suboptions:
                    action:
                        description:
                            - The type of the action.
                        type: str
                        choices:
                            - EmailContacts
                            - AutoRenew
                    lifetime_percentage:
                        description:
                            - Percentage of lifetime at which to trigger. Value should be between 1 and 99.
                        type: int
                    days_before_expiry:
                        description:
                            - Days before expiry to attempt renewal.
                            - Value should be between 1 and `validity_in_months` multiplied by 27.
                            - If validity_in_months is 36, then value should be between 1 and 972 (36 * 27).
                        type: int
            certificate_type:
                description:
                    - Type of certificate to be requested from the issuer provider.
                type: str
            san_emails:
                description:
                    - Subject alternative emails of the X509 object.
                    - Either subject or one of the subject alternative name parameters are required for creating a certificate.
                type: list
                elements: str
            certificate_transparency:
                description:
                    - Indicates if the certificates generated under this policy should be published to certificate transparency logs.
                type: bool
            san_dns_names:
                description:
                    - Subject alternative DNS names of the X509 object.
                    - Either subject or one of the subject alternative name parameters are required for creating a certificate.
                type: list
                elements: str
            san_user_principal_names:
                description:
                    - Subject alternative user principal names of the X509 object.
                    - Either subject or one of the subject alternative name parameters are required for creating a certificate.
                type: list
                elements: str
    enabled:
        description:
            - Whether the certificate is enabled for use.
        type: bool
    password:
        description:
            - If the private key in the passed in certificate is encrypted, it is the password used for encryption.
        type: str
    cert_data:
        description:
            - Aan existing valid certificate, containing a private key, into Azure Key Vault.
        type: str
    state:
        description:
            - State of the keyvault certificate.
        type: str
        required: True
        choices:
            - generate
            - import
            - delete
            - purge
            - recover
            - merge
            - update

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Import a keyvault certificate
  azure_rm_keyvaultcertificate:
    vault_uri: https://vault{{ rpfx }}.vault.azure.net
    name: fredcerticate
    enabled: true
    password: Password@****
    cert_data: "{{ lookup('file', 'cert.pem') }}"
    state: import
    tags:
      key1: value1

- name: Generate a keyvault certificate
  azure_rm_keyvaultcertificate:
    vault_uri: https://vault{{ rpfx }}.vault.azure.net
    name: fredcerticate
    policy:
      subject: 'CN=Anhui02'
      issuer_name: self
      exportable: true
      key_type: RSA
      key_size: 2048
      san_emails:
        - 7170222076@qq.com
      content_type: 'application/x-pkcs12'
      validity_in_months: 36
      lifetime_actions:
        - action: EmailContacts
          days_before_expiry: 10
    enabled: true
    state: generate


- name: Update the keyvault certificate
  azure_rm_keyvaultcertificate:
    vault_uri: https://vault{{ rpfx }}.vault.azure.net
    name: fredcerticate
    policy:
      subject: 'CN=Anhui'
      issuer_name: self
      exportable: true
      key_type: RSA
      key_size: 2048
      san_emails:
        - 7170222076@qq.com
      content_type: 'application/x-pkcs12'
      validity_in_months: 36
      lifetime_actions:
        - action: EmailContacts
          days_before_expiry: 10
    enabled: true
    state: update

- name: Purge the keyvault certificate
  azure_rm_keyvaultcertificate:
    vault_uri: https://vault{{ rpfx }}.vault.azure.net
    name: fredcerticate
    state: purge

- name: Recover the keyvault certificate
  azure_rm_keyvaultcertificate:
    vault_uri: https://vault{{ rpfx }}.vault.azure.net
    name: fredcerticate
    state: recover

- name: Delete the keyvault certificate
  azure_rm_keyvaultcertificate:
    vault_uri: https://vault{{ rpfx }}.vault.azure.net
    name: fredcerticate
    state: absent
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
            sample: "bytearray(b'0.....................x16')"
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
            sample: 2025-01-14T09"
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
            sample: 2025-02-14T09"
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

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.keyvault.certificates import CertificateClient, CertificatePolicy, LifetimeAction
    import base64
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


def certificatebundle_to_dict(certificate):
    response = dict(policy=dict(), properties=dict(), cert_data=None)
    if certificate.cer is not None:
        response['cert_data'] = str(certificate.cer)
    response['name'] = certificate.name
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


def policy_bundle_to_dict(policy):
    result = dict()
    if policy is not None:
        result['issuer_name'] = policy._issuer_name
        result['subject'] = policy._subject
        result['exportable'] = policy._exportable
        result['key_type'] = policy._key_type
        result['key_size'] = policy._key_size
        result['reuse_key'] = policy._reuse_key
        result['key_curve_name'] = policy._key_curve_name
        result['enhanced_key_usage'] = policy._enhanced_key_usage
        result['key_usage'] = policy._key_usage
        result['content_type'] = policy._content_type
        result['validity_in_months'] = policy._validity_in_months
        result['certificate_type'] = policy._certificate_type
        result['certificate_transparency'] = policy._certificate_transparency
        result['san_emails'] = policy._san_emails
        result['san_dns_names'] = policy._san_dns_names
        result['san_user_principal_names'] = policy._san_user_principal_names
        result['attributes'] = dict()
        if policy._attributes is not None:
            result['attributes']['enabled'] = policy._attributes.enabled
            result['attributes']['not_before'] = policy._attributes.not_before
            result['attributes']['expires'] = policy._attributes.expires
            result['attributes']['created'] = policy._attributes.created
            result['attributes']['updated'] = policy._attributes.updated
            result['attributes']['recoverable_days'] = policy._attributes.recoverable_days
            result['attributes']['recovery_level'] = policy._attributes.recovery_level
        else:
            result['attributes'] = None
        if policy._lifetime_actions is not None:
            result['lifetime_actions'] = []
            for item in policy._lifetime_actions:
                result['lifetime_actions'].append(dict(action=item.action,
                                                       lifetime_percentage=item.lifetime_percentage,
                                                       days_before_expiry=item.days_before_expiry))
        else:
            result['lifetime_actions'] = None
    else:
        result = None

    return result


def deleted_certificatebundle_to_dict(certificate):
    response = dict(policy=dict(), properties=dict(), cert_data=None)
    if certificate.cer is not None:
        response['cert_data'] = str(certificate.cer)
    response['name'] = certificate.name
    response['recovery_id'] = certificate._recovery_id
    response['scheduled_purge_date'] = certificate._scheduled_purge_date
    response['deleted_on'] = certificate._deleted_on
    if certificate.cer is not None:
        response['cert_data'] = str(certificate.cer)
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


policy_spec = dict(
    issuer_name=dict(type='str', choices=['self', 'unknown']),
    subject=dict(type='str'),
    exportable=dict(type='bool',),
    key_type=dict(type='str', choices=['EC', 'EC-HSM', 'RSA', 'RSA-HSM', 'oct', 'oct-HSM']),
    key_size=dict(type='int'),
    reuse_key=dict(type='bool',),
    key_curve_name=dict(type='str', choices=['P-256', 'P-384', 'P-521', 'P-256K']),
    enhanced_key_usage=dict(type='list', elements='str'),
    key_usage=dict(
        type='list',
        elements='str',
        choices=['digitalSignature', 'nonRepudiation', 'keyEncipherment', 'dataEncipherment',
                 'keyAgreement', 'keyCertSign', 'cRLSign', 'encipherOnly', 'decipherOnly']
    ),
    content_type=dict(type='str', default='application/x-pkcs12', choices=['application/x-pkcs12', 'application/x-pem-file']),
    validity_in_months=dict(type='int',),
    certificate_type=dict(type='str'),
    certificate_transparency=dict(type='bool'),
    san_emails=dict(type='list', elements='str'),
    san_dns_names=dict(type='list', elements='str'),
    san_user_principal_names=dict(type='list', elements='str'),
    lifetime_actions=dict(
        type='list',
        elements='dict',
        options=dict(
            action=dict(type='str', choices=['EmailContacts', 'AutoRenew']),
            lifetime_percentage=dict(type='int'),
            days_before_expiry=dict(type='int')
        )
    ),
)


class AzureRMKeyVaultCertificate(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(name=dict(type='str', required=True),
                                    vault_uri=dict(type='str', required=True),
                                    policy=dict(type='dict', options=policy_spec),
                                    enabled=dict(type='bool'),
                                    password=dict(type='str', no_log=True),
                                    cert_data=dict(type='str'),
                                    state=dict(
                                        type='str',
                                        required=True,
                                        choices=['generate', 'import', 'delete', 'purge', 'update', 'recover', 'merge']))
        self.vault_uri = None
        self.name = None
        self.policy = None
        self.enabled = None
        self.cert_data = None
        self.password = None
        self.state = None
        self.tags = None

        self.results = dict(changed=False)
        self._client = None
        required_if = [('state', 'import', ['cert_data', 'password'])]

        super(AzureRMKeyVaultCertificate,
              self).__init__(derived_arg_spec=self.module_arg_spec,
                             supports_check_mode=True,
                             supports_tags=True,
                             required_if=required_if,
                             facts_module=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, None)

        self._client = self.get_keyvault_client()
        changed = False
        response = None

        del_response = self.get_deleted_certificate()
        response = self.get_certificate()

        if self.state == 'delete':
            if response is not None:
                changed = True
                if not self.check_mode:
                    response = self.delete_certificate()
        elif self.state == 'purge':
            if del_response is not None:
                changed = True
                if not self.check_mode:
                    response = self.purge_certificate()
        elif self.state == 'merge':
            if response is not None:
                changed = True
                if not self.check_mode:
                    response = self.merge_certificate()
            else:
                self.fail("The certificate not exist {0}".format(self.name))
        elif self.state == 'recover':
            if del_response is not None:
                changed = True
                if not self.check_mode:
                    response = self.recover_certificate()
            else:
                self.log("The certificate {0} exist or purged".format(self.name))
        else:
            if response is not None:
                a = {}
                b = dict(compare=[])

                # if not self.default_compare({}, self.policy, response['policy'], '', dict(compare=[])):
                if not self.default_compare(a, self.policy, response['policy'], '', b):
                    changed = True
                    if not self.check_mode:
                        response['policy'] = self.update_certificate_policy()

                update_tags, self.tags = self.update_tags(response['properties']['tags'])
                if update_tags or (self.enabled is not None and bool(self.enabled) != bool(response['properties']['attributes']['enabled'])):
                    changed = True
                    if not self.check_mode:
                        response = self.update_certificate_properties()
            else:
                changed = True
                if self.state == 'import':
                    if not self.check_mode:
                        response = self.import_certificate()
                else:
                    if not self.check_mode:
                        response = self.create_certificate()

        self.results['changed'] = changed
        self.results['certificate'] = response

        return self.results

    def get_keyvault_client(self):

        return CertificateClient(vault_url=self.vault_uri, credential=self.azure_auth.azure_credential_track2)

    def get_certificate(self):
        '''
        Gets the certificate fact of the specified in key vault.

        :return: deserialized certificate state dictionary
        '''
        self.log("Get the certificate {0}".format(self.name))

        try:
            return certificatebundle_to_dict(self._client.get_certificate(certificate_name=self.name))

        except Exception as ec:
            self.log("Did not find the key vault certificate {0}: {1}".format(self.name, str(ec)))

    def create_certificate(self):
        '''
        Create the certificate in key vault.

        :return: deserialized certificate state dictionary
        '''
        self.log("Create the certificate {0}".format(self.name))

        lifetime_actions = []
        for item in self.policy['lifetime_actions']:
            lifetime_actions.append(LifetimeAction(**item))

        try:
            if self.policy is None:
                policy = CertificatePolicy.get_default()
            else:
                policy = CertificatePolicy(subject=self.policy.get('subject'),
                                           issuer_name=self.policy.get('issuer_name'),
                                           exportable=self.policy.get('exportable'),
                                           key_type=self.policy.get('key_type'),
                                           key_size=self.policy.get('key_size'),
                                           san_emails=self.policy.get('san_emails'),
                                           content_type=self.policy.get('content_type'),
                                           validity_in_months=self.policy.get('validity_in_months'),
                                           reuse_key=self.policy.get('reuse_key'),
                                           key_curve_name=self.policy.get('key_curve_name'),
                                           enhanced_key_usage=self.policy.get('enhanced_key_usage'),
                                           key_usage=self.policy.get('key_usage'),
                                           certificate_type=self.policy.get('certificate_type'),
                                           certificate_transparency=self.policy.get('certificate_transparency'),
                                           san_dns_names=self.policy.get('san_dns_names'),
                                           lifetime_actions=lifetime_actions,
                                           san_user_principal_names=self.policy.get('san_user_principal_names'))
            response = self._client.begin_create_certificate(certificate_name=self.name,
                                                             policy=policy,
                                                             enabled=self.enabled,
                                                             tags=self.tags)
            if isinstance(response, LROPoller):
                return certificatebundle_to_dict(self.get_poller_result(response))

        except Exception as ec:
            self.fail("Did not create the key vault certificate {0}: {1}".format(self.name, str(ec)))

    def import_certificate(self):
        '''
        Import the certificate in key vault.

        :return: deserialized certificate state dictionary
        '''
        self.log("Import the certificate {0}".format(self.name))

        try:
            response = self._client.import_certificate(certificate_name=self.name,
                                                       certificate_bytes=self.cert_data.encode('utf-8'),
                                                       enabled=self.enabled,
                                                       password=self.password,
                                                       tags=self.tags)

            if response:
                response = certificatebundle_to_dict(response)
                return response

        except Exception as ec:
            self.fail("Did not import the key vault certificate {0}: {1}".format(self.name, str(ec)))

    def delete_certificate(self):
        '''
        Delete the certificate in key vault.

        :return: deserialized certificate state dictionary
        '''
        self.log("Delete the certificate {0}".format(self.name))

        try:
            response = self._client.begin_delete_certificate(certificate_name=self.name)
            if isinstance(response, LROPoller):
                return deleted_certificatebundle_to_dict(self.get_poller_result(response))
            self.log("Delete the certificate")
        except Exception as ec:
            self.fail("Did not delete the key vault certificate {0}: {1}".format(self.name, str(ec)))

    def get_deleted_certificate(self):
        '''
        Gets the deleted certificate facts in key vault.

        :return: deserialized certificate state dictionary
        '''
        self.log("Get the certificate {0}".format(self.name))

        try:
            return deleted_certificatebundle_to_dict(self._client.get_deleted_certificate(certificate_name=self.name))
        except Exception as ec:
            self.log("Find the key vault certificate got exception, exception as {0}".format(str(ec)))

    def recover_certificate(self):
        '''
        Recover the certificate in key vault.

        :return: deserialized certificate state dictionary
        '''
        self.log("Recover the certificate {0}".format(self.name))

        try:
            response = self._client.begin_recover_deleted_certificate(certificate_name=self.name)
            if isinstance(response, LROPoller):
                return certificatebundle_to_dict(self.get_poller_result(response))

        except Exception as ec:
            self.fail("Did not recover the key vault certificate {0}: {1}".format(self.name, str(ec)))

    def update_certificate_properties(self):
        '''
        Update the certificate properties in key vault.

        :return: deserialized certificate state dictionary
        '''
        self.log("Merge the certificate {0}".format(self.name))

        try:
            response = self._client.update_certificate_properties(certificate_name=self.name,
                                                                  version=None,
                                                                  enabled=self.enabled,
                                                                  tags=self.tags)
            if response is not None:
                return certificatebundle_to_dict(response)
        except Exception as ec:
            self.fail("Did not update the key vault certificate {0}: {1}".format(self.name, str(ec)))

    def update_certificate_policy(self):
        '''
        Update the certificate policy in key vault.

        :return: deserialized certificate state dictionary
        '''
        self.log("Update the certificate policy {0}".format(self.name))

        lifetime_actions = []
        for item in self.policy['lifetime_actions']:
            lifetime_actions.append(LifetimeAction(**item))

        policy = CertificatePolicy(subject=self.policy.get('subject'),
                                   issuer_name=self.policy.get('issuer_name'),
                                   exportable=self.policy.get('exportable'),
                                   key_type=self.policy.get('key_type'),
                                   key_size=self.policy.get('key_size'),
                                   san_emails=self.policy.get('san_emails'),
                                   content_type=self.policy.get('content_type'),
                                   validity_in_months=self.policy.get('validity_in_months'),
                                   reuse_key=self.policy.get('reuse_key'),
                                   key_curve_name=self.policy.get('key_curve_name'),
                                   enhanced_key_usage=self.policy.get('enhanced_key_usage'),
                                   key_usage=self.policy.get('key_usage'),
                                   certificate_type=self.policy.get('certificate_type'),
                                   certificate_transparency=self.policy.get('certificate_transparency'),
                                   san_dns_names=self.policy.get('san_dns_names'),
                                   lifetime_actions=lifetime_actions,
                                   san_user_principal_names=self.policy.get('san_user_principal_names'))
        try:
            response = self._client.update_certificate_policy(certificate_name=self.name,
                                                              policy=policy)
            if response is not None:
                return policy_bundle_to_dict(response)

        except Exception as ec:
            self.fail("Did not update policy in the key vault certificate {0}: {1}".format(self.name, str(ec)))

    def purge_certificate(self):
        '''
        Permanently deletes a deleted certificate.
        '''
        self.log("Permanently deletes the certificate {0}".format(self.name))

        try:
            self._client.purge_deleted_certificate(certificate_name=self.name)

        except Exception as ec:
            self.fail("Did not permanently delete the key vault certificate {0}: {1}".format(self.name, str(ec)))


def main():
    """Main execution"""
    AzureRMKeyVaultCertificate()


if __name__ == '__main__':
    main()
