#!/usr/bin/python
#
# Copyright (c) 2020  haiyuazhang <haiyzhan@micosoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_openshiftmanagedcluster_info
version_added: '1.11.0'
short_description: Get Info onf Azure Red Hat OpenShift Managed Cluster
description:
    - Create, update and delete instance of Azure Red Hat OpenShift Managed Cluster instance.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: false
        type: str
    name:
        description:
            - Resource name.
        required: false
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Paul Czarkowski (@paulczar)
'''

EXAMPLES = '''
- name: List all Azure Red Hat OpenShift Managed Clusters for a given subscription
  azure_rm_openshiftmanagedcluster_info:
- name: List all Azure Red Hat OpenShift Managed Clusters for a given resource group
  azure_rm_openshiftmanagedcluster_info:
    resource_group: myResourceGroup
- name: Get Azure Red Hat OpenShift Managed Clusters
  azure_rm_openshiftmanagedcluster_info:
    resource_group: myResourceGroup
    name: myAzureFirewall
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/xx-xx-xx-xx/resourceGroups/mycluster-eastus/providers/Microsoft.RedHatOpenShift/openShiftClusters/mycluster
name:
    description:
        - Resource name.
    returned: always
    type: str
    sample: mycluster
type:
    description:
        - Resource type.
    returned: always
    type: str
    sample: Microsoft.RedHatOpenShift/openShiftClusters
location:
    description:
        - Resource location.
    returned: always
    type: str
    sample: eatus
properties:
    description:
        - Properties of a OpenShift managed cluster.
    returned: always
    type: complex
    sample: null
    contains:
        provisioningState:
            description:
                - The current deployment or provisioning state, which only appears in the response.
            returned: always
            type: str
            sample: Creating
        clusterProfile:
            description:
                - Configuration for Openshift cluster.
            returned: always
            type: complex
            contains:
                domain:
                    description:
                        - Domain for the cluster.
                    returned: always
                    type: str
                    sample: mycluster
                version:
                    description:
                        - Openshift version.
                    returned: always
                    type: str
                    sample: 4.4.17
                resourceGroupId:
                    description:
                        - The ID of the cluster resource group.
                    returned: always
                    type: str
                    sample: /subscriptions/xx-xx-xx-xx/resourceGroups/mycluster-eastus-cluster
        servicePrincipalProfile:
            description:
                - Service principal.
            type: complex
            returned: always
            contains:
                clientId:
                    description: Client ID of the service principal.
                    returned: always
                    type: str
                    sample: xxxxxxxx-xxxx-xxxx-xxxxxxxxxxxx
        networkProfile:
            description:
                - Configuration for OpenShift networking.
            returned: always
            type: complex
            contains:
                podCidr:
                    description:
                        - CIDR for the OpenShift Pods.
                    returned: always
                    type: str
                    sample: 10.128.0.0/14
                serviceCidr:
                    description:
                        - CIDR for OpenShift Services.
                    type: str
                    returned: always
                    sample: 172.30.0.0/16
        masterProfile:
            description:
                - Configuration for OpenShift master VMs.
            returned: always
            type: complex
            contains:
                vmSize:
                    description:
                        - Size of agent VMs (immutable).
                    type: str
                    returned: always
                    sample: Standard_D8s_v3
                subnetId:
                    description:
                        - The Azure resource ID of the master subnet (immutable).
                    type: str
                    returned: always
                    sample: /subscriptions/xx-xx-xx-xx/resourceGroups/mycluster-eastus/providers/Microsoft.Network/
                            virtualNetworks/mycluster-vnet/subnets/mycluster-worker
        workerProfiles:
            description:
                - Configuration of OpenShift cluster VMs.
            returned: always
            type: complex
            contains:
                name:
                    description:
                        - Unique name of the pool profile in the context of the subscription and resource group.
                    returned: always
                    type: str
                    sample: worker
                count:
                    description:
                        - Number of agents (VMs) to host docker containers.
                    returned: always
                    type: int
                    sample: 3
                vmSize:
                    description:
                        - Size of agent VMs.
                    returned: always
                    type: str
                    sample: Standard_D4s_v3
                diskSizeGB:
                    description:
                        - disk size in GB.
                    returned: always
                    type: int
                    sample: 128
                subnetId:
                    description:
                        - Subnet ID for worker pool.
                    returned: always
                    type: str
                    sample: /subscriptions/xx-xx-xx-xx/resourceGroups/mycluster-eastus/providers/Microsoft.Network/
                            virtualNetworks/mycluster-vnet/subnets/mycluster-worker
        ingressProfiles:
            description:
                - Ingress configruation.
            returned: always
            type: list
            sample: [{"name": "default", "visibility": "Public"}, ]
        apiserverProfile:
            description:
                - API server configuration.
            returned: always
            type: complex
            contains:
                visibility:
                    description:
                        - api server visibility.
                    returned: always
                    type: str
                    sample: Public
'''

import time
import json
import random
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient
try:
    from msrestazure.azure_exceptions import CloudError
except ImportError:
    # this is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMOpenShiftManagedClustersInfo(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            name=dict(
                type='str'
            )
        )

        self.resource_group = None
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        self.query_parameters = {}
        self.query_parameters['api-version'] = '2020-04-30'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        self.mgmt_client = None
        super(AzureRMOpenShiftManagedClustersInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and self.name is not None):
            self.results['clusters'] = self.get()
        elif (self.resource_group is not None):
            self.results['clusters'] = self.list()
        else:
            self.results['clusters'] = self.listall()
        return self.results

    def get(self):
        response = None
        results = {}
        # prepare url
        self.url = ('/subscriptions' +
                    '/{{ subscription_id }}' +
                    '/resourceGroups' +
                    '/{{ resource_group }}' +
                    '/providers' +
                    '/Microsoft.RedHatOpenShift' +
                    '/openShiftClusters' +
                    '/{{ open_shift_managed_cluster_name }}')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)
        self.url = self.url.replace('{{ resource_group }}', self.resource_group)
        self.url = self.url.replace('{{ open_shift_managed_cluster_name }}', self.name)

        try:
            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            results = json.loads(response.text)
            # self.log('Response : {0}'.format(response))
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')
            return {}

        return self.format_item(results)

    def list(self):
        response = None
        results = {}
        # prepare url
        self.url = ('/subscriptions' +
                    '/{{ subscription_id }}' +
                    '/resourceGroups' +
                    '/{{ resource_group }}' +
                    '/providers' +
                    '/Microsoft.RedHatOpenShift' +
                    '/openShiftClusters')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)
        self.url = self.url.replace('{{ resource_group }}', self.resource_group)

        try:
            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            results = json.loads(response.text)
            # self.log('Response : {0}'.format(response))
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return [self.format_item(x) for x in results['value']] if results['value'] else []

    def listall(self):
        response = None
        results = {}
        # prepare url
        self.url = ('/subscriptions' +
                    '/{{ subscription_id }}' +
                    '/providers' +
                    '/Microsoft.RedHatOpenShift' +
                    '/openShiftClusters')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)

        try:
            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            results = json.loads(response.text)
            # self.log('Response : {0}'.format(response))
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')
        return results
        # return [self.format_item(x) for x in results['value']] if results['value'] else []

    def format_item(self, item):
        return item
        # d = {
        #     'id': item['id'],
        #     'name': item['name'],
        #     'location': item['location'],
        #     'tags': item.get('tags'),
        #     'api_server_url': item['properties']['apiserverProfile']['url'],
        #     'console_url': item['properties']['consoleProfile']['url'],
        #     'provisioning_state': item['properties']['provisioningState']
        # }
        # return d


def main():
    AzureRMOpenShiftManagedClustersInfo()


if __name__ == '__main__':
    main()
