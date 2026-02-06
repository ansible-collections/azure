#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_appconfigurationkey
version_added: "3.15.0"
short_description: Manage key-values (and Key Vault reference) in Azure App Configuration.
description:
    - Create, update, lock/unlock, or delete a key in an Azure App Configuration store.
    - Supports both simple key-values (type=kv) and Key Vault reference (type=vault).
    - For C(type=vault), the module writes the reference value and content-type required by App Configuration.

options:
    endpoint:
        description:
            - The App Configuration data-plane endpoint, for example C(https://myappconf.azconfig.io).
        type: str
        required: true
    key:
        description:
            - Name of the configuration key.
            - Together with I(label), identifies a single setting.
        type: str
        required: true
    label:
        description:
            - Optional label to disambiguate settings with the same key.
        type: str
    type:
        description:
            - The setting type to manage.
            - C(kv) creates/updates a plain key-value.
            - C(vault) creates/updates a Key Vault reference entry.
        type: str
        choices:
            - kv
            - vault
        default: kv
    value:
        description:
            - The value for C(type=kv). Required when creating a new C(kv) setting.
            - Ignored on updates if you only want to change I(content_type), or I(read_only).
        type: str
    content_type:
        description:
            - Content type metadata for the setting.
            - Ignored for C(type=vault), the KV-reference content-type is fixed by the service.
        type: str
    vault_key_reference:
        description:
            - The versionless Key Vault Secret ID for a Key Vault reference C(type=vault).
        type: str
    read_only:
        description:
            - Whether the setting should be read-only in App Configuration.
        type: bool
    state:
        description:
            - Assert the state of the configuration setting. Use C(present) to create or update the setting and C(absent) to delete.
        type: str
        default: present
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)

'''

EXAMPLES = '''
- name: Create/Update a plain key-value
  azure.azcollection.azure_rm_appconfigurationkey:
    endpoint: https://myappconf.azconfig.io
    key: "Payments:TimeoutSeconds"
    label: "prod"
    type: kv
    value: "30"
    content_type: "text/plain"
    read_only: true
    state: present

- name: Create/Update a Key Vault reference (versionless secret ID)
  azure.azcollection.azure_rm_appconfigurationkey:
    endpoint: https://myappconf.azconfig.io
    key: "Payments:ApiKey"
    label: "prod"
    type: vault
    vault_key_reference: "https://myvault.vault.azure.net/secrets/my-secret/xxxx"
    read_only: false
    state: present

- name: Delete a key
  azure.azcollection.azure_rm_appconfigurationkey:
    endpoint: https://myappconf.azconfig.io
    key: "Legacy:Flag"
    label: "prod"
    state: absent
'''

RETURN = '''
id:
    description:
        - Identifier of the configuration setting (data-plane URL form).
    returned: always
    type: str
    example: https://myappconf.azconfig.io/kv/Payments:TimeoutSeconds?label=prod
'''  # NOQA

import json
import traceback
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.appconfiguration import AzureAppConfigurationClient, ConfigurationSetting
except ImportError:
    # Handled in azure_rm_common_ext
    pass


VAULT_CT = "application/vnd.microsoft.appconfig.keyvaultref+json;charset=utf-8"


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMAppConfigurationKey(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            endpoint=dict(type='str', required=True),
            key=dict(
                type='str',
                required=True,
                no_log=False
            ),
            label=dict(type='str'),
            type=dict(
                type='str',
                choices=['kv', 'vault'],
                default='kv'
            ),
            value=dict(
                type='str',
                no_log=True
            ),
            content_type=dict(type='str'),
            vault_key_reference=dict(type='str', no_log=True),
            read_only=dict(type='bool'),

            state=dict(
                type='str',
                default='present',
                choices=['absent', 'present']
            )
        )

        self.endpoint = None
        self.key = None
        self.label = None
        self.type = None
        self.value = None
        self.content_type = None
        self.vault_key_reference = None
        self.read_only = None

        self.dataplane_client = None
        self.mgmt_client = None
        self.state = None
        self.parameters = dict()
        self.results = dict(changed=False)
        self.to_do = Actions.NoAction

        super(AzureRMAppConfigurationKey, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                         supports_tags=False,
                                                         supports_check_mode=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if key in kwargs:
                setattr(self, key, kwargs[key])
            if key in kwargs and kwargs.get(key) is not None:
                if key == 'type':
                    self.parameters['type'] = kwargs[key]
                elif key == 'content_type':
                    self.parameters['content_type'] = kwargs[key]
                elif key == 'value':
                    self.parameters['value'] = kwargs[key]
                elif key == 'vault_key_reference':
                    self.parameters['vault_key_reference'] = kwargs[key]
                elif key == 'read_only':
                    self.parameters['read_only'] = bool(kwargs[key])

        # Resolve endpoint if needed (from ARM ID)
        self.mgmt_client = None

        # Build data-plane client
        self.dataplane_client = AzureAppConfigurationClient(self.endpoint,
                                                            credential=self.azure_auth.azure_credential_track2)

        # Read current
        old_response = self.get_setting()
        response = None

        # Validation: kv vs value
        if self.state == 'present' and old_response is None:
            # default type if not provided
            if self.type == 'kv' and self.value is None:
                self.fail("Parameter 'value' is required when creating a type='kv' setting.")
            if self.type == 'vault' and not self.vault_key_reference:
                self.fail("Parameter 'vault_key_reference' is required when creating a type='vault' setting.")

        # Decide action
        if not old_response:
            if self.state == 'absent':
                self.log("Settings did not exist")
                self.to_do = Actions.NoAction
            else:
                self.to_do = Actions.Create
        else:
            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                self.to_do = self._needs_update(old_response, self.parameters)

        # unlock-first, upsert/delete, lock-finally
        if self.to_do in (Actions.Create, Actions.Update):
            # If the existing setting is locked, unlock BEFORE upsert.
            original_ro = bool(old_response.get('read_only')) if old_response else False
            if old_response and original_ro and not self.check_mode:
                self.ensure_lock_state(False)

            # Perform the upsert
            self.results['changed'] = True
            if not self.check_mode:
                response = self.upsert_setting()

            # Decide final lock state:
            # If caller explicitly set read_only, honor it.
            # Otherwise, restore the original lock (for updates).
            final_ro = bool(self.read_only) if self.read_only is not None else original_ro
            if not self.check_mode:
                self.ensure_lock_state(final_ro)

            if response is None:
                response = self.get_setting()

        elif self.to_do == Actions.Delete:
            # If the existing setting is locked, unlock BEFORE delete.
            original_ro = bool(old_response.get('read_only')) if old_response else False
            if old_response and original_ro and not self.check_mode:
                self.ensure_lock_state(False)

            self.results['changed'] = True
            if not self.check_mode:
                self.delete_setting()
            self.results['id'] = self._compose_id(self.endpoint, self.key, self.label)
            return self.results

        else:
            # No data changes; converge lock ONLY if the user explicitly asked.
            self.log("No action needed on the setting.")
            self.results['changed'] = False
            response = old_response

            if response and self.read_only is not None:
                current_ro = bool(response.get('read_only'))
                desired_ro = bool(self.read_only)
                if current_ro != desired_ro:
                    self.results['changed'] = True
                    if not self.check_mode:
                        self.ensure_lock_state(desired_ro)
                    response = self.get_setting()

        if response:
            self.results['id'] = self._compose_id(self.endpoint, self.key, self.label)

        return self.results

    def get_setting(self):
        '''
        Retrieve the current configuration setting from the data plane.

        :return: The configuration setting as a dictionary, or False if not found.
        '''
        try:
            response = self.dataplane_client.get_configuration_setting(
                key=self.key,
                label=self.label
            )
            return response.as_dict()
        except ResourceNotFoundError:
            return False
        except Exception as e:
            # Catch SDK bug: empty response causes JSONDecodeError
            self.fail("Failed to retrieve setting '{}': {}\n{}".format(self.key, str(e), traceback.format_exc()))

    def upsert_setting(self):
        '''
        Upsert (create or update) the configuration setting in the data plane.

        :return: The updated configuration setting as a dictionary.
        '''
        try:
            if self.type == 'kv':
                if self.value is not None:
                    desired_value = self.value
                else:
                    cur = self.get_setting() or {}
                    desired_value = cur.get('value', '')

                cs = ConfigurationSetting(key=self.key,
                                          label=self.label,
                                          value=desired_value,
                                          content_type=self.content_type)

                response = self.dataplane_client.set_configuration_setting(configuration_setting=cs)
            else:
                # vault
                payload = json.dumps({"uri": self.vault_key_reference})

                cs = ConfigurationSetting(key=self.key,
                                          label=self.label,
                                          value=payload,
                                          content_type=VAULT_CT)  # official KV-ref MIME

                response = self.dataplane_client.set_configuration_setting(configuration_setting=cs)
            return response.as_dict()
        except Exception as exc:
            self.fail("Error creating/updating the Configuration Setting '{}': {}".format(self.key, str(exc)))

    def delete_setting(self):
        '''
        Delete the configuration setting from the data plane.

        :return: The deleted configuration setting as a dictionary.
        '''
        try:
            response = self.dataplane_client.delete_configuration_setting(key=self.key,
                                                                          label=self.label)
            return response.as_dict()
        except Exception as exc:
            self.fail("Error deleting the Configuration Setting '{}': {}".format(self.key, str(exc)))

    def ensure_lock_state(self, read_only):
        '''
        Converge the read-only (lock) state of the setting.

        :return: The updated configuration setting as a dictionary.
        '''
        try:
            cs = ConfigurationSetting(key=self.key, label=self.label)
            response = self.dataplane_client.set_read_only(configuration_setting=cs,
                                                           read_only=bool(read_only))
            return response.as_dict()
        except Exception as exc:
            self.fail("Error setting read_only={} on Configuration Setting '{}': {}".format(read_only, self.key, str(exc)))

    def _needs_update(self, old, new_params):
        '''
        Determine whether an update is required by comparing fields, honoring user intent.

        :return: Actions.Update or Actions.NoAction
        '''
        to_do = Actions.NoAction
        # type
        if (old.get('type') or 'kv') != (new_params.get('type') or 'kv'):
            to_do = Actions.Update

        if (new_params.get('type') or 'kv') == 'kv':
            if self.value is not None and old.get('value') != self.value:
                to_do = Actions.Update
            if self.content_type is not None and (self.content_type or None) != (old.get('content_type') or None):
                to_do = Actions.Update
        else:
            if self.vault_key_reference is not None and old.get('vault_key_reference') != self.vault_key_reference:
                to_do = Actions.Update

        return to_do

    @staticmethod
    def _compose_id(endpoint, key, label):
        '''
        Compose a deterministic data-plane identifier for the setting.
        - With label: "<endpoint>/kv/<key>?label=<label>"
        - Without label: "<endpoint>/kv/<key>"

        :return: The composed identifier string.
        '''
        base = endpoint.rstrip('/')
        if label:
            return f"{base}/kv/{key}?label={label}"
        return f"{base}/kv/{key}"


def main():
    """Main execution"""
    AzureRMAppConfigurationKey()


if __name__ == '__main__':
    main()
