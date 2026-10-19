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
            - Custom Web API skills (C(#Microsoft.Skills.Custom.WebApiSkill)) may
              embed secrets in C(httpHeaders) and in the C(?code=) query of C(uri).
              Azure redacts these on read (as C(<redacted>)). When an update omits
              I(skills), the module carries the existing skills forward and replaces
              those C(<redacted>) placeholders with the C(<unchanged>) sentinel so
              the real secrets are preserved. Because the redacted values cannot be
              compared, a skillset with such skills may still report C(changed) when
              you do supply I(skills) with the real secret values.
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
            - For key-based bindings Azure redacts the key on read, so changes to
              the key alone are not detected as drift, and on update a key-based
              binding must be resupplied to be retained (it is not echoed back).
              If an update to an existing skillset with a key-based binding omits
              I(cognitive_services), the module fails rather than silently dropping
              the binding. Keyless bindings hold no secret and are preserved across
              updates.
        type: dict
        suboptions:
            type:
                description:
                    - The binding C(@odata.type), for example
                      C(#Microsoft.Azure.Search.CognitiveServicesByKey),
                      C(#Microsoft.Azure.Search.AIServicesByKey),
                      C(#Microsoft.Azure.Search.AIServicesByIdentity) (keyless), or
                      C(#Microsoft.Azure.Search.DefaultCognitiveServices).
                type: str
                required: true
            key:
                description: API key, for the C(*ByKey) bindings.
                type: str
            subdomain_url:
                description: Custom subdomain URL, for the C(AIServices*) bindings.
                type: str
            identity:
                description:
                    - Managed identity, for C(AIServicesByIdentity). Pass-through dict
                      with its own C(@odata.type) (for example
                      C(#Microsoft.Azure.Search.DataUserAssignedIdentity) with a
                      C(userAssignedIdentity) resource ID).
                type: dict
    knowledge_store:
        description:
            - Knowledge store definition (projections to Azure Storage).
            - Must be supplied in full on every run. The service requires both
              C(storage_connection_string) and C(projections), the update is a
              full-replace, and the connection string is redacted on read - so a
              partial value cannot be merged with the existing store.
        type: dict
        suboptions:
            storage_connection_string:
                description: Connection string for the Azure Storage account the projections are written to.
                type: str
                required: true
            projections:
                description:
                    - List of projection definitions (tables, objects, files).
                    - Passed through to the Azure AI Search API using camelCase keys.
                type: list
                elements: dict
                required: true
            identity:
                description:
                    - Managed identity used to access the storage account.
                    - Passed through using camelCase keys.
                type: dict
    index_projections:
        description:
            - Index projections definition (project enriched content into one or more
              search indexes), sent as C(indexProjections).
            - Passed through to the Azure AI Search API using camelCase keys; see the
              Azure AI Search reference for structure.
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

- name: Skillset billed to an Azure AI Services account via managed identity (keyless)
  azure.azcollection.azure_rm_searchskillset:
    resource_group: myResourceGroup
    search_service_name: mysearchsvc
    name: enrichment-skillset
    skills:
      - "@odata.type": "#Microsoft.Skills.Text.V3.EntityRecognitionSkill"
        context: /document
        inputs:
          - name: text
            source: /document/content
        outputs:
          - name: persons
            targetName: people
    cognitive_services:
      type: "#Microsoft.Azure.Search.AIServicesByIdentity"
      subdomain_url: https://myaiservices.cognitiveservices.azure.com/
      identity:
        "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity"
        userAssignedIdentity: "/subscriptions/xxx/resourceGroups/myResourceGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/mi"
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
                type=dict(type='str', required=True),
                key=dict(type='str', no_log=True),
                subdomain_url=dict(type='str'),
                identity=dict(type='dict'),
            )),
            knowledge_store=dict(type='dict', options=dict(
                storage_connection_string=dict(type='str', required=True, no_log=True),
                projections=dict(type='list', elements='dict', required=True),
                identity=dict(type='dict'),
            )),
            index_projections=dict(type='dict'),
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
        self.index_projections = None
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
                    self._check_binding_preserved(existing)
                    self._check_knowledge_store_preserved(existing)
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
        if self.cognitive_services is not None:
            cs = {"@odata.type": self.cognitive_services["type"]}
            if self.cognitive_services.get("key") is not None:
                cs["key"] = self.cognitive_services["key"]
            if self.cognitive_services.get("subdomain_url") is not None:
                cs["subdomainUrl"] = self.cognitive_services["subdomain_url"]
            if self.cognitive_services.get("identity") is not None:
                cs["identity"] = self.cognitive_services["identity"]
            body["cognitiveServices"] = cs
        if self.knowledge_store is not None:
            ks = {}
            if self.knowledge_store.get("storage_connection_string") is not None:
                ks["storageConnectionString"] = self.knowledge_store["storage_connection_string"]
            if self.knowledge_store.get("projections") is not None:
                ks["projections"] = self.knowledge_store["projections"]
            if self.knowledge_store.get("identity") is not None:
                ks["identity"] = self.knowledge_store["identity"]
            body["knowledgeStore"] = ks
        if self.index_projections is not None:
            body["indexProjections"] = self.index_projections
        return body

    def _check_binding_preserved(self, existing):
        # A key-based cognitiveServices binding has its key redacted on read and
        # cannot be carried forward, so an update that omits cognitive_services
        # would silently drop the binding (billable skills fall back to the free
        # tier). Fail clearly instead; the user must resupply cognitive_services.
        existing_cs = (existing or {}).get('cognitiveServices')
        if (self.cognitive_services is None and existing_cs is not None
                and self._binding_has_secret(existing_cs)):
            self.fail(msg="skillset '%s' has a key-based cognitive_services binding whose key "
                          "is redacted on read and cannot be preserved; resupply "
                          "cognitive_services so it is not dropped on update" % self.name)

    def _check_knowledge_store_preserved(self, existing):
        # knowledgeStore.storageConnectionString is redacted on read and cannot be
        # carried forward, so an update that omits knowledge_store would drop the
        # existing store. Fail clearly; the user must resupply knowledge_store.
        if self.knowledge_store is None and (existing or {}).get('knowledgeStore') is not None:
            self.fail(msg="skillset '%s' has a knowledge_store whose connection string is "
                          "redacted on read and cannot be preserved; resupply knowledge_store "
                          "so it is not dropped on update" % self.name)

    @staticmethod
    def _binding_has_secret(binding):
        # A cognitiveServices binding carries a secret (redacted on read) when it
        # has a 'key' field or its @odata.type is a *ByKey variant.
        if not isinstance(binding, dict):
            return False
        if binding.get('key') is not None:
            return True
        return str(binding.get('@odata.type', '')).endswith('ByKey')

    def _merge_existing(self, desired, existing):
        # Shared mixin helper does the common merge (strips @odata.* and the
        # unmanaged encryptionKey). cognitiveServices is dropped and handled here:
        # a key-based binding is redacted on read, so it must be resupplied to be
        # retained; a keyless binding (identity / default) holds no secret, so it
        # is preserved across updates when the user did not resupply one.
        # Drop cognitiveServices and knowledgeStore from the carry-forward: both
        # hold secrets redacted on read (the binding key / storageConnectionString)
        # so the existing values cannot be echoed back.
        merged = self.merge_search_update(existing, desired,
                                          drop_keys=('cognitiveServices', 'knowledgeStore'))
        existing_cs = (existing or {}).get('cognitiveServices')
        if (existing_cs is not None and not self._binding_has_secret(existing_cs)
                and 'cognitiveServices' not in desired):
            merged['cognitiveServices'] = existing_cs
        # When skills are carried forward from the existing skillset (the user did
        # not resupply them), replace Azure's <redacted> secret placeholders with
        # the <unchanged> sentinel so the PUT keeps the real secrets (e.g. custom
        # Web API skill httpHeaders / uri) instead of overwriting them.
        if 'skills' not in desired and isinstance(merged.get('skills'), list):
            merged['skills'] = self._mask_redacted(merged['skills'])
        return merged

    @classmethod
    def _mask_redacted(cls, obj):
        # Azure redacts skill secrets on read as the literal "<redacted>" - either
        # as a whole value (httpHeaders values) or embedded in a string (the
        # ?code= query of a Web API skill uri). Replace any string that contains
        # it with the "<unchanged>" sentinel, which the service keeps as-is.
        if isinstance(obj, dict):
            return {k: cls._mask_redacted(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [cls._mask_redacted(v) for v in obj]
        if isinstance(obj, str) and '<redacted>' in obj:
            return '<unchanged>'
        return obj

    def _create_or_update(self, body):
        # create_or_update_skillset accepts a plain camelCase dict and returns
        # the full model; .as_dict() yields the wire shape.
        return self.client.create_or_update_skillset(body).as_dict()

    def _is_current(self, desired, existing):
        # Azure redacts only cognitiveServices.key on read, so compare the rest of
        # the binding (its @odata.type, subdomainUrl, identity) and drop just the
        # key - this detects a binding-type switch while ignoring the redacted key.
        # Everything else is compared via default_compare (union-of-keys walk, so
        # server defaults present only in `existing` are ignored). Deep-copy so the
        # comparison cannot mutate the body we would PUT.
        compare_body = copy.deepcopy(desired)
        cs = compare_body.get("cognitiveServices")
        if isinstance(cs, dict):
            cs.pop("key", None)
        # knowledgeStore.storageConnectionString is likewise redacted on read;
        # drop it so a skillset with a knowledge store is not reported changed
        # every run (other knowledgeStore fields are still compared).
        ks = compare_body.get("knowledgeStore")
        if isinstance(ks, dict):
            ks.pop("storageConnectionString", None)
        result = dict(compare=[])
        return self.default_compare({}, compare_body, existing, '', result)


def main():
    AzureRMSearchSkillset()


if __name__ == '__main__':
    main()
