#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_databrickscluster
version_added: "4.3.0"
short_description: Manage clusters in an Azure Databricks workspace
description:
    - Create, update, and delete all-purpose clusters in an Azure Databricks workspace.
    - Authenticate to the workspace data plane using the configured Azure identity.
    - I(state=absent) permanently deletes the cluster. Databricks keeps merely terminated
      clusters in the cluster list for 30 days, so absent does not stop at terminating it.
options:
    resource_group:
        description: Resource group containing the workspace.
        required: true
        type: str
    workspace_name:
        description: Azure Databricks workspace name.
        required: true
        type: str
    name:
        description: Cluster name.
        required: true
        type: str
    spark_version:
        description: Databricks Runtime version identifier.
        type: str
    node_type_id:
        description: Databricks worker node type identifier.
        type: str
    num_workers:
        description: Fixed number of workers. Mutually exclusive with I(autoscale).
        type: int
    autoscale:
        description: Autoscaling bounds for the worker count.
        type: dict
        suboptions:
            min_workers:
                description: Minimum worker count.
                required: true
                type: int
            max_workers:
                description: Maximum worker count.
                required: true
                type: int
    autotermination_minutes:
        description: Automatically terminate an idle cluster after this many minutes.
        type: int
        default: 60
    data_security_mode:
        description:
            - Cluster access mode. Required on Premium workspaces, which do not allow
              clusters without an explicit access mode.
            - C(SINGLE_USER) dedicates the cluster to one user, C(USER_ISOLATION) shares
              it between users, and C(NONE) creates a no-isolation cluster where allowed.
            - The access mode cannot be changed on an existing cluster.
        type: str
        choices: [SINGLE_USER, USER_ISOLATION, NONE]
    state:
        description: Desired state of the cluster.
        type: str
        choices: [present, absent]
        default: present
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create an autoscaling Databricks cluster
  azure.azcollection.azure_rm_databrickscluster:
    resource_group: analytics
    workspace_name: analytics-workspace
    name: etl
    spark_version: 13.3.x-scala2.12
    node_type_id: Standard_DS3_v2
    data_security_mode: SINGLE_USER
    autoscale:
      min_workers: 2
      max_workers: 4

- name: Remove a cluster
  azure.azcollection.azure_rm_databrickscluster:
    resource_group: analytics
    workspace_name: analytics-workspace
    name: etl
    state: absent
'''

RETURN = '''
cluster:
    description: Databricks cluster configuration returned by the workspace API.
    returned: when I(state=present)
    type: dict
    sample: {"cluster_id": "0123-456789-abcd", "cluster_name": "etl", "spark_version": "13.3.x-scala2.12", "state": "RUNNING"}
'''

import time
from urllib.parse import urlencode

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_databricks import (
    databricks_request,
    databricks_workspace_host,
)

# clusters/edit only accepts a RUNNING or TERMINATED cluster, and starting a
# cluster can take several minutes.
STATE_TIMEOUT = 600
STATE_INTERVAL = 10
EDITABLE_STATES = ('RUNNING', 'TERMINATED')

# clusters/edit replaces the whole cluster spec, so every field this module
# does not manage must be carried forward from the existing cluster.
PRESERVED_SPEC_FIELDS = (
    'azure_attributes',
    'cluster_log_conf',
    'cluster_source',
    'custom_tags',
    'docker_image',
    'driver_node_type_id',
    'enable_elastic_disk',
    'enable_local_disk_encryption',
    'init_scripts',
    'instance_pool_id',
    'policy_id',
    'runtime_engine',
    'single_user_name',
    'spark_conf',
    'spark_env_vars',
    'ssh_public_keys',
)


class AzureRMDatabricksCluster(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            workspace_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            spark_version=dict(type='str'),
            node_type_id=dict(type='str'),
            num_workers=dict(type='int'),
            autoscale=dict(type='dict', options=dict(
                min_workers=dict(type='int', required=True),
                max_workers=dict(type='int', required=True),
            )),
            autotermination_minutes=dict(type='int', default=60),
            data_security_mode=dict(type='str', choices=['SINGLE_USER', 'USER_ISOLATION', 'NONE']),
            state=dict(type='str', choices=['present', 'absent'], default='present'),
        )

        self.resource_group = None
        self.workspace_name = None
        self.name = None
        self.spark_version = None
        self.node_type_id = None
        self.num_workers = None
        self.autoscale = None
        self.autotermination_minutes = None
        self.data_security_mode = None
        self.state = None

        self.results = dict(changed=False)
        self.host = None

        super(AzureRMDatabricksCluster, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            mutually_exclusive=[('num_workers', 'autoscale')],
            required_if=[
                ('state', 'present', ('spark_version', 'node_type_id')),
                ('state', 'present', ('num_workers', 'autoscale'), True),
            ],
            supports_tags=False,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        # Validate the desired sizing before any Azure reads or writes, so a
        # malformed autoscale cannot leave a partially reconciled workspace.
        if self.state == 'present' and self.autoscale is not None and (
                self.autoscale['min_workers'] < 0 or
                self.autoscale['max_workers'] < self.autoscale['min_workers']):
            self.fail('autoscale requires 0 <= min_workers <= max_workers')

        self.host = databricks_workspace_host(self, self.resource_group, self.workspace_name)

        existing = self.get_cluster()

        if self.state == 'absent':
            if existing is not None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.delete_cluster(existing)
            return self.results

        return self.create_or_update_cluster(existing)

    def get_cluster(self):
        self.log('Get Databricks cluster {0}'.format(self.name))
        clusters = databricks_request(self, self.host, '/api/2.0/clusters/list').get('clusters', [])
        return next((cluster for cluster in clusters if cluster.get('cluster_name') == self.name), None)

    def create_or_update_cluster(self, existing):
        desired = self._body()
        if existing is None:
            self.results['changed'] = True
            if not self.check_mode:
                created = databricks_request(self, self.host, '/api/2.0/clusters/create', 'POST', desired)
                self.results['cluster'] = self._get_cluster_by_id(created['cluster_id'])
            else:
                self.results['cluster'] = desired
            return self.results

        self.results['changed'] = any(existing.get(key) != value for key, value in desired.items())
        if not self.results['changed']:
            self.results['cluster'] = existing
            return self.results
        if self.check_mode:
            self.results['cluster'] = dict(existing, **desired)
            return self.results
        desired['cluster_id'] = existing['cluster_id']
        for field in PRESERVED_SPEC_FIELDS:
            if field not in desired and field in existing:
                desired[field] = existing[field]
        if existing.get('state') not in EDITABLE_STATES:
            self._wait_for_state(existing['cluster_id'], EDITABLE_STATES, 'be ready for the update',
                                 fail_states=('ERROR', 'UNKNOWN'))
        databricks_request(self, self.host, '/api/2.0/clusters/edit', 'POST', desired)
        self.results['cluster'] = self._get_cluster_by_id(existing['cluster_id'])
        return self.results

    def delete_cluster(self, existing):
        """Permanently delete the cluster.

        clusters/delete only terminates a cluster and Databricks keeps
        terminated clusters in clusters/list for 30 days, so absent calls
        clusters/permanent-delete, which terminates and removes the cluster
        in a single call whatever its state.
        """
        self.log('Delete Databricks cluster {0}'.format(self.name))
        try:
            databricks_request(self, self.host, '/api/2.0/clusters/permanent-delete', 'POST',
                               {'cluster_id': existing['cluster_id']})
        except Exception as exc:
            self.fail('Error deleting Databricks cluster {0}: {1}'.format(self.name, str(exc)))

    def _get_cluster_by_id(self, cluster_id):
        """Read the cluster back so the result reflects the stored configuration."""
        return databricks_request(
            self, self.host, '/api/2.0/clusters/get?' + urlencode({'cluster_id': cluster_id}))

    def _wait_for_state(self, cluster_id, states, action, fail_states=()):
        """Wait until the cluster reaches one of the given states."""
        deadline = time.time() + STATE_TIMEOUT
        while time.time() < deadline:
            cluster = databricks_request(
                self, self.host, '/api/2.0/clusters/get?' + urlencode({'cluster_id': cluster_id}))
            state = cluster.get('state')
            if state in states:
                return
            if state in fail_states:
                self.fail('Databricks cluster {0} is in state {1}; start or terminate it before updating it'.format(
                    self.name, state))
            time.sleep(STATE_INTERVAL)
        self.fail('Timed out waiting for Databricks cluster {0} to {1}'.format(self.name, action))

    def _body(self):
        """Build the cluster payload for the create / edit call."""
        desired = dict(
            cluster_name=self.name,
            spark_version=self.spark_version,
            node_type_id=self.node_type_id,
            autotermination_minutes=self.autotermination_minutes,
        )
        if self.data_security_mode is not None:
            desired['data_security_mode'] = self.data_security_mode
        if self.autoscale is not None:
            desired['autoscale'] = self.autoscale
        else:
            desired['num_workers'] = self.num_workers
        return desired


def main():
    AzureRMDatabricksCluster()


if __name__ == '__main__':
    main()
