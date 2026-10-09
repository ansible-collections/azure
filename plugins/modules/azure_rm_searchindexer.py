#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_searchindexer
version_added: "4.2.0"
short_description: Manage an indexer in an Azure AI Search service
description:
    - Create, update, delete, run, and reset an indexer within an Azure AI Search
      service (data plane).
    - An indexer is the automated ingestion pipeline that pulls data from a data
      source, optionally enriches it through a skillset, and writes it into a
      search index on a schedule.
options:
    resource_group:
        description:
            - Name of the resource group containing the search service.
        required: true
        type: str
    search_service_name:
        description:
            - Name of the Azure AI Search service that hosts the indexer.
        required: true
        type: str
    name:
        description:
            - Name of the indexer.
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
    target_index_name:
        description:
            - Name of the search index the indexer writes documents to.
            - Required when creating an indexer.
        type: str
    data_source_name:
        description:
            - Name of the data source the indexer reads documents from.
            - Required when creating an indexer.
        type: str
    skillset_name:
        description:
            - Name of a skillset to run against documents during ingestion.
        type: str
    description:
        description:
            - Free-text description of the indexer.
        type: str
    schedule:
        description:
            - Indexing schedule for the indexer. Omit for an on-demand indexer.
        type: dict
        suboptions:
            interval:
                description:
                    - The interval between indexer runs, as an ISO 8601 duration
                      (for example C(P1D) for daily or C(PT6H) for every six hours).
                    - The smallest supported interval is five minutes (C(PT5M)).
                type: str
                required: true
            start_time:
                description:
                    - The UTC start time for the schedule, as an ISO 8601 datetime.
                    - If omitted, Azure assigns one.
                type: str
    field_mappings:
        description:
            - Mappings from source fields to target index fields.
            - Each entry is a dict with C(sourceFieldName), C(targetFieldName), and
              optionally C(mappingFunction).
        type: list
        elements: dict
    output_field_mappings:
        description:
            - Mappings from enriched (skillset output) fields to target index fields.
            - Each entry is a dict with C(sourceFieldName), C(targetFieldName), and
              optionally C(mappingFunction).
        type: list
        elements: dict
    parameters:
        description:
            - Indexer execution parameters such as C(batchSize), C(maxFailedItems),
              and a C(configuration) block (for example C(parsingMode) and
              C(excludedFileNameExtensions)).
        type: dict
    state:
        description:
            - Assert the state of the indexer.
            - C(present) creates or updates, C(absent) deletes.
            - C(run) triggers an on-demand run of an existing indexer.
            - C(reset) clears the indexer's change-tracking state so the next run
              reprocesses all documents.
            - C(run) and C(reset) are actions and always report C(changed=true).
        type: str
        default: present
        choices:
            - present
            - absent
            - run
            - reset
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create a scheduled indexer for a RAG knowledge base
  azure.azcollection.azure_rm_searchindexer:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: blob-indexer
    target_index_name: knowledge-index
    data_source_name: blob-datasource
    skillset_name: embedding-skillset
    schedule:
      interval: PT6H
    field_mappings:
      - sourceFieldName: metadata_storage_name
        targetFieldName: title
    output_field_mappings:
      - sourceFieldName: /document/embeddings
        targetFieldName: vector
    parameters:
      batchSize: 50
      configuration:
        parsingMode: default
        excludedFileNameExtensions: ".png,.jpg"
    state: present

- name: Trigger an on-demand indexer run
  azure.azcollection.azure_rm_searchindexer:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: blob-indexer
    state: run

- name: Reset the indexer's change-tracking state
  azure.azcollection.azure_rm_searchindexer:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: blob-indexer
    state: reset

- name: Delete an indexer
  azure.azcollection.azure_rm_searchindexer:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: blob-indexer
    state: absent
'''

RETURN = '''
state:
    description:
        - The indexer definition as returned by Azure AI Search.
    returned: when I(state=present)
    type: dict
    sample: {"name": "blob-indexer", "targetIndexName": "knowledge-index", "dataSourceName": "blob-datasource"}
'''

import copy

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_search_common import (
    AzureRMSearchDataPlaneMixin,
    ResourceNotFoundError,
)


class AzureRMSearchIndexer(AzureRMSearchDataPlaneMixin, AzureRMModuleBaseExt):

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            search_service_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            admin_key=dict(type='str', no_log=True),
            target_index_name=dict(type='str'),
            data_source_name=dict(type='str'),
            skillset_name=dict(type='str'),
            description=dict(type='str'),
            schedule=dict(type='dict', options=dict(
                interval=dict(type='str', required=True),
                start_time=dict(type='str'),
            )),
            field_mappings=dict(type='list', elements='dict'),
            output_field_mappings=dict(type='list', elements='dict'),
            parameters=dict(type='dict'),
            state=dict(type='str', default='present', choices=['present', 'absent', 'run', 'reset']),
        )
        self.resource_group = None
        self.search_service_name = None
        self.name = None
        self.admin_key = None
        self.target_index_name = None
        self.data_source_name = None
        self.skillset_name = None
        self.description = None
        self.schedule = None
        self.field_mappings = None
        self.output_field_mappings = None
        self.parameters = None
        self.state = None
        self.results = dict(changed=False)
        super(AzureRMSearchIndexer, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self.client = self.get_search_indexer_client(
            self.search_service_name, admin_key=self.admin_key)

        existing = self._get_existing()

        if self.state in ('run', 'reset'):
            self._action(existing)
        elif self.state == 'present':
            self._present(existing)
        else:  # absent
            if existing is not None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.client.delete_indexer(self.name)
        return self.results

    def _present(self, existing):
        if existing is None and (self.target_index_name is None or self.data_source_name is None):
            self.fail(msg="target_index_name and data_source_name are required to "
                          "create indexer '%s'; it does not exist yet" % self.name)
        desired = self._build_body()
        if existing is None:
            self.results['changed'] = True
            self.results['state'] = desired if self.check_mode else self._create_or_update(desired)
        elif not self._is_current(desired, existing):
            # create_or_update is a full-replace PUT; merge the user-supplied keys
            # onto the existing indexer so unsupplied settings are preserved.
            body = self._merge_existing(desired, existing)
            self.results['changed'] = True
            self.results['state'] = body if self.check_mode else self._create_or_update(body)
        else:
            self.results['state'] = existing

    def _action(self, existing):
        # run and reset are on-demand actions, not declarative state; they only
        # apply to an existing indexer and always report changed.
        if existing is None:
            self.fail(msg="indexer '%s' does not exist" % self.name)
        self.results['changed'] = True
        if not self.check_mode:
            if self.state == 'run':
                self.client.run_indexer(self.name)
            else:
                self.client.reset_indexer(self.name)

    def _get_existing(self):
        # The SDK raises ResourceNotFoundError when the indexer does not exist;
        # translate to None. Otherwise return the camelCase wire shape.
        try:
            return self.client.get_indexer(self.name).as_dict()
        except ResourceNotFoundError:
            return None

    def _build_body(self):
        body = {"name": self.name}
        if self.target_index_name is not None:
            body["targetIndexName"] = self.target_index_name
        if self.data_source_name is not None:
            body["dataSourceName"] = self.data_source_name
        if self.skillset_name is not None:
            body["skillsetName"] = self.skillset_name
        if self.description is not None:
            body["description"] = self.description
        if self.schedule is not None:
            body["schedule"] = self._map_schedule(self.schedule)
        if self.field_mappings is not None:
            body["fieldMappings"] = self.field_mappings
        if self.output_field_mappings is not None:
            body["outputFieldMappings"] = self.output_field_mappings
        if self.parameters is not None:
            body["parameters"] = self.parameters
        return body

    def _map_schedule(self, schedule):
        out = {"interval": schedule.get("interval")}
        if schedule.get("start_time") is not None:
            out["startTime"] = schedule["start_time"]
        return out

    def _merge_existing(self, desired, existing):
        # Overlay the user-supplied keys onto a copy of the existing indexer so a
        # PUT update does not drop settings the user did not resupply
        # (targetIndexName, dataSourceName, skillsetName, schedule, mappings,
        # parameters). Strip response-only @odata.* annotations.
        merged = {k: v for k, v in copy.deepcopy(existing).items()
                  if not k.startswith('@odata.')}
        merged.update(desired)
        return merged

    def _create_or_update(self, body):
        # create_or_update_indexer accepts a plain camelCase dict and returns the
        # full model; .as_dict() yields the wire shape.
        return self.client.create_or_update_indexer(body).as_dict()

    def _is_current(self, desired, existing):
        # Compare the REST-shaped desired body against the existing resource.
        # default_compare walks the union of keys, so keys present only in
        # `existing` (server defaults, @odata.etag, schedule.startTime) are
        # ignored. Deep-copy desired so the comparison cannot mutate the body
        # we would PUT.
        result = dict(compare=[])
        return self.default_compare({}, copy.deepcopy(desired), existing, '', result)


def main():
    AzureRMSearchIndexer()


if __name__ == '__main__':
    main()
