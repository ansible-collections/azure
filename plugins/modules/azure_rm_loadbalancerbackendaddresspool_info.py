#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Zun Yang (@zunyangc).
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_loadbalancerbackendaddresspool_info

version_added: '4.0.0'

short_description: Get facts for one or all backend address pools of an Azure load balancer

description:
    - Get facts for a single backend address pool by name, or list all backend address pools on a load balancer.

options:
    resource_group:
        description:
            - Name of the resource group that contains the load balancer.
        required: true
        type: str
    load_balancer_name:
        description:
            - Name of the parent load balancer.
        required: true
        type: str
    name:
        description:
            - Name of a specific backend address pool.
            - If omitted, all backend address pools on the load balancer are returned.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Get facts for a single backend address pool
  azure_rm_loadbalancerbackendaddresspool_info:
    resource_group: myResourceGroup
    load_balancer_name: myLoadBalancer
    name: bepool0

- name: List all backend address pools on a load balancer
  azure_rm_loadbalancerbackendaddresspool_info:
    resource_group: myResourceGroup
    load_balancer_name: myLoadBalancer
'''

RETURN = '''
backend_address_pools:
    description:
        - List of backend address pools matching the query.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description:
                - Resource ID of the backend address pool.
            type: str
            returned: always
            sample: "/subscriptions/xxx/resourceGroups/myRG/providers/Microsoft.Network/loadBalancers/myLB/backendAddressPools/bepool0"
        name:
            description:
                - Name of the backend address pool.
            type: str
            returned: always
            sample: bepool0
        provisioning_state:
            description:
                - Provisioning state of the backend address pool.
            type: str
            returned: always
            sample: Succeeded
        virtual_network:
            description:
                - Resource ID of the virtual network the pool is bound to.
            type: str
            returned: when-used
            sample: null
        sync_mode:
            description:
                - Backend address synchronous mode.
            type: str
            returned: when-used
            sample: null
        drain_period_in_seconds:
            description:
                - Drain period in seconds.
            type: int
            returned: when-used
            sample: null
        load_balancer_backend_addresses:
            description:
                - List of backend addresses attached to the pool.
            type: list
            returned: when-used
        tunnel_interfaces:
            description:
                - Gateway load balancer tunnel interfaces.
            type: list
            returned: when-used
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMLoadBalancerBackendAddressPoolInfo(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            load_balancer_name=dict(type='str', required=True),
            name=dict(type='str'),
        )

        self.results = dict(changed=False, backend_address_pools=[])
        self.resource_group = None
        self.load_balancer_name = None
        self.name = None

        super(AzureRMLoadBalancerBackendAddressPoolInfo, self).__init__(
            self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec):
            setattr(self, key, kwargs[key])

        if self.name:
            pool = self.get_backend_address_pool()
            pools = [pool] if pool else []
        else:
            pools = self.list_backend_address_pools()

        self.results['backend_address_pools'] = [self.format_item(p) for p in pools]
        return self.results

    def get_backend_address_pool(self):
        try:
            return self.network_client.load_balancer_backend_address_pools.get(
                self.resource_group, self.load_balancer_name, self.name
            )
        except ResourceNotFoundError:
            return None

    def list_backend_address_pools(self):
        try:
            return list(self.network_client.load_balancer_backend_address_pools.list(
                self.resource_group, self.load_balancer_name
            ))
        except ResourceNotFoundError:
            return []
        except Exception as exc:
            self.fail("Error listing backend address pools on load balancer {0} - {1}".format(
                self.load_balancer_name, str(exc)))

    def format_item(self, item):
        if item is None:
            return None
        result = dict(
            id=item.id,
            name=item.name,
            provisioning_state=item.provisioning_state,
            virtual_network=item.virtual_network.id if item.virtual_network is not None else None,
            sync_mode=item.sync_mode,
            drain_period_in_seconds=item.drain_period_in_seconds,
            tunnel_interfaces=None,
            load_balancer_backend_addresses=None,
        )
        if item.tunnel_interfaces is not None:
            result['tunnel_interfaces'] = [dict(
                port=ti.port,
                identifier=ti.identifier,
                protocol=ti.protocol,
                type=ti.type,
            ) for ti in item.tunnel_interfaces]
        if item.load_balancer_backend_addresses is not None:
            result['load_balancer_backend_addresses'] = [dict(
                name=addr.name,
                ip_address=addr.ip_address,
                virtual_network=addr.virtual_network.id if addr.virtual_network is not None else None,
                subnet=addr.subnet.id if addr.subnet is not None else None,
                network_interface_ip_configuration=(
                    addr.network_interface_ip_configuration.id
                    if addr.network_interface_ip_configuration is not None else None
                ),
                load_balancer_frontend_ip_configuration=(
                    addr.load_balancer_frontend_ip_configuration.id
                    if addr.load_balancer_frontend_ip_configuration is not None else None
                ),
                admin_state=addr.admin_state,
            ) for addr in item.load_balancer_backend_addresses]
        return result


def main():
    AzureRMLoadBalancerBackendAddressPoolInfo()


if __name__ == '__main__':
    main()
