#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_sqlmanagedinstance_info
version_added: "0.15.0"
short_description: Get Azure SQL managed instance facts
description:
    - Get facts of Azure SQL manged instance facts.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource.
        type: str
    name:
        description:
            - The name of the SQL managed instance.
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
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
  - name: Get SQL managed instance by name
    azure_rm_sqlmanagedinstance_info:
      resource_group: testrg
      name: testinstancename

  - name: List SQL managed instance by resource group
    azure_rm_sqlmanagedinstance_info:
      resource_group: testrg

  - name: List SQL manged instance by subscription and filter by tags
    azure_rm_sqlmanagedinstance_info:
      tags:
        - foo
'''

RETURN = '''
sql_managed_instance:
    description:
        - A list of dictionaries containing facts for SQL Managed Instance.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscription/xxx-xxx/resourceGroups/testRG/providers/Microsoft.Sql/managedInstances/fredsqlinstance"
        name:
            description:
                - SQL manged instance name.
            returned: always
            type: str
            sample: testmanagedinstance
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
        identity:
            description:
                - Azure Active Directory identity configuration for a resource.
            returned: always
            type: complex
            contains:
                principal_id:
                    description:
                        - The Azure Active Directory principal ID.
                    type: str
                    returned: always
                    sample: 895c-xxx-xxxbe
                tenant_id:
                    description:
                        - The Azure Active Directory tenant ID.
                    type: str
                    returned: always
                    sample: 72fxxxxx-xxxx-xxxx-xxxx-xxxxxx11db47
                type:
                    description:
                        - The identity type.
                    type: str
                    returned: always
                    sample: SystemAssigned
                user_assigned_identities:
                    description:
                        - The resource ids of the user assigned identities to use.
                    type: str
                    returned: always
                    sample: null
        sku:
            description:
                - An ARM Resource SKU.
            returned: always
            type: complex
            contains:
                name:
                    description:
                        - The name of the SKU.
                    returned: always
                    type: str
                    sample: BC_Gen4_2
                tier:
                    description:
                        - The SKU tier.
                    returned: always
                    type: str
                    sample: BusinessCritical
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
        collation:
            description:
                - The collation of the SQL managed instance.
            returned: always
            type: str
            sample: SQL_Latin1_General_CP1_CI_AS
        administrator_login:
            description:
                - Administrator username for the managed instance.
            type: str
            returned: always
            sample: azureuser
        administrators:
            description:
                - The Azure Active Directory administrator of the server.
            type: str
            returned: always
            sample: null
        dns_zone:
            description:
                -The Dns Zone that the managed instance is in.
            type: str
            returned: always
            sample: 8a23abba54cd
        dns_zone_partner:
            description:
                - The resource id of another managed instance whose DNS zone this managed instance will share after creation.
            type: str
            returned: always
            sample: null
        fully_qualified_domain_name:
            description:
                - The fully qualified domain name of the managed instance.
            type: str
            returned: always
            sample: fredsqlinstance.8a23abba54cd.database.windows.net
        instance_pool_id:
            description:
                - The ID of the instance pool this managed server belongs to.
            type: str
            returned: always
            sample: null
        key_id:
            description:
                - A CMK URI of the key to use for encryption.
            type: str
            returned: always
            sample: null
        license_type:
            description:
                - The license type.
            type: str
            returned: always
            sample: LicenseIncluded
        maintenance_configuration_id:
            description:
                - Specifies maintenance configuration ID to apply to this managed instance.
            type: str
            returned: always
            sample: /subscriptions/xxx-xxxx/providers/Microsoft.Maintenance/publicMaintenanceConfigurations/SQL_Default
        managed_instance_create_mode:
            description:
                - Specifies the mode of database creation.
            type: str
            returned: always
            sample: null
        minimal_tls_version:
            description:
                - Minimal TLS version. Allowed values 'None', '1.0', '1.1', '1.2'.
            type: str
            returned: always
            sample: 1.2
        primary_user_assigned_identity_id:
            description:
                - The resource ID of a user assigned identity to be used by default.
            type: str
            returned: always
            sample: null
        private_endpoint_connections:
            description:
                - List of private endpoint connections on a managed instance.
            type: list
            returned: always
            sample: []
        provisioning_state:
            description:
                - The Status of the SQL managed instance.
            type: str
            returned: always
            sample: Successed
        proxy_override:
            description:
                - Connection type used for connecting to the instance.
            type: str
            returned: always
            sample: Proxy
        public_data_endpoint_enabled:
            description:
                - Whether or not the public data endpoint is enabled.
            type: bool
            returned: always
            sample: false
        restore_point_in_time:
            description:
                - Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database.
            type: str
            returned: always
            sample: null
        source_managed_instance_id:
            description:
                - The resource identifier of the source managed instance associated with create operation of this instance.
            type: str
            returned: always
            sample: null
        state:
            description:
                - The state of the managed instance.
            type: str
            returned: always
            sample: Ready
        storage_account_type:
            description:
                - The storage account type used to store backups for this instance.
            type: str
            returned: always
            sample: GRS
        storage_size_in_gb:
            description:
                - Storage size in GB. Minimum value 32. Maximum value 8192.
            type: int
            returned: always
            sample: 256
        subnet_id:
            description:
                - Subnet resource ID for the managed instance.
            type: str
            returned: always
            sample: /subscriptions/xxx-xxxx/resourceGroups/testRG/providers/Microsoft.Network/virtualNetworks/vnet-smi/subnets/sqi_sub
        timezone_id:
            description:
                - ID of the timezone. Allowed values are timezones supported by Windows.
            type: str
            returned: always
            sample: UTC
        type:
            description:
                - The SQL managed instance type.
            type: str
            returned: always
            sample: "Microsoft.Sql/managedInstances"
        v_cores:
            description:
                - The number of vCores. Allowed values 8, 16, 24, 32, 40, 64, 80.
            type: int
            returned: always
            sample: 8
        zone_redundant:
            description:
                - Whether or not the multi-az is enabled.
            type: bool
            returned: always
            sample: false
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSqManagedInstanceInfo(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
            ),
            name=dict(
                type='str',
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
        self.name = None
        self.tags = None
        super(AzureRMSqManagedInstanceInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None and self.resource_group is not None:
            self.results['sql_managed_instance'] = self.get()
        elif self.resource_group is not None:
            self.results['sql_managed_instance'] = self.list_by_resource_group()
        else:
            self.results['sql_managed_instance'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.sql_client.managed_instances.get(resource_group_name=self.resource_group,
                                                             managed_instance_name=self.name)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError:
            self.log('Could not get facts for SQL managed instance.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.sql_client.managed_instances.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except Exception:
            self.fail('Could not list facts for SQL managed instance.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.sql_client.managed_instances.list()
            self.log("Response : {0}".format(response))
        except Exception:
            self.fail('Could not list facts for SQL Managed Instance.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'type': d.get('type', None),
            'tags': d.get('tags', None),
            'identity': {
                'user_assigned_identities': d.get('identity', {}).get('user_assigned_identities', None),
                'principal_id': d.get('identity', {}).get('principal_id', None),
                'type': d.get('identity', {}).get('type', None),
                'tenant_id': d.get('identity', {}).get('tenant_id', None)
            },
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'size': d.get('sku', {}).get('size', None),
                'family': d.get('sku', {}).get('family', None),
                'tier': d.get('sku', {}).get('tier', None),
                'capacity': d.get('sku', {}).get('capacity', None)
            },
            'provisioning_state': d.get('provisioning_state', None),
            'managed_instance_create_mode': d.get('managed_instance_create_mode', None),
            'fully_qualified_domain_name': d.get('fully_qualified_domain_name', None),
            'administrator_login': d.get('administrator_login', None),
            'subnet_id': d.get('subnet_id', None),
            'state': d.get('state', None),
            'license_type': d.get('license_type', None),
            'v_cores': d.get('v_cores', None),
            'storage_size_in_gb': d.get('storage_size_in_gb', None),
            'collation': d.get('collation', None),
            'dns_zone': d.get('dns_zone', None),
            'dns_zone_partner': d.get('dns_zone_partner', None),
            'public_data_endpoint_enabled': d.get('public_data_endpoint_enabled', None),
            'source_managed_instance_id': d.get('source_managed_instance_id', None),
            'restore_point_in_time': d.get('restore_point_in_time', None),
            'proxy_override': d.get('proxy_override', None),
            'timezone_id': d.get('timezone_id', None),
            'instance_pool_id': d.get('instance_pool_id', None),
            'maintenance_configuration_id': d.get('maintenance_configuration_id', None),
            'private_endpoint_connections': d.get('private_endpoint_connections', None),
            'minimal_tls_version': d.get('minimal_tls_version', None),
            'storage_account_type': d.get('storage_account_type', None),
            'zone_redundant': d.get('zone_redundant', None),
            'primary_user_assigned_identity_id': d.get('primary_user_assigned_identity_id', None),
            'key_id': d.get('key_id', None),
            'administrators': d.get('administrators', None)
        }
        return d


def main():
    AzureRMSqManagedInstanceInfo()


if __name__ == '__main__':
    main()
