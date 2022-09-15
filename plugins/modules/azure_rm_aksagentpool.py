#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_aksagentpool
version_added: '1.14.0'
short_description: Manage node pools in Kubernetes kubernetes cluster
description:
    - Create, update or delete node pools in kubernetes cluster.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: True
    cluster_name:
        description:
            - The name of the kubernetes cluster.
        type: str
        required: True
    name:
        description:
            - The name of the node agent pool.
        type: str
        required: True
    count:
        description:
            - Number of agents (VMs) to host docker containers.
        type: int
    vm_size:
        description:
            - Size of agent VMs
        type: str
    os_disk_size_gb:
        description:
            - OS Disk Size in GB to be used to specify the disk size for every machine in this master/agent pool.
        type: int
    vnet_subnet_id:
        description:
            - VNet SubnetID specifies the VNet's subnet identifier.
        type: str
    availability_zones:
        description:
            - Availability zones for nodes. Must use VirtualMachineScaleSets AgentPoolType.
        type: list
        elements: int
        choices:
            - 1
            - 2
            - 3
    os_type:
        description:
            - OsType to be used to specify os type.
        type: str
        choices:
            - Linux
            - Windows
    orchestrator_version:
        description:
            - Version of orchestrator specified when creating the managed cluster.
        type: str
    type_properties_type:
        description:
            - AgentPoolType represents types of an agent pool.
        type: str
        choices:
            - VirtualMachineScaleSets
            - AvailabilitySet
    mode:
        description:
            - AgentPoolMode represents mode of an agent pool.
        type: str
        choices:
            - System
            - User
    enable_auto_scaling:
        description:
            - Whether to enable auto-scaler.
        type: bool
    max_count:
        description:
            - Maximum number of nodes for auto-scaling.
        type: int
    node_labels:
        description:
            -  Agent pool node labels to be persisted across all nodes in agent pool.
        type: dict
    min_count:
        description:
            - Minimum number of nodes for auto-scaling.
        type: int
    max_pods:
        description:
            - Maximum number of pods that can run on a node.
        type: int
    state:
        description:
            - State of the automation runbook. Use C(present) to create or update a automation runbook and use C(absent) to delete.
        type: str
        default: present
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred Sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Add new node agent pool
  azure_rm_aksagentpool:
    resource_group: "{{ resource_group }}"
    cluster_name: aksfred01
    name: default-new
    count: 2
    vm_size: Standard_B2s
    type_properties_type: VirtualMachineScaleSets
    mode: System
    node_labels: {"release":"stable"}
    max_pods: 42
    orchestrator_version: 1.23.5
    availability_zones:
      - 1
      - 2
- name: Delete node agent pool
  azure_rm_aksagentpool:
    resource_group: "{{ resource_group }}"
    cluster_name: aksfred01
    name: default-new
'''

RETURN = '''
aks_agent_pools:
    description:
        - Details for a node pool in the managed Kubernetes cluster.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            type: str
            returned: always
            sample: "/subscriptions/xxx-xxxf/resourcegroups/myRG/providers/Microsoft.ContainerService/managedClusters/cluster/agentPools/default"
        resource_group:
            description:
                - Resource group name.
            type: str
            returned: always
            sample: myRG
        name:
            description:
                - Resource name.
            type: str
            returned: always
            sample: default
        cluster_name:
            description:
                - The cluster name.
            type: str
            returned: always
            sample: testcluster
        availability_zones:
            description:
                - Availability zones for nodes. Must use VirtualMachineScaleSets AgentPoolType.
            type: list
            returned: always
            sample: [1, 2]
        count:
            description:
                - Number of agents (VMs) to host docker containers.
            type: int
            returned: always
            sample: 2
        enable_auto_scaling:
            description:
                - Whether to enable auto-scaler.
            type: str
            returned: always
            sample: null
        enable_node_public_ip:
            description:
                -  Enable public IP for nodes.
            type: str
            returned: always
            sample: bool
        max_count:
            description:
                - Maximum number of nodes for auto-scaling.
            type: int
            returned: always
            sample: 10
        min_count:
            description:
                - Minimum number of nodes for auto-scaling.
            type: int
            returned: always
            sample: 1
        max_pods:
            description:
                - Maximum number of pods that can run on a node.
            type: int
            returned: always
            sample: 42
        mode:
            description:
                - AgentPoolMode represents mode of an agent pool.
            type: str
            returned: always
            sample: System
        node_image_version:
            description:
                - Version of node image.
            type: str
            returned: always
            sample: AKSUbuntu-1804gen2containerd-2022.08.23
        node_labels:
            description:
                - Agent pool node labels to be persisted across all nodes in agent pool.
            type: list
            returned: always
            sample: ["release": "stable"]
        node_taints:
            description:
                - Taints added to new nodes during node pool create and scale.
            type: str
            returned: always
            sample: null
        orchestrator_version:
            description:
                - Version of orchestrator specified when creating the managed cluster.
            type: str
            returned: always
            sample: 1.22.11
        os_disk_size_gb:
            description:
                - OS Disk Size in GB to be used to specify the disk size for every machine in this master/agent pool.
            type: int
            returned: always
            sample: 128
        os_type:
            description:
                - OsType to be used to specify os type.
            type: str
            returned: always
            sample: Linux
        provisioning_state:
            description:
                - The current deployment or provisioning state, which only appears in the response.
            type: str
            returned: always
            sample: Succeeded
        scale_set_eviction_policy:
            description:
                - ScaleSetEvictionPolicy to be used to specify eviction policy for Spot virtual machine scale set.
            type: str
            returned: always
            sample: null
        scale_set_priority:
            description:
                - caleSetPriority to be used to specify virtual machine scale set priority.
            type: str
            returned: always
            sample: null
        spot_max_price:
            description:
                - SpotMaxPrice to be used to specify the maximum price you are willing to pay in US Dollars.
            type: float
            returned: always
            sample: null
        type:
            description:
                - Resource Type.
            type: str
            returned: always
            sample: Microsoft.ContainerService/managedClusters/agentPools
        type_properties_type:
            description:
                - AgentPoolType represents types of an agent pool.
            type: str
            returned: always
            sample: VirtualMachineScaleSets
        upgrade_settings:
            description:
                - Settings for upgrading the agentpool.
            type: str
            returned: always
            sample: null
        vm_size:
            description:
                - Size of agent VMs.
            type: str
            returned: always
            sample: Standard_B2s
        vnet_subnet_id:
            description:
                - VNet SubnetID specifies the VNet's subnet identifier.
            type: str
            returned: always
            sample: null
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    pass


class AzureRMAksAgentPool(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            cluster_name=dict(
                type='str',
                required=True
            ),
            count=dict(
                type='int',
            ),
            vm_size=dict(
                type='str',
            ),
            os_disk_size_gb=dict(
                type='int'
            ),
            vnet_subnet_id=dict(
                type='str'
            ),
            availability_zones=dict(
                type='list',
                elements='int',
                choices=[1, 2, 3]
            ),
            os_type=dict(
                type='str',
                choices=['Linux', 'Windows']
            ),
            orchestrator_version=dict(
                type='str',
            ),
            type_properties_type=dict(
                type='str',
                choices=['VirtualMachineScaleSets', 'AvailabilitySet']
            ),
            mode=dict(
                type='str',
                choices=['System', 'User'],
            ),
            enable_auto_scaling=dict(
                type='bool'
            ),
            max_count=dict(
                type='int'
            ),
            node_labels=dict(
                type='dict'
            ),
            min_count=dict(
                type='int'
            ),
            max_pods=dict(
                type='int'
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                default='present'
            )
        )
        # store the results of the module operation
        self.results = dict()
        self.resource_group = None
        self.name = None
        self.cluster_name = None
        self.count = None
        self.vm_size = None
        self.mode = None
        self.os_disk_size_gb = None
        self.storage_profiles = None
        self.vnet_subnet_id = None
        self.availability_zones = None
        self.os_type = None
        self.orchestrator_version = None
        self.type_properties_type = None
        self.enable_auto_scaling = None
        self.max_count = None
        self.node_labels = None
        self.min_count = None
        self.max_pods = None
        self.body = dict()

        super(AzureRMAksAgentPool, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec):
            setattr(self, key, kwargs[key])
            if key not in ['resource_group', 'cluster_name', 'name', 'state']:
                self.body[key] = kwargs[key]

        agent_pool = self.get()
        changed = False
        response = None

        if self.state == 'present':
            if agent_pool:
                for key in self.body.keys():
                    if self.body[key] is not None and self.body[key] != agent_pool[key]:
                        changed = True
                    else:
                        self.body[key] = agent_pool[key]
            else:
                changed = True

            if changed:
                if not self.check_mode:
                    response = self.create_or_update(self.body)

        else:
            if not self.check_mode:
                if agent_pool:
                    response = self.delete_agentpool()
                    changed = True
                else:
                    changed = False
            else:
                changed = True

        self.results['changed'] = changed
        self.results['aks_agent_pools'] = response
        return self.results

    def get(self):
        try:
            response = self.managedcluster_client.agent_pools.get(self.resource_group, self.cluster_name, self.name)
            return self.to_dict(response)
        except ResourceNotFoundError:
            pass

    def create_or_update(self, parameters):
        try:
            response = self.managedcluster_client.agent_pools.begin_create_or_update(self.resource_group, self.cluster_name, self.name, parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
            return self.to_dict(response)
        except Exception as exc:
            self.fail('Error when creating cluster node agent pool {0}: {1}'.format(self.name, exc))

    def delete_agentpool(self):
        try:
            response = self.managedcluster_client.agent_pools.begin_delete(self.resource_group, self.cluster_name, self.name)
        except Exception as exc:
            self.fail('Error when deleting cluster agent pool {0}: {1}'.format(self.name, exc))

    def to_dict(self, agent_pool):
        if not agent_pool:
            return None
        agent_pool_dict = dict(
            resource_group=self.resource_group,
            cluster_name=self.cluster_name,
            id=agent_pool.id,
            type=agent_pool.type,
            name=agent_pool.name,
            count=agent_pool.count,
            vm_size=agent_pool.vm_size,
            os_disk_size_gb=agent_pool.os_disk_size_gb,
            vnet_subnet_id=agent_pool.vnet_subnet_id,
            max_pods=agent_pool.max_pods,
            os_type=agent_pool.os_type,
            max_count=agent_pool.max_count,
            min_count=agent_pool.min_count,
            enable_auto_scaling=agent_pool.enable_auto_scaling,
            type_properties_type=agent_pool.type_properties_type,
            mode=agent_pool.mode,
            orchestrator_version=agent_pool.orchestrator_version,
            node_image_version=agent_pool.node_image_version,
            upgrade_settings=agent_pool.upgrade_settings,
            provisioning_state=agent_pool.provisioning_state,
            availability_zones=[],
            enable_node_public_ip=agent_pool.enable_node_public_ip,
            scale_set_priority=agent_pool.scale_set_priority,
            scale_set_eviction_policy=agent_pool.scale_set_eviction_policy,
            spot_max_price=agent_pool.spot_max_price,
            node_labels=agent_pool.node_labels,
            node_taints=agent_pool.node_taints,
        )

        if agent_pool.availability_zones is not None:
            for key in agent_pool.availability_zones:
                agent_pool_dict['availability_zones'].append(int(key))

        return agent_pool_dict


def main():
    AzureRMAksAgentPool()


if __name__ == '__main__':
    main()
