#!/usr/bin/python
#
# Copyright (c) 2019 Zim Kalinowski, (@zikalino)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_galleryimage
version_added: "0.1.2"
short_description: Manage Azure SIG Image instance
description:
    - Create, update and delete instance of Azure SIG Image.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    gallery_name:
        description:
            - The name of the Shared Image Gallery in which the Image Definition is to be created.
        required: true
        type: str
    name:
        description:
            - The name of the gallery Image Definition to be created or updated.
            - The allowed characters are alphabets and numbers with dots, dashes, and periods allowed in the middle.
            - The maximum length is 80 characters.
        required: true
        type: str
    location:
        description:
            - Resource location.
        type: str
    description:
        description:
            - The description of this gallery Image Definition resource. This property is updatable.
        type: str
    eula:
        description:
            - The Eula agreement for the gallery Image Definition.
        type: str
    privacy_statement_uri:
        description:
            - The privacy statement uri.
        type: str
    release_note_uri:
        description:
            - The release note uri.
        type: str
    os_type:
        description:
            - This property allows you to specify the type of the OS that is included in the disk when creating a VM from a managed image.
            - Required when creating.
        choices:
            - windows
            - linux
            - Windows
            - Linux
        type: str
    os_state:
        description:
            - The allowed values for OS State are C(generalized).
            - Required when creating.
        choices:
            - generalized
            - specialized
        type: str
    hypervgeneration:
        description:
            - This property allows you to specify the Hyper V Version of the Virtual Machines.
        choices:
            - V1
            - V2
        type: str
    architecture:
        description:
            - This property allows you to specify the hardware architecture of the Virtual Machines.
            - Arm64 is only supported with Hyper V Version 2.
        choices:
            - Arm64
            - x64
        type: str
    end_of_life_date:
        description:
            - The end of life date of the gallery Image Definition.
            - This property can be used for decommissioning purposes.
            - This property is updatable.
            - Format should be according to ISO-8601, for instance "2019-06-26".
        type: str
    identifier:
        description:
            - Image identifier.
            - Required when creating.
        type: dict
        suboptions:
            publisher:
                description:
                    - The name of the gallery Image Definition publisher.
                required: true
                type: str
            offer:
                 description:
                     - The name of the gallery Image Definition offer.
                 required: true
                 type: str
            sku:
                description:
                    - The name of the gallery Image Definition SKU.
                required: true
                type: str
    recommended:
        description:
            - Recommended parameter values.
        type: dict
        suboptions:
            v_cpus:
                description:
                    - Number of virtual CPUs.
                type: dict
                suboptions:
                    min:
                        description:
                            - The minimum number of the resource.
                        type: int
                    max:
                        description:
                            - The maximum number of the resource.
                        type: int
            memory:
                description:
                    - Memory.
                type: dict
                suboptions:
                    min:
                        description:
                            - The minimum number of the resource.
                        type: int
                    max:
                        description:
                            - The maximum number of the resource.
                        type: int
    disallowed:
        description:
            - Disallowed parameter values.
        type: dict
        suboptions:
            disk_types:
                description:
                    - A list of disallowed disk types.
                type: list
                elements: str
    purchase_plan:
        description:
            - Purchase plan.
        type: dict
        suboptions:
            name:
                description:
                    - The plan ID.
                type: str
            publisher:
                description:
                    - The publisher ID.
                type: str
            product:
                description:
                    - The product ID.
                type: str
    features:
        description:
            - A list of gallery image features.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of the gallery image feature.
                type: str
                required: True
            value:
                description:
                    - The value of the gallery image feature.
                type: str
                required: True
    state:
        description:
            - Assert the state of the GalleryImage.
            - Use C(present) to create or update an GalleryImage and C(absent) to delete it.
        default: present
        choices:
            - absent
            - present
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
  - Zim Kalinowski (@zikalino)

'''

EXAMPLES = '''
- name: Create or update gallery image
  azure_rm_galleryimage:
    resource_group: myResourceGroup
    gallery_name: myGallery1283
    name: myImage
    location: West US
    os_type: linux
    os_state: generalized
    identifier:
      publisher: myPublisherName
      offer: myOfferName
      sku: mySkuName
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Compute/galleries/myGalle
           ry1283/images/myImage"
'''

import time
import json
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMGalleryImages(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            gallery_name=dict(
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
            description=dict(
                type='str',
            ),
            eula=dict(
                type='str',
            ),
            privacy_statement_uri=dict(
                type='str',
            ),
            release_note_uri=dict(
                type='str',
            ),
            os_type=dict(
                type='str',
                choices=['windows', 'Windows',
                         'Linux', 'linux']
            ),
            os_state=dict(
                type='str',
                choices=['generalized',
                         'specialized']
            ),
            hypervgeneration=dict(
                type='str',
                choices=['V1',
                         'V2']
            ),
            architecture=dict(
                type='str',
                choices=['Arm64',
                         'x64']
            ),
            end_of_life_date=dict(
                type='str',
            ),
            identifier=dict(
                type='dict',
                options=dict(
                    publisher=dict(
                        type='str',
                        required=True,
                    ),
                    offer=dict(
                        type='str',
                        required=True
                    ),
                    sku=dict(
                        type='str',
                        required=True
                    )
                )
            ),
            recommended=dict(
                type='dict',
                options=dict(
                    v_cpus=dict(
                        type='dict',
                        options=dict(
                            min=dict(
                                type='int'
                            ),
                            max=dict(
                                type='int'
                            )
                        )
                    ),
                    memory=dict(
                        type='dict',
                        options=dict(
                            min=dict(
                                type='int'
                            ),
                            max=dict(
                                type='int'
                            )
                        )
                    )
                )
            ),
            disallowed=dict(
                type='dict',
                options=dict(
                    disk_types=dict(
                        type='list',
                        elements='str',
                    )
                )
            ),
            purchase_plan=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    publisher=dict(
                        type='str'
                    ),
                    product=dict(
                        type='str'
                    )
                )
            ),
            features=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(
                        type='str',
                        required=True
                    ),
                    value=dict(
                        type='str',
                        required=True
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.gallery_name = None
        self.name = None
        self.gallery_image = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200, 201, 202]
        self.to_do = Actions.NoAction

        self.body = {}
        self.body['properties'] = {}
        self.query_parameters = {}
        self.query_parameters['api-version'] = '2022-03-03'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(AzureRMGalleryImages, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == 'description':
                    self.body['properties']['description'] = kwargs[key]
                elif key == 'eula':
                    self.body['properties']['eula'] = kwargs[key]
                elif key == 'privacy_statement_uri':
                    self.body['properties']['privacyStatementUri'] = kwargs[key]
                elif key == 'release_note_uri':
                    self.body['properties']['releaseNoteUri'] = kwargs[key]
                elif key == 'os_type':
                    self.body['properties']['osType'] = kwargs[key]
                elif key == 'os_state':
                    self.body['properties']['osState'] = kwargs[key]
                elif key == 'hypervgeneration':
                    self.body['properties']['hyperVGeneration'] = kwargs[key]
                elif key == 'architecture':
                    self.body['properties']['architecture'] = kwargs[key]
                elif key == 'end_of_life_date':
                    self.body['properties']['endOfLifeDate'] = kwargs[key]
                elif key == 'identifier':
                    self.body['properties']['identifier'] = kwargs[key]
                elif key == 'recommended':
                    self.body['properties']['recommended'] = {}
                    for item in kwargs[key].keys():
                        if item == 'v_cpus':
                            self.body['properties']['recommended']['vCPUs'] = kwargs[key].get('v_cpus')
                        elif item == 'memory':
                            self.body['properties']['recommended']['memory'] = kwargs[key].get('memory')
                elif key == 'disallowed':
                    self.body['properties']['disallowed'] = {}
                    self.body['properties']['disallowed']['diskTypes'] = kwargs[key].get('disk_types')
                elif key == 'purchase_plan':
                    self.body['properties']['purchasePlan'] = kwargs[key]
                elif key == 'features':
                    self.body['properties']['features'] = kwargs[key]
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
                    '/{{ gallery_name }}' +
                    '/images' +
                    '/{{ image_name }}')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)
        self.url = self.url.replace('{{ resource_group }}', self.resource_group)
        self.url = self.url.replace('{{ gallery_name }}', self.gallery_name)
        self.url = self.url.replace('{{ image_name }}', self.name)

        old_response = self.get_resource()

        if not old_response:
            self.log("GalleryImage instance doesn't exist")

            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log('GalleryImage instance already exists')

            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                if self.body['properties'].get('description') is not None and \
                   self.body['properties']['description'] != old_response['properties'].get('description'):
                    self.to_do = Actions.Update
                elif self.body['properties'].get('eula') is not None and self.body['properties']['eula'] != old_response['properties'].get('eula'):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('privacyStatementUri') is not None and
                      self.body['properties']['privacyStatementUri'] != old_response['properties'].get('privacyStatementUri')):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('releaseNoteUri') is not None and
                      self.body['properties']['releaseNoteUri'] != old_response['properties'].get('releaseNoteUri')):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('osType') is not None and
                      self.body['properties']['osType'].lower() != old_response['properties'].get('osType', '').lower()):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('osState') is not None and
                      self.body['properties']['osState'].lower() != old_response['properties'].get('osState', '').lower()):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('hyperVGeneration') is not None and
                      self.body['properties']['hyperVGeneration'] != old_response['properties'].get('hyperVGeneration')):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('architecture') is not None and
                      self.body['properties']['architecture'] != old_response['properties'].get('architecture')):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('endOfLifeDate') is not None and
                      self.body['properties']['endOfLifeDate'] != old_response['properties'].get('endOfLifeDate')):
                    self.to_do = Actions.Update
                elif (self.body['properties'].get('identifier') is not None and
                      self.body['properties']['identifier'].get('offer') != old_response['properties']['identifier'].get('offer') or
                      self.body['properties']['identifier'].get('sku') != old_response['properties']['identifier'].get('sku')):
                    self.to_do = Actions.Update
                elif self.body['properties'].get('recommended') is not None:
                    if self.body['properties']['recommended'].get('vCPUS') is not None:
                        for item in self.body['properties']['recommended']['vCPUS'].keys():
                            if self.body['properties']['recommended']['vCPUS'].get(item) != old_response['properties']['recommended']['vCPUS'].get(item):
                                self.to_do = Actions.Update
                    elif (self.body['properties']['recommended'].get('memory') is not None and
                          not all(self.body['properties']['recommended']['memory'].get(item) == old_response['properties']['recommended']['memory'].get(item)
                          for item in self.body['properties']['recommended']['memory'].keys())):
                        self.to_do = Actions.Update
                elif (self.body['properties'].get('disallowed') is not None and
                      self.body['properties']['disallowed'].get('diskTypes') != old_response['properties']['disallowed'].get('diskTypes')):
                    self.to_do = Actions.Update
                elif self.body['properties'].get('purchasePlan') is not None:
                    for item in self.body['properties']['purchasePlan'].keys():
                        if self.body['properties']['purchasePlan'][item] != old_response['properties']['purchasePlan'].get(item):
                            self.to_do = Actions.Update
                elif self.body['properties'].get('features') is not None:
                    if old_response['properties'].get('features') is None:
                        self.to_do = Actions.Update
                    else:
                        if not all(item in old_response['properties']['features'] for item in self.body['properties']['features']):
                            self.to_do = Actions.Update
                update_tags, self.body['tags'] = self.update_tags(old_response.get('tags'))
                if update_tags:
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log('Need to Create / Update the GalleryImage instance')

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
            self.log('GalleryImage instance deleted')
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_resource()

            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_resource():
                time.sleep(20)
        else:
            self.log('GalleryImage instance unchanged')
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]

        return self.results

    def create_update_resource(self):
        # self.log('Creating / Updating the GalleryImage instance {0}'.format(self.))

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
            self.log('Error attempting to create the GalleryImage instance.')
            self.fail('Error creating the GalleryImage instance: {0}'.format(str(exc)))

        if hasattr(response, 'body'):
            response = json.loads(response.body())
        elif hasattr(response, 'context'):
            response = response.context['deserialized_data']
        else:
            self.fail("Create or Updating fail, no match message return, return info as {0}".format(response))

        return response

    def delete_resource(self):
        # self.log('Deleting the GalleryImage instance {0}'.format(self.))
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
            self.log('Error attempting to delete the GalleryImage instance.')
            self.fail('Error deleting the GalleryImage instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        # self.log('Checking if the GalleryImage instance {0} is present'.format(self.))
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
    AzureRMGalleryImages()


if __name__ == '__main__':
    main()
