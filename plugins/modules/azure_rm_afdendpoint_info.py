#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Python SDK Reference: https://learn.microsoft.com/en-us/python/api/azure-mgmt-cdn/azure.mgmt.cdn.operations.afdendpointsoperations?view=azure-python

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_afdendpoint_info
version_added: "2.7.0"
short_description: Get Azure Front Door Endpoint facts to be used with Standard or Premium Frontdoor Service
description:
    - Get facts for a specific Azure Front Door (AFD) Endpoint or all AFD Endpoints.
    - This differs from the Front Door classic service and only is intended to be used by the Standard or Premium service offering.

options:
    resource_group:
        description:
            - Name of the resource group where this AFD Profile belongs.
        required: true
        type: str
    profile_name:
        description:
            - Name of the AFD profile.
        required: true
        type: str
    name:
        description:
            - Limit results to a specific AFD Endpoint.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Jarret Tooley (@jartoo)
'''

EXAMPLES = '''
- name: Get facts for all Endpoints in AFD Profile
  azure_rm_afdendpoint_info:
    resource_group: myResourceGroup
    profile_name: myCDNProfile
    tags:
      - key
      - key:value

- name: Get facts of specific AFD Endpoint
  azure_rm_afdendpoint_info:
    resource_group: myResourceGroup
    profile_name: myCDNProfile
    name: myEndpoint1
'''

RETURN = '''
afdendpoints:
    description: List of AFD Endpoints.
    returned: always
    type: complex
    contains:
        auto_generated_domain_name_label_scope:
            description:
                - Indicates the endpoint name reuse scope.
            type: str
            sample: TenantReuse
        deployment_status:
            description:
                - Current state of the resource.
            type: str
            sample: NotStarted
        enabled_state:
            description:
                - Whether to enable use of this rule.
            type: str
            sample: Enabled
        host_name:
            description:
                - The host name of the AFD Endpoint structured as endpointName.DNSZone.
            type: str
            sample: contoso.azureedge.net
        id:
            description:
                - ID of the AFD Endpoint.
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/myCDN/providers/Microsoft.Cdn/profiles/myProf/endpoints/myEndpoint1"
        location:
            description:
                - Location of the AFD Endpoint.
            type: str
            sample: Global
        name:
            description:
                - Name of the AFD Endpoint.
            returned: always
            type: str
            sample: myEndpoint
        profile_name:
            description:
                - Name of the AFD Profile which holds the Endpoint.
            returned: always
            type: str
            sample: myProfile
        provisioning_state:
            description:
                - Provisioning status of the AFD Endpoint.
            type: str
            sample: Succeeded
        resource_group:
            description:
                - Name of a resource group where the AFD Endpoint exists.
            returned: always
            type: str
            sample: myResourceGroup
        tags:
            description:
                - The tags of the AFD Endpoint.
            type: list
            sample: foo
        type:
            description:
                - Resource type.
            type: str
            sample: Microsoft.Cdn/profiles/afdendpoints
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
import re

AZURE_OBJECT_CLASS = 'AFDEndpoint'


class AzureRMAFDEndpointInfo(AzureRMModuleBase):
    """Utility class to get Azure AFD Endpoint facts"""

    def __init__(self):

        self.module_args = dict(
            name=dict(type='str'),
            resource_group=dict(
                type='str',
                required=True
            ),
            profile_name=dict(
                type='str',
                required=True
            ),
            tags=dict(
                type='list',
                elements='str'
            )
        )

        self.results = dict(
            changed=False,
            afdendpoints=[]
        )

        self.name = None
        self.resource_group = None
        self.profile_name = None
        self.tags = None

        super(AzureRMAFDEndpointInfo, self).__init__(
            supports_check_mode=True,
            derived_arg_spec=self.module_args,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):

        for key in self.module_args:
            setattr(self, key, kwargs[key])

        if self.name:
            self.results['afdendpoints'] = self.get_item()
        else:
            self.results['afdendpoints'] = self.list_by_profile()

        return self.results

    def get_item(self):
        """Get a single Azure AFD Endpoint"""

        self.log('Get properties for {0}'.format(self.name))

        item = None
        result = []

        try:
            item = self.cdn_client.afd_endpoints.get(self.resource_group, self.profile_name, self.name)
        except Exception:
            pass

        if item and self.has_tags(item.tags, self.tags):
            result = [self.serialize_afdendpoint(item)]

        return result

    def list_by_profile(self):
        """Get all Azure AFD Endpoints within an AFD profile"""

        self.log('List all AFD Endpoints within an AFD profile')

        try:
            response = self.cdn_client.afd_endpoints.list_by_profile(self.resource_group, self.profile_name)
        except Exception as exc:
            self.fail('Failed to list all items - {0}'.format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(self.serialize_afdendpoint(item))

        return results

    def serialize_afdendpoint(self, afdendpoint):
        '''
        Convert a AFD Endpoint object to dict.
        :param afdendpoint: AFD Endpoint object
        :return: dict
        '''
        result = self.serialize_obj(afdendpoint, AZURE_OBJECT_CLASS)

        new_result = {}
        new_result['auto_generated_domain_name_label_scope'] = afdendpoint.auto_generated_domain_name_label_scope
        new_result['deployment_status'] = afdendpoint.deployment_status
        new_result['enabled_state'] = afdendpoint.enabled_state
        new_result['host_name'] = afdendpoint.host_name
        new_result['id'] = afdendpoint.id
        new_result['location'] = afdendpoint.location
        new_result['name'] = afdendpoint.name
        new_result['profile_name'] = re.sub('\\/.*', '', re.sub('.*profiles\\/', '', result['id']))
        new_result['provisioning_state'] = afdendpoint.provisioning_state
        new_result['resource_group'] = re.sub('\\/.*', '', re.sub('.*resourcegroups\\/', '', result['id']))
        new_result['tags'] = afdendpoint.tags
        new_result['type'] = afdendpoint.type
        return new_result


def main():
    """Main module execution code path"""

    AzureRMAFDEndpointInfo()


if __name__ == '__main__':
    main()
