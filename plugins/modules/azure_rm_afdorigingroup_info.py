#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Python SDK Reference: https://learn.microsoft.com/en-us/python/api/azure-mgmt-cdn/azure.mgmt.cdn.operations.afdorigingroupsoperations?view=azure-python
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_afdorigingroup_info
version_added: "3.4.0"
short_description: Get Azure Front Door OriginGroup facts to be used with Standard or Premium Frontdoor Service
description:
    - Get facts for a specific Azure Front Door (AFD) OriginGroup or all AFD OriginGroups.
    - This differs from the Front Door classic service and only is intended to be used by the Standard or Premium service offering.

options:
    name:
        description:
            - Limit results to a specific AFD OriginGroup.
        type: str
    profile_name:
        description:
            - Name of the AFD profile.
        required: true
        type: str
    resource_group:
        description:
            - Name of the resource group where this AFD Profile belongs.
        required: true
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Jarret Tooley (@jartoo)
'''

EXAMPLES = '''
- name: Get facts for all OriginGroups in AFD Profile
  azure_rm_afdorigingroup_info:
    resource_group: myResourceGroup
    profile_name: myCDNProfile

- name: Get facts of specific AFD OriginGroup
  azure_rm_afdorigingroup_info:
    name: myOriginGroup1
    profile_name: myCDNProfile
    resource_group: myResourceGroup
'''

RETURN = '''
afdorigingroups:
    description: List of AFD OriginGroups.
    returned: always
    type: complex
    contains:
        deployment_status:
            description:
                - Current state of the resource.
            type: str
            sample: NotStarted
        health_probe_settings:
            description:
                - Health probe settings to the origin that is used to determine the health of the origin.
            type: dict
            contains:
                probe_interval_in_seconds:
                    description:
                        - The number of seconds between health probes.
                    type: int
                probe_path:
                    description:
                        - The path relative to the origin that is used to determine the health of the origin.
                    type: str
                probe_protocol:
                    description:
                        - Protocol to use for health probe.
                    type: str
                    choices:
                        - Http
                        - Https
                        - NotSet
                probe_request_type:
                    description:
                        - The type of health probe request that is made.
                    type: str
                    choices:
                        - GET
                        - HEAD
                        - NotSet
        id:
            description:
                - ID of the AFD OriginGroup.
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/myCDN/providers/Microsoft.Cdn/profiles/myProfile/origingroups/myOG1"
        load_balancing_settings:
            description:
                - Load balancing settings for a backend pool.
            type: dict
            contains:
                additional_latency_in_milliseconds:
                    description:
                        - The additional latency in milliseconds for probes to fall into the lowest latency bucket.
                    type: int
                sample_size:
                    description:
                        - The number of samples to consider for load balancing decisions.
                    type: int
                successful_samples_required:
                    description:
                        - The number of samples within the sample period that must succeed.
                    type: int
        name:
            description:
                - Name of the AFD OriginGroup.
            type: str
        profile_name:
            description:
                - Name of the AFD Profile where the OriginGroup will be added.
            type: str
        provisioning_state:
            description:
                - Provisioning status of the AFD OriginGroup.
            type: str
            sample: Succeeded
        resource_group:
            description:
                - Name of a resource group where the AFD OriginGroup exists or will be created.
            type: str
        session_affinity_state:
            description:
                - Whether to allow session affinity on this host.
            type: str
            choices:
                - Enabled
                - Disabled
        type:
            description:
                - Resource type.
            type: str
            sample: Microsoft.Cdn/profiles/afdorigingroups
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
import re

AZURE_OBJECT_CLASS = 'AFDOriginGroup'


class AzureRMAFDOriginGroupInfo(AzureRMModuleBase):
    """Utility class to get Azure AFD OriginGroup facts"""

    def __init__(self):

        self.module_args = dict(
            name=dict(
                type='str'
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            profile_name=dict(
                type='str',
                required=True
            )
        )

        self.results = dict(
            changed=False,
            afdorigingroups=[]
        )

        self.name = None
        self.resource_group = None
        self.profile_name = None

        super(AzureRMAFDOriginGroupInfo, self).__init__(
            supports_check_mode=True,
            derived_arg_spec=self.module_args,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):

        for key in self.module_args:
            setattr(self, key, kwargs[key])

        if self.name:
            self.results['afdorigingroups'] = self.get_item()
        else:
            self.results['afdorigingroups'] = self.list_by_profile()

        return self.results

    def get_item(self):
        """Get a single Azure AFD OriginGroup"""

        self.log('Get properties for {0}'.format(self.name))

        item = None
        result = []

        try:
            item = self.cdn_client.afd_origin_groups.get(self.resource_group, self.profile_name, self.name)
        except Exception:
            pass

        if item:
            result = [self.serialize_afdorigingroup(item)]

        return result

    def list_by_profile(self):
        """Get all Azure AFD OriginGroups within an AFD profile"""

        self.log('List all AFD OriginGroups within an AFD profile')

        try:
            response = self.cdn_client.afd_origin_groups.list_by_profile(self.resource_group, self.profile_name)
        except Exception as exc:
            self.fail('Failed to list all items - {0}'.format(str(exc)))

        results = []
        for item in response:
            results.append(self.serialize_afdorigingroup(item))

        return results

    def serialize_afdorigingroup(self, afdorigingroup):
        '''
        Convert a AFD OriginGroup object to dict.
        :param afdorigingroup: AFD OriginGroup object
        :return: dict
        '''
        result = self.serialize_obj(afdorigingroup, AZURE_OBJECT_CLASS)

        new_result = {}
        new_result['deployment_status'] = afdorigingroup.deployment_status
        new_result['health_probe_settings'] = dict()
        new_result['health_probe_settings']['probe_interval_in_seconds'] = afdorigingroup.health_probe_settings.probe_interval_in_seconds
        new_result['health_probe_settings']['probe_path'] = afdorigingroup.health_probe_settings.probe_path
        new_result['health_probe_settings']['probe_protocol'] = afdorigingroup.health_probe_settings.probe_protocol
        new_result['health_probe_settings']['probe_request_type'] = afdorigingroup.health_probe_settings.probe_request_type
        new_result['id'] = afdorigingroup.id
        new_result['load_balancing_settings'] = dict()
        new_result['load_balancing_settings']['additional_latency_in_milliseconds'] = afdorigingroup.load_balancing_settings.additional_latency_in_milliseconds
        new_result['load_balancing_settings']['sample_size'] = afdorigingroup.load_balancing_settings.sample_size
        new_result['load_balancing_settings']['successful_samples_required'] = afdorigingroup.load_balancing_settings.successful_samples_required
        new_result['name'] = afdorigingroup.name
        new_result['profile_name'] = re.sub('\\/.*', '', re.sub('.*profiles\\/', '', result['id']))
        new_result['provisioning_state'] = afdorigingroup.provisioning_state
        new_result['resource_group'] = re.sub('\\/.*', '', re.sub('.*resourcegroups\\/', '', result['id']))
        new_result['session_affinity_state'] = afdorigingroup.session_affinity_state
        new_result['type'] = afdorigingroup.type
        return new_result


def main():
    """Main module execution code path"""
    AzureRMAFDOriginGroupInfo()


if __name__ == '__main__':
    main()
