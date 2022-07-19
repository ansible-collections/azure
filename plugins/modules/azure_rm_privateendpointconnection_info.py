#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_privateendpointconnection_info

version_added: "1.12.0"

short_description: Get private endpoint connection info

description:
    - Get facts for private endpoint connection info.

options:
    name:
        description:
            - The name of the private end point connection.
        type: str
    service_name:
        description:
            - The name of the private link service.
        type: str
        required: true
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: true

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get private endpoint connection info by name
  azure_rm_privateendpointconnection_info:
    name: pe-connection-name
    service_name: testserviceName
    resource_group: myRG

- name: Get all private endpoint connection info by service name
  azure_rm_privateendpointconnection_info:
    service_name: testserviceName
    resource_group: myRG
'''

RETURN = '''
endpoint_connection:
    description:
        - List of private endpoint connection info.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID of the private endpoint connection.
            sample: "/subscriptions/xxx/resourceGroups/myRG/providers/Microsoft.Network/privateLinkServices/linkservice/privateEndpointConnections/link.09"
            returned: always
            type: str
        name:
            description:
                - Name of the private endpoint connection.
            returned: always
            type: str
            sample: testlink.09
        link_identifier:
            description:
                - The consumer link id.
            returned: always
            type: str
            sample: 536890208
        PrivateEndpoint:
            description:
                - The resource of private end point.
            type: complex
            returned: always
            contains:
                id:
                    description:
                        - The private endpoint resource ID.
                    type: str
                    returned: always
                    sample: "/subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Network/privateEndpoints/testlink02"
        private_link_service_connection_state:
            description:
                - A collection of information about the state of the connection between service consumer and provider.
            type: complex
            returned: always
            contains:
                description:
                    description:
                        - The reason for approval/rejection of the connection.
                    returned: always
                    type: str
                    sample: "Auto Approved"
                status:
                    description:
                        - Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
                    returned: always
                    type: str
                    sample: Approved
                actions_required:
                    description:
                        - A message indicating if changes on the service provider require any updates on the consumer.
                    type: str
                    returned: always
                    sample: "This is action_required string"
        provisioning_state:
            description:
                - Provisioning state of the resource.
            returned: always
            type: str
            sample: Succeeded
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
            sample: Microsoft.Network/privateLinkServices/privateEndpointConnections
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMPrivateEndpointConnectionInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type="str"),
            service_name=dict(type="str", required=True),
            resource_group=dict(type="str", required=True),
        )

        self.name = None
        self.service_name = None
        self.resource_group = None
        self.results = dict(
            changed=False,
        )

        super(AzureRMPrivateEndpointConnectionInfo, self).__init__(self.module_arg_spec,
                                                                   supports_check_mode=True,
                                                                   supports_tags=False,
                                                                   facts_module=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results["endpoint_connection"] = self.get_item()
        else:
            self.results["endpoint_connection"] = self.list_items()

        return self.results

    def get_item(self):
        self.log("Get properties for {0} in {1}".format(self.name, self.service_name))

        try:
            response = self.network_client.private_link_services.get_private_endpoint_connection(self.resource_group, self.service_name, self.name)
            return [self.connect_to_dict(response)]
        except ResourceNotFoundError:
            self.log("Could not get info for {0} in {1}".format(self.name, self.service_name))

        return []

    def list_items(self):
        result = []
        self.log("List all in {0}".format(self.service_name))
        try:
            response = self.network_client.private_link_services.list_private_endpoint_connections(self.resource_group, self.service_name)
            while True:
                result.append(response.next())
        except StopIteration:
            pass
        except Exception as exc:
            self.fail("Failed to list all items in {0}: {1}".format(self.service_name, str(exc)))
        return [self.connect_to_dict(item) for item in result]

    def connect_to_dict(self, connect_info):
        connect = connect_info.as_dict()
        result = dict(
            id=connect.get("id"),
            name=connect.get('name'),
            type=connect.get('type'),
            etag=connect.get('etag'),
            private_endpoint=dict(),
            private_link_service_connection_state=dict(),
            provisioning_state=connect.get('provisioning_state'),
            link_identifier=connect.get('link_identifier')
        )
        if connect.get('private_endpoint') is not None:
            result['private_endpoint']['id'] = connect.get('private_endpoint')['id']

        if connect.get('private_link_service_connection_state') is not None:
            result['private_link_service_connection_state']['status'] = connect.get('private_link_service_connection_state')['status']
            result['private_link_service_connection_state']['description'] = connect.get('private_link_service_connection_state')['description']
            result['private_link_service_connection_state']['actions_required'] = connect.get('private_link_service_connection_state')['actions_required']
        return result


def main():
    AzureRMPrivateEndpointConnectionInfo()


if __name__ == "__main__":
    main()
