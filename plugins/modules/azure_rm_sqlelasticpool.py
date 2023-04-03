#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_sqlelasticpool
version_added: "1.14.0"
short_description: Manage SQL Elastic Pool instance
description:
    - Create, update and delete instance of SQL Elastic Pool.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource.
            - You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
        type: str
    server_name:
        description:
            - The name of the server.
        required: True
        type: str
    name:
        description:
            - The name of the elastic pool to be operated on (updated or created).
        required: True
        type: str
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
        type: str
    sku:
        description:
            - The sku of the elastic pool. The Elastic PoolEditions enumeration contains all the valid sku.
        type: dict
        suboptions:
            name:
                description:
                    - Name of the elastic pool SKU, typically, a letter + Number code, e.g. P3
                required: True
                type: str
            tier:
                description:
                    - The tier or edition of the particular SKU, e.g. Basic, Premium
                type: str
            capacity:
                description:
                    - Capacity of the particular SKU.
                type: int
            size:
                description:
                    - Size of the particular SKU
                type: str
            family:
                description:
                    - If the service has different generations of hardware, for the same SKU, then that can be used here
                type: str
    max_size_bytes:
        description:
            - The max size of the elasticpool expressed in bytes.
            - If not I(create_mode=default), this value is ignored.
            - To see possible values, query the capabilities API (/subscriptions/{subscriptionId}/providers/Microsoft.Sql/locations/{locationID}/capabilities).
              referred to by operationId:'Capabilities_ListByLocation'.
        type: str
    zone_redundant:
        description:
            - Is this elasticpool is zone redundant? It means the replicas of this elasticpool will be spread across multiple availability zones.
        type: bool
        default: False
    per_elasticpool_settings:
        description:
            - The per database settings for the elastic pool.
        type: dict
        suboptions:
            min_capacity:
                description:
                    - The minimum capacity all databases are guaranteed.
                type: float
            max_capacity:
                description:
                    - The maximum capacity all databases are guaranteed.
                type: float
    license_type:
        description:
            - The license type to apply for this elastic pool.
        type: str
        default: LicenseIncluded
        choices:
            - LicenseIncluded
            - BasePrice
    maintenance_configuration_id:
        description:
            - Maintenance configuration id assigned to the elastic pool.
        type: str
    state:
        description:
            - Assert the state of the SQL Elastic Pool. Use C(present) to create or update an SQL Elastic Pool and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
  - name: Create (or update) SQL Elastic Pool
    azure_rm_elastic_pool:
      resource_group: myResourceGroup
      server_name: sqlcrudtest-5961
      name: testEP
      zone_redundant: False
      sku:
        name: GP_Gen5
        family: Gen5
        capacity: 3
      tags:
        key1: value1

  - name: Delete SQL Elastic Pool
    azure_rm_elastic_pool:
      resource_group: myResourceGroup
      server_name: sqlcrudtest-5961
      name: testEP
      state: absent
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

import time
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass

sku_spec = dict(
    name=dict(type='str', required=True),
    tier=dict(type='str'),
    size=dict(type='str'),
    family=dict(type='str'),
    capacity=dict(type='int')
)


per_elasticpool_settings_spec = dict(
    min_capacity=dict(type='float'),
    max_capacity=dict(type='float')
)


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMSqlElasticPool(AzureRMModuleBase):
    """Configuration class for an Azure RM SQL Elastic Pool resource"""

    def __init__(self):
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
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict',
                options=sku_spec
            ),
            max_size_bytes=dict(
                type='str'
            ),
            zone_redundant=dict(
                type='bool',
                default=False
            ),
            per_elasticpool_settings=dict(
                type='dict',
                options=per_elasticpool_settings_spec
            ),
            maintenance_configuration_id=dict(
                type='str'
            ),
            license_type=dict(
                type='str',
                default="LicenseIncluded",
                choices=["LicenseIncluded", "BasePrice"]
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.name = None
        self.location = None
        self.sku = None
        self.max_size_bytes = None
        self.zone_redundant = None
        self.per_elasticpool_settings = None
        self.maintenance_configuration_id = None
        self.body = dict()

        self.results = dict(changed=False)
        self.to_do = Actions.NoAction

        super(AzureRMSqlElasticPool, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])
            if key not in ['resource_group', 'server_name', 'name', 'state']:
                self.body[key] = kwargs[key]

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        old_response = None
        response = None

        old_response = self.get_elastic_pool()

        if not old_response:
            self.log("SQL Elastic Pool instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("SQL Elastic Pool instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log(
                    "Need to check if SQL Elastic Pool instance has to be deleted or may be updated")
                if self.per_elasticpool_settings is not None and (self.body['per_elasticpool_settings'] != old_response['per_elasticpool_settings']):
                    self.to_do = Actions.Update
                if self.maintenance_configuration_id and (self.body['maintenance_configuration_id'] != old_response['maintenance_configuration_id']):
                    self.to_do = Actions.Update
                if self.license_type is not None and (self.body['license_type'] != old_response['license_type']):
                    self.to_do = Actions.Update
                if self.zone_redundant is not None and (bool(self.body['zone_redundant']) != bool(old_response['zone_redundant'])):
                    self.to_do = Actions.Update
                if self.max_size_bytes is not None and (self.body['max_size_bytes'] != old_response['max_size_bytes']):
                    self.to_do = Actions.Update
                if self.sku is not None:
                    for key in self.sku.keys():
                        if self.sku[key] is not None and (self.sku[key] != old_response['sku'][key]):
                            self.to_do = Actions.Update
                        else:
                            self.sku[key] = old_response['sku'][key]
                update_tags, newtags = self.update_tags(old_response.get('tags', dict()))
                if update_tags:
                    self.body['tags'] = newtags
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the SQL Elastic Pool instance")

            self.results['changed'] = True

            if self.check_mode:
                return self.results

            if self.to_do == Actions.Create:
                self.body['location'] = self.location
                response = self.create_elastic_pool(self.body)
            else:
                response = self.update_elastic_pool(self.body)

        elif self.to_do == Actions.Delete:
            self.log("SQL Elastic Pool instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_elastic_pool()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_elastic_pool():
                time.sleep(20)
        else:
            self.log("SQL Elastic Pool instance unchanged")
            self.results['changed'] = False
            response = old_response

        self.results['elastic_pool'] = response

        return self.results

    def update_elastic_pool(self, parameters):
        '''
        Creates or updates SQL Elastic Pool with the specified configuration.

        :return: deserialized SQL Elastic Pool instance state dictionary
        '''
        self.log(
            "Creating / Updating the SQL Elastic Pool instance {0}".format(self.name))

        try:
            response = self.sql_client.elastic_pools.begin_update(resource_group_name=self.resource_group,
                                                                  server_name=self.server_name,
                                                                  elastic_pool_name=self.name,
                                                                  parameters=parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.log('Error attempting to create the SQL Elastic Pool instance.')
            self.fail(
                "Error creating the SQL Elastic Pool instance: {0}".format(str(exc)))
        return self.format_item(response)

    def create_elastic_pool(self, parameters):
        '''
        Creates or updates SQL Elastic Pool with the specified configuration.

        :return: deserialized SQL Elastic Pool instance state dictionary
        '''
        self.log(
            "Creating / Updating the SQL Elastic Pool instance {0}".format(self.name))

        try:
            response = self.sql_client.elastic_pools.begin_create_or_update(resource_group_name=self.resource_group,
                                                                            server_name=self.server_name,
                                                                            elastic_pool_name=self.name,
                                                                            parameters=parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.log('Error attempting to create the SQL Elastic Pool instance.')
            self.fail(
                "Error creating the SQL Elastic Pool instance: {0}".format(str(exc)))
        return self.format_item(response)

    def delete_elastic_pool(self):
        '''
        Deletes specified SQL Elastic Pool instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the SQL Elastic Pool instance {0}".format(self.name))
        try:
            response = self.sql_client.elastic_pools.begin_delete(resource_group_name=self.resource_group,
                                                                  server_name=self.server_name,
                                                                  elastic_pool_name=self.name)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as e:
            self.log('Error attempting to delete the SQL Elastic Pool instance.')
            self.fail(
                "Error deleting the SQL Elastic Pool instance: {0}".format(str(e)))

        return True

    def get_elastic_pool(self):
        '''
        Gets the properties of the specified SQL Elastic Pool.

        :return: deserialized SQL Elastic Pool instance state dictionary
        '''
        found = False
        try:
            response = self.sql_client.elastic_pools.get(resource_group_name=self.resource_group,
                                                         server_name=self.server_name,
                                                         elastic_pool_name=self.name)
            found = True
        except ResourceNotFoundError:
            self.log('Did not find the SQL Elastic Pool instance.')
        if found is True:
            return self.format_item(response)

        return False

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
    """Main execution"""
    AzureRMSqlElasticPool()


if __name__ == '__main__':
    main()
