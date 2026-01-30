#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_appconfiguration
version_added: "3.15.0"
short_description: Manage Azure App Configuration stores.
description:
    - Create, update and delete Azure App Configuration stores.

options:
    resource_group:
        description:
            - The name of the Resource Group to which the App Configuration store belongs.
        required: True
        type: str
    appconfig_name:
        description:
            - Name of the app configuration store.
        required: True
        type: str
    identity:
        description:
            - Managed identity configuration for the store.
        type: dict
        suboptions:
            type:
                description:
                    - Type of the managed identity
                required: true
                choices:
                    - SystemAssigned
                    - UserAssigned
                    - SystemAssigned, UserAssigned
                type: str
            user_assigned_identity_ids:
                description:
                    - List of user-assigned identity resource IDs (required when type includes UserAssigned).
                required: false
                type: list
                elements: str
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
        type: str
    sku:
        description:
            - SKU tier of the store.
        type: str
        choices:
            - 'free'
            - 'developer'
            - 'standard'
            - 'premium'
    enable_purge_protection:
        description:
            - Property specifying whether protection against purge is enabled for this store.
        type: bool
        default: False
    soft_delete_retention_in_days:
        description:
            - Property specifying the number of days to retain deleted store.
        type: int
    public_network_access:
        description:
            - Public network access setting for the store.
            - If omitted at creation, Azure treats it as C(Automatic). Once set to C(Enabled) or C(Disabled), it cannot be returned to C(Automatic);
              omit the property in updates to leave unchanged.
        type: str
        choices:
            - Disabled
            - Enabled
    disable_local_auth:
        description:
            - Property specifying whether local authentication (access keys) is enabled for the store.
        type: bool
        default: False
    replicas:
        description:
            - List of replicas to manage for this store.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Name of the replica.
                required: true
                type: str
            location:
                description:
                    - Location of the replica.
                required: true
                type: str
    is_purge_deleted:
        description:
            - Whether permanently deletes the specified store. aka Purges the deleted Azure App Configuration store
            - When I(is_purge_deleted) is specified, the I(location) has to be configured.
            - If not configured, the default location of the resource group will be used.
        type: bool
        default: False
    state:
        description:
            - Assert the state of the App Configuration store. Use C(present) to create or update an App Configuration store and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Zun Yang (@zunyangc)

'''

EXAMPLES = '''
- name: Create a Standard App Configuration store with system-assigned identity
  azure.azcollection.azure_rm_appconfiguration:
    resource_group: myResourceGroup
    appconfig_name: myAppConfigStore
    location: eastus
    sku: standard
    identity:
      type: SystemAssigned
    enable_local_auth: true
    tags:
      env: prod
    state: present

- name: Assign a user-assigned identity and enable purge protection
  azure.azcollection.azure_rm_appconfiguration:
    resource_group: myResourceGroup
    appconfig_name: myAppConfigStore
    identity:
      type: UserAssigned
      user_assigned_identity_ids:
        - /subscriptions/xxxx/resourceGroups/myResourceGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myIdentity
    enable_purge_protection: true
    soft_delete_retention_in_days: 7
    state: present

- name: Delete an App Configuration store
  azure.azcollection.azure_rm_appconfiguration:
    resource_group: myRG
    appconfig_name: my-appconf-legacy
    state: absent

- name: Purge a soft-deleted App Configuration store (subscription-level permission required)
  azure.azcollection.azure_rm_appconfiguration:
    resource_group: myRG
    appconfig_name: my-appconf-legacy
    location: eastus
    is_purge_deleted: true
    state: absent

- name: Create store with two replicas
  azure.azcollection.azure_rm_appconfiguration:
    resource_group: myRG
    appconfig_name: myappconf
    location: eastus
    sku: standard
    replicas:
      - name: r1
        location: westus
      - name: r2
        location: northeurope
    state: present
'''

RETURN = '''
id:
    description:
        - The Azure Resource Manager resource ID for the App Configuration store.
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myRG/providers/Microsoft.AppConfiguration/configurationStores/myAppConfigStore
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.polling import LROPoller
    from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
    from azure.mgmt.appconfiguration import AppConfigurationManagementClient
except ImportError:
    # Handled in azure_rm_common_ext
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMAppConfiguration(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            appconfig_name=dict(
                type='str',
                required=True
            ),
            identity=dict(
                type='dict',
                options=dict(
                    type=dict(
                        type='str',
                        required=True,
                        choices=['SystemAssigned', 'UserAssigned', 'SystemAssigned, UserAssigned']
                    ),
                    user_assigned_identity_ids=dict(
                        type='list',
                        elements='str'
                    )
                )
            ),
            location=dict(type='str'),
            sku=dict(
                type='str',
                choices=['free', 'developer', 'standard', 'premium']
            ),
            enable_purge_protection=dict(
                type='bool',
                default=False
            ),
            soft_delete_retention_in_days=dict(
                type='int'
            ),
            public_network_access=dict(
                type='str',
                choices=['Disabled', 'Enabled']
            ),
            disable_local_auth=dict(
                type='bool',
                default=False
            ),
            replicas=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(type='str', required=True),
                    location=dict(type='str', required=True)
                )
            ),
            # Administrative op: purge soft-deleted store
            is_purge_deleted=dict(type='bool', default=False),

            # Azure tags (provided by AzureRMModuleBaseExt)
            # 'tags' is injected by base class when supports_tags=True

            state=dict(
                type='str',
                default='present',
                choices=['absent', 'present']
            )
        )

        self.resource_group = None
        self.appconfig_name = None
        self.identity = None
        self.is_purge_deleted = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction
        self.parameters = dict()
        self.tags = None

        super(AzureRMAppConfiguration, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_tags=True,
                                                      supports_check_mode=True)

    @property
    def managed_identity(self):
        return {}

    def exec_module(self, **kwargs):
        """Main module execution method"""

        # Bind known attributes and build parameters payload
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if key in kwargs:
                setattr(self, key, kwargs[key])
            if key in kwargs and kwargs.get(key) is not None:
                if key == 'location':
                    self.parameters['location'] = kwargs[key]
                elif key == 'sku':
                    # ARM expects {"sku": {"name": "<tier>"}}
                    self.parameters.setdefault('sku', {})['name'] = kwargs[key]
                elif key == "public_network_access":
                    self.parameters.setdefault("properties", {})["publicNetworkAccess"] = kwargs[key]
                elif key == "disable_local_auth":
                    self.parameters.setdefault("properties", {})["disableLocalAuth"] = kwargs[key]
                elif key == "enable_purge_protection":
                    self.parameters.setdefault("properties", {})["enablePurgeProtection"] = kwargs[key]
                elif key == "soft_delete_retention_in_days":
                    self.parameters.setdefault("properties", {})["softDeleteRetentionInDays"] = kwargs[key]

        self.mgmt_client = self.get_mgmt_svc_client(AppConfigurationManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        # Resolve RG + default location
        resource_group = self.get_resource_group(self.resource_group)
        if "location" not in self.parameters:
            self.parameters['location'] = resource_group.location

        # Validation: SKU vs purge fields
        if self.sku not in ('standard', 'premium'):
            if self.enable_purge_protection:
                self.fail("enable_purge_protection is only supported on 'standard' or 'premium' SKUs.")
            if self.soft_delete_retention_in_days is not None:
                self.fail("soft_delete_retention_in_days is only supported on 'standard' or 'premium' SKUs.")

        # Normalize identity changes using base helper
        identity_dict = None
        if self.identity:
            id_type = (self.identity.get("type") or "").strip()
            ids = self.identity.get("user_assigned_identity_ids") or []
            if "UserAssigned" in id_type and not ids:
                self.fail("identity.user_assigned_identity_ids must be provided when identity.type includes 'UserAssigned'.")
            if id_type == "SystemAssigned":
                identity_dict = {"type": "SystemAssigned"}
            elif id_type == "UserAssigned":
                identity_dict = {"type": "UserAssigned",
                                 "userAssignedIdentities": {uid: {} for uid in ids}}
            elif id_type == "SystemAssigned, UserAssigned":
                identity_dict = {"type": "SystemAssigned, UserAssigned",
                                 "userAssignedIdentities": {uid: {} for uid in ids}}
            else:
                # If not provided or unrecognized, omit identity block altogether
                identity_dict = None

            if identity_dict:
                self.parameters["identity"] = identity_dict

        # Read current
        old_response = self.get_instance()
        response = None

        # Compute identity_changed
        identity_changed = False
        if old_response and identity_dict:
            old_ident = old_response.get('identity') or {}
            old_type = (old_ident.get('type') or '').lower()
            new_type = (identity_dict.get('type') or '').lower()
            if old_type != new_type:
                identity_changed = True
            else:
                # Compare UAMI sets if applicable
                if 'userassigned' in new_type:
                    old_ids = set(((old_ident.get('user_assigned_identities') or {}).keys()) or [])
                    new_ids = set(((identity_dict.get('userAssignedIdentities') or {}).keys()) or [])
                    if old_ids != new_ids:
                        identity_changed = True

        # Decide action
        if not old_response:
            if self.state == 'absent':
                self.log("Old instance didn't exist")
                self.to_do = Actions.NoAction
            else:
                self.to_do = Actions.Create
        else:
            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                # compute update deltas
                self.to_do = self._needs_update(old_response, self.parameters, identity_changed)

        # Execute
        if self.to_do in (Actions.Create, Actions.Update):
            self.results['changed'] = True
            if not self.check_mode:
                self.parameters["tags"] = self.tags
                response = self.create_or_update_store()
                if self.replicas is not None:
                    self.reconcile_replicas(self.replicas)
                if response is None:
                    response = self.get_instance()
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            if not self.check_mode:
                self.delete_store()
        elif self.to_do == Actions.NoAction and self.replicas is not None:
            self.reconcile_replicas(self.replicas)
            if response is None:
                response = old_response or self.get_instance()
        else:
            # NoAction
            self.results['changed'] = False
            response = old_response

        # Purge soft-deleted if requested
        if self.is_purge_deleted:
            purge_response = self.get_deleted(self.parameters["location"])
            if purge_response:
                self.results['changed'] = True
                if not self.check_mode:
                    self.purge_deleted(self.parameters["location"])

        if response is not None and hasattr(response, "as_dict"):
            response = response.as_dict()

        if response:
            self.results["id"] = response["id"]

        return self.results

    def get_instance(self):
        '''
        Get the properties of the specified App Configuration store.

        :return: deserialized App Configuration store instance state dictionary.
        '''
        try:
            response = self.mgmt_client.configuration_stores.get(resource_group_name=self.resource_group,
                                                                 config_store_name=self.appconfig_name)
            return response.as_dict()
        except ResourceNotFoundError:
            return False

    def create_or_update_store(self):
        '''
        Create or update (PUT) App Configuration store with the specified configuration.

        :return: deserialized App Configuration store state dictionary.
        '''
        try:
            poller = self.mgmt_client.configuration_stores.begin_create(resource_group_name=self.resource_group,
                                                                        config_store_name=self.appconfig_name,
                                                                        config_store_creation_parameters=self.parameters)
            if isinstance(poller, LROPoller):
                return self.get_poller_result(poller)
            return poller.as_dict() if hasattr(poller, "as_dict") else poller
        except Exception as exc:
            self.fail("Error creating/updating App Configuration store '{}': {}".format(self.appconfig_name, str(exc)))

    def delete_store(self):
        '''
        Delete the specified App Configuration store.

        :return: True.
        '''
        try:
            poller = self.mgmt_client.configuration_stores.begin_delete(resource_group_name=self.resource_group,
                                                                        config_store_name=self.appconfig_name)
            if isinstance(poller, LROPoller):
                return self.get_poller_result(poller)
            return True
        except Exception as exc:
            self.fail("Error deleting the App Configuration store '{}': {}".format(self.appconfig_name, str(exc)))

    def get_deleted(self, location):
        '''
        Get deleted store
        :return: True or False
        '''
        try:
            self.mgmt_client.configuration_stores.get_deleted(self.appconfig_name, location)
        except Exception as e:
            self.log('Error attempting to get the deleted store: {0}'.format(str(e)))
            return False
        return True

    def purge_deleted(self, location):
        '''
        Purge the specified soft-deleted App Configuration store.
        '''
        try:
            poller = self.mgmt_client.configuration_stores.begin_purge_deleted(location=location,
                                                                               config_store_name=self.appconfig_name)
            if isinstance(poller, LROPoller):
                return self.get_poller_result(poller)
            return True
        except HttpResponseError as e:
            # 404/NotFound => nothing to purge
            status = getattr(e, 'status_code', None) or getattr(getattr(e, 'response', None), 'status_code', None)
            if status == 404:
                return False
            self.fail("Error purging deleted App Configuration store '{0}' in '{1}': {2}".format(
                self.appconfig_name, location, str(e)))
        except Exception as exc:
            self.fail("Error purging deleted App Configuration store '{0}' in '{1}': {2}".format(
                self.appconfig_name, location, str(exc)))

    def _list_replicas(self):
        '''
        List replicas for the specified App Configuration store.

        :return: Dictionary of replicas.
        '''
        found = {}
        pager = self.mgmt_client.replicas.list_by_configuration_store(
            resource_group_name=self.resource_group,
            config_store_name=self.appconfig_name
        )
        for r in pager:
            rd = r.as_dict()
            found[rd['name']] = {'location': rd.get('location'), 'id': rd.get('id')}
        return found

    def _create_replica(self, name, location):
        '''
        Create a replica for the specified App Configuration store.

        :return: deserialized replica instance state dictionary.
        '''
        poller = self.mgmt_client.replicas.begin_create(
            resource_group_name=self.resource_group,
            config_store_name=self.appconfig_name,
            replica_name=name,
            replica_creation_parameters={'location': location, 'properties': {}}
        )
        return self.get_poller_result(poller)

    def _delete_replica(self, name):
        '''
        Delete a replica for the specified App Configuration store.

        :return: True.
        '''
        poller = self.mgmt_client.replicas.begin_delete(
            resource_group_name=self.resource_group,
            config_store_name=self.appconfig_name,
            replica_name=name
        )
        return self.get_poller_result(poller)

    def reconcile_replicas(self, desired):
        '''
        Reconcile replicas to match desired state.
        Authoritative: create missing, delete extras, recreate on location change.
        '''
        # desired: list[{'name': ..., 'location': ...}]
        # authoritative behavior: create missing, delete extras, (re)create on location change
        desired_index = {x['name']: x['location'] for x in (desired or [])}
        current = self._list_replicas()

        # create or recreate when location changed
        for name, loc in desired_index.items():
            if name not in current:
                self.results['changed'] = True
                if not self.check_mode:
                    self._create_replica(name, loc)
            else:
                if loc and (loc.lower() != (current[name].get('location') or '').lower()):
                    self.results['changed'] = True
                    if not self.check_mode:
                        self._delete_replica(name)
                        self._create_replica(name, loc)

        # delete extras (authoritative)
        extra = set(current.keys()) - set(desired_index.keys())
        for name in sorted(extra):
            self.results['changed'] = True
            if not self.check_mode:
                self._delete_replica(name)

    def _needs_update(self, old, new_params, identity_changed):
        '''
        Determine whether an update is required by comparing fields.
        Explicitly manage. Keep parity with Azure defaults where possible.

        :return: Action Required.
        '''
        to_do = Actions.NoAction
        props_new = new_params.get('properties') or {}

        # sku
        sku_old = ((old.get('sku') or {}).get('name') or '').lower()
        sku_new = ((new_params.get('sku') or {}).get('name') or '').lower()
        if sku_new and sku_new != sku_old:
            # Note: provider/API might restrict downgrades; PUT will handle errors.
            to_do = Actions.Update

        # publicNetworkAccess
        if 'publicNetworkAccess' in props_new:
            if (props_new.get('publicNetworkAccess') or '').lower() != (old.get('public_network_access') or '').lower():
                to_do = Actions.Update

        # disableLocalAuth
        if 'disableLocalAuth' in props_new:
            if bool(props_new.get('disableLocalAuth')) != bool(old.get('disable_local_auth')):
                to_do = Actions.Update

        # enablePurgeProtection
        if 'enablePurgeProtection' in props_new:
            if bool(props_new.get('enablePurgeProtection')) != bool(old.get('enable_purge_protection')):
                to_do = Actions.Update

        # softDeleteRetentionInDays
        if 'softDeleteRetentionInDays' in props_new:
            if props_new.get('softDeleteRetentionInDays') != old.get('soft_delete_retention_in_days'):
                to_do = Actions.Update

        # tags
        update_tags, newtags = self.update_tags(old.get('tags', {}) or {})
        if update_tags:
            self.tags = newtags
            to_do = Actions.Update

        # identity
        if identity_changed:
            to_do = Actions.Update

        # Write back potentially adjusted props
        if props_new:
            new_params['properties'] = props_new

        return to_do


def main():
    """Main execution"""
    AzureRMAppConfiguration()


if __name__ == '__main__':
    main()
