#!/usr/bin/python
#
# Copyright (c) 2021 Ross Bender (@l3ender)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_monitordiagnosticsetting
version_added: "1.10.0"
short_description: Create, update, or manage Azure Monitor diagnostic settings.

description:
    - Create, update, or manage Azure Monitor diagnostic settings for any type of resource.

options:
    name:
        description:
            - The name of the diagnostic settings.
        type: str
        required: true
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
    storage_account:
        description:
            - A storage account which will receive the diagnostic logs.
            - It can be a string containing the storage account resource ID.
            - It can be a dictionary containing I(name) and optionally I(subscription_id) and I(resource_group).
            - At least one of I(storage_account), I(log_analytics), or I(event_hub) must be specified for the diagnostic setting.
        type: raw
    log_analytics:
        description:
            - A log analytics workspace which will receive the diagnostic logs.
            - It can be a string containing the log analytics workspace resource ID.
            - It can be a dictionary containing I(name) and optionally I(subscription_id) and I(resource_group).
            - At least one of I(storage_account), I(log_analytics), or I(event_hub) must be specified for the diagnostic setting.
        type: raw
    event_hub:
        description:
            - An event hub which will receive the diagnostic logs.
            - At least one of I(storage_account), I(log_analytics), or I(event_hub) must be specified for the diagnostic setting.
        type: dict
        suboptions:
            namespace:
                description:
                    - The event hub namespace.
                type: str
                required: true
            policy:
                description:
                    - The shared access policy.
                type: str
                required: true
            hub:
                description:
                    - An event hub name to receive logs. If none is specified, the default event hub will be selected.
                type: str
            resource_group:
                description:
                    - The resource group containing the event hub. If none is specified, the resource group of the I(resource) parameter will be used.
                type: str
            subscription_id:
                description:
                    - The subscription ID containing the event hub. If none is specified, the subscription ID of the I(resource) parameter will be used.
                type: str
    logs:
        description:
            - The list of log setttings.
            - At least one of I(metrics) or I(logs) must be specified for the diagnostic setting.
        type: list
        elements: dict
        suboptions:
            category:
                description:
                    - Name of a Management Group Diagnostic Log category for a resource type this setting is applied to.
                type: str
            category_group:
                description:
                    - Name of a Management Group Diagnostic Log category group for a resource type this setting is applied to.
                type: str
            enabled:
                description:
                    - Whether the log is enabled.
                type: bool
                default: true
            retention_policy:
                description:
                    - The retention policy for this log.
                type: dict
                suboptions:
                    days:
                        description:
                            - The number of days for the retention policy.
                        type: int
                        default: 0
                    enabled:
                        description:
                            - Whether the retention policy is enabled.
                        type: bool
                        default: true
    metrics:
        description:
            - The list of metric setttings.
            - At least one of I(metrics) or I(logs) must be specified for the diagnostic setting.
        type: list
        elements: dict
        suboptions:
            category:
                description:
                    - Name of a Diagnostic Metric category for a resource type this setting is applied to.
                type: str
            enabled:
                description:
                    - Whether the metric category is enabled.
                type: bool
                default: true
            retention_policy:
                description:
                    - The retention policy for this metric.
                type: dict
                suboptions:
                    days:
                        description:
                            - The number of days for the retention policy.
                        type: int
                        default: 0
                    enabled:
                        description:
                            - Whether the retention policy is enabled.
                        type: bool
                        default: true
    state:
        description:
            - State of the private endpoint DNS zone group. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Ross Bender (@l3ender)
'''

EXAMPLES = '''
- name: Create storage-based diagnostic setting for a virtual network
  azure_rm_monitordiagnosticsetting:
    name: "logs-storage"
    resource: "{{ vnet_output.state.id }}"
    storage_account: "{{ storage_output.state.id }}"
    logs:
      - category_group: "allLogs"
    metrics:
      - category: "AllMetrics"

- name: Create diagnostic setting for webapp with log analytics, event hub, and storage
  azure_rm_monitordiagnosticsetting:
    name: "webapp-logs"
    resource:
      name: "my-webapp"
      type: "Microsoft.Web/sites"
      resource_group: "my-webapp-resource-group"
    event_hub:
      namespace: "my-event-hub"
      policy: "RootManageSharedAccessKey"
    log_analytics:
      name: "my-log-analytics-workspace"
      resource_group: "my-log-analytics-workspace-resource-group"
    storage_account:
      name: "mystorageaccount"
    logs:
      - category: "AppServiceHTTPLogs"
      - category: "AppServiceConsoleLogs"
      - category: "AppServiceAppLogs"
      - category: "AppServiceAuditLogs"
      - category: "AppServiceIPSecAuditLogs"
      - category: "AppServicePlatformLogs"

- name: Delete diagnostic setting
  azure_rm_monitordiagnosticsetting:
    name: "webapp-logs"
    resource:
      name: "my-webapp"
      type: "Microsoft.Web/sites"
      resource_group: "my-webapp-resource-group"
    state: "absent"
'''

RETURN = '''
state:
    description:
        - The state of the diagnostic setting.
    returned: always
    type: dict
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
    from msrestazure.tools import (parse_resource_id, resource_id)
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


event_hub_spec = dict(
    namespace=dict(type="str", required=True),
    policy=dict(type="str", required=True),
    hub=dict(type="str"),
    resource_group=dict(type="str"),
    subscription_id=dict(type="str"),
)

retention_policy_spec = dict(
    days=dict(type="int", default=0),
    enabled=dict(type="bool", default=True),
)

logs_spec = dict(
    category=dict(type="str"),
    category_group=dict(type="str"),
    enabled=dict(type="bool", default=True),
    retention_policy=dict(type="dict", options=retention_policy_spec),
)

metrics_spec = dict(
    category=dict(type="str"),
    enabled=dict(type="bool", default=True),
    retention_policy=dict(type="dict", options=retention_policy_spec),
)


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMMonitorDiagnosticSetting(AzureRMModuleBaseExt):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type="str", required=True),
            resource=dict(type="raw", required=True),
            storage_account=dict(type="raw"),
            log_analytics=dict(type="raw"),
            event_hub=dict(type="dict", options=event_hub_spec),
            logs=dict(type="list", elements="dict", options=logs_spec),
            metrics=dict(type="list", elements="dict", options=metrics_spec),
            state=dict(type="str", default="present", choices=["present", "absent"]),
        )

        self.name = None
        self.resource = None
        self.state = None
        self.parameters = dict()
        self.results = dict(
            changed=False,
            state=dict()
        )
        self.to_do = Actions.NoAction

        super(AzureRMMonitorDiagnosticSetting, self).__init__(self.module_arg_spec,
                                                              required_if=[
                                                                  ("state", "present", ("storage_account", "log_analytics", "event_hub"), True),
                                                                  ("state", "present", ("logs", "metrics"), True),
                                                              ],
                                                              supports_tags=False,
                                                              supports_check_mode=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        self.process_parameters()

        old_response = self.get_item()

        if old_response is None or not old_response:
            if self.state == "present":
                self.to_do = Actions.Create
        else:
            if self.state == "absent":
                self.to_do = Actions.Delete
            else:
                self.results["compare"] = []
                if not self.idempotency_check(old_response, self.diagnostic_setting_to_dict(self.parameters)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.results["changed"] = True
            if self.check_mode:
                return self.results
            response = self.create_update_setting()
        elif self.to_do == Actions.Delete:
            self.results["changed"] = True
            if self.check_mode:
                return self.results
            response = self.delete_setting()
        else:
            self.results["changed"] = False
            response = old_response

        if response is not None:
            self.results["state"] = response

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

        parsed_resource = parse_resource_id(self.resource)

        storage_account = self.parameters.pop("storage_account", None)
        if storage_account:
            if isinstance(storage_account, dict):
                if not storage_account.get("name"):
                    self.fail("storage_account must contain 'name'")

                storage_account_id = resource_id(subscription=storage_account.get("subscription_id", parsed_resource.get("subscription")),
                                                 resource_group=storage_account.get("resource_group", parsed_resource.get("resource_group")),
                                                 namespace="Microsoft.Storage",
                                                 type="storageAccounts",
                                                 name=storage_account.get("name"))
            else:
                storage_account_id = storage_account

            self.parameters["storage_account_id"] = storage_account_id

        log_analytics = self.parameters.pop("log_analytics", None)
        if log_analytics:
            if isinstance(log_analytics, dict):
                if not log_analytics.get("name"):
                    self.fail("log_analytics must contain 'name'")

                log_analytics_id = resource_id(subscription=log_analytics.get("subscription_id", parsed_resource.get("subscription")),
                                               resource_group=log_analytics.get("resource_group", parsed_resource.get("resource_group")),
                                               namespace="microsoft.operationalinsights",
                                               type="workspaces",
                                               name=log_analytics.get("name"))
            else:
                log_analytics_id = log_analytics

            self.parameters["workspace_id"] = log_analytics_id

        event_hub = self.parameters.pop("event_hub", None)
        if event_hub:
            hub_subscription_id = event_hub.get("subscription_id") if event_hub.get("subscription_id") else parsed_resource.get("subscription")
            hub_resource_group = event_hub.get("resource_group") if event_hub.get("resource_group") else parsed_resource.get("resource_group")
            auth_rule_id = resource_id(subscription=hub_subscription_id,
                                       resource_group=hub_resource_group,
                                       namespace="Microsoft.EventHub",
                                       type="namespaces",
                                       name=event_hub.get("namespace"),
                                       child_type_1="authorizationrules",
                                       child_name_1=event_hub.get("policy"))
            self.parameters["event_hub_authorization_rule_id"] = auth_rule_id
            self.parameters["event_hub_name"] = event_hub.get("hub")

    def get_item(self):
        self.log("Get diagnostic setting for {0} in {1}".format(self.name, self.resource))

        try:
            item = self.monitor_diagnostic_settings_client.diagnostic_settings.get(resource_uri=self.resource, name=self.name)
            return self.diagnostic_setting_to_dict(item)
        except Exception:
            self.log("Did not find diagnostic setting for {0} in {1}".format(self.name, self.resource))

        return None

    def create_update_setting(self):
        try:
            response = self.monitor_diagnostic_settings_client.diagnostic_settings.create_or_update(resource_uri=self.resource,
                                                                                                    name=self.name,
                                                                                                    parameters=self.parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

            return self.diagnostic_setting_to_dict(response)
        except Exception as exc:
            self.fail("Error creating or updating diagnostic setting {0} for resource {1}: {2}".format(self.name, self.resource, str(exc)))

    def delete_setting(self):
        try:
            response = self.monitor_diagnostic_settings_client.diagnostic_settings.delete(resource_uri=self.resource,
                                                                                          name=self.name)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

            return response
        except Exception as exc:
            self.fail("Error deleting diagnostic setting {0} for resource {1}: {2}".format(self.name, self.resource, str(exc)))

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
    AzureRMMonitorDiagnosticSetting()


if __name__ == "__main__":
    main()
