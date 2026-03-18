# Copyright (c) 2026 Bill Peck, <bpeck@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import traceback
try:
    from typing import Dict
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
    from azure.ai.ml import MLClient
    from azure.ai.ml._restclient.v2022_02_01_preview.models import ListViewType
    import json
except ImportError:
    pass


class MLClientCommon(AzureRMModuleBaseExt):

    @property
    def client(self):
        self.log('Getting client')
        if not self._client:
            self._client = MLClient(self.azure_auth.azure_credential_track2,
                                    subscription_id=self.subscription_id,
                                    resource_group_name=self.resource_group,
                                    workspace_name=self.ml_workspace,
                                    registry_name=self.ml_registry)
        return self._client

    def entity_to_dict(self, entity):
        """
        ENTITY._to_dict() returns and OrderedDict so we abuse json
        dumps and loads to return a Dict
        """
        if isinstance(entity, Dict):
            return entity
        try:
            entity = json.loads(json.dumps(entity._to_dict()))
            return entity
        except Exception as err:  # pylint: disable=broad-exception-caught
            self.module.warn("Failed to deserialize response: %s", str(err))
            self.module.warn(str(entity))
            self.module.debug(traceback.format_exc())

    def filter_required(self, workspace):
        """
        Filter out required networks which are automatically
        added so we can be idempotent.
        """

        if "managed_network" in workspace and \
                "outbound_rules" in workspace["managed_network"]:
            outbound_rules = workspace["managed_network"].pop("outbound_rules")
            updated_rules = []
            for outbound_rule in outbound_rules:
                if outbound_rule.get("category") != "required":
                    updated_rules.append(outbound_rule)
            workspace["managed_network"]["outbound_rules"] = updated_rules

        return workspace

    def get_list_view_type(self, list_type):
        list_types = dict(active=ListViewType.ACTIVE_ONLY,
                          archived=ListViewType.ARCHIVED_ONLY,
                          all=ListViewType.ALL)
        return list_types.get(list_type, ListViewType.ACTIVE_ONLY)
