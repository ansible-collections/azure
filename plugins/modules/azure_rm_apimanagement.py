#!/usr/bin/python
#
# Copyright (c) 2020 Sakar Mehra (@sakar97), Nikhil Patne (@nikhilpatne)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_apimanagement
version_added: "1.6.0"
short_description: Manage Azure api instances
description:
    - Create azure api instance.
    - Update the existing azure api instance.
    - Delete azure api instance.

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
    api_id:
        description:
            - API revision identifier. It must be unique in the current API Management service instance.
        required: true
        type: str
    description:
        description:
            - Description of the API.
        type: str
    authentication_settings:
        description:
            - Collection of authentication settings included into this API.
        type: dict
        suboptions:
            o_auth2:
                description:
                    - OAuth2 Authentication settings
                type: dict
                suboptions:
                    authorization_server_id:
                        description:
                            - OAuth authorization server identifier.
                        type: str
                    scope:
                        description:
                            - operations scope.
                        type: str
            openid:
                description:
                    - OpenID Connect Authentication Settings
                type: dict
                suboptions:
                    openid_provider_id:
                        description:
                            - OAuth authorization server identifier.
                        type: str
                    bearer_token_sending_methods:
                        description:
                            - How to send token to the server.
                        type: list
                        elements: str
                        choices:
                            - authorizationHeader
                            - query
    subscription_key_parameter_names:
        description:
            - Protocols over which API is made available.
        type: dict
        suboptions:
            header:
                description:
                    - Subscription key header name.
                type: str
            query:
                description:
                    - Subscription key query string parameter name.
                type: str
    type:
        description:
            - Type of API
        type: str
        choices:
            - http
            - soap
    api_revision:
        description:
            - Describes the Revision of the Api.
            - If no value is provided, default revision 1 is created
        type: str
    api_version:
        description:
            - Indicates the Version identifier of the API if the API is versioned
        type: str
    is_current:
        description:
            - Indicates if API revision is current api revision.
        type: bool
    api_revision_description:
        description:
            - Description of the Api Revision.
        type: str
    api_version_description:
        description:
            - Description of the Api Version.
        type: str
    api_version_set_id:
        description:
            - A resource identifier for the related ApiVersionSet.
        type: str
    subscription_required:
        description:
            - Specifies whether an API or Product subscription is required for accessing the API.
        type: bool
    source_api_id:
        description:
            - API identifier of the source API.
        type: str
    display_name:
        description:
            - API Name to be displayed. It must be 1 to 300 characters long.
        type: str
    service_url:
        description:
            - Absolute URL of the backend service implementing this API
            - Cannot be more than 2000 characters long.
        type: str
    path:
        description:
            - Relative URL uniquely identifying this API.
        type: str
    protocols:
        description:
            - Describes on which protocols the operations in this API can be invoked.
        type: list
        elements: str
        choices:
            - http
            - https
    api_version_set:
        description:
            - Version set details
        type: dict
        suboptions:
            id:
                description:
                    - Identifier for existing API Version Set
                    - Omit this value to create a new Version Set.
                type: str
            name:
                description:
                    - The display Name of the API Version Set.
                type: str
            description:
                description:
                    - Description of API Version Set.
                type: str
            versioning_scheme:
                description:
                    - An value that determines where the API Version identifer will be located in a HTTP request.
                type: str
                choices:
                    - Segment
                    - Query
                    - Header
            version_query_name:
                description:
                    - Name of query parameter that indicates the API Version if versioningScheme is set to `query`.
                type: str
            version_header_name:
                description:
                    - Name of HTTP header parameter that indicates the API Version if versioningScheme is set to `header`.
                type: str
    value:
        description:
            - Content value when Importing an API.
        type: str
    format:
        description:
            - Format of the Content in which the API is getting imported.
        type: str
        choices:
            - wadl-xml
            - wadl-link-json
            - swagger-json
            - swagger-link-json
            - wsdl
            - wsdl-link
            - openapi
            - openapi+json
            - openapi-link
    wsdl_selector:
        description:
            - Criteria to limit import of WSDL to a subset of the document.
        type: dict
        suboptions:
            wsdl_service_name:
                description:
                    - Name of service to import from WSDL.
                type: str
            wsdl_endpoint_name:
                description:
                    - Name of endpoint(port) to import from WSDL.
                type: str
    api_type:
        description:
            - Type of Api to create.
            - C(http) creates a SOAP to REST API.
            - C(soap) creates a SOAP pass-through API.
        type: str
        choices:
            - soap
            - http
    state:
        description:
            - State of the Api.
            - Use C(present) to create or update an Api and C(absent) to delete it.
        type: str
        default: present
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Sakar Mehra (@sakar97)
    - Nikhil Patne (@nikhilpatne)

'''

EXAMPLES = '''
    - name: Create a new API instance
      azure_rm_apimanagement:
        resource_group: 'myResourceGroup'
        service_name: myService
        api_id: testApi
        description: testDescription
        display_name: TestAPI
        service_url: 'http://testapi.example.net/api'
        path: myapiPath
        protocols:
        - https
    - name: Update an existing API instance.
      azure_rm_apimanagement:
        resource_group: myResourceGroup
        service_name: myService
        api_id: testApi
        display_name: newTestAPI
        service_url: 'http://testapi.example.net/api'
        path: myapiPath
        protocols:
        - https
    - name: ApiManagementDeleteApi
      azure_rm_apimanagement:
        resource_group: myResourceGroup
        service_name: myService
        api_id: testApi
        state: absent
'''

RETURN = \
    '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
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


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureApiManagement(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                updatable=False,
                disposition='resourceGroupName',
                required=True
            ),
            service_name=dict(
                type='str',
                updatable=False,
                disposition='serviceName',
                required=True
            ),
            api_id=dict(
                type='str',
                updatable=False,
                disposition='apiId',
                required=True
            ),
            description=dict(
                type='str',
                disposition='/properties/description'
            ),
            authentication_settings=dict(
                type='dict',
                disposition='/properties/authenticationSettings',
                options=dict(
                    o_auth2=dict(
                        type='dict',
                        disposition='oAuth2',
                        options=dict(
                            authorization_server_id=dict(
                                type='str',
                                disposition='authorizationServerId'
                            ),
                            scope=dict(
                                type='str',
                                disposition='scope'
                            )
                        )
                    ),
                    openid=dict(
                        type='dict',
                        options=dict(
                            openid_provider_id=dict(
                                type='str',
                                disposition='openidProviderId'
                            ),
                            bearer_token_sending_methods=dict(
                                type='list',
                                elements='str',
                                disposition='bearerTokenSendingMethods',
                                choices=['authorizationHeader', 'query']
                            )
                        )
                    )
                )
            ),
            subscription_key_parameter_names=dict(
                type='dict',
                no_log=True,
                disposition='/properties/subscriptionKeyParameterNames',
                options=dict(
                    header=dict(
                        type='str',
                        required=False
                    ),
                    query=dict(
                        type='str',
                        required=False
                    )
                )
            ),
            type=dict(
                type='str',
                disposition='/properties/type',
                choices=['http', 'soap']
            ),
            api_revision=dict(
                type='str',
                disposition='/properties/apiRevision'
            ),
            api_version=dict(
                type='str',
                disposition='/properties/apiVersion'
            ),
            is_current=dict(
                type='bool',
                disposition='/properties/isCurrent'
            ),
            api_revision_description=dict(
                type='str',
                disposition='/properties/apiRevisionDescription'
            ),
            api_version_description=dict(
                type='str',
                disposition='/properties/apiVersionDescription'
            ),
            api_version_set_id=dict(
                type='str',
                disposition='/properties/apiVersionSetId',
            ),
            subscription_required=dict(
                type='bool',
                disposition='/properties/subscriptionRequired'
            ),
            source_api_id=dict(
                type='str',
                disposition='/properties/sourceApiId',
            ),
            display_name=dict(
                type='str',
                disposition='/properties/displayName'
            ),
            service_url=dict(
                type='str',
                disposition='/properties/serviceUrl'
            ),
            path=dict(
                type='str',
                disposition='/properties/*',
            ),
            protocols=dict(
                type='list',
                elements='str',
                disposition='/properties/protocols',
                choices=['http',
                         'https']
            ),
            api_version_set=dict(
                type='dict',
                disposition='/properties/apiVersionSet',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    name=dict(
                        type='str'
                    ),
                    description=dict(
                        type='str'
                    ),
                    versioning_scheme=dict(
                        type='str',
                        disposition='versioningScheme',
                        choices=['Segment',
                                 'Query',
                                 'Header']
                    ),
                    version_query_name=dict(
                        type='str',
                        disposition='versionQueryName'
                    ),
                    version_header_name=dict(
                        type='str',
                        disposition='versionHeaderName'
                    )
                )
            ),
            value=dict(
                type='str',
                disposition='/properties/*'
            ),
            format=dict(
                type='str',
                disposition='/properties/*',
                choices=['wadl-xml',
                         'wadl-link-json',
                         'swagger-json',
                         'swagger-link-json',
                         'wsdl',
                         'wsdl-link',
                         'openapi',
                         'openapi+json',
                         'openapi-link']
            ),
            wsdl_selector=dict(
                type='dict',
                disposition='/properties/wsdlSelector',
                options=dict(
                    wsdl_service_name=dict(
                        type='str',
                        disposition='wsdlServiceName'
                    ),
                    wsdl_endpoint_name=dict(
                        type='str',
                        disposition='wsdlEndpointName'
                    )
                )
            ),
            api_type=dict(
                type='str',
                disposition='/properties/apiType',
                choices=['http', 'soap']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.service_name = None
        self.api_id = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200, 201, 202]
        self.to_do = Actions.NoAction

        self.body = {}
        self.query_parameters = {}
        self.query_parameters['api-version'] = '2020-06-01-preview'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(AzureApiManagement, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def get_url(self):
        return '/subscriptions' + '/' + self.subscription_id \
               + '/resourceGroups' + '/' + self.resource_group \
               + '/providers' + '/Microsoft.ApiManagement' + '/service' \
               + '/' + self.service_name + '/apis' + '/' + self.api_id

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        # https://docs.microsoft.com/en-us/azure/templates/microsoft.apimanagement/service/apis
        self.inflate_parameters(self.module_arg_spec, self.body, 0)
        self.url = self.get_url()
        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_resource()

        if not old_response:
            self.log("Api instance does not exist in the given service.")
            if self.state == 'present':
                self.to_do = Actions.Create
            else:
                self.log("Old instance didn't exist")
        else:
            self.log("Api instance already exists in the given service.")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                modifiers = {}
                self.create_compare_modifiers(self.module_arg_spec, '', modifiers)
                self.results['modifiers'] = modifiers
                self.results['compare'] = []
                if not self.default_compare(modifiers, self.body, old_response, '', self.results):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log('Create and Update the Api instance.')

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_and_update_resource()
            self.results['changed'] = True

        elif self.to_do == Actions.Delete:
            self.log('Api instance deleted.')

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            self.delete_resource()
            self.results['changed'] = True
        else:
            self.log('No change in Api instance.')
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]

        return self.results

    # This function will create and update resource on the api management service.
    def create_and_update_resource(self):

        try:
            response = self.mgmt_client.query(
                self.url,
                'PUT',
                self.query_parameters,
                self.header_parameters,
                self.body,
                self.status_code,
                600,
                30,
            )
        except CloudError as exc:
            self.log('Error while creating/updating the Api instance.')
            self.fail('Error creating the Api instance: {0}'.format(str(exc)))
        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}

        return response

    def delete_resource(self):
        isDeleted = False
        try:
            response = self.mgmt_client.query(
                self.url,
                'DELETE',
                self.query_parameters,
                self.header_parameters,
                None,
                self.status_code,
                600,
                30,
            )
            isDeleted = True
        except CloudError as e:
            self.log('Error attempting to delete the Api instance.')
            self.fail('Error deleting the Api instance: {0}'.format(str(e)))

        return isDeleted

    def get_resource(self):
        isFound = False
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
            isFound = True
            response = json.loads(response.text)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not find the Api instance from the given parameters.')
        if isFound is True:
            return response
        return False


def main():
    AzureApiManagement()


if __name__ == '__main__':
    main()
