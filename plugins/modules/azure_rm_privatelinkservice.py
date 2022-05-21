#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_privatelinkservice

version_added: "1.12.0"

short_description: Managed private link service resource

description:
    - Create, Update or Delete private link service resource.

options:
    name:
        description:
            - The name of the private link service.
        type: str
        required: True
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: True
    location:
        description:
            - The resource location.
        type: str
    load_balancer_frontend_ip_configurations:
        description:
            - An array of references to the load balancer IP configurations
            - Cannot have more than one load balancer frontend IP configuration on the private link service.
        type: list
        elements: dict
        suboptions:
            id:
                description:
                    - The load balancer frontend IP's ID.
                type: str
    fqdns:
        description:
            - The list of Fqdn.
        elements: str
        type: list
    auto_approval:
        description:
            - The auto-approval list of the private link service.
        type: dict
        suboptions:
            subscriptions:
                description:
                    - The list of subscriptions.
                type: list
                elements: str
    visibility:
        description:
            - The visibility list of the private link service.
        type: dict
        suboptions:
            subscriptions:
                description:
                    - The list of subscriptions.
                type: list
                elements: str
    enable_proxy_protocol:
        description:
            - Whether the private link service is enabled for proxy protocol or not.
        type: bool
    ip_configurations:
        description:
            - An array of private link service IP configurations.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of private link service ip configuration.
                type: str
            properties:
                description:
                    - The property of the private link service IP configurations.
                type: dict
                suboptions:
                    primary:
                        description:
                            - Whether the ip configuration is primary or not.
                        type: bool
                    private_ip_allocation_method:
                        description:
                            - The private IP address allocation method.
                        type: str
                        choices:
                            - Static
                            - Dynamic
                    private_ip_address_version:
                        description:
                            - Whether the specific IP configuration is IPv4 or IPv6.
                        type: str
                        choices:
                            - IPv4
                            - IPv6
                    subnet:
                        description:
                            - The reference to the subnet resource.
                        type: dict
                        suboptions:
                            id:
                                description:
                                    - The ID of the subnet.
                                type: str
    state:
        description:
            - Assert the state of the pirvate link service.
            - Use I(state=present) to create or update the link service and I(state=absent) to delete it.
        type: str
        default: present
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Create the private link service
  azure_rm_privatelinkservice:
    name: linkservice-name
    resource_group: myResourceGroup
    enable_proxy_protocol: True
    fqdns:
      - 'dns01.com'
      - 'dns02.com'
    visibility:
      subscriptions:
        - xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        - yyyyyy-yyyyy-yyyy-yyyy-yyyyyyyyyyy
    auto_approval:
      subscriptions:
        - xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        - yyyyyy-yyyyy-yyyy-yyyy-yyyyyyyyyyy
    load_balancer_frontend_ip_configurations:
          - id: load_balancer_frontend_ip_configurations_id
    ip_configurations:
      - name: testSubnet
        properties:
          primary: False
          private_ip_allocation_method: 'Dynamic'
          private_ip_address_version: 'IPv4'
          subnet:
            id: subnet_id
      - name: subnetfredprivate-1
        properties:
          primary: True
          private_ip_allocation_method: 'Static'
          private_ip_address_version: 'IPv4'
          subnet:
            id: subnet_id
    tags:
      key1: value1
      key2: value2

- name: delete the private link service
  azure_rm_privatelinkservice:
    name: linkservice-name
    resource_group: myResourceGroup
    state: absent
'''

RETURN = '''
link_service:
    description:
        - List of private link service info.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID of the private link service.
            sample: "/subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/privateLinkServices/linkservice"
            returned: always
            type: str
        name:
            description:
                - Name of the private link service.
            returned: always
            type: str
            sample: linkservice
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: eastus
        alias:
            description:
                - The alias of the private link service.
            type: str
            returned: always
            sample: "linkservice.6a244dd8-8416-40cf-8c04-52b353bdd507.eastus.azure.privatelinkservice"
        auto_approval:
            description:
                - The auto-approval list of the private link service.
            type: dict
            returned: always
            sample: { "subscriptions": ['xxxx-xxxx', 'yyyy-yyyyy'] }
        enable_proxy_protocol:
            description:
                - Whether the private link service is enabled for proxy protocol or not.
            type: bool
            returned: always
            sample: False
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            type: str
            returned: always
            sample: "f7d60f37-ea2b-4091-8546-1327f35468c4"
        type:
            description:
                - The resource type.
            type: str
            returned: always
            sample: Microsoft.Network/privateLinkServices
        visibility:
            description:
                - The visibility list of the private link service.
            type: dict
            returned: always
            sample: { "subscriptions": ['xxxx-xxxx', 'yyyy-yyyyy'] }
        tags:
            description:
                - The resource tags.
            type: dict
            returned: always
            sample: { 'key1': 'value1' }
        provisioning_state:
            description:
                - The provisioning state of the private link service resource.
            type: str
            returned: always
            sample: Succeeded
        network_interfaces:
            description:
                - An array of references to the network interfaces created for this private link service.
            type: list
            returned: always
            sample:  [{ "id": "/subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/networkInterfaces/testlinkservice.nic.f5"}]
        ip_configurations:
            description:
                - An array of private link service IP configurations.
            type: complex
            returned: always
            contains:
                name:
                    description:
                        - The name of the IP configurations
                    type: str
                    returned: always
                    sample: subnetfredprivate-1
                properties:
                    description:
                        - The IP configuration properties.
                    type: complex
                    returned: always
                    contains:
                        primary:
                            description:
                                - Whether the ip configuration is primary or not.
                            returned: always
                            type: bool
                            sample: True
                        private_ip_address_version:
                            description:
                                - Whether the specific IP configuration is IPv4 or IPv6.
                            returned: always
                            type: str
                            sample: IPv4
                        private_ip_allocation_method:
                            description:
                                - The private IP address allocation method.
                            returned: always
                            type: str
                            sample: Dynamic
                        subnet:
                            description:
                                - The reference to the subnet resource.
                            returned: always
                            type: dict
                            sample: { "id": "/subscriptions/xxx/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/vnet/subnets/subnamee" }
        load_balancer_frontend_ip_configurations:
            description:
                - An array of references to the load balancer IP configurations.
            type: list
            returned: awalys
            sample: [{ "id": "/subscriptions/xxx/resourceGroups/myRG/providers/Microsoft.Network/loadBalancers/testlb/frontendIPConfigurations/front01" }]
        fqdns:
            description:
                - The list of Fqdn.
            type: list
            returned: always
            sample: ['fqdns1.com', 'fqdns2.com']
        private_endpoint_connections:
            description:
                - An array of list about connections to the private endpoint.
            type: complex
            returned: always
            contains:
                id:
                    description:
                        - The ID of the private endpoint connection.
                    type: str
                    returned: always
                    sample: "/subscriptions/xxx/resourceGroups/myRG/providers/Microsoft.Network/privateLinkServices/linkservice/privateEndpointConnections/tes"
                private_endpoint:
                    description:
                        - The ID of the private endpoint.
                    type: str
                    returned: always
                    sample: "/subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/privateEndpoints/test002"
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except Exception:
    # This is handled in azure_rm_common
    pass


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

load_balancer_frontend_ip_configurations_spec = dict(
    id=dict(type='str'),
)

auto_approval_spec = dict(
    subscriptions=dict(type='list', elements='str')
)

visibility_spec = dict(
    subscriptions=dict(type='list', elements='str')
)

properties_spec = dict(
    primary=dict(type='bool'),
    # private_ip_address=dict(type='str'),
    private_ip_allocation_method=dict(type='str', choices=['Static', 'Dynamic']),
    subnet=dict(type='dict', options=dict(id=dict(type='str'))),
    private_ip_address_version=dict(type='str', choices=['IPv4', 'IPv6'])
)


class AzureRMPrivateLinkService(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type="str", required=True),
            resource_group=dict(type="str", required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            load_balancer_frontend_ip_configurations=dict(
                type='list',
                elements='dict',
                options=load_balancer_frontend_ip_configurations_spec
            ),
            ip_configurations=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(type='str'),
                    properties=dict(type='dict', options=properties_spec)
                )
            ),
            visibility=dict(type='dict', options=visibility_spec),
            fqdns=dict(type='list', elements='str'),
            enable_proxy_protocol=dict(type='bool'),
            auto_approval=dict(type='dict', options=auto_approval_spec),
        )

        self.name = None
        self.resource_group = None
        self.location = None
        self.tags = None
        self.state = None
        self.results = dict(
            changed=False,
        )
        self.body = {}

        super(AzureRMPrivateLinkService, self).__init__(self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=True,
                                                        facts_module=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        old_response = self.get_item()
        result = None
        changed = False

        if not self.location:
            resource_group = self.get_resource_group(self.resource_group)
            self.location = resource_group.location

        self.body['location'] = self.location
        self.body['tags'] = self.tags

        if self.state == 'present':
            if old_response:
                update_tags, tags = self.update_tags(old_response['tags'])
                if update_tags:
                    changed = True
                self.body['tags'] = tags
                if self.body.get('enable_proxy_protocol') is not None:
                    if self.body.get('enable_proxy_protocol') != old_response['enable_proxy_protocol']:
                        changed = True
                else:
                    self.body['enable_proxy_protocol'] = old_response['enable_proxy_protocol']

                if self.body.get("auto_approval") is not None:
                    for value in old_response["auto_approval"]['subscriptions']:
                        if value not in self.body["auto_approval"]['subscriptions']:
                            self.body["auto_approval"]['subscriptions'].append(value)
                    if len(self.body["auto_approval"]['subscriptions']) != len(old_response["auto_approval"]['subscriptions']):
                        changed = True
                else:
                    self.body["auto_approval"] = old_response["auto_approval"]

                if self.body.get("visibility") is not None:
                    for value in old_response["visibility"]['subscriptions']:
                        if value not in self.body["visibility"]['subscriptions']:
                            self.body["visibility"]['subscriptions'].append(value)
                    if len(self.body["visibility"]['subscriptions']) != len(old_response["visibility"]['subscriptions']):
                        changed = True
                else:
                    self.body["visibility"] = old_response["visibility"]

                if self.body.get('fqdns') is not None:
                    for value in old_response['fqdns']:
                        if value not in self.body['fqdns']:
                            self.body['fqdns'].append(value)
                    if len(self.body.get('fqdns')) != len(old_response['fqdns']):
                        changed = True
                else:
                    self.body['fqdns'] = old_response['fqdns']

                if self.body.get('load_balancer_frontend_ip_configurations') is not None:
                    if self.body['load_balancer_frontend_ip_configurations'] != old_response['load_balancer_frontend_ip_configurations']:
                        self.fail("Private Link Service Load Balancer Reference Cannot Be Changed")
                else:
                    self.body['load_balancer_frontend_ip_configurations'] = old_response['load_balancer_frontend_ip_configurations']

                if self.body.get('ip_configurations') is not None:
                    for items in old_response['ip_configurations']:
                        if items['name'] not in [item['name'] for item in self.body['ip_configurations']]:
                            self.body['ip_configurations'].append(items)
                    if len(self.body['ip_configurations']) != len(old_response['ip_configurations']):
                        changed = True
                else:
                    self.body['ip_configurations'] = old_response['ip_configurations']
            else:
                changed = True

            if changed:
                if self.check_mode:
                    self.log("Check mode test. The private link service is exist, will be create or updated")
                else:
                    result = self.create_or_update(self.body)
            else:
                if self.check_mode:
                    self.log("Check mode test. The private endpoint connection is exist, No operation in this task")
                else:
                    self.log("The private endpoint connection is exist, No operation in this task")
                    result = old_response
        else:
            if old_response:
                changed = True
                if self.check_mode:
                    self.log("Check mode test. The private link service is exist, will be deleted")
                else:
                    result = self.delete_resource()
            else:
                if self.check_mode:
                    self.log("The private link service isn't exist, no action")
                else:
                    self.log("The private link service isn't exist, don't need to delete")

        self.results["link_service"] = result
        self.results['changed'] = changed
        return self.results

    def get_item(self):
        self.log("Get properties for {0} in {1}".format(self.name, self.resource_group))
        try:
            response = self.network_client.private_link_services.get(self.resource_group, self.name)
            return self.service_to_dict(response)
        except ResourceNotFoundError:
            self.log("Could not get info for {0} in {1}".format(self.name, self.resource_group))

        return []

    def create_or_update(self, parameters):
        self.log("Create or update the private link service for {0} in {1}".format(self.name, self.resource_group))
        try:
            response = self.network_client.private_link_services.begin_create_or_update(self.resource_group, self.name, parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

            result = self.network_client.private_link_services.get(self.resource_group, self.name)
            return self.service_to_dict(result)
        except Exception as ec:
            self.fail("Create or Update {0} in {1} failed, mesage {2}".format(self.name, self.resource_group, ec))

        return []

    def delete_resource(self):
        self.log("delete the private link service for {0} in {1}".format(self.name, self.resource_group))
        try:
            response = self.network_client.private_link_services.begin_delete(self.resource_group, self.name)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
            return response
        except Exception as ec:
            self.fail("Delete {0} in {1} failed, message {2}".format(self.name, self.resource_group, ec))

        return []

    def service_to_dict(self, service_info):

        service = service_info.as_dict()
        result = dict(
            id=service.get("id"),
            name=service.get('name'),
            type=service.get('type'),
            etag=service.get('etag'),
            location=service.get('location'),
            tags=service.get('tags'),
            load_balancer_frontend_ip_configurations=service.get('load_balancer_frontend_ip_configurations'),
            ip_configurations=list(),
            network_interfaces=service.get('network_interfaces'),
            provisioning_state=service.get('provisioning_state'),
            private_endpoint_connections=list(),
            visibility=service.get('visibility'),
            fqdns=service.get('fqdns'),
            auto_approval=service.get('auto_approval'),
            alias=service.get('alias'),
            enable_proxy_protocol=service.get('enable_proxy_protocol')
        )
        if service.get('private_endpoint_connections'):
            for items in service['private_endpoint_connections']:
                result['private_endpoint_connections'].append({'id': items['id'], 'private_endpoint': items['private_endpoint']['id']})

        if service.get('ip_configurations'):
            for items in service['ip_configurations']:
                result['ip_configurations'].append(
                    {
                        "name": items['name'],
                        'properties': {
                            "primary": items['primary'],
                            "private_ip_address_version": items["private_ip_address_version"],
                            "private_ip_allocation_method": items["private_ip_allocation_method"],
                            "subnet": items["subnet"],
                        }
                    }
                )

        return result


def main():
    AzureRMPrivateLinkService()


if __name__ == "__main__":
    main()
