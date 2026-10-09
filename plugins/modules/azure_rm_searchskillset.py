#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_searchskillset
version_added: "4.2.0"
short_description: Manage a skillset in an Azure AI Search service
description:
    - Create, update, and delete a skillset within an Azure AI Search service
      (data plane). A skillset is an ordered set of enrichment skills (OCR,
      entity recognition, text split, embeddings, custom Web API skills, ...)
      that an indexer applies to documents during ingestion.
options:
    resource_group:
        description:
            - Name of the resource group containing the search service.
        required: true
        type: str
    search_service_name:
        description:
            - Name of the Azure AI Search service that hosts the skillset.
        required: true
        type: str
    name:
        description:
            - Name of the skillset.
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
    skills:
        description:
            - The ordered list of skills in the skillset. Required when creating a skillset.
            - Each skill is a dict passed through to the Azure AI Search API verbatim,
              keyed by its C(@odata.type) (for example
              C(#Microsoft.Skills.Text.SplitSkill)). See the Azure AI Search
              reference for each skill's inputs, outputs, and parameters.
        type: list
        elements: dict
    description:
        description:
            - Free-text description of the skillset.
        type: str
    cognitive_services:
        description:
            - Reference to an Azure AI (Cognitive) Services account used to bill
              the billable skills in the skillset.
            - Sent to Azure as C(cognitiveServices) using the by-key resource
              reference. Azure redacts the key on read, so changes to the key
              alone are not detected as drift.
            - On update, this must be resupplied to retain a key-based binding;
              if omitted, it is not re-sent and the skillset reverts to the
              default (free) cognitive services allocation.
        type: dict
        suboptions:
            key:
                description: API key of the Azure AI (Cognitive) Services account.
                type: str
                required: true
    knowledge_store:
        description:
            - Knowledge store definition (projections to Azure Storage).
            - Passed through to the Azure AI Search API using camelCase keys; see the Azure AI Search reference for structure.
        type: dict
    state:
        description:
            - Assert the state of the skillset. Use C(present) to create/update, C(absent) to delete.
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
- name: Create a text-split skillset
  azure.azcollection.azure_rm_searchskillset:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: chunking-skillset
    skills:
      - "@odata.type": "#Microsoft.Skills.Text.SplitSkill"
        context: /document
        textSplitMode: pages
        maximumPageLength: 1000
        inputs:
          - name: text
            source: /document/content
        outputs:
          - name: textItems
            targetName: pages
    state: present

- name: Delete a skillset
  azure.azcollection.azure_rm_searchskillset:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: chunking-skillset
    state: absent
'''

RETURN = '''
state:
    description:
        - The skillset definition as returned by Azure AI Search.
        - The cognitive services key is redacted by Azure and is not returned in clear text.
    returned: when I(state=present)
    type: dict
    sample: {"name": "chunking-skillset", "skills": [{"@odata.type": "#Microsoft.Skills.Text.SplitSkill"}]}
'''

import copy

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_search_common import (
    AzureRMSearchDataPlaneMixin,
    ResourceNotFoundError,
)


class AzureRMSearchSkillset(AzureRMSearchDataPlaneMixin, AzureRMModuleBaseExt):

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            search_service_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            admin_key=dict(type='str', no_log=True),
            skills=dict(type='list', elements='dict'),
            description=dict(type='str'),
            cognitive_services=dict(type='dict', options=dict(
                key=dict(type='str', required=True, no_log=True),
            )),
            knowledge_store=dict(type='dict'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )
        self.resource_group = None
        self.search_service_name = None
        self.name = None
        self.admin_key = None
        self.skills = None
        self.description = None
        self.cognitive_services = None
        self.knowledge_store = None
        self.state = None
        self.results = dict(changed=False)
        super(AzureRMSearchSkillset, self).__init__(
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
            if self.skills is None and existing is None:
                self.fail(msg="skills is required to create skillset '%s'; "
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
                    # supplied keys onto the existing skillset so unsupplied
                    # settings (skills, description, knowledgeStore) are preserved.
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
                    self.client.delete_skillset(self.name)
        return self.results

    def _get_existing(self):
        # The SDK raises ResourceNotFoundError when the skillset does not exist;
        # translate to None. Otherwise return the camelCase wire shape.
        try:
            return self.client.get_skillset(self.name).as_dict()
        except ResourceNotFoundError:
            return None

    def _build_body(self):
        body = {"name": self.name}
        if self.skills is not None:
            body["skills"] = self.skills
        if self.description is not None:
            body["description"] = self.description
        if self.cognitive_services is not None and self.cognitive_services.get("key") is not None:
            body["cognitiveServices"] = {
                "@odata.type": "#Microsoft.Azure.Search.CognitiveServicesByKey",
                "key": self.cognitive_services["key"],
            }
        if self.knowledge_store is not None:
            body["knowledgeStore"] = self.knowledge_store
        return body

    def _merge_existing(self, desired, existing):
        # Overlay the user-supplied keys onto a copy of the existing skillset so
        # a PUT update does not drop settings the user did not resupply (skills,
        # description, knowledgeStore). Strip response-only @odata.* annotations.
        # Azure redacts cognitiveServices.key on read and there is no "keep"
        # sentinel, so never echo the existing cognitiveServices; it is re-sent
        # only when the user supplies a key in `desired`.
        merged = {k: v for k, v in copy.deepcopy(existing).items()
                  if not k.startswith('@odata.')}
        merged.pop('cognitiveServices', None)
        merged.update(desired)
        return merged

    def _create_or_update(self, body):
        # create_or_update_skillset accepts a plain camelCase dict and returns
        # the full model; .as_dict() yields the wire shape.
        return self.client.create_or_update_skillset(body).as_dict()

    def _is_current(self, desired, existing):
        # Azure redacts cognitiveServices.key on read, so it can never match
        # what we would PUT. Drop cognitiveServices from the comparison; every
        # other field is compared via default_compare (union-of-keys walk, so
        # server defaults present only in `existing` are ignored). Deep-copy so
        # the comparison cannot mutate the body we would PUT.
        compare_body = copy.deepcopy(desired)
        compare_body.pop("cognitiveServices", None)
        result = dict(compare=[])
        return self.default_compare({}, compare_body, existing, '', result)


def main():
    AzureRMSearchSkillset()


if __name__ == '__main__':
    main()
