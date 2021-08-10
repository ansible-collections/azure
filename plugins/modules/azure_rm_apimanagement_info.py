#!/usr/bin/python
#
# Copyright (c) 2020 Sakar Mehra (@sakar97), Nikhil Patne (@nikhilpatne)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_apimanagement_info
version_added: "1.6.0"
short_description: Get the infomation of the API Instance
description:
    - Get the information of api instance.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    service_name:
        description:
            - The name of the API Management service.
        required: true
        type: str
    expand_api_version_set:
        description:
            - Include full ApiVersionSet resource in response
        type: bool
    include_not_tagged_apis:
        description:
            - Included not tagged APIs in the response.
        type: bool
    api_id:
        description:
            - API revision identifier. It must be unique in the current API Management service instance.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Sakar Mehra (@sakar97)
    - Nikhil Patne (@nikhilpatne)

'''

EXAMPLES = '''
    - name: Get the information of api
      azure_rm_apimanagement_info:
        resource_group: myResourceGroup
        service_name: myService
    - name: Get the information of api
      azure_rm_apimanagement_info:
        resource_group: myResourceGroup
        service_name: myService
        api_id: testApi
'''

RETURN = '''
api:
    description:
        - A list of dict results where the key is the name of the Api and the values are the facts for that Api.
    returned: always
    type: complex
    contains:
        api_name:
            description:
                - The api name provided by the user.
            type: complex
            contains:
                id:
                    description:
                        - Resource ID.
                    returned: always
                    type: str
                    sample: null
                name:
                    description:
                        - Resource name.
                    returned: always
                    type: str
                    sample: null
                type:
                    description:
                        - Resource type for API Management resource.
                    returned: always
                    type: str
                    sample: null
                properties:
                    description:
                        - Api entity contract properties.
                    returned: always
                    type: dict
                    sample: null

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from copy import deepcopy
import time
import json
import re
try:
    from msrestazure.azure_exceptions import CloudError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureApiManagementInfo(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            service_name=dict(
                type='str',
                required=True
            ),
            expand_api_version_set=dict(
                type='bool'
            ),
            include_not_tagged_apis=dict(
                type='bool'
            ),
            api_id=dict(
                type='str'
            )
        )

        self.resource_group = None
        self.service_name = None
        self.tags = None
        self.expand_api_version_set = None
        self.include_not_tagged_apis = None
        self.api_id = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        self.query_parameters = {}
        self.query_parameters['api-version'] = '2020-06-01-preview'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(AzureApiManagementInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.service_name is not None and
                self.api_id is not None):
            self.results['api'] = self.get_api_info()
        elif (self.resource_group is not None and
                self.service_name is not None):
            self.results['api'] = self.listbytags()
        elif (self.resource_group is not None and
                self.service_name is not None):
            self.results['api'] = self.listbyservice()
        return self.results

    def get_url(self):
        return '/subscriptions' + '/' + self.subscription_id \
               + '/resourceGroups' + '/' + self.resource_group \
               + '/providers' + '/Microsoft.ApiManagement' + '/service' \
               + '/' + self.service_name + '/apis' + '/' + self.api_id

    def get_url_bytags(self):
        return '/subscriptions' + '/' + self.subscription_id \
               + '/resourceGroups' + '/' + self.resource_group \
               + '/providers' + '/Microsoft.ApiManagement' + '/service' \
               + '/' + self.service_name + '/apisByTags'

    def get_url_byservice(self):
        return '/subscriptions' + '/' + self.subscription_id \
               + '/resourceGroups' + '/' + self.resource_group \
               + '/providers' + '/Microsoft.ApiManagement' + '/service' \
               + '/' + self.service_name + '/apis'

    def get_api_info(self):
        self.url = self.get_url()
        response = None

        try:
            response = self.mgmt_client.query(
                self.url,
                'GET',
                self.query_parameters,
                self.header_parameters,
                None,
                self.status_code,
                600,
                30,
            )
        except CloudError as e:
            self.log('Could not get the information.{0}'.format(e))
        try:
            response = json.loads(response.text)
        except Exception:
            return None

        return response

    def listbytags(self):
        self.url = self.get_url_bytags()
        response = None
        try:
            response = self.mgmt_client.query(
                self.url,
                'GET',
                self.query_parameters,
                self.header_parameters,
                None,
                self.status_code,
                600,
                30,
            )
        except CloudError as e:
            self.log('Could not get info for the given api tags {0}'.format(e))
        try:
            response = json.loads(response.text)
        except Exception:
            return None

        return response

    def listbyservice(self):
        self.url = self.get_url_byservice()
        response = None
        try:
            response = self.mgmt_client.query(
                self.url,
                'GET',
                self.query_parameters,
                self.header_parameters,
                None,
                self.status_code,
                600,
                30,
            )
            response = json.loads(response.text)
        except CloudError as e:
            self.log('Could not get info for a given services.{0}'.format(e))
        try:
            response = json.loads(response.text)
        except Exception:
            return None

        return response


def main():
    AzureApiManagementInfo()


if __name__ == '__main__':
    main()
