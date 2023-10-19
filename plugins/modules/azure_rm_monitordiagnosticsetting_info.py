#!/usr/bin/python
#
# Copyright (c) 2021 Ross Bender (@l3ender)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_monitordiagnosticsetting_info
version_added: "1.10.0"
short_description: Get Azure Monitor diagnostic setting facts.

description:
    - Get facts for Azure Monitor diagnostic settings for any type of resource.

options:
    name:
        description:
            - Limit results to a single diagnostic setting within a resource.
        type: str
    resource:
        description:
            - The resource which will be monitored with the diagnostic setting.
            - It can be a string containing the resource ID.
            - It can be a dictionary containing I(name), I(type), I(resource_group), and optionally I(subscription_id).
            - I(name). The resource name.
            - I(type). The resource type including namespace, such as 'Microsoft.Network/virtualNetworks'.
            - I(resource_group). The resource group containing the resource.
            - I(subscription_id). The subscription ID containing the resource. If none is specified, the credential's subscription ID will be used.
        type: raw
        required: true

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Ross Bender (@l3ender)
'''

EXAMPLES = '''
- name: Get all diagnostic settings for a resource
  azure_rm_monitordiagnosticsetting_info:
    resource: "/subscriptions/my-resource-group/resourceGroups/my-resource-group/providers/Microsoft.Web/sites/my-web-app"

- name: Get all diagnostic settings for a resource using a dictionary
  azure_rm_monitordiagnosticsetting_info:
    resource:
      name: "my-web-app"
      type: "Microsoft.Web/sites"
      resource_group: "my-resource-group"

- name: Get a specific diagnostic setting
  azure_rm_monitordiagnosticsetting_info:
    name: "my-diagnostic-setting"
    resource: "/subscriptions/my-resource-group/resourceGroups/my-resource-group/providers/Microsoft.Network/virtualNetworks/my-vnet"
'''

RETURN = '''
settings:
    description:
        - List of diagnostic settings, sorted by name.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description:
                - ID of the diagnostic setting.
            sample: >-
                /subscriptions/xxx/resourcegroups/my-resource-group/providers/microsoft.network/applicationgateways/my-appgw/
                providers/microsoft.insights/diagnosticSettings/my-diagnostic-setting
            returned: always
            type: str
        name:
            description:
                - Name of the diagnostic setting.
            returned: always
            type: str
            sample: my-diagnostic-setting
        logs:
            description:
                - Enabled log configurations for the diagnostic setting.
            returned: always
            type: list
            elements: dict
            contains:
                category:
                    description:
                        - Name of a Management Group Diagnostic Log category for a resource type this setting is applied to.
                    type: str
                    returned: always
                category_group:
                    description:
                        - Name of a Management Group Diagnostic Log category group for a resource type this setting is applied to.
                    type: str
                    returned: always
                enabled:
                    description:
                        - Whether this log is enabled.
                    type: bool
                    returned: always
                retention_policy:
                    description:
                        - The retention policy for this log.
                    type: dict
                    returned: always
                    contains:
                        enabled:
                            description:
                                - Whether the retention policy is enabled.
                            type: bool
                            returned: always
                        days:
                            description:
                                - The number of days for the retention policy.
                            type: int
                            returned: always
        metrics:
            description:
                - Enabled metric configurations for the diagnostic setting.
            returned: always
            type: list
            elements: dict
            contains:
                category:
                    description:
                        - Name of a Diagnostic Metric category for a resource type this setting is applied to.
                    type: str
                    returned: always
                enabled:
                    description:
                        - Whether the metric category is enabled.
                    type: bool
                    returned: always
                retention_policy:
                    description:
                        - The retention policy for the metric category.
                    type: dict
                    returned: always
                    contains:
                        enabled:
                            description:
                                - Whether the retention policy is enabled.
                            type: bool
                            returned: always
                        days:
                            description:
                                - The number of days for the retention policy.
                            type: int
                            returned: always
        event_hub:
            description:
                - The event hub for the diagnostic setting, if configured.
            returned: always
            type: dict
            contains:
                id:
                    description:
                        - ID of the event hub namespace.
                    returned: always
                    type: str
                    sample: >-
                        /subscriptions/xxx/resourceGroups/my-resource-group/providers/Microsoft.EventHub/namespaces/my-event-hub-namespace
                namespace:
                    description:
                        - Name of the event hub namespace.
                    returned: always
                    type: str
                    sample: my-event-hub-namespace
                hub:
                    description:
                        - Name of the hub within the namespace.
                    returned: always
                    type: str
                    sample: my-event-hub
                policy:
                    description:
                        - Name of the event hub shared access policy.
                    returned: always
                    type: str
                    sample: RootManageSharedAccessKey
        log_analytics:
            description:
                - The log analytics workspace for the diagnostic setting, if configured.
            returned: always
            type: dict
            contains:
                id:
                    description:
                        - ID of the log analytics workspace.
                    returned: always
                    type: str
                    sample: >-
                        /subscriptions/xxx/resourcegroups/my-resource-group/providers/microsoft.operationalinsights/workspaces/my-log-analytics-workspace
        storage_account:
            description:
                - The storage account for the diagnostic setting, if configured.
            returned: always
            type: dict
            contains:
                id:
                    description:
                        - ID of the storage account.
                    returned: always
                    type: str
                    sample: >-
                        /subscriptions/xxx/resourceGroups/my-resource-group/providers/Microsoft.Storage/storageAccounts/my-storage-account
'''

try:
    from azure.mgmt.core.tools import (parse_resource_id, resource_id)
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


class AzureRMMonitorDiagnosticSettingInfo(AzureRMModuleBaseExt):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type="str"),
            resource=dict(type="raw", required=True),
        )

        self.results = dict(
            changed=False,
            settings=[],
        )

        self.name = None
        self.resource = None

        super(AzureRMMonitorDiagnosticSettingInfo, self).__init__(self.module_arg_spec,
                                                                  supports_check_mode=True,
                                                                  supports_tags=False,
                                                                  facts_module=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self.process_parameters()

        if self.name is not None:
            self.results["settings"] = self.get_item()
        else:
            self.results["settings"] = self.list_items()

        return self.results

    def process_parameters(self):
        if isinstance(self.resource, dict):
            if "/" not in self.resource.get("type"):
                self.fail("resource type parameter must include namespace, such as 'Microsoft.Network/virtualNetworks'")
            self.resource = resource_id(subscription=self.resource.get("subscription_id", self.subscription_id),
                                        resource_group=self.resource.get("resource_group"),
                                        namespace=self.resource.get("type").split("/")[0],
                                        type=self.resource.get("type").split("/")[1],
                                        name=self.resource.get("name"))

    def get_item(self):
        self.log("Get diagnostic setting for {0} in {1}".format(self.name, self.resource))

        try:
            item = self.monitor_diagnostic_settings_client.diagnostic_settings.get(resource_uri=self.resource, name=self.name)
            return [self.diagnostic_setting_to_dict(item)]
        except Exception:
            self.log("Could not get diagnostic setting for {0} in {1}".format(self.name, self.resource))

        return []

    def list_items(self):
        self.log("List all diagnostic settings in {0}".format(self.resource))
        try:
            items = self.monitor_diagnostic_settings_client.diagnostic_settings.list(resource_uri=self.resource)
            items = [self.diagnostic_setting_to_dict(item) for item in items]
            items = sorted(items, key=lambda d: d["name"])
            return items
        except Exception as exc:
            self.fail("Failed to list all diagnostic settings in {0}: {1}".format(self.resource, str(exc)))

    def diagnostic_setting_to_dict(self, diagnostic_setting):
        setting_dict = diagnostic_setting if isinstance(diagnostic_setting, dict) else diagnostic_setting.as_dict()
        result = dict(
            id=setting_dict.get("id"),
            name=setting_dict.get("name"),
            event_hub=self.event_hub_dict(setting_dict),
            storage_account=self.storage_dict(setting_dict.get("storage_account_id")),
            log_analytics=self.log_analytics_dict(setting_dict.get("workspace_id")),
            logs=[self.log_config_to_dict(log) for log in setting_dict.get("logs", [])],
            metrics=[self.metric_config_to_dict(metric) for metric in setting_dict.get("metrics", [])],
        )
        return self.remove_disabled_config(result)

    def remove_disabled_config(self, diagnostic_setting):
        diagnostic_setting["logs"] = [log for log in diagnostic_setting.get("logs", []) if log.get("enabled")]
        diagnostic_setting["metrics"] = [metric for metric in diagnostic_setting.get("metrics", []) if metric.get("enabled")]
        return diagnostic_setting

    def event_hub_dict(self, setting_dict):
        auth_rule_id = setting_dict.get("event_hub_authorization_rule_id")
        if auth_rule_id:
            parsed_rule_id = parse_resource_id(auth_rule_id)
            return dict(
                id=resource_id(subscription=parsed_rule_id.get("subscription"),
                               resource_group=parsed_rule_id.get("resource_group"),
                               namespace=parsed_rule_id.get("namespace"),
                               type=parsed_rule_id.get("type"),
                               name=parsed_rule_id.get("name")),
                namespace=parsed_rule_id.get("name"),
                hub=setting_dict.get("event_hub_name"),
                policy=parsed_rule_id.get("resource_name"),
            )
        return None

    def storage_dict(self, storage_account_id):
        if storage_account_id:
            return dict(
                id=storage_account_id,
            )
        return None

    def log_analytics_dict(self, workspace_id):
        if workspace_id:
            return dict(
                id=workspace_id,
            )
        return None

    def log_config_to_dict(self, log_config):
        return dict(
            category=log_config.get("category"),
            category_group=log_config.get("category_group"),
            enabled=log_config.get("enabled"),
            retention_policy=self.retention_policy_to_dict(log_config.get("retention_policy")),
        )

    def metric_config_to_dict(self, metric_config):
        return dict(
            category=metric_config.get("category"),
            enabled=metric_config.get("enabled"),
            retention_policy=self.retention_policy_to_dict(metric_config.get("retention_policy")),
        )

    def retention_policy_to_dict(self, policy):
        if policy:
            return dict(
                days=policy.get("days"),
                enabled=policy.get("enabled"),
            )
        return None


def main():
    AzureRMMonitorDiagnosticSettingInfo()


if __name__ == "__main__":
    main()
