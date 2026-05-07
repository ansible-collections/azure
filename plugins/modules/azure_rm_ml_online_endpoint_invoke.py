#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_online_endpoint_invoke
version_added: "3.18.0"
short_description: Invoke ML Online Endpoint resources
description:
    - Invoke ML Online Endpoint resources.
options:
    name:
        description:
            - Name of the Azure ML online endpoint.
        required: true
        type: str
    deployment_name:
        description:
            - Name of the Azure ML Online deployment to target.
        required: false
        type: str
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
    request_file:
        description:
            - Local path to the JSON file containing the request data.
        required: false
        type: str
    local:
        description:
            - Invoke all local endpoints.
        type: bool
        default: false

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Invoke ML Online Endpoint
  azure.azcollection.azure_rm_ml_online_endpoint_invoke:
    name: endpoint-command-ansible
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    request_file: ./targets/azure_rm_ml_online_deployment/files/sample-request.json
'''

RETURN = '''
changed:
    description:
        - Will return True if successfully invoked
    returned: always
    type: bool
    sample: true
ml_online_endpoint_invoke:
    description:
        - Online Endpoint Invoked that match the name and deployment.
    returned: always
    type: dict
    sample: [11055.977245525679, 4503.079536107787]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLOnlineEndpointInvoke(MLClientCommon):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True,
            ),
            deployment_name=dict(
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
            request_file=dict(
                type='str',
                required=False,
            ),
            local=dict(
                type='bool',
                default=False,
            ),
        )

        self._client = None
        self.ml_registry = None

        self.results = dict(
            changed=False,
            ml_online_endpoint_invoke=None
        )

        super(AzureRMMLOnlineEndpointInvoke, self).__init__(self.module_arg_spec,
                                                            supports_tags=False,
                                                            supports_check_mode=False,
                                                            facts_module=True,
                                                            )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        input_data_asset = None

        ml_online_endpoint_invoke = self.client.online_endpoints.invoke(
            endpoint_name=self.name,
            request_file=self.request_file,
            input_data=input_data_asset,
            deployment_name=self.deployment_name,
            local=self.local,
        )

        self.results['changed'] = True
        self.results['ml_online_endpoint_invoke'] = ml_online_endpoint_invoke
        return self.results


def main():
    AzureRMMLOnlineEndpointInvoke()


if __name__ == '__main__':
    main()
