#!/usr/bin/python
#
# Copyright (c) 2016 Matt Davis, <mdavis@ansible.com>
#                    Chris Houseknecht, <house@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_securitygroup_info

version_added: "0.1.2"

short_description: Get security group facts

description:
    - Get facts for a specific security group or all security groups within a resource group.

options:
    name:
        description:
            - Only show results for a specific security group.
    resource_group:
        description:
            - Name of the resource group to use.
        required: true
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Chris Houseknecht (@chouseknecht)
    - Matt Davis (@nitzmahone)

'''

EXAMPLES = '''
    - name: Get facts for one security group
      azure_rm_securitygroup_info:
        resource_group: myResourceGroup
        name: secgroup001

    - name: Get facts for all security groups
      azure_rm_securitygroup_info:
        resource_group: myResourceGroup

'''

RETURN = '''
securitygroups:
    description:
        - List containing security group dicts.
    returned: always
    type: complex
    contains:
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample:  'W/"d036f4d7-d977-429a-a8c6-879bc2523399"'
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroup/myResourceGroup/providers/Microsoft.Network/networkSecurityGroups/secgroup001"
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: "eastus2"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: "secgroup001"
        default_rules:
            description:
                - The default security rules of network security group.
            returned: always
            type: list
            sample: [
                    {
                        "access": "Allow",
                        "description": "Allow inbound traffic from all VMs in VNET",
                        "destination_address_prefix": "VirtualNetwork",
                        "destination_port_range": "*",
                        "direction": "Inbound",
                        "etag": 'W/"edf48d56-b315-40ca-a85d-dbcb47f2da7d"',
                        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroup/myResourceGroup/providers/Microsoft.Network/networkSecurityGroups/mysecgroup/defaultSecurityRules/AllowVnetInBound",
                        "name": "AllowVnetInBound",
                        "priority": 65000,
                        "protocol": "*",
                        "provisioning_state": "Succeeded",
                        "source_address_prefix": "VirtualNetwork",
                        "source_port_range": "*"
                    },
                    {
                        "access": "Allow",
                        "description": "Allow inbound traffic from azure load balancer",
                        "destination_address_prefix": "*",
                        "destination_port_range": "*",
                        "direction": "Inbound",
                        "etag": 'W/"edf48d56-b315-40ca-a85d-dbcb47f2da7d"',
                        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroup/myResourceGroup/providers/Microsoft.Network/networkSecurityGroups/mysecgroup/defaultSecurityRules/AllowAzureLoadBalancerInBound",
                        "name": "AllowAzureLoadBalancerInBound",
                        "priority": 65001,
                        "protocol": "*",
                        "provisioning_state": "Succeeded",
                        "source_address_prefix": "AzureLoadBalancer",
                        "source_port_range": "*"
                    },
                    {
                        "access": "Deny",
                        "description": "Deny all inbound traffic",
                        "destination_address_prefix": "*",
                        "destination_port_range": "*",
                        "direction": "Inbound",
                        "etag": 'W/"edf48d56-b315-40ca-a85d-dbcb47f2da7d"',
                        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroup/myResourceGroup/providers/Microsoft.Network/networkSecurityGroups/mysecgroup/defaultSecurityRules/DenyAllInBound",
                        "name": "DenyAllInBound",
                        "priority": 65500,
                        "protocol": "*",
                        "provisioning_state": "Succeeded",
                        "source_address_prefix": "*",
                        "source_port_range": "*"
                    },
                    {
                        "access": "Allow",
                        "description": "Allow outbound traffic from all VMs to all VMs in VNET",
                        "destination_address_prefix": "VirtualNetwork",
                        "destination_port_range": "*",
                        "direction": "Outbound",
                        "etag": 'W/"edf48d56-b315-40ca-a85d-dbcb47f2da7d"',
                        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroup/myResourceGroup/providers/Microsoft.Network/networkSecurityGroups/mysecgroup/defaultSecurityRules/AllowVnetOutBound",
                        "name": "AllowVnetOutBound",
                        "priority": 65000,
                        "protocol": "*",
                        "provisioning_state": "Succeeded",
                        "source_address_prefix": "VirtualNetwork",
                        "source_port_range": "*"
                    },
                    {
                        "access": "Allow",
                        "description": "Allow outbound traffic from all VMs to Internet",
                        "destination_address_prefix": "Internet",
                        "destination_port_range": "*",
                        "direction": "Outbound",
                        "etag": 'W/"edf48d56-b315-40ca-a85d-dbcb47f2da7d"',
                        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroup/myResourceGroup/providers/Microsoft.Network/networkSecurityGroups/mysecgroup/defaultSecurityRules/AllowInternetOutBound",
                        "name": "AllowInternetOutBound",
                        "priority": 65001,
                        "protocol": "*",
                        "provisioning_state": "Succeeded",
                        "source_address_prefix": "*",
                        "source_port_range": "*"
                    },
                    {
                        "access": "Deny",
                        "description": "Deny all outbound traffic",
                        "destination_address_prefix": "*",
                        "destination_port_range": "*",
                        "direction": "Outbound",
                        "etag": 'W/"edf48d56-b315-40ca-a85d-dbcb47f2da7d"',
                        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroup/myResourceGroup/providers/Microsoft.Network/networkSecurityGroups/mysecgroup/defaultSecurityRules/DenyAllOutBound",
                        "name": "DenyAllOutBound",
                        "priority": 65500,
                        "protocol": "*",
                        "provisioning_state": "Succeeded",
                        "source_address_prefix": "*",
                        "source_port_range": "*"
                    }
                ]
        network_interfaces:
            description:
                - A collection of references to network interfaces.
            returned: always
            type: list
            sample: []
        rules:
            description:
                - A collection of security rules of the network security group.
            returned: always
            type: list
            sample: [
                {
                    "access": "Deny",
                    "description": null,
                    "destination_address_prefix": "*",
                    "destination_port_range": "22",
                    "direction": "Inbound",
                    "etag": 'W/"edf48d56-b315-40ca-a85d-dbcb47f2da7d"',
                    "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroup/myResourceGroup/providers/Microsoft.Network/networkSecurityGroups/mysecgroup/securityRules/DenySSH",
                    "name": "DenySSH",
                    "priority": 100,
                    "protocol": "Tcp",
                    "provisioning_state": "Succeeded",
                    "source_address_prefix": "*",
                    "source_port_range": "*"
                },
                {
                    "access": "Allow",
                    "description": null,
                    "destination_address_prefix": "*",
                    "destination_port_range": "22",
                    "direction": "Inbound",
                    "etag": 'W/"edf48d56-b315-40ca-a85d-dbcb47f2da7d"',
                    "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroup/myResourceGroup/providers/Microsoft.Network/networkSecurityGroups/mysecgroup/securityRules/AllowSSH",
                    "name": "AllowSSH",
                    "priority": 101,
                    "protocol": "Tcp",
                    "provisioning_state": "Succeeded",
                    "source_address_prefix": "174.109.158.0/24",
                    "source_port_range": "*"
                }
            ]
        subnets:
            description:
                - A collection of references to subnets.
            returned: always
            type: list
            sample: []
        tags:
            description:
                - Tags to assign to the security group.
            returned: always
            type: dict
            sample: { 'tag': 'value' }
        type:
            description:
                - Type of the resource.
            returned: always
            type: str
            sample: "Microsoft.Network/networkSecurityGroups"

'''  # NOQA

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


def create_rule_dict_from_obj(rule):
    return dict(
        id=rule.id,
        name=rule.name,
        description=rule.description,
        protocol=rule.protocol,
        source_port_range=rule.source_port_range,
        destination_port_range=rule.destination_port_range,
        source_address_prefix=rule.source_address_prefix,
        destination_address_prefix=rule.destination_address_prefix,
        source_port_ranges=rule.source_port_ranges,
        destination_port_ranges=rule.destination_port_ranges,
        source_address_prefixes=rule.source_address_prefixes,
        destination_address_prefixes=rule.destination_address_prefixes,
        source_application_security_groups=[p.id for p in rule.source_application_security_groups] if rule.source_application_security_groups else None,
        destination_application_security_groups=[
            p.id for p in rule.destination_application_security_groups] if rule.destination_application_security_groups else None,
        access=rule.access,
        priority=rule.priority,
        direction=rule.direction,
        provisioning_state=rule.provisioning_state,
        etag=rule.etag
    )


def create_network_security_group_dict(nsg):
    result = dict(
        etag=nsg.etag,
        id=nsg.id,
        location=nsg.location,
        name=nsg.name,
        tags=nsg.tags,
        type=nsg.type,
    )
    result['rules'] = []
    if nsg.security_rules:
        for rule in nsg.security_rules:
            result['rules'].append(create_rule_dict_from_obj(rule))

    result['default_rules'] = []
    if nsg.default_security_rules:
        for rule in nsg.default_security_rules:
            result['default_rules'].append(create_rule_dict_from_obj(rule))

    result['network_interfaces'] = []
    if nsg.network_interfaces:
        for interface in nsg.network_interfaces:
            result['network_interfaces'].append(interface.id)

    result['subnets'] = []
    if nsg.subnets:
        for subnet in nsg.subnets:
            result['subnets'].append(subnet.id)

    return result


class AzureRMSecurityGroupInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(required=True, type='str'),
            tags=dict(type='list', elements='str'),
        )

        self.results = dict(
            changed=False,
        )

        self.name = None
        self.resource_group = None
        self.tags = None

        super(AzureRMSecurityGroupInfo, self).__init__(self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False,
                                                       facts_module=True)

    def exec_module(self, **kwargs):

        is_old_facts = self.module._name == 'azure_rm_securitygroup_facts'
        if is_old_facts:
            self.module.deprecate("The 'azure_rm_securitygroup_facts' module has been renamed to 'azure_rm_securitygroup_info'", version=(2.9, ))

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            info = self.get_item()
        else:
            info = self.list_items()

        if is_old_facts:
            self.results['ansible_facts'] = {
                'azure_securitygroups': info
            }
        self.results['securitygroups'] = info

        return self.results

    def get_item(self):
        self.log('Get properties for {0}'.format(self.name))
        item = None
        result = []

        try:
            item = self.network_client.network_security_groups.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            pass

        if item and self.has_tags(item.tags, self.tags):
            result = [create_network_security_group_dict(item)]

        return result

    def list_items(self):
        self.log('List all items')
        try:
            response = self.network_client.network_security_groups.list(self.resource_group)
        except Exception as exc:
            self.fail("Error listing all items - {0}".format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(create_network_security_group_dict(item))
        return results


def main():
    AzureRMSecurityGroupInfo()


if __name__ == '__main__':
    main()
