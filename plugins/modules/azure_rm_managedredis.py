#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang, (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_managedredis
version_added: "4.2.0"
short_description: Manage an Azure Managed Redis cluster
description:
    - Create, update and delete an Azure Managed Redis cluster (C(Microsoft.Cache/redisEnterprise)).
    - Databases inside the cluster are managed separately.

options:
    resource_group:
        description:
            - The name of the resource group to which the cluster belongs.
        required: True
        type: str
    name:
        description:
            - The name of the Azure Managed Redis cluster.
        required: True
        type: str
    location:
        description:
            - Azure Resource location. If not set, location from the resource group will be used as default.
            - Cannot be changed after the cluster has been created.
        type: str
    sku:
        description:
            - The SKU of the cluster, which affects price, performance, and features.
            - Required when I(state=present).
            - Scaling between the C(FlashOptimized) tier and the C(Balanced), C(MemoryOptimized) or C(ComputeOptimized) tiers is not supported,
              and scaling down is only possible to a subset of smaller SKUs.
            - Changing the SKU of an existing cluster requires the cluster to have a database.
        type: str
        choices:
            - Balanced_B0
            - Balanced_B1
            - Balanced_B3
            - Balanced_B5
            - Balanced_B10
            - Balanced_B20
            - Balanced_B50
            - Balanced_B100
            - Balanced_B150
            - Balanced_B250
            - Balanced_B350
            - Balanced_B500
            - Balanced_B700
            - Balanced_B1000
            - MemoryOptimized_M10
            - MemoryOptimized_M20
            - MemoryOptimized_M50
            - MemoryOptimized_M100
            - MemoryOptimized_M150
            - MemoryOptimized_M250
            - MemoryOptimized_M350
            - MemoryOptimized_M500
            - MemoryOptimized_M700
            - MemoryOptimized_M1000
            - MemoryOptimized_M1500
            - MemoryOptimized_M2000
            - ComputeOptimized_X3
            - ComputeOptimized_X5
            - ComputeOptimized_X10
            - ComputeOptimized_X20
            - ComputeOptimized_X50
            - ComputeOptimized_X100
            - ComputeOptimized_X150
            - ComputeOptimized_X250
            - ComputeOptimized_X350
            - ComputeOptimized_X500
            - ComputeOptimized_X700
            - FlashOptimized_A250
            - FlashOptimized_A500
            - FlashOptimized_A700
            - FlashOptimized_A1000
            - FlashOptimized_A1500
            - FlashOptimized_A2000
            - FlashOptimized_A4500
    high_availability:
        description:
            - Whether the data set is replicated.
            - Disabling high availability affects the availability SLA and increases the risk of data loss.
            - The service enables high availability when not specified at creation.
            - High availability can be enabled on an existing cluster, but cannot be disabled after the cluster has been created.
            - Enabling high availability on an existing cluster requires the cluster to have a database.
        type: str
        choices:
            - Enabled
            - Disabled
    minimum_tls_version:
        description:
            - The minimum TLS version for the cluster to support.
            - Azure Managed Redis only supports TLS 1.2 and later.
        type: str
        choices:
            - '1.2'
    public_network_access:
        description:
            - Whether public network traffic can access the cluster.
            - Required when creating a new cluster.
        type: str
        choices:
            - Enabled
            - Disabled
    encryption:
        description:
            - Encryption-at-rest configuration for the cluster.
            - When set, the whole block is sent to the service as given.
        type: dict
        suboptions:
            customer_managed_key_encryption:
                description:
                    - Customer-managed key settings.
                type: dict
                suboptions:
                    key_encryption_key_url:
                        description:
                            - Versioned key encryption key URL.
                            - For example C(https://contosovault.vault.azure.net/keys/contosokek/562a4bb76b524a1493a6afe8e536ee78).
                        type: str
                    key_encryption_key_identity:
                        description:
                            - Identity used to authenticate to Key Vault.
                        type: dict
                        suboptions:
                            identity_type:
                                description:
                                    - Type of the identity used to access the key encryption key.
                                    - Only C(userAssignedIdentity) is supported by the current API version.
                                type: str
                                choices:
                                    - userAssignedIdentity
                            user_assigned_identity_resource_id:
                                description:
                                    - Resource ID of the user assigned identity used to access the key encryption key URL.
                                type: str
    state:
        description:
            - Assert the state of the cluster.
            - Use C(present) to create or update a cluster and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
    - azure.azcollection.azure_identity_multiple

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Create an Azure Managed Redis cluster
  azure_rm_managedredis:
    resource_group: myResourceGroup
    name: myredis
    location: eastus
    sku: Balanced_B1
    public_network_access: Disabled
    minimum_tls_version: '1.2'
    tags:
      env: test

- name: Create a cluster with customer-managed key encryption
  azure_rm_managedredis:
    resource_group: myResourceGroup
    name: myredis
    sku: MemoryOptimized_M10
    public_network_access: Disabled
    identity:
      type: UserAssigned
      user_assigned_identities:
        id:
          - /subscriptions/xxxx/resourceGroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myuai
    encryption:
      customer_managed_key_encryption:
        key_encryption_key_url: https://mykeyvault.vault.azure.net/keys/mykey/562a4bb76b524a1493a6afe8e536ee78
        key_encryption_key_identity:
          identity_type: userAssignedIdentity
          user_assigned_identity_resource_id: /subscriptions/xxxx/resourceGroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myuai

- name: Scale the cluster to a larger SKU
  azure_rm_managedredis:
    resource_group: myResourceGroup
    name: myredis
    sku: Balanced_B3

- name: Delete the cluster
  azure_rm_managedredis:
    resource_group: myResourceGroup
    name: myredis
    state: absent
'''

RETURN = '''
id:
    description:
        - The Azure Resource Manager resource ID for the cluster.
    returned: when the cluster exists or has been created
    type: str
    sample: /subscriptions/xxxx-xxxx/resourceGroups/myResourceGroup/providers/Microsoft.Cache/redisEnterprise/myredis
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.polling import LROPoller
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.redisenterprise.models import (
        Cluster, ClusterUpdate, Sku, ManagedServiceIdentity, UserAssignedIdentity,
        ClusterPropertiesEncryption, ClusterPropertiesEncryptionCustomerManagedKeyEncryption,
        ClusterPropertiesEncryptionCustomerManagedKeyEncryptionKeyIdentity,
    )
except ImportError:
    # This is handled in azure_rm_common
    pass


SKU_CHOICES = [
    'Balanced_B0', 'Balanced_B1', 'Balanced_B3', 'Balanced_B5', 'Balanced_B10', 'Balanced_B20', 'Balanced_B50',
    'Balanced_B100', 'Balanced_B150', 'Balanced_B250', 'Balanced_B350', 'Balanced_B500', 'Balanced_B700',
    'Balanced_B1000',
    'MemoryOptimized_M10', 'MemoryOptimized_M20', 'MemoryOptimized_M50', 'MemoryOptimized_M100',
    'MemoryOptimized_M150', 'MemoryOptimized_M250', 'MemoryOptimized_M350', 'MemoryOptimized_M500',
    'MemoryOptimized_M700', 'MemoryOptimized_M1000', 'MemoryOptimized_M1500', 'MemoryOptimized_M2000',
    'ComputeOptimized_X3', 'ComputeOptimized_X5', 'ComputeOptimized_X10', 'ComputeOptimized_X20',
    'ComputeOptimized_X50', 'ComputeOptimized_X100', 'ComputeOptimized_X150', 'ComputeOptimized_X250',
    'ComputeOptimized_X350', 'ComputeOptimized_X500', 'ComputeOptimized_X700',
    'FlashOptimized_A250', 'FlashOptimized_A500', 'FlashOptimized_A700', 'FlashOptimized_A1000',
    'FlashOptimized_A1500', 'FlashOptimized_A2000', 'FlashOptimized_A4500',
]


def _build_encryption(payload):
    if not payload:
        return None
    cmk = payload.get('customer_managed_key_encryption')
    if not cmk:
        return None
    kek_identity = None
    identity = cmk.get('key_encryption_key_identity')
    if identity:
        kek_identity = ClusterPropertiesEncryptionCustomerManagedKeyEncryptionKeyIdentity(
            identity_type=identity.get('identity_type'),
            user_assigned_identity_resource_id=identity.get('user_assigned_identity_resource_id'),
        )
    return ClusterPropertiesEncryption(
        customer_managed_key_encryption=ClusterPropertiesEncryptionCustomerManagedKeyEncryption(
            key_encryption_key_identity=kek_identity,
            key_encryption_key_url=cmk.get('key_encryption_key_url'),
        ),
    )


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMManagedRedis(AzureRMModuleBaseExt):
    """Configuration class for an Azure Managed Redis cluster"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            sku=dict(type='str', choices=SKU_CHOICES),
            high_availability=dict(type='str', choices=['Enabled', 'Disabled']),
            minimum_tls_version=dict(type='str', choices=['1.2']),
            public_network_access=dict(type='str', choices=['Enabled', 'Disabled']),
            identity=dict(
                type='dict',
                options=self.managed_identity_multiple_spec,
            ),
            encryption=dict(
                type='dict',
                options=dict(
                    customer_managed_key_encryption=dict(
                        type='dict',
                        no_log=False,
                        options=dict(
                            key_encryption_key_url=dict(type='str', no_log=False),
                            key_encryption_key_identity=dict(
                                type='dict',
                                no_log=False,
                                options=dict(
                                    identity_type=dict(type='str', choices=['userAssignedIdentity']),
                                    user_assigned_identity_resource_id=dict(type='str'),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.sku = None
        self.high_availability = None
        self.minimum_tls_version = None
        self.public_network_access = None
        self.identity = None
        self.encryption = None
        self.state = None
        self.tags = None

        self.results = dict(changed=False)
        self.to_do = Actions.NoAction
        self._managed_identity = None

        required_if = [
            ('state', 'present', ['sku']),
        ]

        super(AzureRMManagedRedis, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=True,
            required_if=required_if,
        )

    @property
    def managed_identity(self):
        if not self._managed_identity:
            self._managed_identity = {"identity": ManagedServiceIdentity,
                                      "user_assigned": UserAssignedIdentity}
        return self._managed_identity

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = self.get_instance()
        if old_response:
            self.results['id'] = old_response.get('id')

        identity_result = None
        update_identity = False
        if self.state == 'present' and self.identity:
            curr_identity = old_response.get('identity') if old_response else None
            update_identity, identity_result = self.update_managed_identity(new_identity=self.identity,
                                                                            curr_identity=curr_identity,
                                                                            patch_support=True)
            if not (self.identity.get('user_assigned_identities') or {}).get('append', True):
                curr_ids = set(((curr_identity or {}).get('user_assigned_identities') or {}).keys())
                new_ids = set((self.identity.get('user_assigned_identities') or {}).get('id') or [])
                if curr_ids - new_ids:
                    update_identity = True

        new_tags = None
        response = None
        if not old_response:
            if self.state == 'absent':
                self.log("Azure Managed Redis cluster {0} does not exist".format(self.name))
            else:
                if not self.public_network_access:
                    self.fail("public_network_access is required when creating an Azure Managed Redis cluster")
                if not self.location:
                    resource_group = self.get_resource_group(self.resource_group)
                    self.location = resource_group.location
                new_tags = self.update_tags(None)[1]
                self.to_do = Actions.Create
        else:
            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                if self.location and \
                   self.location.replace(' ', '').lower() != (old_response.get('location') or '').replace(' ', '').lower():
                    self.module.warn("location cannot be changed after the Azure Managed Redis cluster has been created")

                if self.high_availability == 'Disabled' and old_response.get('high_availability') == 'Enabled':
                    self.fail("high_availability cannot be disabled after the Azure Managed Redis cluster has been created")

                update_tags, new_tags = self.update_tags(old_response.get('tags'))
                if update_tags or update_identity:
                    self.to_do = Actions.Update

                desired = dict(
                    sku=dict(name=self.sku),
                    high_availability=self.high_availability,
                    minimum_tls_version=self.minimum_tls_version,
                    public_network_access=self.public_network_access,
                    encryption=self.encryption,
                )
                current = dict((key, old_response.get(key)) for key in desired)
                compare_result = dict(compare=[])
                if not self.default_compare({}, desired, current, '', compare_result):
                    self.log("Azure Managed Redis cluster differences: {0}".format(compare_result['compare']))
                    self.to_do = Actions.Update

        if self.to_do == Actions.Create:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.create_cluster(new_tags, identity_result)
        elif self.to_do == Actions.Update:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.update_cluster(new_tags, identity_result)
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            self.delete_cluster()
        else:
            response = old_response

        if response:
            self.results['id'] = response.get('id')

        return self.results

    def create_cluster(self, tags, identity):
        self.log("Creating the Azure Managed Redis cluster {0}".format(self.name))
        parameters = Cluster(
            location=self.location,
            tags=tags,
            sku=Sku(name=self.sku),
            identity=identity,
            high_availability=self.high_availability,
            minimum_tls_version=self.minimum_tls_version,
            public_network_access=self.public_network_access,
            encryption=_build_encryption(self.encryption),
        )
        try:
            response = self.redisenterprise_client.redis_enterprise.begin_create(
                resource_group_name=self.resource_group,
                cluster_name=self.name,
                parameters=parameters,
            )
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error creating the Azure Managed Redis cluster {0}: {1}".format(self.name, str(exc)))
        return response and as_attribute_dict(response, exclude_readonly=False) or self.get_instance()

    def update_cluster(self, tags, identity):
        self.log("Updating the Azure Managed Redis cluster {0}".format(self.name))
        parameters = ClusterUpdate(
            tags=tags,
            sku=Sku(name=self.sku) if self.sku else None,
            identity=identity,
            high_availability=self.high_availability,
            minimum_tls_version=self.minimum_tls_version,
            public_network_access=self.public_network_access,
            encryption=_build_encryption(self.encryption),
        )
        try:
            response = self.redisenterprise_client.redis_enterprise.begin_update(
                resource_group_name=self.resource_group,
                cluster_name=self.name,
                parameters=parameters,
            )
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error updating the Azure Managed Redis cluster {0}: {1}".format(self.name, str(exc)))
        return response and as_attribute_dict(response, exclude_readonly=False) or self.get_instance()

    def delete_cluster(self):
        self.log("Deleting the Azure Managed Redis cluster {0}".format(self.name))
        try:
            response = self.redisenterprise_client.redis_enterprise.begin_delete(
                resource_group_name=self.resource_group,
                cluster_name=self.name,
            )
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error deleting the Azure Managed Redis cluster {0}: {1}".format(self.name, str(exc)))
        return True

    def get_instance(self):
        self.log("Checking if the Azure Managed Redis cluster {0} is present".format(self.name))
        try:
            response = self.redisenterprise_client.redis_enterprise.get(
                resource_group_name=self.resource_group,
                cluster_name=self.name,
            )
            return as_attribute_dict(response, exclude_readonly=False)
        except ResourceNotFoundError:
            self.log("Did not find the Azure Managed Redis cluster {0}".format(self.name))
            return False


def main():
    """Main execution"""
    AzureRMManagedRedis()


if __name__ == '__main__':
    main()
