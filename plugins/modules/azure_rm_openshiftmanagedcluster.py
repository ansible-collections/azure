#!/usr/bin/python
#
# Copyright (c) 2020  haiyuazhang <haiyzhan@micosoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_openshiftmanagedcluster
version_added: '1.2.0'
short_description: Manage Azure Red Hat OpenShift Managed Cluster instance
description:
    - Create, update and delete instance of Azure Red Hat OpenShift Managed Cluster instance.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - Resource name.
        required: true
        type: str
    location:
        description:
            - Resource location.
        required: true
        type: str
    cluster_profile:
        description:
            - Configuration for OpenShift cluster.
        type: dict
        default: {}
        suboptions:
            pull_secret:
                description:
                    - Pull secret for the cluster (immutable).
                type: str
            domain:
                description:
                    - The domain for the cluster (immutable).
                type: str
            cluster_resource_group_id:
                description:
                    - The ID of the cluster resource group (immutable).
                type: str
            version:
                description:
                    - The Openshift version (immutable).
                type: str
            fips_validated_modules:
                description:
                    - If FIPS validated crypto modules are used
                type: str
                choices:
                    - Disabled
                    - Enabled
                default: Enabled
    service_principal_profile:
        description:
            - Service principal for the cluster.
            - Required when not using managed identity.
            - Mutually exclusive with I(identity).
        type: dict
        suboptions:
            client_id:
                description:
                    - Client ID of the service principal (immutable).
                type: str
            client_secret:
                description:
                    - Client secret of the service principal (immutable).
                type: str
    platform_workload_identity_profile:
        description:
            - The workload identity profile for the cluster.
            - Required when using managed identity (I(identity)).
            - Maps ARO operator names to user-assigned managed identity resource IDs.
        type: dict
        suboptions:
            platform_workload_identities:
                description:
                    - Dictionary of operator names to identity configurations.
                    - Each key is an operator name (e.g., C(image-registry), C(disk-csi-driver), C(ingress)).
                    - Each value is a dictionary with a C(resource_id) key pointing to the user-assigned managed identity.
                type: dict
            upgradeable_to:
                description:
                    - The OpenShift version that the workload identity cluster can be upgraded to.
                type: str
    network_profile:
        description:
            - Configuration for OpenShift networking (immutable).
        type: dict
        default: {'pod_cidr' : '10.128.0.0/14', 'service_cidr' : '172.30.0.0/16'}
        suboptions:
            pod_cidr:
                description:
                    - CIDR for the OpenShift Pods (immutable).
                type: str
            service_cidr:
                description:
                    - CIDR for OpenShift Services (immutable).
                type: str
            outbound_type:
                description:
                    - The OutboundType used for egress traffic.
                type: str
                choices:
                    - Loadbalancer
                    - UserDefinedRouting
            preconfigured_nsg:
                description:
                    - Specifies whether subnets are pre-attached with an NSG
                type: str
                choices:
                    - Disabled
                    - Enabled
                default: Disabled
    master_profile:
        description:
            - Configuration for OpenShift master VMs.
        type: dict
        suboptions:
            vm_size:
                description:
                    - Size of agent VMs (immutable).
                type: str
            subnet_id:
                description:
                    - The Azure resource ID of the master subnet (immutable).
                required: true
                type: str
            encryption_at_host:
                description:
                    - Whether master virtual machines are encrypted at host.
                type: str
                choices:
                    - Disabled
                    - Enabled
                default: Disabled
            disk_encryption_set_id:
                description:
                    - The resource ID of an associated DiskEncryptionSet, if applicable.
                type: str
    worker_profiles:
        description:
            - Configuration for OpenShift worker Vms.
        type: list
        elements: dict
        suboptions:
            name:
                description: name of the worker profile (immutable).
                type: str
                required: true
                choices:
                    - worker
            vm_size:
                description:
                    - The size of the worker Vms (immutable).
                type: str
            disk_size:
                description:
                    - The disk size of the worker VMs in GB. Must be 128 or greater (immutable).
                type: int
            subnet_id:
                description:
                    - The Azure resource ID of the worker subnet (immutable).
                type: str
                required: true
            count:
                description:
                    - The number of worker VMs. Must be between 3 and 20 (immutable).
                type: int
            encryption_at_host:
                description:
                    - Whether worker virtual machines are encrypted at host.
                type: str
                choices:
                    - Disabled
                    - Enabled
                default: Disabled
            disk_encryption_set_id:
                description:
                    - The resource ID of an associated DiskEncryptionSet, if applicable.
                type: str
    api_server_profile:
        description:
            - API server configuration.
        type: dict
        suboptions:
            visibility:
                description:
                    - API server visibility.
                type: str
                default: Public
                choices:
                    - Public
                    - Private
            ip:
                description:
                    - IP address of api server (immutable), only appears in response.
                type: str
            url:
                description:
                    - Url of api server (immutable), only appears in response.
                type: str
    ingress_profiles:
        description:
            - Ingress profiles configuration. only one profile is supported at the current API version.
        type: list
        elements: dict
        suboptions:
            visibility:
                description:
                    - Ingress visibility.
                type: str
                default: Public
                choices:
                    - Public
                    - Private
            name:
                description:
                    - Name of the ingress  (immutable).
                type: str
                default: default
                choices:
                    - default
            ip:
                description:
                    - IP of the ingress (immutable), only appears in response.
                type: str
    provisioning_state:
        description:
            - The current deployment or provisioning state, which only appears in the response.
        type: str
    state:
        description:
            - Assert the state of the OpenShiftManagedCluster.
            - Use C(present) to create or update an OpenShiftManagedCluster and C(absent) to delete it.
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
    - Haiyuan Zhang (@haiyuazhang)
'''

EXAMPLES = '''
- name: Create openshift cluster
  azure_rm_openshiftmanagedcluster:
    resource_group: "myResourceGroup"
    name: "myCluster"
    location: "eastus"
    cluster_profile:
      cluster_resource_group_id: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/clusterResourceGroup"
      domain: "mydomain"
    service_principal_profile:
      client_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      client_secret: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    network_profile:
      pod_cidr: "10.128.0.0/14"
      service_cidr: "172.30.0.0/16"
    worker_profiles:
      - name: worker
        vm_size: "Standard_D4s_v3"
        subnet_id: "/subscriptions/xx-xx-xx-xx-xx/resourceGroups/myResourceGroup/Microsoft.Network/virtualNetworks/myVnet/subnets/worker"
        disk_size: 128
        count: 3
    master_profile:
      vm_size: "Standard_D8s_v3"
      subnet_id: "/subscriptions/xx-xx-xx-xx-xx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/myVnet/subnets/master"
- name: Create openshift cluster with multi parameters
  azure_rm_openshiftmanagedcluster:
    resource_group: "myResourceGroup"
    name: "myCluster"
    location: "eastus"
    cluster_profile:
      cluster_resource_group_id: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/clusterResourceGroup"
      domain: "mydomain"
      fips_validated_modules: Enabled
    service_principal_profile:
      client_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      client_secret: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    network_profile:
      pod_cidr: "10.128.0.0/14"
      service_cidr: "172.30.0.0/16"
      outbound_type: Loadbalancer
      preconfigured_nsg: Disabled
    worker_profiles:
      - name: worker
        vm_size: "Standard_D4s_v3"
        subnet_id: "/subscriptions/xx-xx-xx-xx-xx/resourceGroups/myResourceGroup/Microsoft.Network/virtualNetworks/myVnet/subnets/worker"
        disk_size: 128
        count: 3
        encryption_at_host: Disabled
    master_profile:
      vm_size: "Standard_D8s_v3"
      subnet_id: "/subscriptions/xx-xx-xx-xx-xx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/myVnet/subnets/master"
      encryption_at_host: Disabled
- name: Delete OpenShift Managed Cluster
  azure_rm_openshiftmanagedcluster:
    resource_group: myResourceGroup
    name: myCluster
    location: eastus
    state: absent

- name: Create openshift cluster with managed identity
  azure_rm_openshiftmanagedcluster:
    resource_group: "myResourceGroup"
    name: "myCluster"
    location: "eastus"
    identity:
      type: UserAssigned
      user_assigned_identities:
        id:
          - "/subscriptions/xx-xx/resourceGroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aro-cluster-identity"
    cluster_profile:
      cluster_resource_group_id: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/clusterResourceGroup"
      domain: "mydomain"
    platform_workload_identity_profile:
      platform_workload_identities:
        ClusterOperator.OpenShift.IO/cloud-controller-manager:
          resource_id: "/subscriptions/xx-xx/resourceGroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aro-ccm"
        ClusterOperator.OpenShift.IO/ingress:
          resource_id: "/subscriptions/xx-xx/resourceGroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aro-ingress"
        ClusterOperator.OpenShift.IO/image-registry:
          resource_id: "/subscriptions/xx-xx/resourceGroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aro-registry"
        ClusterOperator.OpenShift.IO/machine-api:
          resource_id: "/subscriptions/xx-xx/resourceGroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aro-machine"
        ClusterOperator.OpenShift.IO/cloud-network-config:
          resource_id: "/subscriptions/xx-xx/resourceGroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aro-network"
        CloudControllerManager.ARO.OpenShift.IO:
          resource_id: "/subscriptions/xx-xx/resourceGroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aro-cloud"
        ServiceOperator.ARO.OpenShift.IO:
          resource_id: "/subscriptions/xx-xx/resourceGroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aro-service"
    network_profile:
      pod_cidr: "10.128.0.0/14"
      service_cidr: "172.30.0.0/16"
    worker_profiles:
      - name: worker
        vm_size: "Standard_D4s_v3"
        subnet_id: "/subscriptions/xx-xx/resourceGroups/myResourceGroup/Microsoft.Network/virtualNetworks/myVnet/subnets/worker"
        disk_size: 128
        count: 3
    master_profile:
      vm_size: "Standard_D8s_v3"
      subnet_id: "/subscriptions/xx-xx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/myVnet/subnets/master"
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
identity:
    description:
        - The managed service identities assigned to the cluster.
    returned: when configured
    type: complex
    contains:
        type:
            description:
                - Type of managed service identity.
            type: str
            sample: UserAssigned
        userAssignedIdentities:
            description:
                - The set of user assigned identities associated with the resource.
            type: dict
            sample: {"/subscriptions/xx/resourceGroups/rg/providers/Microsoft.ManagedIdentity/userAssignedIdentities/id": {}}
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
                fipsValidatedModules:
                    description:
                        - If FIPS validated crypto modules are used
                    type: str
                    returned: always
                    sample: Enabled
        servicePrincipalProfile:
            description:
                - Service principal.
            type: complex
            returned: when configured
            contains:
                clientId:
                    description: Client ID of the service principal.
                    returned: always
                    type: str
                    sample: xxxxxxxx-xxxx-xxxx-xxxxxxxxxxxx
        platformWorkloadIdentityProfile:
            description:
                - The workload identity profile.
            type: complex
            returned: when configured
            contains:
                platformWorkloadIdentities:
                    description:
                        - Dictionary of operator names to workload identity configurations.
                    type: dict
                    returned: always
                upgradeableTo:
                    description:
                        - The OpenShift version the cluster can be upgraded to.
                    type: str
                    returned: when available
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
                outboundType:
                    description:
                        - The OutboundType used for egress traffic.
                    type: str
                    returned: always
                    sample: Loadbalancer
                preconfiguredNSG:
                    description:
                        - Specifies whether subnets are pre-attached with an NSG
                    type: str
                    returned: always
                    sample: Disabled
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
                encryptionAtHost:
                    description:
                        - Whether master virtual machines are encrypted at host.
                    type: str
                    returned: always
                    sample: Disabled
                disk_encryption_set_id:
                    description:
                        - The resource ID of an associated DiskEncryptionSet, if applicable.
                    type: str
                    returned: successd
                    sample: null
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
                encryptionAtHost:
                    description:
                        - Whether worker virtual machines are encrypted at host.
                    type: str
                    returned: always
                    sample: Disabled
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

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient
    from azure.mgmt.redhatopenshift.models import (ManagedServiceIdentity, UserAssignedIdentity)
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMOpenShiftManagedClusters(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
                required=True
            ),
            cluster_profile=dict(
                type='dict',
                default=dict(),
                options=dict(
                    pull_secret=dict(
                        type='str',
                        no_log=True,
                    ),
                    cluster_resource_group_id=dict(
                        type='str',
                    ),
                    domain=dict(
                        type='str',
                    ),
                    version=dict(
                        type='str',
                    ),
                    fips_validated_modules=dict(
                        type='str',
                        choices=['Enabled', 'Disabled'],
                        default='Enabled'
                    ),
                ),
            ),
            service_principal_profile=dict(
                type='dict',
                options=dict(
                    client_id=dict(
                        type='str',
                    ),
                    client_secret=dict(
                        type='str',
                        no_log=True,
                    )
                )
            ),
            identity=dict(
                type='dict',
                options=self.managed_identity_multiple_spec,
                required_if=[
                    ('type', 'UserAssigned', ['user_assigned_identities']),
                    ('type', 'SystemAssigned, UserAssigned', ['user_assigned_identities']),
                ]
            ),
            platform_workload_identity_profile=dict(
                type='dict',
                options=dict(
                    platform_workload_identities=dict(
                        type='dict',
                    ),
                    upgradeable_to=dict(
                        type='str',
                    )
                )
            ),
            network_profile=dict(
                type='dict',
                options=dict(
                    pod_cidr=dict(
                        type='str',
                    ),
                    service_cidr=dict(
                        type='str',
                    ),
                    outbound_type=dict(
                        type='str',
                        choices=['Loadbalancer', 'UserDefinedRouting']
                    ),
                    preconfigured_nsg=dict(
                        type='str',
                        choices=['Disabled', 'Enabled'],
                        default='Disabled'
                    )
                ),
                default=dict(
                    pod_cidr="10.128.0.0/14",
                    service_cidr="172.30.0.0/16"
                )
            ),
            master_profile=dict(
                type='dict',
                options=dict(
                    vm_size=dict(
                        type='str'
                    ),
                    subnet_id=dict(
                        type='str',
                        required=True
                    ),
                    encryption_at_host=dict(
                        type='str',
                        choices=['Disabled', 'Enabled'],
                        default='Disabled'
                    ),
                    disk_encryption_set_id=dict(
                        type='str'
                    )
                )
            ),
            worker_profiles=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(
                        type='str',
                        required=True,
                        choices=['worker']
                    ),
                    count=dict(
                        type='int',
                    ),
                    vm_size=dict(
                        type='str'
                    ),
                    subnet_id=dict(
                        type='str',
                        required=True
                    ),
                    disk_size=dict(
                        type='int',
                    ),
                    encryption_at_host=dict(
                        type='str',
                        choices=['Disabled', 'Enabled'],
                        default='Disabled'
                    ),
                    disk_encryption_set_id=dict(
                        type='str'
                    )
                )
            ),
            api_server_profile=dict(
                type='dict',
                options=dict(
                    visibility=dict(
                        type='str',
                        choices=['Public', 'Private'],
                        default='Public'
                    ),
                    url=dict(
                        type='str',
                    ),
                    ip=dict(
                        type='str',
                    )
                )
            ),
            ingress_profiles=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(
                        type='str',
                        choices=['default'],
                        default='default'
                    ),
                    visibility=dict(
                        type='str',
                        choices=['Public', 'Private'],
                        default='Public'
                    ),
                    ip=dict(
                        type='str',
                    )
                )
            ),
            provisioning_state=dict(
                type='str',
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.identity = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200, 201, 202]
        self.to_do = Actions.NoAction

        self.body = {}
        self.body['properties'] = {}
        self.query_parameters = {}
        self.header_parameters = {}
        self._managed_identity = None

        self.query_parameters['api-version'] = '2025-07-25'
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(AzureRMOpenShiftManagedClusters, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                              supports_check_mode=True,
                                                              supports_tags=True)

    @property
    def managed_identity(self):
        if not self._managed_identity:
            self._managed_identity = {"identity": ManagedServiceIdentity,
                                      "user_assigned": UserAssignedIdentity}
        return self._managed_identity

    def format_for_body(self, identity):
        if identity:
            identity = identity.as_dict()
            if identity.get("user_assigned_identities"):
                identity["userAssignedIdentities"] = identity.pop("user_assigned_identities")
        return identity

    def format_for_helper(self, identity):
        if identity and identity.get("userAssignedIdentities"):
            identity["user_assigned_identities"] = identity.pop("userAssignedIdentities")
        return identity

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == 'cluster_profile':
                    self.body['properties']['clusterProfile'] = {}
                    for item in ['pull_secret', 'cluster_resource_group_id', 'domain', 'version', 'fips_validated_modules']:
                        if not kwargs[key].get(item):
                            continue
                        if item == 'pull_secret':
                            self.body['properties']['clusterProfile']['pullSecret'] = kwargs[key].get(item)
                        elif item == 'cluster_resource_group_id':
                            self.body['properties']['clusterProfile']['resourceGroupId'] = kwargs[key].get(item)
                        elif item == 'domain':
                            self.body['properties']['clusterProfile']['domain'] = kwargs[key].get(item)
                        elif item == 'version':
                            self.body['properties']['clusterProfile']['version'] = kwargs[key].get(item)
                        elif item == 'fips_validated_modules':
                            self.body['properties']['clusterProfile']['fipsValidatedModules'] = kwargs[key].get(item)
                elif key == 'service_principal_profile':
                    sp = kwargs[key]
                    if sp.get('client_id') and sp.get('client_secret'):
                        self.body['properties']['servicePrincipalProfile'] = {}
                        self.body['properties']['servicePrincipalProfile']['clientId'] = sp.get('client_id')
                        self.body['properties']['servicePrincipalProfile']['clientSecret'] = sp.get('client_secret')
                elif key == 'platform_workload_identity_profile':
                    pwi_profile = {}
                    pwi = kwargs[key].get('platform_workload_identities')
                    if pwi:
                        pwi_body = {}
                        for operator_name, identity_config in pwi.items():
                            pwi_body[operator_name] = {}
                            if isinstance(identity_config, dict) and identity_config.get('resource_id'):
                                pwi_body[operator_name]['resourceId'] = identity_config['resource_id']
                        pwi_profile['platformWorkloadIdentities'] = pwi_body
                    if kwargs[key].get('upgradeable_to'):
                        pwi_profile['upgradeableTo'] = kwargs[key]['upgradeable_to']
                    self.body['properties']['platformWorkloadIdentityProfile'] = pwi_profile
                elif key == 'network_profile':
                    self.body['properties']['networkProfile'] = {}
                    for item in kwargs[key].keys():
                        value = kwargs[key].get(item)
                        if value is None:
                            continue
                        if item == 'pod_cidr':
                            self.body['properties']['networkProfile']['podCidr'] = value
                        elif item == 'service_cidr':
                            self.body['properties']['networkProfile']['serviceCidr'] = value
                        elif item == 'outbound_type':
                            self.body['properties']['networkProfile']['outboundType'] = value
                        elif item == 'preconfigured_nsg':
                            self.body['properties']['networkProfile']['preconfiguredNSG'] = value
                elif key == 'master_profile':
                    self.body['properties']['masterProfile'] = {}
                    if kwargs[key].get('subnet_id') is not None:
                        self.body['properties']['masterProfile']['subnetId'] = kwargs[key].get('subnet_id')
                    if kwargs[key].get('disk_encryption_set_id') is not None:
                        self.body['properties']['masterProfile']['diskEncryptionSetId'] = kwargs[key].get('disk_encryption_set_id')
                    if kwargs[key].get('encryption_at_host') is not None:
                        self.body['properties']['masterProfile']['encryptionAtHost'] = kwargs[key].get('encryption_at_host')
                    if kwargs[key].get('vm_size') is not None:
                        self.body['properties']['masterProfile']['vmSize'] = kwargs[key].get('vm_size')
                elif key == 'worker_profiles':
                    self.body['properties']['workerProfiles'] = []
                    for item in kwargs[key]:
                        worker_profile = {}
                        if item.get('name') is not None:
                            worker_profile['name'] = item['name']
                        if item.get('subnet_id') is not None:
                            worker_profile['subnetId'] = item['subnet_id']
                        if item.get('count') is not None:
                            worker_profile['count'] = item['count']
                        if item.get('vm_size') is not None:
                            worker_profile['vmSize'] = item['vm_size']
                        if item.get('disk_size') is not None:
                            worker_profile['diskSizeGB'] = item['disk_size']
                        if item.get('encryption_at_host') is not None:
                            worker_profile['encryptionAtHost'] = item['encryption_at_host']
                        if item.get('disk_encryption_set_id') is not None:
                            worker_profile['diskEncryptionSetId'] = item['disk_encryption_set_id']

                        self.body['properties']['workerProfiles'].append(worker_profile)
                elif key == 'api_server_profile':
                    self.body['properties']['apiserverProfile'] = kwargs[key]
                elif key == 'ingress_profiles':
                    self.body['properties']['ingressProfiles'] = kwargs[key]
                elif key == 'provisioning_state':
                    self.body['properties']['provisioningState'] = kwargs[key]
                else:
                    self.body[key] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

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

        old_response = self.get_resource()

        # Handle managed identity
        if self.identity:
            old_identity = self.format_for_helper((old_response or {}).get('identity') or {})
            update_identity, identity = self.update_managed_identity(
                new_identity=self.identity,
                curr_identity=old_identity)
            self.body['identity'] = self.format_for_body(identity)

        if not old_response:
            self.log("OpenShiftManagedCluster instance doesn't exist")

            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log('OpenShiftManagedCluster instance already exists')

            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                modifiers = {}
                # self.create_compare_modifiers(self.module_arg_spec, '', modifiers)
                # self.results['modifiers'] = modifiers
                # self.results['compare'] = []
                # if 'workProfiles' in self.body['properties']:
                #     self.body['properties'].pop('workerProfiles')
                # if not self.default_compare(modifiers, self.body, old_response, '', self.results):
                #     self.to_do = Actions.Update
                self.fail("module doesn't support cluster update yet")

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log('Need to Create / Update the OpenShiftManagedCluster instance')

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_resource()

            self.results['changed'] = True
            self.log('Creation / Update done')
        elif self.to_do == Actions.Delete:
            self.log('OpenShiftManagedCluster instance deleted')
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_resource()

            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_resource():
                time.sleep(20)
        else:
            self.log('OpenShiftManagedCluster instance unchanged')
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]
            self.results["name"] = response["name"]
            self.results["type"] = response["type"]
            self.results["location"] = response["location"]
            self.results["properties"] = response["properties"]
            if response.get("identity"):
                self.results["identity"] = response["identity"]

        return self.results

    def create_update_resource(self):

        if self.to_do == Actions.Create:
            required_profile_for_creation = ["workerProfiles", "clusterProfile", "masterProfile"]

            if 'properties' not in self.body:
                self.fail('{0} are required for creating a openshift cluster'.format(
                    '[worker_profile, cluster_profile, master_profile]'))
            for profile in required_profile_for_creation:
                if profile not in self.body['properties']:
                    self.fail('{0} is required for creating a openshift cluster'.format(profile))

            # Validate authentication: require either service_principal_profile or identity (not both)
            has_sp = 'servicePrincipalProfile' in self.body['properties']
            has_identity = 'identity' in self.body
            if has_sp and has_identity:
                self.fail('service_principal_profile and identity are mutually exclusive. '
                          'Provide either service_principal_profile or identity, not both.')
            if not has_sp and not has_identity:
                self.fail('Either service_principal_profile or identity is required for creating a openshift cluster.')
            if has_identity:
                pwi_profile = self.body['properties'].get('platformWorkloadIdentityProfile', {})
                pwi = pwi_profile.get('platformWorkloadIdentities', {})
                if not pwi_profile or not pwi:
                    self.fail('platform_workload_identity_profile with at least one platform_workload_identities entry '
                              'is required when using managed identity.')
                for operator_name, identity_config in pwi.items():
                    if not identity_config.get('resourceId'):
                        self.fail("platform_workload_identities entry '{0}' is missing required field 'resource_id'.".format(
                            operator_name))

            self.set_default()

        try:
            response = self.mgmt_client.query(self.url,
                                              'PUT',
                                              self.query_parameters,
                                              self.header_parameters,
                                              self.body,
                                              self.status_code,
                                              600,
                                              30)
        except Exception as exc:
            self.log('Error attempting to create the OpenShiftManagedCluster instance.')
            self.fail('Error creating the OpenShiftManagedCluster instance: {0}'
                      '\n{1}'.format(str(self.body), str(exc)))
        if hasattr(response, 'body'):
            response = json.loads(response.body())
        elif hasattr(response, 'context'):
            response = response.context['deserialized_data']
        else:
            self.fail("Create or Updating fail, no match message return, return info as {0}".format(response))

        return response

    def delete_resource(self):
        # self.log('Deleting the OpenShiftManagedCluster instance {0}'.format(self.))
        try:
            response = self.mgmt_client.query(self.url,
                                              'DELETE',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
        except Exception as e:
            self.log('Error attempting to delete the OpenShiftManagedCluster instance.')
            self.fail('Error deleting the OpenShiftManagedCluster instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        # self.log('Checking if the OpenShiftManagedCluster instance {0} is present'.format(self.))
        found = False
        try:
            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            found = True
            response = json.loads(response.body())
            found = True
            self.log("Response : {0}".format(response))
            # self.log("OpenShiftManagedCluster instance : {0} found".format(response.name))
        except Exception as e:
            self.log('Did not find the OpenShiftManagedCluster instance.')
        if found is True:
            return response

        return False

#    def random_id(self):
#        import random
#        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(8))

# Added per Mangirdas Judeikis (RED HAT INC) to fix first letter of cluster domain beginning with digit ; currently not supported
    def random_id(self):
        random_id = (''.join(random.choice('abcdefghijklmnopqrstuvwxyz')) +
                     ''.join(random.choice('abcdefghijklmnopqrstuvwxyz1234567890')
                             for key in range(7)))
        return random_id
###

    def set_default(self):
        if 'apiserverProfile' not in self.body['properties']:
            api_profile = dict(visibility="Public")
            self.body['properties']['apiserverProfile'] = api_profile
        if 'ingressProfiles' not in self.body['properties']:
            ingress_profile = dict(visibility="Public", name="default")
            self.body['properties']['ingressProfiles'] = [ingress_profile]
        else:
            # hard code the ingress profile name as default, so user don't need to specify it
            for profile in self.body['properties']['ingressProfiles']:
                profile['name'] = "default"
        if 'name' not in self.body['properties']['workerProfiles'][0]:
            self.body['properties']['workerProfiles'][0]['name'] = 'worker'
        if 'vmSize' not in self.body['properties']['workerProfiles'][0]:
            self.body['properties']['workerProfiles'][0]['vmSize'] = "Standard_D4s_v3"
        if 'diskSizeGB' not in self.body['properties']['workerProfiles'][0]:
            self.body['properties']['workerProfiles'][0]['diskSizeGB'] = 128
        if 'vmSize' not in self.body['properties']['masterProfile']:
            self.body['properties']['masterProfile']['vmSize'] = "Standard_D8s_v3"
        if 'pullSecret' not in self.body['properties']['clusterProfile']:
            self.body['properties']['clusterProfile']['pullSecret'] = ''
        if 'resourceGroupId' not in self.body['properties']['clusterProfile']:
            resourcegroup_id = "/subscriptions/" + self.subscription_id + "/resourceGroups/" + self.name + "-cluster"
            self.body['properties']['clusterProfile']['resourceGroupId'] = resourcegroup_id
        # if domain is not set in cluster profile or it is set to an empty string or null value then generate a random domain
        if 'domain' not in self.body['properties']['clusterProfile'] or not self.body['properties']['clusterProfile']['domain']:
            self.body['properties']['clusterProfile']['domain'] = self.random_id()


def main():
    AzureRMOpenShiftManagedClusters()


if __name__ == '__main__':
    main()
