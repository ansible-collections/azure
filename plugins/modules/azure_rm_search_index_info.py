#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_search_index_info
version_added: "4.2.0"
short_description: Get information about Azure AI Search indexes
description:
    - Get details of a single index, or list all indexes in an Azure AI Search service.
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
            - Name of a specific index to fetch. If omitted, all indexes are listed.
        type: str
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
- name: List all indexes
  azure.azcollection.azure_rm_search_index_info:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc

- name: Get one index
  azure.azcollection.azure_rm_search_index_info:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: rag-index
'''

RETURN = '''
indexes:
    description:
        - List of index definitions.
    returned: always
    type: list
    elements: dict
    sample: [{"name": "rag-index", "fields": [{"name": "id", "type": "Edm.String", "key": true}]}]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_search_common import AzureRMSearchDataPlaneMixin


class AzureRMSearchIndexInfo(AzureRMSearchDataPlaneMixin, AzureRMModuleBaseExt):

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            search_service_name=dict(type='str', required=True),
            name=dict(type='str'),
            admin_key=dict(type='str', no_log=True),
        )
        self.resource_group = None
        self.search_service_name = None
        self.name = None
        self.admin_key = None
        self.results = dict(changed=False, indexes=[])
        super(AzureRMSearchIndexInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])
        if self.name:
            result = self.search_query(
                self.search_service_name, "/indexes/{0}".format(self.name),
                "GET", admin_key=self.admin_key, expected_status_codes=[200])
            self.results['indexes'] = [result] if result else []
        else:
            result = self.search_query(
                self.search_service_name, "/indexes", "GET",
                admin_key=self.admin_key, expected_status_codes=[200])
            self.results['indexes'] = (result or {}).get('value', []) if result else []
        return self.results


def main():
    AzureRMSearchIndexInfo()


if __name__ == '__main__':
    main()
