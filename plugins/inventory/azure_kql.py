# Copyright (c) 2018 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
    name: azure_kql
    version_added: "3.7.0"
    short_description: Azure Resource Manager inventory plugin using Graph QL
    extends_documentation_fragment:
      - azure.azcollection.azure
      - azure.azcollection.azure_kql
      - constructed
      - inventory_cache
    description:
        - Query VM details from Azure Resource Manager using Graph QL
        - See https://learn.microsoft.com/en-us/azure/virtual-machines/resource-graph-samples?tabs=azure-cli
          for how to craft your own query.  The one requirement is that you need to provide inventory_hostname.
        - Requires a YAML configuration file whose name ends with 'azure_kql.(yml|yaml)'
        - Be aware that currently Azure Resource Graph may not be consistent with the actual state of your
          resources.  It can take up to 30 minutes for updates to propagate.  This applies both for resources
          to appear and to dissapear.
'''

EXAMPLES = '''
plugin: azure.azcollection.azure_kql

graph_query: |-
  Resources
      | where type =~ 'microsoft.compute/virtualmachines'
      | project vmId = tolower(tostring(id)),
                inventory_hostname = name,
                tags,
                location,
                resourceGroup,
                osType = tostring(properties.storageProfile.osDisk.osType),
                powerState = tostring(properties.extended.instanceView.powerState.displayStatus),
                hostName = properties.osProfile.computerName,
                subscription_id = subscriptionId
      | join kind=inner (ResourceContainers
          | where type=='microsoft.resources/subscriptions'
          | extend subscription_name = name,
                   subscription_id = subscriptionId,
                   state = properties.state
          | where state == 'Enabled'
          | project subscription_name,
                    subscription_id)
            on subscription_id
      | project-away subscription_id1
      | join (Resources
          | where type =~ 'microsoft.network/networkinterfaces'
          | mv-expand ipconfig=properties.ipConfigurations
          | project vmId = tolower(tostring(properties.virtualMachine.id)),
                    privateIp = ipconfig.properties.privateIPAddress,
                    publicIpId = tostring(ipconfig.properties.publicIPAddress.id)
          | join kind=leftouter (Resources
              | where type =~ 'microsoft.network/publicipaddresses'
              | project publicIpId = id, publicIp = properties.ipAddress
          ) on publicIpId
          | project-away publicIpId, publicIpId1
          | summarize privateIps = make_list(privateIp), publicIps = make_list(publicIp) by vmId
      ) on vmId
      | project-away vmId1
      | sort by inventory_hostname asc

# adds variables to each host found by this inventory plugin, whose values are the result of the associated expression
compose:
    ansible_host: "(publicIps + privateIps) | first"
    ansible_winrm_kerberos_hostname_override: "inventory_name + '.domain.tld'"
    ansible_winrm_transport: "'ntlm' if ('AAP_managed' in tags and ('DMZ' in (tags.AAP_Managed|list) or 'Local' in (tags.AAP_Managed|list))) else 'kerberos'"

groups:
    AAP_Managed: "'AAP_Managed' in (tags|list)"
    ubuntu18: "'AAP_Managed' in (tags|list) and 'ubuntu18' in tags.Ansible_OS"
    ubuntu20: "'AAP_Managed' in (tags|list) and 'ubuntu20' in tags.Ansible_OS"
    ubuntu22: "'AAP_Managed' in (tags|list) and 'ubuntu22' in tags.Ansible_OS"
    rhel7: "'AAP_Managed' in (tags|list) and 'rhel7' in tags.Ansible_OS"
    rhel8: "'AAP_Managed' in (tags|list) and 'rhel8' in tags.Ansible_OS"
    rhel9: "'AAP_Managed' in (tags|list) and 'rhel9' in tags.Ansible_OS"
    windows2012: "'AAP_Managed' in (tags|list) and 'windows2012' in tags.Ansible_OS"
    windows2016: "'AAP_Managed' in (tags|list) and 'windows2016' in tags.Ansible_OS"
    windows2019: "'AAP_Managed' in (tags|list) and 'windows2019' in tags.Ansible_OS"
    windows2022: "'AAP_Managed' in (tags|list) and 'windows2022' in tags.Ansible_OS"
    Asia: "'AAP_managed' in (tags|list) and 'Asia' in tags.AAP_Managed"
    North_America: "'AAP_managed' in (tags|list) and 'Asia' not in tags.AAP_Managed"

# change how inventory_hostname is generated. Each item is a jinja2 expression similar to hostvar_expressions.
hostnames:
    - "tags.vm_name if 'vm_name' in tags"
    - default_inventory_hostname + ".domain.tld" # Transfer to fqdn if you use shortnames for VMs
    - default  # special var that uses the default hashed name

keyed_groups:
    - prefix: ""
      separator: ""
      key: osType
    - prefix: ""
      separator: ""
      key: location
    - prefix: ""
      separator: ""
      key: powerState
'''

import re
from ansible.module_utils.six import iteritems
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
from ansible.errors import AnsibleError
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.module_utils._text import to_native, to_text
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMAuth
from os import environ

try:
    import pandas as pd
    import azure.mgmt.resourcegraph as arg
except ImportError:
    pd = object
    arg = object
    pass


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

    NAME = 'azure.azcollection.azure_kql'

    def __init__(self):
        super(InventoryModule, self).__init__()

        self.azure_auth = None

    def verify_file(self, path):
        """ Verify inventory file """
        if super(InventoryModule, self).verify_file(path):
            if re.match(r'.{0,}azure_kql\.y(a)?ml$', path):
                return True
        raise AnsibleError("azure_kql inventory filename must end with 'azure_kql.yml' or 'azure_kql.yaml'")

    def parse(self, inventory, loader, path, cache=True):
        """ parses the inventory file """

        super(InventoryModule, self).parse(inventory, loader, path)

        self._read_config_data(path)

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
                results = self._get_hosts()
            except Exception:
                raise
        if cache_needs_update:
            self._cache[cache_key] = results

        self._populate(results)

    def _populate(self, results):
        """ Populate inventory """
        constructable_config_strict = boolean(self.get_option('fail_on_template_errors'))
        constructable_config_compose = self.get_option('compose')
        constructable_config_groups = self.get_option('groups')
        constructable_config_keyed_groups = self.get_option('keyed_groups')
        constructable_hostnames = self.get_option('hostnames')

        for h in results:
            hostvars = h.get("hostvars")
            inventory_hostname = self._get_hostname(h,
                                                    hostnames=constructable_hostnames,
                                                    strict=constructable_config_strict)
            self.inventory.add_host(inventory_hostname)

            for k, v in iteritems(hostvars):
                self.inventory.set_variable(inventory_hostname, k, v)

            # constructable delegation
            self._set_composite_vars(constructable_config_compose,
                                     hostvars,
                                     inventory_hostname,
                                     strict=constructable_config_strict)
            self._add_host_to_composed_groups(constructable_config_groups,
                                              hostvars,
                                              inventory_hostname,
                                              strict=constructable_config_strict)
            self._add_host_to_keyed_groups(constructable_config_keyed_groups,
                                           hostvars,
                                           inventory_hostname,
                                           strict=constructable_config_strict)

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

    def execute_kql(self, query, resource_name='VMs'):
        """ Execute KQL query """

        argClient = arg.ResourceGraphClient(self.azure_auth.azure_credential_track2)
        skpToken = 'hasData'
        output = []

        while skpToken is not None:
            if skpToken == 'hasData':
                argQueryOptions = arg.models.QueryRequestOptions(result_format="objectArray")
            else:
                argQueryOptions = arg.models.QueryRequestOptions(result_format="objectArray", skip_token=skpToken)
            argQuery = arg.models.QueryRequest(query=query, options=argQueryOptions)
            argResults = argClient.resources(argQuery)
            output.extend(argResults.data)
            skpToken = argResults.skip_token

        df_output = pd.DataFrame(output)
        return df_output

    def _get_hosts(self):
        """ Get all hosts via graph_query """

        df_vms = self.execute_kql(query=self.get_option('graph_query'))
        results = []

        for index, row in df_vms.iterrows():
            # Convert panda object to dict
            row = row.to_dict()
            # If no tags are present use an empty dict
            tags = row.pop('tags') or {}
            # Update row with updated tags
            row.update({'tags': tags})
            results.append(dict(default_inventory_hostname=row.get('inventory_hostname'),
                                hostvars=row))

        return results
