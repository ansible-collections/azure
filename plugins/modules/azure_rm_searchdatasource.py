#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_searchdatasource
version_added: "4.2.0"
short_description: Manage a data source in an Azure AI Search service
description:
    - Create, update, and delete a data source connection within an Azure AI
      Search service (data plane). A data source tells an indexer where to read
      documents from (Blob storage, Azure SQL, Cosmos DB, ADLS Gen2, or Table).
options:
    resource_group:
        description:
            - Name of the resource group containing the search service.
        required: true
        type: str
    search_service_name:
        description:
            - Name of the Azure AI Search service that hosts the data source.
        required: true
        type: str
    name:
        description:
            - Name of the data source.
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
    type:
        description:
            - The type of the data source. Required when creating a data source.
        type: str
        choices:
            - azureblob
            - azuretable
            - azuresql
            - cosmosdb
            - adlsgen2
    connection_string:
        description:
            - Connection string for the data source. Required when creating a data source.
            - Sent to Azure as C(credentials.connectionString). Azure redacts this
              value on read, so changes to the connection string alone are not
              detected as drift; every other field is compared normally.
            - On update, if omitted, the existing connection string is preserved.
        type: str
    container:
        description:
            - The container/table/collection the indexer reads from.
        type: dict
        suboptions:
            name:
                description: Name of the container, table, or collection.
                type: str
                required: true
            query:
                description:
                    - Optional query that narrows or shapes the rows/blobs returned
                      (for example a SQL query, a blob path prefix, or a Cosmos DB query).
                type: str
    data_change_detection_policy:
        description:
            - Change-detection policy used for incremental indexing.
            - Passed through to the Azure AI Search API using camelCase keys; see the Azure AI Search reference for structure.
        type: dict
    data_deletion_detection_policy:
        description:
            - Soft-delete detection policy used to remove documents from the index.
            - Passed through to the Azure AI Search API using camelCase keys; see the Azure AI Search reference for structure.
        type: dict
    description:
        description:
            - Free-text description of the data source.
        type: str
    state:
        description:
            - Assert the state of the data source. Use C(present) to create/update, C(absent) to delete.
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
- name: Create a blob data source
  azure.azcollection.azure_rm_searchdatasource:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: blob-ds
    type: azureblob
    connection_string: "{{ storage_connection_string }}"
    container:
      name: documents
      query: knowledge-base/
    state: present

- name: Delete a data source
  azure.azcollection.azure_rm_searchdatasource:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: blob-ds
    state: absent
'''

RETURN = '''
state:
    description:
        - The data source definition as returned by Azure AI Search.
        - The connection string is redacted by Azure and is not returned in clear text.
    returned: when I(state=present)
    type: dict
    sample: {"name": "blob-ds", "type": "azureblob", "container": {"name": "documents"}}
'''

import copy

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_search_common import (
    AzureRMSearchDataPlaneMixin,
    ResourceNotFoundError,
)

# Azure AI Search sentinel: keep the existing connection string unchanged on update.
UNCHANGED_CONNECTION_STRING = "<unchanged>"


class AzureRMSearchDataSource(AzureRMSearchDataPlaneMixin, AzureRMModuleBaseExt):

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            search_service_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            admin_key=dict(type='str', no_log=True),
            type=dict(type='str', choices=['azureblob', 'azuretable', 'azuresql', 'cosmosdb', 'adlsgen2']),
            connection_string=dict(type='str', no_log=True),
            container=dict(type='dict', options=dict(
                name=dict(type='str', required=True),
                query=dict(type='str'),
            )),
            data_change_detection_policy=dict(type='dict'),
            data_deletion_detection_policy=dict(type='dict'),
            description=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )
        self.resource_group = None
        self.search_service_name = None
        self.name = None
        self.admin_key = None
        self.type = None
        self.connection_string = None
        self.container = None
        self.data_change_detection_policy = None
        self.data_deletion_detection_policy = None
        self.description = None
        self.state = None
        self.results = dict(changed=False)
        super(AzureRMSearchDataSource, self).__init__(
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

        if self.state == 'present':
            if existing is None:
                if self.type is None:
                    self.fail(msg="type is required to create data source '%s'; "
                                  "it does not exist yet" % self.name)
                if self.connection_string is None:
                    self.fail(msg="connection_string is required to create data source "
                                  "'%s'; it does not exist yet" % self.name)
            desired = self._build_body(existing)
            if existing is None:
                self.results['changed'] = True
                if not self.check_mode:
                    self.results['state'] = self._create_or_update(desired)
                else:
                    self.results['state'] = desired
            else:
                if not self._is_current(desired, existing):
                    # create_or_update is a full-replace PUT; merge the user-
                    # supplied keys onto the existing data source so unsupplied
                    # settings are preserved.
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
                    self.client.delete_data_source_connection(self.name)
        return self.results

    def _get_existing(self):
        # The SDK raises ResourceNotFoundError when the data source does not
        # exist; translate to None. Otherwise return the camelCase wire shape.
        try:
            return self.client.get_data_source_connection(self.name).as_dict()
        except ResourceNotFoundError:
            return None

    def _build_body(self, existing):
        body = {"name": self.name}
        # type is immutable once set; fall back to the existing value on update
        # so a caller updating other fields need not repeat it.
        if self.type is not None:
            body["type"] = self.type
        elif existing is not None and existing.get("type") is not None:
            body["type"] = existing["type"]
        if self.connection_string is not None:
            body["credentials"] = {"connectionString": self.connection_string}
        if self.container is not None:
            container = {"name": self.container["name"]}
            if self.container.get("query") is not None:
                container["query"] = self.container["query"]
            body["container"] = container
        if self.data_change_detection_policy is not None:
            body["dataChangeDetectionPolicy"] = self.data_change_detection_policy
        if self.data_deletion_detection_policy is not None:
            body["dataDeletionDetectionPolicy"] = self.data_deletion_detection_policy
        if self.description is not None:
            body["description"] = self.description
        return body

    def _merge_existing(self, desired, existing):
        # Overlay the user-supplied keys onto a copy of the existing data source
        # so a PUT update does not drop settings the user did not resupply.
        # Response-only @odata.* annotations must not be echoed back.
        merged = {k: v for k, v in copy.deepcopy(existing).items()
                  if not k.startswith('@odata.')}
        merged.update(desired)
        # Azure redacts the connection string on read, so the value carried in
        # `existing` is not usable. If the user did not supply a new connection
        # string, send the <unchanged> sentinel to preserve the current one.
        if 'credentials' not in desired:
            merged['credentials'] = {"connectionString": UNCHANGED_CONNECTION_STRING}
        return merged

    def _create_or_update(self, body):
        # create_or_update_data_source_connection accepts a plain camelCase dict
        # and returns the full model; .as_dict() yields the wire shape.
        return self.client.create_or_update_data_source_connection(body).as_dict()

    def _is_current(self, desired, existing):
        # Azure redacts credentials.connectionString on read, so it can never
        # match what we would PUT. Drop credentials from the comparison; every
        # other field is compared via default_compare (union-of-keys walk, so
        # server defaults present only in `existing` are ignored). Deep-copy so
        # the comparison cannot mutate the body we would PUT.
        compare_body = copy.deepcopy(desired)
        compare_body.pop("credentials", None)
        result = dict(compare=[])
        return self.default_compare({}, compare_body, existing, '', result)


def main():
    AzureRMSearchDataSource()


if __name__ == '__main__':
    main()
