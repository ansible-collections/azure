#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_appconfiguration_info
version_added: "3.15.0"
short_description: Get Azure App Configuration store facts
description:
    - Get facts for Azure App Configuration stores (Microsoft.AppConfiguration/configurationStores).
    - Supports get by name, list by resource group and list by subscription.
    - Optionally includes store replicas when fetching by name.

options:
    resource_group:
        description:
            - The name of the resource group to which the App Configuration store belongs.
        type: str
    appconfig_name:
        description:
            - The name of the App Configuration store.
        type: str
    include_replicas:
        description:
            - When C(appconfig_name) is specified, indicates whether to include the store replicas in the response.
            - Disabled for list operations to avoid extra calls by default.
        type: bool
        default: false
    tags:
        description:
            - Limit results by a list of tags. Format tags as C(key) or C(key:value).
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Get App Configuration store
  azure_rm_appconfiguration_info:
    resource_group: myRG
    appconfig_name: myAGS

- name: Get App Configuration store with replicas
  azure_rm_appconfiguration_info:
    resource_group: myRG
    appconfig_name: myAGS
    include_replicas: true

- name: List stores in RG
  azure_rm_appconfiguration_info:
    resource_group: myRG

- name: List stores in subscription
  azure_rm_appconfiguration_info:
'''

RETURN = '''
appconfigurations:
    description: List of App Configuration stores.
    returned: always
    type: list
    contains:
        appconfig_name:
            description:
                - Name of the App Configuration store.
            returned: always
            type: str
            sample: myAGS
        id:
            description:
                - Resource ID of the App Configuration store.
            returned: always
            type: str
            sample: /subscriptions/xxxx/resourceGroups/myRG/providers/Microsoft.AppConfiguration/configurationStores/myAGS
        location:
            description:
                - Azure location of the App Configuration store.
            returned: always
            type: str
            sample: eastus
        tags:
            description:
                - List of tags.
            type: dict
            sample: "{'env': 'prod', 'department': 'finance'}"
        sku:
            description:
                - SKU of the App Configuration store.
            returned: always
            type: dict
            contains:
                name:
                    description: SKU name.
                    type: str
                    returned: always
                    sample: Standard
        public_network_access:
            description:
                - Whether public network access is enabled.
            returned: always
            type: str
            sample: Enabled
        disable_local_auth:
            description:
                - Whether local authentication is disabled.
            returned: always
            type: bool
            sample: false
        replicas:
            description:
                - List of replicas for the App Configuration store.
            returned: when include_replicas is true and appconfig_name is specified
            type: list
            elements: dict
            contains:
                name:
                    description:
                        - Name of the replica.
                    returned: always
                    type: str
                    sample: myAGSrep
                location:
                    description:
                        - Azure location of the replica.
                    returned: always
                    type: str
                    sample: westus
                id:
                    description:
                        - Resource ID of the replica.
                    returned: always
                    type: str
                    sample: /subscriptions/xxxx/resourceGroups/myrg/providers/Microsoft.AppConfiguration/configurationStores/myAGS/replicas/myAGSrep
        soft_delete_retention_in_days:
            description:
                - Number of days to retain soft-deleted items.
            returned: always
            type: int
            sample: 7
        enable_purge_protection:
            description:
                - Whether purge protection is enabled.
            returned: always
            type: bool
            sample: true
        identity:
            description:
                - Managed identity information.
            returned: always
            type: dict
            contains:
                type:
                    description: Type of managed identity.
                    type: str
                    returned: always
                    sample: SystemAssigned
                principal_id:
                    description: Principal ID of the managed identity.
                    type: str
                    returned: always
                    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                tenant_id:
                    description: Tenant ID of the managed identity.
                    type: str
                    returned: always
                    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
'''


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.mgmt.appconfiguration import AppConfigurationManagementClient
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


def appconfig_to_dict(appconfig, replicas=None, include_replicas=False):
    s = appconfig.as_dict()

    data = dict(
        id=s.get("id"),
        appconfig_name=s.get("name"),
        location=s.get("location"),
        tags=s.get("tags"),
        sku=dict(name=s.get("sku", {}).get("name")),

        endpoint=s.get("endpoint"),
        public_network_access=s.get("public_network_access"),
        disable_local_auth=s.get("disable_local_auth"),
        enable_purge_protection=s.get("enable_purge_protection"),
        soft_delete_retention_in_days=s.get("soft_delete_retention_in_days"),
        identity=s.get("identity")
    )

    # Only include replicas when explicitly requested
    if include_replicas:
        data["replicas"] = replicas or []

    return data


class AzureRMAppConfigurationInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            appconfig_name=dict(type='str'),
            include_replicas=dict(type='bool', default=False),
            tags=dict(type='list', elements='str'),
        )

        self.resource_group = None
        self.appconfig_name = None
        self.include_replicas = None
        self.tags = None
        self.results = dict(changed=False)
        self._client = None

        super(AzureRMAppConfigurationInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=False,
                                                          facts_module=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        self._client = self.get_mgmt_svc_client(AppConfigurationManagementClient,
                                                base_url=self._cloud_environment.endpoints.resource_manager)

        if self.appconfig_name:
            if not self.resource_group:
                self.fail("Parameter 'resource_group' is required when filtering by appconfig_name.")
            self.results['appconfigurations'] = [self.get_by_appconfig_name()]

        elif self.resource_group:
            self.results['appconfigurations'] = self.list_appconfig_by_resource_group()

        else:
            self.results["appconfigurations"] = self.list_appconfig_by_subscription()

        return self.results

    def get_by_appconfig_name(self):
        '''
        Get the properties of this specified app configuration store.

        :return: deserialized app configuration store state dictionary.
        '''
        try:
            s = self._client.configuration_stores.get(resource_group_name=self.resource_group,
                                                      config_store_name=self.appconfig_name)
            replicas = self.list_appconfig_replicas(self.resource_group, self.appconfig_name) if self.include_replicas else []
            if self.has_tags(s.tags, self.tags):
                return appconfig_to_dict(s, replicas, self.include_replicas)
        except ResourceNotFoundError as e:
            self.log("Did not find the app configurations {0}: {1}".format(self.appconfig_name, str(e)))

    def list_appconfig_by_resource_group(self):
        '''
        List the properties of app configuration store in specific resource group.

        :return: deserialized app configuration store state dictionary.
        '''
        results = []
        try:
            stores = list(self._client.configuration_stores.list_by_resource_group(resource_group_name=self.resource_group))

            if stores:
                for s in stores:
                    if not self.has_tags(s.tags, self.tags):
                        continue

                    replicas = self.list_appconfig_replicas(self.resource_group, s.name) if self.include_replicas else []
                    results.append(appconfig_to_dict(s, replicas, self.include_replicas))
        except Exception as e:
            self.log("Did not find appconfig in resource group {0} : {1}.".format(self.resource_group, str(e)))

        return results

    def list_appconfig_by_subscription(self):
        '''
        List the properties of app configuration stores in specific subscription.

        :return: deserialized app configuration stores state dictionary.
        '''
        results = []
        try:
            stores = list(self._client.configuration_stores.list())

            for s in stores:
                if not self.has_tags(s.tags, self.tags):
                    continue

                # parse ID to retrieve RG + name
                parts = s.id.split("/")
                rg = parts[4]
                name = parts[8]

                replicas = self.list_appconfig_replicas(rg, name) if self.include_replicas else []

                store_obj = self._client.configuration_stores.get(rg, name)
                results.append(appconfig_to_dict(store_obj, replicas, self.include_replicas))
        except Exception as e:
            self.log("Did not find appconfig in current subscription {0}.", format(str(e)))
        return results

    def list_appconfig_replicas(self, rg, name):
        '''
        List replicas of the specific app configuration stores

        :return: name, id and location of the replicas
        '''
        rlist = []
        pager = self._client.replicas.list_by_configuration_store(resource_group_name=rg,
                                                                  config_store_name=name)
        for r in pager:
            rlist.append(dict(id=r.id,
                              name=r.name,
                              location=r.location))
        return rlist


def main():
    """Main execution"""
    AzureRMAppConfigurationInfo()


if __name__ == '__main__':
    main()
