#!/usr/bin/python
#
# Copyright (c) 2019 Zim Kalinowski, (@zikalino)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_galleryimageversion
version_added: "0.1.2"
short_description: Manage Azure SIG Image Version instance
description:
    - Create, update and delete instance of Azure SIG Image Version.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    gallery_name:
        description:
            - The name of the Shared Image Gallery in which the Image Definition resides.
        required: true
        type: str
    gallery_image_name:
        description:
            - The name of the gallery Image Definition in which the Image Version is to be created.
        required: true
        type: str
    name:
        description:
            - The name of the gallery Image Version to be created.
            - Needs to follow semantic version name pattern, The allowed characters are digit and period.
            - Digits must be within the range of a 32-bit integer. For example <MajorVersion>.<MinorVersion>.<Patch>.
        required: true
        type: str
    location:
        description:
            - Resource location.
        type: str
    storage_profile:
        description:
            - Storage profile
        required: true
        type: dict
        suboptions:
            source_image:
                description:
                    - Reference to managed image or gallery image version
                    - Could be resource ID to managed image, or dictionary containing I(resource_group) and I(name)
                    - Could be resource ID to image version, or dictionary containing I(resource_group),I(gallery_name), I(gallery_image_name) and I(version)
                    - Mutual exclusive with os_disk and data_disks
                type: raw
            os_disk:
                description:
                    - os disk snapshot
                    - Mutual exclusive with source_image
                type: raw
                suboptions:
                    source:
                        description:
                            - Reference to os disk snapshot. Could be resource ID or dictionary containing I(resource_group) and I(name)
                        type: str
                    host_caching:
                        description:
                            - host disk caching
                        type: str
                        default: None
                        choices:
                            - None
                            - ReadOnly
                            - ReadWrite
            data_disks:
                description:
                    - list of data disk snapshot
                    - Mutual exclusive with source_image
                type: list
                suboptions:
                    source:
                        description:
                            - Reference to data disk snapshot. Could be resource ID or dictionary containing I(resource_group) and I(name)
                        type: str
                    lun:
                        description:
                            - lun of the data disk
                        type: int
                    host_caching:
                        description:
                            - host disk caching
                        type: str
                        default: None
                        choices:
                            - None
                            - ReadOnly
                            - ReadWrite
    publishing_profile:
        description:
            - Publishing profile.
        required: true
        type: dict
        suboptions:
            target_regions:
                description:
                    - The target regions where the Image Version is going to be replicated to.
                    - This property is updatable.
                type: list
                suboptions:
                    name:
                        description:
                            - Region name.
                        type: str
                    regional_replica_count:
                        description:
                            - The number of replicas of the Image Version to be created per region.
                            - This property would take effect for a region when regionalReplicaCount is not specified.
                            - This property is updatable.
                        type: str
                    storage_account_type:
                        description:
                            - Storage account type.
                        type: str
            managed_image:
                description:
                    - Managed image reference, could be resource ID, or dictionary containing I(resource_group) and I(name)
                    - Obsolete since 2.10, use storage_profile instead
            snapshot:
                description:
                    - Source snapshot to be used.
                    - Obsolete since 2.10, use storage_profile instead
            replica_count:
                description:
                    - The number of replicas of the Image Version to be created per region.
                    - This property would take effect for a region when regionalReplicaCount is not specified.
                    - This property is updatable.
                type: int
            exclude_from_latest:
                description:
                    If I(exclude_from_latest=true), Virtual Machines deployed from the latest version of the Image Definition won't use this Image Version.
                type: bool
            end_of_life_date:
                description:
                    - The end of life date of the gallery Image Version.
                    - This property can be used for decommissioning purposes.
                    - This property is updatable. Format should be according to ISO-8601, for instance "2019-06-26".
                type: str
            storage_account_type:
                description:
                    - Specifies the storage account type to be used to store the image.
                    - This property is not updatable.
                type: str
    state:
        description:
            - Assert the state of the GalleryImageVersion.
            - Use C(present) to create or update an GalleryImageVersion and C(absent) to delete it.
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
- name: Create a gallery image version form a managed image
  azure_rm_galleryimageversion:
    resource_group: myResourceGroup
    gallery_name: myGallery
    gallery_image_name: myGalleryImage
    name: 1.1.0
    location: East US
    publishing_profile:
      end_of_life_date: "2020-10-01t00:00:00+00:00"
      exclude_from_latest: yes
      replica_count: 4
      storage_account_type: Standard_LRS
      target_regions:
        - name: West US
          regional_replica_count: 1
        - name: East US
          regional_replica_count: 3
          storage_account_type: Standard_LRS
    storage_profile:
        source_image: /subscriptions/sub123/resourceGroups/group123/providers/Microsoft.Compute/images/myOsImage

- name: Create a gallery image version from another gallery image version
  azure_rm_galleryimageversion:
    resource_group: myResourceGroup
    gallery_name: myGallery
    gallery_image_name: myGalleryImage
    name: 1.2.0
    location: East US
    publishing_profile:
      end_of_life_date: "2020-10-01t00:00:00+00:00"
      exclude_from_latest: yes
      replica_count: 4
      storage_account_type: Standard_LRS
      target_regions:
        - name: West US
          regional_replica_count: 1
        - name: East US
          regional_replica_count: 3
          storage_account_type: Standard_LRS
    storage_profile:
        source_image:
            version: 1.1.0
            gallery_name: myGallery2
            gallery_image_name: myGalleryImage2

- name: Create gallery image by using one os dist snapshot and zero or many data disk snapshots
  azure_rm_galleryimageversion:
    resource_group: myRsourceGroup
    gallery_name: myGallery
    gallery_image_name: myGalleryImage
    name: 3.4.0
    location: East  US
    publishing_profile:
      end_of_life_date: "2020-10-01t00:00:00+00:00"
      exclude_from_latest: yes
      replica_count: 1
      storage_account_type: Standard_LRS
      target_regions:
        - name: East US
          regional_replica_count: 1
          storage_account_type: Standard_LRS
    storage_profile:
      os_disk:
          source: "/subscriptions/mySub/resourceGroups/myGroup/providers/Microsoft.Compute/snapshots/os_snapshot_vma"
      data_disks:
          - lun: 0
            source:
              name: data_snapshot_vma
          - lun: 1
            source: "/subscriptions/mySub/resourceGroups/myGroup/providers/Microsoft.Compute/snapshots/data_snapshot_vmb"
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Compute/galleries/myGalle
           ry1283/images/myImage/versions/10.1.3"
'''

import time
import json
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient
try:
    from msrestazure.azure_exceptions import CloudError
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMGalleryImageVersions(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                updatable=False,
                disposition='resourceGroupName',
                required=True
            ),
            gallery_name=dict(
                type='str',
                updatable=False,
                disposition='galleryName',
                required=True
            ),
            gallery_image_name=dict(
                type='str',
                updatable=False,
                disposition='galleryImageName',
                required=True
            ),
            name=dict(
                type='str',
                updatable=False,
                disposition='galleryImageVersionName',
                required=True
            ),
            tags=dict(
                type='dict',
                updatable=False,
                disposition='tags',
                comparison='tags'
            ),
            location=dict(
                type='str',
                updatable=False,
                disposition='/',
                comparison='location'
            ),
            storage_profile=dict(
                type='dict',
                updatable=False,
                disposition='/properties/storageProfile',
                comparison='ignore',
                options=dict(
                    source_image=dict(
                        type='raw',
                        disposition='source/id',
                        purgeIfNone=True,
                        pattern=[('/subscriptions/{subscription_id}/resourceGroups'
                                  '/{resource_group}/providers/Microsoft.Compute'
                                  '/images/{name}'),
                                 ('/subscriptions/{subscription_id}/resourceGroups'
                                  '/{resource_group}/providers/Microsoft.Compute'
                                  '/galleries/{gallery_name}/images/{gallery_image_name}'
                                  '/versions/{version}')]
                    ),
                    os_disk=dict(
                        type='dict',
                        disposition='osDiskImage',
                        purgeIfNone=True,
                        comparison='ignore',
                        options=dict(
                            source=dict(
                                type='raw',
                                disposition='source/id',
                                pattern=('/subscriptions/{subscription_id}/resourceGroups'
                                         '/{resource_group}/providers/Microsoft.Compute'
                                         '/snapshots/{name}')
                            ),
                            host_caching=dict(
                                type='str',
                                disposition='hostCaching',
                                default="None",
                                choices=["ReadOnly", "ReadWrite", "None"]
                            )
                        )
                    ),
                    data_disks=dict(
                        type='list',
                        disposition='dataDiskImages',
                        purgeIfNone=True,
                        options=dict(
                            lun=dict(
                                type='int'
                            ),
                            source=dict(
                                type='raw',
                                disposition="source/id",
                                pattern=('/subscriptions/{subscription_id}/resourceGroups'
                                         '/{resource_group}/providers/Microsoft.Compute'
                                         '/snapshots/{name}')
                            ),
                            host_caching=dict(
                                type='str',
                                disposition='hostCaching',
                                default="None",
                                choices=["ReadOnly", "ReadWrite", "None"]
                            )
                        )
                    )
                )
            ),
            publishing_profile=dict(
                type='dict',
                disposition='/properties/publishingProfile',
                options=dict(
                    target_regions=dict(
                        type='list',
                        disposition='targetRegions',
                        options=dict(
                            name=dict(
                                type='str',
                                required=True,
                                comparison='location'
                            ),
                            regional_replica_count=dict(
                                type='int',
                                disposition='regionalReplicaCount'
                            ),
                            storage_account_type=dict(
                                type='str',
                                disposition='storageAccountType'
                            )
                        )
                    ),
                    managed_image=dict(
                        type='raw',
                        pattern=('/subscriptions/{subscription_id}/resourceGroups'
                                 '/{resource_group}/providers/Microsoft.Compute'
                                 '/images/{name}'),
                        comparison='ignore'
                    ),
                    snapshot=dict(
                        type='raw',
                        pattern=('/subscriptions/{subscription_id}/resourceGroups'
                                 '/{resource_group}/providers/Microsoft.Compute'
                                 '/snapshots/{name}'),
                        comparison='ignore'
                    ),
                    replica_count=dict(
                        type='int',
                        disposition='replicaCount'
                    ),
                    exclude_from_latest=dict(
                        type='bool',
                        disposition='excludeFromLatest'
                    ),
                    end_of_life_date=dict(
                        type='str',
                        disposition='endOfLifeDate'
                    ),
                    storage_account_type=dict(
                        type='str',
                        disposition='storageAccountType',
                        choices=['Standard_LRS',
                                 'Standard_ZRS']
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
        self.gallery_image_name = None
        self.name = None
        self.gallery_image_version = None
        self.tags = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200, 201, 202]
        self.to_do = Actions.NoAction

        self.body = {}
        self.query_parameters = {}
        self.query_parameters['api-version'] = '2019-07-01'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(AzureRMGalleryImageVersions, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
                if key == 'tags':
                    self.body[key] = kwargs[key]
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_parameters(self.module_arg_spec, self.body, 0)

        # keep backward compatibility
        snapshot = self.body.get('properties', {}).get('publishingProfile', {}).pop('snapshot', None)
        if snapshot is not None:
            self.body['properties'].setdefault('storageProfile', {}).setdefault('osDiskImage', {}).setdefault('source', {})['id'] = snapshot
        managed_image = self.body.get('properties', {}).get('publishingProfile', {}).pop('managed_image', None)
        if managed_image:
            self.body['properties'].setdefault('storageProfile', {}).setdefault('source', {})['id'] = managed_image

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
                    '/{{ image_name }}' +
                    '/versions' +
                    '/{{ version_name }}')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)
        self.url = self.url.replace('{{ resource_group }}', self.resource_group)
        self.url = self.url.replace('{{ gallery_name }}', self.gallery_name)
        self.url = self.url.replace('{{ image_name }}', self.gallery_image_name)
        self.url = self.url.replace('{{ version_name }}', self.name)

        old_response = self.get_resource()

        if not old_response:
            self.log("GalleryImageVersion instance doesn't exist")

            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log('GalleryImageVersion instance already exists')

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
            self.log('Need to Create / Update the GalleryImageVersion instance')

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_resource()

            self.results['changed'] = True
            self.log('Creation / Update done')
        elif self.to_do == Actions.Delete:
            self.log('GalleryImageVersion instance deleted')
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_resource()
        else:
            self.log('GalleryImageVersion instance unchanged')
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]

        return self.results

    def create_update_resource(self):
        # self.log('Creating / Updating the GalleryImageVersion instance {0}'.format(self.))

        try:
            response = self.mgmt_client.query(self.url,
                                              'PUT',
                                              self.query_parameters,
                                              self.header_parameters,
                                              self.body,
                                              self.status_code,
                                              600,
                                              30)
        except CloudError as exc:
            self.log('Error attempting to create the GalleryImageVersion instance.')
            self.fail('Error creating the GalleryImageVersion instance: {0}'.format(str(exc)))

        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}

        while response['properties']['provisioningState'] == 'Creating':
            time.sleep(60)
            response = self.get_resource()

        return response

    def delete_resource(self):
        # self.log('Deleting the GalleryImageVersion instance {0}'.format(self.))
        try:
            response = self.mgmt_client.query(self.url,
                                              'DELETE',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
        except CloudError as e:
            self.log('Error attempting to delete the GalleryImageVersion instance.')
            self.fail('Error deleting the GalleryImageVersion instance: {0}'.format(str(e)))
        return True

    def get_resource(self):
        # self.log('Checking if the GalleryImageVersion instance {0} is present'.format(self.))
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
            response = json.loads(response.text)
            found = True
            self.log("Response : {0}".format(response))
            # self.log("AzureFirewall instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the AzureFirewall instance.')
        if found is True:
            return response

        return False


def main():
    AzureRMGalleryImageVersions()


if __name__ == '__main__':
    main()
