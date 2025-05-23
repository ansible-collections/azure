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
            - linux
            - windows
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
    node_taints:
        description:
            - The taints added to new nodes during node pool create and scale.
            - For example as example, value:NoSchedule'.
        type: list
        elements: str
    min_count:
        description:
            - Minimum number of nodes for auto-scaling.
        type: int
    max_pods:
        description:
            - Maximum number of pods that can run on a node.
        type: int
    kubelet_disk_type:
        description:
            - Determines the placement of emptyDir volumes, container runtime data root, and Kubelet ephemeral storage.
        type: str
        choices:
            - OS
            - Temporary
    workload_runtime:
        description:
            - Determines the type of workload a node can run.
        type: str
        choices:
            - OCIContainer
            - WasmWasi
    os_sku:
        description:
            - Specifies an OS SKU.
            - This value must not be specified if OSType is Windows.
            - The I(os_sku=CBLMariner) deprecated. Microsoft recommends that new deployments choose 'AzureLinux' instead.
        type: str
        choices:
            - Ubuntu
            - AzureLinux
            - Windows2019
            - Windows2022
    scale_down_mode:
        description:
            - This also effects the cluster autoscaler behavior.
            - If not specified, it defaults to C(Delete).
        type: str
        default: Delete
        choices:
            - Delete
            - Deallocate
    upgrade_settings:
        description:
            - Settings for upgrading the agentpool.
        type: dict
        suboptions:
            max_surge:
                description:
                    - This can either be set to an integer, sucha as C(5) or percentage C(50%).
                    - If a percentage is specified, it is the percentage of the total agent pool size at the time of the upgrade.
                    - For percentages, fractional nodes are rounded up.
                    - If not specified, the default is C(1).
                type: str
    power_state:
        description:
            - When an Agent Pool is first created it is initially C(Running).
            - The Agent Pool can be stopped by setting this field to C(Stopped).
            -  A stopped Agent Pool stops all of its VMs and does not accrue billing charges.
            - An Agent Pool can only be stopped if it is Running and provisioning state is Succeeded.
        type: dict
        suboptions:
            code:
                description:
                    - Tells whether the cluster is C(Running) or C(Stopped).
                type: str
                choices:
                    - Running
                    - Stopped
    enable_node_public_ip:
        description:
            - Some scenarios may require nodes in a node pool to receive theirown dedicated public IP addresses.
            - A common scenario is for gaming workloads, where a console needs to make a direct connection to a cloud virtual machine to minimize hops.
        type: bool
    scale_set_priority:
        description:
            - The Virtual Machine Scale Set priority.
            - If not specified, the default is C(Regular).
        type: str
        choices:
            - Spot
            - Regular
    node_public_ip_prefix_id:
        description:
            - The Azure Public IP prefix's ID.
        type: str
    scale_set_eviction_policy:
        description:
            - This cannot be specified unless the I(scale_set_priority=Spot).
            - If not specified, the default is C(Delete).
        type: str
        choices:
            - Delete
            - Deallocate
    spot_max_price:
        description:
            - Possible values are any decimal value greater than zero or -1.
            - Indicates the willingness to pay any on-demand price.
        type: float
    proximity_placement_group_id:
        description:
            - The ID for Proximity Placement Group.
        type: str
    kubelet_config:
        description:
            - The Kubelet configuration on the agent pool nodes.
        type: dict
        suboptions:
            cpu_manager_policy:
                description:
                    - Kubernetes CPU management policies.
                    - The default is C(none).
                type: str
                default: none
                choices:
                    - none
                    - static
            cpu_cfs_quota:
                description:
                    - The default is C(true).
                type: bool
                default: true
            cpu_cfs_quota_period:
                description:
                    - The default is C(100ms).
                    - Valid values are a sequence of decimal numbers with an optional fraction and a unit suffix.
                type: str
                default: 100ms
            image_gc_high_threshold:
                description:
                    - To disable image garbage collection, set to C(100).
                    - The default is C(85)
                type: int
                default: 85
            image_gc_low_threshold:
                description:
                    - This cannot be set higher than imageGcHighThreshold.
                    - The default is C(80).
                type: int
                default: 80
            topology_manager_policy:
                description:
                    - Kubernetes Topology Manager policies.
                    - The default is C(none).
                type: str
                default: none
                choices:
                    - none
                    - best-effort
                    - restricted
                    - single-numa-node
            allowed_unsafe_sysctls:
                description:
                    - Allowed list of unsafe sysctls or unsafe sysctl patterns.
                type: list
                elements: str
            fail_swap_on:
                description:
                    - If set to true it will make the Kubelet fail to start if swap is enabled on the node.
                type: bool
            container_log_max_size_mb:
                description:
                    - The maximum size of container log file before it is rotated.
                type: int
            container_log_max_files:
                description:
                    - The maximum number of container log files that can be present for a container. The number must be ≥ 2.
                type: int
            pod_max_pids:
                description:
                    - The maximum number of processes per pod.
                type: int
    linux_os_config:
        description:
            - The OS configuration of Linux agent nodes.
        type: dict
        suboptions:
            sysctls:
                description:
                    - Sysctl settings for Linux agent nodes.
                type: dict
                suboptions:
                    net_core_somaxconn:
                        description:
                            - Sysctl setting net.core.somaxconn.
                        type: int
                    net_core_netdev_max_backlog:
                        description:
                            - Sysctl setting net.core.netdev_max_backlog.
                        type: int
                    net_core_rmem_default:
                        description:
                            - Sysctl setting net.core.rmem_default.
                        type: int
                    net_core_rmem_max:
                        description:
                            - Sysctl setting net.core.rmem_max.
                        type: int
                    net_core_wmem_default:
                        description:
                            - Sysctl setting net.core.wmem_default.
                        type: int
                    net_core_wmem_max:
                        description:
                            - Sysctl setting net.core.wmem_max.
                        type: int
                    net_core_optmem_max:
                        description:
                            - Sysctl setting net.core.optmem_max.
                        type: int
                    net_ipv4_tcp_max_syn_backlog:
                        description:
                            - Sysctl setting net.ipv4.tcp_max_syn_backlog.
                        type: int
                    net_ipv4_tcp_max_tw_buckets:
                        description:
                            - Sysctl setting net.ipv4.tcp_max_tw_buckets.
                        type: int
                    net_ipv4_tcp_fin_timeout:
                        description:
                            - Sysctl setting net.ipv4.tcp_fin_timeout.
                        type: int
                    net_ipv4_tcp_keepalive_time:
                        description:
                            - Sysctl setting net.ipv4.tcp_keepalive_time.
                        type: int
                    net_ipv4_tcp_keepalive_probes:
                        description:
                            - Sysctl setting net.ipv4.tcp_keepalive_probes.
                        type: int
                    net_ipv4_tcpkeepalive_intvl:
                        description:
                            - Sysctl setting net.ipv4.tcp_keepalive_intvl.
                        type: int
                    net_ipv4_tcp_tw_reuse:
                        description:
                            - Sysctl setting net.ipv4.tcp_tw_reuse.
                        type: bool
                    net_ipv4_ip_local_port_range:
                        description:
                            - Sysctl setting net.ipv4.ip_local_port_range.
                        type: str
                    net_ipv4_neigh_default_gc_thresh1:
                        description:
                            - Sysctl setting net.ipv4.neigh.default.gc_thresh1.
                        type: int
                    net_ipv4_neigh_default_gc_thresh2:
                        description:
                            - Sysctl setting net.ipv4.neigh.default.gc_thresh2.
                        type: int
                    net_ipv4_neigh_default_gc_thresh3:
                        description:
                            - Sysctl setting net.ipv4.neigh.default.gc_thresh3.
                        type: int
                    fs_inotify_max_user_watches:
                        description:
                            - Sysctl setting fs.inotify.max_user_watches.
                        type: int
                    fs_file_max:
                        description:
                            - Sysctl setting fs.file-max.
                        type: int
                    fs_aio_max_nr:
                        description:
                            - Sysctl setting fs.aio-max-nr.
                        type: int
                    fs_nr_open:
                        description:
                            - Sysctl setting fs.nr_open.
                        type: int
                    kernel_threads_max:
                        description:
                            - Sysctl setting kernel.threads-max.
                        type: int
                    vm_max_map_count:
                        description:
                            - Sysctl setting vm.max_map_count.
                        type: int
                    vm_swappiness:
                        description:
                            - Sysctl setting vm.swappiness.
                        type: int
                    vm_vfs_cache_pressure:
                        description:
                            - Sysctl setting vm.vfs_cache_pressure.
                        type: int
                    net_netfilter_nf_conntrack_max:
                        description:
                            - sysctl setting net.netfilter.nf_conntrack_max.
                        type: int
                    net_netfilter_nf_conntrack_buckets:
                        description:
                            - Sysctl setting net.netfilter.nf_conntrack_buckets.
                        type: int
            transparent_huge_page_enabled:
                description:
                    - The node agent pool transparent hugepage.
                    - The default is C(always).
                type: str
                default: always
                choices:
                    - always
                    - madvise
                    - never
            transparent_huge_page_defrag:
                description:
                    - The node agent pool transparent huge page deferag.
                    - The default is C(madvise).
                type: str
                default: madvise
                choices:
                    - always
                    - defer
                    - defer+madvise
                    - madvise
                    - never
            swap_file_size_mb:
                description:
                    - The size in MB of a swap file that will be created on each node.
                type: int
    enable_encryption_at_host:
        description:
            - This is only supported on certain VM sizes and in certain Azure regions.
        type: bool
    enable_ultra_ssd:
        description:
            - Whether to enable UltraSSD.
        type: bool
    enable_fips:
        description:
            - Whether enable FIPS node pool.
        type: bool
    gpu_instance_profile:
        description:
            - GPUInstanceProfile to be used to specify GPU MIG instance profile for supported GPU VM SKU.
        type: str
        choices:
            - MIG1g
            - MIG2g
            - MIG3g
            - MIG4g
            - MIG7g
    security_profile:
        description:
            - The security settings of an agent pool.
        type: dict
        suboptions:
            enable_vtpm:
                description:
                    - Whether to disable or enabled the vTPM.
                type: bool
                default: false
            enable_secure_boot:
                description:
                    - Whether to disable or enabled the secure boot.
                default: false
                type: bool
    os_disk_type:
        description:
            - The default is C(Ephemeral) if the VM supports it and has a cache disk larger than the requested OSDiskSizeGB.
            - Otherwise, defaults to C(Managed).
            - May not be changed after creation.
        type: str
        choices:
            - Ephemeral
            - Managed
    capacity_reservation_group_id:
        description:
            - The Capacity Reservation Group ID.
        type: str
    host_group_id:
        description:
            - The Host Group ID.
            - Sample as C(/subscriptions/{subscriptionId}/resourceGroups/{RG_Name}/providers/Microsoft.Compute/hostGroups/{hostGroupName)
        type: str
    pod_subnet_id:
        description:
            - If omitted, pod IPs are statically assigned on the node subnet.
        type: str
    windows_profile:
        description:
            - The Windows agent pool's specific profile.
        type: dict
        suboptions:
            disable_outbound_nat:
                description:
                    - The default value is C(false).
                    - Outbound NAT can only be disabled if the cluster outboundType is NAT Gateway.
                    - The Windows agent pool does not have node public IP enabled.
                type: bool
    network_profile:
        description:
            - Network-related settings of an agent pool.
        type: dict
        suboptions:
            node_public_ip_tags:
                description:
                    - IPTags of instance-level public IPs.
                type: list
                elements: dict
                suboptions:
                    ip_tag_type:
                        description:
                            - The IP tag type. Example as C(RoutingPreference).
                        type: str
                    tag:
                        description:
                            - The value of the IP tag associated with the public IP. Sample as C(Internet).
                        type: str
            allowed_host_ports:
                description:
                    - The port ranges that are allowed to access.
                    - The specified ranges are allowed to overlap.
                type: list
                elements: dict
                suboptions:
                    port_start:
                        description:
                            - The minimum port that is included in the range.
                            - It should be ranged from C(1) to C(65535), and be less than or equal to I(port_end).
                        type: int
                    port_end:
                        description:
                            - The maximum port that is included in the range.
                            - It should be ranged from C(1) to C(65535), and be greater than or equal to I(port_start).
                        type: int
                    protocol:
                        description:
                            - The network protocol of the port.
                        type: str
                        choices:
                            - UDP
                            - TCP
            application_security_groups:
                description:
                    - The IDs of the application security groups which agent pool will associate when created.
                type: list
                elements: str
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
- name: Create a node agent pool with custom config
  azure_rm_aksagentpool:
    resource_group: "{{ resource_group }}"
    cluster_name: "min{{ rpfx }}"
    name: default-new2
    count: 1
    vm_size: Standard_B2s
    type_properties_type: VirtualMachineScaleSets
    mode: System
    node_labels: {"release":"stable"}
    max_pods: 42
    enable_auto_scaling: true
    min_count: 1
    max_count: 10
    orchestrator_version: 1.23.5
    availability_zones:
      - 1
    kubelet_config:
      cpu_manager_policy: static
      cpu_cfs_quota: true
      fail_swap_on: false
    linux_os_config:
      transparent_huge_page_enabled: madvise
      swap_file_size_mb: 1500
      transparent_huge_page_defrag: defer+madvise
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
        security_profile:
            description:
                - The security settings of an agent pool.
            type: complex
            contains:
                enable_secure_boot:
                    description:
                        - The secure boot is disabled or enabled.
                    type: bool
                    returned: always
                    sample: true
                enable_vtpm:
                    description:
                        - The vTPM is enabled or disabled.
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
        os_sku:
            description:
                - The node agent pool's SKU.
            type: str
            returned: always
            sample: Ubuntu
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

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    pass


class AzureRMAksAgentPool(AzureRMModuleBaseExt):
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
                choices=['Linux', 'Windows', 'linux', 'windows']
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
            node_taints=dict(
                type='list',
                elements='str'
            ),
            min_count=dict(
                type='int'
            ),
            max_pods=dict(
                type='int'
            ),
            kubelet_disk_type=dict(
                type='str', choices=['OS', 'Temporary']
            ),
            workload_runtime=dict(
                type='str', choices=['OCIContainer', 'WasmWasi']
            ),
            os_sku=dict(
                type='str', choices=["Ubuntu", "AzureLinux", "Windows2022", "Windows2019"]
            ),
            scale_down_mode=dict(
                type='str',
                choices=['Delete', 'Deallocate'],
                default='Delete'
            ),
            upgrade_settings=dict(
                type='dict',
                options=dict(
                    max_surge=dict(
                        type='str'
                    )
                )
            ),
            power_state=dict(
                type='dict',
                options=dict(
                    code=dict(
                        type='str',
                        choices=['Running', 'Stopped']
                    )
                )
            ),
            enable_node_public_ip=dict(
                type='bool'
            ),
            scale_set_priority=dict(
                type='str',
                choices=["Spot", "Regular"],
            ),
            node_public_ip_prefix_id=dict(
                type='str'
            ),
            scale_set_eviction_policy=dict(
                type='str',
                choices=['Delete', 'Deallocate'],
            ),
            spot_max_price=dict(
                type='float'
            ),
            proximity_placement_group_id=dict(
                type='str'
            ),
            kubelet_config=dict(
                type='dict',
                options=dict(
                    cpu_manager_policy=dict(type='str', choices=['none', 'static'], default='none'),
                    cpu_cfs_quota=dict(type='bool', default='true'),
                    cpu_cfs_quota_period=dict(type='str', default='100ms'),
                    image_gc_high_threshold=dict(type='int', default=85),
                    image_gc_low_threshold=dict(type='int', default=80),
                    topology_manager_policy=dict(
                        type='str',
                        default='none',
                        choices=['none', 'best-effort', 'restricted', 'single-numa-node']
                    ),
                    allowed_unsafe_sysctls=dict(
                        type='list',
                        elements='str'
                    ),
                    fail_swap_on=dict(type='bool'),
                    container_log_max_size_mb=dict(type='int'),
                    container_log_max_files=dict(type='int'),
                    pod_max_pids=dict(type='int')
                )
            ),
            linux_os_config=dict(
                type='dict',
                options=dict(
                    sysctls=dict(
                        type='dict',
                        options=dict(
                            net_core_somaxconn=dict(type='int'),
                            net_core_netdev_max_backlog=dict(type='int'),
                            net_core_rmem_default=dict(type='int'),
                            net_core_rmem_max=dict(type='int'),
                            net_core_wmem_default=dict(type='int'),
                            net_core_wmem_max=dict(type='int'),
                            net_core_optmem_max=dict(type='int'),
                            net_ipv4_tcp_max_syn_backlog=dict(type='int'),
                            net_ipv4_tcp_max_tw_buckets=dict(type='int'),
                            net_ipv4_tcp_fin_timeout=dict(type='int'),
                            net_ipv4_tcp_keepalive_time=dict(type='int'),
                            net_ipv4_tcp_keepalive_probes=dict(type='int'),
                            net_ipv4_tcpkeepalive_intvl=dict(type='int'),
                            net_ipv4_tcp_tw_reuse=dict(type='bool'),
                            net_ipv4_ip_local_port_range=dict(type='str'),
                            net_ipv4_neigh_default_gc_thresh1=dict(type='int'),
                            net_ipv4_neigh_default_gc_thresh2=dict(type='int'),
                            net_ipv4_neigh_default_gc_thresh3=dict(type='int'),
                            net_netfilter_nf_conntrack_max=dict(type='int'),
                            net_netfilter_nf_conntrack_buckets=dict(type='int'),
                            fs_inotify_max_user_watches=dict(type='int'),
                            fs_file_max=dict(type='int'),
                            fs_aio_max_nr=dict(type='int'),
                            fs_nr_open=dict(type='int'),
                            kernel_threads_max=dict(type='int'),
                            vm_max_map_count=dict(type='int'),
                            vm_swappiness=dict(type='int'),
                            vm_vfs_cache_pressure=dict(type='int')
                        )
                    ),
                    transparent_huge_page_enabled=dict(
                        type='str',
                        choices=['always', 'madvise', 'never'],
                        default='always'
                    ),
                    swap_file_size_mb=dict(
                        type='int'
                    ),
                    transparent_huge_page_defrag=dict(
                        type='str',
                        default='madvise',
                        choices=['always', 'defer', 'defer+madvise', 'madvise', 'never']
                    )
                )
            ),
            enable_encryption_at_host=dict(
                type='bool'
            ),
            enable_ultra_ssd=dict(
                type='bool'
            ),
            enable_fips=dict(
                type='bool'
            ),
            gpu_instance_profile=dict(
                type='str',
                choices=["MIG1g", "MIG2g", "MIG3g", "MIG4g", "MIG7g"]
            ),
            security_profile=dict(
                type='dict',
                options=dict(
                    enable_secure_boot=dict(type='bool', default=False),
                    enable_vtpm=dict(type='bool', default=False)
                )
            ),
            os_disk_type=dict(
                type='str',
                choices=['Managed', 'Ephemeral']
            ),
            capacity_reservation_group_id=dict(
                type='str',
            ),
            host_group_id=dict(
                type='str',
            ),
            pod_subnet_id=dict(
                type='str',
            ),
            network_profile=dict(
                type='dict',
                options=dict(
                    node_public_ip_tags=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            ip_tag_type=dict(type='str'),
                            tag=dict(type='str')
                        )
                    ),
                    allowed_host_ports=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            port_start=dict(type='int'),
                            port_end=dict(type='int'),
                            protocol=dict(
                                type='str',
                                choices=['UDP', 'TCP']
                            )
                        )
                    ),
                    application_security_groups=dict(
                        type='list',
                        elements='str'
                    )
                )
            ),
            windows_profile=dict(
                type='dict',
                options=dict(
                    disable_outbound_nat=dict(type='bool')
                )
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
        self.node_taints = None
        self.min_count = None
        self.max_pods = None
        self.tags = None
        self.kubelet_disk_type = None
        self.workload_runtime = None
        self.os_sku = None
        self.scale_down_mode = None
        self.upgrade_settings = None
        self.power_state = None
        self.enable_node_public_ip = None
        self.scale_set_priority = None
        self.node_public_ip_prefix_id = None
        self.scale_set_eviction_policy = None
        self.spot_max_price = None
        self.proximity_placement_group_id = None
        self.kubelet_config = None
        self.linux_os_config = None
        self.enable_encryption_at_host = None
        self.enable_ultra_ssd = None
        self.enable_fips = None
        self.gpu_instance_profile = None
        self.security_profile = None
        self.os_disk_type = None
        self.capacity_reservation_group_id = None
        self.host_group_id = None
        self.pod_subnet_id = None
        self.network_profile = None
        self.windows_profile = None
        self.body = dict()

        super(AzureRMAksAgentPool, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec) + ['tags']:
            setattr(self, key, kwargs[key])
            if key not in ['resource_group', 'cluster_name', 'name', 'state']:
                self.body[key] = kwargs[key]

        agent_pool = self.get()
        changed = False
        response = None

        if self.state == 'present':
            if agent_pool:
                update_tags, self.body['tags'] = self.update_tags(agent_pool.get('tags'))
                for key in self.body.keys():
                    if key == 'tags':
                        if update_tags:
                            changed = True
                    elif self.body[key] is not None and isinstance(self.body[key], dict):
                        for item in self.body[key].keys():
                            if key == 'security_profile':
                                if bool(self.body[key][item]) != bool(agent_pool[key].get(item)):
                                    changed = True
                            elif key == 'windows_profile':
                                if agent_pool.get(key) is None or bool(self.body[key][item]) != bool(agent_pool[key].get(item)):
                                    changed = True
                            elif not self.default_compare({}, self.body[key], agent_pool[key], '', dict(compare=[])):
                                changed = True
                    elif key == 'node_public_ip_prefix_id':
                        pass
                    elif key == 'node_taints' and self.body[key] is not None:
                        if len(self.body[key]) != len(agent_pool[key]) or (not all(item in agent_pool[key] for item in self.body[key])):
                            changed = True
                    elif self.body[key] is not None and self.body[key] != agent_pool[key] and key not in ['scale_set_priority', 'spot_max_price']:
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
            self.managedcluster_client.agent_pools.begin_delete(self.resource_group, self.cluster_name, self.name)
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
            upgrade_settings=dict(),
            provisioning_state=agent_pool.provisioning_state,
            availability_zones=[],
            enable_node_public_ip=agent_pool.enable_node_public_ip,
            scale_set_priority=agent_pool.scale_set_priority,
            scale_set_eviction_policy=agent_pool.scale_set_eviction_policy,
            spot_max_price=agent_pool.spot_max_price,
            node_labels=agent_pool.node_labels,
            node_taints=agent_pool.node_taints if agent_pool.node_taints else [],
            tags=agent_pool.tags,
            kubelet_disk_type=agent_pool.kubelet_disk_type,
            workload_runtime=agent_pool.workload_runtime,
            os_sku=agent_pool.os_sku,
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

        if agent_pool.power_state is not None:
            agent_pool_dict['power_state']['code'] = agent_pool.power_state.code
        else:
            agent_pool_dict['power_state'] = None

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

        if agent_pool.security_profile is not None:
            agent_pool_dict['security_profile']['enable_vtpm'] = agent_pool.security_profile.enable_vtpm
            agent_pool_dict['security_profile']['enable_secure_boot'] = agent_pool.security_profile.enable_secure_boot
        else:
            agent_pool_dict['security_profile'] = None

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
    AzureRMAksAgentPool()


if __name__ == '__main__':
    main()
