#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_containerappenvironment
version_added: "4.0.0"
short_description: Manage Azure Container Apps Managed Environment
description:
    - Create, update and delete an Azure Container Apps Managed Environment.
    - Managed environments are the shared runtime that hosts one or more Container Apps.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - Name of the managed environment.
        required: true
        type: str
    location:
        description:
            - Resource location. If not set, location from the resource group will be used.
        type: str
    zone_redundant:
        description:
            - Whether the managed environment is zone-redundant.
            - Requires I(vnet_configuration.infrastructure_subnet_id) to be set.
        type: bool
    vnet_configuration:
        description:
            - VNet configuration for the environment.
        type: dict
        suboptions:
            internal:
                description:
                    - Whether the environment only has an internal load balancer.
                    - Requires I(infrastructure_subnet_id) to be set.
                type: bool
            infrastructure_subnet_id:
                description:
                    - Resource ID of a subnet for infrastructure components.
                type: str
            docker_bridge_cidr:
                description:
                    - CIDR notation IP range assigned to the Docker bridge network.
                type: str
            platform_reserved_cidr:
                description:
                    - IP range in CIDR notation reserved for environment infrastructure IP addresses.
                type: str
            platform_reserved_dns_ip:
                description:
                    - IP address from the range defined by I(platform_reserved_cidr) reserved for the internal DNS server.
                type: str
    app_logs_configuration:
        description:
            - Cluster configuration which enables the log daemon to export app logs.
        type: dict
        suboptions:
            destination:
                description:
                    - Logs destination.
                type: str
                choices:
                    - log-analytics
                    - azure-monitor
                    - none
            log_analytics_configuration:
                description:
                    - Log Analytics configuration. Required when I(destination=log-analytics).
                type: dict
                suboptions:
                    customer_id:
                        description:
                            - Log Analytics workspace customer ID.
                        type: str
                    shared_key:
                        description:
                            - Log Analytics workspace shared key.
                        type: str
    workload_profiles:
        description:
            - Workload profiles configured for the managed environment.
            - When omitted, the environment is created in the Consumption-only workload profile.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Workload profile display name.
                required: true
                type: str
            workload_profile_type:
                description:
                    - Workload profile type. Common values are C(Consumption), C(D4), C(D8), C(D16), C(D32), C(E4), C(E8), C(E16), C(E32).
                required: true
                type: str
            minimum_count:
                description:
                    - Minimum capacity for dedicated workload profiles.
                type: int
            maximum_count:
                description:
                    - Maximum capacity for dedicated workload profiles.
                type: int
    dapr_ai_connection_string:
        description:
            - Application Insights connection string used by Dapr to export Service to Service communication telemetry.
        type: str
    infrastructure_resource_group:
        description:
            - Name of the platform-managed resource group created for the managed environment infrastructure.
            - Read-only unless I(workload_profiles) is set and I(vnet_configuration.infrastructure_subnet_id) is provided.
        type: str
    public_network_access:
        description:
            - Whether the environment accepts traffic from the public network.
        type: str
        choices:
            - Enabled
            - Disabled
    peer_authentication_mtls_enabled:
        description:
            - Whether mutual TLS authentication is enabled between apps in the environment.
        type: bool
    peer_traffic_encryption_enabled:
        description:
            - Whether peer-to-peer traffic encryption is enabled in the environment.
        type: bool
    state:
        description:
            - Assert the state of the managed environment.
            - Use C(present) to create or update, C(absent) to delete.
        default: present
        type: str
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Create a managed environment (Consumption profile, no VNet)
  azure.azcollection.azure_rm_containerappenvironment:
    resource_group: myResourceGroup
    name: myenv
    location: eastus
    app_logs_configuration:
      destination: log-analytics
      log_analytics_configuration:
        customer_id: "{{ workspace_customer_id }}"
        shared_key: "{{ workspace_shared_key }}"

- name: Create a VNet-integrated environment with dedicated workload profile
  azure.azcollection.azure_rm_containerappenvironment:
    resource_group: myResourceGroup
    name: myenv-vnet
    location: eastus
    zone_redundant: true
    vnet_configuration:
      internal: true
      infrastructure_subnet_id: "/subscriptions/xxxx/resourceGroups/net/providers/Microsoft.Network/virtualNetworks/vnet/subnets/aca-infra"
    workload_profiles:
      - name: Consumption
        workload_profile_type: Consumption
      - name: dedicated-d4
        workload_profile_type: D4
        minimum_count: 1
        maximum_count: 3
    peer_authentication_mtls_enabled: true
    tags:
      environment: prod

- name: Delete the managed environment
  azure.azcollection.azure_rm_containerappenvironment:
    resource_group: myResourceGroup
    name: myenv
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the managed environment.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource ID of the managed environment.
            type: str
            returned: always
            sample: "/subscriptions/xxxx/resourceGroups/rg/providers/Microsoft.App/managedEnvironments/myenv"
        name:
            description:
                - Name of the managed environment.
            type: str
            returned: always
            sample: myenv
        type:
            description:
                - Resource type.
            type: str
            returned: always
            sample: Microsoft.App/managedEnvironments
        location:
            description:
                - Resource location.
            type: str
            returned: always
            sample: eastus
        tags:
            description:
                - Resource tags.
            type: dict
            returned: always
            sample: { environment: prod }
        provisioning_state:
            description:
                - Provisioning state of the environment.
            type: str
            returned: always
            sample: Succeeded
        default_domain:
            description:
                - Default domain name for the environment.
            type: str
            returned: always
            sample: myenv.polite-1234abcd.eastus.azurecontainerapps.io
        static_ip:
            description:
                - Static IP of the environment.
            type: str
            returned: always
            sample: 20.10.20.30
        zone_redundant:
            description:
                - Whether the environment is zone redundant.
            type: bool
            returned: always
            sample: false
        vnet_configuration:
            description:
                - VNet configuration used by the environment.
            type: dict
            returned: always
        workload_profiles:
            description:
                - Workload profiles configured on the environment.
            type: list
            returned: always
        app_logs_configuration:
            description:
                - App logs configuration for the environment.
            type: dict
            returned: always
        public_network_access:
            description:
                - Whether the environment accepts public network traffic.
            type: str
            returned: always
            sample: Enabled
'''

try:
    from azure.core.polling import LROPoller
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.appcontainers.models import (
        ManagedEnvironment, VnetConfiguration, AppLogsConfiguration,
        LogAnalyticsConfiguration, WorkloadProfile,
        ManagedEnvironmentPropertiesPeerAuthentication, Mtls,
        ManagedEnvironmentPropertiesPeerTrafficConfiguration,
        ManagedEnvironmentPropertiesPeerTrafficConfigurationEncryption,
    )
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


def _normalize(obj):
    """
    Return a snake_case flat dict for an ``azure-mgmt-appcontainers`` model.
    """
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj
    return as_attribute_dict(obj, exclude_readonly=False)


def _build_env_model(params):
    """Construct a ``ManagedEnvironment`` from a snake_case dict.

    ``azure-mgmt-appcontainers`` 5.0.0 uses hybrid/typed models — passing a
    flat dict directly leaves resource-specific fields at the top level
    instead of ARM's required ``properties`` envelope. Build the model tree
    explicitly (mirroring the ``azure_rm_keyvault`` migration pattern) so the
    wire payload is nested under ``properties`` with correct camelCase keys.
    """
    vnet = params.get('vnet_configuration')
    if vnet is not None:
        vnet = VnetConfiguration(**{k: v for k, v in vnet.items() if v is not None})

    logs = params.get('app_logs_configuration')
    if logs is not None:
        la = logs.get('log_analytics_configuration')
        if la is not None:
            la = LogAnalyticsConfiguration(**{k: v for k, v in la.items() if v is not None})
        logs = AppLogsConfiguration(destination=logs.get('destination'), log_analytics_configuration=la)

    profiles = params.get('workload_profiles')
    if profiles is not None:
        profiles = [WorkloadProfile(**{k: v for k, v in wp.items() if v is not None}) for wp in profiles]

    peer_auth = params.get('peer_authentication')
    if peer_auth is not None:
        mtls_cfg = peer_auth.get('mtls')
        mtls_cfg = Mtls(**mtls_cfg) if mtls_cfg else None
        peer_auth = ManagedEnvironmentPropertiesPeerAuthentication(mtls=mtls_cfg)

    peer_traffic = params.get('peer_traffic_configuration')
    if peer_traffic is not None:
        enc = peer_traffic.get('encryption')
        enc = ManagedEnvironmentPropertiesPeerTrafficConfigurationEncryption(**enc) if enc else None
        peer_traffic = ManagedEnvironmentPropertiesPeerTrafficConfiguration(encryption=enc)

    return ManagedEnvironment(
        location=params.get('location'),
        tags=params.get('tags'),
        zone_redundant=params.get('zone_redundant'),
        vnet_configuration=vnet,
        app_logs_configuration=logs,
        workload_profiles=profiles,
        dapr_ai_connection_string=params.get('dapr_ai_connection_string'),
        infrastructure_resource_group=params.get('infrastructure_resource_group'),
        public_network_access=params.get('public_network_access'),
        peer_authentication=peer_auth,
        peer_traffic_configuration=peer_traffic,
    )


class Actions:
    NoAction, Create, Update, Delete = range(4)


vnet_configuration_spec = dict(
    internal=dict(type='bool'),
    infrastructure_subnet_id=dict(type='str'),
    docker_bridge_cidr=dict(type='str'),
    platform_reserved_cidr=dict(type='str'),
    platform_reserved_dns_ip=dict(type='str'),
)


log_analytics_configuration_spec = dict(
    customer_id=dict(type='str'),
    shared_key=dict(type='str', no_log=True),
)


app_logs_configuration_spec = dict(
    destination=dict(type='str', choices=['log-analytics', 'azure-monitor', 'none']),
    log_analytics_configuration=dict(type='dict', options=log_analytics_configuration_spec),
)


workload_profile_spec = dict(
    name=dict(type='str', required=True),
    workload_profile_type=dict(type='str', required=True),
    minimum_count=dict(type='int'),
    maximum_count=dict(type='int'),
)


class AzureRMContainerAppEnvironment(AzureRMModuleBaseExt):
    """Manage Container Apps Managed Environment resources."""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            zone_redundant=dict(type='bool'),
            vnet_configuration=dict(type='dict', options=vnet_configuration_spec),
            app_logs_configuration=dict(type='dict', options=app_logs_configuration_spec),
            workload_profiles=dict(type='list', elements='dict', options=workload_profile_spec),
            dapr_ai_connection_string=dict(type='str', no_log=True),
            infrastructure_resource_group=dict(type='str'),
            public_network_access=dict(type='str', choices=['Enabled', 'Disabled']),
            peer_authentication_mtls_enabled=dict(type='bool'),
            peer_traffic_encryption_enabled=dict(type='bool'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.tags = None
        self.state = None

        self.parameters = dict()
        self.update_parameters = dict()

        self.results = dict(changed=False)
        self.to_do = Actions.NoAction

        super(AzureRMContainerAppEnvironment, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=True,
        )

    def exec_module(self, **kwargs):
        """Main module execution."""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self._assign_parameter(key, kwargs[key])

        resource_group = self.get_resource_group(self.resource_group)
        if self.location is None:
            self.location = resource_group.location
        self.parameters['location'] = self.location

        old_response = self.get_resource()

        changed = False
        if old_response is None:
            if self.state == 'present':
                self.to_do = Actions.Create
                changed = True
        else:
            if self.state == 'absent':
                self.to_do = Actions.Delete
                changed = True
            else:
                update_tags, self.update_parameters['tags'] = self.update_tags(old_response.get('tags'))
                if update_tags:
                    changed = True
                    self.to_do = Actions.Update

                for item in ('zone_redundant', 'public_network_access', 'infrastructure_resource_group',
                             'vnet_configuration', 'app_logs_configuration', 'workload_profiles',
                             'peer_authentication', 'peer_traffic_configuration'):
                    if not self.default_compare({}, self.parameters.get(item), old_response.get(item), '', dict(compare=[])):
                        changed = True
                        self.to_do = Actions.Update

        if self.to_do in (Actions.Create, Actions.Update):
            if not self.check_mode:
                self.create_update_resource()
                self.results['state'] = self.get_resource()
            else:
                self.results['state'] = old_response or self.parameters
        elif self.to_do == Actions.Delete:
            if not self.check_mode:
                self.delete_resource()
            self.results['state'] = dict()
        else:
            self.results['state'] = old_response or dict()

        self.results['changed'] = changed
        return self.results

    def _assign_parameter(self, key, value):
        if key == 'peer_authentication_mtls_enabled':
            self.parameters.setdefault('peer_authentication', dict())['mtls'] = dict(enabled=value)
            self.update_parameters.setdefault('peer_authentication', dict())['mtls'] = dict(enabled=value)
        elif key == 'peer_traffic_encryption_enabled':
            self.parameters.setdefault('peer_traffic_configuration', dict())['encryption'] = dict(enabled=value)
            self.update_parameters.setdefault('peer_traffic_configuration', dict())['encryption'] = dict(enabled=value)
        else:
            self.parameters[key] = value
            # A subset of properties are updatable via PATCH
            if key in ('workload_profiles', 'app_logs_configuration', 'vnet_configuration',
                       'public_network_access', 'dapr_ai_connection_string',
                       'peer_authentication', 'peer_traffic_configuration'):
                self.update_parameters[key] = value

    def create_update_resource(self):
        self.log("Creating / Updating managed environment {0}".format(self.name))
        try:
            if self.to_do == Actions.Create:
                self.parameters['tags'] = self.tags
                envelope = _build_env_model(self.parameters)
                response = self.containerapps_client.managed_environments.begin_create_or_update(
                    resource_group_name=self.resource_group,
                    environment_name=self.name,
                    environment_envelope=envelope,
                )
            else:
                envelope = _build_env_model(self.update_parameters)
                response = self.containerapps_client.managed_environments.begin_update(
                    resource_group_name=self.resource_group,
                    environment_name=self.name,
                    environment_envelope=envelope,
                )
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error creating/updating managed environment {0}: {1}".format(self.name, str(exc)))

        return self.format_item(response)

    def delete_resource(self):
        self.log("Deleting managed environment {0}".format(self.name))
        try:
            response = self.containerapps_client.managed_environments.begin_delete(
                resource_group_name=self.resource_group,
                environment_name=self.name,
            )
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error deleting managed environment {0}: {1}".format(self.name, str(exc)))
        return True

    def get_resource(self):
        self.log("Checking if managed environment {0} exists".format(self.name))
        try:
            response = self.containerapps_client.managed_environments.get(
                resource_group_name=self.resource_group,
                environment_name=self.name,
            )
        except ResourceNotFoundError:
            return None
        except Exception as exc:
            self.fail("Error retrieving managed environment {0}: {1}".format(self.name, str(exc)))
        return self.format_item(response)

    def format_item(self, item):
        if item is None:
            return None
        normalized = _normalize(item)
        if normalized.get('id'):
            parsed = self.parse_resource_to_dict(normalized['id'])
            normalized['resource_group'] = parsed.get('resource_group')
        else:
            normalized['resource_group'] = self.resource_group
        return normalized


def main():
    AzureRMContainerAppEnvironment()


if __name__ == '__main__':
    main()
