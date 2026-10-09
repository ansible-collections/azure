# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import traceback

from ansible.module_utils.basic import missing_required_lib

try:
    from azure.core.credentials import AzureKeyCredential
    from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
    from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
    HAS_SEARCH_SDK = True
    SEARCH_SDK_IMPORT_ERROR = None
except ImportError:  # pragma: no cover - exercised only without the SDK
    HAS_SEARCH_SDK = False
    # Capture the full traceback so a dependency incompatibility (an installed
    # but broken package) is distinguishable from a simply-missing package.
    SEARCH_SDK_IMPORT_ERROR = traceback.format_exc()
    # Define placeholders so module-level references resolve; the mixin guards
    # on HAS_SEARCH_SDK before using any of these.
    ResourceNotFoundError = Exception
    HttpResponseError = Exception

# ResourceNotFoundError and HttpResponseError are re-exported here so the search
# modules import their SDK exceptions from one place; declare them exported.
__all__ = ['AzureRMSearchDataPlaneMixin', 'ResourceNotFoundError', 'HttpResponseError']


class AzureRMSearchDataPlaneMixin(object):
    """Mixin for Azure AI Search data-plane (search.windows.net) access.

    Uses the ``azure-search-documents`` SDK (``SearchIndexClient`` and
    ``SearchIndexerClient``). Must be combined with AzureRMModuleBaseExt, which
    provides azure_auth, _cloud_environment, fail and default_compare.
    """

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

    def _search_credential(self, admin_key):
        # Admin-key auth uses an AzureKeyCredential (api-key header); otherwise
        # authenticate with the standard Azure (RBAC) token credential. The SDK
        # requests the https://search.azure.com/.default data-plane scope.
        if admin_key:
            return AzureKeyCredential(admin_key)
        return self.azure_auth.azure_credential_track2

    def _require_search_sdk(self):
        if not HAS_SEARCH_SDK:
            self.fail(msg=missing_required_lib('azure-search-documents'),
                      exception=SEARCH_SDK_IMPORT_ERROR)

    def get_search_index_client(self, service_name, admin_key=None):
        """Return a SearchIndexClient for index and synonym-map operations."""
        self._require_search_sdk()
        return SearchIndexClient(
            endpoint=self.search_endpoint(service_name),
            credential=self._search_credential(admin_key))

    def get_search_indexer_client(self, service_name, admin_key=None):
        """Return a SearchIndexerClient for data source, skillset and indexer ops."""
        self._require_search_sdk()
        return SearchIndexerClient(
            endpoint=self.search_endpoint(service_name),
            credential=self._search_credential(admin_key))
