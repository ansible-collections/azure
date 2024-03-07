#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_akscredentials_info

version_added: "2.3.0"

short_description: List Azure Kubernetes Service Credentials facts

description:
    - List Azure Kubernetes Service Credentials facts.

options:
    cluster_name:
        description:
            - Azure Kubernetes Service or all Azure Kubernetes Services.
        type: str
        required: true
    resource_group:
        description:
            - The resource group to search for the desired Azure Kubernetes Service.
        type: str
        required: true
    show_admin_credentials:
        description:
            - Whether list Cluster Admin Credentials.
        type: bool
        default: false
    show_user_credentials:
        description:
            - Whether list Cluster User Credentials.
        type: bool
        default: false
    show_monitor_credentials:
        description:
            - Whether list Cluster Monitoring User Credentials.
        type: bool
        default: false

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get managecluster admin credentials
  azure_rm_akscredentials_info:
    resource_group: "{{ resource_group }}"
    cluster_name: cluter_name
    show_admin_credentials: true

- name: Get managecluster user credentials
  azure_rm_akscredentials_info:
    resource_group: "{{ resource_group }}"
    cluster_name: cluster_name
    show_user_credentials: true

- name: Get managecluster monitor user credentials
  azure_rm_akscredentials_info:
    resource_group: "{{ resource_group }}"
    cluster_name: cluster_name
    show_monitor_credentials: true
'''

RETURN = '''
cluster_credentials:
    description:
        - Lists the cluster user, admin or monitoring user credentials of a managed cluster
    returned: always
    type: complex
    contains:
        cluster_name:
            description:
                - Azure Kubernetes Service or all Azure Kubernetes Services.
            type: str
            returned: always
            sample: testcluster01
        resource_group:
            description:
                - The resource group to search for the desired Azure Kubernetes Service.
            type: str
            returned: always
            sample:
        name:
            description:
                - The name of the credential.
            type: str
            returned: always
            sample:
        value:
            description:
                -  Base64-encoded Kubernetes configuration file.
            type: str
            returned: always
            sample: "apiVersion: ************************"
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import HttpResponseError
except Exception:
    # handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'managedClustersCredentials'


class AzureRMAksCredentialsInfo(AzureRMModuleBase):
    """Utility class to get Azure Kubernetes Service Credentials facts"""

    def __init__(self):

        self.module_args = dict(
            cluster_name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            show_admin_credentials=dict(type='bool', default=False),
            show_user_credentials=dict(type='bool', default=False),
            show_monitor_credentials=dict(type='bool', default=False),
        )

        self.results = dict(
            changed=False,
            cluster_credentials=[],
        )

        mutually_exclusive = [('show_admin_credentials', 'show_user_credentials', 'show_monitor_credentials')]

        super(AzureRMAksCredentialsInfo, self).__init__(
            derived_arg_spec=self.module_args,
            supports_check_mode=True,
            supports_tags=False,
            mutually_exclusive=mutually_exclusive,
            facts_module=True
        )

    def exec_module(self, **kwargs):

        for key in self.module_args:
            setattr(self, key, kwargs[key])

        if self.show_user_credentials:
            self.results['cluster_credentials'] = self.get_user_credentials()
        elif self.show_admin_credentials:
            self.results['cluster_credentials'] = self.get_admin_credentials()
        elif self.show_monitor_credentials:
            self.results['cluster_credentials'] = self.get_monitor_credentials()

        self.results['resource_group'] = self.resource_group
        self.results['cluster_name'] = self.cluster_name
        return self.results

    def get_user_credentials(self):
        """Get The Azure Kubernetes Service USER Credentials"""
        response = None

        try:
            response = self.managedcluster_client.managed_clusters.list_cluster_user_credentials(self.resource_group, self.cluster_name)
        except HttpResponseError as ec:
            self.fail("Lists the cluster user credentials of a managed cluster Failed, Exception as {0}".format(ec))
        return [self.format_response(item) for item in response.kubeconfigs]

    def get_admin_credentials(self):
        """Get The Azure Kubernetes Service Admin Credentials"""
        response = None

        try:
            response = self.managedcluster_client.managed_clusters.list_cluster_admin_credentials(self.resource_group, self.cluster_name)
        except HttpResponseError as ec:
            self.fail("Lists the cluster admin credentials of a managed cluster Failed, Exception as {0}".format(ec))

        return [self.format_response(item) for item in response.kubeconfigs]

    def get_monitor_credentials(self):
        """Get The Azure Kubernetes Service Monitor Credentials"""
        response = None

        try:
            response = self.managedcluster_client.managed_clusters.list_cluster_monitoring_user_credentials(self.resource_group, self.cluster_name)
        except HttpResponseError as ec:
            self.fail("Lists the cluster monitoring credentials of a managed cluster Failed, Exception as {0}".format(ec))
        return [self.format_response(item) for item in response.kubeconfigs]

    def format_response(self, item):
        if not item:
            return
        return dict(name=item.name, value=item.value.decode('utf-8'))


def main():
    """Main module execution code path"""

    AzureRMAksCredentialsInfo()


if __name__ == '__main__':
    main()
