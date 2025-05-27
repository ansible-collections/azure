# Copyright (c) 2018 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
    name: azure_rm
    short_description: Azure Resource Manager inventory plugin
    options:
        batch_fetch_interval:
            description: Interval with which to check if the batched requests are completed
            default: 3
            type: int
        batch_fetch_timeout:
            description: The timeout to use when polling for batched requests
            default: 5
            type: int
    extends_documentation_fragment:
      - azure.azcollection.azure
      - azure.azcollection.azure_rm
      - constructed
      - inventory_cache
    description:
        - Query VM details from Azure Resource Manager
        - Requires a YAML configuration file whose name ends with 'azure_rm.(yml|yaml)'
        - By default, sets C(ansible_host) to the first public IP address found (preferring the primary NIC). If no
          public IPs are found, the first private IP (also preferring the primary NIC). The default may be overridden
          via C(hostvar_expressions); see examples.
'''

EXAMPLES = '''
# The following host variables are always available:
# public_ipv4_addresses: all public IP addresses, with the primary IP config from the primary NIC first
# public_dns_hostnames: all public DNS hostnames, with the primary IP config from the primary NIC first
# private_ipv4_addresses: all private IP addressses, with the primary IP config from the primary NIC first
# id: the VM's Azure resource ID, eg /subscriptions/00000000-0000-0000-1111-1111aaaabb/resourceGroups/my_rg/providers/Microsoft.Compute/virtualMachines/my_vm
# location: the VM's Azure location, eg 'westus', 'eastus'
# name: the VM's resource name, eg 'myvm'
# os_profile: The VM OS properties, a dictionary, only system is currently available, eg 'os_profile.system not in ['linux']'
# powerstate: the VM's current power state, eg: 'running', 'stopped', 'deallocated'
# provisioning_state: the VM's current provisioning state, eg: 'succeeded'
# tags: dictionary of the VM's defined tag values
# resource_type: the VM's resource type, eg: 'Microsoft.Compute/virtualMachine', 'Microsoft.Compute/virtualMachineScaleSets/virtualMachines',
# 'microsoft.azurestackhci/virtualmachineinstances'
# vmid: the VM's internal SMBIOS ID, eg: '36bca69d-c365-4584-8c06-a62f4a1dc5d2'
# vmss: if the VM is a member of a scaleset (vmss), a dictionary including the id and name of the parent scaleset
# availability_zone: availability zone in which VM is deployed, eg '1','2','3'
# creation_time: datetime object of when the VM was created, eg '2023-07-21T09:30:30.4710164+00:00'
#
# The following host variables are sometimes available:
# computer_name: the Operating System's hostname. Will not be available if azure agent is not available and picking it up.
# The following host variables are available for Azure Stack HCI vms:
# customLocation: the azure arc custom location.
# virtual_machine_memoryMB: RAM allowed (static)
# virtual_machine_processors: number of vCPUs


# sample 'myazuresub.azure_rm.yaml'

# required for all azure_rm inventory plugin configs
plugin: azure.azcollection.azure_rm

# forces this plugin to use a CLI auth session instead of the automatic auth source selection (eg, prevents the
# presence of 'ANSIBLE_AZURE_RM_X' environment variables from overriding CLI auth)
auth_source: cli

# fetches VMs from an explicit list of resource groups instead of default all (- '*')
include_vm_resource_groups:
    - myrg1
    - myrg2

# fetches VMs from VMSSs in all resource groups (defaults to no VMSS fetch)
include_vmss_resource_groups:
    - '*'

# fetches VMs from Azure StackHCI in specific resource groups (defaults to no HCI vm fetch)
include_hcivm_resource_groups:
    - myrg1

# fetches ARC hosts in specific resource groups (defaults to no ARC fetch)
include_arc_resource_groups:
    - myrg1

# places a host in the named group if the associated condition evaluates to true
conditional_groups:
    # since this will be true for every host, every host sourced from this inventory plugin config will be in the
    # group 'all_the_hosts'
    all_the_hosts: true
    # if the VM's "name" variable contains "dbserver", it will be placed in the 'db_hosts' group
    db_hosts: "'dbserver' in name"

# adds variables to each host found by this inventory plugin, whose values are the result of the associated expression
hostvar_expressions:
    my_host_var:
    # A statically-valued expression has to be both single and double-quoted, or use escaped quotes, since the outer
    # layer of quotes will be consumed by YAML. Without the second set of quotes, it interprets 'staticvalue' as a
    # variable instead of a string literal.
    some_statically_valued_var: "'staticvalue'"
    # overrides the default ansible_host value with a custom Jinja2 expression, in this case, the first DNS hostname, or
    # if none are found, the first public IP address.
    ansible_host: (public_dns_hostnames + public_ipv4_addresses) | first

# change how inventory_hostname is generated. Each item is a jinja2 expression similar to hostvar_expressions.
hostnames:
    - tags.vm_name
    - default_inventory_hostname + ".domain.tld" # Transfer to fqdn if you use shortnames for VMs
    - default  # special var that uses the default hashed name

# places hosts in dynamically-created groups based on a variable value.
keyed_groups:
# places each host in a group named 'tag_(tag name)_(tag value)' for each tag on a VM.
    - prefix: tag
      key: tags
# places each host in a group named 'azure_loc_(location name)', depending on the VM's location
    - prefix: azure_loc
      key: location
# places host in a group named 'some_tag_X' using the value of the 'sometag' tag on a VM as X, and defaulting to the
# value 'none' (eg, the group 'some_tag_none') if the 'sometag' tag is not defined for a VM.
    - prefix: some_tag
      key: tags.sometag | default('none')

# excludes a host from the inventory when any of these expressions is true, can refer to any vars defined on the host
exclude_host_filters:
    # excludes hosts in the eastus region
    - location in ['eastus']
    - tags['tagkey'] is defined and tags['tagkey'] == 'tagvalue'
    - tags['tagkey2'] is defined and tags['tagkey2'] == 'tagvalue2'
    # excludes hosts that are powered off
    - powerstate != 'running'

# includes a host to the inventory when any of these expressions is true, can refer to any vars defined on the host
include_host_filters:
    # includes hosts that in the eastus region and power on
    - location in ['eastus'] and powerstate == 'running'
    # includes hosts in the eastus region and power on OR includes hosts in the eastus2 region and tagkey value is tagvalue
    - location in ['eastus'] and powerstate == 'running'
    - location in ['eastus2'] and tags['tagkey'] is defined and tags['tagkey'] == 'tagvalue'
'''

# FUTURE: do we need a set of sane default filters, separate from the user-defineable ones?
# eg, powerstate==running, provisioning_state==succeeded


import hashlib
import json
import re
import uuid
import os
import time

try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty

from collections import namedtuple
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
from ansible.module_utils.six import iteritems
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMAuth
from ansible.errors import AnsibleParserError, AnsibleError
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.module_utils._text import to_native, to_bytes, to_text
from itertools import chain
from os import environ
try:
    from ansible.template import trust_as_template
except ImportError:
    trust_as_template = None

try:
    from azure.core._pipeline_client import PipelineClient
    from azure.core.pipeline.policies import BearerTokenCredentialPolicy
    from azure.core.configuration import Configuration
    from azure.mgmt.core.tools import parse_resource_id
    from azure.core.pipeline import PipelineResponse
    from azure.mgmt.core.polling.arm_polling import ARMPolling
    from azure.core.polling import LROPoller
    from netaddr import IPAddress
except ImportError:
    Configuration = object
    parse_resource_id = object
    PipelineClient = object
    BearerTokenCredentialPolicy = object
    pass


class AzureRMRestConfiguration(Configuration):
    def __init__(self, credentials, subscription_id, base_url=None):

        if credentials is None:
            raise ValueError("Parameter 'credentials' must not be None.")
        if subscription_id is None:
            raise ValueError("Parameter 'subscription_id' must not be None.")
        if not base_url:
            base_url = 'https://management.azure.com'

        credential_scopes = base_url + '/.default'

        super(AzureRMRestConfiguration, self).__init__()

        self.authentication_policy = BearerTokenCredentialPolicy(credentials, credential_scopes)
        self.credentials = credentials
        self.subscription_id = subscription_id


UrlAction = namedtuple('UrlAction', ['url', 'api_version', 'handler', 'handler_args'])


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

    NAME = 'azure.azcollection.azure_rm'

    def __init__(self):
        super(InventoryModule, self).__init__()

        self._hosts = []
        self._filters = None

        # FUTURE: use API profiles with defaults
        self._compute_api_version = '2024-07-01'
        self._network_api_version = '2024-05-01'
        self._hybridcompute_api_version = '2024-05-20-preview'
        self._stackhci_api_version = '2024-01-01'

        self._default_header_parameters = {'Content-Type': 'application/json; charset=utf-8'}

        self._request_queue = Queue()

        self.azure_auth = None

        self._batch_fetch = False

    def verify_file(self, path):
        '''
            :param loader: an ansible.parsing.dataloader.DataLoader object
            :param path: the path to the inventory config file
            :return the contents of the config file
        '''
        if super(InventoryModule, self).verify_file(path):
            if re.match(r'.{0,}azure_rm\.y(a)?ml$', path):
                return True
        # display.debug("azure_rm inventory filename must end with 'azure_rm.yml' or 'azure_rm.yaml'")
        raise AnsibleError("azure_rm inventory filename must end with 'azure_rm.yml' or 'azure_rm.yaml'")

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)

        self._read_config_data(path)

        if self.get_option('use_contrib_script_compatible_sanitization'):
            self._sanitize_group_name = self._legacy_script_compatible_group_sanitization

        self._batch_fetch = self.get_option('batch_fetch')
        self._batch_fetch_interval = self.get_option('batch_fetch_interval')
        self._batch_fetch_timeout = self.get_option('batch_fetch_timeout')

        self._legacy_hostnames = self.get_option('plain_host_names')

        self._filters = self.get_option('exclude_host_filters') + self.get_option('default_host_filters')

        self._include_filters = self.get_option('include_host_filters')

        # Load results from Cache if requested
        cache_key = self.get_cache_key(path)

        # cache may be True or False at this point to indicate if the inventory is being refreshed
        # get the user's cache option too to see if we should save the cache if it is changing
        user_cache_setting = self.get_option('cache')

        # read if the user has caching enabled and the cache isn't being refreshed
        attempt_to_read_cache = user_cache_setting and cache
        # update if the user has caching enabled and the cache is being refreshed;
        # update this value to True if the cache has expired below
        cache_needs_update = user_cache_setting and not cache

        # attempt to read the cache if inventory isn't being refreshed and the user has caching enabled
        if attempt_to_read_cache:
            try:
                results = self._cache[cache_key]
            except KeyError:
                # This occurs if the cache_key is not in the cache or if the cache_key
                # expired, so the cache needs to be updated
                cache_needs_update = True
        if not attempt_to_read_cache or cache_needs_update:
            # parse the provided inventory source
            try:
                self._credential_setup()
                self._get_hosts()
                results = self._serialize(self._hosts)
            except Exception:
                raise
        if cache_needs_update:
            self._cache[cache_key] = results

        self._populate(results)

    def _serialize(self, hosts):
        results = []
        for h in hosts:
            results.append(dict(default_inventory_hostname=h.default_inventory_hostname,
                                hostvars=h.hostvars))
        return results

    def _credential_setup(self):
        auth_source = environ.get('ANSIBLE_AZURE_AUTH_SOURCE', None) or self.get_option('auth_source')
        auth_options = dict(
            auth_source=auth_source,
            profile=self.get_option('profile'),
            subscription_id=self.get_option('subscription_id'),
            client_id=self.get_option('client_id'),
            secret=self.get_option('secret'),
            tenant=self.get_option('tenant'),
            ad_user=self.get_option('ad_user'),
            password=self.get_option('password'),
            cloud_environment=self.get_option('cloud_environment'),
            cert_validation_mode=self.get_option('cert_validation_mode'),
            api_profile=self.get_option('api_profile'),
            track1_cred=True,
            adfs_authority_url=self.get_option('adfs_authority_url')
        )

        if self.templar.is_template(auth_options["tenant"]):
            auth_options["tenant"] = self.templar.template(variable=auth_options["tenant"], disable_lookups=False)

        if self.templar.is_template(auth_options["client_id"]):
            auth_options["client_id"] = self.templar.template(variable=auth_options["client_id"], disable_lookups=False)

        if self.templar.is_template(auth_options["secret"]):
            auth_options["secret"] = self.templar.template(variable=auth_options["secret"], disable_lookups=False)

        if self.templar.is_template(auth_options["subscription_id"]):
            auth_options["subscription_id"] = self.templar.template(variable=auth_options["subscription_id"], disable_lookups=False)

        self.azure_auth = AzureRMAuth(**auth_options)

        self._clientconfig = AzureRMRestConfiguration(self.azure_auth.azure_credential_track2, self.azure_auth.subscription_id,
                                                      self.azure_auth._cloud_environment.endpoints.resource_manager)

        self.new_client = PipelineClient(self.azure_auth._cloud_environment.endpoints.resource_manager, config=self._clientconfig)

    def _enqueue_get(self, url, api_version, handler, handler_args=None):
        if not handler_args:
            handler_args = {}
        self._request_queue.put_nowait(UrlAction(url=url, api_version=api_version, handler=handler, handler_args=handler_args))

    def _enqueue_vm_list(self, rg='*'):
        if not rg or rg == '*':
            url = '/subscriptions/{subscriptionId}/providers/Microsoft.Compute/virtualMachines'
        else:
            url = '/subscriptions/{subscriptionId}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines'

        url = url.format(subscriptionId=self._clientconfig.subscription_id, rg=rg)
        self._enqueue_get(url=url, api_version=self._compute_api_version, handler=self._on_vm_page_response)

    def _enqueue_arc_list(self, rg='*'):
        if not rg or rg == '*':
            url = '/subscriptions/{subscriptionId}/providers/Microsoft.HybridCompute/machines'
        else:
            url = '/subscriptions/{subscriptionId}/resourceGroups/{rg}/providers/Microsoft.HybridCompute/machines'

        url = url.format(subscriptionId=self._clientconfig.subscription_id, rg=rg)
        self._enqueue_get(url=url, api_version=self._hybridcompute_api_version, handler=self._on_arc_page_response)

    def _enqueue_arcvm_list(self, rg='*'):
        if not rg or rg == '*':
            url = '/subscriptions/{subscriptionId}/providers/Microsoft.HybridCompute/machines'
        else:
            url = '/subscriptions/{subscriptionId}/resourceGroups/{rg}/providers/Microsoft.HybridCompute/machines'

        url = url.format(subscriptionId=self._clientconfig.subscription_id, rg=rg)
        self._enqueue_get(url=url, api_version=self._hybridcompute_api_version, handler=self._on_arcvm_page_response)

    def _enqueue_vmss_list(self, rg=None):
        if not rg or rg == '*':
            url = '/subscriptions/{subscriptionId}/providers/Microsoft.Compute/virtualMachineScaleSets'
        else:
            url = '/subscriptions/{subscriptionId}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachineScaleSets'

        url = url.format(subscriptionId=self._clientconfig.subscription_id, rg=rg)
        self._enqueue_get(url=url, api_version=self._compute_api_version, handler=self._on_vmss_page_response)

    def _get_hosts(self):
        if os.environ.get('ANSIBLE_AZURE_VM_RESOURCE_GROUPS'):
            for vm_rg in os.environ['ANSIBLE_AZURE_VM_RESOURCE_GROUPS'].split(","):
                self._enqueue_vm_list(vm_rg)
        else:
            for vm_rg in self.get_option('include_vm_resource_groups'):
                self._enqueue_vm_list(vm_rg)

        for arc_rg in self.get_option('include_arc_resource_groups'):
            self._enqueue_arc_list(arc_rg)

        for vm_rg in self.get_option('include_hcivm_resource_groups'):
            self._enqueue_arcvm_list(vm_rg)

        if os.environ.get('ANSIBLE_AZURE_VMSS_RESOURCE_GROUPS'):
            for vmss_rg in os.environ['ANSIBLE_AZURE_VMSS_RESOURCE_GROUPS'].split(","):
                self._enqueue_vmss_list(vmss_rg)
        else:
            for vmss_rg in self.get_option('include_vmss_resource_groups'):
                self._enqueue_vmss_list(vmss_rg)

        if self._batch_fetch:
            self._process_queue_batch()
        else:
            self._process_queue_serial()

    def _populate(self, results):
        constructable_config_strict = boolean(self.get_option('fail_on_template_errors'))
        if self.get_option('hostvar_expressions') is not None:
            constructable_config_compose = self.get_option('hostvar_expressions')
        else:
            constructable_config_compose = self.get_option('compose')
        constructable_config_groups = self.get_option('conditional_groups')
        constructable_config_keyed_groups = self.get_option('keyed_groups')

        constructable_hostnames = self.get_option('hostnames')

        for h in results:
            hostvars = h.get("hostvars")
            # FUTURE: track hostnames to warn if a hostname is repeated (can happen for legacy and for composed inventory_hostname)
            inventory_hostname = self._get_hostname(h, hostnames=constructable_hostnames, strict=constructable_config_strict)
            if self._filter_exclude_host(inventory_hostname, hostvars):
                continue
            if not self._filter_include_host(inventory_hostname, hostvars):
                continue
            self.inventory.add_host(inventory_hostname)
            # FUTURE: configurable default IP list? can already do this via hostvar_expressions
            self.inventory.set_variable(inventory_hostname, "ansible_host",
                                        next(chain(hostvars['public_ipv4_address'], hostvars['private_ipv4_addresses']), None))
            for k, v in iteritems(hostvars):
                # FUTURE: configurable hostvar prefix? Makes docs harder...
                self.inventory.set_variable(inventory_hostname, k, v)

            # constructable delegation
            self._set_composite_vars(constructable_config_compose, hostvars, inventory_hostname, strict=constructable_config_strict)
            self._add_host_to_composed_groups(constructable_config_groups, hostvars, inventory_hostname, strict=constructable_config_strict)
            self._add_host_to_keyed_groups(constructable_config_keyed_groups, hostvars, inventory_hostname, strict=constructable_config_strict)

    # FUTURE: fix underlying inventory stuff to allow us to quickly access known groupvars from reconciled host
    def _filter_host(self, filter, inventory_hostname, hostvars):
        self.templar.available_variables = hostvars

        for condition in filter:
            # FUTURE: should warn/fail if conditional doesn't return True or False
            conditional = "{{% if {0} %}}true{{% else %}}false{{% endif %}}".format(condition)
            if trust_as_template:
                conditional = trust_as_template(conditional)
            try:
                if boolean(self.templar.template(conditional)):
                    return True
            except Exception as e:
                if boolean(self.get_option('fail_on_template_errors')):
                    raise AnsibleParserError("Error evaluating filter condition '{0}' for host {1}: {2}".format(condition, inventory_hostname, to_native(e)))
                continue

        return False

    def _filter_include_host(self, inventory_hostname, hostvars):
        return self._filter_host(self._include_filters, inventory_hostname, hostvars)

    def _filter_exclude_host(self, inventory_hostname, hostvars):
        return self._filter_host(self._filters, inventory_hostname, hostvars)

    def _get_hostname(self, host, hostnames=None, strict=False):
        hostname = None
        errors = []

        for preference in hostnames:
            if preference == 'default':
                return host.get("default_inventory_hostname")
            try:
                hostname = self._compose(preference, host.get("hostvars"))
            except Exception as e:  # pylint: disable=broad-except
                if strict:
                    raise AnsibleError("Could not compose %s as hostnames - %s" % (preference, to_native(e)))
                else:
                    errors.append(
                        (preference, str(e))
                    )
            if hostname:
                return to_text(hostname)

        raise AnsibleError(
            'Could not template any hostname for host, errors for each preference: %s' % (
                ', '.join(['%s: %s' % (pref, err) for pref, err in errors])
            )
        )

    def _process_queue_serial(self):
        try:
            while True:
                item = self._request_queue.get_nowait()
                resp = self.send_request(item.url, item.api_version)
                item.handler(resp, **item.handler_args)
        except Empty:
            pass

    def _on_vm_page_response(self, response, vmss=None, arcvm=None):
        next_link = response.get('nextLink')

        if next_link:
            self._enqueue_get(url=next_link, api_version=self._compute_api_version, handler=self._on_vm_page_response,
                              handler_args=dict(vmss=vmss, arcvm=arcvm))

        if 'value' in response:
            for h in response['value']:
                # FUTURE: add direct VM filtering by tag here (performance optimization)?
                self._hosts.append(AzureHost(h, self, vmss=vmss, arcvm=arcvm, legacy_name=self._legacy_hostnames))

    def _on_arc_page_response(self, response):
        next_link = response.get('nextLink')

        if next_link:
            self._enqueue_get(url=next_link, api_version=self._hybridcompute_api_version, handler=self._on_arc_page_response)

        for arcvm in response['value']:
            self._hosts.append(ArcHost(arcvm, self, legacy_name=self._legacy_hostnames))

    def _on_arcvm_page_response(self, response):
        next_link = response.get('nextLink')

        if next_link:
            self._enqueue_get(url=next_link, api_version=self._hybridcompute_api_version, handler=self._on_arcvm_page_response)

        for arcvm in response['value']:
            url = '{0}/providers/Microsoft.AzureStackHCI/virtualMachineInstances'.format(arcvm['id'])
            # Stack HCI instances look close enough to regular VMs that we can share the handler impl...
            self._enqueue_get(url=url, api_version=self._stackhci_api_version, handler=self._on_vm_page_response, handler_args=dict(arcvm=arcvm))

    def _on_vmss_page_response(self, response):
        next_link = response.get('nextLink')

        if next_link:
            self._enqueue_get(url=next_link, api_version=self._compute_api_version, handler=self._on_vmss_page_response)

        # FUTURE: add direct VMSS filtering by tag here (performance optimization)?
        for vmss in response['value']:
            url = '{0}/virtualMachines'.format(vmss['id'])

            # Since Flexible instance is a standalone VM we are processing them as regular VM.
            if vmss['properties']['orchestrationMode'] != 'Flexible':
                # VMSS instances look close enough to regular VMs that we can share the handler impl...
                self._enqueue_get(url=url, api_version=self._compute_api_version, handler=self._on_vm_page_response, handler_args=dict(vmss=vmss))

    # use the undocumented /batch endpoint to bulk-send up to 500 requests in a single round-trip
    #
    def _process_queue_batch(self):
        while True:
            batch_requests = []
            batch_item_index = 0
            batch_response_handlers = dict()
            try:
                while batch_item_index < 100:
                    item = self._request_queue.get_nowait()

                    name = str(uuid.uuid4())
                    query_parameters = {'api-version': item.api_version}
                    header_parameters = {'x-ms-client-request-id': str(uuid.uuid4()), 'Content-Type': 'application/json; charset=utf-8'}
                    body = {}
                    req = self.new_client.get(item.url, query_parameters, header_parameters, body)
                    batch_requests.append(dict(httpMethod="GET", url=req.url, name=name))
                    batch_response_handlers[name] = item
                    batch_item_index += 1
            except Empty:
                pass

            if not batch_requests:
                break

            self.retry_batch(batch_requests, batch_response_handlers)

    def retry_batch(self, batch_requests, batch_response_handlers, backoff_factor=0.8, retry_limit=10):
        retry_count = 1
        _SAFE_CODES = set(range(506)) - set([408, 429, 500, 502, 503, 504])
        _RETRY_CODES = set(range(999)) - _SAFE_CODES
        while True:
            batch_resp = self._send_batch(batch_requests)
            key_name = None
            if 'responses' in batch_resp:
                key_name = 'responses'
            elif 'value' in batch_resp:
                key_name = 'value'
            else:
                raise AnsibleError("didn't find expected key responses/value in batch response")
            batch_processed = []
            batch_retry = False
            for idx, r in enumerate(batch_resp[key_name]):
                status_code = r.get('httpStatusCode')
                returned_name = r['name']
                result = batch_response_handlers[returned_name]
                if status_code == 200:
                    # FUTURE: error-tolerant operation mode (eg, permissions)
                    # FUTURE: store/handle errors from individual handlers
                    result.handler(r['content'], **result.handler_args)
                    batch_processed.append(returned_name)
                elif status_code in _RETRY_CODES:
                    # 429: Too many requests Error, Backoff and Retry
                    batch_retry = True
            if batch_retry:
                time.sleep(backoff_factor * (2 ** (retry_count)))
                retry_count += 1
                if len(batch_processed) > 0:
                    # Remove already processed requests
                    for idx, r in enumerate(batch_requests):
                        if r.get('name') in batch_processed:
                            processed = batch_requests.pop(idx)
                if retry_count > retry_limit:
                    raise AnsibleError("Reached maximum retries in batch request")
            else:
                break

    def _send_batch(self, batched_requests):
        url = '/batch'
        query_parameters = {'api-version': '2015-11-01'}
        header_parameters = {'x-ms-client-request-id': str(uuid.uuid4()), 'Content-Type': 'application/json; charset=utf-8'}
        operation_config = {}
        body_content = dict(requests=batched_requests)

        header = {'x-ms-client-request-id': str(uuid.uuid4())}
        header.update(self._default_header_parameters)

        request_new = self.new_client.post(url, query_parameters, header_parameters, body_content)
        response = self.new_client.send_request(request_new, **operation_config)

        if response.status_code == 202:
            def get_long_running_output(response):
                return response
            poller = LROPoller(self.new_client,
                               PipelineResponse(None, response, None),
                               get_long_running_output,
                               ARMPolling(self._batch_fetch_interval, **operation_config))
            response = self.get_poller_result(poller, self._batch_fetch_timeout)
            if hasattr(response, 'body'):
                response = json.loads(response.body())
            elif hasattr(response, 'context'):
                response = response.context['deserialized_data']
        else:
            response = json.loads(response.body())

        return response

    def get_poller_result(self, poller, timeout):
        try:
            while not poller.done():
                poller.wait(timeout=timeout)
            return poller.result()
        except Exception as exc:
            raise

    def send_request(self, url, api_version):
        query_parameters = {'api-version': api_version}
        header_parameters = {'x-ms-client-request-id': str(uuid.uuid4()), 'Content-Type': 'application/json; charset=utf-8'}
        body = {}
        request_new = self.new_client.get(url, query_parameters, header_parameters)
        response = self.new_client.send_request(request_new)

        return json.loads(response.body())

    @staticmethod
    def _legacy_script_compatible_group_sanitization(name):

        # note that while this mirrors what the script used to do, it has many issues with unicode and usability in python
        regex = re.compile(r"[^A-Za-z0-9\_\-]")

        return regex.sub('_', name)

# VM list (all, N resource groups): VM -> InstanceView, N NICs, N PublicIPAddress)
# VMSS VMs (all SS, N specific SS, N resource groups?): SS -> VM -> InstanceView, N NICs, N PublicIPAddress)


class ArcHost(object):
    def __init__(self, arc_model, inventory_client, legacy_name=False):
        self._inventory_client = inventory_client
        self._arc_model = arc_model
        self._instanceview = self._arc_model
        self._status = self._arc_model['properties'].get('status', {}).lower()  # 'Connected'
        self._powerstate = self._status.replace('connected', 'running')

        self._hostvars = {}

        arc_name = self._arc_model['name']

        if legacy_name:
            self.default_inventory_hostname = arc_name
        else:
            # Azure often doesn't provide a globally-unique filename, so use resource name + a chunk of ID hash
            self.default_inventory_hostname = '{0}_{1}'.format(arc_name, hashlib.sha1(to_bytes(arc_model['id'])).hexdigest()[0:4])

    @property
    def hostvars(self):
        if self._hostvars != {}:
            return self._hostvars

        properties = self._arc_model.get('properties', {})
        new_hostvars = dict(
            network_interface=[],
            mac_address=[],
            ansible_all_ipv4_addresses=[],
            ansible_all_ipv6_addresses=[],
            public_ipv4_address=[],
            private_ipv4_addresses=[],
            public_dns_hostnames=[],
            ansible_dns=[],
            id=self._arc_model['id'],
            location=self._arc_model['location'],
            name=self._arc_model['name'],
            default_inventory_hostname=self.default_inventory_hostname,
            powerstate=self._powerstate,
            status=self._status,
            provisioning_state=properties.get('provisioningState', 'unknown').lower(),
            vmid=self._arc_model['properties']['vmId'],
            os_profile=dict(
                sku=properties.get('osSku', 'unknown'),
                system=properties.get('osType', 'unknown'),
                version=properties.get('osVersion', 'unknown'),
            ),
            tags=self._arc_model.get('tags', {}),
            resource_type=self._arc_model.get('type', "unknown"),
            resource_group=parse_resource_id(self._arc_model['id']).get('resource_group').lower(),
        )

        for nic in properties.get('networkProfile', {}).get('networkInterfaces', []):
            new_hostvars['mac_address'].append(nic.get('macAddress'))
            new_hostvars['network_interface'].append(nic.get('name'))
            for ipaddr in nic.get('ipAddresses', []):
                ipAddressVersion = ipaddr.get('ipAddressVersion')
                if ipAddressVersion == 'IPv4':
                    ipv4_address = ipaddr.get('address')
                    new_hostvars['ansible_all_ipv4_addresses'].append(ipv4_address)
                    if IPAddress(ipv4_address).is_global():
                        new_hostvars['public_ipv4_address'].append(ipv4_address)
                    else:
                        new_hostvars['private_ipv4_addresses'].append(ipv4_address)
                if ipAddressVersion == 'IPv6':
                    new_hostvars['ansible_all_ipv6_addresses'].append(ipaddr.get('address'))
        self._hostvars = new_hostvars
        return self._hostvars


class AzureHost(object):
    _powerstate_regex = re.compile('^PowerState/(?P<powerstate>.+)$')

    def __init__(self, vm_model, inventory_client, vmss=None, arcvm=None, legacy_name=False):
        self._inventory_client = inventory_client
        self._vm_model = vm_model
        self._vmss = vmss
        self._arcvm = arcvm

        self._instanceview = None

        self._powerstate = "unknown"
        self.nics = []

        vm_name = self._arcvm['name'] if self._arcvm else self._vm_model['name']

        if legacy_name:
            self.default_inventory_hostname = vm_name
        else:
            # Azure often doesn't provide a globally-unique filename, so use resource name + a chunk of ID hash
            self.default_inventory_hostname = '{0}_{1}'.format(vm_name, hashlib.sha1(to_bytes(vm_model['id'])).hexdigest()[0:4])

        self._hostvars = {}

        if self._arcvm:
            self._instanceview = self._vm_model
            self._powerstate = self._vm_model['properties'].get('status', {}).get('powerState', '').lower()  # 'Running'
        else:
            inventory_client._enqueue_get(url="{0}/instanceView".format(vm_model['id']),
                                          api_version=self._inventory_client._compute_api_version,
                                          handler=self._on_instanceview_response)

        nic_refs = vm_model['properties']['networkProfile']['networkInterfaces']
        for nic in nic_refs:
            # single-nic instances don't set primary, so figure it out...
            is_primary = nic.get('properties', {}).get('primary', len(nic_refs) == 1)
            api_version = self._inventory_client._stackhci_api_version if self._arcvm else self._inventory_client._network_api_version
            inventory_client._enqueue_get(url=nic['id'],
                                          api_version=api_version,
                                          handler=self._on_nic_response,
                                          handler_args=dict(is_primary=is_primary))

    @property
    def hostvars(self):
        if self._hostvars != {}:
            return self._hostvars

        system = "unknown"
        if self._arcvm and self._arcvm['properties'].get('osType'):  # osType unavailable with disabled guest agent
            system = self._arcvm['properties']['osType']
        elif 'osProfile' in self._vm_model['properties']:
            if 'linuxConfiguration' in self._vm_model['properties']['osProfile']:
                system = 'linux'
            if 'windowsConfiguration' in self._vm_model['properties']['osProfile']:
                system = 'windows'
        else:
            osType = self._vm_model['properties']['storageProfile']['osDisk']['osType']
            if osType == 'Linux':
                system = 'linux'
            if osType == 'Windows':
                system = 'windows'
        av_zone = None
        if 'zones' in self._vm_model:
            av_zone = self._vm_model['zones']

        createdAt = self._vm_model.get('systemData', {}).get('createdAt')  # hci specific

        new_hostvars = dict(
            network_interface=[],
            network_interface_properties=[],
            mac_address=[],
            network_interface_id=[],
            security_group_id=[],
            security_group=[],
            public_ip_address=[],
            public_ipv4_address=[],
            public_dns_hostnames=[],
            private_ipv4_addresses=[],
            subnet=[],
            id=self._vm_model['id'],
            location=self._arcvm['location'] if self._arcvm else self._vm_model['location'],
            name=self._arcvm['name'] if self._arcvm else self._vm_model['name'],
            computer_name=self._vm_model['properties'].get('osProfile', {}).get('computerName'),
            availability_zone=av_zone,
            powerstate=self._powerstate,
            provisioning_state=self._vm_model['properties']['provisioningState'].lower(),
            tags=self._arcvm.get('tags', {}) if self._arcvm else self._vm_model.get('tags', {}),
            resource_type=self._vm_model.get('type', "unknown"),
            vmid=self._vm_model['properties']['vmId'],
            os_profile=dict(
                system=system,
            ),
            vmss=dict(
                id=self._vmss['id'],
                name=self._vmss['name'],
            ) if self._vmss else {},
            virtual_machine_size=self._vm_model['properties']['hardwareProfile']['vmSize'] if self._vm_model['properties'].get('hardwareProfile') else None,
            plan=self._vm_model['properties']['plan']['name'] if self._vm_model['properties'].get('plan') else None,
            resource_group=parse_resource_id(self._vm_model['id']).get('resource_group').lower(),
            default_inventory_hostname=self.default_inventory_hostname,
            creation_time=createdAt if createdAt else self._vm_model['properties'].get('timeCreated'),
            license_type=self._vm_model['properties'].get('licenseType', 'Unknown')
        )
        if self._arcvm:
            new_hostvars['customLocation'] = self._vm_model.get('extendedLocation', {}).get('name', '').split('/')[-1]
            new_hostvars['virtual_machine_memoryMB'] = self._vm_model['properties']['hardwareProfile'].get('memoryMB')
            new_hostvars['virtual_machine_processors'] = self._vm_model['properties']['hardwareProfile'].get('processors')

        # set nic-related values from the primary NIC first
        for nic in sorted(self.nics, key=lambda n: n.is_primary, reverse=True):
            # and from the primary IP config per NIC first
            for ipc in sorted(nic._nic_model.get('properties', {}).get('ipConfigurations', []),
                              key=lambda i: i.get('properties', {}).get('primary', False), reverse=True):
                try:
                    subnet = ipc['properties'].get('subnet')
                    if subnet:
                        new_hostvars['subnet'].append(subnet)
                    private_ip = ipc['properties'].get('privateIPAddress')
                    if private_ip:
                        new_hostvars['private_ipv4_addresses'].append(private_ip)
                    pip_id = ipc['properties'].get('publicIPAddress', {}).get('id')
                    if pip_id and pip_id in nic.public_ips:
                        pip = nic.public_ips[pip_id]
                        new_hostvars['public_ipv4_address'].append(pip._pip_model['properties'].get('ipAddress', None))
                        new_hostvars['public_ip_address'].append({
                            'id': pip_id,
                            'name': pip._pip_model['name'],
                            'ipv4_address': pip._pip_model['properties'].get('ipAddress', None),
                        })
                        pip_fqdn = pip._pip_model['properties'].get('dnsSettings', {}).get('fqdn')
                        if pip_fqdn:
                            new_hostvars['public_dns_hostnames'].append(pip_fqdn)
                except Exception:
                    continue

            new_hostvars['mac_address'].append(nic._nic_model['properties'].get('macAddress'))
            new_hostvars['network_interface'].append(nic._nic_model['name'])
            new_hostvars['network_interface_id'].append(nic._nic_model['id'])
            new_hostvars['security_group_id'].append(nic._nic_model['properties']['networkSecurityGroup']['id']) \
                if nic._nic_model['properties'].get('networkSecurityGroup') else None
            new_hostvars['security_group'].append(parse_resource_id(nic._nic_model['properties']['networkSecurityGroup']['id'])['resource_name']) \
                if nic._nic_model['properties'].get('networkSecurityGroup') else None

            new_hostvars['network_interface_properties'].append(nic._nic_model)

        # set image and os_disk
        new_hostvars['image'] = {}
        new_hostvars['os_disk'] = {}
        new_hostvars['data_disks'] = []
        storageProfile = self._vm_model['properties'].get('storageProfile')
        if storageProfile:
            imageReference = storageProfile.get('imageReference')
            if imageReference:
                if imageReference.get('publisher'):
                    new_hostvars['image'] = dict(
                        sku=imageReference.get('sku'),
                        publisher=imageReference.get('publisher'),
                        version=imageReference.get('version'),
                        offer=imageReference.get('offer')
                    )
                elif imageReference.get('id'):
                    new_hostvars['image'] = dict(
                        id=imageReference.get('id')
                    )

            osDisk = storageProfile.get('osDisk')
            new_hostvars['os_disk'] = dict(
                name=osDisk.get('name'),
                operating_system_type=osDisk.get('osType').lower() if osDisk.get('osType') else None,
                id=storageProfile.get('vmConfigStoragePathId') if self._arcvm else osDisk.get('managedDisk', {}).get('id')
            )

            if self._arcvm:
                new_hostvars['data_disks'] = [
                    dict(
                        name=dataDisk.get('id').split('/')[-1],
                        id=dataDisk.get('id')
                    ) for dataDisk in storageProfile.get('dataDisks', [])
                ]
            else:
                new_hostvars['data_disks'] = [
                    dict(
                        name=dataDisk.get('name'),
                        lun=dataDisk.get('lun'),
                        id=dataDisk.get('managedDisk', {}).get('id')
                    ) for dataDisk in storageProfile.get('dataDisks', [])
                ]

        self._hostvars = new_hostvars
        return self._hostvars

    def _on_instanceview_response(self, vm_instanceview_model):
        self._instanceview = vm_instanceview_model
        self._powerstate = next((self._powerstate_regex.match(s.get('code', '')).group('powerstate')
                                 for s in vm_instanceview_model.get('statuses', []) if self._powerstate_regex.match(s.get('code', ''))), 'unknown')

    def _on_nic_response(self, nic_model, is_primary=False):
        nic = AzureNic(nic_model=nic_model, inventory_client=self._inventory_client, is_primary=is_primary)
        self.nics.append(nic)


class AzureNic(object):
    def __init__(self, nic_model, inventory_client, is_primary=False):
        self._nic_model = nic_model
        self.is_primary = is_primary
        self._inventory_client = inventory_client

        self.public_ips = {}

        if nic_model.get('properties', {}).get('ipConfigurations'):
            for ipc in nic_model['properties']['ipConfigurations']:
                pip = ipc['properties'].get('publicIPAddress')
                if pip:
                    self._inventory_client._enqueue_get(url=pip['id'], api_version=self._inventory_client._network_api_version, handler=self._on_pip_response)

    def _on_pip_response(self, pip_model):
        self.public_ips[pip_model['id']] = AzurePip(pip_model)


class AzurePip(object):
    def __init__(self, pip_model):
        self._pip_model = pip_model
