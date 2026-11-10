#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_cosmosdbsqlcontainer
version_added: "4.3.0"
short_description: Manage a Cosmos DB SQL container
description:
    - Create, update, or delete a SQL API container in an existing Cosmos DB database.
    - Update indexing mode and dedicated throughput without replacing the container.
options:
    resource_group:
        description: Resource group containing the account.
        type: str
        required: true
    account_name:
        description: Cosmos DB account name.
        type: str
        required: true
    database_name:
        description: Existing SQL database name.
        type: str
        required: true
    name:
        description: Container name.
        type: str
        required: true
    partition_key_paths:
        description:
            - Partition key paths, for example C(/tenantId).
            - Two or three paths define a hierarchical partition key.
            - Required when creating a container. Partition keys cannot be changed.
        type: list
        elements: str
    indexing_mode:
        description: Indexing mode. Other indexing settings are preserved on update.
        type: str
        choices: [consistent, none]
    automatic:
        description: Whether indexing is automatic. Defaults to false when I(indexing_mode=none).
        type: bool
    throughput:
        description:
            - Dedicated manual throughput in request units per second.
            - Mutually exclusive with I(autoscale_max_throughput).
            - Existing containers must already have manual dedicated throughput.
        type: int
    autoscale_max_throughput:
        description:
            - Maximum dedicated autoscale throughput in request units per second.
            - Existing containers must already have autoscale dedicated throughput.
        type: int
    state:
        description: Desired state of the container.
        type: str
        choices: [present, absent]
        default: present
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create a SQL container
  azure.azcollection.azure_rm_cosmosdbsqlcontainer:
    resource_group: analytics
    account_name: example-account
    database_name: example-database
    name: events
    partition_key_paths: [/tenantId]
    indexing_mode: consistent
    throughput: 400

- name: Create a container with a hierarchical partition key
  azure.azcollection.azure_rm_cosmosdbsqlcontainer:
    resource_group: analytics
    account_name: example-account
    database_name: example-database
    name: orders
    partition_key_paths: [/tenantId, /orderId]

- name: Disable indexing without recreating the container
  azure.azcollection.azure_rm_cosmosdbsqlcontainer:
    resource_group: analytics
    account_name: example-account
    database_name: example-database
    name: events
    indexing_mode: none
'''

RETURN = '''
container:
    description: Azure SQL container definition.
    returned: when state is present and not in check mode
    type: dict
    sample: {"name": "events", "resource": {"id": "events"}}
'''

import copy

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.mgmt.cosmosdb import models
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMCosmosDBSqlContainer(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            account_name=dict(type='str', required=True),
            database_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            partition_key_paths=dict(type='list', elements='str', no_log=False),
            indexing_mode=dict(type='str', choices=['consistent', 'none']),
            automatic=dict(type='bool'),
            throughput=dict(type='int'),
            autoscale_max_throughput=dict(type='int'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.resource_group = None
        self.account_name = None
        self.database_name = None
        self.name = None
        self.partition_key_paths = None
        self.indexing_mode = None
        self.automatic = None
        self.throughput = None
        self.autoscale_max_throughput = None
        self.state = None

        self.results = dict(changed=False)
        self.client = None

        super(AzureRMCosmosDBSqlContainer, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True,
            supports_tags=False, mutually_exclusive=[('throughput', 'autoscale_max_throughput')])

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self.client = self.cosmosdb_client.sql_resources

        existing = self.get_container()

        if self.state == 'absent':
            if existing is not None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.delete_container()
            return self.results

        return self.create_or_update_container(existing)

    def get_container(self):
        self.log('Get SQL container {0}'.format(self.name))
        try:
            return self.client.get_sql_container(self.resource_group, self.account_name,
                                                 self.database_name, self.name)
        except ResourceNotFoundError:
            return None
        except Exception as exc:
            self.fail('Error retrieving SQL container {0}: {1}'.format(self.name, str(exc)))

    def create_or_update_container(self, existing):
        if self.throughput is not None and self.throughput <= 0:
            self.fail('throughput must be positive')
        if self.autoscale_max_throughput is not None and self.autoscale_max_throughput <= 0:
            self.fail('autoscale_max_throughput must be positive')

        resource = self._resource(existing)
        resource_changed = self._reconcile_indexing_policy(resource, existing)
        throughput_changed = self._throughput_needs_update(existing)
        self.results['changed'] = resource_changed or throughput_changed

        if self.check_mode or not self.results['changed']:
            if not self.check_mode:
                self.results['container'] = existing.as_dict()
            return self.results

        try:
            if resource_changed:
                options = None
                if existing is None and self._desired_throughput() is not None:
                    options = models.CreateUpdateOptions(
                        throughput=self.throughput,
                        autoscale_settings=models.AutoscaleSettings(max_throughput=self.autoscale_max_throughput)
                        if self.autoscale_max_throughput is not None else None)
                existing = self.get_poller_result(self.client.begin_create_update_sql_container(
                    self.resource_group, self.account_name, self.database_name, self.name,
                    create_update_sql_container_parameters=models.SqlContainerCreateUpdateParameters(
                        resource=resource, options=options)))
            if throughput_changed:
                value = models.ThroughputSettingsResource(
                    throughput=self.throughput,
                    autoscale_settings=models.AutoscaleSettingsResource(max_throughput=self.autoscale_max_throughput)
                    if self.autoscale_max_throughput is not None else None)
                self.get_poller_result(self.client.begin_update_sql_container_throughput(
                    self.resource_group, self.account_name, self.database_name, self.name,
                    update_throughput_parameters=models.ThroughputSettingsUpdateParameters(resource=value)))
        except Exception as exc:
            self.fail('Error creating / updating SQL container {0}: {1}'.format(self.name, str(exc)))

        self.results['container'] = existing.as_dict()
        return self.results

    def delete_container(self):
        self.log('Delete SQL container {0}'.format(self.name))
        try:
            self.get_poller_result(self.client.begin_delete_sql_container(
                self.resource_group, self.account_name, self.database_name, self.name))
        except Exception as exc:
            self.fail('Error deleting SQL container {0}: {1}'.format(self.name, str(exc)))

    def _resource(self, existing):
        """Build the container resource payload for the create / update call."""
        if existing is None:
            if not self.partition_key_paths:
                self.fail('partition_key_paths is required when creating a container')
            if len(self.partition_key_paths) > 3:
                self.fail('partition_key_paths supports at most three paths')
            return models.SqlContainerResource(
                id=self.name, partition_key=models.ContainerPartitionKey(
                    paths=self.partition_key_paths, kind=self._partition_key_kind(self.partition_key_paths)))
        if self.partition_key_paths is not None:
            current = existing.resource.partition_key
            if (not current or self.partition_key_paths != current.paths
                    or self._partition_key_kind(self.partition_key_paths) != current.kind):
                self.fail('partition_key_paths cannot be changed on an existing container')
        return copy.deepcopy(existing.resource)

    def _partition_key_kind(self, paths):
        """A single path uses a Hash key; multiple paths form a hierarchical MultiHash key."""
        return 'MultiHash' if len(paths) > 1 else 'Hash'

    def _reconcile_indexing_policy(self, resource, existing):
        """Apply the desired indexing policy to the container payload.

        Returns whether the resulting policy differs from the existing container.
        """
        old_mode = resource.indexing_policy.indexing_mode if resource.indexing_policy else None
        old_automatic = resource.indexing_policy.automatic if resource.indexing_policy else None
        desired_automatic = self.automatic
        if self.indexing_mode is not None:
            if resource.indexing_policy is None:
                resource.indexing_policy = models.IndexingPolicy()
            resource.indexing_policy.indexing_mode = self.indexing_mode
            if self.indexing_mode == 'none' and self.automatic is None:
                desired_automatic = False
            elif self.indexing_mode == 'consistent' and old_mode == 'none' and self.automatic is None:
                desired_automatic = True
                resource.indexing_policy.included_paths = [models.IncludedPath(path='/*')]
                resource.indexing_policy.excluded_paths = [models.ExcludedPath(path='/*/_etag/?')]
        if self.indexing_mode == 'none':
            resource.indexing_policy.included_paths = None
            resource.indexing_policy.excluded_paths = None
            resource.indexing_policy.composite_indexes = None
            resource.indexing_policy.spatial_indexes = None
        if desired_automatic is not None:
            if self.indexing_mode == 'none' and desired_automatic:
                self.fail('automatic must be false when indexing_mode is none')
            if resource.indexing_policy is None:
                resource.indexing_policy = models.IndexingPolicy()
            resource.indexing_policy.automatic = desired_automatic
        return existing is None or (
            self.indexing_mode is not None and self.indexing_mode != old_mode) or (
                desired_automatic is not None and desired_automatic != old_automatic) or (
                    self.indexing_mode == 'none' and old_mode == 'none' and existing.resource.indexing_policy and (
                        existing.resource.indexing_policy.included_paths or
                        existing.resource.indexing_policy.excluded_paths or
                        existing.resource.indexing_policy.composite_indexes or
                        existing.resource.indexing_policy.spatial_indexes))

    def _desired_throughput(self):
        return self.throughput if self.throughput is not None else self.autoscale_max_throughput

    def _throughput_needs_update(self, existing):
        """Return whether the dedicated throughput settings must be reconciled."""
        desired = self._desired_throughput()
        if desired is None or existing is None:
            return False
        try:
            current = self.client.get_sql_container_throughput(
                self.resource_group, self.account_name, self.database_name, self.name).resource
        except ResourceNotFoundError:
            self.fail('Container has no dedicated throughput; shared throughput cannot be updated here')
        except Exception as exc:
            self.fail('Error retrieving container throughput: {0}'.format(str(exc)))
        autoscale = current.autoscale_settings
        if (autoscale is not None) != (self.autoscale_max_throughput is not None):
            self.fail('Changing throughput mode is not supported; migrate the container throughput first')
        return desired != (autoscale.max_throughput if autoscale else current.throughput)


def main():
    AzureRMCosmosDBSqlContainer()


if __name__ == '__main__':
    main()
