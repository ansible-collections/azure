#!/usr/bin/python
#
# Copyright (c) 2020 Nikhil Patne (@nikhilpatne) and Sakar Mehra (@sakar97)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_apimanagementservice_info
version_added: '1.5.0'
short_description: Get ApiManagementService info
description:
    - Get info of ApiManagementService.
options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
    name:
        description:
            - Resource name.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Nikhil Patne (@nikhilpatne)
    - Sakar Mehra (@Sakar97)

'''

EXAMPLES = '''
- name: Get Api Management Service By Name and Resource Group
  azure_rm_apimanagementservice_info:
    resource_group: myResourceGroup
    name: myApiName

- name: Get Api Management Service By Resource Group
  azure_rm_apimanagementservice_info:
    resource_group: myResourceGroup

- name: Get Api Management Service By Subscription
  azure_rm_apimanagementservice_info:
'''

RETURN = '''
api_management_service:
    description:
        - A list of dict results where the key is the name of the ApiManagementService.
        - The values are the facts for that ApiManagementService.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.ApiManagement/service/myPolicy
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: myPolicy
        type:
            description:
                - Resource type for API Management resource is set to Microsoft.ApiManagement.
            returned: always
            type: str
            sample: Microsoft.ApiManagement/service
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: {'key1':'value1'}
        properties:
            description:
                - Properties of the API Management service.
            returned: always
            type: dict
            sample: null
        location:
            description:
                - Resource location.
            type: str
            returned: always
            sample: 'East US'
        sku:
            description:
                - SKU properties of the API Management service.
            returned: always
            type: str
            sample: Developer
        etag:
            description:
                - ETag of the resource.
            returned: always
            type: str
            sample: AAAAAAAsQK8=
        zones:
            description:
                - Zone of the resource.
            type: str
            returned: always
            sample: null
        identity:
            description:
                - Identity of the resource.
            type: str
            returned: always
            sample: null
'''

import time
import json
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from copy import deepcopy
try:
    from msrestazure.azure_exceptions import CloudError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMApiManagementServiceInfo(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            name=dict(
                type='str'
            )
        )

        self.resource_group = None
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        self.query_parameters = {}
        self.query_parameters['api-version'] = '2020-06-01-preview'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        self.mgmt_client = None
        super(AzureRMApiManagementServiceInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and self.name is not None):
            self.results['api_management_service'] = self.get()
        elif (self.resource_group is not None):
            self.results['api_management_service'] = self.listbyresourcegroup()
        else:
            self.results['api_management_service'] = self.list()
        return self.results

    def get(self):
        response = None
        results = {}
        self.url = ('/subscriptions' +
                    '/{{ subscription_id }}' +
                    '/resourceGroups' +
                    '/{{ resource_group }}' +
                    '/providers' +
                    '/Microsoft.ApiManagement' +
                    '/service' +
                    '/{{ service_name }}')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)
        self.url = self.url.replace('{{ resource_group }}', self.resource_group)
        self.url = self.url.replace('{{ service_name }}', self.name)

        try:
            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            results = json.loads(response.text)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return self.format_item(results)

    def listbyresourcegroup(self):
        response = None
        results = {}
        # prepare url
        self.url = ('/subscriptions' +
                    '/{{ subscription_id }}' +
                    '/resourceGroups' +
                    '/{{ resource_group }}' +
                    '/providers' +
                    '/Microsoft.ApiManagement' +
                    '/service')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)
        self.url = self.url.replace('{{ resource_group }}', self.resource_group)

        try:
            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            results = json.loads(response.text)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return [self.format_item(x) for x in results['value']] if results['value'] else []

    def list(self):
        response = None
        results = {}
        # prepare url
        self.url = ('/subscriptions' +
                    '/{{ subscription_id }}' +
                    '/providers' +
                    '/Microsoft.ApiManagement' +
                    '/service')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)

        try:
            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            results = json.loads(response.text)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return [self.format_item(x) for x in results['value']] if results['value'] else []

    def format_item(self, item):
        if item:
            d = {
                'id': item['id'],
                'name': item['name'],
                'type': item['type'],
                'sku': item['sku']['name'],
                'identity': item['identity'],
                'zones': item['zones'],
                'location': item['location'],
                'etag': item['etag'],
                'properties': item['properties']
            }
        else:
            return dict()
        return d


def main():
    AzureRMApiManagementServiceInfo()


if __name__ == '__main__':
    main()
