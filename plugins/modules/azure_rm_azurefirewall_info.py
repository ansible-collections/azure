#!/usr/bin/python
#
# Copyright (c) 2019 Liu Qingyi, (@smile37773)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_azurefirewall_info
version_added: '0.1.2'
short_description: Get AzureFirewall info
description:
    - Get info of AzureFirewall.
options:
    resource_group:
        description:
            - The name of the resource group. Required when I(name) is provided.
        type: str
    name:
        description:
            - Resource name. When set, I(resource_group) is required.
        type: str
    tags:
        description:
            - Limit the results by providing resource tags.
        type: list
        elements: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Liu Qingyi (@smile37773)

'''

EXAMPLES = '''
- name: List all Azure Firewalls for a given subscription
  azure_rm_azurefirewall_info:
- name: List all Azure Firewalls for a given resource group
  azure_rm_azurefirewall_info:
    resource_group: myResourceGroup
- name: Get Azure Firewall
  azure_rm_azurefirewall_info:
    resource_group: myResourceGroup
    name: myAzureFirewall
'''

RETURN = '''
firewalls:
    description:
        - A list of Azure Firewalls matching the query.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description:
                - Fully qualified Azure resource ID.
            type: str
            sample: >-
                /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/azureFirewalls/myAzureFirewall
        name:
            description:
                - Firewall resource name.
            type: str
            sample: myAzureFirewall
        resource_group:
            description:
                - Name of the resource group containing the firewall.
            type: str
            sample: myResourceGroup
        location:
            description:
                - Azure region.
            type: str
            sample: eastus
        provisioning_state:
            description:
                - Provisioning state of the resource.
            type: str
            sample: Succeeded
        application_rule_collections:
            description:
                - Collection of application rule collections used by the firewall.
            type: list
        nat_rule_collections:
            description:
                - Collection of NAT rule collections used by the firewall.
            type: list
        network_rule_collections:
            description:
                - Collection of network rule collections used by the firewall.
            type: list
        ip_configurations:
            description:
                - IP configuration of the firewall.
            type: list
        additional_properties:
            description:
                - Additional properties used to further configure the firewall.
                - Includes DNS proxy settings such as C(Network.DNS.EnableProxy) and C(Network.DNS.Servers).
            type: dict
        sku:
            description:
                - The SKU of the Azure Firewall (for example C(AZFW_VNet) / C(Standard)).
            type: dict
        threat_intel_mode:
            description:
                - Operation mode for threat intelligence.
            type: str
            sample: Alert
        tags:
            description:
                - Resource tags.
            type: dict
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            type: str
        type:
            description:
                - Azure resource type.
            type: str
            sample: Microsoft.Network/azureFirewalls
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAzureFirewallsInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            tags=dict(type='list', elements='str'),
        )

        self.resource_group = None
        self.name = None
        self.tags = None

        self.results = dict(changed=False, firewalls=[])

        super(AzureRMAzureFirewallsInfo, self).__init__(
            self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True,
        )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            if self.resource_group is None:
                self.fail("Parameter error: resource_group is required when name is provided.")
            results = self.get_item()
        elif self.resource_group is not None:
            results = self.list_resource_group()
        else:
            results = self.list_all()

        self.results['firewalls'] = [self.firewall_to_dict(item) for item in results]
        return self.results

    def get_item(self):
        try:
            item = self.network_client.azure_firewalls.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            return []
        if self.has_tags(item.tags, self.tags):
            return [item]
        return []

    def list_resource_group(self):
        try:
            response = self.network_client.azure_firewalls.list(self.resource_group)
        except Exception as exc:
            self.fail("Failed to list Azure Firewalls in resource group {0}: {1}".format(self.resource_group, str(exc)))
        return [item for item in response if self.has_tags(item.tags, self.tags)]

    def list_all(self):
        try:
            response = self.network_client.azure_firewalls.list_all()
        except Exception as exc:
            self.fail("Failed to list Azure Firewalls in subscription: {0}".format(str(exc)))
        return [item for item in response if self.has_tags(item.tags, self.tags)]

    def firewall_to_dict(self, firewall):
        result = firewall.as_dict()
        rg = None
        if firewall.id:
            # ARM ID: /subscriptions/<sub>/resourceGroups/<rg>/providers/...
            parts = firewall.id.split('/')
            if len(parts) > 4 and parts[3].lower() == 'resourcegroups':
                rg = parts[4]
        result['resource_group'] = self.resource_group or rg
        return result


def main():
    AzureRMAzureFirewallsInfo()


if __name__ == '__main__':
    main()
