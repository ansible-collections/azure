#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Zun Yang (@zunyangc).
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_loadbalancerbackendaddresspool

version_added: '4.0.0'

short_description: Manage a backend address pool of an Azure load balancer

description:
    - Create, update or delete a single backend address pool on an existing Azure load balancer.
    - The parent module M(azure.azcollection.azure_rm_loadbalancer) only declares empty pool stubs by name; this module owns all pool-level properties and members.

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
            - Name of the backend address pool.
        required: true
        type: str
    state:
        description:
            - Assert the state of the backend address pool.
            - Use C(present) to create or update, or C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present
    virtual_network:
        description:
            - Resource ID of the virtual network the backend address pool is bound to.
            - Required when I(sync_mode) is set.
        type: str
    sync_mode:
        description:
            - Backend address synchronous mode for the backend pool.
            - Requires Standard SKU load balancer and I(virtual_network) to be set.
        type: str
        choices:
            - Automatic
            - Manual
    drain_period_in_seconds:
        description:
            - Seconds the load balancer waits before sending RESET to client and backend address on connection close.
        type: int
    tunnel_interfaces:
        description:
            - Gateway load balancer tunnel interfaces for the backend address pool.
        type: list
        elements: dict
        suboptions:
            port:
                description:
                    - Port of the gateway load balancer tunnel interface.
                type: int
            identifier:
                description:
                    - Identifier of the gateway load balancer tunnel interface.
                type: int
            protocol:
                description:
                    - Protocol of the gateway load balancer tunnel interface.
                type: str
                choices:
                    - None
                    - Native
                    - VXLAN
            type:
                description:
                    - Traffic type of the gateway load balancer tunnel interface.
                type: str
                choices:
                    - None
                    - Internal
                    - External
    load_balancer_backend_addresses:
        description:
            - Backend addresses (IP-based or NIC-config-based) for the backend pool.
            - Requires Standard SKU load balancer.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Name of the backend address, unique within the pool.
                type: str
                required: true
            ip_address:
                description:
                    - IP address belonging to the referenced I(virtual_network).
                type: str
            virtual_network:
                description:
                    - Resource ID of the virtual network the backend address belongs to.
                type: str
            subnet:
                description:
                    - Resource ID of the subnet the backend address belongs to.
                type: str
            network_interface_ip_configuration:
                description:
                    - Resource ID of an existing NIC IP configuration to attach to the pool.
                type: str
            load_balancer_frontend_ip_configuration:
                description:
                    - Resource ID of a regional load balancer frontend IP configuration.
                    - Used only when attaching a regional load balancer to a Global cross-region load balancer.
                type: str
            admin_state:
                description:
                    - Administrative state which can override health probe results for this backend address.
                type: str
                choices:
                    - None
                    - Up
                    - Down

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Create backend address pool with two IP-based members
  azure_rm_loadbalancerbackendaddresspool:
    resource_group: myResourceGroup
    load_balancer_name: myLoadBalancer
    name: bepool0
    load_balancer_backend_addresses:
      - name: address1
        ip_address: 10.0.0.10
        virtual_network: /subscriptions/xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/myVnet
      - name: address2
        ip_address: 10.0.0.11
        virtual_network: /subscriptions/xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/myVnet

- name: Attach an existing NIC IP configuration to a backend pool
  azure_rm_loadbalancerbackendaddresspool:
    resource_group: myResourceGroup
    load_balancer_name: myLoadBalancer
    name: bepool0
    load_balancer_backend_addresses:
      - name: web-server1-nic
        network_interface_ip_configuration: /subscriptions/xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/networkInterfaces/web1-nic/ipConfigurations/ipconfig1

- name: Delete backend address pool
  azure_rm_loadbalancerbackendaddresspool:
    resource_group: myResourceGroup
    load_balancer_name: myLoadBalancer
    name: bepool0
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the backend address pool.
    returned: always
    type: complex
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
            returned: always
            sample:
                - name: address1
                  ip_address: 10.0.0.10
                  virtual_network: /subscriptions/xxx/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVnet
                  admin_state: None
        tunnel_interfaces:
            description:
                - Gateway load balancer tunnel interfaces.
            type: list
            returned: when-used
            sample: null
changed:
    description:
        - Whether or not the resource has changed.
    returned: always
    type: bool
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


backend_address_spec = dict(
    name=dict(type='str', required=True),
    ip_address=dict(type='str'),
    virtual_network=dict(type='str'),
    subnet=dict(type='str'),
    network_interface_ip_configuration=dict(type='str'),
    load_balancer_frontend_ip_configuration=dict(type='str'),
    admin_state=dict(type='str', choices=['None', 'Up', 'Down']),
)


tunnel_interface_spec = dict(
    port=dict(type='int'),
    identifier=dict(type='int'),
    protocol=dict(type='str', choices=['None', 'Native', 'VXLAN']),
    type=dict(type='str', choices=['None', 'Internal', 'External']),
)


class AzureRMLoadBalancerBackendAddressPool(AzureRMModuleBaseExt):

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            load_balancer_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            virtual_network=dict(type='str'),
            sync_mode=dict(type='str', choices=['Automatic', 'Manual']),
            drain_period_in_seconds=dict(type='int'),
            tunnel_interfaces=dict(type='list', elements='dict', options=tunnel_interface_spec),
            load_balancer_backend_addresses=dict(type='list', elements='dict', options=backend_address_spec),
        )

        self.resource_group = None
        self.load_balancer_name = None
        self.name = None
        self.state = None
        self.virtual_network = None
        self.sync_mode = None
        self.drain_period_in_seconds = None
        self.tunnel_interfaces = None
        self.load_balancer_backend_addresses = None

        self.results = dict(changed=False, state=None)

        super(AzureRMLoadBalancerBackendAddressPool, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec):
            setattr(self, key, kwargs[key])

        existing = self.get_backend_address_pool()
        existing_dict = self.format_item(existing) if existing else None
        desired = self.build_desired_dict()
        changed = False
        response = existing_dict

        if self.state == 'present':
            if existing is None:
                changed = True
                if not self.check_mode:
                    response = self.create_or_update()
            else:
                if not self.default_compare({}, desired, existing_dict, '', dict(compare=[])):
                    changed = True
                    if not self.check_mode:
                        response = self.create_or_update()
        else:
            if existing is not None:
                changed = True
                if not self.check_mode:
                    self.delete_backend_address_pool()
                    response = None

        self.results['changed'] = changed
        self.results['state'] = response
        return self.results

    def build_desired_dict(self):
        return dict(
            name=self.name,
            virtual_network=self.virtual_network,
            sync_mode=self.sync_mode,
            drain_period_in_seconds=self.drain_period_in_seconds,
            tunnel_interfaces=self.tunnel_interfaces,
            load_balancer_backend_addresses=self.load_balancer_backend_addresses,
        )

    def build_pool_param(self):
        return self.network_models.BackendAddressPool(
            name=self.name,
            virtual_network=self.network_models.SubResource(
                id=self.virtual_network
            ) if self.virtual_network else None,
            sync_mode=self.sync_mode,
            drain_period_in_seconds=self.drain_period_in_seconds,
            tunnel_interfaces=[self.network_models.GatewayLoadBalancerTunnelInterface(
                port=ti.get('port'),
                identifier=ti.get('identifier'),
                protocol=ti.get('protocol'),
                type=ti.get('type'),
            ) for ti in self.tunnel_interfaces] if self.tunnel_interfaces else None,
            load_balancer_backend_addresses=[self.network_models.LoadBalancerBackendAddress(
                name=addr.get('name'),
                ip_address=addr.get('ip_address'),
                virtual_network=self.network_models.SubResource(
                    id=addr.get('virtual_network')
                ) if addr.get('virtual_network') else None,
                subnet=self.network_models.SubResource(
                    id=addr.get('subnet')
                ) if addr.get('subnet') else None,
                network_interface_ip_configuration=self.network_models.SubResource(
                    id=addr.get('network_interface_ip_configuration')
                ) if addr.get('network_interface_ip_configuration') else None,
                load_balancer_frontend_ip_configuration=self.network_models.SubResource(
                    id=addr.get('load_balancer_frontend_ip_configuration')
                ) if addr.get('load_balancer_frontend_ip_configuration') else None,
                admin_state=addr.get('admin_state'),
            ) for addr in self.load_balancer_backend_addresses] if self.load_balancer_backend_addresses else None,
        )

    def get_backend_address_pool(self):
        try:
            return self.network_client.load_balancer_backend_address_pools.get(
                self.resource_group, self.load_balancer_name, self.name
            )
        except ResourceNotFoundError:
            return None

    def create_or_update(self):
        param = self.build_pool_param()
        try:
            poller = self.network_client.load_balancer_backend_address_pools.begin_create_or_update(
                self.resource_group, self.load_balancer_name, self.name, param
            )
            result = self.get_poller_result(poller)
            return self.format_item(result)
        except Exception as exc:
            self.fail("Error creating or updating backend address pool {0} on load balancer {1} - {2}".format(
                self.name, self.load_balancer_name, str(exc)))

    def delete_backend_address_pool(self):
        try:
            poller = self.network_client.load_balancer_backend_address_pools.begin_delete(
                self.resource_group, self.load_balancer_name, self.name
            )
            self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error deleting backend address pool {0} from load balancer {1} - {2}".format(
                self.name, self.load_balancer_name, str(exc)))

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
    AzureRMLoadBalancerBackendAddressPool()


if __name__ == '__main__':
    main()
