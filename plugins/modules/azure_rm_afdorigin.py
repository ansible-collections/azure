#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Python SDK Reference: https://learn.microsoft.com/en-us/python/api/azure-mgmt-cdn/azure.mgmt.cdn.operations.afdoriginsoperations?view=azure-python
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_afdorigin
version_added: "3.4.0"
short_description: Manage an Azure Front Door Origin to be used with Standard or Premium Frontdoor.
description:
    - Create, update and delete an Azure Front Door (AFD) Origin to be used by a Front Door Service Profile created using azure_rm_cdnprofile.

options:
    azure_origin:
        description:
            - Resource reference to the AFD origin resource.
        type: str
    enabled_state:
        description:
            - Whether to enable health probes to be made against backends defined under backend pools.
            - Health probes can only be disabled if there is a single enabled backend in single enabled backend pool.
        type: str
        choices:
            - Enabled
            - Disabled
    host_name:
        description:
            - The address of the origin. Domain names, IPv4 addresses, and IPv6 addresses are supported.
            - This should be unique across all origins in an endpoint.
        type: str
    http_port:
        description:
            - The value of the HTTP port. Must be between 1 and 65535.
        default: 80
        type: int
    https_port:
        description:
            - The value of the HTTPS port. Must be between 1 and 65535.
        default: 443
        type: int
    name:
        description:
            - Name of the origin that is unique within the AFD Profile.
        required: true
        type: str
    origin_host_header:
        description:
            - The host header value sent to the origin with each request. If you leave this blank, the request hostname determines this value.
            - Azure Front Door origins, such as Web Apps, Blob Storage,
            - and Cloud Services require this host header value to match the origin hostname by default.
            - This overrides the host header defined at the AFD Endpoint.
        type: str
    origin_group_name:
        description:
            - Name of the origin group which is unique within the profile.
        required: true
        type: str
    priority:
        description:
            - Priority of origin in given origin group for load balancing.
            - Higher priorities will not be used for load balancing if any lower priority origin is healthy. Must be between 1 and 5.
        type: int
    profile_name:
        description:
            - Name of the AFD Profile.
        required: true
        type: str
    resource_group:
        description:
            - Name of a resource group where the AFD Origin exists or will be created.
        required: true
        type: str
    shared_private_link_resource:
        description:
            - The properties of the private link resource for private origin.
        type: dict
        suboptions:
            group_id:
                description:
                    - The group id from the provider of resource the shared private link resource is for.
                type: str
            private_link:
                description:
                    - The resource id of the resource the shared private link resource is for.
                type: str
            private_link_location:
                description:
                    - The location of the shared private link resource.
                type: str
            request_message:
                description:
                    - The request message for requesting approval of the shared private link resource.
                type: str
            status:
                description:
                    - Status of the shared private link resource. Can be Pending, Approved, Rejected, Disconnected, or Timeout.
                type: str
                default: Approved
                choices:
                    - Approved
                    - Disconnected
                    - Pending
                    - Rejected
                    - Timeout
    state:
        description:
            - Assert the state of the AFD Profile. Use C(present) to create or update an AFD profile and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present
    weight:
        description:
            - Weight of the origin in given origin group for load balancing. Must be between 1 and 1000.
        type: int

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Jarret Tooley (@jartoo)
'''

EXAMPLES = '''
- name: Create an AFD Origin
  azure_rm_afdorigin:
    name: myOrigin
    origin_group_name: myOriginGroup
    profile_name: myProfile
    resource_group: myResourceGroup
    state: present
    host_name: "10.0.0.1"
    origin_host_header: "10.0.0.1"
    http_port: 80
    https_port: 443
    priority: 1
    weight: 1000

- name: Delete an AFD Origin
  azure_rm_afdorigin:
    name: myOrigin
    origin_group_name: myOriginGroup
    profile_name: myProfile
    resource_group: myResourceGroup
    state: absent
'''
RETURN = '''
id:
    description:
        - ID of the AFD Origin.
    returned: always
    type: str
    sample: "id: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx/resourcegroups/myRG/providers/Microsoft.Cdn/profiles/myProf/origingroups/myOG/origins/myO"
host_name:
    description:
        - Host name of the AFD Origin.
    returned: always
    type: str
    sample: "myorigin.azurefd.net"

'''
import re
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


try:
    from azure.mgmt.cdn.models import AFDOrigin, AFDOriginUpdateParameters, SharedPrivateLinkResourceProperties, ResourceReference
except ImportError as ec:
    # This is handled in azure_rm_common
    pass


def origin_to_dict(origin):
    ''' Convert object to dict '''
    return dict(
        azure_origin=origin.azure_origin,
        deployment_status=origin.deployment_status,
        enabled_state=origin.enabled_state,
        # enforce_certificate_check = origin.enforce_certificate_check, # Not fully implemented yet
        host_name=origin.host_name,
        http_port=origin.http_port,
        https_port=origin.https_port,
        id=origin.id,
        name=origin.name,
        origin_group_name=re.sub('\\/.*', '', re.sub('.*origingroups\\/', '', origin.id)),
        origin_host_header=origin.origin_host_header,
        priority=origin.priority,
        provisioning_state=origin.provisioning_state,
        shared_private_link_resource=origin.shared_private_link_resource,
        type=origin.type,
        weight=origin.weight
    )


class AzureRMOrigin(AzureRMModuleBase):
    ''' Class for managing Origin '''
    def __init__(self):
        self.module_arg_spec = dict(
            azure_origin=dict(type='str'),
            enabled_state=dict(type='str', choices=['Enabled', 'Disabled']),
            # enforce_certification_name_check=dict(type='bool'),
            host_name=dict(type='str'),
            http_port=dict(type='int', default=80),
            https_port=dict(type='int', default=443),
            name=dict(
                type='str',
                required=True
            ),
            origin_group_name=dict(
                type='str',
                required=True
            ),
            origin_host_header=dict(type='str'),
            priority=dict(type='int'),
            profile_name=dict(
                type='str',
                required=True
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            shared_private_link_resource=dict(
                type='dict',
                options=dict(
                    group_id=dict(type='str'),
                    private_link=dict(type='str'),
                    private_link_location=dict(type='str'),
                    request_message=dict(type='str'),
                    status=dict(
                        type='str',
                        default='Approved',
                        choices=[
                            "Pending",
                            "Approved",
                            "Rejected",
                            "Disconnected",
                            "Timeout"
                        ]
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            weight=dict(type='int')
        )

        self.azure_origin = None
        self.enabled_state = None
        self.host_name = None
        self.http_port = None
        self.https_port = None
        self.origin_host_header = None
        self.priority = None
        self.shared_private_link_resource = None
        self.weight = None

        self.name = None
        self.origin_group_name = None
        self.profile_name = None
        self.resource_group = None
        self.state = None

        self.results = dict(changed=False)

        super(AzureRMOrigin, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        to_be_updated = False

        response = self.get_origin()

        if self.state == 'present':

            if not response:
                self.log("Need to create the Origin")

                if not self.check_mode:
                    new_response = self.create_origin()
                    self.results['id'] = new_response['id']
                    self.results['host_name'] = new_response['host_name']

                self.results['changed'] = True

            else:
                self.log('Results : {0}'.format(response))
                self.results['id'] = response['id']
                self.results['host_name'] = response['host_name']

                if response['host_name'] != self.host_name and self.host_name:
                    to_be_updated = True
                if response['http_port'] != self.http_port and self.http_port:
                    to_be_updated = True
                if response['https_port'] != self.https_port and self.https_port:
                    to_be_updated = True
                if response['origin_host_header'] != self.origin_host_header and self.origin_host_header:
                    to_be_updated = True
                if response['priority'] != self.priority and self.priority:
                    to_be_updated = True
                if response['weight'] != self.weight and self.weight:
                    to_be_updated = True
                if response['enabled_state'] != self.enabled_state and self.enabled_state:
                    to_be_updated = True
                if response['shared_private_link_resource'] != self.shared_private_link_resource and self.shared_private_link_resource:
                    to_be_updated = True
                elif response['shared_private_link_resource']:
                    if response['shared_private_link_resource']['group_id'] != \
                            self.shared_private_link_resource.get('group_id') and \
                            self.shared_private_link_resource.get('group_id'):
                        to_be_updated = True
                    if response['shared_private_link_resource']['private_link'] != \
                            self.shared_private_link_resource.get('private_link') and \
                            self.shared_private_link_resource.get('private_link'):
                        to_be_updated = True
                    if response['shared_private_link_resource']['private_link_location'] != \
                            self.shared_private_link_resource.get('private_link_location') and \
                            self.shared_private_link_resource.get('private_link_location'):
                        to_be_updated = True
                    if response['shared_private_link_resource']['request_message'] != self.origin['shared_private_link_resource']['request_message'] and \
                            self.shared_private_link_resource.get('request_message'):
                        to_be_updated = True
                    if response['shared_private_link_resource']['status'] != self.shared_private_link_resource.get('status') and \
                            self.shared_private_link_resource.get('status'):
                        to_be_updated = True

                if to_be_updated:
                    self.log("Need to update the Origin")

                    if not self.check_mode:
                        new_response = self.update_origin()
                        self.results['id'] = new_response['id']
                        self.results['host_name'] = new_response['host_name']

                    self.results['changed'] = True

        elif self.state == 'absent':
            if not response:
                self.log("Origin {0} does not exist.".format(self.name))
                self.results['id'] = ""
                self.results['host_name'] = ""
            else:
                self.log("Need to delete the Origin")
                self.results['changed'] = True
                self.results['id'] = response['id']
                self.results['host_name'] = response['host_name']

                if not self.check_mode:
                    self.delete_origin()

        return self.results

    def create_origin(self):
        '''
        Creates a Azure Origin.

        :return: deserialized Azure Origin instance state dictionary
        '''
        self.log("Creating the Azure Origin instance {0}".format(self.name))

        shared_private_link_resource = None
        if self.shared_private_link_resource:
            shared_private_link_resource = SharedPrivateLinkResourceProperties(
                group_id=self.shared_private_link_resource.get('group_id'),
                private_link=ResourceReference(id=self.shared_private_link_resource.get('private_link')),
                private_link_location=self.shared_private_link_resource.get('private_link_location'),
                request_message=self.shared_private_link_resource.get('request_message'),
                status=self.shared_private_link_resource.get('status')
            )

        parameters = AFDOrigin(
            azure_origin=self.azure_origin,
            host_name=self.host_name,
            http_port=self.http_port,
            https_port=self.https_port,
            origin_host_header=self.origin_host_header,
            priority=self.priority,
            weight=self.weight,
            enabled_state=self.enabled_state,
            shared_private_link_resource=shared_private_link_resource
        )

        try:
            poller = self.cdn_client.afd_origins.begin_create(resource_group_name=self.resource_group,
                                                              profile_name=self.profile_name,
                                                              origin_group_name=self.origin_group_name,
                                                              origin_name=self.name,
                                                              origin=parameters)
            response = self.get_poller_result(poller)
            return origin_to_dict(response)
        except Exception as exc:
            self.log('Error attempting to create Azure Origin instance.')
            self.fail("Error Creating Azure Origin instance: {0}".format(str(exc)))

    def update_origin(self):
        '''
        Updates an Azure Origin.

        :return: deserialized Azure Origin instance state dictionary
        '''
        self.log("Updating the Azure Origin instance {0}".format(self.name))

        shared_private_link_resource = None
        if self.shared_private_link_resource:
            shared_private_link_resource = SharedPrivateLinkResourceProperties(
                group_id=self.shared_private_link_resource.get('group_id'),
                private_link=ResourceReference(id=self.shared_private_link_resource.get('private_link')),
                private_link_location=self.shared_private_link_resource.get('private_link_location'),
                request_message=self.shared_private_link_resource.get('request_message'),
                status=self.shared_private_link_resource.get('status')
            )

        parameters = AFDOriginUpdateParameters(
            azure_origin=self.azure_origin,
            host_name=self.host_name,
            http_port=self.http_port,
            https_port=self.https_port,
            origin_host_header=self.origin_host_header,
            priority=self.priority,
            weight=self.weight,
            enabled_state=self.enabled_state,
            shared_private_link_resource=shared_private_link_resource
        )

        try:
            poller = self.cdn_client.afd_origins.begin_update(resource_group_name=self.resource_group,
                                                              profile_name=self.profile_name,
                                                              origin_group_name=self.origin_group_name,
                                                              origin_name=self.name,
                                                              origin_update_properties=parameters)
            response = self.get_poller_result(poller)
            return origin_to_dict(response)
        except Exception as exc:
            self.log('Error attempting to update Azure Origin instance.')
            self.fail("Error updating Azure Origin instance: {0}".format(str(exc)))

    def delete_origin(self):
        '''
        Deletes the specified Azure Origin in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Origin {0}".format(self.name))
        try:
            poller = self.cdn_client.afd_origins.begin_delete(resource_group_name=self.resource_group,
                                                              profile_name=self.profile_name,
                                                              origin_group_name=self.origin_group_name,
                                                              origin_name=self.name)
            self.get_poller_result(poller)
            return True
        except Exception as exc:
            self.log('Error attempting to delete the Origin.')
            self.fail("Error deleting the Origin: {0}".format(str(exc)))
            return False

    def get_origin(self):
        '''
        Gets the properties of the specified Origin.

        :return: deserialized Origin state dictionary
        '''
        self.log(
            "Checking if the Origin {0} is present".format(self.name))
        try:
            response = self.cdn_client.afd_origins.get(resource_group_name=self.resource_group,
                                                       profile_name=self.profile_name,
                                                       origin_group_name=self.origin_group_name,
                                                       origin_name=self.name)
            self.log("Response : {0}".format(response))
            self.log("Origin : {0} found".format(response.name))
            return origin_to_dict(response)
        except Exception as exc:
            self.log('Did not find the Origin. {0}'.format(str(exc)))
            return False


def main():
    """Main execution"""
    AzureRMOrigin()


if __name__ == '__main__':
    main()
