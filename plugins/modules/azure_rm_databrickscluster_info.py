#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_databrickscluster_info
version_added: "4.3.0"
short_description: Get Azure Databricks cluster facts
description:
    - Get one cluster by name or ID, or list clusters in an Azure Databricks workspace.
    - Authentication uses the configured Azure identity.
options:
    resource_group:
        description: Resource group containing the workspace.
        type: str
        required: true
    workspace_name:
        description: Azure Databricks workspace name.
        type: str
        required: true
    name:
        description: Return only the cluster with this name.
        type: str
    cluster_id:
        description: Return only the cluster with this Databricks cluster ID.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get a cluster by name
  azure.azcollection.azure_rm_databrickscluster_info:
    resource_group: analytics
    workspace_name: analytics-workspace
    name: etl

- name: List clusters
  azure.azcollection.azure_rm_databrickscluster_info:
    resource_group: analytics
    workspace_name: analytics-workspace
'''

RETURN = '''
clusters:
    description: Clusters returned by the Databricks workspace REST API.
    returned: always
    type: list
    elements: dict
    sample: [{"cluster_id": "0123-456789-abcd", "cluster_name": "etl", "state": "RUNNING"}]
'''

from urllib.parse import urlencode

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_databricks import databricks_request


class AzureRMDatabricksClusterInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            workspace_name=dict(type='str', required=True),
            name=dict(type='str'),
            cluster_id=dict(type='str'),
        )
        self.results = dict(changed=False, clusters=[])
        super(AzureRMDatabricksClusterInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True,
            supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        if self.name and self.cluster_id:
            self.fail('name and cluster_id are mutually exclusive')
        try:
            workspace = self.databricks_client.workspaces.get(self.resource_group, self.workspace_name)
        except ResourceNotFoundError:
            self.fail('Databricks workspace {0} was not found'.format(self.workspace_name))
        except Exception as exc:
            self.fail('Error retrieving Databricks workspace {0}: {1}'.format(self.workspace_name, exc))
        workspace_url = getattr(workspace, 'workspace_url', None)
        if not workspace_url:
            self.fail('Databricks workspace {0} did not return a workspace URL'.format(self.workspace_name))
        host = 'https://' + workspace_url
        if self.cluster_id:
            cluster = databricks_request(
                self, host, '/api/2.0/clusters/get?' + urlencode({'cluster_id': self.cluster_id}),
                allow_not_found=True)
            clusters = [cluster] if cluster else []
        else:
            try:
                clusters = databricks_request(self, host, '/api/2.0/clusters/list').get('clusters', [])
            except Exception as exc:
                self.fail('Error listing Databricks clusters: {0}'.format(exc))
            if self.name:
                clusters = [cluster for cluster in clusters if cluster.get('cluster_name') == self.name]
        self.results['clusters'] = clusters
        return self.results


def main():
    AzureRMDatabricksClusterInfo()


if __name__ == '__main__':
    main()
