#!/usr/bin/python
#
# Copyright (c) 2021 Ross Bender (@l3ender)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_privateendpointdnszonegroup

version_added: "1.10.0"

short_description: Create, update, or manage private endpoint DNS zone groups.

description:
    - Create, update, or manage private endpoint DNS zone groups.

options:
    name:
        description:
            - The name of the private endpoint DNS zone group.
        type: str
        required: true
    private_endpoint:
        description:
            - Name of private endpoint.
        type: str
        required: true
    resource_group:
        description:
            - Resource group of the private endpoint.
        type: str
        required: true
    private_dns_zone_configs:
        description:
            - The Private DNS zones configurations.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of the private dns zone configs.
                type: str
            private_dns_zone:
                description:
                    - The name of the Private DNS zone.
                type: str
    state:
        description:
            - State of the private endpoint DNS zone group. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Ross Bender (@l3ender)
'''

EXAMPLES = '''
- name: Create zone group for private endpoint
  azure_rm_privateendpointdnszonegroup:
    name: "my-zone-group"
    private_endpoint: "my-private-endpoint"
    resource_group: "my-resource-group"
    private_dns_zone_configs:
      - name: "default"
        private_dns_zone: "privatelink.postgres.database.azure.com"

- name: Create zone group for private endpoint
  azure_rm_privateendpointdnszonegroup:
    name: "my-zone-group"
    private_endpoint: "my-private-endpoint"
    resource_group: "my-resource-group"
    state: "absent"
'''


RETURN = '''
state:
    description:
        - Current state of the private endpoint zone group.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID of the private endpoint zone group.
            sample: >-
                /subscriptions/xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/privateEndpoints/
                myPrivateEndpoint/privateDnsZoneGroups/myZoneGroup
            returned: always
            type: str
        name:
            description:
                - Name of the private endpoint zone group.
            returned: always
            type: str
            sample: myZoneGroup
        private_dns_zone_configs:
            description:
                - List of zone configuration within the zone group.
            returned: always
            type: list
            contains:
                name:
                    description:
                        - Name of the zone config.
                    returned: always
                    type: str
                    sample: default
                private_dns_zone_id:
                    description:
                        - ID of the private DNS zone.
                    returned: always
                    type: str
                    sample: >-
                        /subscriptions/xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/
                        privateDnsZones/privatelink.postgres.database.azure.com
                record_sets:
                    description:
                        - List of DNS records for zone.
                    returned: always
                    type: list
                    contains:
                        fqdn:
                            description:
                                - Fully qualified domain name of the record.
                            returned: always
                            type: str
                            sample: myPostgreSqlSrv-123.privatelink.postgres.database.azure.com
                        ip_addresses:
                            description:
                                - IP addresses for the record.
                            returned: always
                            type: list
                            sample: ['10.1.0.4']
                        provisioning_state:
                            description:
                                - Provisioning state of the resource.
                            returned: always
                            type: str
                            sample: Succeeded
                        record_set_name:
                            description:
                                - Name of the record.
                            returned: always
                            type: str
                            sample: myPostgreSqlSrv-123
                        record_type:
                            description:
                                - Type of record.
                            returned: always
                            type: str
                            sample: A
                        ttl:
                            description:
                                - Time to live value of the record.
                            returned: always
                            type: int
                            sample: 10
        provisioning_state:
            description:
                - Provisioning state of the resource.
            returned: always
            type: str
            sample: Succeeded
'''

try:
    from msrestazure.tools import resource_id
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


private_dns_zone_configs_spec = dict(
    name=dict(type="str"),
    private_dns_zone=dict(type="str")
)


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMPrivateEndpointDnsZoneGroup(AzureRMModuleBaseExt):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type="str", required=True),
            private_endpoint=dict(type="str", required=True),
            resource_group=dict(type="str", required=True),
            private_dns_zone_configs=dict(type="list", elements="dict", options=private_dns_zone_configs_spec),
            state=dict(type="str", default="present", choices=["present", "absent"]),
        )

        self.name = None
        self.private_endpoint = None
        self.resource_group = None
        self.state = None
        self.parameters = dict()
        self.results = dict(
            changed=False,
            state=dict()
        )
        self.to_do = Actions.NoAction

        super(AzureRMPrivateEndpointDnsZoneGroup, self).__init__(self.module_arg_spec,
                                                                 supports_tags=False,
                                                                 supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        for zone_config in self.parameters.get("private_dns_zone_configs", []):
            zone_name = zone_config.pop("private_dns_zone")
            zone_config["private_dns_zone_id"] = self.private_dns_zone_id(zone_name)

        self.log("Fetching private endpoint {0}".format(self.name))
        old_response = self.get_zone()

        if old_response is None or not old_response:
            if self.state == "present":
                self.to_do = Actions.Create
                self.ensure_private_endpoint()
        else:
            if self.state == "absent":
                self.to_do = Actions.Delete
            else:
                self.results["compare"] = []
                if not self.idempotency_check(old_response, self.parameters):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.results["changed"] = True
            if self.check_mode:
                return self.results
            response = self.create_update_zone()
        elif self.to_do == Actions.Delete:
            self.results["changed"] = True
            if self.check_mode:
                return self.results
            response = self.delete_zone()
        else:
            self.results["changed"] = False
            response = old_response

        if response is not None:
            self.results["state"] = response

        return self.results

    def get_zone(self):
        try:
            item = self.network_client.private_dns_zone_groups.get(resource_group_name=self.resource_group,
                                                                   private_endpoint_name=self.private_endpoint,
                                                                   private_dns_zone_group_name=self.name)
            return self.zone_to_dict(item)
        except Exception:
            self.log("Did not find the private endpoint resource")
        return None

    def create_update_zone(self):
        try:
            self.parameters["name"] = self.name
            response = self.network_client.private_dns_zone_groups.create_or_update(resource_group_name=self.resource_group,
                                                                                    private_endpoint_name=self.private_endpoint,
                                                                                    private_dns_zone_group_name=self.name,
                                                                                    parameters=self.parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

            return self.zone_to_dict(response)
        except Exception as exc:
            self.fail("Error creating or updating DNS zone group {0} for private endpoint {1}: {2}".format(self.name, self.private_endpoint, str(exc)))

    def ensure_private_endpoint(self):
        try:
            self.network_client.private_endpoints.get(resource_group_name=self.resource_group,
                                                      private_endpoint_name=self.private_endpoint)
        except Exception:
            self.fail("Could not load the private endpoint {0}.".format(self.private_endpoint))

    def delete_zone(self):
        try:
            response = self.network_client.private_dns_zone_groups.delete(resource_group_name=self.resource_group,
                                                                          private_endpoint_name=self.private_endpoint,
                                                                          private_dns_zone_group_name=self.name)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)

            return response
        except Exception as exc:
            self.fail("Error deleting private endpoint {0}: {1}".format(self.name, str(exc)))

    def zone_to_dict(self, zone):
        zone_dict = zone.as_dict()
        return dict(
            id=zone_dict.get("id"),
            name=zone_dict.get("name"),
            private_dns_zone_configs=[self.zone_config_to_dict(zone_config) for zone_config in zone_dict.get("private_dns_zone_configs", [])],
            provisioning_state=zone_dict.get("provisioning_state"),
        )

    def zone_config_to_dict(self, zone_config):
        return dict(
            name=zone_config.get("name"),
            private_dns_zone_id=zone_config.get("private_dns_zone_id"),
            record_sets=[self.record_set_to_dict(record_set) for record_set in zone_config.get("record_sets", [])],
        )

    def record_set_to_dict(self, record_set):
        return dict(
            fqdn=record_set.get("fqdn"),
            ip_addresses=record_set.get("ip_addresses"),
            provisioning_state=record_set.get("provisioning_state"),
            record_set_name=record_set.get("record_set_name"),
            record_type=record_set.get("record_type"),
            ttl=record_set.get("ttl"),
        )

    def private_dns_zone_id(self, name):
        return resource_id(subscription=self.subscription_id,
                           resource_group=self.resource_group,
                           namespace='Microsoft.Network',
                           type='privateDnsZones',
                           name=name)


def main():
    AzureRMPrivateEndpointDnsZoneGroup()


if __name__ == "__main__":
    main()
