#!/usr/bin/python
#
# Copyright (c) 2018 Hai Cao, <t-haicao@microsoft.com> Yunge Zhu <yungez@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_trafficmanagerprofile
version_added: "0.1.2"
short_description: Manage Azure Traffic Manager profile
description:
    - Create, update and delete a Traffic Manager profile.

options:
    resource_group:
        description:
            - Name of a resource group where the Traffic Manager profile exists or will be created.
        required: true
        type: str
    name:
        description:
            - Name of the Traffic Manager profile.
        required: true
        type: str
    state:
        description:
            - Assert the state of the Traffic Manager profile. Use C(present) to create or update a Traffic Manager profile and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present
    location:
        description:
            - Valid Azure location. Defaults to C(global) because in default public Azure cloud, Traffic Manager profile can only be deployed globally.
            - Reference U(https://docs.microsoft.com/en-us/azure/traffic-manager/quickstart-create-traffic-manager-profile#create-a-traffic-manager-profile).
        type: str
        default: global
    profile_status:
        description:
            - The status of the Traffic Manager profile.
        default: enabled
        type: str
        choices:
            - enabled
            - disabled
    routing_method:
        description:
            - The traffic routing method of the Traffic Manager profile.
        default: performance
        type: str
        choices:
            - performance
            - priority
            - weighted
            - geographic
    dns_config:
        description:
            - The DNS settings of the Traffic Manager profile.
        type: dict
        suboptions:
            relative_name:
                description:
                    - The relative DNS name provided by this Traffic Manager profile.
                    - If not provided, name of the Traffic Manager will be used.
                type: str
            ttl:
                description:
                    - The DNS Time-To-Live (TTL), in seconds.
                type: int
    monitor_config:
        description:
            - The endpoint monitoring settings of the Traffic Manager profile.
        type: dict
        suboptions:
            profile_monitor_status:
                description:
                    - The profile-level monitoring status of the Traffic Manager.
                type: str
                choices:
                    - CheckingEndpoint
                    - Online
                    - Degraded
                    - Inactive
                    - Stopped
                    - Disabled
            protocol:
                description:
                    - The protocol C(HTTP), C(HTTPS) or C(TCP) used to probe for endpoint health.
                type: str
                choices:
                    - HTTPS
                    - HTTP
                    - TCP
            port:
                description:
                    - The TCP port used to probe for endpoint health.
                type: int
            path:
                description:
                    - The path relative to the endpoint domain name used to probe for endpoint health.
                type: str
            interval:
                description:
                    - The monitor interval for endpoints in this profile in seconds.
                type: int
            timeout:
                description:
                    - The monitor timeout for endpoints in this profile in seconds.
                type: int
            tolerated_failures:
                description:
                    - The number of consecutive failed health check before declaring an endpoint in this profile Degraded after the next failed health check.
                type: int
            custom_headers:
                description:
                    - List of custom headers.
                type: list
                elements: dict
                suboptions:
                    name:
                        description:
                            - Header name.
                        type: str
                        required: true
                    value:
                        description:
                            - Header value.
                        type: str
                        required: true
            expected_status_code_ranges:
                description:
                    - List of expected status code ranges.
                type: list
                elements: dict
                suboptions:
                    max:
                        description:
                            - Max status code.
                        type: int
                        required: true
                    min:
                        description:
                            - Min status code.
                        type: int
                        required: true
        default:
            protocol: HTTP
            port: 80
            path: /
    max_return:
        description:
            -  Maximum number of endpoints to be returned for MultiValue routing type.
        type: int
    allowed_endpoint_record_types:
        description:
            - The list of allowed endpoint record types.
        type: list
        elements: str
        choices:
            - DomainName
            - IPv4Address
            - IPv6Address
            - Any

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Hai Cao (@caohai)
    - Yunge Zhu (@yungezz)

'''

EXAMPLES = '''
- name: Create a Traffic Manager Profile
  azure_rm_trafficmanagerprofile:
    name: tmtest
    resource_group: myResourceGroup
    location: global
    profile_status: enabled
    routing_method: priority
    dns_config:
      relative_name: tmtest
      ttl: 60
    monitor_config:
      protocol: HTTPS
      port: 80
      path: '/'
    tags:
      Environment: Test

- name: Delete a Traffic Manager Profile
  azure_rm_trafficmanagerprofile:
    state: absent
    name: tmtest
    resource_group: myResourceGroup
'''
RETURN = '''
id:
    description:
        - The ID of the traffic manager profile.
    returned: when traffic manager profile exists
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/tmt/providers/Microsoft.Network/trafficManagerProfiles/tmtest"
endpoints:
    description:
        - List of endpoint IDs attached to the profile.
    returned: when traffic manager endpoints exists
    type: list
    sample: [
            "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/tmt/providers/Microsoft.Network/trafficManagerProfiles/tm049b1ae293/exter
             nalEndpoints/e2",
            "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/tmt/providers/Microsoft.Network/trafficManagerProfiles/tm049b1ae293/exter
             nalEndpoints/e1"
            ]
'''
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import normalize_location_name
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.mgmt.trafficmanager.models import (
        Profile, DnsConfig, MonitorConfig, MonitorConfigExpectedStatusCodeRangesItem, MonitorConfigCustomHeadersItem
    )
except ImportError:
    # This is handled in azure_rm_common
    pass


def shorten_traffic_manager_dict(tmd):
    return dict(
        id=tmd['id'],
        endpoints=[endpoint['id'] for endpoint in tmd['endpoints']] if tmd['endpoints'] else []
    )


def traffic_manager_profile_to_dict(tmp):
    result = dict(
        id=tmp.id,
        name=tmp.name,
        type=tmp.type,
        tags=tmp.tags,
        location=tmp.location,
        profile_status=tmp.profile_status,
        routing_method=tmp.traffic_routing_method,
        dns_config=dict(),
        monitor_config=dict(),
        endpoints=[],
        max_return=tmp.max_return,
        allowed_endpoint_record_types=tmp.allowed_endpoint_record_types
    )
    if tmp.dns_config:
        result['dns_config']['relative_name'] = tmp.dns_config.relative_name
        result['dns_config']['fqdn'] = tmp.dns_config.fqdn
        result['dns_config']['ttl'] = tmp.dns_config.ttl
    if tmp.monitor_config:
        result['monitor_config']['profile_monitor_status'] = tmp.monitor_config.profile_monitor_status
        result['monitor_config']['protocol'] = tmp.monitor_config.protocol
        result['monitor_config']['port'] = tmp.monitor_config.port
        result['monitor_config']['path'] = tmp.monitor_config.path
        result['monitor_config']['interval'] = tmp.monitor_config.interval_in_seconds
        result['monitor_config']['timeout'] = tmp.monitor_config.timeout_in_seconds
        result['monitor_config']['tolerated_failures'] = tmp.monitor_config.tolerated_number_of_failures
        if tmp.monitor_config.expected_status_code_ranges is not None:
            result['monitor_config']['expected_status_code_ranges'] = [dict(min=x.min, max=x.max) for x in tmp.monitor_config.expected_status_code_ranges]
        else:
            result['monitor_config']['expected_status_code_ranges'] = None
        if tmp.monitor_config.custom_headers is not None:
            result['monitor_config']['custom_headers'] = [dict(name=x.name, value=x.value) for x in tmp.monitor_config.custom_headers]
        else:
            result['monitor_config']['custom_headers'] = None
    if tmp.endpoints:
        for endpoint in tmp.endpoints:
            result['endpoints'].append(dict(
                id=endpoint.id,
                name=endpoint.name,
                type=endpoint.type,
                target_resource_id=endpoint.target_resource_id,
                target=endpoint.target,
                endpoint_status=endpoint.endpoint_status,
                weight=endpoint.weight,
                priority=endpoint.priority,
                endpoint_location=endpoint.endpoint_location,
                endpoint_monitor_status=endpoint.endpoint_monitor_status,
                min_child_endpoints=endpoint.min_child_endpoints,
                geo_mapping=endpoint.geo_mapping
            ))
    return result


def create_dns_config_instance(dns_config):
    return DnsConfig(
        relative_name=dns_config['relative_name'],
        ttl=dns_config['ttl']
    )


def create_monitor_config_instance(monitor_config):

    custom_headers = []
    expected_status_code_ranges = []
    if monitor_config.get('custom_headers') is not None:
        for item in monitor_config['custom_headers']:
            custom_headers.append(MonitorConfigCustomHeadersItem(name=item['name'], value=item['value']))
    else:
        custom_headers = None
    if monitor_config.get('expected_status_code_ranges') is not None:
        for item in monitor_config['expected_status_code_ranges']:
            expected_status_code_ranges.append(MonitorConfigExpectedStatusCodeRangesItem(min=item['min'], max=item['max']))
    else:
        expected_status_code_ranges = None

    return MonitorConfig(
        profile_monitor_status=monitor_config.get('profile_monitor_status'),
        protocol=monitor_config.get('protocol'),
        port=monitor_config.get('port'),
        path=monitor_config.get('path'),
        interval_in_seconds=monitor_config.get('interval'),
        timeout_in_seconds=monitor_config.get('timeout'),
        tolerated_number_of_failures=monitor_config.get('tolerated_failures'),
        custom_headers=custom_headers,
        expected_status_code_ranges=expected_status_code_ranges
    )


dns_config_spec = dict(
    relative_name=dict(type='str'),
    ttl=dict(type='int')
)

monitor_config_spec = dict(
    profile_monitor_status=dict(type='str', choices=['CheckingEndpoint', 'Online', 'Degraded', 'Disabled', 'Inactive', 'Stopped']),
    protocol=dict(type='str', choices=['HTTP', 'HTTPS', 'TCP']),
    port=dict(type='int'),
    path=dict(type='str'),
    interval=dict(type='int'),
    timeout=dict(type='int'),
    tolerated_failures=dict(type='int'),
    custom_headers=dict(
        type='list',
        elements='dict',
        options=dict(
            name=dict(type='str', required=True),
            value=dict(type='str', required=True)
        )
    ),
    expected_status_code_ranges=dict(
        type='list',
        elements='dict',
        options=dict(
            min=dict(type='int', required=True),
            max=dict(type='int', required=True)
        )
    )
)


class AzureRMTrafficManagerProfile(AzureRMModuleBaseExt):

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            location=dict(
                type='str',
                default='global'
            ),
            profile_status=dict(
                type='str',
                default='enabled',
                choices=['enabled', 'disabled']
            ),
            routing_method=dict(
                type='str',
                default='performance',
                choices=['performance', 'priority', 'weighted', 'geographic']
            ),
            dns_config=dict(
                type='dict',
                options=dns_config_spec
            ),
            monitor_config=dict(
                type='dict',
                default=dict(
                    protocol='HTTP',
                    port=80,
                    path='/'
                ),
                options=monitor_config_spec
            ),
            max_return=dict(
                type='int'
            ),
            allowed_endpoint_record_types=dict(
                type='list',
                elements='str',
                choices=['DomainName', 'IPv4Address', 'IPv6Address', 'Any']
            ),
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.tags = None
        self.location = None
        self.profile_status = None
        self.routing_method = None
        self.dns_config = None
        self.monitor_config = None
        self.endpoints_copy = None
        self.max_return = None
        self.allowed_endpoint_record_types = None

        self.results = dict(
            changed=False
        )

        super(AzureRMTrafficManagerProfile, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                           supports_check_mode=True,
                                                           supports_tags=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        to_be_updated = False

        if not self.dns_config:
            self.dns_config = dict(
                relative_name=self.name,
                ttl=60
            )

        if not self.location:
            self.location = 'global'

        response = self.get_traffic_manager_profile()

        if self.state == 'present':
            if not response:
                to_be_updated = True
            else:
                self.results = shorten_traffic_manager_dict(response)
                self.log('Results : {0}'.format(response))
                update_tags, response['tags'] = self.update_tags(response['tags'])

                if update_tags:
                    to_be_updated = True

                to_be_updated = to_be_updated or self.check_update(response)

            if to_be_updated:
                self.log("Need to Create / Update the Traffic Manager profile")

                if not self.check_mode:
                    self.results = shorten_traffic_manager_dict(self.create_update_traffic_manager_profile())
                    self.log("Creation / Update done.")

                self.results['changed'] = True
                return self.results

        elif self.state == 'absent' and response:
            self.log("Need to delete the Traffic Manager profile")
            self.results = shorten_traffic_manager_dict(response)
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_traffic_manager_profile()

            self.log("Traffic Manager profile deleted")

        return self.results

    def get_traffic_manager_profile(self):
        '''
        Gets the properties of the specified Traffic Manager profile

        :return: deserialized Traffic Manager profile dict
        '''
        self.log("Checking if Traffic Manager profile {0} is present".format(self.name))
        try:
            response = self.traffic_manager_management_client.profiles.get(self.resource_group, self.name)
            self.log("Response : {0}".format(response))
            self.log("Traffic Manager profile : {0} found".format(response.name))
            self.endpoints_copy = response.endpoints if response and response.endpoints else None
            return traffic_manager_profile_to_dict(response)
        except ResourceNotFoundError:
            self.log('Did not find the Traffic Manager profile.')
            return False

    def delete_traffic_manager_profile(self):
        '''
        Deletes the specified Traffic Manager profile in the specified subscription and resource group.
        :return: True
        '''

        self.log("Deleting the Traffic Manager profile {0}".format(self.name))
        try:
            self.traffic_manager_management_client.profiles.delete(self.resource_group, self.name)
            return True
        except Exception as e:
            self.log('Error attempting to delete the Traffic Manager profile.')
            self.fail("Error deleting the Traffic Manager profile: {0}".format(e.message))
            return False

    def create_update_traffic_manager_profile(self):
        '''
        Creates or updates a Traffic Manager profile.

        :return: deserialized Traffic Manager profile state dictionary
        '''
        self.log("Creating / Updating the Traffic Manager profile {0}".format(self.name))

        parameters = Profile(
            tags=self.tags,
            location=self.location,
            profile_status=self.profile_status,
            traffic_routing_method=self.routing_method,
            dns_config=create_dns_config_instance(self.dns_config) if self.dns_config else None,
            monitor_config=create_monitor_config_instance(self.monitor_config) if self.monitor_config else None,
            endpoints=self.endpoints_copy,
            max_return=self.max_return,
            allowed_endpoint_record_types=self.allowed_endpoint_record_types
        )
        try:
            response = self.traffic_manager_management_client.profiles.create_or_update(self.resource_group, self.name, parameters)
            return traffic_manager_profile_to_dict(response)
        except Exception as exc:
            self.log('Error attempting to create the Traffic Manager.')
            self.fail("Error creating the Traffic Manager: {0}".format(exc.message))

    def check_update(self, response):
        if self.location and normalize_location_name(response['location']) != normalize_location_name(self.location):
            self.log("Location Diff - Origin {0} / Update {1}".format(response['location'], self.location))
            return True

        if self.profile_status and response['profile_status'].lower() != self.profile_status:
            self.log("Profile Status Diff - Origin {0} / Update {1}".format(response['profile_status'], self.profile_status))
            return True

        if self.routing_method and response['routing_method'].lower() != self.routing_method:
            self.log("Traffic Routing Method Diff - Origin {0} / Update {1}".format(response['routing_method'], self.routing_method))
            return True

        if self.dns_config and \
           (response['dns_config']['relative_name'] != self.dns_config['relative_name'] or response['dns_config']['ttl'] != self.dns_config['ttl']):
            self.log("DNS Config Diff - Origin {0} / Update {1}".format(response['dns_config'], self.dns_config))
            return True

        if self.max_return and response['max_return'] != self.max_return:
            self.log("Profile max_return Diff - Origin {0} / Update {1}".format(response['max_return'], self.max_return))
            return True
        else:
            self.max_return = response['max_return']

        if not self.default_compare({}, self.allowed_endpoint_record_types, response['allowed_endpoint_record_types'], '', dict(compare=[])):
            self.log("Profile allowed_endpoint_record_types Diff - Origin {0} / Update {1}".format(response['allowed_endpoint_record_types'],
                                                                                                   self.allowed_endpoint_record_types))
            return True

        if not self.default_compare({}, self.monitor_config, response['monitor_config'], '', dict(compare=[])):
            self.log("Monitor Config Diff - Origin {0} / Update {1}".format(response['monitor_config'], self.monitor_config))
            return True

        return False


def main():
    """Main execution"""
    AzureRMTrafficManagerProfile()


if __name__ == '__main__':
    main()
