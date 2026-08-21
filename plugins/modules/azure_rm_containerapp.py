#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_containerapp
version_added: "4.0.0"
short_description: Manage Azure Container Apps
description:
    - Create, update, delete, start and stop an Azure Container App.
    - Container Apps run in a Managed Environment created with M(azure.azcollection.azure_rm_containerappenvironment).

options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - Name of the container app.
        required: true
        type: str
    location:
        description:
            - Resource location. If not set, location from the resource group will be used.
        type: str
    environment_id:
        description:
            - Full resource ID of the parent managed environment.
            - Required when creating a container app.
        type: str
    workload_profile_name:
        description:
            - Workload profile name to pin the app to. Must exist on the parent environment.
        type: str
    identity:
        description:
            - Managed identity assigned to the container app.
        type: dict
        suboptions:
            type:
                description:
                    - Type of the managed identity.
                type: str
                choices:
                    - SystemAssigned
                    - UserAssigned
                    - 'SystemAssigned, UserAssigned'
                    - None
                default: None
            user_assigned_identities:
                description:
                    - User-assigned managed identities.
                type: dict
                default: {}
                suboptions:
                    id:
                        description:
                            - List of resource IDs of user-assigned managed identities.
                        type: list
                        elements: str
                        default: []
                    append:
                        description:
                            - Whether to append the provided identities to any already assigned.
                        type: bool
                        default: true
    active_revisions_mode:
        description:
            - Active revisions mode for the container app.
        type: str
        choices:
            - Single
            - Multiple
    secrets:
        description:
            - List of secrets exposed to the container app.
        type: list
        elements: dict
        suboptions:
            name:
                description: Secret name.
                type: str
                required: true
            value:
                description: Secret value.
                type: str
            key_vault_url:
                description: Azure Key Vault URL pointing at the secret.
                type: str
            identity:
                description: Resource ID of the managed identity used to access the Key Vault secret. Use C(system) for system-assigned.
                type: str
    registries:
        description:
            - Container image registries the container app pulls from.
        type: list
        elements: dict
        suboptions:
            server:
                description: Container registry server (for example C(myacr.azurecr.io)).
                type: str
                required: true
            username:
                description: Registry username. Omit when using managed identity.
                type: str
            password_secret_ref:
                description: Name of the secret in I(secrets) that contains the registry password.
                type: str
            identity:
                description: Resource ID of a user-assigned managed identity, or C(system) for system-assigned.
                type: str
    ingress:
        description:
            - Ingress configuration for the container app.
        type: dict
        suboptions:
            external:
                description: Whether ingress is externally reachable.
                type: bool
            target_port:
                description: Container port that ingress forwards to.
                type: int
            exposed_port:
                description: Exposed TCP port (transport C(tcp) only).
                type: int
            transport:
                description: Transport protocol.
                type: str
                choices: [auto, http, http2, tcp]
            allow_insecure:
                description: Allow insecure HTTP connections.
                type: bool
            client_certificate_mode:
                description: Client certificate mode.
                type: str
                choices: [ignore, accept, require]
            traffic:
                description: Traffic weights across revisions.
                type: list
                elements: dict
                suboptions:
                    revision_name:
                        description: Target revision name.
                        type: str
                    weight:
                        description: Traffic weight assigned to the revision.
                        type: int
                    label:
                        description: Associates a traffic label with a revision.
                        type: str
                    latest_revision:
                        description: Whether the traffic weight targets the latest revision.
                        type: bool
            custom_domains:
                description: Custom domain bindings.
                type: list
                elements: dict
                suboptions:
                    name:
                        description: Domain hostname.
                        type: str
                        required: true
                    binding_type:
                        description: Binding type.
                        type: str
                        choices: [Disabled, SniEnabled]
                    certificate_id:
                        description: Resource ID of the certificate.
                        type: str
            ip_security_restrictions:
                description: IP-based restrictions.
                type: list
                elements: dict
                suboptions:
                    name:
                        description: Rule name.
                        type: str
                        required: true
                    description:
                        description: Rule description.
                        type: str
                    ip_address_range:
                        description: CIDR notation for the range.
                        type: str
                        required: true
                    action:
                        description: Allow or Deny.
                        type: str
                        choices: [Allow, Deny]
                        required: true
            cors_policy:
                description: CORS policy pass-through as an SDK-shaped dict.
                type: dict
    dapr:
        description:
            - Dapr configuration for the container app.
        type: dict
        suboptions:
            enabled:
                description: Whether Dapr is enabled on the app.
                type: bool
            app_id:
                description: Dapr application identifier.
                type: str
            app_protocol:
                description: Protocol Dapr uses to talk to the app.
                type: str
                choices: [http, grpc]
            app_port:
                description: Port on which the app listens.
                type: int
            enable_api_logging:
                description: Enables API logging for the Dapr sidecar.
                type: bool
            log_level:
                description: Dapr sidecar log level.
                type: str
                choices: [info, debug, warn, error]
            http_read_buffer_size:
                description: Maximum size of HTTP header read buffer in kilobytes.
                type: int
            http_max_request_size:
                description: Increasing max size of request body http server parameter in kilobytes.
                type: int
    max_inactive_revisions:
        description:
            - Maximum number of inactive revisions the app will keep.
        type: int
    revision_suffix:
        description:
            - User-friendly suffix appended to the revision name.
        type: str
    termination_grace_period_seconds:
        description:
            - Optional duration in seconds the app instance needs to terminate gracefully.
        type: int
    containers:
        description:
            - List of containers that make up the app.
        type: list
        elements: dict
        suboptions:
            name:
                description: Container name.
                type: str
                required: true
            image:
                description: Container image tag.
                type: str
                required: true
            command:
                description: Container start command.
                type: list
                elements: str
            args:
                description: Container start command arguments.
                type: list
                elements: str
            env:
                description: Container environment variables.
                type: list
                elements: dict
                suboptions:
                    name:
                        description: Environment variable name.
                        type: str
                        required: true
                    value:
                        description: Environment variable value.
                        type: str
                    secret_ref:
                        description: Name of the container-app secret to pull the value from.
                        type: str
            resources:
                description: Container resource requests.
                type: dict
                suboptions:
                    cpu:
                        description: CPU cores in decimal notation.
                        type: float
                    memory:
                        description: Memory (for example C(0.5Gi), C(1Gi)).
                        type: str
                    ephemeral_storage:
                        description: Ephemeral storage.
                        type: str
            probes:
                description: List of probes for the container.
                type: list
                elements: dict
            volume_mounts:
                description: List of volume mounts inside the container.
                type: list
                elements: dict
                suboptions:
                    volume_name:
                        description: Volume name.
                        type: str
                    mount_path:
                        description: Mount path inside the container.
                        type: str
                    sub_path:
                        description: Path inside the volume.
                        type: str
    init_containers:
        description:
            - Container definitions that run before the app containers.
            - Same schema as I(containers).
        type: list
        elements: dict
        suboptions:
            name:
                description: Init container name.
                type: str
                required: true
            image:
                description: Init container image tag.
                type: str
                required: true
            command:
                description: Init container start command.
                type: list
                elements: str
            args:
                description: Init container start command arguments.
                type: list
                elements: str
            env:
                description: Init container environment variables.
                type: list
                elements: dict
                suboptions:
                    name:
                        description: Environment variable name.
                        type: str
                        required: true
                    value:
                        description: Environment variable value.
                        type: str
                    secret_ref:
                        description: Name of the container-app secret to pull the value from.
                        type: str
            resources:
                description: Init container resource requests.
                type: dict
                suboptions:
                    cpu:
                        description: CPU cores in decimal notation.
                        type: float
                    memory:
                        description: Memory (for example C(0.5Gi), C(1Gi)).
                        type: str
                    ephemeral_storage:
                        description: Ephemeral storage.
                        type: str
            volume_mounts:
                description: List of volume mounts inside the init container.
                type: list
                elements: dict
                suboptions:
                    volume_name:
                        description: Volume name.
                        type: str
                    mount_path:
                        description: Mount path inside the container.
                        type: str
                    sub_path:
                        description: Path inside the volume.
                        type: str
    scale:
        description:
            - Scaling configuration.
        type: dict
        suboptions:
            min_replicas:
                description: Minimum replica count.
                type: int
            max_replicas:
                description: Maximum replica count.
                type: int
            cooldown_period:
                description: Cooldown period in seconds after scaling.
                type: int
            polling_interval:
                description: Interval in seconds between scaling decisions.
                type: int
            rules:
                description:
                    - List of KEDA scaling rules.
                    - Each item follows the SDK ScaleRule model shape.
                type: list
                elements: dict
    volumes:
        description:
            - List of volumes for containers to mount.
        type: list
        elements: dict
    status:
        description:
            - Runtime action to apply after any create/update.
            - C(start) starts a stopped app. C(stop) stops a running app.
        type: str
        choices:
            - start
            - stop
    state:
        description:
            - Assert the state of the container app.
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
- name: Create minimal container app
  azure.azcollection.azure_rm_containerapp:
    resource_group: myResourceGroup
    name: hello
    environment_id: "/subscriptions/xxxx/resourceGroups/myResourceGroup/providers/Microsoft.App/managedEnvironments/myenv"
    ingress:
      external: true
      target_port: 80
      transport: auto
    containers:
      - name: hello
        image: mcr.microsoft.com/k8se/quickstart:latest
        resources:
          cpu: 0.25
          memory: 0.5Gi
    scale:
      min_replicas: 0
      max_replicas: 3

- name: Container app pulling from ACR with user-assigned managed identity
  azure.azcollection.azure_rm_containerapp:
    resource_group: myResourceGroup
    name: private-app
    environment_id: "{{ env_id }}"
    identity:
      type: UserAssigned
      user_assigned_identities:
        id:
          - "/subscriptions/xxxx/resourceGroups/myResourceGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aca-pull"
    registries:
      - server: myacr.azurecr.io
        identity: "/subscriptions/xxxx/resourceGroups/myResourceGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aca-pull"
    containers:
      - name: app
        image: myacr.azurecr.io/hello:1.0
        resources:
          cpu: 0.5
          memory: 1Gi

- name: Stop the container app
  azure.azcollection.azure_rm_containerapp:
    resource_group: myResourceGroup
    name: hello
    status: stop

- name: Delete the container app
  azure.azcollection.azure_rm_containerapp:
    resource_group: myResourceGroup
    name: hello
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the container app.
    returned: always
    type: complex
    contains:
        id:
            description: Fully qualified resource ID.
            type: str
            returned: always
        name:
            description: Container app name.
            type: str
            returned: always
        location:
            description: Resource location.
            type: str
            returned: always
        provisioning_state:
            description: Provisioning state.
            type: str
            returned: always
        latest_revision_name:
            description: Latest revision name of the app.
            type: str
            returned: always
        latest_revision_fqdn:
            description: FQDN of the latest revision.
            type: str
            returned: always
        configuration:
            description: App configuration.
            type: dict
            returned: always
        template:
            description: App template with containers and scaling.
            type: dict
            returned: always
'''

try:
    from azure.core.polling import LROPoller
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.appcontainers.models import (
        ContainerApp, Configuration, Template, Ingress, Dapr, Scale, ScaleRule,
        HttpScaleRule, TcpScaleRule, QueueScaleRule, CustomScaleRule,
        ScaleRuleAuth, Container, InitContainer, ContainerResources,
        ContainerAppProbe, ContainerAppProbeHttpGet, ContainerAppProbeTcpSocket,
        ContainerAppProbeHttpGetHttpHeadersItem, EnvironmentVar, VolumeMount,
        Volume, Secret, RegistryCredentials, TrafficWeight, CustomDomain,
        IpSecurityRestrictionRule, CorsPolicy, IngressStickySessions,
        IngressPortMapping, ServiceBind,
        ManagedServiceIdentity, UserAssignedIdentity,
    )
except ImportError:
    pass

import copy

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


def _strip_write_only(parameters):
    """
    Remove fields that Azure never returns on read (secret values, etc.)
    so idempotence compare against the fetched state does not always report a
    diff.
    """
    sanitized = copy.deepcopy(parameters)
    config = sanitized.get('configuration') or {}
    for secret in (config.get('secrets') or []):
        secret.pop('value', None)
    return sanitized


def _clean(model_cls, data):
    """Instantiate ``model_cls(**data)`` skipping ``None`` values so we do not
    override server defaults with explicit nulls.
    """
    if data is None:
        return None
    return model_cls(**{k: v for k, v in data.items() if v is not None})


def _build_ingress(ingress):
    if ingress is None:
        return None
    data = dict(ingress)
    if data.get('traffic') is not None:
        data['traffic'] = [_clean(TrafficWeight, t) for t in data['traffic']]
    if data.get('custom_domains') is not None:
        data['custom_domains'] = [_clean(CustomDomain, c) for c in data['custom_domains']]
    if data.get('ip_security_restrictions') is not None:
        data['ip_security_restrictions'] = [_clean(IpSecurityRestrictionRule, r) for r in data['ip_security_restrictions']]
    if data.get('cors_policy') is not None:
        data['cors_policy'] = _clean(CorsPolicy, data['cors_policy'])
    if data.get('sticky_sessions') is not None:
        data['sticky_sessions'] = _clean(IngressStickySessions, data['sticky_sessions'])
    if data.get('additional_port_mappings') is not None:
        data['additional_port_mappings'] = [_clean(IngressPortMapping, p) for p in data['additional_port_mappings']]
    return _clean(Ingress, data)


def _build_probe(probe):
    if probe is None:
        return None
    data = dict(probe)
    hg = data.get('http_get')
    if hg is not None:
        hg_data = dict(hg)
        if hg_data.get('http_headers') is not None:
            hg_data['http_headers'] = [_clean(ContainerAppProbeHttpGetHttpHeadersItem, h) for h in hg_data['http_headers']]
        data['http_get'] = _clean(ContainerAppProbeHttpGet, hg_data)
    if data.get('tcp_socket') is not None:
        data['tcp_socket'] = _clean(ContainerAppProbeTcpSocket, data['tcp_socket'])
    return _clean(ContainerAppProbe, data)


def _build_container(c, is_init=False):
    if c is None:
        return None
    data = dict(c)
    if data.get('env') is not None:
        data['env'] = [_clean(EnvironmentVar, e) for e in data['env']]
    if data.get('resources') is not None:
        data['resources'] = _clean(ContainerResources, data['resources'])
    if data.get('volume_mounts') is not None:
        data['volume_mounts'] = [_clean(VolumeMount, v) for v in data['volume_mounts']]
    if data.get('probes') is not None:
        data['probes'] = [_build_probe(p) for p in data['probes']]
    return _clean(InitContainer if is_init else Container, data)


def _build_scale_rule(rule):
    if rule is None:
        return None
    data = dict(rule)
    for shape, cls in (('http', HttpScaleRule), ('tcp', TcpScaleRule),
                       ('azure_queue', QueueScaleRule), ('custom', CustomScaleRule)):
        if data.get(shape) is not None:
            inner = dict(data[shape])
            if inner.get('auth') is not None:
                inner['auth'] = [_clean(ScaleRuleAuth, a) for a in inner['auth']]
            data[shape] = _clean(cls, inner)
    return _clean(ScaleRule, data)


def _build_scale(scale):
    if scale is None:
        return None
    data = dict(scale)
    if data.get('rules') is not None:
        data['rules'] = [_build_scale_rule(r) for r in data['rules']]
    return _clean(Scale, data)


def _build_configuration(config):
    if config is None:
        return None
    data = dict(config)
    if data.get('secrets') is not None:
        data['secrets'] = [_clean(Secret, s) for s in data['secrets']]
    if data.get('registries') is not None:
        data['registries'] = [_clean(RegistryCredentials, r) for r in data['registries']]
    if data.get('ingress') is not None:
        data['ingress'] = _build_ingress(data['ingress'])
    if data.get('dapr') is not None:
        data['dapr'] = _clean(Dapr, data['dapr'])
    return _clean(Configuration, data)


def _build_template(template):
    if template is None:
        return None
    data = dict(template)
    if data.get('containers') is not None:
        data['containers'] = [_build_container(c, is_init=False) for c in data['containers']]
    if data.get('init_containers') is not None:
        data['init_containers'] = [_build_container(c, is_init=True) for c in data['init_containers']]
    if data.get('scale') is not None:
        data['scale'] = _build_scale(data['scale'])
    if data.get('volumes') is not None:
        data['volumes'] = [_clean(Volume, v) for v in data['volumes']]
    if data.get('service_binds') is not None:
        data['service_binds'] = [_clean(ServiceBind, s) for s in data['service_binds']]
    return _clean(Template, data)


def _build_identity_model(identity):
    if identity is None:
        return None
    data = dict(identity)
    if data.get('user_assigned_identities') is not None:
        data['user_assigned_identities'] = {
            k: _clean(UserAssignedIdentity, v) if isinstance(v, dict) else v
            for k, v in data['user_assigned_identities'].items()
        }
    return _clean(ManagedServiceIdentity, data)


def _build_app_model(params):
    """Construct a ``ContainerApp`` model tree from a snake_case dict.

    ``azure-mgmt-appcontainers`` 5.0.0 typed models require explicit model
    instances so the ARM wire payload nests resource fields under
    ``properties`` with correct camelCase keys (mirrors ``azure_rm_keyvault``
    14.0.1 pattern).
    """
    return ContainerApp(
        location=params.get('location'),
        tags=params.get('tags'),
        identity=_build_identity_model(params.get('identity')),
        kind=params.get('kind'),
        managed_environment_id=params.get('managed_environment_id'),
        workload_profile_name=params.get('workload_profile_name'),
        configuration=_build_configuration(params.get('configuration')),
        template=_build_template(params.get('template')),
    )


class Actions:
    NoAction, Create, Update, Delete = range(4)


SECRET_SPEC = dict(
    name=dict(type='str', required=True),
    value=dict(type='str', no_log=True),
    key_vault_url=dict(type='str', no_log=False),
    identity=dict(type='str'),
)


REGISTRY_SPEC = dict(
    server=dict(type='str', required=True),
    username=dict(type='str'),
    password_secret_ref=dict(type='str', no_log=False),
    identity=dict(type='str'),
)


TRAFFIC_SPEC = dict(
    revision_name=dict(type='str'),
    weight=dict(type='int'),
    label=dict(type='str'),
    latest_revision=dict(type='bool'),
)


CUSTOM_DOMAIN_SPEC = dict(
    name=dict(type='str', required=True),
    binding_type=dict(type='str', choices=['Disabled', 'SniEnabled']),
    certificate_id=dict(type='str'),
)


IP_RESTRICTION_SPEC = dict(
    name=dict(type='str', required=True),
    description=dict(type='str'),
    ip_address_range=dict(type='str', required=True),
    action=dict(type='str', choices=['Allow', 'Deny'], required=True),
)


INGRESS_SPEC = dict(
    external=dict(type='bool'),
    target_port=dict(type='int'),
    exposed_port=dict(type='int'),
    transport=dict(type='str', choices=['auto', 'http', 'http2', 'tcp']),
    allow_insecure=dict(type='bool'),
    client_certificate_mode=dict(type='str', choices=['ignore', 'accept', 'require']),
    traffic=dict(type='list', elements='dict', options=TRAFFIC_SPEC),
    custom_domains=dict(type='list', elements='dict', options=CUSTOM_DOMAIN_SPEC),
    ip_security_restrictions=dict(type='list', elements='dict', options=IP_RESTRICTION_SPEC),
    cors_policy=dict(type='dict'),
)


DAPR_SPEC = dict(
    enabled=dict(type='bool'),
    app_id=dict(type='str'),
    app_protocol=dict(type='str', choices=['http', 'grpc']),
    app_port=dict(type='int'),
    enable_api_logging=dict(type='bool'),
    log_level=dict(type='str', choices=['info', 'debug', 'warn', 'error']),
    http_read_buffer_size=dict(type='int'),
    http_max_request_size=dict(type='int'),
)


ENV_VAR_SPEC = dict(
    name=dict(type='str', required=True),
    value=dict(type='str'),
    secret_ref=dict(type='str', no_log=False),
)


RESOURCES_SPEC = dict(
    cpu=dict(type='float'),
    memory=dict(type='str'),
    ephemeral_storage=dict(type='str'),
)


VOLUME_MOUNT_SPEC = dict(
    volume_name=dict(type='str'),
    mount_path=dict(type='str'),
    sub_path=dict(type='str'),
)


CONTAINER_SPEC = dict(
    name=dict(type='str', required=True),
    image=dict(type='str', required=True),
    command=dict(type='list', elements='str'),
    args=dict(type='list', elements='str'),
    env=dict(type='list', elements='dict', options=ENV_VAR_SPEC),
    resources=dict(type='dict', options=RESOURCES_SPEC),
    probes=dict(type='list', elements='dict'),
    volume_mounts=dict(type='list', elements='dict', options=VOLUME_MOUNT_SPEC),
)


INIT_CONTAINER_SPEC = dict(
    name=dict(type='str', required=True),
    image=dict(type='str', required=True),
    command=dict(type='list', elements='str'),
    args=dict(type='list', elements='str'),
    env=dict(type='list', elements='dict', options=ENV_VAR_SPEC),
    resources=dict(type='dict', options=RESOURCES_SPEC),
    volume_mounts=dict(type='list', elements='dict', options=VOLUME_MOUNT_SPEC),
)


SCALE_SPEC = dict(
    min_replicas=dict(type='int'),
    max_replicas=dict(type='int'),
    cooldown_period=dict(type='int'),
    polling_interval=dict(type='int'),
    rules=dict(type='list', elements='dict'),
)


CONFIG_KEYS = ('secrets', 'active_revisions_mode', 'registries', 'ingress', 'dapr', 'max_inactive_revisions')
TEMPLATE_KEYS = ('revision_suffix', 'termination_grace_period_seconds', 'containers', 'init_containers', 'scale', 'volumes')


class AzureRMContainerApp(AzureRMModuleBaseExt):
    """Manage Azure Container Apps."""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            environment_id=dict(type='str'),
            workload_profile_name=dict(type='str'),
            identity=dict(type='dict', options=self.managed_identity_multiple_spec),
            active_revisions_mode=dict(type='str', choices=['Single', 'Multiple']),
            secrets=dict(type='list', elements='dict', options=SECRET_SPEC, no_log=False),
            registries=dict(type='list', elements='dict', options=REGISTRY_SPEC),
            ingress=dict(type='dict', options=INGRESS_SPEC),
            dapr=dict(type='dict', options=DAPR_SPEC),
            max_inactive_revisions=dict(type='int'),
            revision_suffix=dict(type='str'),
            termination_grace_period_seconds=dict(type='int'),
            containers=dict(type='list', elements='dict', options=CONTAINER_SPEC),
            init_containers=dict(type='list', elements='dict', options=INIT_CONTAINER_SPEC),
            scale=dict(type='dict', options=SCALE_SPEC),
            volumes=dict(type='list', elements='dict'),
            status=dict(type='str', choices=['start', 'stop']),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.tags = None
        self.state = None
        self.status = None
        self.identity = None

        self.parameters = dict()
        self.update_parameters = dict()

        self.results = dict(changed=False)
        self.to_do = Actions.NoAction

        self._managed_identity = None

        super(AzureRMContainerApp, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=True,
        )

    @property
    def managed_identity(self):
        if not self._managed_identity:
            self._managed_identity = {
                "identity": ManagedServiceIdentity,
                "user_assigned": UserAssignedIdentity,
            }
        return self._managed_identity

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self._assign(key, kwargs[key])

        resource_group = self.get_resource_group(self.resource_group)
        if self.location is None:
            self.location = resource_group.location
        self.parameters['location'] = self.location

        old_response = self.get_resource()

        identity_changed = False
        if self.identity is not None:
            curr_identity = old_response.get('identity') if old_response else None
            identity_changed, identity_body = self.update_managed_identity(
                curr_identity=curr_identity,
                new_identity=self.identity,
                patch_support=True,
            )
            if identity_body is not None:
                self.parameters['identity'] = identity_body
                self.update_parameters['identity'] = identity_body

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
                if identity_changed:
                    changed = True
                    self.to_do = Actions.Update

                update_tags, self.update_parameters['tags'] = self.update_tags(old_response.get('tags'))
                if update_tags:
                    changed = True
                    self.to_do = Actions.Update

                # Compare configuration + template payloads against the fetched state.
                # Strip write-only fields (secret values) so they never trigger a false diff.
                sanitized = _strip_write_only(self.parameters)
                for section in ('configuration', 'template'):
                    if section in sanitized and not self.default_compare(
                            {}, sanitized.get(section), old_response.get(section), '', dict(compare=[])):
                        changed = True
                        self.to_do = Actions.Update

                # environment id / workload profile are stored in parameters using their
                # ARM key names — compare against those directly.
                for arm_key in ('managed_environment_id', 'workload_profile_name'):
                    desired = self.parameters.get(arm_key)
                    if desired is not None and desired != old_response.get(arm_key):
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

        if self.status and self.state == 'present' and self.to_do != Actions.Delete:
            # Use the freshly-fetched state so start/stop is idempotent across create+status runs.
            current_state = self.results.get('state') or self.get_resource()
            performed = self.apply_status(current_state)
            if performed:
                changed = True
                if not self.check_mode:
                    self.results['state'] = self.get_resource() or self.results['state']

        self.results['changed'] = changed
        return self.results

    def _assign(self, key, value):
        if key in CONFIG_KEYS:
            self.parameters.setdefault('configuration', dict())[key] = value
            self.update_parameters.setdefault('configuration', dict())[key] = value
        elif key in TEMPLATE_KEYS:
            self.parameters.setdefault('template', dict())[key] = value
            self.update_parameters.setdefault('template', dict())[key] = value
        elif key in ('environment_id', 'workload_profile_name'):
            arm_key = 'managed_environment_id' if key == 'environment_id' else key
            self.parameters[arm_key] = value
            if key == 'workload_profile_name':
                self.update_parameters[arm_key] = value
        else:
            self.parameters[key] = value

    def create_update_resource(self):
        self.log("Creating / updating container app {0}".format(self.name))
        try:
            if self.to_do == Actions.Create:
                self.parameters['tags'] = self.tags
                envelope = _build_app_model(self.parameters)
                response = self.containerapps_client.container_apps.begin_create_or_update(
                    resource_group_name=self.resource_group,
                    container_app_name=self.name,
                    container_app_envelope=envelope,
                )
            else:
                envelope = _build_app_model(self.update_parameters)
                response = self.containerapps_client.container_apps.begin_update(
                    resource_group_name=self.resource_group,
                    container_app_name=self.name,
                    container_app_envelope=envelope,
                )
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error creating/updating container app {0}: {1}".format(self.name, str(exc)))
        return self.format_item(response)

    def delete_resource(self):
        self.log("Deleting container app {0}".format(self.name))
        try:
            response = self.containerapps_client.container_apps.begin_delete(
                resource_group_name=self.resource_group,
                container_app_name=self.name,
            )
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error deleting container app {0}: {1}".format(self.name, str(exc)))
        return True

    def get_resource(self):
        try:
            response = self.containerapps_client.container_apps.get(
                resource_group_name=self.resource_group,
                container_app_name=self.name,
            )
        except ResourceNotFoundError:
            return None
        except Exception as exc:
            self.fail("Error retrieving container app {0}: {1}".format(self.name, str(exc)))
        return self.format_item(response)

    def apply_status(self, current_state):
        """Run start/stop when the desired runtime state differs from the current one."""

        current_running_status = None
        if current_state:
            current_running_status = current_state.get('running_status')

        want_start = self.status == 'start'
        want_stop = self.status == 'stop'

        if want_start and current_running_status == 'Running':
            return False
        if want_stop and current_running_status == 'Stopped':
            return False

        if self.check_mode:
            return True

        try:
            if want_start:
                poller = self.containerapps_client.container_apps.begin_start(
                    resource_group_name=self.resource_group,
                    container_app_name=self.name,
                )
            else:
                poller = self.containerapps_client.container_apps.begin_stop(
                    resource_group_name=self.resource_group,
                    container_app_name=self.name,
                )
            if isinstance(poller, LROPoller):
                self.get_poller_result(poller)
        except Exception as exc:
            self.fail("Error applying status {0} to container app {1}: {2}".format(self.status, self.name, str(exc)))
        return True

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
    AzureRMContainerApp()


if __name__ == '__main__':
    main()
