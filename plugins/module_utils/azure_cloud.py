# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long


from pprint import pformat
import os

GLOBAL_CONFIG_DIR = os.getenv('AZURE_CONFIG_DIR', None) or os.path.expanduser(os.path.join('~', '.azure'))
CLOUD_CONFIG_FILE = os.path.join(GLOBAL_CONFIG_DIR, 'clouds.config')


class CloudEndpoints:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    def __init__(self,  # pylint: disable=unused-argument
                 active_directory=None,
                 active_directory_data_lake_resource_id=None,
                 active_directory_graph_resource_id=None,
                 active_directory_resource_id=None,
                 app_insights_resource_id=None,
                 app_insights_telemetry_channel_resource_id=None,
                 attestation_resource_id=None,
                 azmirror_storage_account_resource_id=None,
                 batch_resource_id=None,
                 gallery=None,
                 log_analytics_resource_id=None,
                 management=None,
                 media_resource_id=None,
                 microsoft_graph_resource_id=None,
                 ossrdbms_resource_id=None,
                 portal=None,
                 resource_manager=None,
                 sql_management=None,
                 synapse_analytics_resource_id=None,
                 vm_image_alias_doc=None,
                 **kwargs):  # To support init with __dict__ for deserialization
        # Attribute names are significant. They are used when storing/retrieving clouds from config
        self.active_directory = active_directory
        self.active_directory_data_lake_resource_id = active_directory_data_lake_resource_id
        self.active_directory_graph_resource_id = active_directory_graph_resource_id
        self.active_directory_resource_id = active_directory_resource_id
        self.app_insights_resource_id = app_insights_resource_id
        self.app_insights_telemetry_channel_resource_id = app_insights_telemetry_channel_resource_id
        self.attestation_resource_id = attestation_resource_id
        self.azmirror_storage_account_resource_id = azmirror_storage_account_resource_id
        self.batch_resource_id = batch_resource_id
        self.gallery = gallery
        self.log_analytics_resource_id = log_analytics_resource_id
        self.management = management
        self.media_resource_id = media_resource_id
        self.microsoft_graph_resource_id = microsoft_graph_resource_id
        self.ossrdbms_resource_id = ossrdbms_resource_id
        self.portal = portal
        self.resource_manager = resource_manager
        self.sql_management = sql_management
        self.synapse_analytics_resource_id = synapse_analytics_resource_id
        self.vm_image_alias_doc = vm_image_alias_doc
        # Please keep the endpoints in alphabetical order

    def has_endpoint_set(self, endpoint_name):
        try:
            # Can't simply use hasattr here as we override __getattribute__ below.
            # Python 3 hasattr() only returns False if an AttributeError is raised but we raise
            # CloudEndpointNotSetException. This exception is not a subclass of AttributeError.
            getattr(self, endpoint_name)
            return True
        except Exception:  # pylint: disable=broad-except
            return False

    def __getattribute__(self, name):
        val = object.__getattribute__(self, name)
        if val is None:
            raise Exception("The endpoint '{}' for this cloud "
                            "is not set but is used.\n"
                            "{} may be corrupt or invalid.\nResolve the error or delete this file "
                            "and try again.".format(name, CLOUD_CONFIG_FILE))
        return val


class Cloud:  # pylint: disable=too-few-public-methods
    """ Represents an Azure Cloud instance """

    def __init__(self, name, endpoints=None):
        self.name = name
        self.endpoints = endpoints or CloudEndpoints()

    def __str__(self):
        o = {
            'name': self.name,
            'endpoints': vars(self.endpoints),
        }
        return pformat(o)

    def to_json(self):
        return {'name': self.name, "endpoints": self.endpoints.__dict__}

    @classmethod
    def from_json(cls, json_str):
        return cls(json_str['name'],
                   endpoints=CloudEndpoints(**json_str['endpoints']))


class CloudNameEnum:  # pylint: disable=too-few-public-methods
    AzureCloud = 'AzureCloud'
    AzureChinaCloud = 'AzureChinaCloud'
    AzureUSGovernment = 'AzureUSGovernment'
    AzureGermanCloud = 'AzureGermanCloud'


AZURE_PUBLIC_CLOUD = Cloud(
    CloudNameEnum.AzureCloud,
    endpoints=CloudEndpoints(
        management='https://management.core.windows.net/',
        resource_manager='https://management.azure.com/',
        sql_management='https://management.core.windows.net:8443/',
        batch_resource_id='https://batch.core.windows.net/',
        gallery='https://gallery.azure.com/',
        active_directory='https://login.microsoftonline.com',
        active_directory_resource_id='https://management.core.windows.net/',
        active_directory_graph_resource_id='https://graph.windows.net/',
        microsoft_graph_resource_id='https://graph.microsoft.com/',
        active_directory_data_lake_resource_id='https://datalake.azure.net/',
        vm_image_alias_doc='https://raw.githubusercontent.com/Azure/azure-rest-api-specs/main/arm-compute/quickstart-templates/aliases.json',
        media_resource_id='https://rest.media.azure.net',
        ossrdbms_resource_id='https://ossrdbms-aad.database.windows.net',
        app_insights_resource_id='https://api.applicationinsights.io',
        log_analytics_resource_id='https://api.loganalytics.io',
        app_insights_telemetry_channel_resource_id='https://dc.applicationinsights.azure.com/v2/track',
        synapse_analytics_resource_id='https://dev.azuresynapse.net',
        attestation_resource_id='https://attest.azure.net',
        portal='https://portal.azure.com'))

AZURE_CHINA_CLOUD = Cloud(
    CloudNameEnum.AzureChinaCloud,
    endpoints=CloudEndpoints(
        management='https://management.core.chinacloudapi.cn/',
        resource_manager='https://management.chinacloudapi.cn',
        sql_management='https://management.core.chinacloudapi.cn:8443/',
        batch_resource_id='https://batch.chinacloudapi.cn/',
        gallery='https://gallery.chinacloudapi.cn/',
        active_directory='https://login.chinacloudapi.cn',
        active_directory_resource_id='https://management.core.chinacloudapi.cn/',
        active_directory_graph_resource_id='https://graph.chinacloudapi.cn/',
        microsoft_graph_resource_id='https://microsoftgraph.chinacloudapi.cn',
        vm_image_alias_doc='https://raw.githubusercontent.com/Azure/azure-rest-api-specs/main/arm-compute/quickstart-templates/aliases.json',
        media_resource_id='https://rest.media.chinacloudapi.cn',
        ossrdbms_resource_id='https://ossrdbms-aad.database.chinacloudapi.cn',
        app_insights_resource_id='https://api.applicationinsights.azure.cn',
        log_analytics_resource_id='https://api.loganalytics.azure.cn',
        app_insights_telemetry_channel_resource_id='https://dc.applicationinsights.azure.cn/v2/track',
        synapse_analytics_resource_id='https://dev.azuresynapse.azure.cn',
        portal='https://portal.azure.cn'))

AZURE_US_GOV_CLOUD = Cloud(
    CloudNameEnum.AzureUSGovernment,
    endpoints=CloudEndpoints(
        management='https://management.core.usgovcloudapi.net/',
        resource_manager='https://management.usgovcloudapi.net/',
        sql_management='https://management.core.usgovcloudapi.net:8443/',
        batch_resource_id='https://batch.core.usgovcloudapi.net/',
        gallery='https://gallery.usgovcloudapi.net/',
        active_directory='https://login.microsoftonline.us',
        active_directory_resource_id='https://management.core.usgovcloudapi.net/',
        active_directory_graph_resource_id='https://graph.windows.net/',
        microsoft_graph_resource_id='https://graph.microsoft.us/',
        vm_image_alias_doc='https://raw.githubusercontent.com/Azure/azure-rest-api-specs/main/arm-compute/quickstart-templates/aliases.json',
        media_resource_id='https://rest.media.usgovcloudapi.net',
        ossrdbms_resource_id='https://ossrdbms-aad.database.usgovcloudapi.net',
        app_insights_resource_id='https://api.applicationinsights.us',
        log_analytics_resource_id='https://api.loganalytics.us',
        app_insights_telemetry_channel_resource_id='https://dc.applicationinsights.us/v2/track',
        synapse_analytics_resource_id='https://dev.azuresynapse.usgovcloudapi.net',
        portal='https://portal.azure.us'))

AZURE_GERMAN_CLOUD = Cloud(
    CloudNameEnum.AzureGermanCloud,
    endpoints=CloudEndpoints(
        management='https://management.core.cloudapi.de/',
        resource_manager='https://management.microsoftazure.de',
        sql_management='https://management.core.cloudapi.de:8443/',
        batch_resource_id='https://batch.cloudapi.de/',
        gallery='https://gallery.cloudapi.de/',
        active_directory='https://login.microsoftonline.de',
        active_directory_resource_id='https://management.core.cloudapi.de/',
        active_directory_graph_resource_id='https://graph.cloudapi.de/',
        microsoft_graph_resource_id='https://graph.microsoft.de',
        vm_image_alias_doc='https://raw.githubusercontent.com/Azure/azure-rest-api-specs/main/arm-compute/quickstart-templates/aliases.json',
        media_resource_id='https://rest.media.cloudapi.de',
        ossrdbms_resource_id='https://ossrdbms-aad.database.cloudapi.de',
        portal='https://portal.microsoftazure.de'))

HARD_CODED_CLOUD_DICT = dict(AzureCloud=AZURE_PUBLIC_CLOUD,
                             AzureChinaCloud=AZURE_CHINA_CLOUD,
                             AzureUSGovernment=AZURE_US_GOV_CLOUD,
                             AzureGermanCloud=AZURE_GERMAN_CLOUD)


def get_cloud_from_endpoint(endpoint):
    for cloud_key, cloud_value in HARD_CODED_CLOUD_DICT.items():
        has_endpoint = False
        for endpoint_key, endpoint_value in vars(cloud_value.endpoints).items():
            if endpoint_value and endpoint.startswith(endpoint_value):
                has_endpoint = True
                break
        if has_endpoint:
            return cloud_value
    return None
