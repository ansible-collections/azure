#!/usr/bin/python
#
# Copyright (c) 2018 Sertac Ozercan, <seozerca@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_aks
version_added: "0.1.2"
short_description: Manage a managed Azure Container Service (AKS) instance
description:
    - Create, update and delete a managed Azure Container Service (AKS) instance.
    - You can only specify C(identity) or C(service_principal), not both.  If you don't specify either it will
      default to identity->type->SystemAssigned.

options:
    resource_group:
        description:
            - Name of a resource group where the managed Azure Container Services (AKS) exists or will be created.
        required: true
        type: str
    name:
        description:
            - Name of the managed Azure Container Services (AKS) instance.
        required: true
        type: str
    state:
        description:
            - Assert the state of the AKS. Use C(present) to create or update an AKS and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present
    location:
        description:
            - Valid azure location. Defaults to location of the resource group.
        type: str
    dns_prefix:
        description:
            - DNS prefix specified when creating the managed cluster.
        type: str
    kubernetes_version:
        description:
            - Version of Kubernetes specified when creating the managed cluster.
        type: str
    linux_profile:
        description:
            - The Linux profile suboptions.
            - Optional, provide if you need an ssh access to the cluster nodes.
        type: dict
        suboptions:
            admin_username:
                description:
                    - The Admin Username for the cluster.
                required: true
                type: str
            ssh_key:
                description:
                    - The Public SSH Key used to access the cluster.
                required: true
                type: str
    agent_pool_profiles:
        description:
            - The agent pool profile suboptions.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Unique name of the agent pool profile in the context of the subscription and resource group.
                required: true
                type: str
            count:
                description:
                    - Number of agents (VMs) to host docker containers.
                    - Allowed values must be in the range of C(1) to C(100) (inclusive).
                required: true
                type: int
            vm_size:
                description:
                    - The VM Size of each of the Agent Pool VM's (e.g. C(Standard_F1) / C(Standard_D2v2)).
                required: true
                type: str
            os_disk_size_gb:
                description:
                    - Size of the OS disk.
                type: int
            enable_auto_scaling:
                description:
                    - To enable auto-scaling.
                type: bool
            max_count:
                description:
                    - Maximum number of nodes for auto-scaling.
                    - Required if I(enable_auto_scaling=True).
                type: int
            min_count:
                description:
                    - Minmum number of nodes for auto-scaling.
                    - Required if I(enable_auto_scaling=True).
                type: int
            max_pods:
                description:
                    - Maximum number of pods schedulable on nodes.
                type: int
            type:
                description:
                    - AgentPoolType represents types of an agent pool.
                    - Possible values include C(VirtualMachineScaleSets) and C(AvailabilitySet).
                choices:
                    - 'VirtualMachineScaleSets'
                    - 'AvailabilitySet'
                type: str
            mode:
                description:
                    - AgentPoolMode represents mode of an agent pool.
                    - Possible values include C(System) and C(User).
                    - System AgentPoolMode requires a minimum VM SKU of at least 2 vCPUs and 4GB memory.
                choices:
                    - 'System'
                    - 'User'
                type: str
            orchestrator_version:
                description:
                    - Version of kubernetes running on the node pool.
                type: str
            node_labels:
                description:
                    - Agent pool node labels to be persisted across all nodes in agent pool.
                type: dict
            vnet_subnet_id:
                description:
                    - Specifies the VNet's subnet identifier.
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
                    - The operating system type.
                type: str
                choices:
                    - Linux
                    - Windows
                    - linux
                    - windows
            storage_profiles:
                description:
                    - Storage profile specifies what kind of storage used.
                type: str
                choices:
                    - StorageAccount
                    - ManagedDisks
            ports:
                description:
                    - List of the agent pool's port.
                type: list
                elements: int
            dns_prefix:
                description:
                    - DNS prefix specified when creating the managed cluster.
                type: str
            tags:
                description:
                    - The tags to be persisted on the agent pool virtual machine scale set.
                type: dict
            os_sku:
                description:
                    - The operating system sku.
                type: str
                choices:
                    - Ubuntu
                    - AzureLinux
                    - Windows2019
                    - Windows2022
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
    security_profile:
        description:
            - Security profile for the container service cluster.
        type: dict
        suboptions:
            workload_identity:
                description:
                    - Workload identity settings for the security profile.
                    - Workload identity enables Kubernetes applications to access Azure cloud resources securely with Azure AD.
                    - See U(https://aka.ms/aks/wi) for more details.
                type: dict
                suboptions:
                    enabled:
                        description:
                            - Whether to enable workload identity.
                        type: bool
            image_cleaner:
                description:
                    - Image Cleaner settings for the security profile.
                type: dict
                suboptions:
                    enabled:
                        description:
                            - Whether to enable Image Cleaner on AKS cluster.
                        type: bool
                    interval_hours:
                        description:
                            - Image Cleaner scanning interval in hours.
                        type: int
            defender:
                description:
                    - Microsoft Defender settings for the security profile.
                type: dict
                suboptions:
                    log_analytics_workspace_resource_id:
                        description:
                            - Resource ID of the Log Analytics workspace to be associated with Microsoft Defender.
                            - When Microsoft Defender is enabled, this field is required and must be a valid workspace resource ID.
                            - When Microsoft Defender is disabled, leave the field empty.
                        type: str
                    security_monitoring:
                        description:
                            - Microsoft Defender threat detection for Cloud settings for the security profile.
                        type: dict
                        suboptions:
                            enabled:
                                description:
                                    - Whether to enable Defender threat detection.
                                type: bool
            azure_key_vault_kms:
                description:
                    - Azure Key Vault.
                    - See U(https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/) settings for the security profile.
                type: dict
                suboptions:
                    enabled:
                        description:
                            -  Whether to enable Azure Key Vault key management service. The default is C(false).
                        type: bool
                        default: false
                    key_id:
                        description:
                            - Identifier of Azure Key Vault key.
                        type: str
                    key_vault_network_acces:
                        description:
                            - Network access of key vault.
                        type: str
                        choices:
                            - Public
                            - Private
                        default: Public
                    key_vault_resource_id:
                        description:
                            - Resource ID of key vault.
                            - When I(key_vault_network_acces=Private), this field is required and must be a valid resource ID.
                            - When I(key_vault_network_acces=Public), leave the field empty.
                        type: str
    service_principal:
        description:
            - The service principal suboptions.
        type: dict
        suboptions:
            client_id:
                description:
                    - The ID for the Service Principal.
                type: str
                required: true
            client_secret:
                description:
                    - The secret password associated with the service principal.
                type: str
    identity:
        description:
            - Identity for the Server.
        type: dict
        version_added: '2.4.0'
        suboptions:
            type:
                description:
                    - Type of the managed identity
                required: false
                choices:
                    - UserAssigned
                    - SystemAssigned
                default: SystemAssigned
                type: str
            user_assigned_identities:
                description:
                    - User Assigned Managed Identity
                type: str
    enable_rbac:
        description:
            - Enable RBAC.
            - Existing non-RBAC enabled AKS clusters cannot currently be updated for RBAC use.
        type: bool
        default: no
    network_profile:
        description:
            - Profile of network configuration.
        type: dict
        suboptions:
            network_plugin:
                description:
                    - Network plugin used for building Kubernetes network.
                    - This property cannot been changed.
                    - With C(kubenet), nodes get an IP address from the Azure virtual network subnet.
                    - AKS features such as Virtual Nodes or network policies aren't supported with C(kubenet).
                    - C(azure) enables Azure Container Networking Interface(CNI), every pod gets an IP address from the subnet and can be accessed directly.
                    - use BYO CNI for custom networking solutions.
                type: str
                choices:
                    - azure
                    - kubenet
                    - none
            network_plugin_mode:
                description:
                    - Network plugin mode used for building the Kubernetes network.
                type: str
                choices:
                    - Overlay
            network_policy:
                description: Network policy used for building Kubernetes network.
                type: str
                choices:
                    - azure
                    - calico
            pod_cidr:
                description:
                    - A CIDR notation IP range from which to assign pod IPs when I(network_plugin=kubenet) is used.
                    - It should be a large address space that isn't in use elsewhere in your network environment.
                    - This address range must be large enough to accommodate the number of nodes that you expect to scale up to.
                type: str
            service_cidr:
                description:
                    - A CIDR notation IP range from which to assign service cluster IPs.
                    - It must not overlap with any Subnet IP ranges.
                    - It should be the *.10 address of your service IP address range.
                type: str
            dns_service_ip:
                description:
                    - An IP address assigned to the Kubernetes DNS service.
                    - It must be within the Kubernetes service address range specified in serviceCidr.
                type: str
            load_balancer_sku:
                description:
                    - The load balancer sku for the managed cluster.
                type: str
                choices:
                    - standard
                    - basic
            outbound_type:
                description:
                    - How outbound traffic will be configured for a cluster.
                type: str
                default: loadBalancer
                choices:
                    - loadBalancer
                    - userDefinedRouting
                    - managedNATGateway
                    - userAssignedNATGateway
    api_server_access_profile:
        description:
            - Profile of API Access configuration.
        type: dict
        suboptions:
            authorized_ip_ranges:
                description:
                    - Authorized IP Ranges to kubernetes API server.
                    - Cannot be enabled when using private cluster
                type: list
                elements: str
            enable_private_cluster:
                description:
                    - Whether to create the cluster as a private cluster or not.
                    - Cannot be changed for an existing cluster.
                type: bool
    aad_profile:
        description:
            - Profile of Azure Active Directory configuration.
        type: dict
        suboptions:
            client_app_id:
                description: The client AAD application ID.
                type: str
            server_app_id:
                description: The server AAD application ID.
                type: str
            server_app_secret:
                description: The server AAD application secret.
                type: str
            tenant_id:
                description:
                    - The AAD tenant ID to use for authentication.
                    - If not specified, will use the tenant of the deployment subscription.
                type: str
            managed:
                description:
                    - Whether to enable managed AAD.
                type: bool
                default: false
            enable_azure_rbac:
                description:
                    - Whether to enable Azure RBAC for Kubernetes authorization.
                type: bool
                default: false
            admin_group_object_ids:
                description:
                    - AAD group object IDs that will have admin role of the cluster.
                type: list
                elements: str
    addon:
        description:
            - Profile of managed cluster add-on.
            - Key can be C(http_application_routing), C(monitoring), C(virtual_node) and C(azure_keyvault_secrets_provider).
            - Value must be a dict contains a bool variable C(enabled).
        type: dict
        suboptions:
            http_application_routing:
                description:
                    - The HTTP application routing solution makes it easy to access applications that are deployed to your cluster.
                type: dict
                aliases:
                    - httpApplicationRouting
                suboptions:
                    enabled:
                        description:
                            - Whether the solution enabled.
                        type: bool
                        default: true
            azure_keyvault_secrets_provider:
                description:
                    - Whether to enable the Azure Key Vault provider in an AKS cluster.
                type: dict
                version_added: "3.7.0"
                aliases:
                    - azureKeyvaultSecretsProvider
                suboptions:
                    enabled:
                        description:
                            - Enabled or disabled the Azure Key Vault provider in the AKS cluster.
                        type: bool
                        default: true
            monitoring:
                description:
                    - It gives you performance visibility by collecting memory and processor metrics from controllers, nodes,
                      and containers that are available in Kubernetes through the Metrics API.
                type: dict
                aliases:
                    - omsagent
                suboptions:
                    enabled:
                        description:
                            - Whether the solution enabled.
                        type: bool
                        default: true
                    log_analytics_workspace_resource_id:
                        description:
                            - Where to store the container metrics.
                        type: str
                        required: true
                        aliases:
                            - logAnalyticsWorkspaceResourceID
            virtual_node:
                description:
                    - With virtual nodes, you have quick provisioning of pods, and only pay per second for their execution time.
                    - You don't need to wait for Kubernetes cluster autoscaler to deploy VM compute nodes to run the additional pods.
                type: dict
                aliases:
                    - aciConnector
                suboptions:
                    enabled:
                        description:
                            - Whether the solution enabled.
                        type: bool
                        default: true
                    subnet_resource_id:
                        description:
                            - Subnet associated to the cluster.
                        type: str
                        required: true
                        aliases:
                            - SubnetName
    node_resource_group:
        description:
            - Name of the resource group containing agent pool nodes.
            - Unable to update.
        type: str
    pod_identity_profile:
        description:
            - Config pod identities in managed Kubernetes cluster.
        type: dict
        suboptions:
            enabled:
                description:
                    - Whether the pod identity addon is enabled.
                type: bool
            allow_network_plugin_kubenet:
                description:
                    - Whether using Kubenet network plugin with AAD Pod Identity.
                type: bool
            user_assigned_identities:
                description:
                    - The pod identities to use in the cluster.
                type: list
                elements: dict
                suboptions:
                    name:
                        description:
                            - The name of the pod identity.
                        type: str
                        required: true
                    namespace:
                        description:
                            - The namespace of the pod identity.
                        type: str
                        required: true
                    binding_selector:
                        description:
                            - The binding selector to use for the AzureIdentityBinding resource.
                        type: str
                    identity:
                        description:
                            - The user assigned identity details.
                        type: dict
                        required: true
                        suboptions:
                            resource_id:
                                description:
                                    - The resource ID of the user assigned identity.
                                type: str
                            object_id:
                                description:
                                    - The object ID of the user assigned identity.
                                type: str
                            client_id:
                                description:
                                    - The client ID of the user assigned identity.
                                type: str
    windows_profile:
        description:
            - The Windows profile suboptions.
        type: dict
        suboptions:
            admin_username:
                description:
                    - The Admin Username for the cluster.
                required: true
                type: str
            admin_password:
                description:
                    - The Admin password for the cluster.
                required: true
                type: str
    disable_local_accounts:
        description:
            - If set to true, getting static credentials will be disabled for this cluster.
            - This must only be used on Managed Clusters that are AAD enabled.
        type: bool
    auto_upgrade_profile:
        description:
            - Auto upgrade profile for a managed cluster.
        type: dict
        suboptions:
            upgrade_channel:
                description:
                    - Setting the AKS cluster auto-upgrade channel.
                type: str
                default: node-image
                choices:
                    - rapid
                    - stable
                    - patch
                    - node-image
                    - none
            node_os_upgrade_channel:
                description:
                    - Manner in which the OS on your nodes is updated.
                type: str
                default: NodeImage
                choices:
                    - None
                    - Unmanaged
                    - SecurityPatch
                    - NodeImage
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Sertac Ozercan (@sozercan)
    - Yuwei Zhou (@yuwzho)

'''

EXAMPLES = '''
- name: Create an AKS instance With A System Node Pool & A User Node Pool
  azure_rm_aks:
    name: myAKS
    resource_group: myResourceGroup
    location: eastus
    dns_prefix: akstest
    kubernetes_version: 1.14.6
    linux_profile:
      admin_username: azureuser
      ssh_key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAA...
    service_principal:
      client_id: "cf72ca99-f6b9-4004-b0e0-bee10c521948"
      client_secret: "Password1234!"
    agent_pool_profiles:
      - name: default
        count: 1
        vm_size: Standard_B2s
        enable_auto_scaling: true
        type: VirtualMachineScaleSets
        mode: System
        max_count: 3
        min_count: 1
        enable_rbac: true
        tags:
          key1: value1
      - name: user
        count: 1
        vm_size: Standard_D2_v2
        enable_auto_scaling: true
        type: VirtualMachineScaleSets
        mode: User
        max_count: 3
        min_count: 1
        enable_rbac: true

- name: Create a managed Azure Container Services (AKS) instance
  azure_rm_aks:
    name: myAKS
    location: eastus
    resource_group: myResourceGroup
    dns_prefix: akstest
    kubernetes_version: 1.14.6
    linux_profile:
      admin_username: azureuser
      ssh_key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAA...
    service_principal:
      client_id: "cf72ca99-f6b9-4004-b0e0-bee10c521948"
      client_secret: "Password123!"
    agent_pool_profiles:
      - name: default
        count: 5
        mode: System
        vm_size: Standard_B2s
    tags:
      Environment: Production

- name: Use minimal parameters and system-assigned identity
  azure_rm_aks:
    name: myMinimalCluster
    location: eastus
    resource_group: myExistingResourceGroup
    dns_prefix: akstest
    agent_pool_profiles:
      - name: default
        count: 1
        vm_size: Standard_D2_v2

- name: Create AKS with userDefinedRouting "Link:https://docs.microsoft.com/en-us/azure/aks/limit-egress-traffic#add-a-dnat-rule-to-azure-firewall"
  azure_rm_aks:
    name: "minimal{{ rpfx }}"
    location: eastus
    resource_group: "{{ resource_group }}"
    kubernetes_version: "{{ versions.azure_aks_versions[0] }}"
    dns_prefix: "aks{{ rpfx }}"
    service_principal:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
    network_profile:
      network_plugin: azure
      load_balancer_sku: standard
      outbound_type: userDefinedRouting
      service_cidr: "10.41.0.0/16"
      dns_service_ip: "10.41.0.10"
    api_server_access_profile:
      authorized_ip_ranges:
        - "20.106.246.252/32"
      enable_private_cluster: false
    agent_pool_profiles:
      - name: default
        count: 1
        vm_size: Standard_B2s
        mode: System
        vnet_subnet_id: "{{ output.subnets[0].id }}"
        type: VirtualMachineScaleSets
        enable_auto_scaling: false

- name: Create an AKS instance wit pod_identity_profile settings
  azure_rm_aks:
    name: "aks{{ rpfx }}"
    resource_group: "{{ resource_group }}"
    location: eastus
    dns_prefix: "aks{{ rpfx }}"
    kubernetes_version: "{{ versions.azure_aks_versions[0] }}"
    service_principal:
      client_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
      client_secret: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    linux_profile:
      admin_username: azureuser
      ssh_key: ssh-rsa AAAAB3Ip6***************
    agent_pool_profiles:
      - name: default
        count: 1
        vm_size: Standard_B2s
        type: VirtualMachineScaleSets
        mode: System
        node_labels: {"release":"stable"}
        max_pods: 42
        availability_zones:
          - 1
          - 2
    node_resource_group: "node{{ noderpfx }}"
    enable_rbac: true
    network_profile:
      load_balancer_sku: standard
    pod_identity_profile:
      enabled: false
      allow_network_plugin_kubenet: false
      user_assigned_identities:
        - name: fredtest
          namespace: fredtest
          binding_selector: test
          identity:
            client_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
            object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

- name: Create a kubernet service with I(os_type=Windows)
  azure_rm_aks:
    name: myaks02
    location: eastus
    resource_group: "{{ resource_group }}"
    kubernetes_version: "{{ versions }}"
    dns_prefix: "aks_dns"
    enable_rbac: true
    windows_profile:
      admin_username: azureuser
      admin_password: Password@0329
    aad_profile:
      managed: true
    agent_pool_profiles:
      - name: default
        count: 1
        vm_size: Standard_D8ds_v5
        mode: System
        os_type: Linux
        os_sku: Ubuntu
      - name: def
        count: 1
        vm_size: Standard_D2as_v4
        mode: User
        os_type: Windows
        os_sku: Windows2022
    api_server_access_profile:
      authorized_ip_ranges:
        - "192.0.2.0"
        - "198.51.100.0"
        - "203.0.113.0"
      enable_private_cluster: false
    network_profile:
      load_balancer_sku: standard
      network_plugin: azure
      outbound_type: loadBalancer

- name: Remove a managed Azure Container Services (AKS) instance
  azure_rm_aks:
    name: myAKS
    resource_group: myResourceGroup
    state: absent
'''
RETURN = '''
state:
    description: Current state of the Azure Container Service (AKS).
    returned: always
    type: dict
    example:
        addon:
          azure_keyvault_secrets_provider: { "enabled": true }
          http_application_routing: { "enabled": false }
          monitoring: null
          virtual_node: null
        agent_pool_profiles:
         - count: 1
           dns_prefix: Null
           name: default
           os_disk_size_gb: Null
           os_type: Linux
           moode: System
           node_labels: { "environment": "dev", "release": "stable" }
           ports: Null
           storage_profile: ManagedDisks
           vm_size: Standard_B2s
           vnet_subnet_id: Null
           os_sku: Ubuntu
           security_profile: { 'enable_secure_boot': true, 'enable_vtpm': false }
        auto_upgrade_profile:
          node_os_upgrade_channel: NodeImage
          upgrade_channel: patch
        changed: false
        dns_prefix: aks9860bdcd89
        disable_local_accounts: true
        id: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/myResourceGroup/providers/Microsoft.ContainerService/managedClusters/aks9860bdc"
        kube_config: ["......"]
        kubernetes_version: 1.14.6
        linux_profile:
           admin_username: azureuser
           ssh_key: ssh-rsa AAAAB3NzaC1yc2EAAAADA.....
        location: eastus
        name: aks9860bdc
        provisioning_state: Succeeded
        service_principal_profile:
           client_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        identity:
           "type": "UserAssigned"
           "user_assigned_identities": {}
        pod_identity_profile: {
            "allow_network_plugin_kubenet": false,
            "user_assigned_identities": [
                {
                        "binding_selector": "test",
                        "identity": {
                            "client_id": xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx,
                            "object_id": xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                        },
                        "name": "fredtest",
                        "namespace": "fredtest",
                        "provisioning_state": "Updating"
                }
            ]
        }
        security_profile: {
            'defender': {
                "log_analytics_workspace_resource_id": "/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.OperationalInsights/workspaces/fred01",
                "security_monitoring": {
                    "enabled": true
                }
            },
            "image_cleaner": {
                "enabled": false,
                "interval_hours": 38
            }
        }
        tags: {}
        type: Microsoft.ContainerService/ManagedClusters
        windows_profile: None
'''
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.exceptions import HttpResponseError
except ImportError:
    # This is handled in azure_rm_common
    pass


def create_aks_dict(aks):
    '''
    Helper method to deserialize a ContainerService to a dict
    :param: aks: ContainerService or AzureOperationPoller with the Azure callback object
    :return: dict with the state on Azure
    '''

    return dict(
        id=aks.id,
        name=aks.name,
        location=aks.location,
        dns_prefix=aks.dns_prefix,
        kubernetes_version=aks.kubernetes_version,
        tags=aks.tags,
        disable_local_accounts=aks.disable_local_accounts,
        linux_profile=create_linux_profile_dict(aks.linux_profile),
        identity=aks.identity.as_dict() if aks.identity else {},
        service_principal_profile=create_service_principal_profile_dict(
            aks.service_principal_profile),
        provisioning_state=aks.provisioning_state,
        agent_pool_profiles=create_agent_pool_profiles_dict(
            aks.agent_pool_profiles),
        type=aks.type,
        kube_config=aks.kube_config,
        enable_rbac=aks.enable_rbac,
        network_profile=create_network_profiles_dict(aks.network_profile),
        aad_profile=create_aad_profiles_dict(aks.aad_profile),
        api_server_access_profile=create_api_server_access_profile_dict(aks.api_server_access_profile),
        addon=create_addon_dict(aks.addon_profiles),
        fqdn=aks.fqdn,
        node_resource_group=aks.node_resource_group,
        auto_upgrade_profile=create_auto_upgrade_profile_dict(aks.auto_upgrade_profile),
        windows_profile=create_windows_profile_dict(aks.windows_profile),
        pod_identity_profile=create_pod_identity_profile(aks.pod_identity_profile.as_dict()) if aks.pod_identity_profile else None,
        security_profile=aks.security_profile.as_dict() if aks.security_profile else None,
    )


def create_auto_upgrade_profile_dict(auto_upgrade_profile):
    return dict(
        upgrade_channel=auto_upgrade_profile.upgrade_channel,
        node_os_upgrade_channel=auto_upgrade_profile.node_os_upgrade_channel
    ) if auto_upgrade_profile else None


def create_pod_identity_profile(pod_profile):
    return dict(
        enabled=pod_profile.get('enabled', False),
        allow_network_plugin_kubenet=pod_profile.get('allow_network_plugin_kubenet', False),
        user_assigned_identities=pod_profile.get('user_assigned_identities')
    ) if pod_profile else {}


def create_network_profiles_dict(network):
    return dict(
        network_plugin=network.network_plugin,
        network_plugin_mode=network.network_plugin_mode,
        network_policy=network.network_policy,
        pod_cidr=network.pod_cidr,
        service_cidr=network.service_cidr,
        dns_service_ip=network.dns_service_ip,
        load_balancer_sku=network.load_balancer_sku,
        outbound_type=network.outbound_type
    ) if network else dict()


def create_aad_profiles_dict(aad):
    return aad.as_dict() if aad else dict()


def create_api_server_access_profile_dict(api_server):
    return api_server.as_dict() if api_server else dict()


def create_addon_dict(addon):
    result = dict()
    addon = addon or dict()
    for key in addon.keys():
        result[key] = addon[key].config
        if result[key] is None:
            result[key] = {}
        result[key]['enabled'] = addon[key].enabled
    return result


def create_linux_profile_dict(linuxprofile):
    '''
    Helper method to deserialize a ContainerServiceLinuxProfile to a dict
    :param: linuxprofile: ContainerServiceLinuxProfile with the Azure callback object
    :return: dict with the state on Azure
    '''
    if linuxprofile:
        return dict(
            ssh_key=linuxprofile.ssh.public_keys[0].key_data,
            admin_username=linuxprofile.admin_username
        )
    else:
        return None


def create_service_principal_profile_dict(serviceprincipalprofile):
    '''
    Helper method to deserialize a ContainerServiceServicePrincipalProfile to a dict
    Note: For security reason, the service principal secret is skipped on purpose.
    :param: serviceprincipalprofile: ContainerServiceServicePrincipalProfile with the Azure callback object
    :return: dict with the state on Azure
    '''
    return dict(
        client_id=serviceprincipalprofile.client_id
    )


def create_windows_profile_dict(windowsprofile):
    '''
    Helper method to deserialize a ManagedClusterWindowsProfile to a dict
    :param: windowsprofile: ManagedClusterWindowsProfile with the Azure callback object
    :return: dict with the state on Azure
    '''
    if windowsprofile:
        return dict(
            admin_username=windowsprofile.admin_username,
            admin_password=windowsprofile.admin_password
        )
    else:
        return None


def create_agent_pool_profiles_dict(agentpoolprofiles):
    '''
    Helper method to deserialize a ContainerServiceAgentPoolProfile to a dict
    :param: agentpoolprofiles: ContainerServiceAgentPoolProfile with the Azure callback object
    :return: dict with the state on Azure
    '''
    return [dict(
        count=profile.count,
        vm_size=profile.vm_size,
        name=profile.name,
        os_disk_size_gb=profile.os_disk_size_gb,
        vnet_subnet_id=profile.vnet_subnet_id,
        availability_zones=profile.availability_zones,
        os_type=profile.os_type,
        type=profile.type,
        mode=profile.mode,
        orchestrator_version=profile.orchestrator_version,
        enable_auto_scaling=profile.enable_auto_scaling,
        max_count=profile.max_count,
        node_labels=profile.node_labels,
        min_count=profile.min_count,
        max_pods=profile.max_pods,
        tags=profile.tags,
        os_sku=profile.os_sku,
        security_profile=dict(
            enable_secure_boot=profile.security_profile.enable_secure_boot,
            enable_vtpm=profile.security_profile.enable_vtpm
        ) if profile.security_profile is not None else None
    ) for profile in agentpoolprofiles] if agentpoolprofiles else None


def create_addon_profiles_spec():
    '''
    Helper method to parse the ADDONS dictionary and generate the addon spec
    '''
    spec = dict()
    for key in ADDONS.keys():
        values = ADDONS[key]
        addon_spec = dict(
            enabled=dict(type='bool', default=True)
        )
        configs = values.get('config') or {}
        for item in configs.keys():
            addon_spec[item] = dict(type='str', aliases=[configs[item]], required=True)
        if key == 'azure_keyvault_secrets_provider':
            spec[key] = dict(type='dict', no_log=True, options=addon_spec, aliases=[values['name']])
        else:
            spec[key] = dict(type='dict', options=addon_spec, aliases=[values['name']])
    return spec


ADDONS = {
    'http_application_routing': dict(name='httpApplicationRouting'),
    'monitoring': dict(name='omsagent', config={'log_analytics_workspace_resource_id': 'logAnalyticsWorkspaceResourceID'}),
    'virtual_node': dict(name='aciConnector', config={'subnet_resource_id': 'SubnetName'}),
    'azure_keyvault_secrets_provider': dict(name='azureKeyvaultSecretsProvider')
}


linux_profile_spec = dict(
    admin_username=dict(type='str', required=True),
    ssh_key=dict(type='str', no_log=True, required=True)
)


service_principal_spec = dict(
    client_id=dict(type='str', required=True),
    client_secret=dict(type='str', no_log=True)
)


agent_pool_profile_spec = dict(
    name=dict(type='str', required=True),
    count=dict(type='int', required=True),
    vm_size=dict(type='str', required=True),
    os_disk_size_gb=dict(type='int'),
    dns_prefix=dict(type='str'),
    ports=dict(type='list', elements='int'),
    storage_profiles=dict(type='str', choices=[
                          'StorageAccount', 'ManagedDisks']),
    vnet_subnet_id=dict(type='str'),
    availability_zones=dict(type='list', elements='int', choices=[1, 2, 3]),
    os_type=dict(type='str', choices=['Linux', 'Windows', 'linux', 'windows']),
    orchestrator_version=dict(type='str', required=False),
    type=dict(type='str', choices=['VirtualMachineScaleSets', 'AvailabilitySet']),
    mode=dict(type='str', choices=['System', 'User']),
    enable_auto_scaling=dict(type='bool'),
    max_count=dict(type='int'),
    node_labels=dict(type='dict'),
    min_count=dict(type='int'),
    max_pods=dict(type='int'),
    tags=dict(type='dict'),
    os_sku=dict(type='str', choices=['Ubuntu', 'AzureLinux', 'Windows2019', 'Windows2022']),
    security_profile=dict(
        type='dict',
        options=dict(
            enable_secure_boot=dict(type='bool', default=False),
            enable_vtpm=dict(type='bool', default=False)
        )
    )
)


network_profile_spec = dict(
    network_plugin=dict(type='str', choices=['azure', 'kubenet', 'none']),
    network_plugin_mode=dict(type='str', choices=['Overlay']),
    network_policy=dict(type='str', choices=['azure', 'calico']),
    pod_cidr=dict(type='str'),
    service_cidr=dict(type='str'),
    dns_service_ip=dict(type='str'),
    load_balancer_sku=dict(type='str', choices=['standard', 'basic']),
    outbound_type=dict(type='str', default='loadBalancer', choices=['userDefinedRouting', 'loadBalancer', 'userAssignedNATGateway', 'managedNATGateway'])
)


aad_profile_spec = dict(
    client_app_id=dict(type='str'),
    server_app_id=dict(type='str'),
    server_app_secret=dict(type='str', no_log=True),
    tenant_id=dict(type='str'),
    managed=dict(type='bool', default='false'),
    enable_azure_rbac=dict(type='bool', default='false'),
    admin_group_object_ids=dict(type='list', elements='str')
)


api_server_access_profile_spec = dict(
    authorized_ip_ranges=dict(type='list', elements='str'),
    enable_private_cluster=dict(type='bool'),
)


managed_identity_spec = dict(
    type=dict(type='str', choices=['SystemAssigned', 'UserAssigned'], default='SystemAssigned'),
    user_assigned_identities=dict(type='str'),
)


windows_profile_spec = dict(
    admin_username=dict(type='str', required=True),
    admin_password=dict(type='str', no_log=True, required=True),
)


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class AzureRMManagedCluster(AzureRMModuleBaseExt):
    """Configuration class for an Azure RM container service (AKS) resource"""

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
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            location=dict(
                type='str'
            ),
            dns_prefix=dict(
                type='str'
            ),
            kubernetes_version=dict(
                type='str'
            ),
            linux_profile=dict(
                type='dict',
                options=linux_profile_spec
            ),
            agent_pool_profiles=dict(
                type='list',
                elements='dict',
                options=agent_pool_profile_spec
            ),
            windows_profile=dict(
                type='dict',
                options=windows_profile_spec
            ),
            service_principal=dict(
                type='dict',
                options=service_principal_spec
            ),
            identity=dict(
                type='dict',
                options=managed_identity_spec,
                required_if=[
                    ('type', 'UserAssigned', [
                        'user_assigned_identities']),
                ]
            ),
            enable_rbac=dict(
                type='bool',
                default=False
            ),
            network_profile=dict(
                type='dict',
                options=network_profile_spec
            ),
            aad_profile=dict(
                type='dict',
                options=aad_profile_spec
            ),
            addon=dict(
                type='dict',
                options=create_addon_profiles_spec()
            ),
            api_server_access_profile=dict(
                type='dict',
                options=api_server_access_profile_spec
            ),
            node_resource_group=dict(
                type='str'
            ),
            pod_identity_profile=dict(
                type='dict',
                options=dict(
                    enabled=dict(type='bool'),
                    allow_network_plugin_kubenet=dict(type='bool'),
                    user_assigned_identities=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            name=dict(type='str', required=True),
                            namespace=dict(type='str', required=True),
                            binding_selector=dict(type='str'),
                            identity=dict(
                                type='dict',
                                required=True,
                                options=dict(
                                    resource_id=dict(type='str'),
                                    client_id=dict(type='str'),
                                    object_id=dict(type='str')
                                )
                            )
                        )
                    )
                )
            ),
            auto_upgrade_profile=dict(
                type='dict',
                options=dict(
                    upgrade_channel=dict(
                        type='str',
                        choices=["rapid", "stable", "patch", "node-image", "none"],
                        default='node-image'
                    ),
                    node_os_upgrade_channel=dict(
                        type='str',
                        choices=["None", "Unmanaged", "SecurityPatch", "NodeImage"],
                        default='NodeImage'
                    )
                )
            ),
            disable_local_accounts=dict(
                type='bool'
            ),
            security_profile=dict(
                type='dict',
                options=dict(
                    defender=dict(
                        type='dict',
                        options=dict(
                            log_analytics_workspace_resource_id=dict(type='str'),
                            security_monitoring=dict(
                                type='dict',
                                options=dict(
                                    enabled=dict(type='bool')
                                )
                            )
                        )
                    ),
                    azure_key_vault_kms=dict(
                        type='dict',
                        no_log=True,
                        options=dict(
                            enabled=dict(type='bool', default=False),
                            key_id=dict(type='str'),
                            key_vault_network_acces=dict(type='str', choices=['Private', 'Public'], default='Public'),
                            key_vault_resource_id=dict(type='str')
                        )
                    ),
                    workload_identity=dict(
                        type='dict',
                        options=dict(
                            enabled=dict(type='bool'),
                        )
                    ),
                    image_cleaner=dict(
                        type='dict',
                        options=dict(
                            enabled=dict(type='bool'),
                            interval_hours=dict(type='int')
                        )
                    ),
                )
            ),
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.dns_prefix = None
        self.kubernetes_version = None
        self.tags = None
        self.state = None
        self.linux_profile = None
        self.agent_pool_profiles = None
        self.service_principal = None
        self.identity = None
        self.enable_rbac = False
        self.network_profile = None
        self.aad_profile = None
        self.api_server_access_profile = None
        self.addon = None
        self.node_resource_group = None
        self.pod_identity_profile = None
        self.auto_upgrade_profile = None
        self.windows_profile = None
        self.disable_local_accounts = None
        self.security_profile = None

        mutually_exclusive = [('identity', 'service_principal')]

        required_if = [
            ('state', 'present', [
             'dns_prefix', 'agent_pool_profiles'])
        ]

        self.results = dict(changed=False)

        super(AzureRMManagedCluster, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=True,
                                                    required_if=required_if,
                                                    mutually_exclusive=mutually_exclusive)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        resource_group = None
        to_be_updated = False
        update_tags = False
        update_agentpool = False

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        response = self.get_aks()

        # Check if the AKS instance already present in the RG
        if self.state == 'present':
            available_versions = self.get_all_versions()
            if not response:
                to_be_updated = True
                # Default to SystemAssigned if service_principal is not specified
                if not self.service_principal and not self.identity:
                    self.identity = dotdict({'type': 'SystemAssigned'})
                if self.identity:
                    changed, self.identity = self.update_identity(self.identity, {})
                if self.kubernetes_version not in available_versions.keys():
                    self.fail("Unsupported kubernetes version. Expected one of {0} but got {1}".format(available_versions.keys(), self.kubernetes_version))
            else:
                self.results = response
                self.results['changed'] = False
                self.log('Results : {0}'.format(response))
                update_tags, response['tags'] = self.update_tags(response['tags'])

                if response['provisioning_state'] == "Succeeded":

                    def is_property_changed(profile, property, ignore_case=False):
                        base = response[profile].get(property)
                        new = getattr(self, profile).get(property)
                        if ignore_case:
                            return base.lower() != new.lower()
                        else:
                            return base != new

                    # Cannot Update the SSH Key for now // Let service to handle it
                    if self.linux_profile and is_property_changed('linux_profile', 'ssh_key'):
                        self.log(("Linux Profile Diff SSH, Was {0} / Now {1}"
                                  .format(response['linux_profile']['ssh_key'], self.linux_profile.get('ssh_key'))))
                        to_be_updated = True
                        # self.module.warn("linux_profile.ssh_key cannot be updated")

                    # self.log("linux_profile response : {0}".format(response['linux_profile'].get('admin_username')))
                    # self.log("linux_profile self : {0}".format(self.linux_profile[0].get('admin_username')))
                    # Cannot Update the Username for now // Let service to handle it
                    if self.linux_profile and is_property_changed('linux_profile', 'admin_username'):
                        self.log(("Linux Profile Diff User, Was {0} / Now {1}"
                                  .format(response['linux_profile']['admin_username'], self.linux_profile.get('admin_username'))))
                        to_be_updated = True
                        # self.module.warn("linux_profile.admin_username cannot be updated")

                    # Cannot have more that one agent pool profile for now
                    if len(response['agent_pool_profiles']) != len(self.agent_pool_profiles):
                        self.log("Agent Pool count is diff, need to update")
                        update_agentpool = True

                    if response['kubernetes_version'] != self.kubernetes_version:
                        upgrade_versions = available_versions.get(response['kubernetes_version']) or available_versions.keys()
                        if upgrade_versions and self.kubernetes_version not in upgrade_versions:
                            self.fail('Cannot upgrade kubernetes version to {0}, supported value are {1}'.format(self.kubernetes_version, upgrade_versions))
                        to_be_updated = True

                    if response['enable_rbac'] != self.enable_rbac:
                        to_be_updated = True

                    if self.disable_local_accounts is not None:
                        if response.get('disable_local_accounts') is None:
                            to_be_updated = True
                        elif bool(self.disable_local_accounts) != bool(response.get('disable_local_accounts')):
                            to_be_updated = True
                        else:
                            self.disable_local_accounts = response.get('disable_local_accounts')

                    if response['api_server_access_profile'] != self.api_server_access_profile and self.api_server_access_profile is not None:
                        if bool(self.api_server_access_profile.get('enable_private_cluster')) != \
                           bool(response['api_server_access_profile'].get('enable_private_cluster')):
                            self.log(("Api Server Access Diff - Origin {0} / Update {1}"
                                     .format(str(self.api_server_access_profile), str(response['api_server_access_profile']))))
                            self.fail("The enable_private_cluster of the api server access profile cannot be updated")
                        elif self.api_server_access_profile.get('authorized_ip_ranges') is not None and \
                                len(self.api_server_access_profile.get('authorized_ip_ranges')) != \
                                len(response['api_server_access_profile'].get('authorized_ip_ranges', [])):
                            self.log(("Api Server Access Diff - Origin {0} / Update {1}"
                                     .format(str(self.api_server_access_profile), str(response['api_server_access_profile']))))
                            to_be_updated = True

                    if self.network_profile:
                        for key in self.network_profile.keys():
                            original = response['network_profile'].get(key) or ''
                            if self.network_profile[key] and self.network_profile[key].lower() != original.lower():
                                to_be_updated = True

                    def compare_addon(origin, patch, config):
                        if not patch:
                            return True
                        if not origin:
                            return False
                        if origin['enabled'] != patch['enabled']:
                            return False
                        config = config or dict()
                        for key in config.keys():
                            if origin.get(config[key]) != patch.get(key):
                                return False
                        return True

                    if self.addon:
                        for key in ADDONS.keys():
                            addon_name = ADDONS[key]['name']
                            if not compare_addon(response['addon'].get(addon_name), self.addon.get(key), ADDONS[key].get('config')):
                                to_be_updated = True

                    if not self.default_compare({}, self.security_profile, response['security_profile'], '', dict(compare=[])):
                        to_be_updated = True
                    else:
                        self.security_profile = response['security_profile']

                    if not self.default_compare({}, self.auto_upgrade_profile, response['auto_upgrade_profile'], '', dict(compare=[])):
                        to_be_updated = True
                    else:
                        self.auto_upgrade_profile = response['auto_upgrade_profile']

                    for profile_result in response['agent_pool_profiles']:
                        matched = False
                        for profile_self in self.agent_pool_profiles:
                            if profile_result['name'] == profile_self['name']:
                                matched = True
                                os_disk_size_gb = profile_self.get('os_disk_size_gb') or profile_result['os_disk_size_gb']
                                vnet_subnet_id = profile_self.get('vnet_subnet_id', profile_result['vnet_subnet_id'])
                                count = profile_self['count']
                                orchestrator_version = profile_self['orchestrator_version']
                                vm_size = profile_self['vm_size']
                                availability_zones = profile_self['availability_zones']
                                enable_auto_scaling = profile_self['enable_auto_scaling']
                                mode = profile_self['mode']
                                max_count = profile_self['max_count']
                                node_labels = profile_self['node_labels']
                                min_count = profile_self['min_count']
                                max_pods = profile_self['max_pods']
                                tags = profile_self['tags']
                                security_profile = profile_self.get('security_profile')

                                if max_pods is not None and profile_result['max_pods'] != max_pods:
                                    self.log(("Agent Profile Diff - Origin {0} / Update {1}".format(str(profile_result), str(profile_self))))
                                    self.fail("The max_pods of the agent pool cannot be updated")
                                elif vnet_subnet_id is not None and profile_result['vnet_subnet_id'] != vnet_subnet_id:
                                    self.log(("Agent Profile Diff - Origin {0} / Update {1}".format(str(profile_result), str(profile_self))))
                                    self.fail("The vnet_subnet_id of the agent pool cannot be updated")
                                elif availability_zones is not None and \
                                        ' '.join(map(str, profile_result['availability_zones'])) != ' '.join(map(str, availability_zones)):
                                    self.log(("Agent Profile Diff - Origin {0} / Update {1}".format(str(profile_result), str(profile_self))))
                                    self.fail("The availability_zones of the agent pool cannot be updated")

                                if count is not None and profile_result['count'] != count:
                                    self.log(("Agent Profile Diff - Origin {0} / Update {1}".format(str(profile_result), str(profile_self))))
                                    to_be_updated = True
                                elif vm_size is not None and profile_result['vm_size'] != vm_size:
                                    self.log(("Agent Profile Diff - Origin {0} / Update {1}".format(str(profile_result), str(profile_self))))
                                    to_be_updated = True
                                elif os_disk_size_gb is not None and profile_result['os_disk_size_gb'] != os_disk_size_gb:
                                    self.log(("Agent Profile Diff - Origin {0} / Update {1}".format(str(profile_result), str(profile_self))))
                                    to_be_updated = True
                                elif enable_auto_scaling is not None and profile_result['enable_auto_scaling'] != enable_auto_scaling:
                                    self.log(("Agent Profile Diff - Origin {0} / Update {1}".format(str(profile_result), str(profile_self))))
                                    to_be_updated = True
                                elif max_count is not None and profile_result['max_count'] != max_count:
                                    self.log(("Agent Profile Diff - Origin {0} / Update {1}".format(str(profile_result), str(profile_self))))
                                    to_be_updated = True
                                elif min_count is not None and profile_result['min_count'] != min_count:
                                    self.log(("Agent Profile Diff - Origin {0} / Update {1}".format(str(profile_result), str(profile_self))))
                                    to_be_updated = True
                                elif mode is not None and profile_result['mode'] != mode:
                                    self.log(("Agent Profile Diff - Origin {0} / Update {1}".format(str(profile_result), str(profile_self))))
                                    to_be_updated = True
                                elif node_labels is not None and profile_result['node_labels'] != node_labels:
                                    self.log(("Agent Profile Diff - Origin {0} / Update {1}".format(str(profile_result), str(profile_self))))
                                    to_be_updated = True
                                elif not self.default_compare({}, tags, profile_result['tags'], '', dict(compare=[])):
                                    self.log("Agent Profile Diff - Origin {0} / Update {1}".format(profile_result['tags'], tags))
                                    to_be_updated = True
                                elif security_profile is not None:
                                    if bool(security_profile['enable_secure_boot']) != bool(profile_result['security_profile']['enable_secure_boot']) or \
                                       bool(security_profile['enable_vtpm']) != bool(profile_result['security_profile']['enable_vtpm']):
                                        self.log(("Agent Profile Diff - Origin {0} / Update {1}".format(str(profile_result), str(profile_self))))
                                        to_be_updated = True

                        if not matched:
                            self.log("Agent Pool not found")
                            to_be_updated = True
                    if not self.default_compare({}, self.pod_identity_profile, response['pod_identity_profile'], '', dict(compare=[])):
                        to_be_updated = True
                    else:
                        self.pod_identity_profile = response['pod_identity_profile']

                    # Default to SystemAssigned if service_principal is not specified
                    if not self.service_principal and not self.identity:
                        self.identity = dotdict({'type': 'SystemAssigned'})
                    if self.identity:
                        changed, self.identity = self.update_identity(self.identity, response['identity'])
                        if changed:
                            to_be_updated = True
                    # Cannot Update the Username for now // Let service to handle it
                    if self.windows_profile and is_property_changed('windows_profile', 'admin_username'):
                        self.log(("Windows Profile Diff User, Was {0} / Now {1}"
                                  .format(response['windows_profile']['admin_username'], self.windows_profile.get('admin_username'))))
                        to_be_updated = True
                        # self.module.warn("windows_profile.admin_username cannot be updated")

            if update_agentpool:
                self.log("Need to update agentpool")
                if not self.check_mode:
                    response_profile_name_list = [response_profile['name'] for response_profile in response['agent_pool_profiles']]
                    self_profile_name_list = [self_profile['name'] for self_profile in self.agent_pool_profiles]
                    to_update = list(set(self_profile_name_list) - set(response_profile_name_list))
                    to_delete = list(set(response_profile_name_list) - set(self_profile_name_list))
                    if len(to_delete) > 0:
                        self.delete_agentpool(to_delete)
                        for profile in self.results['agent_pool_profiles']:
                            if profile['name'] in to_delete:
                                self.results['agent_pool_profiles'].remove(profile)
                    if len(to_update) > 0:
                        self.results['agent_pool_profiles'].extend(self.create_update_agentpool(to_update))
                    self.log("Creation / Update done")
                self.results['changed'] = True

            if to_be_updated:
                self.log("Need to Create / Update the AKS instance")

                if not self.check_mode:
                    self.results = self.create_update_aks()
                    self.log("Creation / Update done")

                self.results['changed'] = True
            elif update_tags:
                self.log("Need to Update the AKS tags")

                if not self.check_mode:
                    self.results['tags'] = self.update_aks_tags()
                self.results['changed'] = True
            return self.results

        elif self.state == 'absent' and response:
            self.log("Need to Delete the AKS instance")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_aks()

            self.log("AKS instance deleted")

        return self.results

    def create_update_aks(self):
        '''
        Creates or updates a managed Azure container service (AKS) with the specified configuration of agents.

        :return: deserialized AKS instance state dictionary
        '''
        self.log("Creating / Updating the AKS instance {0}".format(self.name))

        agentpools = []

        if self.agent_pool_profiles:
            agentpools = [self.create_agent_pool_profile_instance(profile) for profile in self.agent_pool_profiles]

        # Only service_principal or identity can be specified, but default to SystemAssigned if none specified.
        if self.service_principal:
            service_principal_profile = self.create_service_principal_profile_instance(self.service_principal)
            identity = None
        else:
            service_principal_profile = None

        if self.linux_profile:
            linux_profile = self.create_linux_profile_instance(self.linux_profile)
        else:
            linux_profile = None

        if self.windows_profile:
            windows_profile = self.create_windows_profile_instance(self.windows_profile)
        else:
            windows_profile = None

        if self.pod_identity_profile:
            pod_identity_profile = self.managedcluster_models.ManagedClusterPodIdentityProfile(
                enabled=self.pod_identity_profile.get('enabled'),
                allow_network_plugin_kubenet=self.pod_identity_profile.get('allow_network_plugin_kubenet'),
                user_assigned_identities=self.pod_identity_profile.get('user_assigned_identities')
            )
        else:
            pod_identity_profile = None

        if self.auto_upgrade_profile is not None:
            auto_upgrade_profile = self.managedcluster_models.ManagedClusterAutoUpgradeProfile(
                upgrade_channel=self.auto_upgrade_profile.get('upgrade_channel'),
                node_os_upgrade_channel=self.auto_upgrade_profile.get('node_os_upgrade_channel')
            )
        else:
            auto_upgrade_profile = None

        if self.security_profile is not None:
            security_profile = self.managedcluster_models.ManagedClusterSecurityProfile(**self.security_profile)
        else:
            security_profile = None

        parameters = self.managedcluster_models.ManagedCluster(
            location=self.location,
            dns_prefix=self.dns_prefix,
            kubernetes_version=self.kubernetes_version,
            tags=self.tags,
            service_principal_profile=service_principal_profile,
            agent_pool_profiles=agentpools,
            linux_profile=linux_profile,
            windows_profile=windows_profile,
            identity=self.identity,
            enable_rbac=self.enable_rbac,
            network_profile=self.create_network_profile_instance(self.network_profile),
            aad_profile=self.create_aad_profile_instance(self.aad_profile),
            api_server_access_profile=self.create_api_server_access_profile_instance(self.api_server_access_profile),
            addon_profiles=self.create_addon_profile_instance(self.addon),
            node_resource_group=self.node_resource_group,
            pod_identity_profile=pod_identity_profile,
            auto_upgrade_profile=auto_upgrade_profile,
            disable_local_accounts=self.disable_local_accounts,
            security_profile=security_profile,
        )

        # self.log("service_principal_profile : {0}".format(parameters.service_principal_profile))
        # self.log("linux_profile : {0}".format(parameters.linux_profile))
        # self.log("ssh from yaml : {0}".format(results.get('linux_profile')[0]))
        # self.log("ssh : {0}".format(parameters.linux_profile.ssh))
        # self.log("agent_pool_profiles : {0}".format(parameters.agent_pool_profiles))

        try:
            poller = self.managedcluster_client.managed_clusters.begin_create_or_update(self.resource_group, self.name, parameters)
            response = self.get_poller_result(poller)
            response.kube_config = self.get_aks_kubeconfig()
            return create_aks_dict(response)
        except Exception as exc:
            self.log('Error attempting to create the AKS instance.')
            self.fail("Error creating the AKS instance: {0}".format(exc.message))

    def update_aks_tags(self):
        try:
            poller = self.managedcluster_client.managed_clusters.begin_update_tags(self.resource_group, self.name, self.tags)
            response = self.get_poller_result(poller)
            return response.tags
        except Exception as exc:
            self.fail("Error attempting to update AKS tags: {0}".format(exc.message))

    def create_update_agentpool(self, to_update_name_list):
        response_all = []
        for profile in self.agent_pool_profiles:
            if (profile['name'] in to_update_name_list):
                self.log("Creating / Updating the AKS agentpool {0}".format(profile['name']))
                parameters = self.managedcluster_models.AgentPool(
                    count=profile["count"],
                    vm_size=profile["vm_size"],
                    os_disk_size_gb=profile["os_disk_size_gb"],
                    max_count=profile["max_count"],
                    node_labels=profile["node_labels"],
                    min_count=profile["min_count"],
                    orchestrator_version=profile["orchestrator_version"],
                    max_pods=profile["max_pods"],
                    enable_auto_scaling=profile["enable_auto_scaling"],
                    agent_pool_type=profile["type"],
                    mode=profile["mode"],
                    tags=profile['tags'],
                    security_profile=profile['security_profile']
                )
                try:
                    poller = self.managedcluster_client.agent_pools.begin_create_or_update(self.resource_group, self.name, profile["name"], parameters)
                    response = self.get_poller_result(poller)
                    response_all.append(response)
                except Exception as exc:
                    self.fail("Error attempting to update AKS agentpool: {0}".format(exc.message))
        return create_agent_pool_profiles_dict(response_all)

    def delete_agentpool(self, to_delete_name_list):
        for name in to_delete_name_list:
            self.log("Deleting the AKS agentpool {0}".format(name))
            try:
                poller = self.managedcluster_client.agent_pools.begin_delete(self.resource_group, self.name, name)
                self.get_poller_result(poller)
            except Exception as exc:
                self.fail("Error attempting to update AKS agentpool: {0}".format(exc.message))

    def delete_aks(self):
        '''
        Deletes the specified managed container service (AKS) in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the AKS instance {0}".format(self.name))
        try:
            poller = self.managedcluster_client.managed_clusters.begin_delete(self.resource_group, self.name)
            self.get_poller_result(poller)
            return True
        except Exception as e:
            self.log('Error attempting to delete the AKS instance.')
            self.fail("Error deleting the AKS instance: {0}".format(e.message))
            return False

    def get_aks(self):
        '''
        Gets the properties of the specified container service.

        :return: deserialized AKS instance state dictionary
        '''
        self.log("Checking if the AKS instance {0} is present".format(self.name))
        try:
            response = self.managedcluster_client.managed_clusters.get(self.resource_group, self.name)
            self.log("Response : {0}".format(response))
            self.log("AKS instance : {0} found".format(response.name))
            response.kube_config = self.get_aks_kubeconfig()
            return create_aks_dict(response)
        except ResourceNotFoundError:
            self.log('Did not find the AKS instance.')
            return False

    def get_all_versions(self):
        try:
            result = dict()
            response = self.containerservice_client.container_services.list_orchestrators(self.location, resource_type='managedClusters')
            orchestrators = response.orchestrators
            for item in orchestrators:
                result[item.orchestrator_version] = [x.orchestrator_version for x in item.upgrades] if item.upgrades else []
            return result
        except Exception as exc:
            self.fail('Error when getting AKS supported kubernetes version list for location {0} - {1}'.format(self.location, exc.message or str(exc)))

    def get_aks_kubeconfig(self):
        '''
        Gets kubeconfig for the specified AKS instance.

        :return: AKS instance kubeconfig
        '''
        try:
            access_profile = self.managedcluster_client.managed_clusters.list_cluster_user_credentials(self.resource_group, self.name)
        except HttpResponseError as ec:
            self.log("Lists the cluster user credentials of a managed cluster Failed, Exception as {0}".format(ec))
            return []
        return [item.value.decode('utf-8') for item in access_profile.kubeconfigs]

    def create_agent_pool_profile_instance(self, agentpoolprofile):
        '''
        Helper method to serialize a dict to a ManagedClusterAgentPoolProfile
        :param: agentpoolprofile: dict with the parameters to setup the ManagedClusterAgentPoolProfile
        :return: ManagedClusterAgentPoolProfile
        '''
        return self.managedcluster_models.ManagedClusterAgentPoolProfile(**agentpoolprofile)

    def create_service_principal_profile_instance(self, spnprofile):
        '''
        Helper method to serialize a dict to a ManagedClusterServicePrincipalProfile
        :param: spnprofile: dict with the parameters to setup the ManagedClusterServicePrincipalProfile
        :return: ManagedClusterServicePrincipalProfile
        '''
        return self.managedcluster_models.ManagedClusterServicePrincipalProfile(
            client_id=spnprofile['client_id'],
            secret=spnprofile['client_secret']
        )

    def create_linux_profile_instance(self, linuxprofile):
        '''
        Helper method to serialize a dict to a ContainerServiceLinuxProfile
        :param: linuxprofile: dict with the parameters to setup the ContainerServiceLinuxProfile
        :return: ContainerServiceLinuxProfile
        '''
        return self.managedcluster_models.ContainerServiceLinuxProfile(
            admin_username=linuxprofile['admin_username'],
            ssh=self.managedcluster_models.ContainerServiceSshConfiguration(public_keys=[
                self.managedcluster_models.ContainerServiceSshPublicKey(key_data=str(linuxprofile['ssh_key']))])
        )

    def create_windows_profile_instance(self, windowsprofile):
        '''
        Helper method to serialize a dict to a ManagedClusterWindowsProfile
        :param: windowsprofile: dict with the parameters to setup the ManagedClusterWindowsProfile
        :return: ManagedClusterWindowsProfile
        '''
        return self.managedcluster_models.ManagedClusterWindowsProfile(
            admin_username=windowsprofile['admin_username'],
            admin_password=windowsprofile['admin_password']
        )

    def create_network_profile_instance(self, network):
        return self.managedcluster_models.ContainerServiceNetworkProfile(**network) if network else None

    def create_api_server_access_profile_instance(self, server_access):
        return self.managedcluster_models.ManagedClusterAPIServerAccessProfile(**server_access) if server_access else None

    def create_aad_profile_instance(self, aad):
        return self.managedcluster_models.ManagedClusterAADProfile(**aad) if aad else None

    def create_addon_profile_instance(self, addon):
        result = dict()
        addon = addon or {}
        for key in addon.keys():
            if not ADDONS.get(key):
                self.fail('Unsupported addon {0}'.format(key))
            if addon.get(key):
                name = ADDONS[key]['name']
                config_spec = ADDONS[key].get('config') or dict()
                config = addon[key]
                for v in config_spec.keys():
                    config[config_spec[v]] = config[v]
                result[name] = self.managedcluster_models.ManagedClusterAddonProfile(config=config, enabled=config['enabled'])
        return result

    # AKS only supports a single UserAssigned Identity
    def update_identity(self, param_identity, curr_identity):
        user_identity = None
        changed = False
        current_managed_type = curr_identity.get('type', 'SystemAssigned')
        current_managed_identity = curr_identity.get('user_assigned_identities', {})
        param_managed_identity = param_identity.get('user_assigned_identities')

        # If type set to SystamAssigned, and Resource has SystamAssigned, nothing to do
        if 'SystemAssigned' in param_identity.get('type') and current_managed_type == 'SystemAssigned':
            pass
        # If type set to SystemAssigned, and Resource has current identity, remove UserAssigned identity
        elif param_identity.get('type') == 'SystemAssigned':
            changed = True
        # If type in module args contains 'UserAssigned'
        elif 'UserAssigned' in param_identity.get('type'):
            if param_managed_identity not in current_managed_identity.keys():
                user_identity = {param_managed_identity: {}}
                changed = True

        new_identity = self.managedcluster_models.ManagedClusterIdentity(
            type=param_identity.get('type'),
        )
        if user_identity:
            new_identity.user_assigned_identities = user_identity

        return changed, new_identity


def main():
    """Main execution"""
    AzureRMManagedCluster()


if __name__ == '__main__':
    main()
