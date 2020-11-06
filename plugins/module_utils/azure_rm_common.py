# Copyright (c) 2016 Matt Davis, <mdavis@ansible.com>
#                    Chris Houseknecht, <house@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import os
import re
import types
import copy
import inspect
import traceback
import json

try:
    from azure.graphrbac import GraphRbacManagementClient
except Exception:
    pass
from os.path import expanduser

from ansible.module_utils.basic import \
    AnsibleModule, missing_required_lib, env_fallback

try:
    from ansible.module_utils.ansible_release import __version__ as ANSIBLE_VERSION
except Exception:
    ANSIBLE_VERSION = 'unknown'
from ansible.module_utils.six.moves import configparser
import ansible.module_utils.six.moves.urllib.parse as urlparse

AZURE_COMMON_ARGS = dict(
    auth_source=dict(
        type='str',
        choices=['auto', 'cli', 'env', 'credential_file', 'msi'],
        fallback=(env_fallback, ['ANSIBLE_AZURE_AUTH_SOURCE']),
        default="auto"
    ),
    profile=dict(type='str'),
    subscription_id=dict(type='str'),
    client_id=dict(type='str', no_log=True),
    secret=dict(type='str', no_log=True),
    tenant=dict(type='str', no_log=True),
    ad_user=dict(type='str', no_log=True),
    password=dict(type='str', no_log=True),
    cloud_environment=dict(type='str', default='AzureCloud'),
    cert_validation_mode=dict(type='str', choices=['validate', 'ignore']),
    api_profile=dict(type='str', default='latest'),
    adfs_authority_url=dict(type='str', default=None)
)

AZURE_CREDENTIAL_ENV_MAPPING = dict(
    profile='AZURE_PROFILE',
    subscription_id='AZURE_SUBSCRIPTION_ID',
    client_id='AZURE_CLIENT_ID',
    secret='AZURE_SECRET',
    tenant='AZURE_TENANT',
    ad_user='AZURE_AD_USER',
    password='AZURE_PASSWORD',
    cloud_environment='AZURE_CLOUD_ENVIRONMENT',
    cert_validation_mode='AZURE_CERT_VALIDATION_MODE',
    adfs_authority_url='AZURE_ADFS_AUTHORITY_URL'
)


class SDKProfile(object):  # pylint: disable=too-few-public-methods

    def __init__(self, default_api_version, profile=None):
        """Constructor.

        :param str default_api_version: Default API version if not overridden by a profile. Nullable.
        :param profile: A dict operation group name to API version.
        :type profile: dict[str, str]
        """
        self.profile = profile if profile is not None else {}
        self.profile[None] = default_api_version

    @property
    def default_api_version(self):
        return self.profile[None]


# FUTURE: this should come from the SDK or an external location.
# For now, we have to copy from azure-cli
AZURE_API_PROFILES = {
    'latest': {
        'AuthorizationManagementClient': '2018-09-01-preview',
        'ContainerInstanceManagementClient': '2018-02-01-preview',
        'ComputeManagementClient': dict(
            default_api_version='2018-10-01',
            resource_skus='2018-10-01',
            disks='2018-06-01',
            snapshots='2018-10-01',
            virtual_machine_run_commands='2018-10-01'
        ),
        'NetworkManagementClient': '2019-06-01',
        'ResourceManagementClient': '2017-05-10',
        'StorageManagementClient': '2019-06-01',
        'SubscriptionClient': '2019-11-01',
        'WebSiteManagementClient': '2018-02-01',
        'PostgreSQLManagementClient': '2017-12-01',
        'MySQLManagementClient': '2017-12-01',
        'MariaDBManagementClient': '2019-03-01',
        'ManagementLockClient': '2016-09-01'
    },
    '2019-03-01-hybrid': {
        'StorageManagementClient': '2017-10-01',
        'NetworkManagementClient': '2017-10-01',
        'ComputeManagementClient': SDKProfile('2017-12-01', {
            'resource_skus': '2017-09-01',
            'disks': '2017-03-30',
            'snapshots': '2017-03-30'
        }),
        'ManagementLinkClient': '2016-09-01',
        'ManagementLockClient': '2016-09-01',
        'PolicyClient': '2016-12-01',
        'ResourceManagementClient': '2018-05-01',
        'SubscriptionClient': '2016-06-01',
        'DnsManagementClient': '2016-04-01',
        'KeyVaultManagementClient': '2016-10-01',
        'AuthorizationManagementClient': SDKProfile('2015-07-01', {
            'classic_administrators': '2015-06-01',
            'policy_assignments': '2016-12-01',
            'policy_definitions': '2016-12-01'
        }),
        'KeyVaultClient': '2016-10-01',
        'azure.multiapi.storage': '2017-11-09',
        'azure.multiapi.cosmosdb': '2017-04-17'
    },
    '2018-03-01-hybrid': {
        'StorageManagementClient': '2016-01-01',
        'NetworkManagementClient': '2017-10-01',
        'ComputeManagementClient': SDKProfile('2017-03-30'),
        'ManagementLinkClient': '2016-09-01',
        'ManagementLockClient': '2016-09-01',
        'PolicyClient': '2016-12-01',
        'ResourceManagementClient': '2018-02-01',
        'SubscriptionClient': '2016-06-01',
        'DnsManagementClient': '2016-04-01',
        'KeyVaultManagementClient': '2016-10-01',
        'AuthorizationManagementClient': SDKProfile('2015-07-01', {
            'classic_administrators': '2015-06-01'
        }),
        'KeyVaultClient': '2016-10-01',
        'azure.multiapi.storage': '2017-04-17',
        'azure.multiapi.cosmosdb': '2017-04-17'
    },
    '2017-03-09-profile': {
        'StorageManagementClient': '2016-01-01',
        'NetworkManagementClient': '2015-06-15',
        'ComputeManagementClient': SDKProfile('2016-03-30'),
        'ManagementLinkClient': '2016-09-01',
        'ManagementLockClient': '2015-01-01',
        'PolicyClient': '2015-10-01-preview',
        'ResourceManagementClient': '2016-02-01',
        'SubscriptionClient': '2016-06-01',
        'DnsManagementClient': '2016-04-01',
        'KeyVaultManagementClient': '2016-10-01',
        'AuthorizationManagementClient': SDKProfile('2015-07-01', {
            'classic_administrators': '2015-06-01'
        }),
        'KeyVaultClient': '2016-10-01',
        'azure.multiapi.storage': '2015-04-05'
    }
}

AZURE_TAG_ARGS = dict(
    tags=dict(type='dict'),
    append_tags=dict(type='bool', default=True),
)

AZURE_COMMON_REQUIRED_IF = [
    ('log_mode', 'file', ['log_path'])
]

ANSIBLE_USER_AGENT = 'Ansible/{0}'.format(ANSIBLE_VERSION)
CLOUDSHELL_USER_AGENT_KEY = 'AZURE_HTTP_USER_AGENT'
VSCODEEXT_USER_AGENT_KEY = 'VSCODEEXT_USER_AGENT'

CIDR_PATTERN = re.compile(r"(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1"
                          r"[0-9]{2}|2[0-4][0-9]|25[0-5])(/([0-9]|[1-2][0-9]|3[0-2]))")

AZURE_SUCCESS_STATE = "Succeeded"
AZURE_FAILED_STATE = "Failed"

HAS_AZURE = True
HAS_AZURE_EXC = None
HAS_AZURE_CLI_CORE = True
HAS_AZURE_CLI_CORE_EXC = None

HAS_MSRESTAZURE = True
HAS_MSRESTAZURE_EXC = None

try:
    import importlib
except ImportError:
    # This passes the sanity import test, but does not provide a user friendly error message.
    # Doing so would require catching Exception for all imports of Azure dependencies in modules and module_utils.
    importlib = None

try:
    from packaging.version import Version
    HAS_PACKAGING_VERSION = True
    HAS_PACKAGING_VERSION_EXC = None
except ImportError:
    Version = None
    HAS_PACKAGING_VERSION = False
    HAS_PACKAGING_VERSION_EXC = traceback.format_exc()

# NB: packaging issue sometimes cause msrestazure not to be installed, check it separately
try:
    from msrest.serialization import Serializer
except ImportError:
    HAS_MSRESTAZURE_EXC = traceback.format_exc()
    HAS_MSRESTAZURE = False

try:
    from enum import Enum
    from msrestazure.azure_active_directory import AADTokenCredentials
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_active_directory import MSIAuthentication
    from msrestazure.tools import parse_resource_id, resource_id, is_valid_resource_id
    from msrestazure import azure_cloud
    from azure.common.credentials import ServicePrincipalCredentials, UserPassCredentials
    from azure.mgmt.monitor.version import VERSION as monitor_client_version
    from azure.mgmt.network.version import VERSION as network_client_version
    from azure.mgmt.storage.version import VERSION as storage_client_version
    from azure.mgmt.compute.version import VERSION as compute_client_version
    from azure.mgmt.resource.version import VERSION as resource_client_version
    from azure.mgmt.dns.version import VERSION as dns_client_version
    from azure.mgmt.web.version import VERSION as web_client_version
    from azure.mgmt.network import NetworkManagementClient
    from azure.mgmt.resource.resources import ResourceManagementClient
    from azure.mgmt.resource.subscriptions import SubscriptionClient
    from azure.mgmt.storage import StorageManagementClient
    from azure.mgmt.compute import ComputeManagementClient
    from azure.mgmt.dns import DnsManagementClient
    from azure.mgmt.privatedns import PrivateDnsManagementClient
    import azure.mgmt.privatedns.models as PrivateDnsModels
    from azure.mgmt.monitor import MonitorManagementClient
    from azure.mgmt.web import WebSiteManagementClient
    from azure.mgmt.containerservice import ContainerServiceClient
    from azure.mgmt.marketplaceordering import MarketplaceOrderingAgreements
    from azure.mgmt.trafficmanager import TrafficManagerManagementClient
    from azure.storage.cloudstorageaccount import CloudStorageAccount
    from azure.storage.blob import PageBlobService, BlockBlobService
    from adal.authentication_context import AuthenticationContext
    from azure.mgmt.authorization import AuthorizationManagementClient
    from azure.mgmt.sql import SqlManagementClient
    from azure.mgmt.servicebus import ServiceBusManagementClient
    import azure.mgmt.servicebus.models as ServicebusModel
    from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
    from azure.mgmt.rdbms.mysql import MySQLManagementClient
    from azure.mgmt.rdbms.mariadb import MariaDBManagementClient
    from azure.mgmt.containerregistry import ContainerRegistryManagementClient
    from azure.mgmt.containerinstance import ContainerInstanceManagementClient
    from azure.mgmt.loganalytics import LogAnalyticsManagementClient
    import azure.mgmt.loganalytics.models as LogAnalyticsModels
    from azure.mgmt.automation import AutomationClient
    import azure.mgmt.automation.models as AutomationModel
    from azure.mgmt.iothub import IotHubClient
    from azure.mgmt.iothub import models as IoTHubModels
    from msrest.service_client import ServiceClient
    from msrestazure import AzureConfiguration
    from msrest.authentication import Authentication
    from azure.mgmt.resource.locks import ManagementLockClient
except ImportError as exc:
    Authentication = object
    HAS_AZURE_EXC = traceback.format_exc()
    HAS_AZURE = False

from base64 import b64encode, b64decode
from hashlib import sha256
from hmac import HMAC
from time import time

try:
    from urllib import (urlencode, quote_plus)
except ImportError:
    from urllib.parse import (urlencode, quote_plus)

try:
    from azure.cli.core.util import CLIError
    from azure.common.credentials import get_cli_profile
    from azure.common.cloud import get_cli_active_cloud
except ImportError:
    HAS_AZURE_CLI_CORE = False
    HAS_AZURE_CLI_CORE_EXC = None
    CLIError = Exception


def azure_id_to_dict(id):
    pieces = re.sub(r'^\/', '', id).split('/')
    result = {}
    index = 0
    while index < len(pieces) - 1:
        result[pieces[index]] = pieces[index + 1]
        index += 1
    return result


def format_resource_id(val, subscription_id, namespace, types, resource_group):
    return resource_id(name=val,
                       resource_group=resource_group,
                       namespace=namespace,
                       type=types,
                       subscription=subscription_id) if not is_valid_resource_id(val) else val


def normalize_location_name(name):
    return name.replace(' ', '').lower()


# FUTURE: either get this from the requirements file (if we can be sure it's always available at runtime)
# or generate the requirements files from this so we only have one source of truth to maintain...
AZURE_PKG_VERSIONS = {
    'StorageManagementClient': {
        'package_name': 'storage',
        'expected_version': '11.1.0'
    },
    'ComputeManagementClient': {
        'package_name': 'compute',
        'expected_version': '4.4.0'
    },
    'ContainerInstanceManagementClient': {
        'package_name': 'containerinstance',
        'expected_version': '0.4.0'
    },
    'NetworkManagementClient': {
        'package_name': 'network',
        'expected_version': '2.3.0'
    },
    'ResourceManagementClient': {
        'package_name': 'resource',
        'expected_version': '2.1.0'
    },
    'DnsManagementClient': {
        'package_name': 'dns',
        'expected_version': '2.1.0'
    },
    'PrivateDnsManagementClient': {
        'package_name': 'privatedns',
        'expected_version': '0.1.0'
    },
    'WebSiteManagementClient': {
        'package_name': 'web',
        'expected_version': '0.41.0'
    },
    'TrafficManagerManagementClient': {
        'package_name': 'trafficmanager',
        'expected_version': '0.50.0'
    },
} if HAS_AZURE else {}


AZURE_MIN_RELEASE = '2.0.0'


class AzureRMModuleBase(object):
    def __init__(self, derived_arg_spec, bypass_checks=False, no_log=False,
                 check_invalid_arguments=None, mutually_exclusive=None, required_together=None,
                 required_one_of=None, add_file_common_args=False, supports_check_mode=False,
                 required_if=None, supports_tags=True, facts_module=False, skip_exec=False, is_ad_resource=False):

        merged_arg_spec = dict()
        merged_arg_spec.update(AZURE_COMMON_ARGS)
        if supports_tags:
            merged_arg_spec.update(AZURE_TAG_ARGS)

        if derived_arg_spec:
            merged_arg_spec.update(derived_arg_spec)

        merged_required_if = list(AZURE_COMMON_REQUIRED_IF)
        if required_if:
            merged_required_if += required_if

        self.module = AnsibleModule(argument_spec=merged_arg_spec,
                                    bypass_checks=bypass_checks,
                                    no_log=no_log,
                                    mutually_exclusive=mutually_exclusive,
                                    required_together=required_together,
                                    required_one_of=required_one_of,
                                    add_file_common_args=add_file_common_args,
                                    supports_check_mode=supports_check_mode,
                                    required_if=merged_required_if)

        if not HAS_PACKAGING_VERSION:
            self.fail(msg=missing_required_lib('packaging'),
                      exception=HAS_PACKAGING_VERSION_EXC)

        if not HAS_MSRESTAZURE:
            self.fail(msg=missing_required_lib('msrestazure'),
                      exception=HAS_MSRESTAZURE_EXC)

        if not HAS_AZURE:
            self.fail(msg=missing_required_lib('ansible[azure] (azure >= {0})'.format(AZURE_MIN_RELEASE)),
                      exception=HAS_AZURE_EXC)

        self._authorization_client = None
        self._network_client = None
        self._storage_client = None
        self._subscription_client = None
        self._resource_client = None
        self._compute_client = None
        self._dns_client = None
        self._private_dns_client = None
        self._web_client = None
        self._marketplace_client = None
        self._sql_client = None
        self._mysql_client = None
        self._mariadb_client = None
        self._postgresql_client = None
        self._containerregistry_client = None
        self._containerinstance_client = None
        self._containerservice_client = None
        self._managedcluster_client = None
        self._traffic_manager_management_client = None
        self._monitor_client = None
        self._resource = None
        self._log_analytics_client = None
        self._servicebus_client = None
        self._automation_client = None
        self._IoThub_client = None
        self._lock_client = None

        self.check_mode = self.module.check_mode
        self.api_profile = self.module.params.get('api_profile')
        self.facts_module = facts_module
        # self.debug = self.module.params.get('debug')

        # delegate auth to AzureRMAuth class (shared with all plugin types)
        self.azure_auth = AzureRMAuth(fail_impl=self.fail, is_ad_resource=is_ad_resource, **self.module.params)

        # common parameter validation
        if self.module.params.get('tags'):
            self.validate_tags(self.module.params['tags'])

        if not skip_exec:
            res = self.exec_module(**self.module.params)
            self.module.exit_json(**res)

    def check_client_version(self, client_type):
        # Ensure Azure modules are at least 2.0.0rc5.
        package_version = AZURE_PKG_VERSIONS.get(client_type.__name__, None)
        if package_version is not None:
            client_name = package_version.get('package_name')
            try:
                client_module = importlib.import_module(client_type.__module__)
                client_version = client_module.VERSION
            except (RuntimeError, AttributeError):
                # can't get at the module version for some reason, just fail silently...
                return
            expected_version = package_version.get('expected_version')
            if Version(client_version) < Version(expected_version):
                self.fail("Installed azure-mgmt-{0} client version is {1}. The minimum supported version is {2}. Try "
                          "`pip install ansible[azure]`".format(client_name, client_version, expected_version))
            if Version(client_version) != Version(expected_version):
                self.module.warn("Installed azure-mgmt-{0} client version is {1}. The expected version is {2}. Try "
                                 "`pip install ansible[azure]`".format(client_name, client_version, expected_version))

    def exec_module(self, **kwargs):
        self.fail("Error: {0} failed to implement exec_module method.".format(self.__class__.__name__))

    def fail(self, msg, **kwargs):
        '''
        Shortcut for calling module.fail()

        :param msg: Error message text.
        :param kwargs: Any key=value pairs
        :return: None
        '''
        self.module.fail_json(msg=msg, **kwargs)

    def deprecate(self, msg, version=None):
        self.module.deprecate(msg, version)

    def log(self, msg, pretty_print=False):
        if pretty_print:
            self.module.debug(json.dumps(msg, indent=4, sort_keys=True))
        else:
            self.module.debug(msg)

    def validate_tags(self, tags):
        '''
        Check if tags dictionary contains string:string pairs.

        :param tags: dictionary of string:string pairs
        :return: None
        '''
        if not self.facts_module:
            if not isinstance(tags, dict):
                self.fail("Tags must be a dictionary of string:string values.")
            for key, value in tags.items():
                if not isinstance(value, str):
                    self.fail("Tags values must be strings. Found {0}:{1}".format(str(key), str(value)))

    def update_tags(self, tags):
        '''
        Call from the module to update metadata tags. Returns tuple
        with bool indicating if there was a change and dict of new
        tags to assign to the object.

        :param tags: metadata tags from the object
        :return: bool, dict
        '''
        tags = tags or dict()
        new_tags = copy.copy(tags) if isinstance(tags, dict) else dict()
        param_tags = self.module.params.get('tags') if isinstance(self.module.params.get('tags'), dict) else dict()
        append_tags = self.module.params.get('append_tags') if self.module.params.get('append_tags') is not None else True
        changed = False
        # check add or update
        for key, value in param_tags.items():
            if not new_tags.get(key) or new_tags[key] != value:
                changed = True
                new_tags[key] = value
        # check remove
        if not append_tags:
            for key, value in tags.items():
                if not param_tags.get(key):
                    new_tags.pop(key)
                    changed = True
        return changed, new_tags

    def has_tags(self, obj_tags, tag_list):
        '''
        Used in fact modules to compare object tags to list of parameter tags. Return true if list of parameter tags
        exists in object tags.

        :param obj_tags: dictionary of tags from an Azure object.
        :param tag_list: list of tag keys or tag key:value pairs
        :return: bool
        '''

        if not obj_tags and tag_list:
            return False

        if not tag_list:
            return True

        matches = 0
        result = False
        for tag in tag_list:
            tag_key = tag
            tag_value = None
            if ':' in tag:
                tag_key, tag_value = tag.split(':')
            if tag_value and obj_tags.get(tag_key) == tag_value:
                matches += 1
            elif not tag_value and obj_tags.get(tag_key):
                matches += 1
        if matches == len(tag_list):
            result = True
        return result

    def get_resource_group(self, resource_group):
        '''
        Fetch a resource group.

        :param resource_group: name of a resource group
        :return: resource group object
        '''
        try:
            return self.rm_client.resource_groups.get(resource_group)
        except CloudError as cloud_error:
            self.fail("Error retrieving resource group {0} - {1}".format(resource_group, cloud_error.message))
        except Exception as exc:
            self.fail("Error retrieving resource group {0} - {1}".format(resource_group, str(exc)))

    def parse_resource_to_dict(self, resource):
        '''
        Return a dict of the give resource, which contains name and resource group.

        :param resource: It can be a resource name, id or a dict contains name and resource group.
        '''
        resource_dict = parse_resource_id(resource) if not isinstance(resource, dict) else resource
        resource_dict['resource_group'] = resource_dict.get('resource_group', self.resource_group)
        resource_dict['subscription_id'] = resource_dict.get('subscription_id', self.subscription_id)
        return resource_dict

    def serialize_obj(self, obj, class_name, enum_modules=None):
        '''
        Return a JSON representation of an Azure object.

        :param obj: Azure object
        :param class_name: Name of the object's class
        :param enum_modules: List of module names to build enum dependencies from.
        :return: serialized result
        '''
        enum_modules = [] if enum_modules is None else enum_modules

        dependencies = dict()
        if enum_modules:
            for module_name in enum_modules:
                mod = importlib.import_module(module_name)
                for mod_class_name, mod_class_obj in inspect.getmembers(mod, predicate=inspect.isclass):
                    dependencies[mod_class_name] = mod_class_obj
            self.log("dependencies: ")
            self.log(str(dependencies))
        serializer = Serializer(classes=dependencies)
        return serializer.body(obj, class_name, keep_readonly=True)

    def get_poller_result(self, poller, wait=5):
        '''
        Consistent method of waiting on and retrieving results from Azure's long poller

        :param poller Azure poller object
        :return object resulting from the original request
        '''
        try:
            delay = wait
            while not poller.done():
                self.log("Waiting for {0} sec".format(delay))
                poller.wait(timeout=delay)
            return poller.result()
        except Exception as exc:
            self.log(str(exc))
            raise

    def check_provisioning_state(self, azure_object, requested_state='present'):
        '''
        Check an Azure object's provisioning state. If something did not complete the provisioning
        process, then we cannot operate on it.

        :param azure_object An object such as a subnet, storageaccount, etc. Must have provisioning_state
                            and name attributes.
        :return None
        '''

        if hasattr(azure_object, 'properties') and hasattr(azure_object.properties, 'provisioning_state') and \
           hasattr(azure_object, 'name'):
            # resource group object fits this model
            if isinstance(azure_object.properties.provisioning_state, Enum):
                if azure_object.properties.provisioning_state.value != AZURE_SUCCESS_STATE and \
                   requested_state != 'absent':
                    self.fail("Error {0} has a provisioning state of {1}. Expecting state to be {2}.".format(
                              azure_object.name, azure_object.properties.provisioning_state, AZURE_SUCCESS_STATE))
                return
            if azure_object.properties.provisioning_state != AZURE_SUCCESS_STATE and \
               requested_state != 'absent':
                self.fail("Error {0} has a provisioning state of {1}. Expecting state to be {2}.".format(
                    azure_object.name, azure_object.properties.provisioning_state, AZURE_SUCCESS_STATE))
            return

        if hasattr(azure_object, 'provisioning_state') or not hasattr(azure_object, 'name'):
            if isinstance(azure_object.provisioning_state, Enum):
                if azure_object.provisioning_state.value != AZURE_SUCCESS_STATE and requested_state != 'absent':
                    self.fail("Error {0} has a provisioning state of {1}. Expecting state to be {2}.".format(
                        azure_object.name, azure_object.provisioning_state, AZURE_SUCCESS_STATE))
                return
            if azure_object.provisioning_state != AZURE_SUCCESS_STATE and requested_state != 'absent':
                self.fail("Error {0} has a provisioning state of {1}. Expecting state to be {2}.".format(
                    azure_object.name, azure_object.provisioning_state, AZURE_SUCCESS_STATE))

    def get_blob_client(self, resource_group_name, storage_account_name, storage_blob_type='block'):
        keys = dict()
        try:
            # Get keys from the storage account
            self.log('Getting keys')
            account_keys = self.storage_client.storage_accounts.list_keys(resource_group_name, storage_account_name)
        except Exception as exc:
            self.fail("Error getting keys for account {0} - {1}".format(storage_account_name, str(exc)))

        try:
            self.log('Create blob service')
            if storage_blob_type == 'page':
                return PageBlobService(endpoint_suffix=self._cloud_environment.suffixes.storage_endpoint,
                                       account_name=storage_account_name,
                                       account_key=account_keys.keys[0].value)
            elif storage_blob_type == 'block':
                return BlockBlobService(endpoint_suffix=self._cloud_environment.suffixes.storage_endpoint,
                                        account_name=storage_account_name,
                                        account_key=account_keys.keys[0].value)
            else:
                raise Exception("Invalid storage blob type defined.")
        except Exception as exc:
            self.fail("Error creating blob service client for storage account {0} - {1}".format(storage_account_name,
                                                                                                str(exc)))

    def create_default_pip(self, resource_group, location, public_ip_name, allocation_method='Dynamic', sku=None):
        '''
        Create a default public IP address <public_ip_name> to associate with a network interface.
        If a PIP address matching <public_ip_name> exists, return it. Otherwise, create one.

        :param resource_group: name of an existing resource group
        :param location: a valid azure location
        :param public_ip_name: base name to assign the public IP address
        :param allocation_method: one of 'Static' or 'Dynamic'
        :param sku: sku
        :return: PIP object
        '''
        pip = None

        self.log("Starting create_default_pip {0}".format(public_ip_name))
        self.log("Check to see if public IP {0} exists".format(public_ip_name))
        try:
            pip = self.network_client.public_ip_addresses.get(resource_group, public_ip_name)
        except CloudError:
            pass

        if pip:
            self.log("Public ip {0} found.".format(public_ip_name))
            self.check_provisioning_state(pip)
            return pip

        params = self.network_models.PublicIPAddress(
            location=location,
            public_ip_allocation_method=allocation_method,
            sku=sku
        )
        self.log('Creating default public IP {0}'.format(public_ip_name))
        try:
            poller = self.network_client.public_ip_addresses.create_or_update(resource_group, public_ip_name, params)
        except Exception as exc:
            self.fail("Error creating {0} - {1}".format(public_ip_name, str(exc)))

        return self.get_poller_result(poller)

    def create_default_securitygroup(self, resource_group, location, security_group_name, os_type, open_ports):
        '''
        Create a default security group <security_group_name> to associate with a network interface. If a security group matching
        <security_group_name> exists, return it. Otherwise, create one.

        :param resource_group: Resource group name
        :param location: azure location name
        :param security_group_name: base name to use for the security group
        :param os_type: one of 'Windows' or 'Linux'. Determins any default rules added to the security group.
        :param ssh_port: for os_type 'Linux' port used in rule allowing SSH access.
        :param rdp_port: for os_type 'Windows' port used in rule allowing RDP access.
        :return: security_group object
        '''
        group = None

        self.log("Create security group {0}".format(security_group_name))
        self.log("Check to see if security group {0} exists".format(security_group_name))
        try:
            group = self.network_client.network_security_groups.get(resource_group, security_group_name)
        except CloudError:
            pass

        if group:
            self.log("Security group {0} found.".format(security_group_name))
            self.check_provisioning_state(group)
            return group

        parameters = self.network_models.NetworkSecurityGroup()
        parameters.location = location

        if not open_ports:
            # Open default ports based on OS type
            if os_type == 'Linux':
                # add an inbound SSH rule
                parameters.security_rules = [
                    self.network_models.SecurityRule(protocol='Tcp',
                                                     source_address_prefix='*',
                                                     destination_address_prefix='*',
                                                     access='Allow',
                                                     direction='Inbound',
                                                     description='Allow SSH Access',
                                                     source_port_range='*',
                                                     destination_port_range='22',
                                                     priority=100,
                                                     name='SSH')
                ]
                parameters.location = location
            else:
                # for windows add inbound RDP and WinRM rules
                parameters.security_rules = [
                    self.network_models.SecurityRule(protocol='Tcp',
                                                     source_address_prefix='*',
                                                     destination_address_prefix='*',
                                                     access='Allow',
                                                     direction='Inbound',
                                                     description='Allow RDP port 3389',
                                                     source_port_range='*',
                                                     destination_port_range='3389',
                                                     priority=100,
                                                     name='RDP01'),
                    self.network_models.SecurityRule(protocol='Tcp',
                                                     source_address_prefix='*',
                                                     destination_address_prefix='*',
                                                     access='Allow',
                                                     direction='Inbound',
                                                     description='Allow WinRM HTTPS port 5986',
                                                     source_port_range='*',
                                                     destination_port_range='5986',
                                                     priority=101,
                                                     name='WinRM01'),
                ]
        else:
            # Open custom ports
            parameters.security_rules = []
            priority = 100
            for port in open_ports:
                priority += 1
                rule_name = "Rule_{0}".format(priority)
                parameters.security_rules.append(
                    self.network_models.SecurityRule(protocol='Tcp',
                                                     source_address_prefix='*',
                                                     destination_address_prefix='*',
                                                     access='Allow',
                                                     direction='Inbound',
                                                     source_port_range='*',
                                                     destination_port_range=str(port),
                                                     priority=priority,
                                                     name=rule_name)
                )

        self.log('Creating default security group {0}'.format(security_group_name))
        try:
            poller = self.network_client.network_security_groups.create_or_update(resource_group,
                                                                                  security_group_name,
                                                                                  parameters)
        except Exception as exc:
            self.fail("Error creating default security rule {0} - {1}".format(security_group_name, str(exc)))

        return self.get_poller_result(poller)

    @staticmethod
    def _validation_ignore_callback(session, global_config, local_config, **kwargs):
        session.verify = False

    def get_api_profile(self, client_type_name, api_profile_name):
        profile_all_clients = AZURE_API_PROFILES.get(api_profile_name)

        if not profile_all_clients:
            raise KeyError("unknown Azure API profile: {0}".format(api_profile_name))

        profile_raw = profile_all_clients.get(client_type_name, None)

        if not profile_raw:
            self.module.warn("Azure API profile {0} does not define an entry for {1}".format(api_profile_name, client_type_name))

        if isinstance(profile_raw, dict):
            if not profile_raw.get('default_api_version'):
                raise KeyError("Azure API profile {0} does not define 'default_api_version'".format(api_profile_name))
            return profile_raw

        # wrap basic strings in a dict that just defines the default
        return dict(default_api_version=profile_raw)

    def get_graphrbac_client(self, tenant_id):
        cred = self.azure_auth.azure_credentials
        base_url = self.azure_auth._cloud_environment.endpoints.active_directory_graph_resource_id
        client = GraphRbacManagementClient(cred, tenant_id, base_url)

        return client

    def get_mgmt_svc_client(self, client_type, base_url=None, api_version=None, suppress_subscription_id=False):
        self.log('Getting management service client {0}'.format(client_type.__name__))
        self.check_client_version(client_type)

        client_argspec = inspect.getargspec(client_type.__init__)

        if not base_url:
            # most things are resource_manager, don't make everyone specify
            base_url = self.azure_auth._cloud_environment.endpoints.resource_manager

        # Some management clients do not take a subscription ID as parameters.
        if suppress_subscription_id:
            client_kwargs = dict(credentials=self.azure_auth.azure_credentials, base_url=base_url)
        else:
            client_kwargs = dict(credentials=self.azure_auth.azure_credentials, subscription_id=self.azure_auth.subscription_id, base_url=base_url)

        api_profile_dict = {}

        if self.api_profile:
            api_profile_dict = self.get_api_profile(client_type.__name__, self.api_profile)

        # unversioned clients won't accept profile; only send it if necessary
        # clients without a version specified in the profile will use the default
        if api_profile_dict and 'profile' in client_argspec.args:
            client_kwargs['profile'] = api_profile_dict

        # If the client doesn't accept api_version, it's unversioned.
        # If it does, favor explicitly-specified api_version, fall back to api_profile
        if 'api_version' in client_argspec.args:
            profile_default_version = api_profile_dict.get('default_api_version', None)
            if api_version or profile_default_version:
                client_kwargs['api_version'] = api_version or profile_default_version
                if 'profile' in client_kwargs:
                    # remove profile; only pass API version if specified
                    client_kwargs.pop('profile')

        client = client_type(**client_kwargs)

        # FUTURE: remove this once everything exposes models directly (eg, containerinstance)
        try:
            getattr(client, "models")
        except AttributeError:
            def _ansible_get_models(self, *arg, **kwarg):
                return self._ansible_models

            setattr(client, '_ansible_models', importlib.import_module(client_type.__module__).models)
            client.models = types.MethodType(_ansible_get_models, client)

        client.config = self.add_user_agent(client.config)

        if self.azure_auth._cert_validation_mode == 'ignore':
            client.config.session_configuration_callback = self._validation_ignore_callback

        return client

    def add_user_agent(self, config):
        # Add user agent for Ansible
        config.add_user_agent(ANSIBLE_USER_AGENT)
        # Add user agent when running from Cloud Shell
        if CLOUDSHELL_USER_AGENT_KEY in os.environ:
            config.add_user_agent(os.environ[CLOUDSHELL_USER_AGENT_KEY])
        # Add user agent when running from VSCode extension
        if VSCODEEXT_USER_AGENT_KEY in os.environ:
            config.add_user_agent(os.environ[VSCODEEXT_USER_AGENT_KEY])
        return config

    def generate_sas_token(self, **kwags):
        base_url = kwags.get('base_url', None)
        expiry = kwags.get('expiry', time() + 3600)
        key = kwags.get('key', None)
        policy = kwags.get('policy', None)
        url = quote_plus(base_url)
        ttl = int(expiry)
        sign_key = '{0}\n{1}'.format(url, ttl)
        signature = b64encode(HMAC(b64decode(key), sign_key.encode('utf-8'), sha256).digest())
        result = {
            'sr': url,
            'sig': signature,
            'se': str(ttl),
        }
        if policy:
            result['skn'] = policy
        return 'SharedAccessSignature ' + urlencode(result)

    def get_data_svc_client(self, **kwags):
        url = kwags.get('base_url', None)
        config = AzureConfiguration(base_url='https://{0}'.format(url))
        config.credentials = AzureSASAuthentication(token=self.generate_sas_token(**kwags))
        config = self.add_user_agent(config)
        return ServiceClient(creds=config.credentials, config=config)

    # passthru methods to AzureAuth instance for backcompat
    @property
    def credentials(self):
        return self.azure_auth.credentials

    @property
    def _cloud_environment(self):
        return self.azure_auth._cloud_environment

    @property
    def subscription_id(self):
        return self.azure_auth.subscription_id

    @property
    def storage_client(self):
        self.log('Getting storage client...')
        if not self._storage_client:
            self._storage_client = self.get_mgmt_svc_client(StorageManagementClient,
                                                            base_url=self._cloud_environment.endpoints.resource_manager,
                                                            api_version='2019-06-01')
        return self._storage_client

    @property
    def storage_models(self):
        return StorageManagementClient.models("2019-06-01")

    @property
    def authorization_client(self):
        self.log('Getting authorization client...')
        if not self._authorization_client:
            self._authorization_client = self.get_mgmt_svc_client(AuthorizationManagementClient,
                                                                  base_url=self._cloud_environment.endpoints.resource_manager,
                                                                  api_version='2018-09-01-preview')
        return self._authorization_client

    @property
    def authorization_models(self):
        return AuthorizationManagementClient.models('2018-09-01-preview')

    @property
    def subscription_client(self):
        self.log('Getting subscription client...')
        if not self._subscription_client:
            self._subscription_client = self.get_mgmt_svc_client(SubscriptionClient,
                                                                 base_url=self._cloud_environment.endpoints.resource_manager,
                                                                 suppress_subscription_id=True,
                                                                 api_version='2019-11-01')
        return self._subscription_client

    @property
    def subscription_models(self):
        return SubscriptionClient.models("2019-11-01")

    @property
    def network_client(self):
        self.log('Getting network client')
        if not self._network_client:
            self._network_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                            base_url=self._cloud_environment.endpoints.resource_manager,
                                                            api_version='2019-06-01')
        return self._network_client

    @property
    def network_models(self):
        self.log("Getting network models...")
        return NetworkManagementClient.models("2019-06-01")

    @property
    def rm_client(self):
        self.log('Getting resource manager client')
        if not self._resource_client:
            self._resource_client = self.get_mgmt_svc_client(ResourceManagementClient,
                                                             base_url=self._cloud_environment.endpoints.resource_manager,
                                                             api_version='2017-05-10')
        return self._resource_client

    @property
    def rm_models(self):
        self.log("Getting resource manager models")
        return ResourceManagementClient.models("2017-05-10")

    @property
    def compute_client(self):
        self.log('Getting compute client')
        if not self._compute_client:
            self._compute_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                            base_url=self._cloud_environment.endpoints.resource_manager,
                                                            api_version='2019-07-01')
        return self._compute_client

    @property
    def compute_models(self):
        self.log("Getting compute models")
        return ComputeManagementClient.models("2019-07-01")

    @property
    def dns_client(self):
        self.log('Getting dns client')
        if not self._dns_client:
            self._dns_client = self.get_mgmt_svc_client(DnsManagementClient,
                                                        base_url=self._cloud_environment.endpoints.resource_manager,
                                                        api_version='2018-05-01')
        return self._dns_client

    @property
    def dns_models(self):
        self.log("Getting dns models...")
        return DnsManagementClient.models('2018-05-01')

    @property
    def private_dns_client(self):
        self.log('Getting private dns client')
        if not self._private_dns_client:
            self._private_dns_client = self.get_mgmt_svc_client(
                PrivateDnsManagementClient,
                base_url=self._cloud_environment.endpoints.resource_manager)
        return self._private_dns_client

    @property
    def private_dns_models(self):
        self.log('Getting private dns models')
        return PrivateDnsModels

    @property
    def web_client(self):
        self.log('Getting web client')
        if not self._web_client:
            self._web_client = self.get_mgmt_svc_client(WebSiteManagementClient,
                                                        base_url=self._cloud_environment.endpoints.resource_manager,
                                                        api_version='2018-02-01')
        return self._web_client

    @property
    def containerservice_client(self):
        self.log('Getting container service client')
        if not self._containerservice_client:
            self._containerservice_client = self.get_mgmt_svc_client(ContainerServiceClient,
                                                                     base_url=self._cloud_environment.endpoints.resource_manager,
                                                                     api_version='2017-07-01')
        return self._containerservice_client

    @property
    def managedcluster_models(self):
        self.log("Getting container service models")
        return ContainerServiceClient.models('2019-04-01')

    @property
    def managedcluster_client(self):
        self.log('Getting container service client')
        if not self._managedcluster_client:
            self._managedcluster_client = self.get_mgmt_svc_client(ContainerServiceClient,
                                                                   base_url=self._cloud_environment.endpoints.resource_manager,
                                                                   api_version='2019-04-01')
        return self._managedcluster_client

    @property
    def sql_client(self):
        self.log('Getting SQL client')
        if not self._sql_client:
            self._sql_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                        base_url=self._cloud_environment.endpoints.resource_manager)
        return self._sql_client

    @property
    def postgresql_client(self):
        self.log('Getting PostgreSQL client')
        if not self._postgresql_client:
            self._postgresql_client = self.get_mgmt_svc_client(PostgreSQLManagementClient,
                                                               base_url=self._cloud_environment.endpoints.resource_manager)
        return self._postgresql_client

    @property
    def mysql_client(self):
        self.log('Getting MySQL client')
        if not self._mysql_client:
            self._mysql_client = self.get_mgmt_svc_client(MySQLManagementClient,
                                                          base_url=self._cloud_environment.endpoints.resource_manager)
        return self._mysql_client

    @property
    def mariadb_client(self):
        self.log('Getting MariaDB client')
        if not self._mariadb_client:
            self._mariadb_client = self.get_mgmt_svc_client(MariaDBManagementClient,
                                                            base_url=self._cloud_environment.endpoints.resource_manager)
        return self._mariadb_client

    @property
    def sql_client(self):
        self.log('Getting SQL client')
        if not self._sql_client:
            self._sql_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                        base_url=self._cloud_environment.endpoints.resource_manager)
        return self._sql_client

    @property
    def containerregistry_client(self):
        self.log('Getting container registry mgmt client')
        if not self._containerregistry_client:
            self._containerregistry_client = self.get_mgmt_svc_client(ContainerRegistryManagementClient,
                                                                      base_url=self._cloud_environment.endpoints.resource_manager,
                                                                      api_version='2017-10-01')

        return self._containerregistry_client

    @property
    def containerinstance_client(self):
        self.log('Getting container instance mgmt client')
        if not self._containerinstance_client:
            self._containerinstance_client = self.get_mgmt_svc_client(ContainerInstanceManagementClient,
                                                                      base_url=self._cloud_environment.endpoints.resource_manager,
                                                                      api_version='2018-06-01')

        return self._containerinstance_client

    @property
    def marketplace_client(self):
        self.log('Getting marketplace agreement client')
        if not self._marketplace_client:
            self._marketplace_client = self.get_mgmt_svc_client(MarketplaceOrderingAgreements,
                                                                base_url=self._cloud_environment.endpoints.resource_manager)
        return self._marketplace_client

    @property
    def traffic_manager_management_client(self):
        self.log('Getting traffic manager client')
        if not self._traffic_manager_management_client:
            self._traffic_manager_management_client = self.get_mgmt_svc_client(TrafficManagerManagementClient,
                                                                               base_url=self._cloud_environment.endpoints.resource_manager)
        return self._traffic_manager_management_client

    @property
    def monitor_client(self):
        self.log('Getting monitor client')
        if not self._monitor_client:
            self._monitor_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                            base_url=self._cloud_environment.endpoints.resource_manager)
        return self._monitor_client

    @property
    def log_analytics_client(self):
        self.log('Getting log analytics client')
        if not self._log_analytics_client:
            self._log_analytics_client = self.get_mgmt_svc_client(LogAnalyticsManagementClient,
                                                                  base_url=self._cloud_environment.endpoints.resource_manager)
        return self._log_analytics_client

    @property
    def log_analytics_models(self):
        self.log('Getting log analytics models')
        return LogAnalyticsModels

    @property
    def servicebus_client(self):
        self.log('Getting servicebus client')
        if not self._servicebus_client:
            self._servicebus_client = self.get_mgmt_svc_client(ServiceBusManagementClient,
                                                               base_url=self._cloud_environment.endpoints.resource_manager)
        return self._servicebus_client

    @property
    def servicebus_models(self):
        return ServicebusModel

    @property
    def automation_client(self):
        self.log('Getting automation client')
        if not self._automation_client:
            self._automation_client = self.get_mgmt_svc_client(AutomationClient,
                                                               base_url=self._cloud_environment.endpoints.resource_manager)
        return self._automation_client

    @property
    def automation_models(self):
        return AutomationModel

    @property
    def IoThub_client(self):
        self.log('Getting iothub client')
        if not self._IoThub_client:
            self._IoThub_client = self.get_mgmt_svc_client(IotHubClient,
                                                           base_url=self._cloud_environment.endpoints.resource_manager)
        return self._IoThub_client

    @property
    def IoThub_models(self):
        return IoTHubModels

    @property
    def automation_client(self):
        self.log('Getting automation client')
        if not self._automation_client:
            self._automation_client = self.get_mgmt_svc_client(AutomationClient,
                                                               base_url=self._cloud_environment.endpoints.resource_manager)
        return self._automation_client

    @property
    def automation_models(self):
        return AutomationModel

    @property
    def lock_client(self):
        self.log('Getting lock client')
        if not self._lock_client:
            self._lock_client = self.get_mgmt_svc_client(ManagementLockClient,
                                                         base_url=self._cloud_environment.endpoints.resource_manager,
                                                         api_version='2016-09-01')
        return self._lock_client

    @property
    def lock_models(self):
        self.log("Getting lock models")
        return ManagementLockClient.models('2016-09-01')


class AzureSASAuthentication(Authentication):
    """Simple SAS Authentication.
    An implementation of Authentication in
    https://github.com/Azure/msrest-for-python/blob/0732bc90bdb290e5f58c675ffdd7dbfa9acefc93/msrest/authentication.py

    :param str token: SAS token
    """
    def __init__(self, token):
        self.token = token

    def signed_session(self):
        session = super(AzureSASAuthentication, self).signed_session()
        session.headers['Authorization'] = self.token
        return session


class AzureRMAuthException(Exception):
    pass


class AzureRMAuth(object):
    _cloud_environment = None
    _adfs_authority_url = None

    def __init__(self, auth_source=None, profile=None, subscription_id=None, client_id=None, secret=None,
                 tenant=None, ad_user=None, password=None, cloud_environment='AzureCloud', cert_validation_mode='validate',
                 api_profile='latest', adfs_authority_url=None, fail_impl=None, is_ad_resource=False, **kwargs):

        if fail_impl:
            self._fail_impl = fail_impl
        else:
            self._fail_impl = self._default_fail_impl
        self.is_ad_resource = is_ad_resource

        # authenticate
        self.credentials = self._get_credentials(
            auth_source=auth_source,
            profile=profile,
            subscription_id=subscription_id,
            client_id=client_id,
            secret=secret,
            tenant=tenant,
            ad_user=ad_user,
            password=password,
            cloud_environment=cloud_environment,
            cert_validation_mode=cert_validation_mode,
            api_profile=api_profile,
            adfs_authority_url=adfs_authority_url)

        if not self.credentials:
            if HAS_AZURE_CLI_CORE:
                self.fail("Failed to get credentials. Either pass as parameters, set environment variables, "
                          "define a profile in ~/.azure/credentials, or log in with Azure CLI (`az login`).")
            else:
                self.fail("Failed to get credentials. Either pass as parameters, set environment variables, "
                          "define a profile in ~/.azure/credentials, or install Azure CLI and log in (`az login`).")

        # cert validation mode precedence: module-arg, credential profile, env, "validate"
        self._cert_validation_mode = cert_validation_mode or \
            self.credentials.get('cert_validation_mode') or \
            self._get_env('cert_validation_mode') or \
            'validate'

        if self._cert_validation_mode not in ['validate', 'ignore']:
            self.fail('invalid cert_validation_mode: {0}'.format(self._cert_validation_mode))

        # if cloud_environment specified, look up/build Cloud object
        raw_cloud_env = self.credentials.get('cloud_environment')
        if self.credentials.get('credentials') is not None and raw_cloud_env is not None:
            self._cloud_environment = raw_cloud_env
        elif not raw_cloud_env:
            self._cloud_environment = azure_cloud.AZURE_PUBLIC_CLOUD  # SDK default
        else:
            # try to look up "well-known" values via the name attribute on azure_cloud members
            all_clouds = [x[1] for x in inspect.getmembers(azure_cloud) if isinstance(x[1], azure_cloud.Cloud)]
            matched_clouds = [x for x in all_clouds if x.name == raw_cloud_env]
            if len(matched_clouds) == 1:
                self._cloud_environment = matched_clouds[0]
            elif len(matched_clouds) > 1:
                self.fail("Azure SDK failure: more than one cloud matched for cloud_environment name '{0}'".format(raw_cloud_env))
            else:
                if not urlparse.urlparse(raw_cloud_env).scheme:
                    self.fail("cloud_environment must be an endpoint discovery URL or one of {0}".format([x.name for x in all_clouds]))
                try:
                    self._cloud_environment = azure_cloud.get_cloud_from_metadata_endpoint(raw_cloud_env)
                except Exception as e:
                    self.fail("cloud_environment {0} could not be resolved: {1}".format(raw_cloud_env, e.message), exception=traceback.format_exc())

        if self.credentials.get('subscription_id', None) is None and self.credentials.get('credentials') is None:
            self.fail("Credentials did not include a subscription_id value.")
        self.log("setting subscription_id")
        self.subscription_id = self.credentials['subscription_id']

        # get authentication authority
        # for adfs, user could pass in authority or not.
        # for others, use default authority from cloud environment
        if self.credentials.get('adfs_authority_url') is None:
            self._adfs_authority_url = self._cloud_environment.endpoints.active_directory
        else:
            self._adfs_authority_url = self.credentials.get('adfs_authority_url')

        # get resource from cloud environment
        self._resource = self._cloud_environment.endpoints.active_directory_resource_id

        if self.credentials.get('credentials') is not None:
            # AzureCLI credentials
            self.azure_credentials = self.credentials['credentials']
        elif self.credentials.get('client_id') is not None and \
                self.credentials.get('secret') is not None and \
                self.credentials.get('tenant') is not None:
            self.azure_credentials = ServicePrincipalCredentials(client_id=self.credentials['client_id'],
                                                                 secret=self.credentials['secret'],
                                                                 tenant=self.credentials['tenant'],
                                                                 cloud_environment=self._cloud_environment,
                                                                 verify=self._cert_validation_mode == 'validate')

        elif self.credentials.get('ad_user') is not None and \
                self.credentials.get('password') is not None and \
                self.credentials.get('client_id') is not None and \
                self.credentials.get('tenant') is not None:

            self.azure_credentials = self.acquire_token_with_username_password(
                self._adfs_authority_url,
                self._resource,
                self.credentials['ad_user'],
                self.credentials['password'],
                self.credentials['client_id'],
                self.credentials['tenant'])

        elif self.credentials.get('ad_user') is not None and self.credentials.get('password') is not None:
            tenant = self.credentials.get('tenant')
            if not tenant:
                tenant = 'common'  # SDK default

            self.azure_credentials = UserPassCredentials(self.credentials['ad_user'],
                                                         self.credentials['password'],
                                                         tenant=tenant,
                                                         cloud_environment=self._cloud_environment,
                                                         verify=self._cert_validation_mode == 'validate')
        else:
            self.fail("Failed to authenticate with provided credentials. Some attributes were missing. "
                      "Credentials must include client_id, secret and tenant or ad_user and password, or "
                      "ad_user, password, client_id, tenant and adfs_authority_url(optional) for ADFS authentication, or "
                      "be logged in using AzureCLI.")

    def fail(self, msg, exception=None, **kwargs):
        self._fail_impl(msg)

    def _default_fail_impl(self, msg, exception=None, **kwargs):
        raise AzureRMAuthException(msg)

    def _get_env(self, module_key, default=None):
        "Read envvar matching module parameter"
        return os.environ.get(AZURE_CREDENTIAL_ENV_MAPPING[module_key], default)

    def _get_profile(self, profile="default"):
        path = expanduser("~/.azure/credentials")
        try:
            config = configparser.ConfigParser()
            config.read(path)
        except Exception as exc:
            self.fail("Failed to access {0}. Check that the file exists and you have read "
                      "access. {1}".format(path, str(exc)))
        credentials = dict()
        for key in AZURE_CREDENTIAL_ENV_MAPPING:
            try:
                credentials[key] = config.get(profile, key, raw=True)
            except Exception:
                pass

        if credentials.get('subscription_id'):
            return credentials

        return None

    def _get_msi_credentials(self, subscription_id=None, client_id=None, **kwargs):
        credentials = MSIAuthentication(client_id=client_id)
        subscription_id = subscription_id or self._get_env('subscription_id')
        if not subscription_id:
            try:
                # use the first subscription of the MSI
                subscription_client = SubscriptionClient(credentials)
                subscription = next(subscription_client.subscriptions.list())
                subscription_id = str(subscription.subscription_id)
            except Exception as exc:
                self.fail("Failed to get MSI token: {0}. "
                          "Please check whether your machine enabled MSI or grant access to any subscription.".format(str(exc)))
        return {
            'credentials': credentials,
            'subscription_id': subscription_id
        }

    def _get_azure_cli_credentials(self, subscription_id=None, resource=None):
        if self.is_ad_resource:
            resource = 'https://graph.windows.net/'
        subscription_id = subscription_id or self._get_env('subscription_id')
        profile = get_cli_profile()
        credentials, subscription_id, tenant = profile.get_login_credentials(
            subscription_id=subscription_id, resource=resource)
        cloud_environment = get_cli_active_cloud()

        cli_credentials = {
            'credentials': credentials,
            'subscription_id': subscription_id,
            'cloud_environment': cloud_environment
        }
        return cli_credentials

    def _get_env_credentials(self):
        env_credentials = dict()
        for attribute, env_variable in AZURE_CREDENTIAL_ENV_MAPPING.items():
            env_credentials[attribute] = os.environ.get(env_variable, None)

        if env_credentials['profile']:
            credentials = self._get_profile(env_credentials['profile'])
            return credentials

        if env_credentials.get('subscription_id') is not None:
            return env_credentials

        return None

    def _get_credentials(self, auth_source=None, **params):
        # Get authentication credentials.
        self.log('Getting credentials')

        arg_credentials = dict()
        for attribute, env_variable in AZURE_CREDENTIAL_ENV_MAPPING.items():
            arg_credentials[attribute] = params.get(attribute, None)

        if auth_source == 'msi':
            self.log('Retrieving credentials from MSI')
            return self._get_msi_credentials(subscription_id=params.get('subscription_id'), client_id=params.get('client_id'))

        if auth_source == 'cli':
            if not HAS_AZURE_CLI_CORE:
                self.fail(msg=missing_required_lib('azure-cli', reason='for `cli` auth_source'),
                          exception=HAS_AZURE_CLI_CORE_EXC)
            try:
                self.log('Retrieving credentials from Azure CLI profile')
                cli_credentials = self._get_azure_cli_credentials(subscription_id=params.get('subscription_id'))
                return cli_credentials
            except CLIError as err:
                self.fail("Azure CLI profile cannot be loaded - {0}".format(err))

        if auth_source == 'env':
            self.log('Retrieving credentials from environment')
            env_credentials = self._get_env_credentials()
            return env_credentials

        if auth_source == 'credential_file':
            self.log("Retrieving credentials from credential file")
            profile = params.get('profile') or 'default'
            default_credentials = self._get_profile(profile)
            return default_credentials

        # auto, precedence: module parameters -> environment variables -> default profile in ~/.azure/credentials -> azure cli
        # try module params
        if arg_credentials['profile'] is not None:
            self.log('Retrieving credentials with profile parameter.')
            credentials = self._get_profile(arg_credentials['profile'])
            return credentials

        if arg_credentials['client_id'] or arg_credentials['ad_user']:
            self.log('Received credentials from parameters.')
            return arg_credentials

        # try environment
        env_credentials = self._get_env_credentials()
        if env_credentials:
            self.log('Received credentials from env.')
            return env_credentials

        # try default profile from ~./azure/credentials
        default_credentials = self._get_profile()
        if default_credentials:
            self.log('Retrieved default profile credentials from ~/.azure/credentials.')
            return default_credentials

        try:
            if HAS_AZURE_CLI_CORE:
                self.log('Retrieving credentials from AzureCLI profile')
            cli_credentials = self._get_azure_cli_credentials(subscription_id=params.get('subscription_id'))
            return cli_credentials
        except CLIError as ce:
            self.log('Error getting AzureCLI profile credentials - {0}'.format(ce))

        return None

    def acquire_token_with_username_password(self, authority, resource, username, password, client_id, tenant):
        authority_uri = authority

        if tenant is not None:
            authority_uri = authority + '/' + tenant

        context = AuthenticationContext(authority_uri)
        token_response = context.acquire_token_with_username_password(resource, username, password, client_id)

        return AADTokenCredentials(token_response)

    def log(self, msg, pretty_print=False):
        pass
        # Use only during module development
        # if self.debug:
        #     log_file = open('azure_rm.log', 'a')
        #     if pretty_print:
        #         log_file.write(json.dumps(msg, indent=4, sort_keys=True))
        #     else:
        #         log_file.write(msg + u'\n')
