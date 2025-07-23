#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_sqlmanagedinstance
version_added: '1.14.0'
short_description: Manage SQL managed instances
description:
    - Create, update, or delete SQL managed instances.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: True
    name:
        description:
            - The name of the sql managed instance.
        type: str
        required: True
    location:
        description:
            - The location of the sql managed instance.
        type: str
    sku:
        description:
            - An ARM Resource SKU.
        type: dict
        suboptions:
            name:
                description:
                    - The name of the SKU, typically, a letter add Number code.
                type: str
            tier:
                description:
                    - The tier or edition of the particular SKU.
                type: str
            size:
                description:
                    - Size of the particular SKU.
                type: str
            family:
                description:
                    - If the service has different generations of hardware, for the same SKU, then that can be captured here.
                type: str
            capacity:
                description:
                    - The capacity of the managed instance in integer number of vcores.
                type: str
    administrators:
        description:
            - The Azure Active Directory administrator of the server.
        type: str
    managed_instance_create_mode:
        description:
            - Specifies the mode of database creation.
        type: str
    administrator_login:
        description:
            - Administrator username for the managed instance.
            - Can only be specified when the managed instance is being created (and is required for creation).
        type: str
    administrator_login_password:
        description:
            - The administrator login password (required for managed instance creation).
        type: str
    subnet_id:
        description:
            - Subnet resource ID for the managed instance.
        type: str
    license_type:
        description:
            - The license type.
            - Possible values are C(LicenseIncluded) and C(BasePrice).
            - Discounted AHB price for bringing your own SQL licenses.
            - Regular price inclusive of a new SQL license.
        type: str
        choices:
            - LicenseIncluded
            - BasePrice
    v_cores:
        description:
            - The number of vCores.
        type: int
        choices:
            - 8
            - 16
            - 24
            - 32
            - 40
            - 64
            - 80
    storage_size_in_gb:
        description:
            - Storage size in GB.
            - Minimum value is C(32). Maximum value is C(8192).
            - Increments of 32 GB allowed only.
        type: int
    collation:
        description:
            - Collation of the managed instance.
        type: str
    dns_zone:
        description:
            - The Dns Zone that the managed instance is in.
        type: str
    dns_zone_partner:
        description:
            - The resource ID of another managed instance whose DNS zone this managed instance will share after creation.
        type: str
    public_data_endpoint_enabled:
        description:
            - Whether or not the public data endpoint is enabled.
        type: bool
    source_managed_instance_id:
        description:
            - The resource identifier of the source managed instance associated with create operation of this instance.
        type: str
    restore_point_in_time:
        description:
            -  Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database.
        type: str
    proxy_override:
        description:
            - Connection type used for connecting to the instance.
        type: str
        choices:
            - Proxy
            - Redirect
            - Default
    timezone_id:
        description:
            - ID of the timezone.
            - Allowed values are timezones supported by Windows.
            - Windows keeps details on supported timezones.
        type: str
    instance_pool_id:
        description:
            - The ID of the instance pool this managed server belongs to.
        type: str
    private_endpoint_connections:
        description:
            - List of private endpoint connections on a managed instance.
        type: list
        elements: str
    maintenance_configuration_id:
        description:
            - Specifies maintenance configuration ID to apply to this managed instance.
        type: str
    minimal_tls_version:
        description:
            - Minimal TLS version. Allowed values C(None), C(1.0), C(1.1), C(1.2).
        type: str
        choices:
            - 'None'
            - '1.0'
            - '1.1'
            - '1.2'
    storage_account_type:
        description:
            - The storage account type used to store backups for this instance.
        type: str
    zone_redundant:
        description:
            - Whether or not the multi-az is enabled.
        type: bool
    primary_user_assigned_identity_id:
        description:
            - The resource id of a user assigned identity to be used by default.
        type: str
    key_id:
        description:
            - A CMK URI of the key to use for encryption.
        type: str
    state:
        description:
            - State of the sql managed instance.
            - Use C(present) to create or update a automation runbook and use C(absent) to delete.
        type: str
        default: present
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
    - azure.azcollection.azure_identity_multiple

author:
    - xuzhang3 (@xuzhang3)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Create sql managed instance
  azure_rm_sqlmanagedinstance:
    resource_group: "{{ resource_group }}"
    name: testmanagedinstance
    subnet_id: subnet_id
    sku:
      name: GP_Gen5
      tier: GeneralPurpose
      family: Gen5
      capacity: 5
    identity:
      type: SystemAssigned
    administrator_login: azureuser
    administrator_login_password: "{{ password }}"
    storage_size_in_gb: 256
    v_cores: 8

- name: Delete sql managed instance
  azure_rm_sqlmanagedinstance:
    resource_group: "{{ resource_group }}"
    name: testmanagedinstance
    state: absent
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
                - SQL managed instance name.
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
                - The resource ID of another managed instance whose DNS zone this managed instance will share after creation.
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
                - The resource id of a user assigned identity to be used by default.
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
                -  Id of the timezone. Allowed values are timezones supported by Windows.
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

# from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.mgmt.sql.models import (ResourceIdentity, UserIdentity)
    from azure.core.polling import LROPoller
except ImportError:
    pass


sku_spec = dict(
    name=dict(type='str'),
    tier=dict(type='str'),
    size=dict(type='str'),
    family=dict(type='str'),
    capacity=dict(type='str')
)


user_assigned_identities_spec = dict(
    id=dict(
        type='list',
        default=[],
        elements='str'
    )
)


# class AzureRMSqlManagedInstance(AzureRMModuleBase):
class AzureRMSqlManagedInstance(AzureRMModuleBaseExt):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
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
            subnet_id=dict(
                type='str'
            ),
            identity=dict(
                type='dict',
                options=self.managed_identity_multiple_spec
            ),
            sku=dict(
                type='dict',
                options=sku_spec
            ),
            managed_instance_create_mode=dict(
                type='str'
            ),
            administrator_login=dict(
                type='str',
            ),
            administrator_login_password=dict(
                type='str',
                no_log=True,
            ),
            license_type=dict(
                type='str',
                choices=['LicenseIncluded', 'BasePrice']
            ),
            v_cores=dict(
                type='int',
                choices=[8, 16, 24, 32, 40, 64, 80]
            ),
            storage_size_in_gb=dict(
                type='int'
            ),
            collation=dict(
                type='str'
            ),
            dns_zone=dict(
                type='str'
            ),
            dns_zone_partner=dict(
                type='str'
            ),
            public_data_endpoint_enabled=dict(
                type='bool'
            ),
            source_managed_instance_id=dict(
                type='str'
            ),
            restore_point_in_time=dict(
                type='str'
            ),
            proxy_override=dict(
                type='str',
                choices=['Proxy', 'Redirect', 'Default']
            ),
            timezone_id=dict(
                type='str'
            ),
            instance_pool_id=dict(
                type='str'
            ),
            maintenance_configuration_id=dict(
                type='str'
            ),
            private_endpoint_connections=dict(
                type='list',
                elements='str'
            ),
            minimal_tls_version=dict(
                type='str',
                choices=['None', '1.0', '1.1', '1.2']
            ),
            storage_account_type=dict(
                type='str'
            ),
            zone_redundant=dict(
                type='bool'
            ),
            primary_user_assigned_identity_id=dict(
                type='str'
            ),
            key_id=dict(
                type='str'
            ),
            administrators=dict(
                type='str'
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                default='present'
            )
        )
        # store the results of the module operation
        self.results = dict(changed=False)
        self.resource_group = None
        self.name = None
        self.location = None
        self.state = None
        self.identity = None
        self.body = dict()
        self._managed_identity = None

        super(AzureRMSqlManagedInstance, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    @property
    def managed_identity(self):
        if not self._managed_identity:
            self._managed_identity = {"identity": ResourceIdentity,
                                      "user_assigned": UserIdentity
                                      }
        return self._managed_identity

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_parameters(self.module_arg_spec, self.body, 0)

        if not self.location:
            resource_group = self.get_resource_group(self.resource_group)
            self.location = resource_group.location
        self.body['location'] = self.location

        sql_managed_instance = self.get()

        update_identity, identity = self.update_managed_identity(new_identity=self.identity or {},
                                                                 curr_identity=sql_managed_instance and
                                                                 sql_managed_instance.get('identity', {}) or {})
        if update_identity:
            self.body["identity"] = identity.as_dict()

        changed = False
        if self.state == 'present':
            if sql_managed_instance:
                modifiers = {}
                self.create_compare_modifiers(self.module_arg_spec, '', modifiers)
                self.results['modifiers'] = modifiers
                self.results['compare'] = []
                if not self.default_compare(modifiers, self.body, sql_managed_instance, '', self.results):
                    changed = True

                if changed or update_identity:
                    if not self.check_mode:
                        # sql_managed_instance = self.update_sql_managed_instance(self.body)
                        sql_managed_instance = self.create_or_update(self.body)
            else:
                changed = True
                if not self.check_mode:
                    sql_managed_instance = self.create_or_update(self.body)

        else:
            changed = True
            if not self.check_mode:
                sql_managed_instance = self.delete_sql_managed_instance()

        self.results['changed'] = changed
        self.results['state'] = sql_managed_instance
        return self.results

    def get(self):
        try:
            response = self.sql_client.managed_instances.get(self.resource_group, self.name)
            return self.to_dict(response)
        except ResourceNotFoundError:
            pass

    def update_sql_managed_instance(self, parameters):
        try:
            response = self.sql_client.managed_instances.begin_update(resource_group_name=self.resource_group,
                                                                      managed_instance_name=self.name,
                                                                      parameters=parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
            return self.to_dict(response)
        except Exception as exc:
            self.fail('Error when updating SQL managed instance {0}: {1}'.format(self.name, exc.message))

    def create_or_update(self, parameters):
        try:
            response = self.sql_client.managed_instances.begin_create_or_update(resource_group_name=self.resource_group,
                                                                                managed_instance_name=self.name,
                                                                                parameters=parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
            return self.to_dict(response)
        except Exception as exc:
            self.fail('Error when creating SQL managed instance {0}: {1}'.format(self.name, exc))

    def delete_sql_managed_instance(self):
        try:
            response = self.sql_client.managed_instances.begin_delete(self.resource_group, self.name)
            if isinstance(response, LROPoller):
                self.get_poller_result(response)

        except Exception as exc:
            self.fail('Error when deleting SQL managed instance {0}: {1}'.format(self.name, exc))

    def to_dict(self, item):
        if not item:
            return None
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
    AzureRMSqlManagedInstance()


if __name__ == '__main__':
    main()
