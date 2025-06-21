#!/usr/bin/python
#
# Copyright (c) 2019 Zim Kalinowski, (@zikalino)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_gallery
version_added: "0.1.2"
short_description: Manage Azure Shared Image Gallery instance
description:
    - Create, update and delete instance of Azure Shared Image Gallery (SIG).
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - The name of the Shared Image Gallery.
            - Valid names consist of less than 80 alphanumeric characters, underscores and periods.
        required: true
        type: str
    location:
        description:
            - Resource location.
        type: str
    description:
        description:
            - The description of this Shared Image Gallery resource. This property is updatable.
        type: str
    state:
        description:
            - Assert the state of the Gallery.
            - Use C(present) to create or update an Gallery and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Zim Kalinowski (@zikalino)

'''

EXAMPLES = '''
- name: Create or update a simple gallery.
  azure_rm_gallery:
    resource_group: myResourceGroup
    name: myGallery1283
    location: West US
    description: This is the gallery description.
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Compute/galleries/myGallery1283"
'''

import time
import json
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMGalleries(AzureRMModuleBaseExt):
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
                type='str'
            ),
            description=dict(
                type='str',
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.gallery = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200, 201, 202]
        self.to_do = Actions.NoAction

        self.body = {}
        self.body['properties'] = {}
        self.query_parameters = {}
        self.query_parameters['api-version'] = '2019-07-01'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(AzureRMGalleries, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == 'description':
                    self.body['properties']['description'] = kwargs[key]
                else:
                    self.body[key] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if 'location' not in self.body:
            self.body['location'] = resource_group.location

        self.url = ('/subscriptions' +
                    '/{{ subscription_id }}' +
                    '/resourceGroups' +
                    '/{{ resource_group }}' +
                    '/providers' +
                    '/Microsoft.Compute' +
                    '/galleries' +
                    '/{{ gallery_name }}')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)
        self.url = self.url.replace('{{ resource_group }}', self.resource_group)
        self.url = self.url.replace('{{ gallery_name }}', self.name)

        old_response = self.get_resource()

        if not old_response:
            self.log("Gallery instance doesn't exist")

            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log('Gallery instance already exists')

            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                if self.body['properties'].get('description') is not None and\
                   self.body['properties']['description'] != old_response['properties'].get('description'):
                    self.to_do = Actions.Update
                else:
                    self.body['properties']['description'] = old_response['properties'].get('description')

                update_tags, new_tags = self.update_tags(old_response.get('tags'))
                if update_tags:
                    self.to_do = Actions.Update
                    self.body['tags'] = new_tags

        if self.to_do == Actions.Create:
            self.log('Need to Create the Gallery instance')
            if self.check_mode:
                self.results['changed'] = True
                return self.results
            response = self.create_resource()
            # if not old_response:
            self.results['changed'] = True
            # else:
            #     self.results['changed'] = old_response.__ne__(response)
            self.log('Creation done')
        elif self.to_do == Actions.Update:
            self.log('Need to Update the Gallery instance')
            if self.check_mode:
                self.results['changed'] = True
                return self.results
            response = self.update_resource()
            # if not old_response:
            self.results['changed'] = True
            self.log('Update done')
        elif self.to_do == Actions.Delete:
            self.log('Gallery instance deleted')
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_resource()

            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_resource():
                time.sleep(20)
        else:
            self.log('Gallery instance unchanged')
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]

        return self.results

    def update_resource(self):
        # self.log('Updating the Gallery instance {0}'.format(self.))

        try:
            response = self.mgmt_client.query(self.url,
                                              'PATCH',
                                              self.query_parameters,
                                              self.header_parameters,
                                              self.body,
                                              self.status_code,
                                              600,
                                              30)
        except Exception as exc:
            self.log('Error attempting to update the Gallery instance.')
            self.fail('Error updating the Gallery instance: {0}'.format(str(exc)))

        if hasattr(response, 'body'):
            response = json.loads(response.body())
        elif hasattr(response, 'context'):
            response = response.context['deserialized_data']
        else:
            self.fail("Updating fail, no match message return, return info as {0}".format(response))

        return response

    def create_resource(self):
        # self.log('Creating the Gallery instance {0}'.format(self.))

        try:
            response = self.mgmt_client.query(self.url,
                                              'PUT',
                                              self.query_parameters,
                                              self.header_parameters,
                                              self.body,
                                              self.status_code,
                                              600,
                                              30)
        except Exception as exc:
            self.log('Error attempting to create the Gallery instance.')
            self.fail('Error creating the Gallery instance: {0}'.format(str(exc)))

        if hasattr(response, 'body'):
            response = json.loads(response.body())
        elif hasattr(response, 'context'):
            response = response.context['deserialized_data']
        else:
            self.fail("Create fail, no match message return, return info as {0}".format(response))

        return response

    def delete_resource(self):
        # self.log('Deleting the Gallery instance {0}'.format(self.))
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
            self.log('Error attempting to delete the Gallery instance.')
            self.fail('Error deleting the Gallery instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        # self.log('Checking if the Gallery instance {0} is present'.format(self.))
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
            response = json.loads(response.body())
            found = True
            self.log("Response : {0}".format(response))
            # self.log("AzureFirewall instance : {0} found".format(response.name))
        except Exception as e:
            self.log('Did not find the AzureFirewall instance.')
        if found is True:
            return response

        return False


def main():
    AzureRMGalleries()


if __name__ == '__main__':
    main()
