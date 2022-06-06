#!/usr/bin/python
#
# Copyright (c) 2021 Aparna Patil(@aparna-patil)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_firewallpolicy_info

version_added: "1.13.0"

short_description: Get firewall policy facts

description:
    - Get facts for specified firewall policy or all firewall policies in a given resource group.

options:
    resource_group:
        description:
            - Name of the resource group.
        type: str
    name:
        description:
            - Name of the Firewall policy.
        type: str
    tags:
        description:
            - Limit the results by providing resource tags.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Aparna Patil (@aparna-patil)

'''

EXAMPLES = '''
- name: Get facts for one firewall policy
  azure_rm_firewallpolicy_info:
    resource_group: myAzureResourceGroup
    name: myfirewallpolicy

- name: Get facts for all firewall policies in resource group
  azure_rm_firewallpolicy_info:
    resource_group: myAzureResourceGroup
'''

RETURN = '''
firewallpolicies:
    description:
        - Gets a list of firewall policies.
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "base_policy": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/MyAzureResourceGroup/
                            providers/Microsoft.Network/firewallPolicies/firewallparentpolicy",
            "child_policies": [],
            "dns_settings": {
                "enable_proxy": null,
                "require_proxy_for_network_rules": null,
                "servers": []
            },
            "etag": "a7b62add-9a6d-42bc-80ff-c288799e3561",
            "firewalls": [],
            "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/MyAzureResourceGroup/providers/
                   Microsoft.Network/firewallPolicies/myfirewallpolicy",
            "location": "eastus",
            "name": "myfirewallpolicy",
            "provisioning_state": "Succeeded",
            "rule_collection_groups": [
                {
                    "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/MyAzureResourceGroup/
                           providers/Microsoft.Network/firewallPolicies/myfirewallpolicy/
                           ruleCollectionGroups/DefaultNetworkRuleCollectionGroup"
                }
            ],
            "tags": {
                "key1": "value1"
            },
            "threat_intel_mode": "Deny",
            "threat_intel_whitelist": {
                "fqdns": [
                    "*.microsoft.com"
                ],
                "ip_addresses": [
                    "10.0.0.1"
                ]
            },
            "type": "Microsoft.Network/FirewallPolicies"
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.common import AzureMissingResourceHttpError, AzureHttpError
except Exception:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'FirewallPolicy'


class AzureRMFirewallPolicyInfo(AzureRMModuleBase):

    def __init__(self):

        # define user inputs variables
        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        # store the results of the module operation
        self.results = dict(
            changed=False
        )

        self.name = None
        self.resource_group = None
        self.tags = None

        super(AzureRMFirewallPolicyInfo, self).__init__(self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        facts_module=True,
                                                        supports_tags=False)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        results = []
        # list the conditions and results to return based on user input
        if self.name is not None:
            # if firewall policy name is provided, then return facts about that specific firewall policy
            results = self.get_item()
        elif self.resource_group:
            # all the firewall policies listed in specific resource group
            results = self.list_resource_group()
        else:
            # all the firewall policies in a subscription
            results = self.list_items()

        self.results['firewallpolicies'] = self.curated_items(results)

        return self.results

    def get_item(self):
        self.log('Get properties for Firewall policy - {0}'.format(self.name))
        item = None
        results = []
        # get specific Firewall policy
        try:
            item = self.network_client.firewall_policies.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            pass

        # serialize result
        if item and self.has_tags(item.tags, self.tags):
            results = [item]
        return results

    def list_resource_group(self):
        self.log('List all Firewall policies for resource group - {0}'.format(self.resource_group))
        try:
            response = self.network_client.firewall_policies.list(self.resource_group)
        except Exception as exc:
            self.fail("Failed to list firewall policies for resource group {0} - {1}".format(self.resource_group,
                                                                                             str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def list_items(self):
        self.log('List all the Firewall Policies in a subscription.')
        try:
            response = self.network_client.firewall_policies.list_all()
        except Exception as exc:
            self.fail("Failed to list all items - {0}".format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def curated_items(self, raws):
        return [self.firewallpolicy_to_dict(item) for item in raws] if raws else []

    def firewallpolicy_to_dict(self, firewallpolicy):
        result = dict(
            id=firewallpolicy.id,
            name=firewallpolicy.name,
            location=firewallpolicy.location,
            tags=firewallpolicy.tags,
            rule_collection_groups=[dict(id=x.id) for x in firewallpolicy.rule_collection_groups],
            provisioning_state=firewallpolicy.provisioning_state,
            base_policy=firewallpolicy.base_policy.id if firewallpolicy.base_policy is not None else None,
            firewalls=[dict(id=x.id) for x in firewallpolicy.firewalls],
            child_policies=[dict(id=x.id) for x in firewallpolicy.child_policies],
            threat_intel_mode=firewallpolicy.threat_intel_mode,
            threat_intel_whitelist=dict(
                ip_addresses=firewallpolicy.threat_intel_whitelist.ip_addresses,
                fqdns=firewallpolicy.threat_intel_whitelist.fqdns
            ) if firewallpolicy.threat_intel_whitelist is not None else dict(),
            dns_settings=dict(
                enable_proxy=firewallpolicy.dns_settings.enable_proxy,
                servers=firewallpolicy.dns_settings.servers,
                require_proxy_for_network_rules=firewallpolicy.dns_settings.require_proxy_for_network_rules
            )if firewallpolicy.dns_settings is not None else dict(),
            etag=firewallpolicy.etag,
            type=firewallpolicy.type
        )
        return result


def main():
    AzureRMFirewallPolicyInfo()


if __name__ == '__main__':
    main()
