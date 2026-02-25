#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_compute
version_added: "3.15.0"
short_description: Create, Update or Delete an Azure Machine Learning Compute
description:
    - Create, Update or Delete an Azure Machine Learning Compute.
options:
    name:
        description:
            - Name of the Azure ML compute.
        type: str
        required: true
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    ml_workspace:
        description:
            - Name of the Azure ML workspace.
        required: true
        type: str
    description:
        description:
            - Description of the compute target.
        type: str
        required: false
    resource_definition:
        description:
            - Compute definition in YAML
        type: str
        required: false
    identity_type:
        description:
            - The type of managed identity.
        type: str
        choices:
            - SystemAssigned
            - UserAssigned
        required: false
    size:
        description:
            - "VM size to use for the compute target. More details can be
              found here: https://aka.ms/azureml-vm-details."
        type: str
        required: false
    ssh_key_value:
        description:
            - SSH public key of the administrator user account.
        type: str
        required: false
    ssh_public_access_enabled:
        description:
            - Indicates whether public SSH port is enabled.
        type: bool
        required: false
    subnet:
        description:
            - Name of the subnet. Can also reference a subnet in an
              existing vnet by ID instead of name. If subnet ID is
              specified then vnet_name will be ignored. Subnet ID can refer
              to a vnet/subnet in another RG by specifying the fully
              qualified subnet ID. Required when vnet name is specified.
        type: str
        required: false
    type:
        description:
            - The type of compute target.
        choices:
            - amlcompute
            - computeinstance
        type: str
        required: false
    user_assigned_identities:
        description:
            - User Assigned Identities.
        type: list
        elements: str
    vnet_name:
        description:
            - Name of the virtual network.
        type: str
        required: false
    admin_username:
        description:
            - Name of the administrator user account that can be used to
              SSH into the node(s).
        type: str
        required: false
    admin_password:
        description:
            - Password for the administrator user account.
        type: str
        required: false
    idle_time_before_scale_down:
        description:
            - Node idle time in seconds before scaling down the cluster.
        type: int
        required: false
    location:
        description:
            - The location to be used for the new compute.
              If not specified, defaults to the location of the workspace.
        type: str
        required: false
    max_instances:
        description:
            - The maximum number of nodes to use on the cluster.
        required: false
        type: int
    min_instances:
        description:
            - The minimum number of nodes to use on the cluster.
        required: false
        type: int
    tier:
        description:
            - VM priority tier.
        choices:
            - dedicated
            - low_priority
        type: str
    user_object_id:
        description:
            - AAD object ID of the assigned user.
        type: str
        required: false
    user_tenant_id:
        description:
            - AAD tenant ID of the assigned user.
        type: str
        required: false
    state:
        description:
            - State of the Compute. Use C(present) to create
              or update and C(absent) to delete. C(start) to
              start, C(stop) to stop and C(restart) to restart.
        default: present
        type: str
        choices:
            - absent
            - present
            - start
            - stop
            - restart

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create ML Compute
  azure.azcollection.azure_rm_ml_compute:
    location: eastus
    name: MyCompute
    description: My Compute created by Ansible
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    type: amlcompute
    min_instances: 0
    max_instances: 8
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
ml_compute:
    description:
        - Compute that was just created or updated.
    returned: always
    type: dict
    sample: {
      "description": "Compute Integration Tests",
      "enable_node_public_ip": true,
      "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-compute/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxx-xxx/computes/amlxxxxxxx-xxxcomp",
      "idle_time_before_scale_down": 120,
      "location": "eastus",
      "max_instances": 200,
      "min_instances": 0,
      "name": "amlxxxxxxx-xxxcomp",
      "network_settings": {},
      "provisioning_state": "Succeeded",
      "size": "STANDARD_DS3_V2",
      "ssh_public_access_enabled": true,
      "tags": {
        "created_by": "Ansible"
      },
      "tier": "dedicated",
      "type": "amlcompute"
    }
'''  # NOQA


try:
    import io
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_compute
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLCompute(MLClientCommon):

    UPDATE_OVERRIDES = ['min_instances',
                        'max_instances',
                        'idle_time_before_scale_down',
                        'identity_type',
                        'user_assigned_identities',
                        'tags'
                        ]

    PARAM_OVERRIDES = UPDATE_OVERRIDES + ['name',
                                          'type',
                                          'vnet_name',
                                          'subnet',
                                          'admin_username',
                                          'admin_password',
                                          'ssh_key_value',
                                          'size',
                                          'user_tenant_id',
                                          'user_object_id',
                                          'description',
                                          'enable_node_public_ip',
                                          'tier',
                                          'ssh_public_access_enabled',
                                          'location',
                                          ]

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True,
            ),
            description=dict(
                type='str',
                required=False,
            ),
            resource_definition=dict(
                type='str',
                required=False,
            ),
            location=dict(
                type='str',
                required=False,
            ),
            resource_group=dict(
                type='str',
                required=True,
            ),
            ml_workspace=dict(
                type='str',
                required=True,
            ),
            identity_type=dict(
                type='str',
                required=False,
                choices=['SystemAssigned', 'UserAssigned'],
            ),
            size=dict(
                type='str',
                required=False,
            ),
            ssh_key_value=dict(
                type='str',
                required=False,
                no_log=True,
            ),
            ssh_public_access_enabled=dict(
                type='bool',
                required=False,
            ),
            subnet=dict(
                type='str',
                required=False,
            ),
            type=dict(
                choices=['amlcompute', 'computeinstance'],
                type='str',
                required=False,
            ),
            user_assigned_identities=dict(
                type='list',
                elements='str',
                required=False,
            ),
            vnet_name=dict(
                type='str',
                required=False,
            ),
            admin_username=dict(
                type='str',
                required=False,
            ),
            admin_password=dict(
                type='str',
                required=False,
                no_log=True,
            ),
            idle_time_before_scale_down=dict(
                type='int',
                required=False,
            ),
            max_instances=dict(
                type='int',
                required=False,
            ),
            min_instances=dict(
                type='int',
                required=False,
            ),
            tier=dict(
                choices=['dedicated', 'low_priority'],
                type='str',
                required=False,
            ),
            user_object_id=dict(
                type='str',
                required=False,
            ),
            user_tenant_id=dict(
                type='str',
                required=False,
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent', 'start', 'stop', 'restart'],
            ),
        )

        self._client = None
        self.ml_compute = None
        self.ml_registry = None
        self.state = None

        self.results = dict(
            changed=False,
            compare=[],
            ml_compute={}
        )

        super(AzureRMMLCompute, self).__init__(self.module_arg_spec,
                                               supports_check_mode=True,
                                               )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        if self.resource_definition:
            resource_definition = io.StringIO(self.resource_definition)
        else:
            resource_definition = None

        changed = False
        ml_compute_info = self.get(self.name)

        if self.state == 'present':
            if ml_compute_info:
                # Update
                params_override = self.update_params(kwargs,
                                                     self.UPDATE_OVERRIDES,
                                                     ml_compute_info)

                # Generate ml_compute based on ansible args passed in.
                ml_compute = load_compute(None,
                                          params_override=params_override)
                ml_compute_info = self.entity_to_dict(ml_compute_info)
                changed = not self.default_compare({},
                                                   self.entity_to_dict(ml_compute),
                                                   ml_compute_info,
                                                   '',
                                                   self.results)
                if changed and not self.check_mode:
                    response = self.client.compute.begin_update(ml_compute)
                    ml_compute_object = self.get_poller_result(response)
                    ml_compute_info = self.entity_to_dict(ml_compute_object)

            else:
                # Create
                params_override = self.update_params(kwargs, self.PARAM_OVERRIDES)

                # Generate ml_compute based on ansible args passed in.
                ml_compute = load_compute(resource_definition,
                                          params_override=params_override)
                changed = True
                if not self.check_mode:
                    response = self.client.begin_create_or_update(ml_compute)
                    ml_compute_object = self.get_poller_result(response)
                    ml_compute_info = self.entity_to_dict(ml_compute_object)
        elif self.state == 'absent':
            # Delete
            if ml_compute_info:
                changed = True
                if not self.check_mode:
                    response = self.client.compute.begin_delete(name=self.name)
                    result = self.get_poller_result(response)
                ml_compute_info = self.get(self.name, as_dict=True)
        elif self.state == 'start':
            # Start
            if hasattr(ml_compute_info, 'state'):
                if ml_compute_info.state != "Running":
                    changed = True
                    if not self.check_mode:
                        self.start(self.name)
                ml_compute_info = self.get(self.name, as_dict=True)
            else:
                self.fail("Compute instance doesn't exist")
        elif self.state == 'stop':
            # Stop
            if hasattr(ml_compute_info, 'state'):
                if ml_compute_info.state != "Stopped":
                    changed = True
                    if not self.check_mode:
                        self.stop(self.name)
                ml_compute_info = self.get(self.name, as_dict=True)
            else:
                self.fail("Compute instance doesn't exist")
        elif self.state == 'restart':
            # Restart
            if hasattr(ml_compute_info, 'state'):
                changed = True
                if not self.check_mode:
                    self.restart(self.name)
                ml_compute_info = self.get(self.name, as_dict=True)
            else:
                self.fail("Compute instance doesn't exist")

        self.results['ml_compute'] = ml_compute_info
        self.results['changed'] = changed
        return self.results

    def update_params(self, kwargs, param_overrides, ml_compute=None):
        params_override = []

        # If ml_compute is defined use those values as a base.
        # Update can't change some of these values but we need
        # to keep the same values as before the update.
        if ml_compute:
            items = self.entity_to_dict(ml_compute).items()
            params_override = [{k: v} for k, v in items if k != "ssh_settings"]

        # Update values based on what param_overrides says we can update.
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if kwargs[key] is not None and key in param_overrides:
                if key == 'vnet_name':
                    params_override.append({"network_settings.vnet_name":
                                            kwargs[key]})
                elif key == 'subnet':
                    params_override.append({"network_settings.subnet":
                                            kwargs[key]})
                elif key == 'admin_username':
                    params_override.append({"ssh_settings.admin_username":
                                            kwargs[key]})
                elif key == 'admin_password':
                    params_override.append({"ssh_settings.admin_password":
                                            kwargs[key]})
                elif key == 'ssh_key_value':
                    params_override.append({"ssh_settings.ssh_key_value":
                                            kwargs[key]})
                elif key == 'user_tenant_id':
                    params_override.append({"create_on_behalf_of.user_tenant_id":
                                            kwargs[key]})
                elif key == 'user_object_id':
                    params_override.append({"create_on_behalf_of.user_object_id":
                                            kwargs[key]})
                elif key == 'identity_type':
                    params_override.append({"identity.type": kwargs[key]})
                elif key == 'user_assigned_identities':
                    identities = self._process_user_assigned_identities(kwargs[key])
                    params_override.append({"identity.user_assigned_identities": identities})
                else:
                    params_override.append({key: kwargs[key]})
        return params_override

    # Convert list to a list of dictionaries
    def _process_user_assigned_identities(self, resource_ids):
        return [{"resource_id": resource_id} for resource_id in resource_ids]

    def get(self, name, as_dict=False):
        try:
            # Attempt to retrieve ml_compute based on name
            ml_compute_info = self.client.compute.get(name)
            if as_dict:
                ml_compute_info = self.entity_to_dict(ml_compute_info)
        except ResourceNotFoundError:
            ml_compute_info = None
        return ml_compute_info

    def start(self, name):
        try:
            response = self.client.compute.begin_start(name=name)
            result = self.get_poller_result(response)
            return result
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error start the compute instance: {0}".format(str(e)))

    def stop(self, name):
        try:
            response = self.client.compute.begin_stop(name=name)
            result = self.get_poller_result(response)
            return result
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error stop the compute instance: {0}".format(str(e)))

    def restart(self, name):
        try:
            response = self.client.compute.begin_restart(name=name)
            result = self.get_poller_result(response)
            return result
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error restart the compute instance: {0}".format(str(e)))


def main():
    AzureRMMLCompute()


if __name__ == '__main__':
    main()
