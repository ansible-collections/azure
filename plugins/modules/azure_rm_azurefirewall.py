#!/usr/bin/python
#
# Copyright (c) 2019 Zim Kalinowski, (@zikalino), Jurijs Fadejevs (@needgithubid)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_azurefirewall
version_added: '0.1.2'
short_description: Manage Azure Firewall instance
description:
    - Create, update and delete instance of Azure Firewall.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - The name of the Azure Firewall.
        required: true
        type: str
    location:
        description:
            - Resource location.
        type: str
    application_rule_collections:
        description:
            - Collection of application rule collections used by Azure Firewall.
        type: list
        elements: dict
        suboptions:
            priority:
                description:
                    - Priority of the application rule collection resource.
                type: int
            action:
                description:
                    - The action type of a rule collection.
                choices:
                    - allow
                    - deny
                type: str
            rules:
                description:
                    - Collection of rules used by a application rule collection.
                type: list
                elements: raw
                suboptions:
                    name:
                        description:
                            - Name of the application rule.
                        type: str
                    description:
                        description:
                            - Description of the rule.
                        type: str
                    source_addresses:
                        description:
                            - List of source IP addresses for this rule.
                        type: list
                        elements: str
                    protocols:
                        description:
                            - Array of ApplicationRuleProtocols.
                        elements: dict
                        type: list
                        suboptions:
                            type:
                                description:
                                    - The type of the protocols.
                                type: str
                            port:
                                description:
                                    - The ports of the protocols.
                                type: str
                    target_fqdns:
                        description:
                            - List of FQDNs for this rule.
                        type: list
                        elements: raw
                    fqdn_tags:
                        description:
                            - List of FQDN Tags for this rule.
                        type: list
                        elements: raw
            name:
                description:
                    - Gets name of the resource that is unique within a resource group.
                    - This name can be used to access the resource.
                type: str
    nat_rule_collections:
        description:
            - Collection of NAT rule collections used by Azure Firewall.
        type: list
        elements: dict
        suboptions:
            priority:
                description:
                    - Priority of the NAT rule collection resource.
                type: int
            action:
                description:
                    - The action type of a NAT rule collection
                choices:
                    - snat
                    - dnat
                type: str
            rules:
                description:
                    - Collection of rules used by a NAT rule collection.
                type: list
                elements: dict
                suboptions:
                    name:
                        description:
                            - Name of the NAT rule.
                        type: str
                    description:
                        description:
                            - Description of the rule.
                        type: str
                    source_addresses:
                        description:
                            - List of source IP addresses for this rule.
                        type: list
                        elements: str
                    destination_addresses:
                        description:
                            - List of destination IP addresses for this rule.
                        type: list
                        elements: str
                    destination_ports:
                        description:
                            - List of destination ports.
                        type: list
                        elements: str
                    protocols:
                        description:
                            - Array of AzureFirewallNetworkRuleProtocols applicable to this NAT rule.
                        type: list
                        elements: raw
                    translated_address:
                        description:
                            - The translated address for this NAT rule.
                        type: str
                    translated_port:
                        description:
                            - The translated port for this NAT rule.
                        type: str
            name:
                description:
                    - Gets name of the resource that is unique within a resource group.
                    - This name can be used to access the resource.
                type: str
    network_rule_collections:
        description:
            - Collection of network rule collections used by Azure Firewall.
        type: list
        elements: dict
        suboptions:
            priority:
                description:
                    - Priority of the network rule collection resource.
                type: int
            action:
                description:
                    - The action type of a rule collection.
                type: str
                choices:
                    - allow
                    - deny
            rules:
                description:
                    - Collection of rules used by a network rule collection.
                type: list
                elements: dict
                suboptions:
                    name:
                        description:
                            - Name of the network rule.
                        type: str
                    description:
                        description:
                            - Description of the rule.
                        type: str
                    protocols:
                        description:
                            - Array of AzureFirewallNetworkRuleProtocols.
                        type: list
                        elements: raw
                    source_addresses:
                        description:
                            - List of source IP addresses for this rule.
                        type: list
                        elements: str
                    destination_addresses:
                        description:
                            - List of destination IP addresses.
                        type: list
                        elements: str
                    destination_ports:
                        description:
                            - List of destination ports.
                        type: list
                        elements: str
                    destination_fqdns:
                        description:
                            - List of destination FQDNS.
                        type: list
                        elements: str
            name:
                description:
                    - Gets name of the resource that is unique within a resource group.
                    - This name can be used to access the resource.
                type: str
    ip_configurations:
        description:
            - IP configuration of the Azure Firewall resource.
        type: list
        elements: dict
        suboptions:
            subnet:
                description:
                    - Existing subnet.
                    - It can be a string containing subnet resource ID.
                    - It can be a dictionary containing I(name), I(virtual_network_name) and optionally I(resource_group) .
                type: raw
            public_ip_address:
                description:
                    - Existing public IP address.
                    - It can be a string containing resource ID.
                    - It can be a string containing a name in current resource group.
                    - It can be a dictionary containing I(name) and optionally I(resource_group).
                type: raw
            name:
                description:
                    - Name of the resource that is unique within a resource group.
                    - This name can be used to access the resource.
                type: str
    dns_servers:
        description:
            - List of custom DNS server IP addresses used by the firewall.
        type: list
        elements: str
    dns_proxy_enabled:
        description:
            - Whether DNS proxy is enabled on the firewall.
            - When C(true), the firewall listens on port 53 and forwards DNS queries to the addresses in I(dns_servers).
        type: bool
    state:
        description:
            - Assert the state of the AzureFirewall.
            - Use C(present) to create or update an AzureFirewall and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Zim Kalinowski (@zikalino)
    - Jurijs Fadejevs (@needgithubid)

'''

EXAMPLES = '''
- name: Create Azure Firewall
  azure_rm_azurefirewall:
    resource_group: myResourceGroup
    name: myAzureFirewall
    tags:
      key1: value1
    application_rule_collections:
      - priority: 110
        action: deny
        rules:
          - name: rule1
            description: Deny inbound rule
            source_addresses:
              - 216.58.216.164
              - 10.0.0.0/24
            protocols:
              - type: https
                port: '443'
            target_fqdns:
              - www.test.com
        name: apprulecoll
    nat_rule_collections:
      - priority: 112
        action: dnat
        rules:
          - name: DNAT-HTTPS-traffic
            description: D-NAT all outbound web traffic for inspection
            source_addresses:
              - '*'
            destination_addresses:
              - 1.2.3.4
            destination_ports:
              - '443'
            protocols:
              - tcp
            translated_address: 1.2.3.5
            translated_port: '8443'
        name: natrulecoll
    network_rule_collections:
      - priority: 112
        action: deny
        name: netrulecoll
        rules:
          - name: L4-traffic
            description: Block traffic based on source IPs and ports
            protocols:
              - tcp
            source_addresses:
              - 192.168.1.1-192.168.1.12
              - 10.1.4.12-10.1.4.255
            destination_addresses:
              - '*'
            destination_ports:
              - 443-444
              - '8443'
          - name: L4-traffic-destination_fqdns
            description: Block traffic based on source IPs and ports to amazon
            protocols:
              - tcp
            source_addresses:
              - 10.2.4.12-10.2.4.255
            destination_fqdns:
              - 'www.test.com'
            destination_ports:
              - 443-444
              - '8443'
    ip_configurations:
      - subnet: >-
          /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup
          /providers/Microsoft.Network/virtualNetworks/myVirtualNetwork
          /subnets/AzureFirewallSubnet
        public_ip_address: >-
          /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup
          /providers/Microsoft.Network/publicIPAddresses/
          myPublicIpAddress
        name: azureFirewallIpConfiguration
- name: Delete Azure Firewall
  azure_rm_azurefirewall:
    resource_group: myResourceGroup
    name: myAzureFirewall
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the Azure Firewall.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The Azure Firewall resource ID.
            returned: always
            type: str
            sample: >-
                /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/azureFirewalls/myAzureFirewall
        name:
            description:
                - The Azure Firewall name.
            returned: always
            type: str
            sample: myAzureFirewall
        location:
            description:
                - The Azure region where the firewall lives.
            returned: always
            type: str
            sample: eastus
        provisioning_state:
            description:
                - The provisioning state of the resource.
            returned: always
            type: str
            sample: Succeeded
        application_rule_collections:
            description:
                - Collection of application rule collections used by the firewall.
            returned: always
            type: list
        nat_rule_collections:
            description:
                - Collection of NAT rule collections used by the firewall.
            returned: always
            type: list
        network_rule_collections:
            description:
                - Collection of network rule collections used by the firewall.
            returned: always
            type: list
        ip_configurations:
            description:
                - IP configuration of the firewall.
            returned: always
            type: list
        additional_properties:
            description:
                - Additional properties used to further configure the firewall (for example DNS proxy settings).
            returned: always
            type: dict
        sku:
            description:
                - The SKU of the Azure Firewall (for example C(AZFW_VNet) / C(Standard)).
            returned: always
            type: dict
        threat_intel_mode:
            description:
                - Operation mode for threat intelligence.
            returned: always
            type: str
            sample: Alert
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
        type:
            description:
                - The Azure resource type.
            returned: always
            type: str
            sample: Microsoft.Network/azureFirewalls
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import format_resource_id
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
    from azure.mgmt.core.tools import is_valid_resource_id, resource_id
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAzureFirewalls(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
            ),
            application_rule_collections=dict(
                type='list',
                elements='dict',
                options=dict(
                    priority=dict(
                        type='int',
                    ),
                    action=dict(
                        type='str',
                        choices=['allow',
                                 'deny'],
                    ),
                    rules=dict(
                        type='list',
                        elements='raw',
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            description=dict(
                                type='str'
                            ),
                            source_addresses=dict(
                                type='list',
                                elements='str',
                            ),
                            protocols=dict(
                                type='list',
                                elements='dict',
                                options=dict(
                                    type=dict(
                                        type='str',
                                    ),
                                    port=dict(
                                        type='str'
                                    )
                                )
                            ),
                            target_fqdns=dict(
                                type='list',
                                elements='raw',
                            ),
                            fqdn_tags=dict(
                                type='list',
                                elements='raw',
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            nat_rule_collections=dict(
                type='list',
                elements='dict',
                options=dict(
                    priority=dict(
                        type='int',
                    ),
                    action=dict(
                        type='str',
                        choices=['snat',
                                 'dnat'],
                    ),
                    rules=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            description=dict(
                                type='str'
                            ),
                            source_addresses=dict(
                                type='list',
                                elements='str',
                            ),
                            destination_addresses=dict(
                                type='list',
                                elements='str',
                            ),
                            destination_ports=dict(
                                type='list',
                                elements='str',
                            ),
                            protocols=dict(
                                type='list',
                                elements='raw'
                            ),
                            translated_address=dict(
                                type='str',
                            ),
                            translated_port=dict(
                                type='str',
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            network_rule_collections=dict(
                type='list',
                elements='dict',
                options=dict(
                    priority=dict(
                        type='int',
                    ),
                    action=dict(
                        type='str',
                        choices=['allow',
                                 'deny'],
                    ),
                    rules=dict(
                        type='list',
                        elements='dict',
                        mutually_exclusive=[('destination_fqdns', 'destination_addresses')],
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            description=dict(
                                type='str'
                            ),
                            protocols=dict(
                                type='list',
                                elements='raw'
                            ),
                            source_addresses=dict(
                                type='list',
                                elements='str',
                            ),
                            destination_addresses=dict(
                                type='list',
                                elements='str',
                            ),
                            destination_fqdns=dict(
                                type='list',
                                elements='str',
                            ),
                            destination_ports=dict(
                                type='list',
                                elements='str',
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            ip_configurations=dict(
                type='list',
                elements='dict',
                options=dict(
                    subnet=dict(
                        type='raw',
                    ),
                    public_ip_address=dict(
                        type='raw',
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            dns_servers=dict(
                type='list',
                elements='str',
            ),
            dns_proxy_enabled=dict(
                type='bool',
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.application_rule_collections = None
        self.nat_rule_collections = None
        self.network_rule_collections = None
        self.ip_configurations = None
        self.dns_servers = None
        self.dns_proxy_enabled = None
        self.state = None
        self.tags = None

        self.results = dict(changed=False, state=dict())

        super(AzureRMAzureFirewalls, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        if self.state == 'present':
            resource_group = self.get_resource_group(self.resource_group)
            if not self.location:
                self.location = resource_group.location

        existing = self.get_firewall()
        changed = False

        if self.state == 'present':
            desired = self.build_firewall_model()
            if existing is None:
                changed = True
            else:
                existing_addl = getattr(existing, 'additional_properties', None) or {}
                desired_addl = desired.additional_properties or {}
                if existing_addl or desired_addl:
                    merged = dict(existing_addl)
                    merged.update(desired_addl)
                    desired.additional_properties = merged

                # Back-fill every top-level SDK field
                for field in ('application_rule_collections', 'nat_rule_collections',
                              'network_rule_collections', 'ip_configurations',
                              'sku', 'firewall_policy', 'threat_intel_mode',
                              'virtual_hub', 'zones', 'hub_ip_addresses',
                              'management_ip_configuration', 'autoscale_configuration'):
                    if getattr(desired, field, None) is None:
                        setattr(desired, field, getattr(existing, field, None))

                update_tags, new_tags = self.update_tags(existing.tags or {})
                if update_tags:
                    changed = True
                    desired.tags = new_tags
                elif self.tags is None:
                    desired.tags = existing.tags

                new_dict = desired.as_dict()
                old_dict = existing.as_dict()
                self._sort_firewall_dict(new_dict)
                self._sort_firewall_dict(old_dict)
                if not self.default_compare({}, new_dict, old_dict, '', dict(compare=[])):
                    changed = True

            if changed and not self.check_mode:
                existing = self.create_or_update_firewall(desired)
        else:
            if existing is not None:
                changed = True
                if not self.check_mode:
                    self.delete_firewall()
                    existing = None

        self.results['changed'] = changed
        self.results['state'] = existing.as_dict() if existing else {}
        return self.results

    def get_firewall(self):
        try:
            return self.network_client.azure_firewalls.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            return None

    def create_or_update_firewall(self, model):
        try:
            response = self.network_client.azure_firewalls.begin_create_or_update(
                resource_group_name=self.resource_group,
                azure_firewall_name=self.name,
                parameters=model,
            )
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
            return response
        except Exception as exc:
            self.fail("Error creating or updating Azure Firewall {0}: {1}".format(self.name, str(exc)))

    def delete_firewall(self):
        try:
            response = self.network_client.azure_firewalls.begin_delete(
                resource_group_name=self.resource_group,
                azure_firewall_name=self.name,
            )
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error deleting Azure Firewall {0}: {1}".format(self.name, str(exc)))

    def build_firewall_model(self):
        models = self.network_models

        params = dict(location=self.location)
        if self.tags is not None:
            params['tags'] = self.tags

        if self.application_rule_collections is not None:
            params['application_rule_collections'] = [
                self.build_application_rule_collection(item)
                for item in self.application_rule_collections
            ]
        if self.nat_rule_collections is not None:
            params['nat_rule_collections'] = [
                self.build_nat_rule_collection(item)
                for item in self.nat_rule_collections
            ]
        if self.network_rule_collections is not None:
            params['network_rule_collections'] = [
                self.build_network_rule_collection(item)
                for item in self.network_rule_collections
            ]
        if self.ip_configurations is not None:
            params['ip_configurations'] = [
                self.build_ip_configuration(item)
                for item in self.ip_configurations
            ]

        additional = {}
        if self.dns_servers is not None:
            additional['Network.DNS.Servers'] = ','.join(self.dns_servers)
        if self.dns_proxy_enabled is not None:
            additional['Network.DNS.EnableProxy'] = 'true' if self.dns_proxy_enabled else 'false'
        if additional:
            params['additional_properties'] = additional

        return models.AzureFirewall(**params)

    def build_application_rule_collection(self, item):
        models = self.network_models
        # Arg-spec accepts lowercase enums; SDK expects title-case (application) or upper-case (network).
        action = models.AzureFirewallRCAction(type=str(item['action']).title()) if item.get('action') else None
        rules = None
        if item.get('rules') is not None:
            rules = [
                models.AzureFirewallApplicationRule(
                    name=r.get('name'),
                    description=r.get('description'),
                    source_addresses=r.get('source_addresses'),
                    target_fqdns=r.get('target_fqdns'),
                    fqdn_tags=r.get('fqdn_tags'),
                    protocols=[
                        models.AzureFirewallApplicationRuleProtocol(
                            protocol_type=str(p['type']).title() if p.get('type') is not None else None,
                            port=int(p['port']) if p.get('port') is not None else None,
                        )
                        for p in (r.get('protocols') or [])
                    ] if r.get('protocols') is not None else None,
                )
                for r in item['rules']
            ]
        return models.AzureFirewallApplicationRuleCollection(
            name=item.get('name'),
            priority=item.get('priority'),
            action=action,
            rules=rules,
        )

    def build_nat_rule_collection(self, item):
        models = self.network_models
        action = models.AzureFirewallNatRCAction(type=str(item['action']).title()) if item.get('action') else None
        rules = None
        if item.get('rules') is not None:
            rules = [
                models.AzureFirewallNatRule(
                    name=r.get('name'),
                    description=r.get('description'),
                    source_addresses=r.get('source_addresses'),
                    destination_addresses=r.get('destination_addresses'),
                    destination_ports=r.get('destination_ports'),
                    protocols=[self.normalize_network_protocol(p) for p in r['protocols']] if r.get('protocols') is not None else None,
                    translated_address=r.get('translated_address'),
                    translated_port=r.get('translated_port'),
                )
                for r in item['rules']
            ]
        return models.AzureFirewallNatRuleCollection(
            name=item.get('name'),
            priority=item.get('priority'),
            action=action,
            rules=rules,
        )

    def build_network_rule_collection(self, item):
        models = self.network_models
        action = models.AzureFirewallRCAction(type=str(item['action']).title()) if item.get('action') else None
        rules = None
        if item.get('rules') is not None:
            rules = [
                models.AzureFirewallNetworkRule(
                    name=r.get('name'),
                    description=r.get('description'),
                    source_addresses=r.get('source_addresses'),
                    destination_addresses=r.get('destination_addresses'),
                    destination_ports=r.get('destination_ports'),
                    destination_fqdns=r.get('destination_fqdns'),
                    protocols=[self.normalize_network_protocol(p) for p in r['protocols']] if r.get('protocols') is not None else None,
                )
                for r in item['rules']
            ]
        return models.AzureFirewallNetworkRuleCollection(
            name=item.get('name'),
            priority=item.get('priority'),
            action=action,
            rules=rules,
        )

    def build_ip_configuration(self, item):
        models = self.network_models
        subnet_id = self.resolve_subnet_id(item.get('subnet'))
        pip = item.get('public_ip_address')
        pip_id = None
        if isinstance(pip, str):
            pip_id = format_resource_id(pip, self.subscription_id, 'Microsoft.Network', 'publicIPAddresses', self.resource_group)
        elif isinstance(pip, dict):
            if pip.get('id'):
                pip_id = pip['id']
            elif pip.get('name'):
                pip_id = format_resource_id(pip['name'], self.subscription_id, 'Microsoft.Network', 'publicIPAddresses',
                                            pip.get('resource_group') or self.resource_group)
            else:
                self.fail("The ip_configuration's public_ip_address dict must contain 'id' or 'name'")
        return models.AzureFirewallIPConfiguration(
            name=item.get('name'),
            subnet=models.SubResource(id=subnet_id) if subnet_id else None,
            public_ip_address=models.SubResource(id=pip_id) if pip_id else None,
        )

    def normalize_network_protocol(self, proto):
        # SDK enum values: 'TCP', 'UDP', 'ICMP', 'Any'.
        if not isinstance(proto, str):
            return proto
        lower = proto.lower()
        if lower == 'any':
            return 'Any'
        return lower.upper()

    def _sort_firewall_dict(self, fw):
        for col_key in ('application_rule_collections', 'nat_rule_collections',
                        'network_rule_collections'):
            cols = fw.get(col_key)
            if cols:
                cols.sort(key=lambda c: c.get('name') or '')
                for c in cols:
                    rules = c.get('rules')
                    if rules:
                        rules.sort(key=lambda r: r.get('name') or '')
        ip = fw.get('ip_configurations')
        if ip:
            ip.sort(key=lambda x: x.get('name') or '')

    def resolve_subnet_id(self, val):
        if val is None:
            return None
        if isinstance(val, str):
            if is_valid_resource_id(val):
                return val
            self.fail("The ip_configuration's subnet must be a full ARM resource ID or a dict with virtual_network_name and name; got: '{0}'".format(val))
        if isinstance(val, dict):
            if val.get('id'):
                return val['id']
            if val.get('virtual_network_name') and val.get('name'):
                return resource_id(
                    subscription=self.subscription_id,
                    resource_group=val.get('resource_group') or self.resource_group,
                    namespace='Microsoft.Network',
                    type='virtualNetworks',
                    name=val['virtual_network_name'],
                    child_type_1='subnets',
                    child_name_1=val['name'],
                )
        self.fail("The ip_configuration's subnet config error")


def main():
    AzureRMAzureFirewalls()


if __name__ == '__main__':
    main()
