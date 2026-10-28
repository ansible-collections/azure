#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang, (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_managedredis_info
version_added: "4.2.0"
short_description: Get Azure Managed Redis cluster facts
description:
    - Get facts of Azure Managed Redis clusters (C(Microsoft.Cache/redisEnterprise)).

options:
    resource_group:
        description:
            - The name of the resource group to which the cluster belongs.
            - Required when I(name) is set.
        type: str
    name:
        description:
            - The name of the Azure Managed Redis cluster.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Get an Azure Managed Redis cluster by name
  azure_rm_managedredis_info:
    resource_group: myResourceGroup
    name: myredis

- name: List Azure Managed Redis clusters in a resource group
  azure_rm_managedredis_info:
    resource_group: myResourceGroup

- name: List Azure Managed Redis clusters in the current subscription filtered by tag
  azure_rm_managedredis_info:
    tags:
      - env:test
'''

RETURN = '''
clusters:
    description: List of Azure Managed Redis clusters.
    returned: always
    type: list
    contains:
        id:
            description:
                - Resource ID of the cluster.
            returned: always
            type: str
            sample: /subscriptions/xxxx-xxxx/resourceGroups/myResourceGroup/providers/Microsoft.Cache/redisEnterprise/myredis
        name:
            description:
                - Name of the cluster.
            returned: always
            type: str
            sample: myredis
        type:
            description:
                - Type of the resource.
            returned: always
            type: str
            sample: Microsoft.Cache/redisEnterprise
        location:
            description:
                - Location of the cluster.
            returned: always
            type: str
            sample: eastus
        tags:
            description:
                - Tags assigned to the cluster.
            returned: always
            type: dict
            sample: {"env": "test"}
        kind:
            description:
                - Kind of the cluster.
            returned: always
            type: str
            sample: v2
        sku:
            description:
                - SKU of the cluster.
            returned: always
            type: dict
            sample: {"name": "Balanced_B1"}
        zones:
            description:
                - Availability Zones where the cluster is deployed.
            returned: always
            type: list
            elements: str
        identity:
            description:
                - Managed identity of the cluster.
            returned: always
            type: dict
        high_availability:
            description:
                - Whether high availability is enabled.
            returned: always
            type: str
            sample: Enabled
        minimum_tls_version:
            description:
                - Minimum TLS version the cluster supports.
            returned: always
            type: str
            sample: "1.2"
        public_network_access:
            description:
                - Whether public network traffic can access the cluster.
            returned: always
            type: str
            sample: Disabled
        encryption:
            description:
                - Encryption-at-rest configuration of the cluster.
            returned: always
            type: dict
        host_name:
            description:
                - DNS name of the cluster endpoint.
            returned: always
            type: str
            sample: myredis.eastus.redis.azure.net
        provisioning_state:
            description:
                - Provisioning state of the cluster.
            returned: always
            type: str
            sample: Succeeded
        resource_state:
            description:
                - Current resource state of the cluster.
            returned: always
            type: str
            sample: Running
        redundancy_mode:
            description:
                - Redundancy mode of the cluster.
            returned: always
            type: str
            sample: ZR
        redis_version:
            description:
                - Redis version of the cluster.
            returned: always
            type: str
            sample: "7.4"
        private_endpoint_connections:
            description:
                - Private endpoint connections of the cluster.
            returned: always
            type: list
            elements: dict
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
    from azure.core.serialization import as_attribute_dict
except ImportError:
    # This is handled in azure_rm_common
    pass


def cluster_to_dict(cluster):
    cluster_dict = as_attribute_dict(cluster, exclude_readonly=False)
    return dict(
        id=cluster_dict.get('id'),
        name=cluster_dict.get('name'),
        type=cluster_dict.get('type'),
        location=cluster_dict.get('location'),
        tags=cluster_dict.get('tags'),
        kind=cluster_dict.get('kind'),
        sku=cluster_dict.get('sku'),
        zones=cluster_dict.get('zones'),
        identity=cluster_dict.get('identity'),
        high_availability=cluster_dict.get('high_availability'),
        minimum_tls_version=cluster_dict.get('minimum_tls_version'),
        public_network_access=cluster_dict.get('public_network_access'),
        encryption=cluster_dict.get('encryption'),
        host_name=cluster_dict.get('host_name'),
        provisioning_state=cluster_dict.get('provisioning_state'),
        resource_state=cluster_dict.get('resource_state'),
        redundancy_mode=cluster_dict.get('redundancy_mode'),
        redis_version=cluster_dict.get('redis_version'),
        private_endpoint_connections=cluster_dict.get('private_endpoint_connections'),
    )


class AzureRMManagedRedisInfo(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            tags=dict(type='list', elements='str'),
        )

        self.resource_group = None
        self.name = None
        self.tags = None

        self.results = dict(changed=False)

        super(AzureRMManagedRedisInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True,
        )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            if not self.resource_group:
                self.fail("resource_group is required when filtering by name")
            self.results['clusters'] = self.get_by_name()
        elif self.resource_group:
            self.results['clusters'] = self.list_by_resource_group()
        else:
            self.results['clusters'] = self.list_all()

        return self.results

    def get_by_name(self):
        self.log("Get the Azure Managed Redis cluster {0}".format(self.name))
        results = []
        try:
            response = self.redisenterprise_client.redis_enterprise.get(resource_group_name=self.resource_group,
                                                                        cluster_name=self.name)
            if self.has_tags(response.tags, self.tags):
                results.append(cluster_to_dict(response))
        except ResourceNotFoundError:
            self.log("Did not find the Azure Managed Redis cluster {0}".format(self.name))
        except HttpResponseError as exc:
            self.fail("Error getting the Azure Managed Redis cluster {0}: {1}".format(self.name, str(exc)))
        return results

    def list_by_resource_group(self):
        self.log("List Azure Managed Redis clusters in resource group {0}".format(self.resource_group))
        results = []
        try:
            for item in self.redisenterprise_client.redis_enterprise.list_by_resource_group(resource_group_name=self.resource_group):
                if self.has_tags(item.tags, self.tags):
                    results.append(cluster_to_dict(item))
        except HttpResponseError as exc:
            self.fail("Error listing Azure Managed Redis clusters in resource group {0}: {1}".format(self.resource_group, str(exc)))
        return results

    def list_all(self):
        self.log("List Azure Managed Redis clusters in the current subscription")
        results = []
        try:
            for item in self.redisenterprise_client.redis_enterprise.list():
                if self.has_tags(item.tags, self.tags):
                    results.append(cluster_to_dict(item))
        except HttpResponseError as exc:
            self.fail("Error listing Azure Managed Redis clusters in the current subscription: {0}".format(str(exc)))
        return results


def main():
    """Main execution"""
    AzureRMManagedRedisInfo()


if __name__ == '__main__':
    main()
