#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_workspace
version_added: "3.15.0"
short_description: Create, Update or Delete an Azure Machine Learning Workspace
description:
    - Create, Update or Delete an Azure Machine Learning Workspace.
options:
    name:
        description:
            - Name of the Azure ML workspace.
        type: str
        required: true
    display_name:
        description:
            - Display name for the workspace.
        type: str
        required: false
    description:
        description:
            - Description of the Azure ML workspace.
        type: str
        required: false
    resource_definition:
        description:
            - Workspace definition in YAML
        type: str
        required: false
    kind:
        description:
            - Specifies the workspace as a specific kind.
        type: str
        choices:
            - hub
            - project
        required: false
    update_dependent_resources:
        description:
            - Specifying update_dependent_resources, gives your
              consent to update the workspace dependent
              resources. Updating the workspace-attached Azure
              Container Registry or Application Insights resource
              may break lineage of previous jobs, deployed
              inference endpoints, or your ability to rerun
              earlier jobs in this workspace.
        type: bool
        default: false
    public_network_access:
        description:
            - Allow public endpoint connectivity when a workspace
              is private link enabled.
        type: str
        choices:
            - Disabled
            - Enabled
        default: Disabled
    image_build_compute:
        description:
            - The name of the compute target to use for building
              environment Docker images when the container
              registry is behind a VNet.
        type: str
        required: false
    storage_account:
        description:
            - ARM id of the storage account associated with this workspace.
        type: str
        required: false
    key_vault:
        description:
            - ARM id of the key vault associated with this workspace.
        type: str
        required: false
    application_insights:
        description:
            - ARM id of the application insights associated with
              this workspace.
        type: str
        required: false
    container_registry:
        description:
            - ARM id of the container registry associated with
              this workspace.
        type: str
        required: false
    hub_id:
        description:
            - Only applies to O(kind=Project). An ARM ID which defines the
              parent hub of this project.
        type: str
        required: false
    enable_data_isolation:
        description:
            - A flag to determine if a workspace has data
              isolation enabled. The flag can only be set at the
              creation stage, it can't be updated.
        type: bool
        default: false
    primary_user_assigned_identity:
        description:
            - ARM identifier of primary user assigned managed
              identity, in case multiple ones are specified. Also
              the default managed identity for clusterless compute.
        type: str
        required: false
    managed_network:
        description:
            - Managed Network Isolation Mode for the workspace.
        type: str
        choices:
            - disabled
            - allow_internet_outbound
            - allow_only_approved_outbound
        required: false
    network_acls:
        description:
            - List of inbound IP rules
        required: false
        type: list
        elements: str
    provision_network_now:
        description:
            - Set to trigger the provisioning of the
              managed network when creating a worksapce with the
              manged network enabled, or else it does nothing.
        type: bool
        default: false
    system_datastores_auth_mode:
        description:
            - Specifies the auth mode for the system data stores.
        type: str
        choices:
            - accesskey
            - identity
    allow_roleassignment_on_rg:
        description:
            - A flag to determine if a workspace could
              have role assignments on resource group level.
        type: bool
        default: true
    location:
        description:
            - The location to be used for the new workspace.
        type: str
        required: false
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    default_resource_group:
        description:
            - Only applies to O(kind=hub). If set, then child projects of this
              hub will have their resource group set this by default.
        required: false
        type: str
    all_resources:
        description:
            - Only applies to O(state=absent). Delete all the dependent resources
              associated with the workspace (Azure Storage account,
              Azure Container Registry, Azure Application Insights, Azure Key Vault).
        type: bool
        default: false
    permanently_delete:
        description:
            - Only applies to O(state=absent). Workspaces are soft-deleted
              state by default to allow recovery of workspace data. Set this flag
              to override the soft-delete behavior and permanently delete your
              workspace.
        type: bool
        default: false
    state:
        description:
            - State of the Workspace. Use C(present) to create
              or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create ML Workspace
  azure.azcollection.azure_rm_ml_workspace:
    location: eastus
    name: MyWorkspace
    description: My Workspace created by Ansible
    resource_group: myResourceGroup
    resource_definition: |
      managed_network:
        isolation_mode: allow_only_approved_outbound
        outbound_rules:
        - name: microsoft
          destination: 'microsoft.com'
          type: fqdn
        - name: servicetag-w-prefixes
          destination:
            port_ranges: 80, 8080-8089
            protocol: TCP
            service_tag: sometag
            address_prefixes: ["168.63.129.16","10.0.0.0/24"]
          type: service_tag
    tags:
      createdByToolkit: Ansible
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
ml_workspace:
    description:
        - Workspace that was just created or updated.
    returned: always
    type: dict
    sample: {
        "allow_roleassignment_on_rg": false,
        "application_insights": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.insights/components/workspacinsightsxxxxxxxx",
        "description": "Workspace Integration Tests",
        "discovery_url": "https://westus3.api.azureml.ms/discovery",
        "display_name": "workspace-xxxxxxx-xxx",
        "enable_data_isolation": false,
        "hbi_workspace": false,
        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxx-xxx",
        "identity": {
            "principal_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "tenant_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "type": "system_assigned"
        },
        "key_vault": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.Keyvault/vaults/workspackeyvaultxxxxxxxx",
        "location": "westus3",
        "managed_network": {
            "firewall_sku": "standard",
            "isolation_mode": "allow_only_approved_outbound",
            "network_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "outbound_rules": [
                {
                    "category": "user_defined",
                    "destination": "microsoft.com",
                    "name": "microsoft",
                    "status": "Inactive",
                    "type": "fqdn"
                },
                {
                    "category": "user_defined",
                    "destination": {
                        "address_prefixes": [
                            "168.63.129.16",
                            "10.0.0.0/24"
                        ],
                        "port_ranges": "80, 8080-8089",
                        "protocol": "TCP",
                        "service_tag": "sometag"
                    },
                    "name": "servicetag-w-prefixes",
                    "status": "Inactive",
                    "type": "service_tag"
                 }
            ],
            "status": {
                "spark_ready": false,
                "status": "Inactive"
            }
        },
        "mlflow_tracking_uri": "azureml://westus3.api.azureml.ms/mlflow/v1.0/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxx-xxx",
        "name": "workspace-xxxxxxx-xxx",
        "network_acls": {
            "default_action": "Allow",
            "ip_rules": []
        },
        "provision_network_now": false,
        "public_network_access": "Disabled",
        "resource_group": "test-ml-workspace",
        "serverless_compute": {"no_public_ip": false},
        "storage_account": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/test-ml-workspace/providers/Microsoft.Storage/storageAccounts/workspacstoragexxxxxxxxx",
        "system_datastores_auth_mode": "accesskey",
        "tags": {
            "createdByToolkit": "sdk-v2-1.31.0",
            "foo": "bar"
        }
    }
'''  # NOQA


try:
    import io
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_workspace
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLWorkspace(MLClientCommon):

    PARAM_OVERRIDES = ['name',
                       'display_name',
                       'description',
                       'tags',
                       'location',
                       'image_build_compute',
                       'public_network_access',
                       'storage_account',
                       'key_vault',
                       'application_insights',
                       'container_registry',
                       'primary_user_assigned_identity',
                       'provision_network_now',
                       'enable_data_isolation',
                       'hub_id',
                       'default_resource_group',
                       'kind',
                       'system_datastores_auth_mode',
                       'allow_roleassignment_on_rg',
                       ]

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True
            ),
            display_name=dict(
                type='str',
                required=False,
            ),
            description=dict(
                type='str',
                required=False,
            ),
            resource_definition=dict(
                type='str',
                required=False,
            ),
            kind=dict(
                type='str',
                choices=['hub',
                         'project'],
                required=False,
            ),
            update_dependent_resources=dict(
                type='bool',
                default=False,
            ),
            public_network_access=dict(
                type='str',
                choices=['Disabled', 'Enabled'],
                default='Disabled',
            ),
            image_build_compute=dict(
                type='str',
                required=False,
            ),
            storage_account=dict(
                type='str',
                required=False,
            ),
            key_vault=dict(
                type='str',
                required=False,
                no_log=False,
            ),
            application_insights=dict(
                type='str',
                required=False,
            ),
            container_registry=dict(
                type='str',
                required=False,
            ),
            hub_id=dict(
                type='str',
                required=False,
            ),
            enable_data_isolation=dict(
                type='bool',
                default=False,
            ),
            primary_user_assigned_identity=dict(
                type='str',
                required=False,
            ),
            managed_network=dict(
                type='str',
                choices=['disabled',
                         'allow_internet_outbound',
                         'allow_only_approved_outbound'],
                required=False,
            ),
            network_acls=dict(
                type='list',
                required=False,
                elements='str',
            ),
            provision_network_now=dict(
                type='bool',
                default=False,
            ),
            system_datastores_auth_mode=dict(
                type='str',
                choices=['accesskey',
                         'identity'],
                required=False,
            ),
            allow_roleassignment_on_rg=dict(
                type='bool',
                default=True,
            ),
            location=dict(
                type='str',
                required=False
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            default_resource_group=dict(
                type='str',
                required=False
            ),
            all_resources=dict(
                type='bool',
                default=False
            ),
            permanently_delete=dict(
                type='bool',
                default=False
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
        )

        self._client = None
        self.ml_workspace = None
        self.ml_registry = None
        self.state = None

        self.results = dict(
            changed=False,
            compare=[],
            ml_workspace={}
        )

        super(AzureRMMLWorkspace, self).__init__(self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 )

    def exec_module(self, **kwargs):

        params_override = []
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])
            if kwargs[key] is not None and key in self.PARAM_OVERRIDES:
                params_override.append({key: kwargs[key]})

        if self.resource_definition:
            resource_definition = io.StringIO(self.resource_definition)
        else:
            resource_definition = None

        # Process managed_network specially
        if self.managed_network:
            params_override.append({"managed_network": {"isolation_mode": self.managed_network}})

        # Process network_acls specially
        if self.network_acls:
            network_acls = {
                "default_action": "Deny",
                "ip_rules": [{"value": ip} for ip in self.network_acls]
            }
        else:
            network_acls = {
                "default_action": "Allow",
                "ip_rules": []
            }
        params_override.append({'network_acls': network_acls})

        changed = False
        # Generate ml_workspace based on ansible args passed in.
        ml_workspace = load_workspace(resource_definition,
                                      params_override=params_override)
        try:
            # Attempt to retrieve ml_workspace based on name
            ml_workspace_info = self.client.workspaces.get(self.name)
        except ResourceNotFoundError:
            ml_workspace_info = None

        if self.state == 'present':
            if ml_workspace_info:
                # Update
                ml_workspace_info = self.entity_to_dict(ml_workspace_info)
                ml_workspace_info = self.filter_required(ml_workspace_info)
                changed = not self.default_compare({},
                                                   self.filter_required(
                                                       self.entity_to_dict(ml_workspace)),
                                                   ml_workspace_info,
                                                   '',
                                                   self.results)
                if changed and not self.check_mode:
                    response = self.client.workspaces.begin_update(ml_workspace,
                                                                   update_dependent_resources=self.update_dependent_resources
                                                                   )
                    ml_workspace_object = self.get_poller_result(response)
                    ml_workspace_info = self.entity_to_dict(ml_workspace_object)

            else:
                # Create
                changed = True
                if not self.check_mode:
                    response = self.client.workspaces.begin_create(
                        workspace=ml_workspace,
                        update_dependent_resources=self.update_dependent_resources)
                    ml_workspace_object = self.get_poller_result(response)
                    ml_workspace_info = self.entity_to_dict(ml_workspace_object)
        else:
            # Delete
            if ml_workspace_info:
                changed = True
                if not self.check_mode:
                    response = self.client.workspaces.begin_delete(
                        name=self.name,
                        delete_dependent_resources=self.all_resources,
                        permanently_delete=self.permanently_delete)
                    ml_workspace_info = self.get_poller_result(response)

        self.results['ml_workspace'] = ml_workspace_info
        self.results['changed'] = changed
        return self.results


def main():
    AzureRMMLWorkspace()


if __name__ == '__main__':
    main()
