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
import json


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureApiManagement(AzureRMModuleBaseExt):
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
            api_id=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='str',
            ),
            authentication_settings=dict(
                type='dict',
                options=dict(
                    o_auth2=dict(
                        type='dict',
                        options=dict(
                            authorization_server_id=dict(
                                type='str',
                            ),
                            scope=dict(
                                type='str',
                            )
                        )
                    ),
                    openid=dict(
                        type='dict',
                        options=dict(
                            openid_provider_id=dict(
                                type='str',
                            ),
                            bearer_token_sending_methods=dict(
                                type='list',
                                elements='str',
                                choices=['authorizationHeader', 'query']
                            )
                        )
                    )
                )
            ),
            subscription_key_parameter_names=dict(
                type='dict',
                no_log=True,
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
                choices=['http', 'soap']
            ),
            api_revision=dict(
                type='str',
            ),
            api_version=dict(
                type='str',
            ),
            is_current=dict(
                type='bool',
            ),
            api_revision_description=dict(
                type='str',
            ),
            api_version_description=dict(
                type='str',
            ),
            api_version_set_id=dict(
                type='str',
            ),
            subscription_required=dict(
                type='bool',
            ),
            source_api_id=dict(
                type='str',
            ),
            display_name=dict(
                type='str',
            ),
            service_url=dict(
                type='str',
            ),
            path=dict(
                type='str',
            ),
            protocols=dict(
                type='list',
                elements='str',
                choices=['http',
                         'https']
            ),
            api_version_set=dict(
                type='dict',
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
                        choices=['Segment',
                                 'Query',
                                 'Header']
                    ),
                    version_query_name=dict(
                        type='str',
                    ),
                    version_header_name=dict(
                        type='str',
                    )
                )
            ),
            value=dict(
                type='str',
            ),
            format=dict(
                type='str',
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
                options=dict(
                    wsdl_service_name=dict(
                        type='str',
                    ),
                    wsdl_endpoint_name=dict(
                        type='str',
                    )
                )
            ),
            api_type=dict(
                type='str',
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
        self.body['properties'] = {}
        self.query_parameters = {}
        self.query_parameters['api-version'] = '2022-08-01'
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
                if key == 'description':
                    self.body['properties']['description'] = kwargs[key]
                elif key == 'authentication_settings':
                    self.body['properties']['authenticationSettings'] = {}
                    if kwargs[key].get('o_auth2') is not None:
                        self.body['properties']['authenticationSettings']['oAuth2'] = {}
                        for item in kwargs[key]['o_auth2'].keys():
                            if item == 'authorization_server_id':
                                authorization_id = kwargs[key]['o_auth2']['authorization_server_id']
                                self.body['properties']['authenticationSettings']['oAuth2']['authorizationServerId'] = authorization_id
                            elif item == 'scope':
                                self.body['properties']['authenticationSettings']['oAuth2']['scope'] = kwargs[key]['o_auth2']['scope']
                    elif kwargs[key].get('openid') is not None:
                        self.body['properties']['authenticationSettings']['openid'] = {}
                        for item in kwargs[key]['openid'].keys():
                            if item == 'openid_provider_id' and kwargs[key]['openid'].get('openid_provider_id') is not None:
                                openid_pro = kwargs[key]['openid'].get('openid_provider_id')
                                self.body['properties']['authenticationSettings']['openid']['openidProviderId'] = openid_pro
                            elif item == 'bearer_token_sending_methods' and kwargs[key]['openid'].get('bearer_token_sending_methods') is not None:
                                bearer_token = kwargs[key]['openid']['bearer_token_sending_methods']
                                self.body['properties']['authenticationSettings']['openid']['bearerTokenSendingMethods'] = bearer_token
                elif key == 'subscription_key_parameter_names':
                    self.body['properties']['subscriptionKeyParameterNames'] = kwargs[key]
                elif key == 'type':
                    self.body['properties']['type'] = kwargs[key]
                elif key == 'api_revision':
                    self.body['properties']['apiRevision'] = kwargs[key]
                elif key == 'api_version':
                    self.body['properties']['apiVersion'] = kwargs[key]
                elif key == 'is_current':
                    self.body['properties']['isCurrent'] = kwargs[key]
                elif key == 'api_revision_description':
                    self.body['properties']['apiRevisionDescription'] = kwargs[key]
                elif key == 'api_version_description':
                    self.body['properties']['apiVersionDescription'] = kwargs[key]
                elif key == 'api_version_set_id':
                    self.body['properties']['apiVersionSetId'] = kwargs[key]
                elif key == 'subscription_required':
                    self.body['properties']['subscriptionRequired'] = kwargs[key]
                elif key == 'source_api_id':
                    self.body['properties']['sourceApiId'] = kwargs[key]
                elif key == 'display_name':
                    self.body['properties']['displayName'] = kwargs[key]
                elif key == 'service_url':
                    self.body['properties']['serviceUrl'] = kwargs[key]
                elif key == 'protocols':
                    self.body['properties']['protocols'] = kwargs[key]
                elif key == 'api_version_set':
                    self.body['properties']['apiVersionSet'] = {}
                    for item in kwargs[key].keys():
                        if item == 'versioning_scheme':
                            self.body['properties']['apiVersionSet'] = kwargs[key].get('versioning_scheme')
                        elif item == 'version_query_name':
                            self.body['properties']['versionQueryName'] = kwargs[key].get('version_query_name')
                        elif item == 'version_header_name':
                            self.body['properties']['versionHeaderName'] = kwargs[key].get('version_header_name')
                        else:
                            self.body['properties'][item] = kwargs[key].get(item)
                elif key == 'wsdl_selector':
                    self.body['properties']['wsdlSelector'] = {}
                    for item in kwargs[key].keys():
                        if item == 'wsdl_service_name':
                            self.body['properties']['wsdlSelector']['wsdlServiceName'] = kwargs[key].get(item)
                        if item == 'wsdl_endpoint_name':
                            self.body['properties']['wsdlSelector']['wsdlEndpointName'] = kwargs[key].get(item)
                elif key == 'api_type':
                    self.body['properties']['apiType'] = kwargs[key]
                else:
                    self.body['properties'][key] = kwargs[key]

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
                if self.body['properties'].get('description') is not None and \
                   self.body['properties']['description'] != old_response['properties']['description']:
                    self.to_do = Actions.Update
                elif self.body['properties'].get('authenticationSettings') is not None:
                    if old_response['properties'].get('authenticationSettings') is None:
                        self.to_do = Actions.Update
                    elif (self.body['properties']['authenticationSettings'].get('oAuth2') is not None and
                          self.body['properties']['authenticationSettings']['oAuth2'] != old_response['properties']['authenticationSettings'].get('oAuth2')):
                        self.to_do = Actions.Update
                    elif (self.body['properties']['authenticationSettings'].get('openid') is not None and
                          self.body['properties']['authenticationSettings']['openid'] != old_response['properties']['authenticationSettings'].get('openid')):
                        self.to_do = Actions.Update
                elif self.body['properties'].get('subscriptionKeyParameterNames') is not None:
                    tt = old_response['properties']
                    if old_response['properties'].get('subscriptionKeyParameterNames') is None:
                        self.to_do = Actions.Update
                    elif (not all(self.body['properties']['subscriptionKeyParameterNames'].get(item) == tt['subscriptionKeyParameterNames'].get(item)
                          for item in self.body['properties']['subscriptionKeyParameterNames'].keys())):
                        self.to_do = Actions.Update
                elif (self.body['properties'].get('apiRevision') is not None and
                      self.body['properties']['apiRevision'] != old_response['properties'].get('apiRevision')):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('apiVersion') is not None and
                      self.body['properties']['apiVersion'] != old_response['properties'].get('apiVersion')):
                    self.to_do == Actions.Update
                elif (self.body['properties'].get('isCurrent') is not None and
                      self.body['properties']['isCurrent'] != old_response['properties'].get('isCurrent')):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('apiRevisionDescription') is not None and self.body['properties']['apiRevisionDescription'] !=
                      old_response['properties'].get('apiRevisionDescription')):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('apiVersionDescription') is not None and
                      self.body['properties']['apiVersionDescription'] != old_response['properties'].get('apiVersionDescription')):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('apiVersionSetId') is not None and
                      self.body['properties']['apiVersionSetId'] != old_response['properties'].get('apiVersionSetId')):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('subscriptionRequired') is not None and
                      self.body['properties']['subscriptionRequired'] != old_response['properties'].get('subscriptionRequired')):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('sourceApiId') is not None and
                      self.body['properties']['sourceApiId'] != old_response['properties'].get('sourceApiId')):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('displayName') is not None and
                      self.body['properties']['displayName'] != old_response['properties'].get('displayName')):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('serviceUrl') is not None and
                      self.body['properties']['serviceUrl'] != old_response['properties'].get('serviceUrl')):
                    self.to_do = Actions.Update
                elif self.body['properties'].get('path') is not None and self.body['properties']['path'] != old_response['properties'].get('path'):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('protocols') is not None and
                      self.body['properties']['protocols'] != old_response['properties'].get('protocols')):
                    self.to_do = Actions.Update
                elif self.body['properties'].get('type') is not None and self.body['properties']['type'] != old_response['properties'].get('type'):
                    self.to_do = Actions.Update
                elif self.body['properties'].get('apiType') is not None and self.body['properties']['apiType'] != old_response['properties'].get('apiType'):
                    self.to_do = Actions.Update
                elif self.body['properties'].get('value') is not None and self.body['properties']['value'] != old_response['properties'].get('value'):
                    self.to_do = Actions.Update
                elif self.body['properties'].get('format') is not None and self.body['properties']['format'] != old_response['properties'].get('format'):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('wsdlSelector') is not None and
                      not all(self.body['properties']['wsdlSelector'][item] == old_response['properties']['wsdlSelector'].get(item)
                      for item in self.body['properties']['wsdlSelector'].keys())):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('apiVersionSet') is not None and
                      not all(self.body['properties']['apiVersionSet'][item] == old_response['properties']['apiVersionSet'].get(item)
                      for item in self.body['properties']['apiVersionSet'].keys())):
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
        except Exception as exc:
            self.log('Error while creating/updating the Api instance.')
            self.fail('Error creating the Api instance: {0}'.format(str(exc)))
        if hasattr(response, 'body'):
            response = json.loads(response.body())
        elif hasattr(response, 'context'):
            response = response.context['deserialized_data']
        else:
            self.fail("Create or Updating fail, no match message return, return info as {0}".format(response))

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
        except Exception as e:
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
            response = json.loads(response.body())
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.log('Could not find the Api instance from the given parameters.')
        if isFound is True:
            return response
        return False


def main():
    AzureApiManagement()


if __name__ == '__main__':
    main()
