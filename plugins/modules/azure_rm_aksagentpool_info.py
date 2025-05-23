#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_aksagentpool_info
version_added: '1.14.0'
short_description: Show the details for a node pool in the managed Kubernetes cluster
description:
    - Get the details for a node pool in the managed Kubernetes cluster.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: True
    cluster_name:
        description:
            - The cluster name.
        type: str
        required: True
    name:
        description:
            - The node pool name.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get node agent pool by cluster name
  azure_rm_aksagentpool_info:
    resource_group: myRG
    cluster_name: testcluster

- name: Get node agent pool by name
  azure_rm_aksagentpool_info:
    resource_group: myRG
    cluster_name: testcluster
    name: default
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
            type: bool
            returned: always
            sample: null
        enable_node_public_ip:
            description:
                -  Enable public IP for nodes.
            type: bool
            returned: always
            sample: True
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
            sample: ["release":"stable"]
        node_taints:
            description:
                - Taints added to new nodes during node pool create and scale.
            type: list
            returned: always
            sample: ["CriticalAddonsOnly=false:NoSchedule"]
        orchestrator_version:
            description:
                - Version of orchestrator specified when creating the managed cluster.
            type: str
            returned: always
            sample: 1.22.11
        os_disk_size_gb:
            description:
                - OS Disk Size in GB to be used to specify the disk size for every machine in this master agent pool.
            type: int
            returned: always
            sample: 128
        os_type:
            description:
                - OsType to be used to specify os type.
            type: str
            returned: always
            sample: Linux
        os_sku:
            description:
                - OS SKU to be used to specify os type.
            type: str
            returned: always
            sample: Windows2022
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
        security_profile:
            description:
                - The security settings of an agent pool.
            type: complex
            contains:
                enable_secure_boot:
                    description:
                        - The secure boot is diabled or enabled.
                    type: bool
                    returned: always
                    sample: true
                enable_vtpm:
                    description:
                        - The vTPM is diabled or enabled.
                    type: bool
                    returned: always
                    sample: true
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
        kubelet_config:
            description:
                - The Kubelet configuration on the agent pool nodes.
            type: dict
            returned: always
            sample: {
                    cpu_cfs_quota: true,
                    cpu_cfs_quota_period: 100ms,
                    cpu_manager_policy: static,
                    fail_swap_on: false,
                    image_gc_high_threshold: 85,
                    image_gc_low_threshold: 80,
                    topology_manager_policy: none
                }
        linux_os_config:
            description:
                - The OS configuration of Linux agent nodes.
            type: dict
            returned: always
            sample: {
                    swap_file_size_mb: 1500,
                    sysctls: {},
                    transparent_huge_page_defrag: defer+madvise,
                    transparent_huge_page_enabled: madvise
                }
        power_state:
            description:
                - The agent pool's power state.
            type: dict
            returned: always
            sample: {code: Running}
        tags:
            description:
                - The tags of the node agent pool.
            type: dict
            returned: always
            sample: {key1: value1, key2: value2}
        kubelet_disk_type:
            description:
                - Determines the placement of emptyDir volumes, container runtime data root, and Kubelet ephemeral storage.
            type: str
            returned: always
            sample: OS
        workload_runtime:
            description:
                - Determines the type of workload a node can run.
            type: str
            returned: always
            sample: OCIContainer
        scale_down_mode:
            description:
                - This also effects the cluster autoscaler behavior.
            type: str
            returned: always
            sample: Delete
        node_public_ip_prefix_id:
            description:
                - The Azure Public IP prefix's ID.
            type: str
            returned: always
            sample: null
        proximity_placement_group_id:
            description:
                - The ID for Proximity Placement Group.
            type: str
            returned: always
            sample: /subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Compute/proximityPlacementGroups/proxi01
        enable_encryption_at_host:
            description:
                - This is only supported on certain VM sizes and in certain Azure regions.
            type: bool
            returned: always
            sample: false
        enable_ultra_ssd:
            description:
                - Whether enable FIPS node pool.
            type: bool
            returned: always
            sample: false
        gpu_instance_profile:
            description:
                - GPUInstanceProfile to be used to specify GPU MIG instance profile for supported GPU VM SKU.
            type: str
            returned: always
            sample: MIG1g
        windows_profile:
            description:
                - The Windows agent pool's specific profile.
            type: dict
            returned: when-used
            sample: {"disable_outbound_nat": false}
        network_profile:
            description:
                - Network-related settings of an agent pool.
            type: complex
            returned: when-used
            contains:
                allowed_host_ports:
                    description:
                        - The port ranges that are allowed to access.
                    type: list
                    returned: always
                    sample: [{"port_end": 200, "port_start": 10, "protocol": "TCP"}]
                application_security_groups:
                    description:
                        - The IDs of the application security groups which agent pool will associate when created.
                    type: list
                    returned: always
                    sample: ["/subscriptions/xxxxxx/resourceGroups/testRG/providers/Microsoft.Network/applicationSecurityGroups/appnsg"]
        pod_subnet_id:
            description:
                - The subnet ID.
            type: str
            returned: always
            sample: "/subscriptions/xxxx/resourceGroups/testRG/providers/Microsoft.Network/virtualNetworks/My_Virtual_Network/subnets/foobar"
        host_group_id:
            description:
                - The host group ID.
            type: str
            returned: always
            sample: "/subscriptions/xxxxx/resourceGroups/testRG/providers/Microsoft.Compute/hostGroups/hostgroup"
        capacity_reservation_group_id:
            description:
                - The ID of Capacity Reservation Group.
            returned: always
            type: str
            sample: "/subscriptions/xxxxx/resourceGroups/testRG/providers/Microsoft.Compute/capacityReservationGroups/crgid"
        os_disk_type:
            description:
                - The type of the OS disk.
            returned: always
            sample: Managed
            type: str
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass


class AzureRMAgentPoolInfo(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            cluster_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict()
        self.resource_group = None
        self.name = None
        self.cluster_name = None

        super(AzureRMAgentPoolInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec):
            setattr(self, key, kwargs[key])

        if self.name:
            aks_agent_pools = [self.get_agentpool()]
        else:
            aks_agent_pools = self.list_agentpool()
        self.results['aks_agent_pools'] = [self.to_dict(x) for x in aks_agent_pools]
        return self.results

    def get_agentpool(self):
        try:
            return self.managedcluster_client.agent_pools.get(self.resource_group, self.cluster_name, self.name)
        except ResourceNotFoundError:
            pass

    def list_agentpool(self):
        result = []
        try:
            resp = self.managedcluster_client.agent_pools.list(self.resource_group, self.cluster_name)
            while True:
                result.append(resp.next())
        except StopIteration:
            pass
        except Exception:
            pass
        return result

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
            os_sku=agent_pool.os_sku,
            max_count=agent_pool.max_count,
            min_count=agent_pool.min_count,
            enable_auto_scaling=agent_pool.enable_auto_scaling,
            type_properties_type=agent_pool.type_properties_type,
            mode=agent_pool.mode,
            availability_zones=[],
            orchestrator_version=agent_pool.orchestrator_version,
            node_image_version=agent_pool.node_image_version,
            upgrade_settings=dict(),
            provisioning_state=agent_pool.provisioning_state,
            enable_node_public_ip=agent_pool.enable_node_public_ip,
            scale_set_priority=agent_pool.scale_set_priority,
            scale_set_eviction_policy=agent_pool.scale_set_eviction_policy,
            spot_max_price=agent_pool.spot_max_price,
            node_labels=agent_pool.node_labels,
            node_taints=agent_pool.node_taints,
            tags=agent_pool.tags,
            kubelet_disk_type=agent_pool.kubelet_disk_type,
            workload_runtime=agent_pool.workload_runtime,
            scale_down_mode=agent_pool.scale_down_mode,
            power_state=dict(),
            node_public_ip_prefix_id=agent_pool.node_public_ip_prefix_id,
            proximity_placement_group_id=agent_pool.proximity_placement_group_id,
            kubelet_config=dict(),
            linux_os_config=dict(),
            security_profile=dict(),
            enable_encryption_at_host=agent_pool.enable_encryption_at_host,
            enable_ultra_ssd=agent_pool.enable_ultra_ssd,
            enable_fips=agent_pool.enable_fips,
            gpu_instance_profile=agent_pool.gpu_instance_profile,
            os_disk_type=agent_pool.os_disk_type,
            capacity_reservation_group_id=agent_pool.capacity_reservation_group_id,
            host_group_id=agent_pool.host_group_id,
            pod_subnet_id=agent_pool.pod_subnet_id,
            network_profile=dict(),
            windows_profile=dict(),
        )

        if agent_pool.upgrade_settings is not None:
            agent_pool_dict['upgrade_settings']['max_surge'] = agent_pool.upgrade_settings.max_surge
        else:
            agent_pool_dict['upgrade_settings'] = None

        if agent_pool.availability_zones is not None:
            for key in agent_pool.availability_zones:
                agent_pool_dict['availability_zones'].append(int(key))
        else:
            agent_pool_dict['availability_zones'] = None

        if agent_pool.kubelet_config is not None:
            agent_pool_dict['kubelet_config'] = agent_pool.kubelet_config.as_dict()
        else:
            agent_pool_dict['kubelet_config'] = None

        if agent_pool.linux_os_config is not None:
            agent_pool_dict['linux_os_config']['transparent_huge_page_enabled'] = agent_pool.linux_os_config.transparent_huge_page_enabled
            agent_pool_dict['linux_os_config']['transparent_huge_page_defrag'] = agent_pool.linux_os_config.transparent_huge_page_defrag
            agent_pool_dict['linux_os_config']['swap_file_size_mb'] = agent_pool.linux_os_config.swap_file_size_mb
            agent_pool_dict['linux_os_config']['sysctls'] = dict()
            if agent_pool.linux_os_config.sysctls is not None:
                agent_pool_dict['linux_os_config']['sysctls'] = agent_pool.linux_os_config.sysctls.as_dict()
            else:
                agent_pool_dict['linux_os_config']['sysctls'] = None
        else:
            agent_pool_dict['linux_os_config'] = None

        if agent_pool.power_state is not None:
            agent_pool_dict['power_state']['code'] = agent_pool.power_state.code
        else:
            agent_pool_dict['power_state'] = None

        if agent_pool.security_profile is not None:
            agent_pool_dict['security_profile']['enable_vtpm'] = agent_pool.security_profile.enable_vtpm
            agent_pool_dict['security_profile']['enable_secure_boot'] = agent_pool.security_profile.enable_secure_boot
        else:
            agent_pool_dict['security_profile'] = None

        if agent_pool.network_profile is not None:
            agent_pool_dict['network_profile'] = agent_pool.network_profile.as_dict()
        else:
            agent_pool_dict['network_profile'] = None

        if agent_pool.windows_profile is not None:
            agent_pool_dict['windows_profile']['disable_outbound_nat'] = agent_pool.windows_profile.disable_outbound_nat
        else:
            agent_pool_dict['windows_profile'] = None

        return agent_pool_dict


def main():
    AzureRMAgentPoolInfo()


if __name__ == '__main__':
    main()
