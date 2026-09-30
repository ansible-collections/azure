# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import (
        GenericRestClient, SendRequestException,
    )
except ImportError:
    # handled by AzureRMModuleBase import checks in the consuming module
    pass


class AzureRMSearchDataPlaneMixin(object):
    """Mixin for Azure AI Search data-plane (search.windows.net) REST access.

    Must be combined with AzureRMModuleBaseExt, which provides azure_auth,
    subscription_id, _cloud_environment, fail and default_compare.
    """

    SEARCH_API_VERSION = "2024-07-01"

    def search_endpoint(self, service_name):
        # Default public cloud suffix; sovereign clouds override via the
        # cloud environment's suffixes when available.
        suffix = "search.windows.net"
        try:
            configured = getattr(self._cloud_environment.suffixes, "search_endpoint", None)
            if configured:
                suffix = configured.lstrip(".")
        except Exception:
            pass
        return "https://{0}.{1}".format(service_name, suffix)

    def get_search_client(self, service_name, admin_key=None):
        base_url = self.search_endpoint(service_name)
        self._search_headers = {"Content-Type": "application/json; charset=utf-8"}
        if admin_key:
            # Admin-key auth: still need a credential object for the client,
            # but requests authenticate via the api-key header.
            self._search_headers["api-key"] = admin_key
        client = GenericRestClient(
            credential=self.azure_auth.azure_credential_track2,
            subscription_id=self.subscription_id,
            base_url=base_url,
            credential_scopes=["https://search.azure.com/.default"],
        )
        return client

    def search_query(self, service_name, path, method, body=None,
                     admin_key=None, expected_status_codes=None):
        client = self.get_search_client(service_name, admin_key=admin_key)
        url = "{0}{1}".format(self.search_endpoint(service_name), path)
        query_parameters = {"api-version": self.SEARCH_API_VERSION}
        if expected_status_codes is None:
            expected_status_codes = [200, 201, 204]
        # Treat 404 as "absent" for callers that opt in.
        codes = list(expected_status_codes) + [404]
        try:
            response = client.query(
                url, method, query_parameters, self._search_headers,
                body, codes, 0, 0,
            )
        except SendRequestException as exc:
            self.fail(msg="Azure AI Search request failed ({0} {1}): {2}".format(
                method, path, exc.response), status_code=getattr(exc, "status_code", None))
        status = getattr(response, "status_code", None)
        if status == 404:
            return None
        if method == "DELETE":
            return True
        if hasattr(response, "body"):
            text = response.body()
        elif hasattr(response, "text"):
            text = response.text()
        else:
            return None
        if not text:
            return None
        return json.loads(text)
