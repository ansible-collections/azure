# Copyright (c) 2026 Bill Peck, <bpeck@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
    from azure.ai.ml import MLClient
    import json
except ImportError:
    pass


class MLClientCommon(AzureRMModuleBaseExt):

    @property
    def client(self):
        self.log('Getting client')
        if not self._client:
            self._client = MLClient(self.azure_auth.azure_credential_track2,
                                    self.subscription_id,
                                    self.resource_group,
                                    self.ml_workspace)
        return self._client

    def ws_to_dict(self, ws, filter=False):
        """
        Workspace._to_dict() returns an OrderedDict so we abuse json
        dumps and loads to return a Dict
        """
        workspace = json.loads(json.dumps(ws._to_dict()))

        # Filter out required networks which are automatically
        # added so we can be idempotent.
        if filter and \
                "managed_network" in workspace and \
                "outbound_rules" in workspace["managed_network"]:
            outbound_rules = workspace["managed_network"].pop("outbound_rules")
            updated_rules = []
            for outbound_rule in outbound_rules:
                if outbound_rule.get("category") != "required":
                    updated_rules.append(outbound_rule)
            workspace["managed_network"]["outbound_rules"] = updated_rules

        return workspace
