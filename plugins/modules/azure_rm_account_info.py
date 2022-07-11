#!/usr/bin/python
#
# Copyright (c) 2020 Paul Aiton, < @paultaiton >
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
# To be added
'''


try:
    from msrestazure.azure_exceptions import CloudError
    from azure.graphrbac.models import GraphErrorException
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

        # Remove param after below issue resolved
        self.get_user_info = False

        # As different return info is gathered using 2 different clients
        # 1. All except "user" section of the return value uses azure.mgmt.subsctiption.operations.subscriptionoperations
        # 2. "user" section of the return value uses different client (graphrbac), 
        # both clients cannot be used in the same module hence module can return either (1) or (2)

        # Issue mentioned above: https://github.com/mandar242/azure/blob/dev/plugins/module_utils/azure_rm_common.py#L1515
        
        super(AzureRMAccountInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False,
                                                       is_ad_resource=False)


    def exec_module(self, **kwargs):

        result = []
        result = self.list_items()

        self.results['account_info'] = result
        return self.results

    def list_items(self):

        results = {}
        
        # Get
        # "homeTenantId": "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx",
        # "id": "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx",
        # "isDefault": true,
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
        except CloudError as exc:
            self.fail("Failed to list all subscriptions - {0}".format(str(exc)))

        results['id'] = subscription_list_response[0].subscription_id
        results['tenantId'] = subscription_list_response[0].tenant_id
        results['homeTenantId'] = subscription_list_response[0].tenant_id
        results['name'] = subscription_list_response[0].display_name
        results['state'] = subscription_list_response[0].state
        results['managedByTenants'] = self.get_managed_by_tenants_list(subscription_list_response[0].managed_by_tenants)
        
        # Get
        # "user": {
        #     "name": "mandar123456@abcdefg.onmicrosoft.com",
        #     "type": "user"self.
        # }
        # Makes use of azure graphrbac 
        # https://docs.microsoft.com/en-us/python/api/overview/azure/microsoft-graph?view=azure-python#client-library
        if self.get_user_info:
            results['user'] = self.get_aduser_info(subscription_list_response[0].tenant_id)
        else:
            results['user'] = {}

        return results

    def get_managed_by_tenants_list(self, object_list):

        result = []
        
        for item in object_list:
            result.append({"tenantId": item.tenant_id })

        return result

    def get_aduser_info(self, tenant_id):

        user = {}

        try:
            client = self.get_graphrbac_client(tenant_id)
            user_info = client.signed_in_user.get()
            user['name'] = user_info.user_principal_name
            user['type'] = user_info.object_type

        except GraphErrorException as e:
            self.fail("failed to get ad user info {0}".format(str(e)))

        return user

def main():
    AzureRMAccountInfo()


if __name__ == '__main__':
    main()
