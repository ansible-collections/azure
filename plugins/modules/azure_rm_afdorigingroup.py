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
module: azure_rm_afdorigingroup
version_added: "3.4.0"
short_description: Manage an Azure Front Door OriginGroup to be used with Standard or Premium Frontdoor
description:
    - Create, update and delete an Azure Front Door (AFD) OriginGroup to be used by a Front Door Service Profile created using azure_rm_cdnprofile.
    - This differs from the Front Door classic service and only is intended to be used by the Standard or Premium service offering.

options:
    health_probe_settings:
        description:
            - Health probe settings to the origin that is used to determine the health of the origin.
        type: dict
        suboptions:
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
    load_balancing_settings:
        description:
            - Load balancing settings for a backend pool.
        type: dict
        suboptions:
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
        required: true
        type: str
    profile_name:
        description:
            - Name of the AFD Profile where the OriginGroup will be added.
        required: true
        type: str
    resource_group:
        description:
            - Name of a resource group where the AFD OriginGroup exists or will be created.
        required: true
        type: str
    session_affinity_state:
        description:
            - Whether to allow session affinity on this host.
        type: str
        choices:
            - Enabled
            - Disabled
    state:
        description:
            - Assert the state of the AFD OriginGroup. Use C(present) to create or update an AFD OriginGroup and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Jarret Tooley (@jartoo)
'''

EXAMPLES = '''
- name: Create an AFD OriginGroup
  azure_rm_afdorigingroup:
    name: myOriginGroup
    profile_name: myProfile
    resource_group: myResourceGroup
    state: present
    tags:
      testing: testing

- name: Delete the AFD OriginGroup
  azure_rm_afdorigingroup:
    name: myOriginGroup
    profile_name: myProfile
    resource_group: myResourceGroup
    state: absent
'''
RETURN = '''
id:
    description:
        - ID of the AFD OriginGroup.
    returned: always
    type: str
    sample: "id: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/myResourceGroup/providers/Microsoft.Cdn/profiles/myProf/origingroups/myOG"
'''
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.mgmt.cdn.models import AFDOriginGroup, LoadBalancingSettingsParameters, HealthProbeParameters
except ImportError as ec:
    # This is handled in azure_rm_common
    pass


def origingroup_to_dict(origingroup):
    return dict(
        additional_latency_in_milliseconds=origingroup.load_balancing_settings.additional_latency_in_milliseconds,
        deployment_status=origingroup.deployment_status,
        id=origingroup.id,
        name=origingroup.name,
        probe_interval_in_seconds=origingroup.health_probe_settings.probe_interval_in_seconds,
        probe_path=origingroup.health_probe_settings.probe_path,
        probe_protocol=origingroup.health_probe_settings.probe_protocol,
        probe_request_type=origingroup.health_probe_settings.probe_request_type,
        provisioning_state=origingroup.provisioning_state,
        sample_size=origingroup.load_balancing_settings.sample_size,
        session_affinity_state=origingroup.session_affinity_state,
        successful_samples_required=origingroup.load_balancing_settings.successful_samples_required,
        traffic_restoration_time_to_healed_or_new_endpoints_in_minutes=origingroup.traffic_restoration_time_to_healed_or_new_endpoints_in_minutes,
        type=origingroup.type
    )


class AzureRMOriginGroup(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            load_balancing_settings=dict(
                type='dict',
                options=dict(
                    additional_latency_in_milliseconds=dict(type='int'),
                    sample_size=dict(type='int'),
                    successful_samples_required=dict(type='int')
                )
            ),
            health_probe_settings=dict(
                type='dict',
                options=dict(
                    probe_path=dict(type='str'),
                    probe_request_type=dict(type='str', choices=['GET', 'HEAD', 'NotSet']),
                    probe_protocol=dict(type='str', choices=['Http', 'Https', 'NotSet']),
                    probe_interval_in_seconds=dict(type='int')
                )
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
            session_affinity_state=dict(
                type='str',
                choices=['Enabled', 'Disabled']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.health_probe_settings = dict()
        self.health_probe_settings['probe_path'] = None
        self.health_probe_settings['probe_request_type'] = None
        self.health_probe_settings['probe_protocol'] = None
        self.health_probe_settings['probe_interval_in_seconds'] = None
        self.load_balancing_settings = dict()
        self.load_balancing_settings['additional_latency_in_milliseconds'] = None
        self.load_balancing_settings['sample_size'] = None
        self.load_balancing_settings['successful_samples_required'] = None
        self.session_affinity_state = None

        self.name = None
        self.profile_name = None
        self.resource_group = None
        self.state = None

        self.results = dict(changed=False)

        super(AzureRMOriginGroup, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        to_be_updated = False

        response = self.get_origingroup()

        if self.state == 'present':

            if not response:
                self.log("Need to create the OriginGroup")

                if not self.check_mode:
                    new_response = self.create_origingroup()
                    self.results['id'] = new_response['id']

                self.results['changed'] = True

            else:
                self.log('Results : {0}'.format(response))
                self.results['id'] = response['id']

                if response['probe_path'] != self.health_probe_settings['probe_path'] and self.health_probe_settings['probe_path']:
                    to_be_updated = True
                if response['probe_request_type'] != self.health_probe_settings['probe_request_type'] and self.health_probe_settings['probe_request_type']:
                    to_be_updated = True
                if response['probe_protocol'] != self.health_probe_settings['probe_protocol'] and self.health_probe_settings['probe_protocol']:
                    to_be_updated = True
                if response['probe_interval_in_seconds'] != self.health_probe_settings['probe_interval_in_seconds'] and \
                        self.health_probe_settings['probe_interval_in_seconds']:
                    to_be_updated = True
                if response['sample_size'] != self.load_balancing_settings['sample_size'] and self.load_balancing_settings['sample_size']:
                    to_be_updated = True
                if response['successful_samples_required'] != self.load_balancing_settings['successful_samples_required'] and \
                        self.load_balancing_settings['successful_samples_required']:
                    to_be_updated = True
                if response['additional_latency_in_milliseconds'] != self.load_balancing_settings['additional_latency_in_milliseconds'] and \
                        self.load_balancing_settings['additional_latency_in_milliseconds']:
                    to_be_updated = True
                if response['session_affinity_state'] != self.session_affinity_state and self.session_affinity_state:
                    to_be_updated = True

                if to_be_updated:
                    self.log("Need to update the AFD OriginGroup")
                    self.results['id'] = response['id']

                    if not self.check_mode:
                        new_response = self.update_origingroup()
                        self.results['id'] = new_response['id']

                    self.results['changed'] = True

        elif self.state == 'absent':
            if not response:
                self.log("AFD OriginGroup {0} does not exist.".format(self.name))
                self.results['id'] = ""
            else:
                self.log("Need to delete the OriginGroup")
                self.results['changed'] = True
                self.results['id'] = response['id']
                if not self.check_mode:
                    self.delete_origingroup()
                    self.log("Azure AFD OriginGroup deleted")

        return self.results

    def create_origingroup(self):
        '''
        Creates a Azure OriginGroup.

        :return: deserialized Azure OriginGroup instance state dictionary
        '''
        self.log("Creating the Azure OriginGroup instance {0}".format(self.name))

        loadbalancingsettings = LoadBalancingSettingsParameters(
            sample_size=self.load_balancing_settings['sample_size'],
            successful_samples_required=self.load_balancing_settings['successful_samples_required'],
            additional_latency_in_milliseconds=self.load_balancing_settings['additional_latency_in_milliseconds']
        )

        healthprobesettings = HealthProbeParameters(
            probe_path=self.health_probe_settings['probe_path'],
            probe_request_type=self.health_probe_settings['probe_request_type'],
            probe_protocol=self.health_probe_settings['probe_protocol'],
            probe_interval_in_seconds=self.health_probe_settings['probe_interval_in_seconds']
        )

        parameters = AFDOriginGroup(
            load_balancing_settings=loadbalancingsettings,
            health_probe_settings=healthprobesettings,
            session_affinity_state=self.session_affinity_state
        )

        try:
            poller = self.cdn_client.afd_origin_groups.begin_create(self.resource_group,
                                                                    self.profile_name,
                                                                    self.name,
                                                                    parameters)
            response = self.get_poller_result(poller)
            return origingroup_to_dict(response)
        except Exception as exc:
            self.log('Error attempting to create Azure OriginGroup instance.')
            self.fail("Error Creating Azure OriginGroup instance: {0}".format(exc.message))

    def update_origingroup(self):
        '''
        Updates an Azure OriginGroup.

        :return: deserialized Azure OriginGroup instance state dictionary
        '''
        self.log("Updating the Azure OriginGroup instance {0}".format(self.name))

        loadbalancingsettings = LoadBalancingSettingsParameters(
            sample_size=self.load_balancing_settings['sample_size'],
            successful_samples_required=self.load_balancing_settings['successful_samples_required'],
            additional_latency_in_milliseconds=self.load_balancing_settings['additional_latency_in_milliseconds']
        )

        healthprobesettings = HealthProbeParameters(
            probe_path=self.health_probe_settings['probe_path'],
            probe_request_type=self.health_probe_settings['probe_request_type'],
            probe_protocol=self.health_probe_settings['probe_protocol'],
            probe_interval_in_seconds=self.health_probe_settings['probe_interval_in_seconds']
        )

        parameters = AFDOriginGroup(
            load_balancing_settings=loadbalancingsettings,
            health_probe_settings=healthprobesettings,
            session_affinity_state=self.session_affinity_state
        )

        try:
            poller = self.cdn_client.afd_origin_groups.begin_update(
                resource_group_name=self.resource_group,
                profile_name=self.profile_name,
                origin_group_name=self.name,
                origin_group_update_properties=parameters)
            response = self.get_poller_result(poller)
            return origingroup_to_dict(response)
        except Exception as exc:
            self.log('Error attempting to update Azure OriginGroup instance.')
            self.fail("Error updating Azure OriginGroup instance: {0}".format(exc.message))

    def delete_origingroup(self):
        '''
        Deletes the specified Azure OriginGroup in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the OriginGroup {0}".format(self.name))
        try:
            poller = self.cdn_client.afd_origin_groups.begin_delete(self.resource_group, self.profile_name, self.name)
            self.get_poller_result(poller)
            return True
        except Exception as e:
            self.log('Error attempting to delete the OriginGroup.')
            self.fail("Error deleting the OriginGroup: {0}".format(e.message))
            return False

    def get_origingroup(self):
        '''
        Gets the properties of the specified OriginGroup.

        :return: deserialized OriginGroup state dictionary
        '''
        self.log(
            "Checking if the OriginGroup {0} is present".format(self.name))
        try:
            response = self.cdn_client.afd_origin_groups.get(self.resource_group, self.profile_name, self.name)
            self.log("Response : {0}".format(response))
            self.log("OriginGroup : {0} found".format(response.name))
            return origingroup_to_dict(response)
        except Exception as err:
            self.log('Did not find the OriginGroup.' + err.args[0])
            return False


def main():
    """Main execution"""
    AzureRMOriginGroup()


if __name__ == '__main__':
    main()
