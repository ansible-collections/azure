#!/usr/bin/python
#
# Copyright (c) 2022 Mandar Kulkarni, < @mandar242 >
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_account_info

version_added: "1.14.0"

short_description: Get Azure Account facts (output of az account show)

description:
    - Get facts for current logged in user.
    - Output equivalent of `az account show` command.

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Mandar Kulkarni (@mandar242)
'''

EXAMPLES = '''
- name: Get facts for current logged in user
  azure.azcollection.azure_rm_account_info:
'''

RETURN = '''
account_info:
    description:
        - Facts for current logged in user, equivalent to `az account show`.
    returned: always
    type: dict
    contains:
        environmentName:
            description: For cloud environments other than the US public cloud, the environment name.
            returned: always
            type: str
            sample: AzureCloud
        homeTenantId:
            description: Subscription tenant id.
            returned: always
            type: str
            sample: "00000000-0000-0000-0000-000000000000"
        id:
            description: Subscription id.
            returned: always
            type: str
            sample: "00000000-0000-0000-0000-000000000000"
        managedByTenants:
            description: An array containing the tenants managing the subscription.
            returned: always
            type: list
            elements: dict
            contains:
                tenantId:
                    description: Subscription tenant id
                    returned: always
                    type: str
                    sample: "00000000-0000-0000-0000-000000000000"
        name:
            description: The subscription display name.
            returned: always
            type: str
            sample: "Pay-As-You-Go"
        state:
            description:
                - The subscription state.
                - Possible values include "Enabled", "Warned", "PastDue", "Disabled", "Deleted".
            returned: always
            type: str
            sample: "Enabled"
        tenant_id:
            description: Subscription tenant id
            returned: always
            type: str
            sample: "00000000-0000-0000-0000-000000000000"
        user:
            description: An dict containing the current user name and type.
            returned: always
            type: dict
            elements: str
            contains:
                name:
                    description: The principal name of the active directory user.
                    returned: always
                    type: str
                    sample: "sample-user@sample-tenant.onmicrosoft.com"
                type:
                    description: Active Directory user type.
                    returned: always
                    type: str
                    sample: "User"
'''


try:
    import asyncio
    from msgraph.generated.education.me.user.user_request_builder import UserRequestBuilder
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMAccountInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
        )

        self.results = dict(
            changed=False,
            account_info=[]
        )

        # Different return info is gathered using 2 different clients
        # 1. All except "user" section of the return value uses azure.mgmt.subsctiption.operations.subscriptionoperations
        # 2. "user" section of the return value uses different client (GraphServiceClient)

        super(AzureRMAccountInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=False,
                                                 is_ad_resource=True)

    def exec_module(self, **kwargs):
        self.results['account_info'] = self.list_items()
        return self.results

    def list_items(self):

        results = {}

        # Get
        # "homeTenantId": "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx",
        # "id": "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx",
        # "isDefault": true,                                    <- WIP on getting this param
        # "managedByTenants": [
        #     {
        #     "tenantId": "64xxxxxx-xxxx-49fc-xxxx-ebxxxxxxxxxx"
        #     },
        #     {
        #     "tenantId": "2axxxxxx-xxxx-xxxx-a339-ebxxxxxxxxxx"
        #     },
        #     {
        #     "tenantId": "xxxxxxxx-xxxx-4e68-xxxx-ebxxxxxxxxxx"
        #     }
        # ],
        # "name": "Pay-As-You-Go",
        # "state": "Enabled",
        # "tenantId": "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx",

        # Makes use of azure.mgmt.subsctiption.operations.subscriptionoperations
        # https://docs.microsoft.com/en-us/python/api/azure-mgmt-subscription/azure.mgmt.subscription.operations.subscriptionsoperations?view=azure-python#methods

        try:
            subscription_list_response = list(self.subscription_client.subscriptions.list())
        except Exception as exc:
            self.fail("Failed to list all subscriptions - {0}".format(str(exc)))

        results['id'] = subscription_list_response[0].subscription_id
        results['tenantId'] = subscription_list_response[0].tenant_id
        results['homeTenantId'] = subscription_list_response[0].tenant_id
        results['name'] = subscription_list_response[0].display_name
        results['state'] = subscription_list_response[0].state
        results['managedByTenants'] = self.get_managed_by_tenants_list(subscription_list_response[0].managed_by_tenants)
        results['environmentName'] = self.azure_auth._cloud_environment.name
        results['user'] = self.get_aduser_info()

        return results

    def get_managed_by_tenants_list(self, object_list):

        return [dict(tenantId=item.tenant_id) for item in object_list]

    def get_aduser_info(self):

        # Create GraphServiceClient for getting
        # "user": {
        #     "name": "mandar123456@abcdefg.onmicrosoft.com",
        #     "type": "Member"
        # }

        # Makes use of azure MSGraph
        # https://learn.microsoft.com/en-us/graph/api/user-get?view=graph-rest-1.0&tabs=http

        user = {}

        user_info = asyncio.get_event_loop().run_until_complete(self.getAccount())
        user['name'] = user_info.user_principal_name
        user['type'] = user_info.user_type
        return user

    async def getAccount(self):
        return await self.get_msgraph_client().me.get(
            request_configuration=UserRequestBuilder.UserRequestBuilderGetRequestConfiguration(
                query_parameters=UserRequestBuilder.UserRequestBuilderGetQueryParameters(
                    select=["userType", "userPrincipalName", "postalCode", "identities"], ),
            )
        )


def main():
    AzureRMAccountInfo()


if __name__ == '__main__':
    main()
