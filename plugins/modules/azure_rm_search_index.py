#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_search_index
version_added: "4.2.0"
short_description: Manage an index in an Azure AI Search service
description:
    - Create, update, and delete an index within an Azure AI Search service (data plane).
options:
    resource_group:
        description:
            - Name of the resource group containing the search service.
        required: true
        type: str
    search_service_name:
        description:
            - Name of the Azure AI Search service that hosts the index.
        required: true
        type: str
    name:
        description:
            - Name of the search index.
        required: true
        type: str
    admin_key:
        description:
            - Admin API key for the search service.
            - If omitted, RBAC authentication (managed identity / service principal) is used
              with the data-plane scope C(https://search.azure.com/.default).
        type: str
    fields:
        description:
            - The field definitions of the index. Required when I(state=present).
        type: list
        elements: dict
        suboptions:
            name:
                description: Field name.
                type: str
                required: true
            type:
                description:
                    - Field data type, e.g. C(Edm.String), C(Edm.Int32), C(Collection(Edm.String)),
                      or C(Collection(Edm.Single)) for vectors.
                type: str
                required: true
            key:
                description: Whether this field is the document key. Exactly one field must be the key.
                type: bool
            searchable:
                description: Whether the field is full-text searchable.
                type: bool
            filterable:
                description: Whether the field can be used in $filter expressions.
                type: bool
            retrievable:
                description: Whether the field can be returned in results.
                type: bool
            sortable:
                description: Whether the field can be used in $orderby.
                type: bool
            facetable:
                description: Whether the field can be used in faceting.
                type: bool
            analyzer:
                description: Name of the analyzer for the field.
                type: str
            dimensions:
                description: Dimensionality of a vector field (e.g. 1536).
                type: int
            vector_search_profile:
                description: Name of the vector search profile bound to a vector field.
                type: str
    vector_search:
        description:
            - Vector search configuration (algorithms, profiles, vectorizers).
            - Passed through to the REST API; see the Azure AI Search REST reference for structure.
        type: dict
    semantic:
        description:
            - Semantic ranking configuration (configurations, prioritized fields).
        type: dict
    scoring_profiles:
        description:
            - List of scoring profiles for relevance tuning.
        type: list
        elements: dict
    default_scoring_profile:
        description:
            - Name of the scoring profile applied when none is specified at query time.
        type: str
    suggesters:
        description:
            - List of suggesters for autocomplete/suggestions.
        type: list
        elements: dict
    analyzers:
        description:
            - Custom analyzer definitions.
        type: list
        elements: dict
    cors_options:
        description:
            - Cross-origin resource sharing options for the index.
        type: dict
    state:
        description:
            - Assert the state of the index. Use C(present) to create/update, C(absent) to delete.
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
- name: Create a vector-enabled RAG index
  azure.azcollection.azure_rm_search_index:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: rag-index
    fields:
      - name: id
        type: Edm.String
        key: true
        filterable: true
      - name: content
        type: Edm.String
        searchable: true
      - name: contentVector
        type: Collection(Edm.Single)
        dimensions: 1536
        vector_search_profile: my-vector-profile
    vector_search:
      algorithms:
        - name: my-hnsw
          kind: hnsw
      profiles:
        - name: my-vector-profile
          algorithm: my-hnsw
    state: present

- name: Delete an index
  azure.azcollection.azure_rm_search_index:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: rag-index
    state: absent
'''

RETURN = '''
state:
    description:
        - The index definition as returned by Azure AI Search.
    returned: when I(state=present)
    type: dict
    sample: {"name": "rag-index", "fields": [{"name": "id", "type": "Edm.String", "key": true}]}
'''

import copy

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_search_common import AzureRMSearchDataPlaneMixin


class AzureRMSearchIndex(AzureRMSearchDataPlaneMixin, AzureRMModuleBaseExt):

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            search_service_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            admin_key=dict(type='str', no_log=True),
            fields=dict(type='list', elements='dict'),
            vector_search=dict(type='dict'),
            semantic=dict(type='dict'),
            scoring_profiles=dict(type='list', elements='dict'),
            default_scoring_profile=dict(type='str'),
            suggesters=dict(type='list', elements='dict'),
            analyzers=dict(type='list', elements='dict'),
            cors_options=dict(type='dict'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )
        self.resource_group = None
        self.search_service_name = None
        self.name = None
        self.admin_key = None
        self.state = None
        self.results = dict(changed=False)
        super(AzureRMSearchIndex, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        existing = self.search_query(
            self.search_service_name, "/indexes/{0}".format(self.name),
            "GET", admin_key=self.admin_key, expected_status_codes=[200])

        if self.state == 'present':
            if self.fields is None and existing is None:
                self.fail_json(msg="fields is required to create an index")
            desired = self._build_body()
            if existing is None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.results['state'] = self._create_or_update(desired)
                else:
                    self.results['state'] = desired
            else:
                if not self._is_current(desired, existing):
                    self.results['changed'] = True
                    if not self.check_mode:
                        self.results['state'] = self._create_or_update(desired)
                    else:
                        self.results['state'] = desired
                else:
                    self.results['state'] = existing
        else:  # absent
            if existing is not None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.search_query(
                        self.search_service_name, "/indexes/{0}".format(self.name),
                        "DELETE", admin_key=self.admin_key,
                        expected_status_codes=[204, 200])
        return self.results

    def _build_body(self):
        body = {"name": self.name}
        if self.fields is not None:
            body["fields"] = [self._map_field(f) for f in self.fields]
        # pass-through blocks map verbatim (REST uses camelCase keys already)
        if self.vector_search is not None:
            body["vectorSearch"] = self.vector_search
        if self.semantic is not None:
            body["semantic"] = self.semantic
        if self.scoring_profiles is not None:
            body["scoringProfiles"] = self.scoring_profiles
        if self.default_scoring_profile is not None:
            body["defaultScoringProfile"] = self.default_scoring_profile
        if self.suggesters is not None:
            body["suggesters"] = self.suggesters
        if self.analyzers is not None:
            body["analyzers"] = self.analyzers
        if self.cors_options is not None:
            body["corsOptions"] = self.cors_options
        return body

    def _map_field(self, f):
        key_map = {
            "vector_search_profile": "vectorSearchProfile",
        }
        out = {}
        for k, v in f.items():
            if v is None:
                continue
            out[key_map.get(k, k)] = v
        return out

    def _create_or_update(self, body):
        return self.search_query(
            self.search_service_name, "/indexes/{0}".format(self.name),
            "PUT", body=body, admin_key=self.admin_key,
            expected_status_codes=[200, 201])

    def _is_current(self, desired, existing):
        # Compare the REST-shaped desired body against the existing resource.
        # default_compare walks the union of keys, so keys present only in
        # `existing` (server defaults, @odata.etag) are ignored; it returns
        # True when existing already satisfies desired. Deep-copy desired so
        # the comparison cannot mutate the body we would PUT.
        result = dict(compare=[])
        return self.default_compare({}, copy.deepcopy(desired), existing, '', result)


def main():
    AzureRMSearchIndex()


if __name__ == '__main__':
    main()
