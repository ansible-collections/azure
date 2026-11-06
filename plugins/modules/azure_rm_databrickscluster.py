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

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_databricks import databricks_request


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
        super(AzureRMDatabricksCluster, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            mutually_exclusive=[('num_workers', 'autoscale')],
            supports_tags=False,
        )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        if self.state == 'present':
            if not self.spark_version or not self.node_type_id:
                self.fail('spark_version and node_type_id are required when state is present')
            if self.num_workers is None and self.autoscale is None:
                self.fail('Either num_workers or autoscale is required when state is present')
            if self.num_workers is not None and self.num_workers < 0:
                self.fail('num_workers must be zero or greater')
            if self.autoscale is not None and (
                    self.autoscale['min_workers'] < 0 or
                    self.autoscale['max_workers'] < self.autoscale['min_workers']):
                self.fail('autoscale requires 0 <= min_workers <= max_workers')

        try:
            workspace = self.databricks_client.workspaces.get(self.resource_group, self.workspace_name)
        except ResourceNotFoundError:
            self.fail('Databricks workspace {0} was not found'.format(self.workspace_name))
        except Exception as exc:
            self.fail('Error retrieving Databricks workspace {0}: {1}'.format(self.workspace_name, exc))
        workspace_url = getattr(workspace, 'workspace_url', None)
        if not workspace_url:
            self.fail('Databricks workspace {0} did not return a workspace URL'.format(self.workspace_name))

        clusters = databricks_request(self, 'https://' + workspace_url, '/api/2.0/clusters/list').get('clusters', [])
        existing = next((cluster for cluster in clusters if cluster.get('cluster_name') == self.name), None)
        if self.state == 'absent':
            if existing and not self.check_mode:
                databricks_request(self, 'https://' + workspace_url, '/api/2.0/clusters/delete', 'POST',
                                   {'cluster_id': existing['cluster_id']})
            return dict(changed=existing is not None)

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
        if existing is None:
            if self.check_mode:
                return dict(changed=True, cluster=desired)
            cluster = databricks_request(self, 'https://' + workspace_url, '/api/2.0/clusters/create', 'POST', desired)
            return dict(changed=True, cluster=cluster)

        changed = any(existing.get(key) != value for key, value in desired.items())
        if not changed:
            return dict(changed=False, cluster=existing)
        desired['cluster_id'] = existing['cluster_id']
        if self.check_mode:
            return dict(changed=True, cluster=dict(existing, **desired))
        cluster = databricks_request(self, 'https://' + workspace_url, '/api/2.0/clusters/edit', 'POST', desired)
        return dict(changed=True, cluster=cluster or desired)


def main():
    AzureRMDatabricksCluster()


if __name__ == '__main__':
    main()
