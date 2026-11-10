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
    - I(state=absent) terminates the cluster and permanently deletes it; Databricks keeps
      merely terminated clusters in the cluster list for 30 days.
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

# clusters/permanent-delete requires a terminated cluster, and terminating a
# large cluster can take several minutes.
DELETE_TIMEOUT = 600
DELETE_INTERVAL = 10
TERMINAL_STATES = ('TERMINATED', 'ERROR', 'UNKNOWN')


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
                self.results['cluster'] = databricks_request(
                    self, self.host, '/api/2.0/clusters/create', 'POST', desired)
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
        self.results['cluster'] = databricks_request(
            self, self.host, '/api/2.0/clusters/edit', 'POST', desired) or desired
        return self.results

    def delete_cluster(self, existing):
        """Terminate and permanently delete the cluster.

        clusters/delete only terminates a cluster and Databricks keeps
        terminated clusters in clusters/list for 30 days, so absent must also
        call clusters/permanent-delete to remove the cluster entirely.
        """
        self.log('Delete Databricks cluster {0}'.format(self.name))
        cluster_id = existing['cluster_id']
        try:
            if existing.get('state') not in TERMINAL_STATES:
                if existing.get('state') != 'TERMINATING':
                    databricks_request(self, self.host, '/api/2.0/clusters/delete', 'POST',
                                       {'cluster_id': cluster_id})
                self._wait_terminated(cluster_id)
            databricks_request(self, self.host, '/api/2.0/clusters/permanent-delete', 'POST',
                               {'cluster_id': cluster_id})
        except Exception as exc:
            self.fail('Error deleting Databricks cluster {0}: {1}'.format(self.name, str(exc)))

    def _wait_terminated(self, cluster_id):
        """Wait for the cluster to reach a terminal state before permanent deletion."""
        deadline = time.time() + DELETE_TIMEOUT
        while time.time() < deadline:
            cluster = databricks_request(
                self, self.host, '/api/2.0/clusters/get?' + urlencode({'cluster_id': cluster_id}))
            if cluster.get('state') in TERMINAL_STATES:
                return
            time.sleep(DELETE_INTERVAL)
        self.fail('Timed out waiting for Databricks cluster {0} to terminate'.format(self.name))

    def _body(self):
        """Build the cluster payload for the create / edit call."""
        desired = dict(
            cluster_name=self.name,
            spark_version=self.spark_version,
            node_type_id=self.node_type_id,
            autotermination_minutes=self.autotermination_minutes,
        )
        if self.autoscale is not None:
            desired['autoscale'] = self.autoscale
        else:
            desired['num_workers'] = self.num_workers
        return desired


def main():
    AzureRMDatabricksCluster()


if __name__ == '__main__':
    main()
