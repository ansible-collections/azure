#!/usr/bin/python
#
# Copyright (c) 2026
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
            - Required when creating a container. Partition keys cannot be changed.
        type: list
        elements: str
    indexing_mode:
        description: Indexing mode. Other indexing settings are preserved on update.
        type: str
        choices: [consistent, none]
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
    - OpenAI (@openai)
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
    from azure.mgmt.cosmosdb import CosmosDBManagementClient
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
            throughput=dict(type='int'),
            autoscale_max_throughput=dict(type='int'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )
        super(AzureRMCosmosDBSqlContainer, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True,
            supports_tags=False, mutually_exclusive=[('throughput', 'autoscale_max_throughput')])

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.client = self.get_mgmt_svc_client(
            CosmosDBManagementClient, base_url=self._cloud_environment.endpoints.resource_manager).sql_resources
        args = (self.resource_group, self.account_name, self.database_name, self.name)
        try:
            existing = self.client.get_sql_container(*args)
        except ResourceNotFoundError:
            existing = None
        except Exception as exc:
            self.fail('Error retrieving container {0}: {1}'.format(self.name, exc))

        if self.state == 'absent':
            if existing and not self.check_mode:
                try:
                    self.get_poller_result(self.client.begin_delete_sql_container(*args))
                except Exception as exc:
                    self.fail('Error deleting container {0}: {1}'.format(self.name, exc))
            return dict(changed=existing is not None)

        if existing is None and not self.partition_key_paths:
            self.fail('partition_key_paths is required when creating a container')
        if existing and self.partition_key_paths is not None:
            if not existing.resource.partition_key or self.partition_key_paths != existing.resource.partition_key.paths:
                self.fail('partition_key_paths cannot be changed on an existing container')
        if self.throughput is not None and self.throughput <= 0:
            self.fail('throughput must be positive')
        if self.autoscale_max_throughput is not None and self.autoscale_max_throughput <= 0:
            self.fail('autoscale_max_throughput must be positive')

        desired_throughput = self.throughput if self.throughput is not None else self.autoscale_max_throughput
        throughput_changed = False
        if existing and desired_throughput is not None:
            try:
                current = self.client.get_sql_container_throughput(*args).resource
            except ResourceNotFoundError:
                self.fail('Container has no dedicated throughput; shared throughput cannot be updated here')
            except Exception as exc:
                self.fail('Error retrieving container throughput: {0}'.format(exc))
            autoscale = current.autoscale_settings
            if (autoscale is not None) != (self.autoscale_max_throughput is not None):
                self.fail('Changing throughput mode is not supported; migrate the container throughput first')
            throughput_changed = desired_throughput != (autoscale.max_throughput if autoscale else current.throughput)

        resource = copy.deepcopy(existing.resource) if existing else models.SqlContainerResource(
            id=self.name, partition_key=models.ContainerPartitionKey(paths=self.partition_key_paths, kind='Hash'))
        old_mode = resource.indexing_policy.indexing_mode if resource.indexing_policy else None
        resource_changed = existing is None or (self.indexing_mode is not None and self.indexing_mode != old_mode)
        if self.indexing_mode is not None:
            if resource.indexing_policy is None:
                resource.indexing_policy = models.IndexingPolicy()
            resource.indexing_policy.indexing_mode = self.indexing_mode
        if self.check_mode:
            return dict(changed=resource_changed or throughput_changed)

        try:
            if resource_changed:
                options = None
                if existing is None and desired_throughput is not None:
                    options = models.CreateUpdateOptions(
                        throughput=self.throughput,
                        autoscale_settings=models.AutoscaleSettings(max_throughput=self.autoscale_max_throughput)
                        if self.autoscale_max_throughput is not None else None)
                existing = self.get_poller_result(self.client.begin_create_update_sql_container(
                    *args, create_update_sql_container_parameters=models.SqlContainerCreateUpdateParameters(
                        resource=resource, options=options)))
            if throughput_changed:
                throughput = models.ThroughputSettingsResource(
                    throughput=self.throughput,
                    autoscale_settings=models.AutoscaleSettingsResource(max_throughput=self.autoscale_max_throughput)
                    if self.autoscale_max_throughput is not None else None)
                self.get_poller_result(self.client.begin_update_sql_container_throughput(
                    *args, update_throughput_parameters=models.ThroughputSettingsUpdateParameters(resource=throughput)))
        except Exception as exc:
            self.fail('Error updating container {0}: {1}'.format(self.name, exc))
        return dict(changed=resource_changed or throughput_changed, container=existing.as_dict())


def main():
    AzureRMCosmosDBSqlContainer()


if __name__ == '__main__':
    main()
