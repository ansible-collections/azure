#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_networkflowlog
version_added: "2.5.0"
short_description: Manage the network flow logs
description:
    - Create, update or delete the network flow logs.
options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    location:
        description:
            - Valid Azure location. Defaults to location of the resource group.
        type: str
    name:
        description:
            - The name of the network flow logs.
        required: true
        type: str
    network_watcher_name:
        description:
            - The name of the network watcher.
        type: str
        required: true
    target_resource_id:
        description:
            -  ID of network security group to which flow log will be applied.
        type: str
    storage_id:
        description:
            - ID of the storage account which is used to store the flow log.
        type: str
    enabled:
        description:
            - Flag to enable/disable flow logging.
        type: bool
    retention_policy:
        description:
            - Parameters that define the retention policy for flow log.
        type: dict
        suboptions:
            days:
                description:
                    - Number of days to retain flow log records.
                type: int
            enabled:
                description:
                    - Flag to enable/disable retention.
                type: bool
    flow_analytics_configuration:
        description:
            - Parameters that define the configuration of traffic analytics.
        type: dict
        suboptions:
            network_watcher_flow_analytics_configuration:
                description:
                    - Parameters that define the configuration of traffic analytics.
                type: dict
                suboptions:
                    enabled:
                        description:
                            - Flag to enable/disable traffic analytics.
                        type: bool
                    workspace_id:
                        description:
                            - The resource guid of the attached workspace.
                        type: str
                    workspace_region:
                        description:
                            - The location of the attached workspace.
                        type: str
                    workspace_resource_id:
                        description:
                            - Resource Id of the attached workspace.
                        type: str
                    traffic_analytics_interval:
                        description:
                            - The interval in minutes which would decide how frequently TA service should do flow analytics.
                        type: int
                        choices:
                            - 10
                            - 60
    state:
        description:
            - State of the Flow Logs. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Create network flow log
  azure_rm_networkflowlog:
    resource_group: NetworkWatcherRG
    network_watcher_name: NetworkWatcher_eastus
    name: xz3mlwvnet-xz3mlwaiserv-flowlog02
    enabled: false
    flow_analytics_configuration:
      network_watcher_flow_analytics_configuration:
        enabled: false
        traffic_analytics_interval: 60
        workspace_id: 7c16a8dd-b983-4f75-b78b-a804c169306c
        workspace_region: eastus
        workspace_resource_id: "/subscriptions/xxx-xxx/resourceGroups/DefaultRG-EUS/providers/Microsoft.OperationalInsights/workspaces/DeWorkspace-0-EUS"
    retention_policy:
      days: 2
      enabled: true
    storage_id: "/subscriptions/xxx-xxx/resourceGroups/AutoTagFunctionAppRG/providers/Microsoft.Storage/storageAccounts/autotagfunctionappr9a08"
    target_resource_id: "/subscriptions/xxx-xxx/resourceGroups/xz3mlwaiserv/providers/Microsoft.Network/virtualNetworks/xz3mlwvnet"
    tags:
      key2: value2
      key5: value5

- name: Delete a Flow Logs
  azure_rm_networkflowlog:
    resource_group: myResourceGroup
    network_watcher_name: testwatcher
    name: myNetflowlog
    state: absent
'''
RETURN = '''
state:
    description:
        - The facts of the network flow logs.
    returned: always
    type: complex
    contains:
        resource_group:
            description:
                - The resource group.
            type: str
            returned: always
            sample: NetworkWatcherRG
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/NetWatcherRG/providers/Microsoft.Network/networkWatchers/NetWatcher_eastus/flowLogs/xz-flowlog"
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: eastus
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: xz-flowlog
        network_watcher_name:
            description:
                - The name of the network watcher.
            type: str
            returned: always
            sample: NetWatcher_eastus
        target_resource_id:
            description:
                - ID of network security group to which flow log will be applied.
            type: str
            returned: always
            sample: /subscriptions/xxx-xxx/resourceGroups/xz3mlwaiserv/providers/Microsoft.Network/virtualNetworks/xz3mlwvnet"
        storage_id:
            description:
                - ID of the storage account which is used to store the flow log.
            type: str
            returned: always
            sample: "/subscriptions/xxx-xxx/resourceGroups/AutoTagFunctionAppRG/providers/Microsoft.Storage/storageAccounts/autotagfunc01"
        enanbled:
            description:
                - Flag to enable/disable flow logging.
            type: str
            returned: always
            sample: true
        retention_policy:
            description:
                - Parameters that define the retention policy for flow log.
            type: complex
            returned: always
            contains:
                day:
                    description:
                        - Number of days to retain flow log records.
                    type: int
                    returned: always
                    sample: 0
                enabled:
                    description:
                        - Flag to enable/disable retention.
                    type: bool
                    returned: always
                    sample: false
        flow_analytics_configuration:
            description:
                - Parameters that define the configuration of traffic analytics.
            type: complex
            returned: always
            contains:
                network_watcher_flow_analytics_configuration:
                    description:
                        - Parameters that define the configuration of traffic analytics.
                    type: complex
                    returned: always
                    contains:
                        enabled:
                            description:
                                - Flag to enable/disable traffic analytics.
                            type: bool
                            returned: always
                            sample: true
                        workspace_id:
                            description:
                                - The resource guid of the attached workspace.
                            type: str
                            returned: always
                            sample: 7c16a8dd-b983-4f75-b78b-a804c169306c
                        workspace_region:
                            description:
                                - The location of the attached workspace.
                            type: str
                            returned: always
                            sample: eastus
                        workspace_resource_id:
                            description:
                                - Resource Id of the attached workspace.
                            type: str
                            returned: always
                            sample: /subscriptions/xxx-xxx/resourceGroups/DefaulUS/providers/Microsoft.OperationalInsights/workspaces/DefaultWorkspace-0-EUS"
                        traffic_analytics_interval:
                            description:
                                - The interval in minutes which would decide how frequently TA service should do flow analytics.
                            type: str
                            returned: always
                            sample: 60
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: { 'key1':'value1' }
        type:
            description:
                - Resource type.
            returned: always
            type: str
            sample: "Microsoft.Network/networkWatchers/flowLogs"
        provisioning_state:
            description:
                - The provisioning state of the network flow logs resource.
            type: str
            returned: always
            sample: Succeeded
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


class AzureRMNetworkFlowLog(AzureRMModuleBaseExt):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            network_watcher_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            target_resource_id=dict(type='str'),
            storage_id=dict(type='str'),
            enabled=dict(type='bool'),
            retention_policy=dict(
                type='dict',
                options=dict(
                    days=dict(type='int'),
                    enabled=dict(type='bool'),
                ),
            ),
            flow_analytics_configuration=dict(
                type='dict',
                options=dict(
                    network_watcher_flow_analytics_configuration=dict(
                        type='dict',
                        options=dict(
                            enabled=dict(type='bool'),
                            workspace_id=dict(type='str'),
                            workspace_region=dict(type='str'),
                            workspace_resource_id=dict(type='str'),
                            traffic_analytics_interval=dict(type='int', choices=[10, 60])
                        )
                    )
                )
            ),
        )

        self.resource_group = None
        self.network_watcher_name = None
        self.name = None
        self.state = None
        self.location = None
        self.tags = None
        self.body = dict()

        self.results = dict(
            changed=False,
            state=dict()
        )

        super(AzureRMNetworkFlowLog, self).__init__(self.module_arg_spec,
                                                    supports_tags=True,
                                                    supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        resource_group = self.get_resource_group(self.resource_group)
        if self.location is not None:
            self.body['location'] = self.location
        else:
            # Set default location
            self.body['location'] = resource_group.location
        self.body['tags'] = self.tags

        changed = False
        results = dict()

        old_response = self.get_by_name()

        if old_response is not None:
            if self.state == 'present':
                if self.body.get('retention_policy') is not None and\
                   not self.default_compare({}, self.body.get('retention_policy'), old_response.get('retention_policy'), '', dict(compare=[])):
                    changed = True
                elif (self.body.get('flow_analytics_configuration') is not None and not self.default_compare(
                        {}, self.body['flow_analytics_configuration'], old_response['flow_analytics_configuration'], '', dict(compare=[]))):
                    changed = True

                elif self.body.get('enabled') is not None and bool(self.body['enabled']) != bool(old_response.get('enabled')):
                    changed = True
                if changed:
                    results = self.create_or_update(self.body)
                else:
                    results = old_response

                update_tags, new_tags = self.update_tags(old_response['tags'])
                if update_tags:
                    changed = True
                    if not self.check_mode:
                        results = self.update_flowlog_tags(new_tags)
            else:
                changed = True
                if not self.check_mode:
                    results = self.delete_flowlog()
        else:
            if self.state == 'present':
                changed = True
                if not self.check_mode:
                    results = self.create_or_update(self.body)
            else:
                changed = False
                self.log("The Flow Log is not exists")

        self.results['changed'] = changed
        self.results['state'] = results

        return self.results

    def get_by_name(self):
        response = None
        try:
            response = self.network_client.flow_logs.get(self.resource_group, self.network_watcher_name, self.name)

        except ResourceNotFoundError as exec:
            self.log("Failed to get network flow log, Exception as {0}".format(exec))

        return self.to_dict(response)

    def create_or_update(self, body):
        response = None
        try:
            response = self.network_client.flow_logs.begin_create_or_update(self.resource_group, self.network_watcher_name, self.name, body)
            response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error creating Flow Log {0} - {1}".format(self.name, str(exc)))

        return self.to_dict(response)

    def update_flowlog_tags(self, tags):
        response = None
        try:
            response = self.network_client.flow_logs.update_tags(self.resource_group, self.network_watcher_name, self.name, dict(tags=tags))
        except Exception as exc:
            self.fail("Error updating Flow Logs {0} - {1}".format(self.name, str(exc)))
        return self.to_dict(response)

    def delete_flowlog(self):
        try:
            self.network_client.flow_logs.begin_delete(self.resource_group, self.network_watcher_name, self.name)
        except Exception as exc:
            self.fail("Error deleting Flow Logs {0} - {1}".format(self.name, str(exc)))

    def to_dict(self, body):
        results = dict()
        if body is not None:
            results = dict(
                resource_group=self.resource_group,
                network_watcher_name=self.network_watcher_name,
                id=body.id,
                name=body.name,
                location=body.location,
                tags=body.tags,
                type=body.type,
                provisioning_state=body.provisioning_state,
                target_resource_id=body.target_resource_id,
                storage_id=body.storage_id,
                enabled=body.enabled,
                retention_policy=dict(),
                flow_analytics_configuration=dict()
            )
            if body.retention_policy is not None:
                results['retention_policy']['days'] = body.retention_policy.days
                results['retention_policy']['enabled'] = body.retention_policy.enabled
            if body.flow_analytics_configuration is not None:
                results['flow_analytics_configuration']['network_watcher_flow_analytics_configuration'] = dict()
                if body.flow_analytics_configuration.network_watcher_flow_analytics_configuration is not None:
                    new_config = body.flow_analytics_configuration.network_watcher_flow_analytics_configuration
                    results['flow_analytics_configuration']['network_watcher_flow_analytics_configuration']['enabled'] = new_config.enabled
                    results['flow_analytics_configuration']['network_watcher_flow_analytics_configuration']['workspace_id'] = new_config.workspace_id
                    results['flow_analytics_configuration']['network_watcher_flow_analytics_configuration']['workspace_region'] = new_config.workspace_region
                    results['flow_analytics_configuration']['network_watcher_flow_analytics_configuration']['workspace_resource_id'] = \
                        new_config.workspace_resource_id
                    results['flow_analytics_configuration']['network_watcher_flow_analytics_configuration']['traffic_analytics_interval'] = \
                        new_config.traffic_analytics_interval

            return results
        return None


def main():
    AzureRMNetworkFlowLog()


if __name__ == '__main__':
    main()
