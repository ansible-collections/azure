#!/usr/bin/python
#
# Copyright (c) 2020 Nikhil Patne (@nikhilpatne), Sakar Mehra (@sakar97)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_apimanagementservice
version_added: '1.5.0'
short_description: Manage Azure ApiManagementService instance
description:
    - Create and delete instance of Azure ApiManagementService.
    - Updates are not currently supported, this feature should be added in a later release.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - Service name.
        required: true
        type: str
    location:
        description:
            - Location of the Api management service.
        type: str
    publisher_name:
        description:
            - Publisher name.
        type: str
    publisher_email:
        description:
            - Publisher email.
        type: str
    sku_name:
        description:
            - Name of the Sku.
        choices:
            - Developer
            - Standard
            - Premium
            - Basic
            - Consumption
        type: str
    sku_capacity:
        description:
            - Capacity of the SKU (number of deployed units of the SKU).
        type: int
    state:
        description:
            - Assert the state of the ApiManagementService.
            - Use C(present) to create or update an ApiManagementService.
            - Use C(absent) to delete an ApiManagementService.
        type: str
        default: present
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Nikhil Patne (@nikhilpatne)
    - Sakar Mehra (@sakar97)
'''

EXAMPLES = '''
- name: Create Api Management Service
  azure_rm_apimanagementservice:
    resource_group: myResourceGroup
    name: myService
    publisher_email: user@example.com
    publisher_name: Publisher Name
    sku_name: Developer
    sku_capacity: 1

- name: Delete Api Management Service
  azure_rm_apimanagementservice:
    resource_group: myResourceGroup
    name: myService
    state: absent
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: null
'''

import time
import json
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMApiManagementService(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
            ),
            publisher_name=dict(
                type='str',
            ),
            publisher_email=dict(
                type='str',
            ),
            sku_name=dict(
                type='str',
                choices=['Developer',
                         'Standard',
                         'Premium',
                         'Basic',
                         'Consumption']
            ),
            sku_capacity=dict(
                type='int',
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.location = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200, 201, 202]
        self.to_do = Actions.NoAction

        self.body = {}
        self.body['properties'] = {}
        self.body['sku'] = {}
        self.query_parameters = {}
        self.query_parameters['api-version'] = '2022-08-01'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(AzureRMApiManagementService, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == 'publisher_name':
                    self.body['properties']['publisherName'] = kwargs[key]
                elif key == 'publisher_email':
                    self.body['properties']['publisherEmail'] = kwargs[key]
                elif key == 'sku_name':
                    self.body['sku']['name'] = kwargs[key]
                elif key == 'sku_capacity':
                    self.body['sku']['capacity'] = kwargs[key]
                else:
                    self.body[key] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if self.location is None:
            self.location = resource_group.location

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

        old_response = self.get_resource()

        if not old_response:
            self.log("ApiManagementService instance doesn't exist")

            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log('ApiManagementService instance already exists')

            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                for key in self.body.keys():
                    if key == 'properties':
                        for key in self.body['properties'].keys():
                            if self.body['properties'][key] != old_response['properties'].get(key):
                                self.to_do = Actions.Update
                    elif key == 'sku':
                        for key in self.body['sku'].keys():
                            if self.body['sku'][key] != old_response['sku'].get(key):
                                self.to_do = Actions.Update

        self.body['location'] = self.location
        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log('Need to Create / Update the ApiManagementService instance')

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_resource()

            # if not old_response:
            self.results['changed'] = True
            # else:
            #     self.results['changed'] = old_response.__ne__(response)
            self.log('Creation / Update done')
        elif self.to_do == Actions.Delete:
            self.log('To delete ApiManagementService instance')
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_resource()

            # make sure instance is actually deleted, for some Azure resources, instance is hanging around.
            while self.get_resource():
                time.sleep(20)
        else:
            self.log('ApiManagementService instance unchanged')
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]

        return self.results

    def create_update_resource(self):
        # Creating / Updating the ApiManagementService instance.
        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.query(self.url,
                                                  'PUT',
                                                  self.query_parameters,
                                                  self.header_parameters,
                                                  self.body,
                                                  self.status_code,
                                                  600,
                                                  30)
            else:
                response = self.mgmt_client.query(self.url,
                                                  'PATCH',
                                                  self.query_parameters,
                                                  self.header_parameters,
                                                  self.body,
                                                  self.status_code,
                                                  600,
                                                  30)
        except Exception as exc:
            self.log('Error attempting to create the ApiManagementService instance.')
            self.fail('Error creating the ApiManagementService instance: {0}'.format(str(exc)))

        if hasattr(response, 'body'):
            response = json.loads(response.body())
        elif hasattr(response, 'context'):
            response = response.context['deserialized_data']
        else:
            self.fail("Create or Updating fail, no match message return, return info as {0}".format(response))

        return response

    def delete_resource(self):
        # Deleting the ApiManagementService instance.
        try:
            response = self.mgmt_client.query(self.url,
                                              'DELETE',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
        except Exception as e:
            self.log('Error attempting to delete the ApiManagementService instance.')
            self.fail('Error deleting the ApiManagementService instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        # Checking if the ApiManagementService instance is present
        found = False
        try:
            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            found = True
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.log('Did not find the ApiManagementService instance.')
        if found is True:
            return json.loads(response.body())

        return False


def main():
    AzureRMApiManagementService()


if __name__ == '__main__':
    main()
