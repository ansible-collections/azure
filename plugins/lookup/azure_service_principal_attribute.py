# (c) 2018 Yunge Zhu, <yungez@microsoft.com>
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
name: azure_service_principal_attribute

requirements:
    - msgraph-sdk

author:
    - Yunge Zhu (@yungezz)

version_added: "1.12.0"

short_description: Look up Azure service principal attributes.

description:
  - Describes object id of your Azure service principal account.
options:
  client_id:
    description: azure service principal client id.
    aliases:
      - azure_client_id
  secret:
    description: azure service principal secret
    aliases:
      - azure_secret
  tenant:
    description: azure tenant
    aliases:
      - azure_tenant
  cloud_environment:
    description: azure cloud environment
    aliases:
      - azure_cloud_environment
notes:
    - If MSI is not enabled on ansible host, it's required to provide a valid service principal which has access to the key vault.
    - To authenticate via service principal, pass client_id, secret and tenant or set environment variables
      AZURE_CLIENT_ID, AZURE_CLIENT_SECRET and AZURE_TENANT_ID.
    - Authentication via C(az login) is also supported.
"""

EXAMPLES = """
set_fact:
  object_id: "{{ lookup('azure_service_principal_attribute',
                         client_id=azure_client_id,
                         secret=azure_secret,
                         tenant=azure_secret) }}"
"""

RETURN = """
_raw:
  description:
    Returns object id of service principal.
"""

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMAuth
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_native

try:
    import asyncio
    from msgraph import GraphServiceClient
    from msgraph.generated.service_principals.service_principals_request_builder import ServicePrincipalsRequestBuilder
except ImportError:
    pass


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):

        self.set_options(direct=kwargs)

        auth_options = dict(
            client_id=self.get_option('client_id'),
            secret=self.get_option('secret'),
            tenant=self.get_option('tenant', 'common'),
            cloud_environment=self.get_options('cloud_environment'),
            is_ad_resource=True
        )
        azure_auth = AzureRMAuth(**auth_options)

        try:
            client = GraphServiceClient(azure_auth.azure_credential_track2)

            response = asyncio.get_event_loop().run_until_complete(self.get_service_principals(client, azure_auth.credentials['client_id']))
            if not response:
                return []
            return list(response.value)[0].id.split(',')
        except Exception as ex:
            raise AnsibleError("Failed to get service principal object id: %s" % to_native(ex))
        return False

    async def get_service_principals(self, _client, app_id):
        request_configuration = ServicePrincipalsRequestBuilder.ServicePrincipalsRequestBuilderGetRequestConfiguration(
            query_parameters=ServicePrincipalsRequestBuilder.ServicePrincipalsRequestBuilderGetQueryParameters(
                filter="servicePrincipalNames/any(c:c eq '{0}')".format(app_id),
            )
        )
        return await _client.service_principals.get(request_configuration=request_configuration)
