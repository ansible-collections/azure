#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_privatelinkservice_info

version_added: "1.12.0"

short_description: Get private endpoint connection info

description:
    - Get facts for private endpoint connection info.

options:
    name:
        description:
            - The name of the private link service.
        type: str
    resource_group:
        description:
            - The name of the resource group.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get private link service info by name
  azure_rm_privateelinkservice_info:
    name: pn-service-name
    resource_group: myResourceGroup

- name: Get all private link service by resource group
  azure_rm_privateelinkservice_info:
    resource_group: myResourceGroup

- name: Get all private link service by subscription filter by tags
  azure_rm_privateelinkservice_info:
    tags:
      - key1
      - abc
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
            sample: { "subscriptions": [] }
        enable_proxy_protocol:
            description:
                - Whether the private link service is enabled for proxy protocol or not
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
            sample: { "subscriptions": [] }
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
                        - The name of the IP configurations.
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
                            sample: { "id": "/subscriptions/xxx/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/vnet/subnets/subname" }
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
                    sample: "/subscriptions/xxx/resourceGroups/myReG/providers/Microsoft.Network/privateLinkServices/linkservice/privateEndpointConnections/tes"
                private_endpoint:
                    description:
                        - The ID of the private endpoint.
                    type: str
                    returned: always
                    sample: "/subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/privateEndpoints/test002"
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMPrivateLinkServiceInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type="str"),
            resource_group=dict(type="str"),
            tags=dict(type='list', elements='str')
        )

        self.name = None
        self.tags = None
        self.resource_group = None
        self.results = dict(
            changed=False,
        )

        super(AzureRMPrivateLinkServiceInfo, self).__init__(self.module_arg_spec,
                                                            supports_check_mode=True,
                                                            supports_tags=False,
                                                            facts_module=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name is not None and self.resource_group is not None:
            result = self.get_item()
        elif self.resource_group is not None:
            result = self.list_resourcegroup()
        else:
            result = self.list_by_subscription()

        self.results["link_service"] = [item for item in result if item and self.has_tags(item['tags'], self.tags)]
        return self.results

    def get_item(self):
        self.log("Get properties for {0} in {1}".format(self.name, self.resource_group))

        try:
            response = self.network_client.private_link_services.get(self.resource_group, self.name)
            return [self.service_to_dict(response)]
        except ResourceNotFoundError:
            self.log("Could not get info for {0} in {1}".format(self.name, self.resource_group))

        return []

    def list_resourcegroup(self):
        result = []
        self.log("List all in {0}".format(self.resource_group))
        try:
            response = self.network_client.private_link_services.list(self.resource_group)
            while True:
                result.append(response.next())
        except StopIteration:
            pass
        except Exception:
            pass
        return [self.service_to_dict(item) for item in result]

    def list_by_subscription(self):
        result = []
        self.log("List all in by subscription")
        try:
            response = self.network_client.private_link_services.list_by_subscription()
            while True:
                result.append(response.next())
        except StopIteration:
            pass
        except Exception:
            pass
        return [self.service_to_dict(item) for item in result]

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
            auto_approval=service.get('auto_approval'),
            fqdns=service.get('fqdns'),
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
    AzureRMPrivateLinkServiceInfo()


if __name__ == "__main__":
    main()
