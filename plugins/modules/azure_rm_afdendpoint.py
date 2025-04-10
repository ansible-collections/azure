#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Python SDK Reference: https://learn.microsoft.com/en-us/python/api/azure-mgmt-cdn/azure.mgmt.cdn.operations.afdendpointsoperations?view=azure-python
#
# TODO: Name check the URL
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_afdendpoint
version_added: "2.7.0"
short_description: Manage an Azure Front Door Endpoint to be used with Standard or Premium Frontdoor
description:
    - Create, update and delete an Azure Front Door (AFD) Endpoint to be used by a Front Door Service Profile created using azure_rm_cdnprofile.
    - This differs from the Front Door classic service and only is intended to be used by the Standard or Premium service offering.

options:
    auto_generated_domain_name_label_scope:
        description:
            - Indicates the endpoint name reuse scope. Cannot be used to update an existing Endpoint at this time.
        default: TenantReuse
        type: str
        choices:
            - TenantReuse
            - SubscriptionReuse
            - ResourceGroupReuse
            - NoReuse
    enabled_state:
        description:
            - Whether to enable use of this rule.
        default: Enabled
        type: str
        choices:
            - Enabled
            - Disabled
    location:
        description:
            - Valid Azure location. Defaults to location of the resource group. Cannot be used to update an existing Endpoint at this time.
        type: str
    name:
        description:
            - Name of the AFD Endpoint.
        required: True
        type: str
    profile_name:
        description:
            - Name of the AFD Profile where the Endpoint will be attached to.
        required: True
        type: str
    resource_group:
        description:
            - Name of a resource group where the Azure Front Door Endpoint exists or will be created.
        required: True
        type: str
    state:
        description:
            - Assert the state of the AFD Endpoint. Use C(present) to create or update an AFD Endpoint and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Jarret Tooley (@jartoo)
'''

EXAMPLES = '''
- name: Create an AFD Endpoint
  azure_rm_afdendpoint:
    name: myEndpoint
    profile_name: myProfile
    resource_group: myResourceGroup
    state: present
    tags:
      testing: testing

- name: Delete the AFD Endpoint
  azure_rm_afdendpoint:
    name: myEndPoint
    profile_name: myProfile
    resource_group: myResourceGroup
    state: absent
'''
RETURN = '''
id:
    description:
        - ID of the AFD Endpoint.
    returned: always
    type: str
    sample: "id: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/
    myResourceGroup/providers/Microsoft.Cdn/profiles/myProfile/endpoints/myEndpoint"
host_name:
    description:
        - Host name of the AFD Endpoint.
    returned: always
    type: str
    sample: "myendpoint.azurefd.net"

'''
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.mgmt.cdn.models import AFDEndpoint, AFDEndpointUpdateParameters
except ImportError as ec:
    # This is handled in azure_rm_common
    pass


def endpoint_to_dict(endpoint):
    return dict(
        deployment_status=endpoint.deployment_status,
        enabled_state=endpoint.enabled_state,
        host_name=endpoint.host_name,
        id=endpoint.id,
        location=endpoint.location,
        name=endpoint.name,
        provisioning_state=endpoint.provisioning_state,
        tags=endpoint.tags,
        type=endpoint.type
    )


class AzureRMEndpoint(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            auto_generated_domain_name_label_scope=dict(
                type='str',
                default='TenantReuse',
                choices=["TenantReuse", "SubscriptionReuse", "ResourceGroupReuse", "NoReuse"]
            ),
            enabled_state=dict(
                type='str',
                default='Enabled',
                choices=['Enabled', 'Disabled']
            ),
            location=dict(
                type='str'
            ),
            name=dict(
                type='str',
                required=True
            ),
            profile_name=dict(
                type='str',
                required=True
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.auto_generated_domain_name_label_scope = None
        self.enabled_state = None
        self.location = None
        self.tags = None

        self.name = None
        self.profile_name = None
        self.resource_group = None
        self.state = None

        self.results = dict(changed=False)

        super(AzureRMEndpoint, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        to_be_updated = False

        if not self.location:
            resource_group = self.get_resource_group(self.resource_group)
            self.location = resource_group.location

        response = self.get_endpoint()

        if self.state == 'present':

            if not response:
                self.log("Need to create the AFD Endpoint")

                if not self.check_mode:
                    new_response = self.create_endpoint()
                    self.results['id'] = new_response['id']
                    self.results['host_name'] = new_response['host_name']
                    self.log("AFD Endpoint creation done")

                self.results['changed'] = True
                return self.results

            else:
                self.log('Results : {0}'.format(response))
                self.results['id'] = response['id']
                self.results['host_name'] = response['host_name']

                update_tags, self.tags = self.update_tags(response['tags'])

                if update_tags:
                    to_be_updated = True

                if response['provisioning_state'] == "Succeeded":
                    if response['enabled_state'] != self.enabled_state:
                        to_be_updated = True

                    if self.location.lower() != response['location'].lower() and self.location:
                        # Location is not currently implemented in begin_update()
                        self.log("AFD Endpoint locations changes are not idempotent, please delete and recreate the Endpoint.")

                    if to_be_updated:
                        self.log("Need to update the AFD Endpoint")
                        self.results['changed'] = True

                        if not self.check_mode:
                            result = self.update_endpoint()
                            self.results['host_name'] = result['host_name']
                            self.log("AFD Endpoint update done")

        elif self.state == 'absent':
            if not response:
                self.log("AFD Endpoint {0} does not exist.".format(self.name))
                self.results['id'] = ""
            else:
                self.log("Need to delete the AFD Endpoint")
                self.results['changed'] = True
                self.results['id'] = response['id']

                if not self.check_mode:
                    self.delete_endpoint()
                    self.log("Azure AFD Endpoint deleted")

        return self.results

    def create_endpoint(self):
        '''
        Creates an AFD Endpoint.

        :return: deserialized AFD Endpoint instance state dictionary
        '''
        self.log("Creating the AFD Endpoint instance {0}".format(self.name))

        parameters = AFDEndpoint(
            auto_generated_domain_name_label_scope=self.auto_generated_domain_name_label_scope,
            enabled_state=self.enabled_state,
            location=self.location,
            tags=self.tags
        )

        try:
            poller = self.cdn_client.afd_endpoints.begin_create(
                endpoint_name=self.name,
                profile_name=self.profile_name,
                resource_group_name=self.resource_group,
                endpoint=parameters)
            response = self.get_poller_result(poller)
            return endpoint_to_dict(response)
        except Exception as exc:
            self.log('Error attempting to create AFD Endpoint instance.')
            self.fail("Error Creating AFD Endpoint instance: {0}".format(str(exc)))

    def update_endpoint(self):
        '''
        Updates an AFD Endpoint.

        :return: deserialized AFD Endpoint instance state dictionary
        '''
        self.log("Updating the AFD Endpoint instance {0}".format(self.name))

        parameters = AFDEndpointUpdateParameters(
            tags=self.tags,
            enabled_state=self.enabled_state
        )
        try:
            poller = self.cdn_client.afd_endpoints.begin_update(
                endpoint_name=self.name,
                profile_name=self.profile_name,
                resource_group_name=self.resource_group,
                endpoint_update_properties=parameters)
            response = self.get_poller_result(poller)
            return endpoint_to_dict(response)
        except Exception as exc:
            self.log('Error attempting to update AFD Endpoint instance.')
            self.fail("Error updating AFD Endpoint instance: {0}".format(str(exc)))

    def delete_endpoint(self):
        '''
        Deletes the specified AFD Endpoint in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the AFD Endpoint {0}".format(self.name))
        try:
            poller = self.cdn_client.afd_endpoints.begin_delete(
                resource_group_name=self.resource_group, profile_name=self.profile_name, endpoint_name=self.name)
            self.get_poller_result(poller)
            return True
        except Exception as exc:
            self.log('Error attempting to delete the AFD Endpoint.')
            self.fail("Error deleting the AFD Endpoint: {0}".format(str(exc)))
            return False

    def get_endpoint(self):
        '''
        Gets the properties of the specified AFD Endpoint.

        :return: deserialized AFD Endpoint state dictionary
        '''
        self.log(
            "Checking if the AFD Endpoint {0} is present".format(self.name))
        try:
            response = self.cdn_client.afd_endpoints.get(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                endpoint_name=self.name)
            self.log("Response : {0}".format(response))
            self.log("AFD Endpoint : {0} found".format(response.name))
            return endpoint_to_dict(response)
        except Exception as err:
            self.log('Did not find the AFD Endpoint.')
            return False


def main():
    """Main execution"""
    AzureRMEndpoint()


if __name__ == '__main__':
    main()
