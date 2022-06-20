#!/usr/bin/python
#
# Copyright (c) 2022 Andrea Decorte, <adecorte@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_natgateway_info
version_added: "1.13.0"
short_description: Retrieve NAT Gateway instance facts
description:
    - Get facts for a NAT Gateway instance.
options:
    name:
        description:
            - Only show results for a specific NAT gateway.
        type: str
    resource_group:
        description:
            - Limit results by resource group.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Andrea Decorte (@andreadecorte)
'''

EXAMPLES = '''
    - name: Get facts for NAT gateway by name.
      azure_rm_natgateway_info:
        name: Mynatgw
        resource_group: MyResourceGroup

    - name: Get facts for all NAT gateways in resource group.
      azure_rm_natgateway_info:
        resource_group: MyResourceGroup

    - name: Get facts for all NAT gateways.
      azure_rm_natgateway_info:
'''

RETURN = '''
gateways:
    description:
        - A list of dictionaries containing facts for a NAT gateway.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description:
                - NAT gateway resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/natGateways/mynatgw
        name:
            description:
                - Name of NAT gateway.
            returned: always
            type: str
            sample: mynatgw
        resource_group:
            description:
                - Name of resource group.
            returned: always
            type: str
            sample: myResourceGroup
        location:
            description:
                - Location of NAT gateway.
            returned: always
            type: str
            sample: centralus
        idle_timeout_in_minutes:
            description:
                - The idle timeout of the NAT gateway.
            returned: always
            type: int
            sample: 4
        sku:
            description:
                - SKU of the NAT gateway.
            returned: always
            type: dict
            contains:
                name:
                    description:
                        - The name of the SKU.
                    returned: always
                    type: str
                    sample: Standard
        zones:
            description:
                - Availability Zones of the NAT gateway.
            returned: always
            type: list
            elements: str
        public_ip_addresses:
            description:
                - List of ids of public IP addresses associated to the NAT Gateway.
            returned: always
            type: list
            elements: str
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from msrestazure.tools import parse_resource_id
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMNATGatewayInfo(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
        )

        self.results = dict(
            changed=False,
        )

        self.name = None
        self.resource_group = None

        super(AzureRMNATGatewayInfo, self).__init__(self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False,
                                                    facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results["gateways"] = self.get()
        elif self.resource_group is not None:
            self.results["gateways"] = self.list_by_rg()
        else:
            self.results["gateways"] = self.list_all()

        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.network_client.nat_gateways.get(resource_group_name=self.resource_group, nat_gateway_name=self.name)
        except ResourceNotFoundError:
            pass

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_rg(self):
        response = None
        results = []
        try:
            response = self.network_client.nat_gateways.list(resource_group_name=self.resource_group)
        except Exception as exc:
            request_id = exc.request_id if exc.request_id else ''
            self.fail("Error listing NAT gateways in resource groups {0}: {1} - {2}".format(self.resource_group, request_id, str(exc)))

        for item in response:
            results.append(self.format_response(item))

        return results

    def list_all(self):
        response = None
        results = []
        try:
            response = self.network_client.nat_gateways.list_all()
        except Exception as exc:
            request_id = exc.request_id if exc.request_id else ''
            self.fail("Error listing all NAT gateways: {0} - {1}".format(request_id, str(exc)))

        for item in response:
            results.append(self.format_response(item))

        return results

    def format_response(self, natgw):
        d = natgw.as_dict()
        id = d.get("id")
        id_dict = parse_resource_id(id)
        d = {
            "id": id,
            "name": d.get("name"),
            "resource_group": id_dict.get("resource_group", self.resource_group),
            "location": d.get("location"),
            "sku": d.get("sku"),
            "zones": d.get("zones"),
            "idle_timeout_in_minutes": d.get("idle_timeout_in_minutes"),
            "public_ip_addresses": d.get("public_ip_addresses")
        }
        return d


def main():
    AzureRMNATGatewayInfo()


if __name__ == "__main__":
    main()
