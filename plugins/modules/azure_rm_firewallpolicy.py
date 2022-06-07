#!/usr/bin/python
#
# Copyright (c) 2021 Aparna Patil(@aparna-patil)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_firewallpolicy

version_added: "1.13.0"

short_description: Create, delete or update specified firewall policy.

description:
    - Creates, deletes, or updates given firewall policy in specified resource group.

options:
    resource_group:
        description:
            - Name of the resource group.
        required: true
        type: str
    name:
        description:
            - The name of the firewall policy.
        required: true
        type: str
    location:
        description:
            - Location for firewall policy. Defaults to location of resource group if not specified.
        type: str
    base_policy:
        description:
            - The name of the parent firewall policy from which rules are inherited.
        type: str
    threat_intel_mode:
        description:
            - The operation mode for Threat Intel.
        default: alert
        type: str
        choices:
            - alert
            - deny
            - 'off'
    threat_intel_whitelist:
        description:
            - ThreatIntel Whitelist for Firewall Policy.
        type: dict
        suboptions:
            ip_addresses:
                description:
                    - List of IP addresses for the ThreatIntel Whitelist.
                type: list
                elements: str
            append_ip_addresses:
                description:
                    - Flag to indicate if the ip_addresses to be appended or not.
                type: bool
                default: true
            fqdns:
                description:
                    - List of FQDNs for the ThreatIntel Whitelist
                type: list
                elements: str
            append_fqdns:
                description:
                    - Flag to indicate if the fqdns to be appended or not.
                type: bool
                default: true
    state:
        description:
            - Assert the state of the firewall policy. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Aparna Patil (@aparna-patil)
'''

EXAMPLES = '''
- name: Create a Firewall Policy
  azure_rm_firewallpolicy:
    resource_group: myAzureResourceGroup
    name: myfirewallpolicy
    base_policy: firewallparentpolicy
    threat_intel_mode: alert
    threat_intel_whitelist:
      ip_addresses:
        - 10.0.0.1
        - 10.0.0.2
      fqdns:
        - "*.microsoft.com"
        - "*.azure.com"
    state: present

- name: Update Firewall Policy
  azure_rm_firewallpolicy:
    resource_group: myAzureResourceGroup
    name: myfirewallpolicy
    base_policy: firewallparentpolicy
    threat_intel_mode: deny
    threat_intel_whitelist:
      ip_addresses:
        - 10.0.0.1
      fqdns:
        - "*.microsoft.com"
    state: present
    tags:
      key1: "value1"

- name: Delete Firewall Policy
  azure_rm_firewallpolicy:
    resource_group: myAzureResourceGroup
    name: myfirewallpolicy
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the Firewall Policy.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The firewall policy ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/MyAzureResourceGroup/providers/
                     Microsoft.Network/firewallPolicies/myfirewallpolicy"
        name:
            description:
                - The firewall policy name.
            returned: always
            type: str
            sample: 'myfirewallpolicy'
        location:
            description:
                - The Azure Region where the resource lives.
            returned: always
            type: str
            sample: eastus
        base_policy:
            description:
                - The parent firewall policy from which rules are inherited.
            returned: always
            type: dict
            sample: {
              "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/MyAzureResourceGroup/providers/
                     Microsoft.Network/firewallPolicies/firewallparentpolicy"
            }
        child_policies:
            description:
                - List of references to Child Firewall Policies.
            returned: always
            type: list
            elements: dict
            sample: [
            {
              "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/MyAzureResourceGroup/providers/
                     Microsoft.Network/firewallPolicies/childpolicy1"
            }
        ]
        provisioning_state:
            description:
                - The provisioning state of the resource.
            returned: always
            type: str
            sample: Succeeded
        firewalls:
            description:
                - List of references to Azure Firewalls that this Firewall Policy is associated with.
            returned: always
            type: list
            elements: dict
            sample: [
            {
              "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myAzureResourceGroup/providers/
                     Microsoft.Network/azureFirewalls/azurefirewall"
            }
        ]
        rule_collection_groups:
            description:
                - List of references to FirewallPolicyRuleCollectionGroups.
            returned: always
            type: list
            elements: dict
            sample: [
            {
              "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/MyAzureResourceGroup/providers/
                     Microsoft.Network/firewallPolicies/myfirewallpolicy/
                     ruleCollectionGroups/DefaultNetworkRuleCollectionGroup"
            }
        ]
        threat_intel_mode:
            description:
                - The operation mode for Threat Intelligence.
            returned: always
            type: str
            sample: Alert
        threat_intel_whitelist:
            description:
                - ThreatIntel Whitelist for Firewall Policy.
            returned: always
            type: dict
            sample: {
              "fqdns": [
                  "*.microsoft.com",
                  "*.azure.com"
              ],
              "ip_addresses": [
                  "10.0.0.1",
                  "10.0.0.2"
              ]
        }
        tags:
            description:
                - Resource tags.
            returned: always
            type: list
            sample: [{"key1": "value1"}]
        type:
            description:
                - The type of resource.
            returned: always
            type: str
            sample: Microsoft.Network/FirewallPolicies
        etag:
            description:
                - The etag of the firewall policy.
            returned: always
            type: str
            sample: 7cb2538e-0e52-4435-8979-4f417e7269d1
'''

from ansible.module_utils.basic import _load_params
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, HAS_AZURE, \
    format_resource_id, normalize_location_name
import copy

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass

threat_intel_whitelist_spec = dict(
    ip_addresses=dict(type='list', elements='str'),
    append_ip_addresses=dict(type='bool', default=True),
    fqdns=dict(type='list', elements='str'),
    append_fqdns=dict(type='bool', default=True)
)


class AzureRMFirewallPolicy(AzureRMModuleBase):

    def __init__(self):

        _load_params()
        # define user inputs from playbook
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            base_policy=dict(type='str'),
            threat_intel_mode=dict(choices=['alert', 'deny', 'off'], default='alert', type='str'),
            threat_intel_whitelist=dict(type='dict', options=threat_intel_whitelist_spec),
            state=dict(choices=['present', 'absent'], default='present', type='str'),
        )

        self.results = dict(
            changed=False,
            state=dict()
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None
        self.base_policy = None
        self.threat_intel_mode = None
        self.threat_intel_whitelist = None
        self.tags = None

        super(AzureRMFirewallPolicy, self).__init__(self.module_arg_spec,
                                                    supports_tags=True,
                                                    supports_check_mode=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False
        results = dict()
        firewall_policy_old = None
        firewall_policy_new = None
        update_ip_address = False
        update_fqdns = False

        # retrieve resource group to make sure it exists
        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        self.location = normalize_location_name(self.location)

        if self.base_policy:
            base_policy = self.parse_resource_to_dict(self.base_policy)
            self.base_policy = format_resource_id(val=base_policy['name'],
                                                  subscription_id=base_policy['subscription_id'],
                                                  namespace='Microsoft.Network',
                                                  types='firewallPolicies',
                                                  resource_group=base_policy['resource_group'])

        try:
            self.log('Fetching Firewall policy {0}'.format(self.name))
            firewall_policy_old = self.network_client.firewall_policies.get(self.resource_group, self.name)
            # serialize object into a dictionary
            results = self.firewallpolicy_to_dict(firewall_policy_old)
            if self.state == 'present':
                changed = False
                update_tags, results['tags'] = self.update_tags(results['tags'])
                if update_tags:
                    changed = True
                self.tags = results['tags']
                if self.base_policy is not None:
                    if ('base_policy' not in results and self.base_policy != "") or \
                            ('base_policy' in results and self.base_policy != results['base_policy']['id']):
                        changed = True
                        results['base_policy'] = self.base_policy
                if self.threat_intel_mode is not None and \
                        self.threat_intel_mode.lower() != results['threat_intel_mode'].lower():
                    changed = True
                    results['threat_intel_mode'] = self.threat_intel_mode
                if self.threat_intel_whitelist is not None:
                    if 'threat_intel_whitelist' not in results:
                        changed = True
                        results['threat_intel_whitelist'] = self.threat_intel_whitelist
                    else:
                        update_ip_addresses, results['threat_intel_whitelist']['ip_addresses'] = \
                            self.update_values(results['threat_intel_whitelist']['ip_addresses']
                                               if 'ip_addresses' in results['threat_intel_whitelist'] else [],
                                               self.threat_intel_whitelist['ip_addresses']
                                               if self.threat_intel_whitelist['ip_addresses'] is not None else [],
                                               self.threat_intel_whitelist['append_ip_addresses'])
                        update_fqdns, results['threat_intel_whitelist']['fqdns'] = \
                            self.update_values(results['threat_intel_whitelist']['fqdns']
                                               if 'fqdns' in results['threat_intel_whitelist'] else [],
                                               self.threat_intel_whitelist['fqdns']
                                               if self.threat_intel_whitelist['fqdns'] is not None else [],
                                               self.threat_intel_whitelist['append_fqdns'])
                        if update_ip_addresses:
                            changed = True
                        self.threat_intel_whitelist['ip_addresses'] = results['threat_intel_whitelist']['ip_addresses']
                        if update_fqdns:
                            changed = True
                        self.threat_intel_whitelist['fqdns'] = results['threat_intel_whitelist']['fqdns']
            elif self.state == 'absent':
                changed = True

        except ResourceNotFoundError:
            if self.state == 'present':
                changed = True
            else:
                changed = False

        self.results['changed'] = changed
        self.results['state'] = results

        if self.check_mode:
            return self.results

        if changed:
            if self.state == 'present':
                # create or update firewall policy
                firewall_policy_new = \
                    self.network_models.FirewallPolicy(location=self.location,
                                                       threat_intel_mode=self.threat_intel_mode)
                if self.base_policy:
                    firewall_policy_new.base_policy = \
                        self.network_models.FirewallPolicy(id=self.base_policy)
                if self.threat_intel_whitelist:
                    firewall_policy_new.threat_intel_whitelist = self.network_models.FirewallPolicyThreatIntelWhitelist(
                        ip_addresses=self.threat_intel_whitelist['ip_addresses'],
                        fqdns=self.threat_intel_whitelist['fqdns']
                    )
                if self.tags:
                    firewall_policy_new.tags = self.tags
                self.results['state'] = self.create_or_update_firewallpolicy(firewall_policy_new)

            elif self.state == 'absent':
                # delete firewall policy
                self.delete_firewallpolicy()
                self.results['state'] = 'Deleted'

        return self.results

    def create_or_update_firewallpolicy(self, firewall_policy):
        try:
            # create a firewall policy
            response = self.network_client.firewall_policies.begin_create_or_update(resource_group_name=self.resource_group,
                                                                                    firewall_policy_name=self.name,
                                                                                    parameters=firewall_policy)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error creating or updating Firewall policy {0} - {1}".format(self.name, str(exc)))
        return self.firewallpolicy_to_dict(response)

    def delete_firewallpolicy(self):
        try:
            # delete a firewall policy
            response = self.network_client.firewall_policies.begin_delete(resource_group_name=self.resource_group,
                                                                          firewall_policy_name=self.name)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error deleting Firewall policy {0} - {1}".format(self.name, str(exc)))
        return response

    def update_values(self, existing_values, param_values, append):
        # comparing input values with existing values for given parameter

        new_values = copy.copy(existing_values)
        changed = False

        # check add or update
        for item in param_values:
            if item not in new_values:
                changed = True
                new_values.append(item)
        # check remove
        if not append:
            for item in existing_values:
                if item not in param_values:
                    new_values.remove(item)
                    changed = True
        return changed, new_values

    def firewallpolicy_to_dict(self, firewallpolicy):
        result = firewallpolicy.as_dict()
        result['tags'] = firewallpolicy.tags
        return result


def main():
    AzureRMFirewallPolicy()


if __name__ == '__main__':
    main()
