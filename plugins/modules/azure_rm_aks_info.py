#!/usr/bin/python
#
# Copyright (c) 2018 Yuwei Zhou, <yuwzho@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_aks_info

version_added: "0.1.2"

short_description: Get Azure Kubernetes Service facts

description:
    - Get facts for a specific Azure Kubernetes Service or all Azure Kubernetes Services.

options:
    name:
        description:
            - Limit results to a specific resource group.
        type: str
    resource_group:
        description:
            - The resource group to search for the desired Azure Kubernetes Service
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str
    show_kubeconfig:
        description:
            - Show kubeconfig of the AKS cluster.
            - Note the operation will cost more network overhead, not recommended when listing AKS.
            - I(show_kubeconfig=monitoring) to lists the cluster monitoring user credentials of a managed cluster.
            - I(show_kubeconfig=admin) to lists the cluster admin credentials of a managed cluster.
            - I(show_kubeconfig=user) to lists the cluster user credentials of a managed cluster.
        type: str
        choices:
            - user
            - admin
            - monitoring

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Yuwei Zhou (@yuwzho)
'''

EXAMPLES = '''
- name: Get facts for one Azure Kubernetes Service
  azure_rm_aks_info:
    name: Testing
    resource_group: myResourceGroup

- name: Get facts for all Azure Kubernetes Services
  azure_rm_aks_info:

- name: Get facts by tags
  azure_rm_aks_info:
    tags:
      - testing
'''

RETURN = '''
azure_aks:
    description: List of Azure Kubernetes Service dicts.
    returned: always
    type: list
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.exceptions import HttpResponseError
except Exception:
    # handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'managedClusters'


class AzureRMManagedClusterInfo(AzureRMModuleBase):
    """Utility class to get Azure Kubernetes Service facts"""

    def __init__(self):

        self.module_args = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            tags=dict(type='list', elements='str'),
            show_kubeconfig=dict(type='str', choices=['user', 'admin', 'monitoring']),
        )

        self.results = dict(
            changed=False,
            aks=[],
            available_versions=[]
        )

        self.name = None
        self.resource_group = None
        self.tags = None
        self.show_kubeconfig = None

        super(AzureRMManagedClusterInfo, self).__init__(
            derived_arg_spec=self.module_args,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):

        for key in self.module_args:
            setattr(self, key, kwargs[key])

        if self.name is not None and self.resource_group is not None:
            self.results['aks'] = self.get_item()
        elif self.resource_group is not None:
            self.results['aks'] = self.list_by_resourcegroup()
        else:
            self.results['aks'] = self.list_items()

        return self.results

    def get_item(self):
        """Get a single Azure Kubernetes Service"""

        self.log('Get properties for {0}'.format(self.name))

        item = None
        result = []

        try:
            item = self.managedcluster_client.managed_clusters.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            pass

        if item and self.has_tags(item.tags, self.tags):
            result = [self.serialize_obj(item, AZURE_OBJECT_CLASS)]
            if self.show_kubeconfig:
                result[0]['kube_config'] = self.get_aks_kubeconfig(self.resource_group, self.name)

        return result

    def list_by_resourcegroup(self):
        """Get all Azure Kubernetes Services"""

        self.log('List all Azure Kubernetes Services under resource group')

        try:
            response = self.managedcluster_client.managed_clusters.list_by_resource_group(self.resource_group)
        except Exception as exc:
            self.fail('Failed to list all items - {0}'.format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                item_dict = self.serialize_obj(item, AZURE_OBJECT_CLASS)
                if self.show_kubeconfig:
                    item_dict['kube_config'] = self.get_aks_kubeconfig(self.resource_group, item.name)
                results.append(item_dict)

        return results

    def list_items(self):
        """Get all Azure Kubernetes Services"""

        self.log('List all Azure Kubernetes Services')

        try:
            response = self.managedcluster_client.managed_clusters.list()
        except Exception as exc:
            self.fail('Failed to list all items - {0}'.format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                item_dict = self.serialize_obj(item, AZURE_OBJECT_CLASS)
                if self.show_kubeconfig:
                    item_dict['kube_config'] = self.get_aks_kubeconfig(item.resource_group, item.name)
                results.append(item_dict)

        return results

    def get_aks_kubeconfig(self, resource_group, name):
        '''
        Gets kubeconfig for the specified AKS instance.

        :return: AKS instance kubeconfig
        '''
        if self.show_kubeconfig == 'user':
            try:
                access_profile = self.managedcluster_client.managed_clusters.list_cluster_user_credentials(self.resource_group, self.name)
            except HttpResponseError as ec:
                self.log("Lists the cluster user credentials of a managed cluster Failed, Exception as {0}".format(ec))
                return []
            return [item.value.decode('utf-8') for item in access_profile.kubeconfigs]
        elif self.show_kubeconfig == 'admin':
            try:
                access_profile = self.managedcluster_client.managed_clusters.list_cluster_admin_credentials(self.resource_group, self.name)
            except HttpResponseError as ec:
                self.log("Lists the cluster admin credentials of a managed cluster Failed, Exception as {0}".format(ec))
                return []
            return [item.value.decode('utf-8') for item in access_profile.kubeconfigs]
        elif self.show_kubeconfig == 'monitoring':
            try:
                access_profile = self.managedcluster_client.managed_clusters.list_cluster_monitoring_user_credentials(self.resource_group, self.name)
            except HttpResponseError as ec:
                self.log("Lists the cluster monitoring credentials of a managed cluster Failed, Exception as {0}".format(ec))
                return []
            return [item.value.decode('utf-8') for item in access_profile.kubeconfigs]
        else:
            return []


def main():
    """Main module execution code path"""

    AzureRMManagedClusterInfo()


if __name__ == '__main__':
    main()
