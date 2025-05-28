#!/usr/bin/python
#
# Copyright (c) 2025 Klaas Demter (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_monitordatacollectionrules
version_added: "3.7.0"
short_description: Create, update and delete Data Collection Rules
description:
    - Create, update and delete Data Collection Rules

options:
    name:
        description:
            - The name of the data collection rule you're creating/changing
        required: true
        type: str
    resource_group:
        description:
            - The name of the resource group
        required: true
        type: str
    location:
        description:
            - Location of the data colelction rule
            - defaults to location of exiting data collection rule or
            - location of the resource group if unspecified
        required: false
        type: str
    kind:
        description:
            - Kind of the data collection rule
            - Use C(Linux) for Linux.
            - Use C(Windows) for Windows.
        type: str
        choices:
            - Linux
            - Windows
    description:
        description:
            - Description for the data collection rule
        type: str
    data_collection_endpoint_id:
        description:
            - The resource ID of the data collection endpoint that this rule can be used with
        type: str
    stream_declarations:
        description:
            - Declaration of a custom stream. Sub dict is a list of columns used by data in this stream.
            - top level key is the name of the stream_declaration
            - U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.streamdeclaration?view=azure-python)
        type: dict
        suboptions:
            name_of_stream:
                description:
                    - Name of the stream
                type: dict
                suboptions:
                    columns:
                        description:
                            - Declaration of a custom stream.
                        type: list
                        elements: dict
                        suboptions:
                            name:
                                description:
                                    - The name of the column.
                                type: str
                            type:
                                description:
                                    - The type of the column data.
                                type: str
                                choices:
                                    - string
                                    - int
                                    - long
                                    - real
                                    - boolean
                                    - datetime
                                    - dynamic
    data_sources:
        description:
            - The specification of data sources.
            - This property is optional and can be omitted if the rule is meant to be used via direct calls to the provisioned endpoint.
            - >-
              U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.datacollectionruledatasources?view=azure-python)
        type: dict
        suboptions:
            performance_counters:
                description:
                    - Definition of which performance counters will be collected and how they will be collected by this data collection rule.
                    - Collected from both Windows and Linux machines where the counter is present.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.perfcounterdatasource?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    streams:
                        description:
                            - List of streams that this data source will be sent to.
                            - A stream indicates what schema will be used for this data and usually what table in Log Analytics the data will be sent to.
                        type: list
                        elements: str
                    sampling_frequency_in_seconds:
                        description:
                            - The number of seconds between consecutive counter measurements (samples).
                        type: int
                    counter_specifiers:
                        description:
                            - A list of specifier names of the performance counters you want to collect.
                            - Use a wildcard (*) to collect a counter for all instances.
                            - To get a list of performance counters on Windows, run the command 'typeperf'
                        type: list
                        elements: str
                    name:
                        description:
                            - A friendly name for the data source.
                            - This name should be unique across all data sources (regardless of type) within the data collection rule.
                        type: str
            windows_event_logs:
                description:
                    - Definition of which Windows Event Log events will be collected and how they will be collected.
                    - Only collected from Windows machines.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.windowseventlogdatasource?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    streams:
                        description:
                            - List of streams that this data source will be sent to.
                            - A stream indicates what schema will be used for this data and usually what table in Log Analytics the data will be sent to.
                        type: list
                        elements: str
                    x_path_queries:
                        description:
                            - A list of Windows Event Log queries in XPATH format.
                        type: list
                        elements: str
                    name:
                        description:
                            - A friendly name for the data source.
                            - This name should be unique across all data sources (regardless of type) within the data collection rule.
                        type: str
            syslog:
                description:
                    - Definition of which syslog data will be collected and how it will be collected. Only collected from Linux machines.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.syslogdatasource?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    streams:
                        description:
                            - List of streams that this data source will be sent to.
                            - A stream indicates what schema will be used for this data and usually what table in Log Analytics the data will be sent to.
                        type: list
                        elements: str
                    facility_names:
                        description:
                            - The list of facility names.
                        type: list
                        elements: str
                    log_levels:
                        description:
                            - The log levels to collect.
                        type: list
                        elements: str
                    name:
                        description:
                            - A friendly name for the data source.
                            - This name should be unique across all data sources (regardless of type) within the data collection rule.
                        type: str
            extensions:
                description:
                    - Definition of which data will be collected from a separate VM extension that integrates with the Azure Monitor Agent.
                    - Collected from either Windows and Linux machines, depending on which extension is defined.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.extensiondatasource?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    streams:
                        description:
                            - List of streams that this data source will be sent to.
                            - A stream indicates what schema will be used for this data and usually what table in Log Analytics the data will be sent to.
                        type: list
                        elements: str
                    extension_name:
                        description:
                            - The name of the VM extension.
                        type: list
                        elements: str
                    extension_settings:
                        description:
                            - The extension settings. The format is specific for particular extension.
                        type: str
                    input_data_sources:
                        description:
                            - The list of data sources this extension needs data from.
                        type: list
                        elements: str
                    name:
                        description:
                            - A friendly name for the data source.
                            - This name should be unique across all data sources (regardless of type) within the data collection rule.
                        type: str
            log_files:
                description:
                    - Definition of which custom log files will be collected by this data collection rule.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.logfilesdatasource?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    streams:
                        description:
                            - List of streams that this data source will be sent to.
                            - A stream indicates what schema will be used for this data and usually what table in Log Analytics the data will be sent to.
                        type: list
                        elements: str
                    file_patterns:
                        description:
                            - File Patterns where the log files are located
                        type: list
                        elements: str
                    format:
                        description:
                            - The data format of the log files.
                        type: str
                    settings:
                        description:
                            - The log files specific settings.
                        type: dict
                        suboptions:
                            text:
                                description:
                                    - Text settings
                                type: str
                    name:
                        description:
                            - A friendly name for the data source.
                            - This name should be unique across all data sources (regardless of type) within the data collection rule.
                        type: str
            iis_logs:
                description:
                    - Enables IIS logs to be collected by this data collection rule.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.iislogsdatasource?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    streams:
                        description:
                            - IIS streams.
                        type: list
                        elements: str
                    log_directories:
                        description:
                            - Absolute paths file location.
                        type: list
                        elements: str
                    name:
                        description:
                            - A friendly name for the data source.
                            - This name should be unique across all data sources (regardless of type) within the data collection rule.
                        type: str
            windows_firewall_logs:
                description:
                    - Enables Firewall logs to be collected by this data collection rule.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.windowsfirewalllogsdatasource?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    streams:
                        description:
                            - Firewall logs streams.
                        type: list
                        elements: str
                    name:
                        description:
                            - A friendly name for the data source.
                            - This name should be unique across all data sources (regardless of type) within the data collection rule.
                        type: str
            prometheus_forwarder:
                description:
                    - Definition of Prometheus metrics forwarding configuration.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.prometheusforwarderdatasource?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    streams:
                        description:
                            - List of streams that this data source will be sent to.
                        type: list
                        elements: str
                    label_include_filter:
                        description:
                            - The list of label inclusion filters in the form of label "name-value" pairs.
                            - Currently only one label is supported "microsoft_metrics_include_label". Label values are matched case-insensitively.
                        type: dict
                    name:
                        description:
                            - A friendly name for the data source.
                            - This name should be unique across all data sources (regardless of type) within the data collection rule.
                        type: str
            platform_telemetry:
                description:
                    - Definition of platform telemetry data source configuration.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.platformtelemetrydatasource?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    streams:
                        description:
                            - List of platform telemetry streams to collect.
                        type: list
                        elements: str
                    name:
                        description:
                            - A friendly name for the data source.
                            - This name should be unique across all data sources (regardless of type) within the data collection rule.
                        type: str
            data_imports:
                description:
                    - Specifications of pull based data sources.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.datasourcesspecdataimports?view=azure-python)
                type: dict
                suboptions:
                    event_hub:
                        description:
                            - Definition of Event Hub configuration.
                        type: dict
                        suboptions:
                            name:
                                description:
                                    - A friendly name for the data source.
                                    - This name should be unique across all data sources (regardless of type) within the data collection rule.
                                type: str
                            consumer_group:
                                description:
                                    - Event Hub consumer group name.
                                type: str
                            stream:
                                description:
                                    - The stream to collect from EventHub.
                                type: str
    destinations:
        description:
            - >-
              U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.datacollectionruledestinations?view=azure-python)
        type: dict
        suboptions:
            log_analytics:
                description:
                    - List of Log Analytics destinations.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.loganalyticsdestination?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    workspace_resource_id:
                        description:
                            - The resource ID of the Log Analytics workspace.
                        type: str
                    name:
                        description:
                            - A friendly name for the destination.
                            - This name should be unique across all destinations (regardless of type) within the data collection rule.
                        type: str
            monitoring_accounts:
                description:
                    - List of monitoring account destinations.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.monitoringaccountdestination?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    account_resource_id:
                        description:
                            - The resource ID of the monitoring account.
                        type: str
                    name:
                        description:
                            - A friendly name for the destination.
                            - This name should be unique across all destinations (regardless of type) within the data collection rule.
                        type: str
            azure_monitor_metrics:
                description:
                    - Azure Monitor Metrics destination
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.destinationsspecazuremonitormetrics?view=azure-python)
                type: str
            event_hubs:
                description:
                    - List of Event Hubs destinations.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.eventhubdestination?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    event_hub_resource_id:
                        description:
                            - The resource ID of the event hub.
                        type: str
                    name:
                        description:
                            - A friendly name for the destination.
                            - This name should be unique across all destinations (regardless of type) within the data collection rule.
                        type: str
            event_hubs_direct:
                description:
                    - List of Event Hubs Direct destinations.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.eventhubdirectdestination?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    event_hub_resource_id:
                        description:
                            - The resource ID of the event hub.
                        type: str
                    name:
                        description:
                            - A friendly name for the destination.
                            - This name should be unique across all destinations (regardless of type) within the data collection rule.
                        type: str
            storage_blobs_direct:
                description:
                    - List of Storage Blob Direct destinations. To be used only for sending data directly to store from the agent.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.storageblobdestination?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    container_name:
                        description:
                            - The container name of the Storage Blob.
                        type: str
                    storage_account_resource_id:
                        description:
                            - The resource ID of the storage account.
                        type: str
                    name:
                        description:
                            - A friendly name for the destination.
                            - This name should be unique across all destinations (regardless of type) within the data collection rule.
                        type: str
            storage_tables_direct:
                description:
                    - List of Storage Table Direct destinations.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.storagetabledestination?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    table_name:
                        description:
                            - The name of the Storage Table.
                        type: str
                    storage_account_resource_id:
                        description:
                            - The resource ID of the storage account.
                        type: str
                    name:
                        description:
                            - A friendly name for the destination.
                            - This name should be unique across all destinations (regardless of type) within the data collection rule.
                        type: str
            storage_accounts:
                description:
                    - List of storage accounts destinations.
                    - >-
                      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.storageblobdestination?view=azure-python)
                type: list
                elements: dict
                suboptions:
                    container_name:
                        description:
                            - The container name of the Storage Blob.
                        type: str
                    storage_account_resource_id:
                        description:
                            - The resource ID of the storage account.
                        type: str
                    name:
                        description:
                            - A friendly name for the destination.
                            - This name should be unique across all destinations (regardless of type) within the data collection rule.
                        type: str
    data_flows:
        description:
            - Definition of which streams are sent to which destinations.
            - >-
              U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2022_06_01.models.dataflow?view=azure-python)
        type: list
        elements: dict
        suboptions:
            streams:
                description:
                    - List of streams for this data flow.
                    - >-
                      U(https://learn.microsoft.com/en-us/rest/api/monitor/data-collection-rules/create?view=rest-monitor-2023-03-11&tabs=HTTP&tryIt=true#knowndataflowstreams)
                type: list
                elements: str
            destinations:
                description:
                    - List of destinations for this data flow.
                type: list
                elements: str
            transform_kql:
                description:
                    - The KQL query to transform stream data.
                type: str
            output_stream:
                description:
                    - The output stream of the transform. Only required if the transform changes data to a different stream.
                type: str
            built_in_transform:
                description:
                    - The builtIn transform to transform stream data.
                type: str
    state:
        description:
            - State of the data collection rule
            - Use C(present) for creating/updating a data collection rule.
            - Use C(absent) for deleting a data collection rule.
        default: present
        type: str
        choices:
            - present
            - absent
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Klaas Demter (@Klaas-)
'''

EXAMPLES = '''
- name: Add a data collection rule
  azure.azcollection.azure_rm_monitordatacollectionrules:
    state: present
    name: data_collection_rule_name
    resource_group: resource_group_name
    location: westeurope
    kind: Linux
    description: This is an example description of a data collection rule
    data_sources:
      performance_counters:
        - name: perfCounterDataSource
          streams:
            - Microsoft-Perf
          sampling_frequency_in_seconds: 60
          counter_specifiers:
            - Processor(*)\\% Processor Time
            - Processor(*)\\% Idle Time
    destinations:
      log_analytics:
        - workspace_resource_id: \
/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resougce_group_name_log_analytics_workspace/providers/Microsoft.OperationalInsights/workspaces/log_analytics_workspace_name
          name: log_analytics_workspace_name
    data_flows:
      - destinations:
          - log_analytics_workspace_name
        streams:
          - Microsoft-Perf
    append_tags: false
    tags:
      ThisIsAnExampleTag: ExampleValue

- name: Add a data collection rule
  azure.azcollection.azure_rm_monitordatacollectionrules:
    state: present
    name: data_collection_rule_name
    resource_group: resource_group_name
    append_tags: true
    tags:
      ThisIsAnAddedExampleTag: ExampleValue

# Note this needs a DCR endpoint, not sure why, creating one via portal does not need that
# Also the table in your log analytics workspace has to already exist
- name: Add a data collection rule for collecting a custom log
  azure.azcollection.azure_rm_monitordatacollectionrules:
    name: data_collection_rule_name
    resource_group: resource_group_name
    location: westeurope
    kind: Linux
    data_sources:
      log_files:
        - file_patterns:
            - /var/log/dnf.rpm.log
          format: text
          name: Custom-Text-CustomLogs_CL
          streams:
            - Custom-Text-CustomLogs_CL
    destinations:
      log_analytics:
        - workspace_resource_id: \
/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resougce_group_name_log_analytics_workspace/providers/Microsoft.OperationalInsights/workspaces/log_analytics_workspace_name
          name: log_analytics_workspace_name
    data_flows:
      - destinations:
          - log_analytics_workspace_name
        output_stream: Custom-CustomLogs_CL
        streams:
          - Custom-Text-CustomLogs_CL
        transform_kql: source
    data_collection_endpoint_id: \
/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resougce_group_name_log_analytics_workspace/providers/Microsoft.Insights/dataCollectionEndpoints/dcr-endpoint
    stream_declarations:
      Custom-Text-CustomLogs_CL:
        columns:
          - name: TimeGenerated
            type: datetime
          - name: RawData
            type: string
          - name: FilePath
            type: string
          - name: Computer
            type: string


- name: Delete a data collection rule
  azure.azcollection.azure_rm_monitordatacollectionrules:
    state: present
    name: data_collection_rule_name
    resource_group: resource_group_name
'''

RETURN = '''
datacollectionrule:
    description:
        - Details of the data collection rule
        - Is null on state==absent (data collection rule does not exist or will be deleted)
        - Assumes you make legal changes in check mode
    type: dict
    returned: always
    sample: {
        "data_flows": [...],
        "data_sources": {},
        "description": "Description of your data collection rule",
        "destinations": {},
        "etag": "str",
        "id": \
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/resource_group_name/providers/Microsoft.Insights/dataCollectionRules/data_collection_rule_name",
        "immutable_id": "dcr-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "kind": "Linux",
        "location": "westeurope",
        "name": "data_collection_rule_name",
        "provisioning_state": "Succeeded",
        "system_data": {
            "created_at": "2025-01-01T00:00:00.000000Z",
            "created_by": "xxx@domain.tld",
            "created_by_type": "User",
            "last_modified_at": "2025-01-01T00:00:00.000000Z",
            "last_modified_by": "xxx@domain.tld",
            "last_modified_by_type": "User"
        },
        "tags": {},
        "type": "Microsoft.Insights/dataCollectionRules"
    }
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'DataCollectionRules'

data_flows_spec = dict(
    streams=dict(type='list', elements='str'),
    destinations=dict(type='list', elements='str'),
    transform_kql=dict(type='str'),
    output_stream=dict(type='str'),
    built_in_transform=dict(type='str'),
)

destinations_spec_log_analytics_options = dict(
    workspace_resource_id=dict(type='str'),
    name=dict(type='str')
)

destinations_spec_monitoring_accounts_options = dict(
    account_resource_id=dict(type='str'),
    name=dict(type='str')
)

destinations_spec_event_hubs_options = dict(
    event_hub_resource_id=dict(type='str'),
    name=dict(type='str')
)

destinations_spec_storage_blobs_options = dict(
    container_name=dict(type='str'),
    storage_account_resource_id=dict(type='str'),
    name=dict(type='str')
)

destinations_spec_storage_tables_options = dict(
    table_name=dict(type='str'),
    storage_account_resource_id=dict(type='str'),
    name=dict(type='str')
)

destinations_spec = dict(
    log_analytics=dict(type='list', elements='dict', options=destinations_spec_log_analytics_options),
    monitoring_accounts=dict(type='list', elements='dict', options=destinations_spec_monitoring_accounts_options),
    azure_monitor_metrics=dict(type='str'),
    event_hubs=dict(type='list', elements='dict', options=destinations_spec_event_hubs_options),
    event_hubs_direct=dict(type='list', elements='dict', options=destinations_spec_event_hubs_options),
    storage_blobs_direct=dict(type='list', elements='dict', options=destinations_spec_storage_blobs_options),
    storage_tables_direct=dict(type='list', elements='dict', options=destinations_spec_storage_tables_options),
    storage_accounts=dict(type='list', elements='dict', options=destinations_spec_storage_blobs_options)
)

data_sources_spec_performance_counters_options = dict(
    streams=dict(type='list', elements='str'),
    sampling_frequency_in_seconds=dict(type='int'),
    counter_specifiers=dict(type='list', elements='str'),
    name=dict(type='str')
)

data_sources_spec_windows_event_logs_options = dict(
    streams=dict(type='list', elements='str'),
    x_path_queries=dict(type='list', elements='str'),
    name=dict(type='str')
)

data_sources_spec_syslog_options = dict(
    streams=dict(type='list', elements='str'),
    facility_names=dict(type='list', elements='str'),
    log_levels=dict(type='list', elements='str'),
    name=dict(type='str')
)

data_sources_spec_extensions_options = dict(
    streams=dict(type='list', elements='str'),
    extension_name=dict(type='list', elements='str'),
    extension_settings=dict(type='str'),
    input_data_sources=dict(type='list', elements='str'),
    name=dict(type='str')
)

data_sources_spec_log_files_options = dict(
    streams=dict(type='list', elements='str'),
    file_patterns=dict(type='list', elements='str'),
    format=dict(type='str'),
    settings=dict(type='dict', options=dict(text=dict(type='str'))),
    name=dict(type='str')
)

data_sources_spec_iis_logs_options = dict(
    streams=dict(type='list', elements='str'),
    log_directories=dict(type='list', elements='str'),
    name=dict(type='str')
)

data_sources_spec_windows_firewall_logs_options = dict(
    streams=dict(type='list', elements='str'),
    name=dict(type='str')
)

data_sources_spec_prometheus_forwarder_options = dict(
    streams=dict(type='list', elements='str'),
    label_include_filter=dict(type='dict'),
    name=dict(type='str')
)

data_sources_spec_data_imports_event_hub_options = dict(
    name=dict(type='str'),
    consumer_group=dict(type='str'),
    stream=dict(type='str')
)

data_sources_spec_data_imports_options = dict(
    event_hub=dict(type='dict', options=data_sources_spec_data_imports_event_hub_options)
)

data_sources_spec = dict(
    performance_counters=dict(type='list', elements='dict', options=data_sources_spec_performance_counters_options),
    windows_event_logs=dict(type='list', elements='dict', options=data_sources_spec_windows_event_logs_options),
    syslog=dict(type='list', elements='dict', options=data_sources_spec_syslog_options),
    extensions=dict(type='list', elements='dict', options=data_sources_spec_extensions_options),
    log_files=dict(type='list', elements='dict', options=data_sources_spec_log_files_options),
    iis_logs=dict(type='list', elements='dict', options=data_sources_spec_iis_logs_options),
    windows_firewall_logs=dict(type='list', elements='dict', options=data_sources_spec_windows_firewall_logs_options),
    prometheus_forwarder=dict(type='list', elements='dict', options=data_sources_spec_prometheus_forwarder_options),
    # Platform telemetry options are currently same as windows_firewall_logs
    platform_telemetry=dict(type='list', elements='dict', options=data_sources_spec_windows_firewall_logs_options),
    data_imports=dict(type='dict', options=data_sources_spec_data_imports_options)
)


class AzureRMDataCollectionRules(AzureRMModuleBaseExt):
    """Information class for an Azure RM Data Collection Rules"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            location=dict(type='str'),
            kind=dict(type='str', choices=['Linux', 'Windows']),
            description=dict(type='str'),
            data_collection_endpoint_id=dict(type='str'),
            # https://github.com/ansible/ansible/issues/74001
            # Can't properly define this in arg spec
            stream_declarations=dict(type='dict'),
            data_sources=dict(type='dict', options=data_sources_spec),
            destinations=dict(type='dict', options=destinations_spec),
            data_flows=dict(type='list', elements='dict', options=data_flows_spec),
            state=dict(type='str', choices=['present', 'absent'], default='present')
        )

        self.name = None
        self.resource_group = None
        self.location = None
        self.kind = None
        self.description = None
        self.data_collection_endpoint_id = None
        self.stream_declarations = None
        self.data_sources = None
        self.destinations = None
        self.data_flows = None
        self.state = None
        self.tags = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            datacollectionrule=dict(),
            diff=dict(
                before=None,
                after=None
            )
        )

        super(AzureRMDataCollectionRules, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                         supports_check_mode=True,
                                                         supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        # Defaults for variables
        result = None
        result_compare = dict(compare=[])
        before_dict = None

        # Get current data collection rule if it exists
        before_dict = self.get_data_collection_rule()

        # Create dict from input, without None values
        # https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2021_04_01.models.datacollectionruleresource?view=azure-python
        data_collection_rule_template = {
            "location": self.location,
            "kind": self.kind,
            "description": self.description,
            "data_collection_endpoint_id": self.data_collection_endpoint_id,
            "stream_declarations": self.stream_declarations,
            "data_sources": self.data_sources,
            "destinations": self.destinations,
            "data_flows": self.data_flows
        }
        # Filter out all None values
        data_collection_rule_input = {key: value for key, value in data_collection_rule_template.items() if value is not None}

        # Create/Update if state==present
        if self.state == 'present':
            if before_dict is None:
                # Data collection rule does not exist, create
                # On creation default to location of resource group unless otherwise noted in input variables
                if not self.location:
                    resource_group = self.get_resource_group(self.resource_group)
                    data_collection_rule_input['location'] = resource_group.location
                # On creation input == what we send to api
                data_collection_rule_update = data_collection_rule_input
                # Needs to be extended by tags if set
                if self.tags:
                    data_collection_rule_update['tags'] = self.tags
                self.results['changed'] = True
                if self.check_mode:
                    # Check mode, skipping actual creation
                    pass
                else:
                    create_response = self.create_or_update(data_collection_rule_update)
            else:
                # Data collection rule already exists, updating it
                # Dict for update is the union of existing object overwritten by input data
                data_collection_rule_update = before_dict | data_collection_rule_input

                # Enhanced with tags (special behaviour because of append_tags possibility)
                update_tags, update_tags_content = self.update_tags(before_dict.get('tags'))
                # Check if we need to update the data collection rule
                if update_tags or not self.default_compare({}, data_collection_rule_update, before_dict, '', result_compare):
                    data_collection_rule_update['tags'] = update_tags_content
                    # Need to create/update the Data collection rule; changed -> True
                    self.results['changed'] = True
                    if self.check_mode:
                        # Check mode, skipping actual creation
                        pass
                    else:
                        create_response = self.create_or_update(data_collection_rule_update)

            if self.check_mode or not self.results['changed']:
                # When object was not updated or when running in check mode
                # assume data_collection_rule_update is resulting object
                result = data_collection_rule_update
            else:
                # otherwise take resulting new object from response of create call
                result = create_response

        # Delete data collection rule if state is absent and it exists
        # if it doesn't exist, it's already absent
        elif self.state == 'absent' and before_dict is not None:
            self.results['changed'] = True
            if self.check_mode:
                # do not delete in check mode
                pass
            else:
                self.delete()

        self.results['diff']['before'] = before_dict
        self.results['diff']['after'] = result
        self.results['datacollectionrule'] = result

        return self.results

    def get_data_collection_rule(self):
        '''
        Gets the properties of the specified data collection rule.

        :return: List of Data Collection Rules
        '''
        self.log("Checking if data collection rule {0} in resource group {1} is present".format(self.name,
                                                                                                self.resource_group))

        result = None
        response = None

        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_rules.get(data_collection_rule_name=self.name,
                                                                                                      resource_group_name=self.resource_group)
        except ResourceNotFoundError as ex:
            self.log("Could not find data collection rule {0} in resource group {1}".format(self.name, self.resource_group))
        if response:
            result = self.serialize_obj(response, AZURE_OBJECT_CLASS)

        return result

    def create_or_update(self, data_collection_rule_update):
        result = None
        response = None
        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_rules.create(resource_group_name=self.resource_group,
                                                                                                         data_collection_rule_name=self.name,
                                                                                                         body=data_collection_rule_update,
                                                                                                         logging_enable=False)
        except Exception as ex:
            self.fail("Error creating or update data collection rule {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

        if response:
            result = self.serialize_obj(response, AZURE_OBJECT_CLASS)

        return result

    def delete(self):
        response = None
        try:
            response = self.monitor_management_client_data_collection_rules.data_collection_rules.delete(resource_group_name=self.resource_group,
                                                                                                         data_collection_rule_name=self.name)
        except Exception as ex:
            self.fail("Error deleting data collection rule {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

        return response


def main():
    """Main execution"""
    AzureRMDataCollectionRules()


if __name__ == '__main__':
    main()
