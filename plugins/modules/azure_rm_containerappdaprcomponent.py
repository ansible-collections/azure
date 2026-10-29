#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_containerappdaprcomponent
version_added: "4.2.0"
short_description: Manage a Dapr component in an Azure Container Apps managed environment
description:
    - Create, update and delete a Dapr component in an Azure Container Apps
      managed environment.
    - Dapr components (state stores, pub/sub brokers, secret stores, input and
      output bindings) are shared by the container apps in the environment that
      reference the component in their C(dapr) configuration or in the
      component's I(scopes).
    - The managed environment itself is managed with
      M(azure.azcollection.azure_rm_containerappenvironment).
options:
    resource_group:
        description:
            - Name of the resource group containing the managed environment.
        required: true
        type: str
    environment_name:
        description:
            - Name of the managed environment that hosts the Dapr component.
        required: true
        type: str
    name:
        description:
            - Name of the Dapr component.
        required: true
        type: str
    component_type:
        description:
            - Dapr component type, for example C(state.azure.blobstorage),
              C(pubsub.redis), C(secretstores.azure.keyvault) or
              C(bindings.kafka).
            - Required when creating the component.
        type: str
    version:
        description:
            - Version of the Dapr component, for example C(v1).
            - Required when creating the component.
        type: str
    ignore_errors:
        description:
            - Ignore Dapr component errors when the component fails to start.
        type: bool
    init_timeout:
        description:
            - Dapr component initialization timeout, in the
              C(<h>h<m>m<s>s) format, for example C(30s) or C(1m30s).
        type: str
    secrets:
        description:
            - Collection of secrets used by the Dapr component. Secret values
              are referenced from I(metadata) entries by secret name.
            - Each entry is an inline C(name)/I(value) pair. Azure Key Vault
              references are not supported for Dapr component secrets (the
              service rejects I(keyVaultUrl) with DaprComponentSecretNull);
              to consume Key Vault secrets, deploy a
              C(secretstores.azure.keyvault) Dapr component instead.
            - Inline secret values are write-only and never returned by Azure,
              so an update of a component that has secrets must resupply them
              when the update changes anything - the module fails instead of
              silently dropping them.
            - Pass an empty list to remove all secrets.
        type: list
        elements: dict
        suboptions:
            name:
                description: Secret name.
                type: str
                required: true
            value:
                description: Secret value.
                type: str
    metadata:
        description:
            - Dapr component configuration metadata.
            - Each entry is either a plain C(name)/I(value) pair or a
              C(name)/I(secret_ref) pair referencing an entry in I(secrets).
        type: list
        elements: dict
        suboptions:
            name:
                description: Metadata property name.
                type: str
                required: true
            value:
                description: Metadata property value.
                type: str
            secret_ref:
                description: Name of the secret in I(secrets) to pull the value from.
                type: str
    scopes:
        description:
            - Names of the container apps that can use this Dapr component.
            - When omitted, all container apps in the environment can use it.
        type: list
        elements: str
    secret_store_component:
        description:
            - Name of a Dapr secret store component to retrieve component
              secrets from.
        type: str
    state:
        description:
            - Assert the state of the Dapr component. Use C(present) to
              create or update, C(absent) to delete.
        type: str
        default: present
        choices:
            - present
            - absent
    update_secrets:
        description:
            - When I(secrets) is sent to Azure for an existing component.
            - Inline secret values are write-only and cannot be compared
              against the stored values, so a run that only changes a secret
              value is not detected as a change.
            - With C(on_create) (the default), I(secrets) is included when the
              component is created and when an update is triggered by other
              changes, but a run that only supplies I(secrets) does not update
              the component.
            - With C(always), supplying I(secrets) always triggers an update,
              which rotates the secret values of the existing component.
        type: str
        default: on_create
        choices:
            - on_create
            - always
notes:
    - On update, fields that are omitted are carried forward from the existing
      component. Secret values are write-only, so an update of a component
      that has secrets must resupply I(secrets) when the update changes
      anything, and the module fails otherwise. Use I(update_secrets=always)
      to rotate secret values.
    - Azure Key Vault references are not supported for Dapr component secrets
      (the service rejects them with DaprComponentSecretNull). To consume Key
      Vault secrets, deploy a C(secretstores.azure.keyvault) Dapr component
      with the vault name in I(metadata) and give the environment's or apps'
      managed identity access to the vault.
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create a Dapr state store backed by Azure Blob Storage
  azure.azcollection.azure_rm_containerappdaprcomponent:
    resource_group: myResourceGroup
    environment_name: myenvironment
    name: statestore
    component_type: state.azure.blobstorage
    version: v1
    metadata:
      - name: accountName
        value: mystorageaccount
      - name: containerName
        value: dapr-state
      - name: accountKey
        secret_ref: storage-account-key
    secrets:
      - name: storage-account-key
        value: "{{ vault_storage_account_key }}"
    scopes:
      - mycontainerapp

- name: Create a Redis pub/sub component restricted to two apps
  azure.azcollection.azure_rm_containerappdaprcomponent:
    resource_group: myResourceGroup
    environment_name: myenvironment
    name: pubsub
    component_type: pubsub.redis
    version: v1
    init_timeout: 1m
    metadata:
      - name: redisHost
        value: myredis.redis.cache.windows.net:6379
      - name: redisPassword
        secret_ref: redis-password
    secrets:
      - name: redis-password
        value: "{{ vault_redis_password }}"
    scopes:
      - orders-api
      - notifications-worker

- name: Update the scopes of the state store (secrets resupplied)
  azure.azcollection.azure_rm_containerappdaprcomponent:
    resource_group: myResourceGroup
    environment_name: myenvironment
    name: statestore
    scopes:
      - mycontainerapp
      - anotherapp
    secrets:
      - name: storage-account-key
        value: "{{ vault_storage_account_key }}"

- name: Rotate the secret value of the state store
  azure.azcollection.azure_rm_containerappdaprcomponent:
    resource_group: myResourceGroup
    environment_name: myenvironment
    name: statestore
    secrets:
      - name: storage-account-key
        value: "{{ vault_storage_account_key }}"
    update_secrets: always

- name: Delete the pub/sub component
  azure.azcollection.azure_rm_containerappdaprcomponent:
    resource_group: myResourceGroup
    environment_name: myenvironment
    name: pubsub
    state: absent
'''

RETURN = '''
daprcomponent:
    description:
        - The Dapr component definition.
        - Secret values are write-only and are never returned.
    returned: when I(state=present)
    type: dict
    sample: {
        "name": "statestore",
        "component_type": "state.azure.blobstorage",
        "version": "v1",
        "metadata": [{"name": "accountName", "value": "mystorageaccount"}],
        "secrets": [{"name": "storage-account-key"}],
        "scopes": ["mycontainerapp"]
    }
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.appcontainers.models import (
        DaprComponent, DaprComponentProperties, DaprMetadata, Secret,
    )
except ImportError:
    pass

import copy

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

SECRET_SPEC = dict(
    name=dict(type='str', required=True),
    value=dict(type='str', no_log=True),
)

METADATA_SPEC = dict(
    name=dict(type='str', required=True),
    value=dict(type='str'),
    secret_ref=dict(type='str', no_log=False),
)

# Fields Azure accepts on write but fills on its own on read.
READ_ONLY_FIELDS = ('id', 'name', 'system_data', 'provisioning_state', 'deployment_errors')


class AzureRMContainerAppDaprComponent(AzureRMModuleBaseExt):
    """Manage a Dapr component in a Container Apps managed environment."""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            environment_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            component_type=dict(type='str'),
            version=dict(type='str'),
            ignore_errors=dict(type='bool'),
            init_timeout=dict(type='str'),
            secrets=dict(type='list', elements='dict', options=SECRET_SPEC, no_log=False),
            metadata=dict(type='list', elements='dict', options=METADATA_SPEC),
            scopes=dict(type='list', elements='str'),
            secret_store_component=dict(type='str', no_log=False),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            update_secrets=dict(type='str', default='on_create', choices=['on_create', 'always'], no_log=False),
        )

        self.resource_group = None
        self.environment_name = None
        self.name = None
        self.component_type = None
        self.version = None
        self.ignore_errors = None
        self.init_timeout = None
        self.secrets = None
        self.metadata = None
        self.scopes = None
        self.secret_store_component = None
        self.state = None
        self.update_secrets = None

        self.results = dict(changed=False)

        super(AzureRMContainerAppDaprComponent, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        existing = self.get_resource()

        if self.state == 'absent':
            if existing is not None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.delete_resource()
            return self.results

        if existing is None:
            if self.component_type is None or self.version is None:
                self.fail("component_type and version are required to create dapr "
                          "component '{0}' in environment '{1}'".format(self.name, self.environment_name))
            body = self._build_body()
            self.results['changed'] = True
            if not self.check_mode:
                self.results['daprcomponent'] = self.create_update_resource(body)
            else:
                self.results['daprcomponent'] = self._finalize(self.format_body(body))
            return self.results

        # Update: build the full-replace PUT body, carrying forward readable
        # fields the user omitted.
        body = self._merge_existing(existing)
        put_needed = not self._is_current(body, existing)

        # Inline secret values are write-only and cannot be compared, so a
        # run that only supplies secrets is not detected as a change;
        # update_secrets always forces the PUT to rotate the values.
        if not put_needed and self.secrets is not None and self.update_secrets == 'always':
            put_needed = True

        if not put_needed:
            self.results['daprcomponent'] = existing
            return self.results

        # Secret values are write-only and cannot be carried forward; fail
        # when the update would drop them instead of silently removing the
        # secrets.
        if self.secrets is None and existing.get('secrets'):
            dropped = [s.get('name') for s in existing['secrets']]
            self.fail("dapr component '{0}' has inline secret(s) {1} whose values are "
                      "write-only and cannot be carried forward; resupply secrets so "
                      "they are not dropped by the update".format(self.name, dropped))

        self.results['changed'] = True
        if not self.check_mode:
            self.results['daprcomponent'] = self.create_update_resource(body)
        else:
            self.results['daprcomponent'] = self._finalize(self.format_body(body))
        return self.results

    def get_resource(self):
        try:
            response = self.containerapps_client.dapr_components.get(
                resource_group_name=self.resource_group,
                environment_name=self.environment_name,
                component_name=self.name,
            )
        except ResourceNotFoundError:
            return None
        except Exception as exc:
            self.fail("Error retrieving dapr component {0}: {1}".format(self.name, str(exc)))
        return self.format_item(response)

    def create_update_resource(self, body):
        self.log("Creating / updating dapr component {0}".format(self.name))
        try:
            response = self.containerapps_client.dapr_components.create_or_update(
                resource_group_name=self.resource_group,
                environment_name=self.environment_name,
                component_name=self.name,
                dapr_component_envelope=self._build_envelope(body),
            )
        except Exception as exc:
            self.fail("Error creating / updating dapr component {0}: {1}".format(self.name, str(exc)))
        return self.format_item(response)

    def delete_resource(self):
        self.log("Deleting dapr component {0}".format(self.name))
        try:
            self.containerapps_client.dapr_components.delete(
                resource_group_name=self.resource_group,
                environment_name=self.environment_name,
                component_name=self.name,
            )
        except Exception as exc:
            self.fail("Error deleting dapr component {0}: {1}".format(self.name, str(exc)))
        return True

    def _build_body(self):
        """Wire body holding the user-supplied (non C(None)) options."""
        body = dict()
        if self.component_type is not None:
            body['component_type'] = self.component_type
        if self.version is not None:
            body['version'] = self.version
        if self.ignore_errors is not None:
            body['ignore_errors'] = self.ignore_errors
        if self.init_timeout is not None:
            body['init_timeout'] = self.init_timeout
        if self.secrets is not None:
            body['secrets'] = self.secrets
        if self.metadata is not None:
            body['metadata'] = self.metadata
        if self.scopes is not None:
            body['scopes'] = self.scopes
        if self.secret_store_component is not None:
            body['secret_store_component'] = self.secret_store_component
        return body

    def _merge_existing(self, existing):
        """Full-replace PUT body: carry forward readable fields the user omitted.

        Secret values are write-only, so I(secrets) is never carried forward
        into a valid PUT body; the caller fails at PUT time when that would
        drop existing secrets. The carried entries keep the secret names so
        the idempotence comparison still matches.
        """
        body = {k: copy.deepcopy(v) for k, v in existing.items()
                if k not in READ_ONLY_FIELDS and v is not None}
        body.update(self._build_body())
        return body

    def _build_envelope(self, body):
        """Build the SDK model envelope from the snake_case body.

        The secrets use the Secret model with inline name/value pairs; Azure
        rejects Key Vault references for Dapr component secrets
        (DaprComponentSecretNull), so there is nothing else to carry. The
        DaprSecret model is the read-only response type of the listSecrets
        action and must not be used for requests.
        """
        return DaprComponent(
            properties=DaprComponentProperties(
                component_type=body.get('component_type'),
                version=body.get('version'),
                ignore_errors=body.get('ignore_errors'),
                init_timeout=body.get('init_timeout'),
                secret_store_component=body.get('secret_store_component'),
                secrets=[Secret(**{k: v for k, v in s.items() if v is not None})
                         for s in (body.get('secrets') or [])] or None,
                metadata=[DaprMetadata(**{k: v for k, v in m.items() if v is not None})
                          for m in (body.get('metadata') or [])] or None,
                scopes=body.get('scopes'),
            ),
        )

    def _is_current(self, body, existing):
        # Compare the update body against the fetched state, stripping the
        # write-only secret values so they never trigger a false diff.
        compare = copy.deepcopy(body)
        for secret in (compare.get('secrets') or []):
            secret.pop('value', None)
        current = copy.deepcopy(existing)
        # Azure omits empty collections from the GET response, so removing
        # all secrets, metadata or scopes leaves no key behind; treat a
        # missing list as [] so those removals stay idempotent.
        for key in ('secrets', 'metadata', 'scopes'):
            if key in compare and current.get(key) is None:
                current[key] = []
        result = dict(compare=[])
        return self.default_compare({}, compare, current, '', result)

    def format_body(self, body):
        # Check mode: shape the wire body like a fetched resource.
        item = copy.deepcopy(body)
        item['id'] = None
        item['name'] = self.name
        return item

    def format_item(self, item):
        if item is None:
            return None
        return self._finalize(as_attribute_dict(item, exclude_readonly=False))

    def _finalize(self, normalized):
        # Secret values are write-only and never returned by Azure; make sure
        # they never leak into module output either.
        for secret in (normalized.get('secrets') or []):
            secret.pop('value', None)
        normalized['resource_group'] = self.resource_group
        normalized['environment_name'] = self.environment_name
        normalized['name'] = normalized.get('name') or self.name
        return normalized


def main():
    AzureRMContainerAppDaprComponent()


if __name__ == '__main__':
    main()
