#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_sqlelasticpool_info
version_added: "1.14.0"
short_description: Get Azure SQL Elastic Pool facts
description:
    - Get facts of Azure SQL Elastic Pool.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource.
            - You can obtain this value from the Azure Resource Manager API or the portal.
        type: str
        required: True
    server_name:
        description:
            - The name of the server.
        type: str
        required: True
    name:
        description:
            - The name of the elastic pool.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred Sun (@Fred-sun)

'''

EXAMPLES = '''
  - name: Get instance of SQL Elastic Pool
    azure_rm_sqlelasticpool_info:
      resource_group: testrg
      server_name: testserver
      name: testEP

  - name: List instances of SQL Elastic Pool
    azure_rm_sqlelasticpool_info:
      resource_group: testrg
      server_name: testserver
'''

RETURN = '''
elastic_pool:
    description:
        - A list of dictionaries containing facts for SQL Elastic Pool.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/testrg/providers/Microsoft.Sql/servers/sqlsrvfredsqldb/elasticPools/fedelastic01
        name:
            description:
                - Elastic Pool name.
            returned: always
            type: str
            sample: testEP
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: eastus
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: { 'taga':'aaa', 'tagb':'bbb' }
        sku:
            description:
                - The name and tier of the SKU.
            returned: always
            type: complex
            contains:
                name:
                    description:
                        - The name of the SKU.
                    returned: always
                    type: str
                    sample: GP_Gen5
                tier:
                    description:
                        - The SKU tier.
                    returned: always
                    type: str
                    sample: GeneralPurpose
                capacity:
                    description:
                        - The SKU capacity.
                    returned: always
                    type: int
                    sample: 2
                family:
                    description:
                        - If the service has different generations of hardware, for the same SKU, then that can be captured here.
                    type: str
                    returned: always
                    sample: Gen5
                size:
                    description:
                        - Size of the particular SKU.
                    type: str
                    returned: always
                    sample: null
        zone_redundant:
            description:
                - Whether or not this database is zone redundant, which means the replicas of this database will be spread across multiple availability zones.
            returned: always
            type: bool
            sample: true
        license_type:
            description:
                - The license type to apply for this elastic pool.
            type: str
            returned: always
            sample: LicenseIncluded
        maintenance_configuration_id:
            description:
                -  Maintenance configuration id assigned to the elastic pool.
            type: str
            returned: always
            sample: /subscriptions/xxx-xxx/providers/Microsoft.Maintenance/publicMaintenanceConfigurations/SQL_Default
        max_size_bytes:
            description:
                - The storage limit for the database elastic pool in bytes.
            type: str
            returned: always
            sample: 34359738368
        per_database_settings:
            description:
                - The per database settings for the elastic pool.
            type: complex
            returned: always
            contains:
                min_capacity:
                    description:
                        - The minimum capacity all databases are guaranteed
                    type: float
                    returned: always
                    sample: 0.0
                max_capacity:
                    description:
                        - The maximum capacity any one database can consume.
                    type: float
                    returned: always
                    sample: 2.0
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSqlElasticPoolInfo(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            tags=dict(
                type='list',
                elements='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.server_name = None
        self.name = None
        self.tags = None
        super(AzureRMSqlElasticPoolInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results['elastic_pool'] = self.get()
        else:
            self.results['elastic_pool'] = self.list_by_server()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.sql_client.elastic_pools.get(resource_group_name=self.resource_group,
                                                         server_name=self.server_name,
                                                         elastic_pool_name=self.name)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError:
            self.log('Could not get facts for Elastic Pool.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_server(self):
        response = None
        results = []
        try:
            response = self.sql_client.elastic_pools.list_by_server(resource_group_name=self.resource_group,
                                                                    server_name=self.server_name)
            self.log("Response : {0}".format(response))
        except Exception:
            self.fail('Could not get facts for elastic pool.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        if not item:
            return None

        d = dict(
            resource_group=self.resource_group,
            id=item.id,
            name=item.name,
            location=item.location,
            tags=item.tags,
            max_size_bytes=item.max_size_bytes,
            zone_redundant=item.zone_redundant,
            license_type=item.license_type,
            maintenance_configuration_id=item.maintenance_configuration_id,
            per_database_settings=dict(),
            sku=dict()
        )

        if item.sku is not None:
            d['sku']['name'] = item.sku.name
            d['sku']['tier'] = item.sku.tier
            d['sku']['size'] = item.sku.size
            d['sku']['family'] = item.sku.family
            d['sku']['capacity'] = item.sku.capacity
        if item.per_database_settings is not None:
            d['per_database_settings']['min_capacity'] = item.per_database_settings.min_capacity
            d['per_database_settings']['max_capacity'] = item.per_database_settings.max_capacity

        return d


def main():
    AzureRMSqlElasticPoolInfo()


if __name__ == '__main__':
    main()
