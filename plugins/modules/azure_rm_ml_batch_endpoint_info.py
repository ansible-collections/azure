#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_batch_endpoint_info
version_added: "3.18.0"
short_description: List ML Batch Endpoint resources
description:
    - List ML Batch Endpoint resources.
options:
    name:
        description:
            - Name of the Azure ML batch endpoint.
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

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get Specific ML Batch Endpoint by name
  azure.azcollection.azure_rm_ml_batch_endpoint_info:
    name: endpoint-command-xxxxxxxxxx
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List ML Batch Endpoints
  azure.azcollection.azure_rm_ml_batch_endpoint_info:
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
'''

RETURN = '''
ml_batch_endpoints:
    description:
        - Batch Endpoints that match the query.
    returned: always
    type: dict
    sample: [
      {
      }
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLBatchEndpointInfo(MLClientCommon):
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
        )

        self._client = None
        self.ml_registry = None

        self.results = dict(
            ml_batch_endpoints=[]
        )

        super(AzureRMMLBatchEndpointInfo, self).__init__(self.module_arg_spec,
                                                         supports_tags=False,
                                                         supports_check_mode=True,
                                                         facts_module=True,
                                                         )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            ml_batch_endpoints = [self.get(self.name)]
        else:
            results = self.client.batch_endpoints.list()
            ml_batch_endpoints = [self.get(x.name) for x in results]

        self.results['ml_batch_endpoints'] = ml_batch_endpoints
        return self.results

    def get(self, name):
        try:
            result = self.client.batch_endpoints.get(name=name)
            ml_batch_endpoint = self.entity_to_dict(result)
            jobs = self.client.batch_endpoints.list_jobs(endpoint_name=name)
            ml_batch_endpoint['jobs'] = jobs
        except ResourceNotFoundError:
            ml_batch_endpoint = None

        return ml_batch_endpoint


def main():
    AzureRMMLBatchEndpointInfo()


if __name__ == '__main__':
    main()
