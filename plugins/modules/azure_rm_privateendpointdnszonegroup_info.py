#!/usr/bin/python
#
# Copyright (c) 2021 Ross Bender (@l3ender)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_privateendpointdnszonegroup_info

version_added: "1.10.0"

short_description: Get private endpoint DNS zone group info.

description:
    - Get facts for private endpoint DNS zone groups.

options:
    name:
        description:
            - Limit results to a single private endpoint DNS zone group.
        type: str
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

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Ross Bender (@l3ender)
'''

EXAMPLES = '''
- name: Get specific DNS zone groups for a private endpoing
  azure_rm_privateendpointdnszonegroup_info:
    name: "my-zone-group"
    private_endpoint: "my-private-endpoint"
    resource_group: "my-resource-group"

- name: Get all DNS zone groups for a private endpoint
  azure_rm_privateendpointdnszonegroup_info:
    private_endpoint: "my-private-endpoint"
    resource_group: "my-resource-group"
'''

RETURN = '''
groups:
    description:
        - List of private endpoint zone groups.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID of the private endpoint zone group.
            sample: >-
                /subscriptions/xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/privateEndpoints/myPrivateEndpoint/
                privateDnsZoneGroups/myZoneGroup
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
            type: complex
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
                    type: complex
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
    from msrestazure.azure_exceptions import CloudError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMPrivateEndpointDnsZoneGroupInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type="str"),
            private_endpoint=dict(type="str", required=True),
            resource_group=dict(type="str", required=True),
        )

        self.results = dict(
            changed=False,
            groups=[],
        )

        self.name = None
        self.private_endpoint = None
        self.resource_group = None
        self.results = dict(
            changed=False,
        )

        super(AzureRMPrivateEndpointDnsZoneGroupInfo, self).__init__(self.module_arg_spec,
                                                                     supports_check_mode=True,
                                                                     supports_tags=False,
                                                                     facts_module=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results["groups"] = self.get_item()
        else:
            self.results["groups"] = self.list_items()

        return self.results

    def get_item(self):
        self.log("Get properties for {0} in {1}".format(self.name, self.private_endpoint))

        try:
            item = self.network_client.private_dns_zone_groups.get(resource_group_name=self.resource_group,
                                                                   private_endpoint_name=self.private_endpoint,
                                                                   private_dns_zone_group_name=self.name)
            return [self.zone_to_dict(item)]
        except CloudError:
            self.log("Could not get info for {0} in {1}".format(self.name, self.private_endpoint))

        return []

    def list_items(self):
        self.log("List all in {0}".format(self.private_endpoint))
        try:
            items = self.network_client.private_dns_zone_groups.list(private_endpoint_name=self.private_endpoint, resource_group_name=self.resource_group)
            return [self.zone_to_dict(item) for item in items]
        except CloudError as exc:
            self.fail("Failed to list all items in {0}: {1}".format(self.private_endpoint, str(exc)))

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
            id=zone_config.get("id"),
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


def main():
    AzureRMPrivateEndpointDnsZoneGroupInfo()


if __name__ == "__main__":
    main()
