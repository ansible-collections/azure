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

    ARM_METADATA_INDEX = {
        "active_directory": "authentication.loginEndpoint",
        "active_directory_data_lake_resource_id": "activeDirectoryDataLake",
        "active_directory_graph_resource_id": "graphAudience",
        "active_directory_resource_id": "authentication.audiences[0]",
        "app_insights_resource_id": "appInsightsResourceId",
        "app_insights_telemetry_channel_resource_id": "appInsightsTelemetryChannelResourceId",
        "attestation_resource_id": "attestationResourceId",
        "azmirror_storage_account_resource_id": "azmirrorStorageAccountResourceId",
        "batch_resource_id": "batch",
        "gallery": "gallery",
        "log_analytics_resource_id": "logAnalyticsResourceId",
        "management": "authentication.audiences[0]",
        "media_resource_id": "media",
        "microsoft_graph_resource_id": "microsoftGraphResourceId",
        "ossrdbms_resource_id": "ossrdbmsResourceId",
        "portal": "portal",
        "resource_manager": "resourceManager",
        "sql_management": "sqlManagement",
        "synapse_analytics_resource_id": "synapseAnalyticsResourceId",
        "vm_image_alias_doc": "vmImageAliasDoc",
    }  # Please keep the endpoints in alphabetical order

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


class CloudSuffixes:  # pylint: disable=too-few-public-methods,too-many-instance-attributes

    ARM_METADATA_INDEX = {
        "acr_login_server_endpoint": "suffixes.acrLoginServer",
        "attestation_endpoint": "suffixes.attestationEndpoint",
        "azure_datalake_analytics_catalog_and_job_endpoint": "suffixes.azureDataLakeAnalyticsCatalogAndJob",
        "azure_datalake_store_file_system_endpoint": "suffixes.azureDataLakeStoreFileSystem",
        "keyvault_dns": "suffixes.keyVaultDns",
        "mariadb_server_endpoint": "suffixes.mariadbServerEndpoint",
        "mhsm_dns": "suffixes.mhsmDns",
        "mysql_server_endpoint": "suffixes.mysqlServerEndpoint",
        "postgresql_server_endpoint": "suffixes.postgresqlServerEndpoint",
        "sql_server_hostname": "suffixes.sqlServerHostname",
        "storage_endpoint": "suffixes.storage",
        "storage_sync_endpoint": "suffixes.storageSyncEndpointSuffix",
        "synapse_analytics_endpoint": "suffixes.synapseAnalytics"
    }  # Please keep the suffixes in alphabetical order

    def __init__(self,  # pylint: disable=unused-argument
                 acr_login_server_endpoint=None,
                 attestation_endpoint=None,
                 azure_datalake_analytics_catalog_and_job_endpoint=None,
                 azure_datalake_store_file_system_endpoint=None,
                 keyvault_dns=None,
                 mariadb_server_endpoint=None,
                 mhsm_dns=None,
                 mysql_server_endpoint=None,
                 postgresql_server_endpoint=None,
                 sql_server_hostname=None,
                 storage_endpoint=None,
                 storage_sync_endpoint=None,
                 synapse_analytics_endpoint=None,
                 **kwargs):  # To support init with __dict__ for deserialization
        # Attribute names are significant. They are used when storing/retrieving clouds from config
        self.acr_login_server_endpoint = acr_login_server_endpoint
        self.attestation_endpoint = attestation_endpoint
        self.azure_datalake_analytics_catalog_and_job_endpoint = azure_datalake_analytics_catalog_and_job_endpoint
        self.azure_datalake_store_file_system_endpoint = azure_datalake_store_file_system_endpoint
        self.keyvault_dns = keyvault_dns
        self.mariadb_server_endpoint = mariadb_server_endpoint
        self.mhsm_dns = mhsm_dns
        self.mysql_server_endpoint = mysql_server_endpoint
        self.postgresql_server_endpoint = postgresql_server_endpoint
        self.sql_server_hostname = sql_server_hostname
        self.storage_endpoint = storage_endpoint
        self.storage_sync_endpoint = storage_sync_endpoint
        self.synapse_analytics_endpoint = synapse_analytics_endpoint
        # Please keep the suffixes in alphabetical order

    def __getattribute__(self, name):
        val = object.__getattribute__(self, name)
        if val is None:
            raise Exception("The suffix '{}' for this cloud "
                            "is not set but is used.\n"
                            "{} may be corrupt or invalid.\nResolve the error or delete this file "
                            "and try again.".format(name, CLOUD_CONFIG_FILE))
        return val


class Cloud:  # pylint: disable=too-few-public-methods
    """ Represents an Azure Cloud instance """

    def __init__(self,
                 name,
                 endpoints=None,
                 suffixes=None,
                 profile=None,
                 is_active=False):
        self.name = name
        self.endpoints = endpoints or CloudEndpoints()
        self.suffixes = suffixes or CloudSuffixes()
        self.profile = profile
        self.is_active = is_active


    def __str__(self):
        o = {
            'profile': self.profile,
            'name': self.name,
            'is_active': self.is_active,
            'endpoints': vars(self.endpoints),
            'suffixes': vars(self.suffixes),
        }
        return pformat(o)

    def to_json(self):
        return {'name': self.name, "endpoints": self.endpoints.__dict__, "suffixes": self.suffixes.__dict__}

    @classmethod
    def from_json(cls, json_str):
        return cls(json_str['name'],
                   endpoints=CloudEndpoints(**json_str['endpoints']),
                   suffixes=CloudSuffixes(**json_str['suffixes']))


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
        portal='https://portal.azure.com'),
    suffixes=CloudSuffixes(
        storage_endpoint='core.windows.net',
        storage_sync_endpoint='afs.azure.net',
        keyvault_dns='.vault.azure.net',
        mhsm_dns='.managedhsm.azure.net',
        sql_server_hostname='.database.windows.net',
        mysql_server_endpoint='.mysql.database.azure.com',
        postgresql_server_endpoint='.postgres.database.azure.com',
        mariadb_server_endpoint='.mariadb.database.azure.com',
        azure_datalake_store_file_system_endpoint='azuredatalakestore.net',
        azure_datalake_analytics_catalog_and_job_endpoint='azuredatalakeanalytics.net',
        acr_login_server_endpoint='.azurecr.io',
        synapse_analytics_endpoint='.dev.azuresynapse.net',
        attestation_endpoint='.attest.azure.net'))

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
        portal='https://portal.azure.cn'),
    suffixes=CloudSuffixes(
        storage_endpoint='core.chinacloudapi.cn',
        keyvault_dns='.vault.azure.cn',
        mhsm_dns='.managedhsm.azure.cn',
        sql_server_hostname='.database.chinacloudapi.cn',
        mysql_server_endpoint='.mysql.database.chinacloudapi.cn',
        postgresql_server_endpoint='.postgres.database.chinacloudapi.cn',
        mariadb_server_endpoint='.mariadb.database.chinacloudapi.cn',
        acr_login_server_endpoint='.azurecr.cn',
        synapse_analytics_endpoint='.dev.azuresynapse.azure.cn'))

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
        portal='https://portal.azure.us'),
    suffixes=CloudSuffixes(
        storage_endpoint='core.usgovcloudapi.net',
        storage_sync_endpoint='afs.azure.us',
        keyvault_dns='.vault.usgovcloudapi.net',
        mhsm_dns='.managedhsm.usgovcloudapi.net',
        sql_server_hostname='.database.usgovcloudapi.net',
        mysql_server_endpoint='.mysql.database.usgovcloudapi.net',
        postgresql_server_endpoint='.postgres.database.usgovcloudapi.net',
        mariadb_server_endpoint='.mariadb.database.usgovcloudapi.net',
        acr_login_server_endpoint='.azurecr.us',
        synapse_analytics_endpoint='.dev.azuresynapse.usgovcloudapi.net'))

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
        portal='https://portal.microsoftazure.de'),
    suffixes=CloudSuffixes(
        storage_endpoint='core.cloudapi.de',
        keyvault_dns='.vault.microsoftazure.de',
        mhsm_dns='.managedhsm.microsoftazure.de',
        sql_server_hostname='.database.cloudapi.de',
        mysql_server_endpoint='.mysql.database.cloudapi.de',
        postgresql_server_endpoint='.postgres.database.cloudapi.de',
        mariadb_server_endpoint='.mariadb.database.cloudapi.de'))

HARD_CODED_CLOUD_DICT = dict(AzureCloud=AZURE_PUBLIC_CLOUD,
                             AzureChinaCloud=AZURE_CHINA_CLOUD,
                             AzureUSGovernment=AZURE_US_GOV_CLOUD,
                             AzureGermanCloud=AZURE_GERMAN_CLOUD)
