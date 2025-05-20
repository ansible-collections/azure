#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Python SDK Reference: https://learn.microsoft.com/en-us/python/api/azure-mgmt-cdn/azure.mgmt.cdn.operations.afdoriginsoperations?view=azure-python
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_afdorigin_info
version_added: "3.4.0"
short_description: Get Azure Front Door Origin facts to be used with Standard or Premium Frontdoor Service
description:
    - Get facts for a specific Azure Front Door (AFD) Origin or all AFD Origins.
    - This differs from the Front Door classic service and only is intended to be used by the Standard or Premium service offering.

options:
    resource_group:
        description:
            - Name of the resource group where this AFD Profile belongs.
        required: true
        type: str
    origin_group_name:
        description:
            - Name of the origin group which is unique within the profile.
        required: true
        type: str
    profile_name:
        description:
            - Name of the AFD profile.
        required: true
        type: str
    name:
        description:
            - Limit results to a specific AFD Origin.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Jarret Tooley (@jartoo)
'''

EXAMPLES = '''
- name: Get facts for all Origins in AFD Profile
  azure_rm_afdorigin_info:
    resource_group: myResourceGroup
    profile_name: myCDNProfile

- name: Get facts of specific AFD Origin
  azure_rm_afdorigin_info:
    name: myOrigin1
    profile_name: myCDNProfile
    resource_group: myResourceGroup
'''

RETURN = '''
afdorigins:
    description: List of AFD Origins.
    returned: always
    type: complex
    contains:
        azure_origin:
            description:
                - Resource reference to the AFD origin resource.
            type: str
        deployment_status:
            description:
                - Current state of the resource.
            type: str
            sample: NotStarted
        enabled_state:
            description:
                - Whether to enable health probes to be made against backends defined under backend pools.
                - Health probes can only be disabled if there is a single enabled backend in single enabled backend pool.
            type: str
            sample: Enabled
        host_name:
            description:
                - The address of the origin. Domain names, IPv4 addresses, and IPv6 addresses are supported.
                - This should be unique across all origins in an endpoint.
            type: str
        http_port:
            description:
                - The value of the HTTP port. Must be between 1 and 65535.
            type: int
            sample: 80
        https_port:
            description:
                - The value of the HTTPS port. Must be between 1 and 65535.
            type: int
            sample: 443
        id:
            description:
                - ID of the AFD Origin.
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxx/resourcegroups/myRG/providers/Microsoft.Cdn/profiles/myProf/origingroups/myOG/origins/myO"
        name:
            description:
                - Name of the AFD Origin.
            type: str
        origin_group_name:
            description:
                - Name of the origin group which is unique within the profile.
            type: str
        origin_host_header:
            description:
                - The host header value sent to the origin with each request. If you leave this blank, the request hostname determines this value.
                - Azure Front Door origins, such as Web Apps, Blob Storage, and Cloud Services require this host header value to match the origin
                - hostname by default. This overrides the host header defined at the AFD Endpoint.
            type: str
        priority:
            description:
                - Priority of origin in given origin group for load balancing. Higher priorities will not be used for load balancing if any
                - lower priority origin is healthy. Must be between 1 and 5.
            type: int
        profile_name:
            description:
                - Name of the AFD Profile where the Origin will be added.
            type: str
        provisioning_state:
            description:
                - Provisioning status of the AFD Origin.
            type: str
            sample: Succeeded
        resource_group:
            description:
                - Name of a resource group where the AFD Origin exists or will be created.
            type: str
        shared_private_link_resource:
            description:
                - The properties of the private link resource for private origin.
            type: dict
            contains:
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
                    sample: Approved
        type:
            description:
                - Resource type.
            type: str
            sample: Microsoft.Cdn/profiles/origingroups/origins
        weight:
            description:
                - Weight of the origin in given origin group for load balancing. Must be between 1 and 1000.
            type: int
'''

import re
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


AZURE_OBJECT_CLASS = 'AFDOrigin'


class AzureRMAFDOriginInfo(AzureRMModuleBase):
    """Utility class to get Azure AFD Origin facts"""

    def __init__(self):

        self.module_args = dict(
            name=dict(type='str'),
            origin_group_name=dict(
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
            )
        )

        self.results = dict(
            changed=False,
            afdorigins=[]
        )

        self.name = None
        self.origin_group_name = None
        self.resource_group = None
        self.profile_name = None

        super(AzureRMAFDOriginInfo, self).__init__(
            supports_check_mode=True,
            derived_arg_spec=self.module_args,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):

        for key in self.module_args:
            setattr(self, key, kwargs[key])

        if self.name:
            self.results['afdorigins'] = self.get_item()
        else:
            self.results['afdorigins'] = self.list_by_profile()

        return self.results

    def get_item(self):
        """Get a single Azure AFD Origin"""

        self.log('Get properties for {0}'.format(self.name))

        item = None
        result = []

        try:
            item = self.cdn_client.afd_origins.get(resource_group_name=self.resource_group,
                                                   profile_name=self.profile_name,
                                                   origin_group_name=self.origin_group_name,
                                                   origin_name=self.name)
        except Exception as exc:
            self.log("Did not find resource. {0}".format(str(exc)))

        if item:
            result = [self.serialize_afdorigin(item)]

        return result

    def list_by_profile(self):
        """Get all Azure AFD Origins within an AFD profile"""

        self.log('List all AFD Origins within an AFD profile')

        try:
            response = self.cdn_client.afd_origins.list_by_origin_group(resource_group_name=self.resource_group,
                                                                        profile_name=self.profile_name,
                                                                        origin_group_name=self.origin_group_name)
        except Exception as exc:
            self.fail('Failed to list all origins. {0}'.format(str(exc)))

        results = []
        for item in response:
            results.append(self.serialize_afdorigin(item))

        return results

    def serialize_afdorigin(self, afdorigin):
        '''
        Convert a AFD Origin object to dict.
        :param afdorigin: AFD Origin object
        :return: dict
        '''
        result = self.serialize_obj(afdorigin, AZURE_OBJECT_CLASS)

        new_result = {}
        new_result['azure_origin'] = afdorigin.azure_origin
        new_result['deployment_status'] = afdorigin.deployment_status
        new_result['enabled_state'] = afdorigin.enabled_state
        new_result['host_name'] = afdorigin.host_name
        new_result['http_port'] = afdorigin.http_port
        new_result['https_port'] = afdorigin.https_port
        new_result['https_port'] = afdorigin.https_port
        new_result['id'] = afdorigin.id
        new_result['name'] = afdorigin.name
        new_result['origin_group_name'] = re.sub('\\/.*', '', re.sub('.*origingroups\\/', '', result['id']))
        new_result['origin_host_header'] = afdorigin.origin_host_header
        new_result['priority'] = afdorigin.priority
        new_result['provisioning_state'] = afdorigin.provisioning_state
        new_result['priority'] = afdorigin.priority
        new_result['profile_name'] = re.sub('\\/.*', '', re.sub('.*profiles\\/', '', result['id']))
        new_result['resource_group'] = re.sub('\\/.*', '', re.sub('.*resourcegroups\\/', '', result['id']))
        new_result['shared_private_link_resource'] = dict()
        if afdorigin.shared_private_link_resource:
            new_result['shared_private_link_resource']['group_id'] = afdorigin.shared_private_link_resource.group_id
            new_result['shared_private_link_resource']['private_link'] = afdorigin.shared_private_link_resource.private_link
            new_result['shared_private_link_resource']['private_link_location'] = afdorigin.shared_private_link_resource.private_link_location
            new_result['shared_private_link_resource']['request_message'] = afdorigin.shared_private_link_resource.request_message
            new_result['shared_private_link_resource']['status'] = afdorigin.shared_private_link_resource.status
        else:
            new_result['shared_private_link_resource']['group_id'] = None
            new_result['shared_private_link_resource']['private_link'] = None
            new_result['shared_private_link_resource']['private_link_location'] = None
            new_result['shared_private_link_resource']['request_message'] = None
            new_result['shared_private_link_resource']['status'] = None
        new_result['type'] = afdorigin.type
        new_result['weight'] = afdorigin.weight
        return new_result


def main():
    """Main module execution code path"""
    AzureRMAFDOriginInfo()


if __name__ == '__main__':
    main()
