#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_appconfigurationkey_info
version_added: "3.15.0"
short_description: Get key-values (and Key Vault references) from Azure App Configuration.
description:
    - Read configuration settings (key-values or Key Vault references) from an Azure App Configuration store.
    - Supports lookup by key, by label, or by full listing.

options:
    endpoint:
        description:
            - The App Configuration data-plane endpoint, e.g. C(https://myappconf.azconfig.io).
        required: true
        type: str
    key:
        description:
            - Optional key filter. Supports exact key.
        type: str
    label:
        description:
            - Optional label filter.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: List all settings via endpoint
  azure.azcollection.azure_rm_appconfigurationkey_info:
    endpoint: https://myappconf.azconfig.io

- name: Get settings with a specific key + label
  azure.azcollection.azure_rm_appconfigurationkey_info:
    endpoint: https://myappconf.azconfig.io
    key: "Payments:TimeoutSeconds"
    label: "prod"
'''

RETURN = '''
settings:
    description:
        - List of configuration settings returned from the store.
    returned: always
    type: list
    contains:
        key:
            description:
                - The key of the configuration setting.
            type: str
            returned: always
            sample: "Payments:TimeoutSeconds"
        label:
            description:
                - The label of the configuration setting.
            type: str
            returned: always
            sample: "prod"
        value:
            description:
                - The value for C(type=kv).
            type: str
            returned: always
            sample: "30"
        content_type:
            description:
                - Content type metadata for the setting.
            type: str
            returned: always
            sample: "application/json"
        read_only:
            description:
                - Whether the setting is read-only in App Configuration.
            type: bool
            returned: always
            sample: false
        type:
            description:
                - The type of the configuration setting. Possible values are C(kv) and C(vault).
            type: str
            returned: always
            sample: "kv"
        vault_key_reference:
            description:
                - The Key Vault reference details for C(type=vault).
            type: str
            returned: when applicable
            sample: "https://myvault.vault.azure.net/secrets/mysecret/xxxx"
        id:
            description:
                - The unique identifier of the configuration setting.
            type: str
            returned: always
            sample: "https://myappconf.azconfig.io/kv/Payments:TimeoutSeconds?label=prod"
'''


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.appconfiguration import AzureAppConfigurationClient
except ImportError:
    pass


def normalize_setting(s, endpoint):
    d = s.as_dict()
    # infer type
    ct = (d.get("content_type") or "").lower()
    if ct.startswith("application/vnd.microsoft.appconfig.keyvaultref"):
        d["type"] = "vault"
        try:
            import json
            body = json.loads(d.get("value") or "{}")
            d["vault_key_reference"] = body.get("uri")
        except Exception:
            d["vault_key_reference"] = None
    else:
        d["type"] = "kv"
        d["vault_key_reference"] = None

    # add composed id
    base = endpoint.rstrip('/')
    key = d.get("key")
    label = d.get("label")
    if label:
        d["id"] = f"{base}/kv/{key}?label={label}"
    else:
        d["id"] = f"{base}/kv/{key}"
    return d


class AzureRMAppConfigurationKeyInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            endpoint=dict(type='str', required=True),
            key=dict(type='str', no_log=False),
            label=dict(type='str')
        )

        self.endpoint = None
        self.key = None
        self.label = None

        self.dataplane_client = None
        self.mgmt_client = None
        self.results = dict(changed=False)

        super(AzureRMAppConfigurationKeyInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                             supports_tags=False,
                                                             supports_check_mode=True)

    def exec_module(self, **kwargs):
        for k in self.module_arg_spec.keys():
            setattr(self, k, kwargs.get(k))

        self.dataplane_client = AzureAppConfigurationClient(self.endpoint,
                                                            credential=self.azure_auth.azure_credential_track2)

        out = []
        items = self.dataplane_client.list_configuration_settings(key_filter=self.key, label_filter=self.label)

        for s in items:
            nd = normalize_setting(s, self.endpoint)
            out.append(nd)

        self.results["settings"] = out
        return self.results


def main():
    AzureRMAppConfigurationKeyInfo()


if __name__ == '__main__':
    main()
