#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2016, Thomas Stringer <tomstr@microsoft.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_loadbalancer

version_added: "0.1.2"

short_description: Manage Azure load balancers

description:
    - Create, update and delete Azure load balancers.

options:
    resource_group:
        description:
            - Name of a resource group where the load balancer exists or will be created.
        required: true
        type: str
    name:
        description:
            - Name of the load balancer.
        required: true
        type: str
    state:
        description:
            - Assert the state of the load balancer. Use C(present) to create/update a load balancer, or C(absent) to delete one.
        default: present
        type: str
        choices:
            - absent
            - present
    location:
        description:
            - Valid Azure location. Defaults to location of the resource group.
        type: str
    sku:
        description:
            - The load balancer SKU.
        type: str
        choices:
            - Basic
            - Standard
    frontend_ip_configurations:
        description:
            - List of frontend IPs to be used.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Name of the frontend ip configuration.
                type: str
                required: True
            public_ip_address:
                description:
                    - Name of an existing public IP address object in the current resource group to associate with the security group.
                type: str
            private_ip_address:
                description:
                    - The reference of the Public IP resource.
                type: str
            private_ip_allocation_method:
                description:
                    - The Private IP allocation method.
                type: str
                choices:
                    - Static
                    - Dynamic
            subnet:
                description:
                    - The reference of the subnet resource.
                    - Should be an existing subnet's resource id.
                type: str
            zones:
                description:
                    - list of availability zones denoting the IP allocated for the resource needs to come from.
                    - This must be specified I(sku=Standard) and I(subnet) when setting zones.
                type: list
                elements: str
    backend_address_pools:
        description:
            - List of backend address pools.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Name of the backend address pool.
                required: True
                type: str
    probes:
        description:
            - List of probe definitions used to check endpoint health.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Name of the probe.
                type: str
                required: True
            port:
                description:
                    - Probe port for communicating the probe. Possible values range from 1 to 65535, inclusive.
                type: int
                required: True
            protocol:
                description:
                    - The protocol of the end point to be probed.
                    - If C(Tcp) is specified, a received ACK is required for the probe to be successful.
                    - If C(Http) or C(Https) is specified, a 200 OK response from the specified URL is required for the probe to be successful.
                type: str
                choices:
                    - Tcp
                    - Http
                    - Https
            interval:
                description:
                    - The interval, in seconds, for how frequently to probe the endpoint for health status.
                    - Slightly less than half the allocated timeout period, which allows two full probes before taking the instance out of rotation.
                    - The default value is C(15), the minimum value is C(5).
                type: int
                default: 15
            fail_count:
                description:
                    - The number of probes where if no response, will result in stopping further traffic from being delivered to the endpoint.
                    - This values allows endpoints to be taken out of rotation faster or slower than the typical times used in Azure.
                default: 3
                type: int
                aliases:
                    - number_of_probes
            request_path:
                description:
                    - The URI used for requesting health status from the VM.
                    - Path is required if I(protocol=Http) or I(protocol=Https). Otherwise, it is not allowed.
                type: str
    inbound_nat_pools:
        description:
            - Defines an external port range for inbound NAT to a single backend port on NICs associated with a load balancer.
            - Inbound NAT rules are created automatically for each NIC associated with the Load Balancer using an external port from this range.
            - Defining an Inbound NAT pool on your Load Balancer is mutually exclusive with defining inbound Nat rules.
            - Inbound NAT pools are referenced from virtual machine scale sets.
            - NICs that are associated with individual virtual machines cannot reference an inbound NAT pool.
            - They have to reference individual inbound NAT rules.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Name of the inbound NAT pool.
                type: str
                required: True
            frontend_ip_configuration_name:
                description:
                    - A reference to frontend IP addresses.
                required: True
                type: str
            protocol:
                description:
                    - IP protocol for the NAT pool.
                type: str
                choices:
                    - Tcp
                    - Udp
                    - All
            frontend_port_range_start:
                description:
                    - The first port in the range of external ports that will be used to provide inbound NAT to NICs associated with the load balancer.
                    - Acceptable values range between 1 and 65534.
                type: int
                required: True
            frontend_port_range_end:
                description:
                    - The last port in the range of external ports that will be used to provide inbound NAT to NICs associated with the load balancer.
                    - Acceptable values range between 1 and 65535.
                type: int
                required: True
            backend_port:
                description:
                    - The port used for internal connections on the endpoint.
                    - Acceptable values are between 1 and 65535.
                type: int
                required: true
    load_balancing_rules:
        description:
            - Object collection representing the load balancing rules Gets the provisioning.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Name of the load balancing rule.
                type: str
                required: True
            frontend_ip_configuration:
                description:
                    - A reference to frontend IP addresses.
                type: str
                required: True
            backend_address_pool:
                description:
                    - A reference to a pool of DIPs. Inbound traffic is randomly load balanced across IPs in the backend IPs.
                required: True
                type: str
            probe:
                description:
                    - The name of the load balancer probe this rule should use for health checks.
                required: True
                type: str
            protocol:
                description:
                    - IP protocol for the load balancing rule.
                type: str
                choices:
                    - Tcp
                    - Udp
                    - All
            load_distribution:
                description:
                    - The session persistence policy for this rule; C(Default) is no persistence.
                type: str
                choices:
                    - Default
                    - SourceIP
                    - SourceIPProtocol
                default: Default
            frontend_port:
                description:
                    - The port for the external endpoint.
                    - Frontend port numbers must be unique across all rules within the load balancer.
                    - Acceptable values are between 0 and 65534.
                    - Note that value 0 enables "Any Port".
                type: int
                required: true
            backend_port:
                description:
                    - The port used for internal connections on the endpoint.
                    - Acceptable values are between 0 and 65535.
                    - Note that value 0 enables "Any Port".
                type: int
            idle_timeout:
                description:
                    - The timeout for the TCP idle connection.
                    - The value can be set between 4 and 30 minutes.
                    - The default value is C(4) minutes.
                    - This element is only used when the protocol is set to TCP.
                type: int
                default: 4
            enable_floating_ip:
                description:
                    - Configures a virtual machine's endpoint for the floating IP capability required to configure a SQL AlwaysOn Availability Group.
                type: bool
            enable_tcp_reset:
                description:
                    - Receive bidirectional TCP Reset on TCP flow idle timeout or unexpected connection termination.
                    - This element is only used when the protocol is set to TCP.
                type: bool
            disable_outbound_snat:
                description:
                    - Configure outbound source network address translation (SNAT).
                    - The default behavior when omitted is equivalent to I(disable_outbound_snat=True).
                    - True is equivalent to "(Recommended) Use outbound rules to provide backend pool members access to the internet" in portal.
                    - False is equivalent to "Use default outbound access" in portal.
                type: bool
                default: False
    inbound_nat_rules:
        description:
            - Collection of inbound NAT Rules used by a load balancer.
            - Defining inbound NAT rules on your load balancer is mutually exclusive with defining an inbound NAT pool.
            - Inbound NAT pools are referenced from virtual machine scale sets.
            - NICs that are associated with individual virtual machines cannot reference an Inbound NAT pool.
            - They have to reference individual inbound NAT rules.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - name of the inbound nat rule.
                type: str
                required: True
            frontend_ip_configuration:
                description:
                    - A reference to frontend IP addresses.
                type: str
                required: True
            protocol:
                description:
                    - IP protocol for the inbound nat rule.
                type: str
                choices:
                    - Tcp
                    - Udp
                    - All
            frontend_port:
                description:
                    - The port for the external endpoint.
                    - Frontend port numbers must be unique across all rules within the load balancer.
                    - Acceptable values are between 0 and 65534.
                    - Note that value 0 enables "Any Port".
                type: int
                required: True
            backend_port:
                description:
                    - The port used for internal connections on the endpoint.
                    - Acceptable values are between 0 and 65535.
                    - Note that value 0 enables "Any Port".
                type: int
                required: true
            idle_timeout:
                description:
                    - The timeout for the TCP idle connection.
                    - The value can be set between 4 and 30 minutes.
                    - The default value is C(4) minutes.
                    - This element is only used when I(protocol=Tcp).
                type: int
            enable_floating_ip:
                description:
                    - Configures a virtual machine's endpoint for the floating IP capability required to configure a SQL AlwaysOn Availability Group.
                    - This setting is required when using the SQL AlwaysOn Availability Groups in SQL server.
                    - This setting can't be changed after you create the endpoint.
                type: bool
            enable_tcp_reset:
                description:
                    - Receive bidirectional TCP Reset on TCP flow idle timeout or unexpected connection termination.
                    - This element is only used when I(protocol=Tcp).
                type: bool
    outbound_rules:
        description:
            - The outbound rules.
        type: list
        elements: dict
        version_added: '3.5.0'
        suboptions:
            name:
                description:
                    - The name of the resource that is unique within the set of outbound rules used by the load balancer.
                    - This name can be used to access the resource.
                type: str
                required: True
            allocated_outbound_ports:
                description:
                    - The number of outbound ports to be used for NAT.
                type: int
            frontend_ip_configurations:
                description:
                    - The Frontend IP addresses of the load balancer.
                type: list
                elements: str
            backend_address_pool:
                description:
                    - A reference to a pool of DIPs.
                    - Outbound traffic is randomly load balanced across IPs in the backend IPs.
                type: str
            protocol:
                description:
                    - The protocol for the outbound rule in load balancer.
                type: str
                choices:
                    - Tcp
                    - Udp
                    - All
            enable_tcp_reset:
                description:
                    - Receive bidirectional TCP Reset on TCP flow idle timeout or unexpected connection termination.
                    - This element is only used when the protocol is set to C(Tcp).
                type: bool
            idle_timeout_in_minutes:
                description:
                    - The timeout for the TCP idle connection.
                type: int
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Thomas Stringer (@trstringer)
    - Yuwei Zhou (@yuwzho)
'''

EXAMPLES = '''
- name: create load balancer
  azure_rm_loadbalancer:
    resource_group: myResourceGroup
    name: testloadbalancer1
    frontend_ip_configurations:
      - name: frontendipconf0
        public_ip_address: testpip
      - name: frontendipconf1
        public_ip_address: testpip1
    backend_address_pools:
      - name: backendaddrpool0
      - name: backendaddrpool1
    probes:
      - name: prob0
        port: 80
    inbound_nat_pools:
      - name: inboundnatpool0
        frontend_ip_configuration_name: frontendipconf0
        protocol: Tcp
        frontend_port_range_start: 80
        frontend_port_range_end: 81
        backend_port: 8080
    load_balancing_rules:
      - name: lbrbalancingrule0
        frontend_ip_configuration: frontendipconf0
        backend_address_pool: backendaddrpool0
        frontend_port: 80
        backend_port: 80
        probe: prob0
    inbound_nat_rules:
      - name: inboundnatrule0
        backend_port: 8080
        protocol: Tcp
        frontend_port: 8080
        frontend_ip_configuration: frontendipconf0
    outbound_rules:
      - name: outrule1
        allocated_outbound_ports: 800
        frontend_ip_configurations:
          - frontendipconf1
        backend_address_pool: backendaddrpool1
        protocol: Tcp
        enable_tcp_reset: true
        idle_timeout_in_minutes: 4
'''

RETURN = '''
state:
    description:
        - Current state of the load balancer.
    returned: always
    type: dict
changed:
    description:
        - Whether or not the resource has changed.
    returned: always
    type: bool
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import format_resource_id
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible.module_utils._text import to_native
try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.mgmt.core.tools import parse_resource_id
except ImportError:
    # This is handled in azure_rm_common
    pass


frontend_ip_configuration_spec = dict(
    name=dict(
        type='str',
        required=True
    ),
    public_ip_address=dict(
        type='str'
    ),
    private_ip_address=dict(
        type='str'
    ),
    private_ip_allocation_method=dict(
        type='str',
        choices=['Static', 'Dynamic']
    ),
    subnet=dict(
        type='str'
    ),
    zones=dict(
        type='list',
        elements='str'
    )
)


backend_address_pool_spec = dict(
    name=dict(
        type='str',
        required=True
    )
)


probes_spec = dict(
    name=dict(
        type='str',
        required=True
    ),
    port=dict(
        type='int',
        required=True
    ),
    protocol=dict(
        type='str',
        choices=['Tcp', 'Http', 'Https']
    ),
    interval=dict(
        type='int',
        default=15
    ),
    fail_count=dict(
        type='int',
        default=3,
        aliases=['number_of_probes']
    ),
    request_path=dict(
        type='str'
    )
)


inbound_nat_pool_spec = dict(
    name=dict(
        type='str',
        required=True
    ),
    frontend_ip_configuration_name=dict(
        type='str',
        required=True
    ),
    protocol=dict(
        type='str',
        choices=['Tcp', 'Udp', 'All']
    ),
    frontend_port_range_start=dict(
        type='int',
        required=True
    ),
    frontend_port_range_end=dict(
        type='int',
        required=True
    ),
    backend_port=dict(
        type='int',
        required=True
    )
)


inbound_nat_rule_spec = dict(
    name=dict(
        type='str',
        required=True
    ),
    frontend_ip_configuration=dict(
        type='str',
        required=True
    ),
    protocol=dict(
        type='str',
        choices=['Tcp', 'Udp', 'All']
    ),
    frontend_port=dict(
        type='int',
        required=True
    ),
    idle_timeout=dict(
        type='int'
    ),
    backend_port=dict(
        type='int',
        required=True
    ),
    enable_floating_ip=dict(
        type='bool'
    ),
    enable_tcp_reset=dict(
        type='bool'
    )
)


load_balancing_rule_spec = dict(
    name=dict(
        type='str',
        required=True
    ),
    frontend_ip_configuration=dict(
        type='str',
        required=True
    ),
    backend_address_pool=dict(
        type='str',
        required=True
    ),
    probe=dict(
        type='str',
        required=True
    ),
    protocol=dict(
        type='str',
        choices=['Tcp', 'Udp', 'All']
    ),
    load_distribution=dict(
        type='str',
        choices=['Default', 'SourceIP', 'SourceIPProtocol'],
        default='Default'
    ),
    frontend_port=dict(
        type='int',
        required=True
    ),
    backend_port=dict(
        type='int'
    ),
    idle_timeout=dict(
        type='int',
        default=4
    ),
    enable_floating_ip=dict(
        type='bool'
    ),
    disable_outbound_snat=dict(
        type='bool',
        default=False
    ),
    enable_tcp_reset=dict(
        type='bool'
    )
)


outbound_rule_spec = dict(
    name=dict(type='str', required=True),
    allocated_outbound_ports=dict(type='int'),
    frontend_ip_configurations=dict(type='list', elements='str'),
    backend_address_pool=dict(type='str'),
    protocol=dict(type='str', choices=['Tcp', 'Udp', 'All']),
    enable_tcp_reset=dict(type='bool'),
    idle_timeout_in_minutes=dict(type='int')

)


class AzureRMLoadBalancer(AzureRMModuleBaseExt):
    """Configuration class for an Azure RM load balancer resource"""

    def __init__(self):
        self.module_args = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            location=dict(
                type='str'
            ),
            sku=dict(
                type='str',
                choices=['Basic', 'Standard']
            ),
            frontend_ip_configurations=dict(
                type='list',
                elements='dict',
                options=frontend_ip_configuration_spec
            ),
            backend_address_pools=dict(
                type='list',
                elements='dict',
                options=backend_address_pool_spec
            ),
            probes=dict(
                type='list',
                elements='dict',
                options=probes_spec
            ),
            inbound_nat_rules=dict(
                type='list',
                elements='dict',
                options=inbound_nat_rule_spec
            ),
            inbound_nat_pools=dict(
                type='list',
                elements='dict',
                options=inbound_nat_pool_spec
            ),
            load_balancing_rules=dict(
                type='list',
                elements='dict',
                options=load_balancing_rule_spec
            ),
            outbound_rules=dict(
                type='list',
                elements='dict',
                options=outbound_rule_spec
            )
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.sku = None
        self.frontend_ip_configurations = None
        self.backend_address_pools = None
        self.probes = None
        self.inbound_nat_rules = None
        self.inbound_nat_pools = None
        self.outbound_rules = None
        self.load_balancing_rules = None
        self.state = None
        self.tags = None

        self.results = dict(changed=False, state=dict())

        super(AzureRMLoadBalancer, self).__init__(
            derived_arg_spec=self.module_args,
            supports_check_mode=True
        )

    def exec_module(self, **kwargs):
        """Main module execution method"""
        for key in list(self.module_args.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        load_balancer = self.get_load_balancer()

        if self.state == 'present':
            # create new load balancer structure early, so it can be easily compared
            if not load_balancer:
                changed = True
            else:
                response = self.format_item(load_balancer)
                update1, self.frontend_ip_configurations = self.update_item(self.frontend_ip_configurations, response.get('frontend_ip_configurations'))
                update2, self.backend_address_pools = self.update_item(self.backend_address_pools, response.get('backend_address_pools'))
                update3, self.probes = self.update_item(self.probes, response.get('probes'))
                update4, self.inbound_nat_rules = self.update_item(self.inbound_nat_rules, response.get('inbound_nat_rules'))
                update5, self.inbound_nat_pools = self.update_item(self.inbound_nat_pools, response.get('inbound_nat_pools'))
                update6, self.outbound_rules = self.update_item(self.outbound_rules, response.get('outbound_rules'))
                update7, self.load_balancing_rules = self.update_item(self.load_balancing_rules, response.get('load_balancing_rules'))

                changed = update1 or update2 or update3 or update4 or update5 or update6 or update7

            frontend_ip_configurations_param = [self.network_models.FrontendIPConfiguration(
                name=item.get('name'),
                public_ip_address=self.get_public_ip_address_instance(item.get('public_ip_address')) if item.get('public_ip_address') else None,
                private_ip_address=item.get('private_ip_address'),
                private_ip_allocation_method=item.get('private_ip_allocation_method'),
                zones=item.get('zones'),
                subnet=self.network_models.Subnet(
                    id=item.get('subnet'),
                    private_endpoint_network_policies=None,
                    private_link_service_network_policies=None
                ) if item.get('subnet') else None
            ) for item in self.frontend_ip_configurations] if self.frontend_ip_configurations else None

            backend_address_pools_param = [self.network_models.BackendAddressPool(
                name=item.get('name')
            ) for item in self.backend_address_pools] if self.backend_address_pools else None

            probes_param = [self.network_models.Probe(
                name=item.get('name'),
                port=item.get('port'),
                protocol=item.get('protocol'),
                interval_in_seconds=item.get('interval'),
                request_path=item.get('request_path'),
                number_of_probes=item.get('fail_count')
            ) for item in self.probes] if self.probes else None

            inbound_nat_pools_param = [self.network_models.InboundNatPool(
                name=item.get('name'),
                frontend_ip_configuration=self.network_models.SubResource(
                    id=frontend_ip_configuration_id(
                        self.subscription_id,
                        self.resource_group,
                        self.name,
                        item.get('frontend_ip_configuration_name'))),
                protocol=item.get('protocol'),
                frontend_port_range_start=item.get('frontend_port_range_start'),
                frontend_port_range_end=item.get('frontend_port_range_end'),
                backend_port=item.get('backend_port')
            ) for item in self.inbound_nat_pools] if self.inbound_nat_pools else None

            load_balancing_rules_param = [self.network_models.LoadBalancingRule(
                name=item.get('name'),
                frontend_ip_configuration=self.network_models.SubResource(
                    id=frontend_ip_configuration_id(
                        self.subscription_id,
                        self.resource_group,
                        self.name,
                        item.get('frontend_ip_configuration')
                    )
                ),
                backend_address_pool=self.network_models.SubResource(
                    id=backend_address_pool_id(
                        self.subscription_id,
                        self.resource_group,
                        self.name,
                        item.get('backend_address_pool')
                    )
                ),
                probe=self.network_models.SubResource(
                    id=probe_id(
                        self.subscription_id,
                        self.resource_group,
                        self.name,
                        item.get('probe')
                    )
                ),
                protocol=item.get('protocol'),
                load_distribution=item.get('load_distribution'),
                frontend_port=item.get('frontend_port'),
                backend_port=item.get('backend_port'),
                idle_timeout_in_minutes=item.get('idle_timeout'),
                enable_floating_ip=item.get('enable_floating_ip'),
                enable_tcp_reset=item.get('enable_tcp_reset'),
                disable_outbound_snat=item.get('disable_outbound_snat'),
            ) for item in self.load_balancing_rules] if self.load_balancing_rules else None

            inbound_nat_rules_param = [self.network_models.InboundNatRule(
                name=item.get('name'),
                frontend_ip_configuration=self.network_models.SubResource(
                    id=frontend_ip_configuration_id(
                        self.subscription_id,
                        self.resource_group,
                        self.name,
                        item.get('frontend_ip_configuration')
                    )
                ) if item.get('frontend_ip_configuration') else None,
                protocol=item.get('protocol'),
                frontend_port=item.get('frontend_port'),
                backend_port=item.get('backend_port'),
                idle_timeout_in_minutes=item.get('idle_timeout'),
                enable_tcp_reset=item.get('enable_tcp_reset'),
                enable_floating_ip=item.get('enable_floating_ip')
            ) for item in self.inbound_nat_rules] if self.inbound_nat_rules else None

            outbound_rules_param = [self.network_models.OutboundRule(
                name=item.get('name'),
                frontend_ip_configurations=[self.network_models.SubResource(
                    id=frontend_ip_configuration_id(
                        self.subscription_id,
                        self.resource_group,
                        self.name,
                        value
                    )
                )for value in item['frontend_ip_configurations']] if item.get('frontend_ip_configurations') else None,
                backend_address_pool=self.network_models.SubResource(
                    id=backend_address_pool_id(
                        self.subscription_id,
                        self.resource_group,
                        self.name,
                        item.get('backend_address_pool')
                    )
                ),
                allocated_outbound_ports=item.get('allocated_outbound_ports'),
                protocol=item.get('protocol'),
                enable_tcp_reset=item.get('enable_tcp_reset'),
                idle_timeout_in_minutes=item.get('idle_timeout_in_minutes')
            ) for item in self.outbound_rules] if self.outbound_rules else None

            # construct the new instance, if the parameter is none, keep remote one
            self.new_load_balancer = self.network_models.LoadBalancer(
                sku=self.network_models.LoadBalancerSku(name=self.sku) if self.sku else None,
                location=self.location,
                tags=self.tags,
                frontend_ip_configurations=frontend_ip_configurations_param,
                backend_address_pools=backend_address_pools_param,
                probes=probes_param,
                inbound_nat_pools=inbound_nat_pools_param,
                load_balancing_rules=load_balancing_rules_param,
                inbound_nat_rules=inbound_nat_rules_param,
                outbound_rules=outbound_rules_param,
            )

            self.new_load_balancer = self.assign_protocol(self.new_load_balancer, load_balancer)

            if load_balancer:
                self.new_load_balancer = self.object_assign(self.new_load_balancer, load_balancer)
        elif self.state == 'absent' and load_balancer:
            changed = True

        self.results['state'] = load_balancer.as_dict() if load_balancer else {}
        if 'tags' in self.results['state']:
            update_tags, self.results['state']['tags'] = self.update_tags(self.results['state']['tags'])
            if update_tags:
                changed = True
        else:
            if self.tags:
                changed = True
        self.results['changed'] = changed

        if self.check_mode:
            return self.results

        if self.state == 'present' and changed:
            self.results['state'] = self.create_or_update_load_balancer(self.new_load_balancer).as_dict()
        elif self.state == 'absent' and changed:
            self.delete_load_balancer()
            self.results['state'] = None

        return self.results

    def update_item(self, new, old):
        changed = False
        if new is not None:
            if old is not None:
                if not self.default_compare({}, new, old, '', dict(compare=[])):
                    changed = True

                keys = [item['name'] for item in new]
                for item in old:
                    if item['name'] not in keys:
                        new.append(item)
            else:
                changed = True
        else:
            new = old
        return changed, new

    def format_item(self, item):
        results = dict()
        if item.frontend_ip_configurations is not None:
            results['frontend_ip_configurations'] = []
            for value in item.frontend_ip_configurations:
                new_item = dict(name=value.name,
                                public_ip_address=None,
                                private_ip_address=value.private_ip_address,
                                private_ip_allocation_method=value.private_ip_allocation_method,
                                subnet=None,
                                zones=value.zones)
                if value.public_ip_address is not None:
                    new_item['public_ip_address'] = parse_resource_id(value.public_ip_address.id)['name']
                if value.subnet is not None:
                    new_item['subnet'] = value.subnet.id
                results['frontend_ip_configurations'].append(new_item)
        else:
            results['frontend_ip_configurations'] = None
        if item.backend_address_pools is not None:
            results['backend_address_pools'] = []
            for value in item.backend_address_pools:
                results['backend_address_pools'].append(dict(name=value.name))
        else:
            results['backend_address_pools'] = None
        if item.probes is not None:
            results['probes'] = []
            for value in item.probes:
                results['probes'].append(dict(name=value.name,
                                              port=value.port,
                                              protocol=value.protocol,
                                              interval=value.interval_in_seconds,
                                              fail_count=value.number_of_probes,
                                              request_path=value.request_path))
        else:
            results['probes'] = None
        if item.inbound_nat_pools is not None:
            results['inbound_nat_pools'] = []
            for value in item.inbound_nat_pools:
                new_item = dict(name=value.name,
                                frontend_ip_configuration_name=None,
                                protocol=value.protocol,
                                frontend_port_range_start=value.frontend_port_range_start,
                                frontend_port_range_end=value.frontend_port_range_end,
                                backend_port=value.backend_port)
                if value.frontend_ip_configuration is not None:
                    new_item['frontend_ip_configuration_name'] = parse_resource_id(value.frontend_ip_configuration.id)['resource_name']
                results['inbound_nat_pools'].append(new_item)
        else:
            results['inbound_nat_pools'] = None
        if item.inbound_nat_rules is not None:
            results['inbound_nat_rules'] = []
            for value in item.inbound_nat_rules:
                new_item = dict(name=value.name,
                                frontend_ip_configuration=None,
                                protocol=value.protocol,
                                frontend_port=value.frontend_port,
                                idle_timeout=value.idle_timeout_in_minutes,
                                backend_port=value.backend_port,
                                enable_floating_ip=value.enable_floating_ip,
                                enable_tcp_reset=value.enable_tcp_reset)
                if value.frontend_ip_configuration is not None:
                    new_item['frontend_ip_configuration'] = parse_resource_id(value.frontend_ip_configuration.id)['resource_name']
                results['inbound_nat_rules'].append(new_item)
        else:
            results['inbound_nat_rules'] = None
        if item.load_balancing_rules is not None:
            results['load_balancing_rules'] = []
            for value in item.load_balancing_rules:
                new_item = dict(name=value.name,
                                frontend_ip_configuration=None,
                                backend_address_pool=None,
                                probe=None,
                                protocol=value.protocol,
                                load_distribution=value.load_distribution,
                                frontend_port=value.frontend_port,
                                backend_port=value.backend_port,
                                idle_timeout=value.idle_timeout_in_minutes,
                                enable_floating_ip=value.enable_floating_ip,
                                disable_outbound_snat=value.disable_outbound_snat,
                                enable_tcp_reset=value.enable_tcp_reset)
                if value.frontend_ip_configuration is not None:
                    new_item['frontend_ip_configuration'] = parse_resource_id(value.frontend_ip_configuration.id)['resource_name']
                if value.backend_address_pool is not None:
                    new_item['backend_address_pool'] = parse_resource_id(value.backend_address_pool.id)['resource_name']
                if value.probe is not None:
                    new_item['probe'] = parse_resource_id(value.probe.id)['resource_name']
                results['load_balancing_rules'].append(new_item)
        else:
            results['load_balancing_rules'] = None
        if item.outbound_rules is not None:
            results['outbound_rules'] = []
            for value in item.outbound_rules:
                new_item = dict(name=value.name,
                                allocated_outbound_ports=value.allocated_outbound_ports,
                                frontend_ip_configurations=[],
                                backend_address_pool=None,
                                protocol=value.protocol,
                                enable_tcp_reset=value.enable_tcp_reset,
                                idle_timeout_in_minutes=value.idle_timeout_in_minutes)
                if value.frontend_ip_configurations is not None:
                    for key in value.frontend_ip_configurations:
                        new_item['frontend_ip_configurations'].append(parse_resource_id(key.id)['resource_name'])
                else:
                    new_item['frontend_ip_configurations'] = None
                if value.backend_address_pool is not None:
                    new_item['backend_address_pool'] = parse_resource_id(value.backend_address_pool.id)['resource_name']
                results['outbound_rules'].append(new_item)
        else:
            results['outbound_rules'] = None

        return results

    def get_public_ip_address_instance(self, id):
        """Get a reference to the public ip address resource"""
        self.log('Fetching public ip address {0}'.format(id))
        resource_id = format_resource_id(id, self.subscription_id, 'Microsoft.Network', 'publicIPAddresses', self.resource_group)
        return self.network_models.PublicIPAddress(id=resource_id)

    def get_load_balancer(self):
        """Get a load balancer"""
        self.log('Fetching loadbalancer {0}'.format(self.name))
        try:
            return self.network_client.load_balancers.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            return None

    def delete_load_balancer(self):
        """Delete a load balancer"""
        self.log('Deleting loadbalancer {0}'.format(self.name))
        try:
            poller = self.network_client.load_balancers.begin_delete(self.resource_group, self.name)
            return self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error deleting loadbalancer {0} - {1}".format(self.name, str(exc)))

    def create_or_update_load_balancer(self, param):
        try:
            poller = self.network_client.load_balancers.begin_create_or_update(self.resource_group, self.name, param)
            new_lb = self.get_poller_result(poller)
            return new_lb
        except Exception as exc:
            self.fail("Error creating or updating load balancer {0} - {1}".format(self.name, str(exc)))

    def object_assign(self, patch, origin):
        attribute_map = set(self.network_models.LoadBalancer._attribute_map.keys()) - set(self.network_models.LoadBalancer._validation.keys())
        for key in attribute_map:
            if not getattr(patch, key):
                setattr(patch, key, getattr(origin, key))
        return patch

    def assign_protocol(self, patch, origin):
        attribute_map = ['probes', 'inbound_nat_rules', 'inbound_nat_pools', 'load_balancing_rules']
        for attribute in attribute_map:
            properties = getattr(patch, attribute)
            if not properties:
                continue
            references = getattr(origin, attribute) if origin else []
            for item in properties:
                if item.protocol:
                    continue
                refs = [x for x in references if to_native(x.name) == item.name]
                ref = refs[0] if len(refs) > 0 else None
                item.protocol = ref.protocol if ref else 'Tcp'
        return patch


def frontend_ip_configuration_id(subscription_id, resource_group_name, load_balancer_name, name):
    """Generate the id for a frontend ip configuration"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/loadBalancers/{2}/frontendIPConfigurations/{3}'.format(
        subscription_id,
        resource_group_name,
        load_balancer_name,
        name
    )


def backend_address_pool_id(subscription_id, resource_group_name, load_balancer_name, name):
    """Generate the id for a backend address pool"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/loadBalancers/{2}/backendAddressPools/{3}'.format(
        subscription_id,
        resource_group_name,
        load_balancer_name,
        name
    )


def probe_id(subscription_id, resource_group_name, load_balancer_name, name):
    """Generate the id for a probe"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/loadBalancers/{2}/probes/{3}'.format(
        subscription_id,
        resource_group_name,
        load_balancer_name,
        name
    )


def main():
    """Main execution"""
    AzureRMLoadBalancer()


if __name__ == '__main__':
    main()
