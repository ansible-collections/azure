#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_firewallpolicyrulecollectiongroup
version_added: "3.19.0"
short_description: Manage rule collection groups of an Azure Firewall Policy
description:
    - Create, update or delete a rule collection group of an Azure Firewall Policy.
    - A rule collection group hosts an ordered list of filter and/or NAT rule collections, each of which
      contains application, network or NAT rules.
options:
    resource_group:
        description:
            - Name of the resource group.
        required: true
        type: str
    firewall_policy_name:
        description:
            - The name of the parent firewall policy.
        required: true
        type: str
    name:
        description:
            - The name of the rule collection group.
        required: true
        type: str
    priority:
        description:
            - Priority of the rule collection group resource.
            - Valid values are between C(100) and C(65000).
        type: int
    rule_collections:
        description:
            - Group of firewall policy rule collections.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Name of the rule collection.
                required: true
                type: str
            priority:
                description:
                    - Priority of the rule collection.
                    - Valid values are between C(100) and C(65000).
                type: int
            rule_collection_type:
                description:
                    - The type of the rule collection.
                required: true
                type: str
                choices:
                    - filter
                    - nat
            action:
                description:
                    - The action of the rule collection.
                    - Use C(allow) or C(deny) for filter collections.
                    - Use C(dnat) for nat collections.
                type: str
                choices:
                    - allow
                    - deny
                    - dnat
            rules:
                description:
                    - Rules included in this rule collection.
                type: list
                elements: dict
                suboptions:
                    name:
                        description:
                            - Name of the rule.
                        required: true
                        type: str
                    description:
                        description:
                            - Description of the rule.
                        type: str
                    rule_type:
                        description:
                            - Type of the rule.
                            - A filter collection may contain C(application) or C(network) rules.
                            - A nat collection may contain C(nat) rules.
                        required: true
                        type: str
                        choices:
                            - application
                            - network
                            - nat
                    source_addresses:
                        description:
                            - List of source IP addresses or CIDR ranges for this rule.
                        type: list
                        elements: str
                    destination_addresses:
                        description:
                            - List of destination IP addresses, CIDR ranges or service tags for this rule.
                        type: list
                        elements: str
                    source_ip_groups:
                        description:
                            - List of source IP group resource IDs for this rule.
                        type: list
                        elements: str
                    ip_protocols:
                        description:
                            - List of IP protocols for this rule.
                            - Used by C(network) and C(nat) rules only.
                        type: list
                        elements: str
                        choices:
                            - Any
                            - TCP
                            - UDP
                            - ICMP
                    destination_ports:
                        description:
                            - List of destination ports for this rule.
                            - Used by C(network) and C(nat) rules only.
                        type: list
                        elements: str
                    destination_ip_groups:
                        description:
                            - List of destination IP group resource IDs for this rule.
                            - Used by C(network) rules only.
                        type: list
                        elements: str
                    destination_fqdns:
                        description:
                            - List of destination FQDNs for this rule.
                            - Used by C(network) rules only.
                        type: list
                        elements: str
                    protocols:
                        description:
                            - List of application protocols for this rule.
                            - Used by C(application) rules only.
                        type: list
                        elements: dict
                        suboptions:
                            type:
                                description:
                                    - Protocol type.
                                type: str
                                choices:
                                    - Http
                                    - Https
                            port:
                                description:
                                    - Port number for the protocol. Valid values are between C(0) and C(64000).
                                type: int
                    target_fqdns:
                        description:
                            - List of destination FQDNs for this rule.
                            - Used by C(application) rules only.
                        type: list
                        elements: str
                    target_urls:
                        description:
                            - List of destination URLs for this rule.
                            - Used by C(application) rules only.
                        type: list
                        elements: str
                    fqdn_tags:
                        description:
                            - List of FQDN tags for this rule.
                            - Used by C(application) rules only.
                        type: list
                        elements: str
                    web_categories:
                        description:
                            - List of destination Azure web categories for this rule.
                            - Used by C(application) rules only. Requires Premium tier firewall policy.
                        type: list
                        elements: str
                    terminate_tls:
                        description:
                            - Whether to terminate TLS connections for this rule.
                            - Used by C(application) rules only. Requires Premium tier firewall policy.
                        type: bool
                    http_headers_to_insert:
                        description:
                            - List of HTTP/S headers to insert.
                            - Used by C(application) rules only.
                        type: list
                        elements: dict
                        suboptions:
                            header_name:
                                description:
                                    - The name of the header.
                                type: str
                            header_value:
                                description:
                                    - The value of the header.
                                type: str
                    translated_address:
                        description:
                            - The translated address for this NAT rule.
                            - Used by C(nat) rules only.
                        type: str
                    translated_port:
                        description:
                            - The translated port for this NAT rule.
                            - Used by C(nat) rules only.
                        type: str
                    translated_fqdn:
                        description:
                            - The translated FQDN for this NAT rule.
                            - Used by C(nat) rules only.
                        type: str
    state:
        description:
            - Assert the state of the rule collection group.
            - Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Create a rule collection group with filter and NAT collections
  azure_rm_firewallpolicyrulecollectiongroup:
    resource_group: myResourceGroup
    firewall_policy_name: myFirewallPolicy
    name: myRuleCollectionGroup
    priority: 200
    rule_collections:
      - name: filterCollection
        priority: 300
        rule_collection_type: filter
        action: allow
        rules:
          - name: allowWebApp
            rule_type: application
            source_addresses:
              - 10.0.0.0/24
            protocols:
              - type: Https
                port: 443
            target_fqdns:
              - "*.microsoft.com"
          - name: allowNetwork
            rule_type: network
            ip_protocols:
              - TCP
            source_addresses:
              - 10.0.0.0/24
            destination_addresses:
              - 192.168.1.0/24
            destination_ports:
              - "443"
      - name: natCollection
        priority: 400
        rule_collection_type: nat
        action: dnat
        rules:
          - name: dnatRule
            rule_type: nat
            ip_protocols:
              - TCP
            source_addresses:
              - "*"
            destination_addresses:
              - 13.0.0.1
            destination_ports:
              - "443"
            translated_address: 10.0.0.10
            translated_port: "8443"

- name: Delete a rule collection group
  azure_rm_firewallpolicyrulecollectiongroup:
    resource_group: myResourceGroup
    firewall_policy_name: myFirewallPolicy
    name: myRuleCollectionGroup
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the rule collection group.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID of the rule collection group.
            returned: always
            type: str
            sample: "/subscriptions/xxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/firewallPolicies/
                     myFirewallPolicy/ruleCollectionGroups/myRuleCollectionGroup"
        name:
            description:
                - Name of the rule collection group.
            returned: always
            type: str
            sample: myRuleCollectionGroup
        priority:
            description:
                - Priority of the rule collection group.
            returned: always
            type: int
            sample: 200
        provisioning_state:
            description:
                - Provisioning state of the resource.
            returned: always
            type: str
            sample: Succeeded
        rule_collections:
            description:
                - Group of rule collections.
            returned: always
            type: list
            elements: dict
        etag:
            description:
                - Resource ETag.
            returned: always
            type: str
        type:
            description:
                - Resource type.
            returned: always
            type: str
            sample: Microsoft.Network/FirewallPolicies/RuleCollectionGroups
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # Handled in azure_rm_common
    pass


# Map user-facing lowercase action names to SDK enum values.
ACTION_TO_SDK = {
    'allow': 'Allow',
    'deny': 'Deny',
    'dnat': 'DNAT',
}


http_header_spec = dict(
    header_name=dict(type='str'),
    header_value=dict(type='str'),
)

application_protocol_spec = dict(
    type=dict(type='str', choices=['Http', 'Https']),
    port=dict(type='int'),
)

rule_spec = dict(
    name=dict(type='str', required=True),
    description=dict(type='str'),
    rule_type=dict(type='str', required=True, choices=['application', 'network', 'nat']),
    source_addresses=dict(type='list', elements='str'),
    destination_addresses=dict(type='list', elements='str'),
    source_ip_groups=dict(type='list', elements='str'),
    ip_protocols=dict(type='list', elements='str', choices=['Any', 'TCP', 'UDP', 'ICMP']),
    destination_ports=dict(type='list', elements='str'),
    destination_ip_groups=dict(type='list', elements='str'),
    destination_fqdns=dict(type='list', elements='str'),
    protocols=dict(type='list', elements='dict', options=application_protocol_spec),
    target_fqdns=dict(type='list', elements='str'),
    target_urls=dict(type='list', elements='str'),
    fqdn_tags=dict(type='list', elements='str'),
    web_categories=dict(type='list', elements='str'),
    terminate_tls=dict(type='bool'),
    http_headers_to_insert=dict(type='list', elements='dict', options=http_header_spec),
    translated_address=dict(type='str'),
    translated_port=dict(type='str'),
    translated_fqdn=dict(type='str'),
)

rule_collection_spec = dict(
    name=dict(type='str', required=True),
    priority=dict(type='int'),
    rule_collection_type=dict(type='str', required=True, choices=['filter', 'nat']),
    action=dict(type='str', choices=['allow', 'deny', 'dnat']),
    rules=dict(type='list', elements='dict', options=rule_spec),
)


class AzureRMFirewallPolicyRuleCollectionGroup(AzureRMModuleBaseExt):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            firewall_policy_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            priority=dict(type='int'),
            rule_collections=dict(type='list', elements='dict', options=rule_collection_spec),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.results = dict(
            changed=False,
            state=dict(),
        )

        self.resource_group = None
        self.firewall_policy_name = None
        self.name = None
        self.priority = None
        self.rule_collections = None
        self.state = None

        super(AzureRMFirewallPolicyRuleCollectionGroup, self).__init__(self.module_arg_spec,
                                                                       supports_tags=False,
                                                                       supports_check_mode=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec.keys():
            setattr(self, key, kwargs[key])

        self._validate_input()

        changed = False
        results = dict()
        existing = self.get_rule_collection_group()

        if existing is not None:
            results = existing.as_dict()
            if self.state == 'present':
                desired = self._build_rule_collection_group()
                if self._needs_update(existing, desired):
                    changed = True
            else:
                changed = True
        else:
            if self.state == 'present':
                changed = True

        self.results['changed'] = changed
        self.results['state'] = results

        if self.check_mode:
            return self.results

        if changed:
            if self.state == 'present':
                desired = self._build_rule_collection_group()
                self.results['state'] = self.create_or_update_rule_collection_group(desired)
            else:
                self.delete_rule_collection_group()
                self.results['state'] = 'Deleted'

        return self.results

    def _validate_input(self):
        if self.rule_collections is None:
            return
        for collection in self.rule_collections:
            ctype = collection.get('rule_collection_type')
            action = collection.get('action')
            if ctype == 'filter' and action not in (None, 'allow', 'deny'):
                self.fail("rule_collection '{0}': action must be 'allow' or 'deny' for a filter collection".format(
                    collection.get('name')))
            if ctype == 'nat' and action not in (None, 'dnat'):
                self.fail("rule_collection '{0}': action must be 'dnat' for a nat collection".format(
                    collection.get('name')))
            rules = collection.get('rules') or []
            for rule in rules:
                rtype = rule.get('rule_type')
                if ctype == 'filter' and rtype == 'nat':
                    self.fail("rule '{0}': nat rules cannot belong to a filter collection".format(
                        rule.get('name')))
                if ctype == 'nat' and rtype != 'nat':
                    self.fail("rule '{0}': only nat rules can belong to a nat collection".format(
                        rule.get('name')))
            # Azure requires all rules within a single collection to be of the same type
            rule_types = {r.get('rule_type') for r in rules}
            if len(rule_types) > 1:
                self.fail(
                    "rule_collection '{0}': all rules in a single collection must be of the same type; got {1}".format(
                        collection.get('name'), sorted(rule_types)))

    def get_rule_collection_group(self):
        try:
            return self.network_client.firewall_policy_rule_collection_groups.get(
                resource_group_name=self.resource_group,
                firewall_policy_name=self.firewall_policy_name,
                rule_collection_group_name=self.name,
            )
        except ResourceNotFoundError:
            return None

    def create_or_update_rule_collection_group(self, parameters):
        try:
            response = self.network_client.firewall_policy_rule_collection_groups.begin_create_or_update(
                resource_group_name=self.resource_group,
                firewall_policy_name=self.firewall_policy_name,
                rule_collection_group_name=self.name,
                parameters=parameters,
            )
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error creating or updating Firewall Policy Rule Collection Group {0}/{1} - {2}".format(
                self.firewall_policy_name, self.name, str(exc)))
        return response.as_dict()

    def delete_rule_collection_group(self):
        try:
            response = self.network_client.firewall_policy_rule_collection_groups.begin_delete(
                resource_group_name=self.resource_group,
                firewall_policy_name=self.firewall_policy_name,
                rule_collection_group_name=self.name,
            )
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error deleting Firewall Policy Rule Collection Group {0}/{1} - {2}".format(
                self.firewall_policy_name, self.name, str(exc)))
        return response

    def _build_rule_collection_group(self):
        rule_collections = [self._build_rule_collection(c) for c in (self.rule_collections or [])]
        return self.network_models.FirewallPolicyRuleCollectionGroup(
            name=self.name,
            priority=self.priority,
            rule_collections=rule_collections or None,
        )

    def _build_rule_collection(self, collection):
        name = collection['name']
        priority = collection.get('priority')
        rules = [self._build_rule(r) for r in (collection.get('rules') or [])]
        ctype = collection['rule_collection_type']
        action_value = ACTION_TO_SDK.get(collection.get('action')) if collection.get('action') else None

        if ctype == 'filter':
            action = self.network_models.FirewallPolicyFilterRuleCollectionAction(type=action_value) \
                if action_value else None
            return self.network_models.FirewallPolicyFilterRuleCollection(
                name=name,
                priority=priority,
                action=action,
                rules=rules or None,
            )
        action = self.network_models.FirewallPolicyNatRuleCollectionAction(type=action_value) \
            if action_value else None
        return self.network_models.FirewallPolicyNatRuleCollection(
            name=name,
            priority=priority,
            action=action,
            rules=rules or None,
        )

    def _build_rule(self, rule):
        rtype = rule['rule_type']
        common = dict(name=rule['name'], description=rule.get('description'))

        if rtype == 'application':
            protocols = None
            if rule.get('protocols'):
                protocols = [
                    self.network_models.FirewallPolicyRuleApplicationProtocol(
                        protocol_type=p.get('type'),
                        port=p.get('port'),
                    ) for p in rule['protocols']
                ]
            headers = None
            if rule.get('http_headers_to_insert'):
                headers = [
                    self.network_models.FirewallPolicyHttpHeaderToInsert(
                        header_name=h.get('header_name'),
                        header_value=h.get('header_value'),
                    ) for h in rule['http_headers_to_insert']
                ]
            return self.network_models.ApplicationRule(
                source_addresses=rule.get('source_addresses'),
                destination_addresses=rule.get('destination_addresses'),
                protocols=protocols,
                target_fqdns=rule.get('target_fqdns'),
                target_urls=rule.get('target_urls'),
                fqdn_tags=rule.get('fqdn_tags'),
                source_ip_groups=rule.get('source_ip_groups'),
                terminate_tls=rule.get('terminate_tls'),
                web_categories=rule.get('web_categories'),
                http_headers_to_insert=headers,
                **common
            )
        if rtype == 'network':
            return self.network_models.NetworkRule(
                ip_protocols=rule.get('ip_protocols'),
                source_addresses=rule.get('source_addresses'),
                destination_addresses=rule.get('destination_addresses'),
                destination_ports=rule.get('destination_ports'),
                source_ip_groups=rule.get('source_ip_groups'),
                destination_ip_groups=rule.get('destination_ip_groups'),
                destination_fqdns=rule.get('destination_fqdns'),
                **common
            )
        return self.network_models.NatRule(
            ip_protocols=rule.get('ip_protocols'),
            source_addresses=rule.get('source_addresses'),
            destination_addresses=rule.get('destination_addresses'),
            destination_ports=rule.get('destination_ports'),
            translated_address=rule.get('translated_address'),
            translated_port=rule.get('translated_port'),
            source_ip_groups=rule.get('source_ip_groups'),
            translated_fqdn=rule.get('translated_fqdn'),
            **common
        )

    def _needs_update(self, existing, desired):
        '''
        Compare the server-returned model against the user-built desired model.
        '''
        existing_dict = existing.as_dict()
        for key in ('id', 'etag', 'type', 'provisioning_state', 'size'):
            existing_dict.pop(key, None)
        desired_dict = desired.as_dict()
        return not self.default_compare({}, desired_dict, existing_dict, '', dict(compare=[]))


def main():
    AzureRMFirewallPolicyRuleCollectionGroup()


if __name__ == '__main__':
    main()
