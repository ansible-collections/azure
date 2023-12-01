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
  azure_client_id:
    description: azure service principal client id.
  azure_secret:
    description: azure service principal secret
  azure_tenant:
    description: azure tenant
  azure_cloud_environment:
    description: azure cloud environment
"""

EXAMPLES = """
set_fact:
  object_id: "{{ lookup('azure_service_principal_attribute',
                         azure_client_id=azure_client_id,
                         azure_secret=azure_secret,
                         azure_tenant=azure_secret) }}"
"""

RETURN = """
_raw:
  description:
    Returns object id of service principal.
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_native

try:
    from azure.cli.core import cloud as azure_cloud
    from azure.identity._credentials.client_secret import ClientSecretCredential
    import asyncio
    from msgraph import GraphServiceClient
    from msgraph.generated.service_principals.service_principals_request_builder import ServicePrincipalsRequestBuilder
except ImportError:
    pass


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):

        self.set_options(direct=kwargs)

        credentials = {}
        credentials['azure_client_id'] = self.get_option('azure_client_id', None)
        credentials['azure_secret'] = self.get_option('azure_secret', None)
        credentials['azure_tenant'] = self.get_option('azure_tenant', 'common')

        if credentials['azure_client_id'] is None or credentials['azure_secret'] is None:
            raise AnsibleError("Must specify azure_client_id and azure_secret")

        _cloud_environment = azure_cloud.AZURE_PUBLIC_CLOUD
        if self.get_option('azure_cloud_environment', None) is not None:
            _cloud_environment = azure_cloud.get_cloud_from_metadata_endpoint(credentials['azure_cloud_environment'])

        try:
            azure_credential_track2 = ClientSecretCredential(client_id=credentials['azure_client_id'],
                                                             client_secret=credentials['azure_secret'],
                                                             tenant_id=credentials['azure_tenant'],
                                                             authority=_cloud_environment.endpoints.active_directory)

            client = GraphServiceClient(azure_credential_track2)

            response = asyncio.get_event_loop().run_until_complete(self.get_service_principals(client, credentials['azure_client_id']))
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
