#!/usr/bin/python
#
# Copyright (c) 2021 Ross Bender (@l3ender)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_appgateway_info
version_added: "1.10.0"
short_description: Retrieve Application Gateway instance facts
description:
    - Get facts for a Application Gateway instance.
options:
    name:
        description:
            - Only show results for a specific application gateway.
        type: str
    resource_group:
        description:
            - Limit results by resource group.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Ross Bender (@l3ender)
'''

EXAMPLES = '''
    - name: Get facts for application gateway by name.
      azure_rm_appgateway_info:
        name: MyAppgw
        resource_group: MyResourceGroup

    - name: Get facts for application gateways in resource group.
      azure_rm_appgateway_info:
        resource_group: MyResourceGroup

    - name: Get facts for all application gateways.
      azure_rm_appgateway_info:
'''

RETURN = '''
gateways:
    description:
        - A list of dictionaries containing facts for an application gateway.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description:
                - Application gateway resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/applicationGateways/myAppGw
        name:
            description:
                - Name of application gateway.
            returned: always
            type: str
            sample: myAppGw
        resource_group:
            description:
                - Name of resource group.
            returned: always
            type: str
            sample: myResourceGroup
        location:
            description:
                - Location of application gateway.
            returned: always
            type: str
            sample: centralus
        operational_state:
            description:
                - Operating state of application gateway.
            returned: always
            type: str
            sample: Running
        provisioning_state:
            description:
                - Provisioning state of application gateway.
            returned: always
            type: str
            sample: Succeeded
        ssl_policy:
            description:
                - SSL policy of the application gateway.
            returned: always
            type: complex
            version_added: "1.11.0"
            contains:
                policy_type:
                    description:
                        - The type of SSL policy.
                    returned: always
                    type: str
                    sample: predefined
                policy_name:
                    description:
                        - The name of the SSL policy.
                    returned: always
                    type: str
                    sample: ssl_policy20170401_s
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _camel_to_snake

try:
    from azure.core.exceptions import ResourceNotFoundError
    from msrestazure.tools import parse_resource_id
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMApplicationGatewayInfo(AzureRMModuleBase):

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

        super(AzureRMApplicationGatewayInfo, self).__init__(self.module_arg_spec,
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
            response = self.network_client.application_gateways.get(resource_group_name=self.resource_group, application_gateway_name=self.name)
        except ResourceNotFoundError:
            pass

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_rg(self):
        response = None
        results = []
        try:
            response = self.network_client.application_gateways.list(resource_group_name=self.resource_group)
        except Exception as exc:
            request_id = exc.request_id if exc.request_id else ''
            self.fail("Error listing application gateways in resource groups {0}: {1} - {2}".format(self.resource_group, request_id, str(exc)))

        for item in response:
            results.append(self.format_response(item))

        return results

    def list_all(self):
        response = None
        results = []
        try:
            response = self.network_client.application_gateways.list_all()
        except Exception as exc:
            request_id = exc.request_id if exc.request_id else ''
            self.fail("Error listing all application gateways: {0} - {1}".format(request_id, str(exc)))

        for item in response:
            results.append(self.format_response(item))

        return results

    def format_response(self, appgw):
        d = appgw.as_dict()
        id = d.get("id")
        id_dict = parse_resource_id(id)
        d = {
            "id": id,
            "name": d.get("name"),
            "resource_group": id_dict.get('resource_group', self.resource_group),
            "location": d.get("location"),
            "operational_state": d.get("operational_state"),
            "provisioning_state": d.get("provisioning_state"),
            "ssl_policy": None if d.get("ssl_policy") is None else {
                "policy_type": _camel_to_snake(d.get("ssl_policy").get("policy_type", None)),
                "policy_name": self.ssl_policy_name(d.get("ssl_policy").get("policy_name", None)),
            },
        }
        return d

    def ssl_policy_name(self, policy_name):
        if policy_name == "AppGwSslPolicy20150501":
            return "ssl_policy20150501"
        elif policy_name == "AppGwSslPolicy20170401":
            return "ssl_policy20170401"
        elif policy_name == "AppGwSslPolicy20170401S":
            return "ssl_policy20170401_s"
        return None


def main():
    AzureRMApplicationGatewayInfo()


if __name__ == '__main__':
    main()
