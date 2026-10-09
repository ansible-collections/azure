#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_searchindexer_info
version_added: "4.2.0"
short_description: Get information about Azure AI Search indexers
description:
    - Get details of a single indexer, or list all indexers in an Azure AI Search service.
options:
    resource_group:
        description:
            - Name of the resource group containing the search service.
        required: true
        type: str
    search_service_name:
        description:
            - Name of the Azure AI Search service.
        required: true
        type: str
    name:
        description:
            - Name of a specific indexer to fetch. If omitted, all indexers are listed.
        type: str
    include_status:
        description:
            - When C(true) and I(name) is set, also return the indexer's execution
              status (last run result and execution history) in the C(status) key.
        type: bool
        default: false
    admin_key:
        description:
            - Admin API key for the search service, used to authenticate data-plane
              requests via the C(api-key) header.
            - This is supplementary to the standard Azure credentials. The module
              always requires standard Azure authentication parameters and a
              subscription ID (see the I(azure.azcollection.azure) documentation
              fragment) to run, regardless of whether this is set.
            - If omitted, data-plane requests are authenticated with an RBAC bearer
              token (managed identity / service principal) using the data-plane
              scope C(https://search.azure.com/.default).
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: List all indexers
  azure.azcollection.azure_rm_searchindexer_info:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc

- name: Get one indexer
  azure.azcollection.azure_rm_searchindexer_info:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: blob-indexer
'''

RETURN = '''
indexers:
    description:
        - List of indexer definitions.
    returned: always
    type: list
    elements: dict
    sample: [{"name": "blob-indexer", "targetIndexName": "knowledge-index", "dataSourceName": "blob-datasource"}]
status:
    description:
        - The indexer's execution status, when I(name) is set and I(include_status=true).
    returned: when I(include_status=true) and the indexer exists
    type: dict
    sample: {"status": "running", "lastResult": {"status": "success"}}
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_search_common import (
    AzureRMSearchDataPlaneMixin,
    ResourceNotFoundError,
)


class AzureRMSearchIndexerInfo(AzureRMSearchDataPlaneMixin, AzureRMModuleBaseExt):

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            search_service_name=dict(type='str', required=True),
            name=dict(type='str'),
            include_status=dict(type='bool', default=False),
            admin_key=dict(type='str', no_log=True),
        )
        self.resource_group = None
        self.search_service_name = None
        self.name = None
        self.include_status = False
        self.admin_key = None
        self.results = dict(changed=False, indexers=[])
        super(AzureRMSearchIndexerInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])
        client = self.get_search_indexer_client(
            self.search_service_name, admin_key=self.admin_key)
        if self.name:
            try:
                ix = client.get_indexer(self.name)
                self.results['indexers'] = [ix.as_dict()]
                if self.include_status:
                    self.results['status'] = client.get_indexer_status(self.name).as_dict()
            except ResourceNotFoundError:
                self.results['indexers'] = []
        else:
            self.results['indexers'] = [ix.as_dict() for ix in client.get_indexers()]
        return self.results


def main():
    AzureRMSearchIndexerInfo()


if __name__ == '__main__':
    main()
