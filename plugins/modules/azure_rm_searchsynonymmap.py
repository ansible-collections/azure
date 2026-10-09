#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_searchsynonymmap
version_added: "4.2.0"
short_description: Manage a synonym map in an Azure AI Search service
description:
    - Create, update, and delete a synonym map within an Azure AI Search service
      (data plane). A synonym map lets queries match equivalent terms; it is
      referenced from searchable index fields.
options:
    resource_group:
        description:
            - Name of the resource group containing the search service.
        required: true
        type: str
    search_service_name:
        description:
            - Name of the Azure AI Search service that hosts the synonym map.
        required: true
        type: str
    name:
        description:
            - Name of the synonym map.
        required: true
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
    synonyms:
        description:
            - The synonym rules, as a newline-separated string in Apache Solr
              format. Required when creating a synonym map.
            - 'Equivalent synonyms are comma-separated on one line (for example
              C(USA, United States, United States of America)); explicit mappings
              use C(=>) (for example C(Washington, Wash. => WA)).'
        type: str
    format:
        description:
            - The format of the synonym map. Azure AI Search currently supports
              only C(solr).
        type: str
        default: solr
        choices:
            - solr
    state:
        description:
            - Assert the state of the synonym map. Use C(present) to create/update, C(absent) to delete.
        type: str
        default: present
        choices:
            - present
            - absent
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create a synonym map
  azure.azcollection.azure_rm_searchsynonymmap:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: country-synonyms
    synonyms: |-
      USA, United States, United States of America
      UK, United Kingdom
    state: present

- name: Delete a synonym map
  azure.azcollection.azure_rm_searchsynonymmap:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: country-synonyms
    state: absent
'''

RETURN = '''
state:
    description:
        - The synonym map definition as returned by Azure AI Search.
    returned: when I(state=present)
    type: dict
    sample: {"name": "country-synonyms", "format": "solr", "synonyms": "USA, United States"}
'''

import copy

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_search_common import (
    AzureRMSearchDataPlaneMixin,
    ResourceNotFoundError,
)


class AzureRMSearchSynonymMap(AzureRMSearchDataPlaneMixin, AzureRMModuleBaseExt):

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            search_service_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            admin_key=dict(type='str', no_log=True),
            synonyms=dict(type='str'),
            format=dict(type='str', default='solr', choices=['solr']),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )
        self.resource_group = None
        self.search_service_name = None
        self.name = None
        self.admin_key = None
        self.synonyms = None
        self.format = None
        self.state = None
        self.results = dict(changed=False)
        super(AzureRMSearchSynonymMap, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self.client = self.get_search_index_client(
            self.search_service_name, admin_key=self.admin_key)

        existing = self._get_existing()

        if self.state == 'present':
            if self.synonyms is None and existing is None:
                self.fail(msg="synonyms is required to create synonym map '%s'; "
                              "it does not exist yet" % self.name)
            desired = self._build_body()
            if existing is None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.results['state'] = self._create_or_update(desired)
                else:
                    self.results['state'] = desired
            else:
                if not self._is_current(desired, existing):
                    # create_or_update is a full-replace PUT; merge the user-
                    # supplied keys onto the existing synonym map so unsupplied
                    # settings (synonyms, format) are preserved.
                    body = self._merge_existing(desired, existing)
                    self.results['changed'] = True
                    if not self.check_mode:
                        self.results['state'] = self._create_or_update(body)
                    else:
                        self.results['state'] = body
                else:
                    self.results['state'] = existing
        else:  # absent
            if existing is not None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.client.delete_synonym_map(self.name)
        return self.results

    def _get_existing(self):
        # The SDK raises ResourceNotFoundError when the synonym map does not
        # exist; translate to None. Otherwise return the wire shape (synonyms is
        # a newline-joined solr string).
        try:
            return self.client.get_synonym_map(self.name).as_dict()
        except ResourceNotFoundError:
            return None

    def _build_body(self):
        body = {"name": self.name, "format": self.format}
        if self.synonyms is not None:
            body["synonyms"] = self.synonyms
        return body

    def _merge_existing(self, desired, existing):
        # Overlay the user-supplied keys onto a copy of the existing synonym map
        # so a PUT update does not drop settings the user did not resupply.
        # Strip response-only @odata.* annotations. encryptionKey is not managed
        # by this module and its credentials are redacted on read, so never echo
        # it back.
        merged = {k: v for k, v in copy.deepcopy(existing).items()
                  if not k.startswith('@odata.') and k != 'encryptionKey'}
        merged.update(desired)
        return merged

    def _create_or_update(self, body):
        # create_or_update_synonym_map accepts a plain dict and returns the full
        # model; .as_dict() yields the wire shape.
        return self.client.create_or_update_synonym_map(body).as_dict()

    def _is_current(self, desired, existing):
        # Compare the desired body against the existing resource. default_compare
        # walks the union of keys, so server defaults present only in `existing`
        # (@odata.etag, encryptionKey) are ignored. Deep-copy desired so the
        # comparison cannot mutate the body we would PUT.
        result = dict(compare=[])
        return self.default_compare({}, copy.deepcopy(desired), existing, '', result)


def main():
    AzureRMSearchSynonymMap()


if __name__ == '__main__':
    main()
