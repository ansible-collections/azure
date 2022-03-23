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
module: azure_rm_subnet
version_added: "0.1.0"
short_description: Manage Azure subnets
description:
    - Create, update or delete a subnet within a given virtual network.
    - Allows setting and updating the address prefix CIDR, which must be valid within the context of the virtual network.
    - Use the M(azure.azcollection.azure_rm_networkinterface) module to associate interfaces with the subnet and assign specific IP addresses.
options:
    resource_group:
        description:
            - Name of resource group.
        required: true
    name:
        description:
            - Name of the subnet.
        required: true
    address_prefix_cidr:
        description:
            - CIDR defining the IPv4 address space of the subnet. Must be valid within the context of the virtual network.
        aliases:
            - address_prefix
    address_prefixes_cidr:
        description:
            - CIDR defining the IPv4 and IPv6 address space of the subnet. Must be valid within the context of the virtual network.
            - If set I(address_prefix), It will not set.
        aliases:
            - address_prefixes
        type: list
        version_added: "1.0.0"
    security_group:
        description:
            - Existing security group with which to associate the subnet.
            - It can be the security group name which is in the same resource group.
            - Can be the resource ID of the security group.
            - Can be a dict containing the I(name) and I(resource_group) of the security group.
        aliases:
            - security_group_name
    state:
        description:
            - Assert the state of the subnet. Use C(present) to create or update a subnet and use C(absent) to delete a subnet.
        default: present
        choices:
            - absent
            - present
    virtual_network_name:
        description:
            - Name of an existing virtual network with which the subnet is or will be associated.
        required: true
        aliases:
            - virtual_network
    route_table:
        description:
            - The reference of the RouteTable resource.
            - Can be the name or resource ID of the route table.
            - Can be a dict containing the I(name) and I(resource_group) of the route table.
            - Without this configuration, the associated route table will be dissociate. If there is no associated route table, it has no impact.
    service_endpoints:
        description:
            - An array of service endpoints.
        type: list
        suboptions:
            service:
                description:
                    - The type of the endpoint service.
                required: True
            locations:
                description:
                    - A list of locations.
                type: list
    private_endpoint_network_policies:
        description:
            - C(Enabled) or C(Disabled) apply network policies on private endpoints in the subnet.
        type: str
        default: Enabled
        choices:
            - Enabled
            - Disabled
    private_link_service_network_policies:
        description:
            - C(Enabled) or C(Disabled) apply network policies on private link service in the subnet.
        type: str
        default: Enabled
        choices:
            - Enabled
            - Disabled
    delegations:
        description:
            - An array of delegations.
        type: list
        suboptions:
            name:
                description:
                    - The name of delegation.
                required: True
            serviceName:
                description:
                    - The type of the endpoint service.
                required: True
                choices:
                    - Microsoft.Web/serverFarms
                    - Microsoft.ContainerInstance/containerGroups
                    - Microsoft.Netapp/volumes
                    - Microsoft.HardwareSecurityModules/dedicatedHSMs
                    - Microsoft.ServiceFabricMesh/networks
                    - Microsoft.Logic/integrationServiceEnvironments
                    - Microsoft.Batch/batchAccounts
                    - Microsoft.Sql/managedInstances
                    - Microsoft.Web/hostingEnvironments
                    - Microsoft.BareMetal/CrayServers
                    - Microsoft.BareMetal/MonitoringServers
                    - Microsoft.Databricks/workspaces
                    - Microsoft.BareMetal/AzureHostedService
                    - Microsoft.BareMetal/AzureVMware
                    - Microsoft.BareMetal/AzureHPC
                    - Microsoft.BareMetal/AzurePaymentHSM
                    - Microsoft.StreamAnalytics/streamingJobs
                    - Microsoft.DBforPostgreSQL/serversv2
                    - Microsoft.AzureCosmosDB/clusters
                    - Microsoft.MachineLearningServices/workspaces
                    - Microsoft.DBforPostgreSQL/singleServers
                    - Microsoft.DBforPostgreSQL/flexibleServers
                    - Microsoft.DBforMySQL/serversv2
                    - Microsoft.DBforMySQL/flexibleServers
                    - Microsoft.ApiManagement/service
                    - Microsoft.Synapse/workspaces
                    - Microsoft.PowerPlatform/vnetaccesslinks
                    - Microsoft.Network/managedResolvers
                    - Microsoft.Kusto/clusters
            actions:
                description:
                    - A list of actions.
                type: list

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Chris Houseknecht (@chouseknecht)
    - Matt Davis (@nitzmahone)

'''

EXAMPLES = '''
    - name: Create a subnet
      azure_rm_subnet:
        resource_group: myResourceGroup
        virtual_network_name: myVirtualNetwork
        name: mySubnet
        address_prefix_cidr: "10.1.0.0/24"

    - name: Create a subnet refer nsg from other resource group
      azure_rm_subnet:
        resource_group: myResourceGroup
        virtual_network_name: myVirtualNetwork
        name: mySubnet
        address_prefix_cidr: "10.1.0.0/16"
        security_group:
          name: secgroupfoo
          resource_group: mySecondResourceGroup
        route_table: route

    - name: Create a subnet with service endpoint
      azure_rm_subnet:
        resource_group: myResourceGroup
        virtual_network_name: myVirtualNetwork
        name: mySubnet
        address_prefix_cidr: "10.1.0.0/16"
        service_endpoints:
          - service: "Microsoft.Sql"
            locations:
              - "eastus"

    - name: Create a subnet with delegations
      azure_rm_subnet:
        resource_group: myResourceGroup
        virtual_network_name: myVirtualNetwork
        name: mySubnet
        address_prefix_cidr: "10.1.0.0/16"
        delegations:
          - name: 'mydeleg'
            serviceName: 'Microsoft.ContainerInstance/containerGroups'

    - name: Delete a subnet
      azure_rm_subnet:
        resource_group: myResourceGroup
        virtual_network_name: myVirtualNetwork
        name: mySubnet
        state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the subnet.
    returned: success
    type: complex
    contains:
        address_prefix:
            description:
                - IP address CIDR.
            returned: always
            type: str
            sample: "10.1.0.0/16"
        address_prefixes:
            description:
                - IP address for IPv4 and IPv6 CIDR.
            returned: always
            type: list
            sample: ["10.2.0.0/24", "fdda:e69b:1587:495e::/64"]
        id:
            description:
                - Subnet resource path.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroup/myResourceGroup/providers/Microsoft.Network/virtualNetworks/myVirtualNetwork/subnets/mySubnet"
        name:
            description:
                - Subnet name.
            returned: always
            type: str
            sample: "foobar"
        network_security_group:
            description:
                - Associated network security group of subnets.
            returned: always
            type: complex
            contains:
                id:
                    description:
                        - Security group resource identifier.
                    returned: always
                    type: str
                    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroup/myResourceGroup/providers/Microsoft.Network/networkSecurityGroups/secgroupfoo"
                name:
                    description:
                        - Name of the security group.
                    returned: always
                    type: str
                    sample: "secgroupfoo"
        provisioning_state:
            description:
                - Success or failure of the provisioning event.
            returned: always
            type: str
            sample: "Succeeded"
        private_endpoint_network_policies:
            description:
                - C(Enabled) or C(Disabled) apply network policies on private endpoints in the subnet.
            returned: always
            type: str
            sample: "Enabled"
        private_link_service_network_policies:
            description:
                - C(Enabled) or C(Disabled) apply network policies on private link service in the subnet.
            returned: always
            type: str
            sample: "Disabled"
        delegations:
            description:
                - Associated delegation of subnets
            returned: always
            type: list
            contains:
                name:
                    description:
                        - name of delegation
                    returned: when delegation is present
                    type: str
                    sample: "delegationname"
                serviceName:
                    description:
                        - service associated to delegation
                    returned: when delegation is present
                    type: str
                    sample: "Microsoft.ContainerInstance/containerGroups"
                actions:
                    description:
                        - list of actions associated with service of delegation
                    returned : when delegation is present
                    type: list
                    sample: ["Microsoft.Network/virtualNetworks/subnets/action"]
'''  # NOQA

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, CIDR_PATTERN, azure_id_to_dict, format_resource_id

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


delegations_spec = dict(
    name=dict(
        type='str',
        required=True
    ),
    serviceName=dict(
        type='str',
        required=True,
        choices=['Microsoft.Web/serverFarms', 'Microsoft.ContainerInstance/containerGroups', 'Microsoft.Netapp/volumes',
                 'Microsoft.HardwareSecurityModules/dedicatedHSMs', 'Microsoft.ServiceFabricMesh/networks',
                 'Microsoft.Logic/integrationServiceEnvironments', 'Microsoft.Batch/batchAccounts', 'Microsoft.Sql/managedInstances',
                 'Microsoft.Web/hostingEnvironments', 'Microsoft.BareMetal/CrayServers', 'Microsoft.BareMetal/MonitoringServers',
                 'Microsoft.Databricks/workspaces', 'Microsoft.BareMetal/AzureHostedService', 'Microsoft.BareMetal/AzureVMware',
                 'Microsoft.BareMetal/AzureHPC', 'Microsoft.BareMetal/AzurePaymentHSM', 'Microsoft.StreamAnalytics/streamingJobs',
                 'Microsoft.DBforPostgreSQL/serversv2', 'Microsoft.AzureCosmosDB/clusters', 'Microsoft.MachineLearningServices/workspaces',
                 'Microsoft.DBforPostgreSQL/singleServers', 'Microsoft.DBforPostgreSQL/flexibleServers', 'Microsoft.DBforMySQL/serversv2',
                 'Microsoft.DBforMySQL/flexibleServers', 'Microsoft.ApiManagement/service', 'Microsoft.Synapse/workspaces',
                 'Microsoft.PowerPlatform/vnetaccesslinks', 'Microsoft.Network/managedResolvers', 'Microsoft.Kusto/clusters']
    ),
    actions=dict(
        type='list',
        default=[]
    )
)


def subnet_to_dict(subnet):
    result = dict(
        id=subnet.id,
        name=subnet.name,
        provisioning_state=subnet.provisioning_state,
        address_prefix=subnet.address_prefix,
        address_prefixes=subnet.address_prefixes,
        network_security_group=dict(),
        route_table=dict(),
        private_endpoint_network_policies=subnet.private_endpoint_network_policies,
        private_link_service_network_policies=subnet.private_link_service_network_policies
    )
    if subnet.network_security_group:
        id_keys = azure_id_to_dict(subnet.network_security_group.id)
        result['network_security_group']['id'] = subnet.network_security_group.id
        result['network_security_group']['name'] = id_keys['networkSecurityGroups']
        result['network_security_group']['resource_group'] = id_keys['resourceGroups']
    if subnet.route_table:
        id_keys = azure_id_to_dict(subnet.route_table.id)
        result['route_table']['id'] = subnet.route_table.id
        result['route_table']['name'] = id_keys['routeTables']
        result['route_table']['resource_group'] = id_keys['resourceGroups']
    if subnet.service_endpoints:
        result['service_endpoints'] = [{'service': item.service, 'locations': item.locations or []} for item in subnet.service_endpoints]
    if subnet.delegations:
        result['delegations'] = [{'name': item.name, 'serviceName': item.service_name, 'actions': item.actions or []} for item in subnet.delegations]
    return result


class AzureRMSubnet(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            virtual_network_name=dict(type='str', required=True, aliases=['virtual_network']),
            address_prefix_cidr=dict(type='str', aliases=['address_prefix']),
            address_prefixes_cidr=dict(type='list', aliases=['address_prefixes']),
            security_group=dict(type='raw', aliases=['security_group_name']),
            route_table=dict(type='raw'),
            service_endpoints=dict(
                type='list'
            ),
            private_endpoint_network_policies=dict(
                type='str',
                default='Enabled',
                choices=['Enabled', 'Disabled']
            ),
            private_link_service_network_policies=dict(
                type='str',
                default='Enabled',
                choices=['Enabled', 'Disabled']
            ),
            delegations=dict(
                type='list',
                elements='dict',
                options=delegations_spec
            )
        )

        mutually_exclusive = [['address_prefix_cidr', 'address_prefixes_cidr']]

        self.results = dict(
            changed=False,
            state=dict()
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.virtual_network_name = None
        self.address_prefix_cidr = None
        self.address_prefixes_cidr = None
        self.security_group = None
        self.route_table = None
        self.service_endpoints = None
        self.private_link_service_network_policies = None
        self.private_endpoint_network_policies = None
        self.delegations = None

        super(AzureRMSubnet, self).__init__(self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=False)

    def exec_module(self, **kwargs):

        nsg = None
        subnet = None

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.delegations and len(self.delegations) > 1:
            self.fail("Only one delegation is supported for a subnet")

        if self.address_prefix_cidr and not CIDR_PATTERN.match(self.address_prefix_cidr):
            self.fail("Invalid address_prefix_cidr value {0}".format(self.address_prefix_cidr))

        nsg = dict()
        if self.security_group:
            nsg = self.parse_nsg()

        route_table = dict()
        if self.route_table:
            route_table = self.parse_resource_to_dict(self.route_table)
            self.route_table = format_resource_id(val=route_table['name'],
                                                  subscription_id=route_table['subscription_id'],
                                                  namespace='Microsoft.Network',
                                                  types='routeTables',
                                                  resource_group=route_table['resource_group'])

        results = dict()
        changed = False

        try:
            self.log('Fetching subnet {0}'.format(self.name))
            subnet = self.network_client.subnets.get(self.resource_group,
                                                     self.virtual_network_name,
                                                     self.name)
            self.check_provisioning_state(subnet, self.state)
            results = subnet_to_dict(subnet)

            if self.state == 'present':
                if self.private_endpoint_network_policies is not None:
                    if results['private_endpoint_network_policies'] != self.private_endpoint_network_policies:
                        self.log("CHANGED: subnet {0} private_endpoint_network_policies".format(self.private_endpoint_network_policies))
                        changed = True
                        results['private_endpoint_network_policies'] = self.private_endpoint_network_policies
                else:
                    subnet['private_endpoint_network_policies'] = results['private_endpoint_network_policies']
                if self.private_link_service_network_policies is not None:
                    if results['private_link_service_network_policies'] != self.private_link_service_network_policies is not None:
                        self.log("CHANGED: subnet {0} private_link_service_network_policies".format(self.private_link_service_network_policies))
                        changed = True
                        results['private_link_service_network_policies'] = self.private_link_service_network_policies
                else:
                    subnet['private_link_service_network_policies'] = results['private_link_service_network_policies']

                if self.address_prefix_cidr and results['address_prefix'] != self.address_prefix_cidr:
                    self.log("CHANGED: subnet {0} address_prefix_cidr".format(self.name))
                    changed = True
                    results['address_prefix'] = self.address_prefix_cidr
                if self.address_prefixes_cidr and results['address_prefixes'] != self.address_prefixes_cidr:
                    self.log("CHANGED: subnet {0} address_prefixes_cidr".format(self.name))
                    changed = True
                    results['address_prefixes'] = self.address_prefixes_cidr

                if self.security_group is not None and results['network_security_group'].get('id') != nsg.get('id'):
                    self.log("CHANGED: subnet {0} network security group".format(self.name))
                    changed = True
                    results['network_security_group']['id'] = nsg.get('id')
                    results['network_security_group']['name'] = nsg.get('name')
                if self.route_table is not None:
                    if self.route_table != results['route_table'].get('id'):
                        changed = True
                        results['route_table']['id'] = self.route_table
                        self.log("CHANGED: subnet {0} route_table to {1}".format(self.name, route_table.get('name')))
                else:
                    if results['route_table'].get('id') is not None:
                        changed = True
                        results['route_table']['id'] = None
                        self.log("CHANGED: subnet {0} will dissociate to route_table {1}".format(self.name, route_table.get('name')))

                if self.service_endpoints or self.service_endpoints == []:
                    oldd = {}
                    for item in self.service_endpoints:
                        name = item['service']
                        locations = item.get('locations') or []
                        oldd[name] = {'service': name, 'locations': locations.sort()}
                    newd = {}
                    if 'service_endpoints' in results:
                        for item in results['service_endpoints']:
                            name = item['service']
                            locations = item.get('locations') or []
                            newd[name] = {'service': name, 'locations': locations.sort()}
                    if newd != oldd:
                        changed = True
                        results['service_endpoints'] = self.service_endpoints

                if self.delegations:
                    oldde = {}
                    for item in self.delegations:
                        name = item['name']
                        serviceName = item['serviceName']
                        actions = item.get('actions') or []
                        oldde[name] = {'name': name, 'serviceName': serviceName, 'actions': actions.sort()}
                    newde = {}
                    if 'delegations' in results:
                        for item in results['delegations']:
                            name = item['name']
                            serviceName = item['serviceName']
                            actions = item.get('actions') or []
                            newde[name] = {'name': name, 'serviceName': serviceName, 'actions': actions.sort()}
                    if newde != oldde:
                        changed = True
                        results['delegations'] = self.delegations

            elif self.state == 'absent':
                changed = True
        except ResourceNotFoundError:
            # the subnet does not exist
            if self.state == 'present':
                changed = True

        self.results['changed'] = changed
        self.results['state'] = results

        if not self.check_mode:

            if self.state == 'present' and changed:
                if not subnet:
                    # create new subnet
                    if not self.address_prefix_cidr and not self.address_prefixes_cidr:
                        self.fail('address_prefix_cidr or address_prefixes_cidr is not set')
                    self.log('Creating subnet {0}'.format(self.name))
                    subnet = self.network_models.Subnet(
                        address_prefix=self.address_prefix_cidr,
                        address_prefixes=self.address_prefixes_cidr
                    )
                    if nsg:
                        subnet.network_security_group = self.network_models.NetworkSecurityGroup(id=nsg.get('id'))
                    if self.route_table:
                        subnet.route_table = self.network_models.RouteTable(id=self.route_table)
                    if self.service_endpoints:
                        subnet.service_endpoints = self.service_endpoints
                    if self.private_endpoint_network_policies:
                        subnet.private_endpoint_network_policies = self.private_endpoint_network_policies
                    if self.private_link_service_network_policies:
                        subnet.private_link_service_network_policies = self.private_link_service_network_policies
                    if self.delegations:
                        subnet.delegations = self.delegations
                else:
                    # update subnet
                    self.log('Updating subnet {0}'.format(self.name))
                    subnet = self.network_models.Subnet(
                        address_prefix=results['address_prefix'],
                        address_prefixes=results['address_prefixes']
                    )
                    if results['network_security_group'].get('id') is not None:
                        subnet.network_security_group = self.network_models.NetworkSecurityGroup(id=results['network_security_group'].get('id'))
                    if results['route_table'].get('id') is not None:
                        subnet.route_table = self.network_models.RouteTable(id=results['route_table'].get('id'))

                    if results.get('service_endpoints') is not None:
                        subnet.service_endpoints = results['service_endpoints']
                    if results.get('private_link_service_network_policies') is not None:
                        subnet.private_link_service_network_policies = results['private_link_service_network_policies']
                    if results.get('private_endpoint_network_policies') is not None:
                        subnet.private_endpoint_network_policies = results['private_endpoint_network_policies']
                    if results.get('delegations') is not None:
                        subnet.delegations = results['delegations']

                self.results['state'] = self.create_or_update_subnet(subnet)
            elif self.state == 'absent' and changed:
                # delete subnet
                self.delete_subnet()
                # the delete does not actually return anything. if no exception, then we'll assume
                # it worked.
                self.results['state']['status'] = 'Deleted'

        return self.results

    def create_or_update_subnet(self, subnet):
        try:
            poller = self.network_client.subnets.begin_create_or_update(self.resource_group,
                                                                        self.virtual_network_name,
                                                                        self.name,
                                                                        subnet)
            new_subnet = self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error creating or updating subnet {0} - {1}".format(self.name, str(exc)))
        self.check_provisioning_state(new_subnet)
        return subnet_to_dict(new_subnet)

    def delete_subnet(self):
        self.log('Deleting subnet {0}'.format(self.name))
        try:
            poller = self.network_client.subnets.begin_delete(self.resource_group,
                                                              self.virtual_network_name,
                                                              self.name)
            result = self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error deleting subnet {0} - {1}".format(self.name, str(exc)))

        return result

    def parse_nsg(self):
        nsg = self.security_group
        resource_group = self.resource_group
        if isinstance(self.security_group, dict):
            nsg = self.security_group.get('name')
            resource_group = self.security_group.get('resource_group', self.resource_group)
        id = format_resource_id(val=nsg,
                                subscription_id=self.subscription_id,
                                namespace='Microsoft.Network',
                                types='networkSecurityGroups',
                                resource_group=resource_group)
        name = azure_id_to_dict(id).get('name')
        return dict(id=id, name=name)


def main():
    AzureRMSubnet()


if __name__ == '__main__':
    main()
