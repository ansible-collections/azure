#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_compute_info
version_added: "3.15.0"
short_description: List ML Compute resources
description:
    - List ML Compute resources.
options:
    name:
        description:
            - Name of the Azure ML compute.
        type: str
        required: false
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
    type:
        description:
            - The type of compute target.
        choices:
            - amlcompute
            - computeinstance
        required: false
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: List ML Compute
  azure.azcollection.azure_rm_ml_compute_info:
    name: MyCompute
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List ML Compute
  azure.azcollection.azure_rm_ml_compute_info:
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    type: amlcompute
'''

RETURN = '''
ml_computes:
    description:
        - Compute that was just created or updated.
    returned: always
    type: dict
    sample: [
      {
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
        "tags": {"created_by": "Ansible"},
        "tier": "dedicated",
        "type": "amlcompute"
      },
      {
        "created_on": "2026-02-16T19:08:51.821821+0000",
        "description": "Compute Integration Tests",
        "enable_node_public_ip": true,
        "enable_os_patching": false,
        "enable_root_access": true,
        "enable_sso": true,
        "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-compute/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxx-xxx/computes/compxxxxxxx-xxxinst",
        "identity": {
          "principal_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "tenant_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "type": "system_assigned"
        },
        "last_operation": {
          "operation_name": "Stop",
          "operation_status": "Succeeded",
          "operation_time": "2026-02-16T19:12:01.237Z",
          "operation_trigger": "User"
        },
        "location": "eastus",
        "name": "compxxxxxxx-xxxinst",
        "network_settings": {
          "private_ip_address": "10.0.0.4",
          "public_ip_address": "xx.xxx.xxx.xxx"
        },
        "os_image_metadata": {
          "current_image_version": "26.01.05",
          "is_latest_os_image_version": true,
          "latest_image_version": "26.01.05"
        },
        "provisioning_state": "Succeeded",
        "release_quota_on_stop": false,
        "services": [
          {
            "display_name": "Jupyter",
            "endpoint_uri": "https://compxxxxxxx-xxxinst.eastus.instances.azureml.ms/tree/"
          },
          {
            "display_name": "Jupyter Lab",
            "endpoint_uri": "https://compxxxxxxx-xxxinst.eastus.instances.azureml.ms/lab"
          }
        ],
        "size": "Standard_DS3_v2",
        "ssh_public_access_enabled": false,
        "ssh_settings": {
          "admin_username": "azureuser",
          "ssh_key_value": "ssh-rsa AAAAB........PLp/ administrator@xxxxxx-xxxxxxx",
          "ssh_port": "50000"
        },
        "state": "Stopped",
        "tags": {
          "created_by": "Ansible"
        },
        "type": "computeinstance"
      }
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLComputeInfo(MLClientCommon):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
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
            type=dict(
                type='str',
                required=False,
                choices=['amlcompute', 'computeinstance'],
            ),
        )

        self._client = None
        self.ml_compute = None
        self.ml_registry = None

        self.results = dict(
            ml_computes=[]
        )

        super(AzureRMMLComputeInfo, self).__init__(self.module_arg_spec,
                                                   supports_tags=False,
                                                   supports_check_mode=True,
                                                   facts_module=True,
                                                   )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            try:
                result = self.client.compute.get(self.name)
                ml_computes = [self.entity_to_dict(result)]
            except ResourceNotFoundError:
                ml_computes = []
        else:
            results = self.client.compute.list(compute_type=self.type)
            ml_computes = [self.entity_to_dict(x) for x in results]

        self.results['ml_computes'] = ml_computes
        return self.results


def main():
    AzureRMMLComputeInfo()


if __name__ == '__main__':
    main()
