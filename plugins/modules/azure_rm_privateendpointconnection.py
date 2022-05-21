#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_privateendpointconnection

version_added: "1.12.0"

short_description: Managed private endpoint connection

description:
    - Update or delete the private endpoint connection.

options:
    name:
        description:
            - The name of the private end point connection.
        type: str
        required: True
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
    connection_state:
        description:
            - A collection of information about the state of the connection between service consumer and provider.
        type: dict
        suboptions:
            status:
                description:
                    - Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
                type: str
                choices:
                    - Approved
                    - Rejected
                    - Removed
            description:
                description:
                    - The reason for approval/rejection of the connection.
                type: str
            actions_required:
                description:
                    - A message indicating if changes on the service provider require any updates on the consumer.
                type: str
    state:
        description:
            - Assert the state of the connection. Use C(present) to update an connection and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Update private endpoint connection
  azure_rm_privateendpointconnection_info:
    name: pe-connection-name
    service_name: testserviceName
    resource_group: myRG
    connection_state:
      description: "new_description string"
      actions_required: "Message string"
      status: "Rejected"

- name: Delee private endpoint connection
  azure_rm_privateendpointconnection_info:
    name: pe-connection-name
    service_name: testserviceName
    resource_group: myRG
    state: absent
'''

RETURN = '''
state:
    description:
        - List of private endpoint connection info.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID of the private endpoint connection.
            returned: always
            type: str
            sample: "/subscriptions/xxx/resourceGroups/myRG/providers/Microsoft.Network/privateLinkServices/linkservice/privateEndpointConnections/link.09"
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
    from azure.core.polling import LROPoller
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


connection_state_spec = dict(
    status=dict(type='str', choices=['Approved', 'Rejected', 'Removed']),
    description=dict(type='str'),
    actions_required=dict(type='str')
)


class AzureRMPrivateEndpointConnection(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type="str", required=True),
            service_name=dict(type="str", required=True),
            resource_group=dict(type="str", required=True),
            connection_state=dict(type='dict', options=connection_state_spec),
            state=dict(type='str', choices=['present', 'absent'], default='present'),
        )

        self.name = None
        self.service_name = None
        self.resource_group = None
        self.connection_state = None
        self.results = dict(
            changed=False,
        )

        super(AzureRMPrivateEndpointConnection, self).__init__(self.module_arg_spec,
                                                               supports_check_mode=True,
                                                               supports_tags=False,
                                                               facts_module=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        old_response = self.get_resource()
        response = None
        changed = False

        if self.state == 'present':
            if old_response:
                if self.connection_state is not None:

                    if self.connection_state.get('status') is not None:
                        if self.connection_state.get('status') != old_response['private_link_service_connection_state']['status']:
                            changed = True
                    else:
                        self.connection_state['status'] = old_response['private_link_service_connection_state']['status']

                    if self.connection_state.get('description'):
                        if self.connection_state.get('description') != old_response['private_link_service_connection_state']['description']:
                            changed = True
                    else:
                        self.connection_state['description'] = old_response['private_link_service_connection_state']['description']
                    if self.connection_state.get('actions_required'):
                        if self.connection_state.get('actions_required') != old_response['private_link_service_connection_state']['actions_required']:
                            changed = True
                    else:
                        self.connection_state['actions_required'] = old_response['private_link_service_connection_state']['actions_required']

                if changed:
                    if self.check_mode:
                        self.log("The private endpoint connection is exist, will be updated")
                    else:
                        parameters = {'private_link_service_connection_state': self.connection_state}
                        response = self.update_resource(parameters)
                        if response:
                            response = self.connect_to_dict(response)
                else:
                    if self.check_mode:
                        self.log("Check mode test. The private endpoint connection is exist, No operation in this task")
                    else:
                        response = old_response
                        self.log("The private endpoint connection is exist, No operation in this task")
            else:
                if self.check_mode:
                    changed = True
                    self.log("The private endpoint conneection is not exist, will be created, but this module not support create funciont")
                else:
                    self.fail("The private endpoint connection {0} isn't exist, This Module not support create".format(self.name))
        else:
            if old_response:
                changed = True
                if self.check_mode:
                    self.log("The private endpoint conneection is exist, will be deleted")
                else:
                    self.delete_resource()
            else:
                if self.check_mode:
                    self.log("The private endpoint connection isn't exist, no action")
                else:
                    self.log("The private endpoint connection isn't exist, don't need to delete")

        self.results['changed'] = changed
        self.results['state'] = response
        return self.results

    def get_resource(self):
        self.log("Get properties for {0} in {1}".format(self.name, self.service_name))
        try:
            response = self.network_client.private_link_services.get_private_endpoint_connection(self.resource_group, self.service_name, self.name)
            return self.connect_to_dict(response)
        except ResourceNotFoundError:
            self.log("Could not get info for {0} in {1}".format(self.name, self.service_name))

        return []

    def update_resource(self, parameters):
        self.log("Update the private endpoint connection for {0} in {1}".format(self.name, self.service_name))
        try:
            response = self.network_client.private_link_services.update_private_endpoint_connection(self.resource_group,
                                                                                                    self.service_name,
                                                                                                    self.name, parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
            return response
        except Exception:
            self.log("Update {0} in {1} failed".format(self.name, self.service_name))

        return []

    def delete_resource(self):
        self.log("delete the private endpoint connection for {0} in {1}".format(self.name, self.service_name))
        try:
            response = self.network_client.private_link_services.begin_delete_private_endpoint_connection(self.resource_group, self.service_name, self.name)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
            return response
        except Exception:
            self.log("Delete {0} in {1} failed".format(self.name, self.service_name))

        return []

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
    AzureRMPrivateEndpointConnection()


if __name__ == "__main__":
    main()
