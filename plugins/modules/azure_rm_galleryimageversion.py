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
            - Required when creating.
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
                type: dict
                suboptions:
                    source:
                        description:
                            - Reference to os disk snapshot.
                            - Could be resource ID.
                            - Could be a dictionary containing I(resource_group) and I(name).
                            - Could be a dictionary containing I(resource_group), I(storage_account), and I(uri)
                              if the snapshot is stored as a PageBlob in a storage account container.
                        type: raw
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
                elements: raw
                suboptions:
                    source:
                        description:
                            - Reference to data disk snapshot. Could be resource ID or dictionary containing I(resource_group) and I(name)
                        type: raw
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
        type: dict
        suboptions:
            target_regions:
                description:
                    - The target regions where the Image Version is going to be replicated to.
                    - This property is updatable.
                type: list
                elements: raw
                suboptions:
                    name:
                        description:
                            - Region name.
                        type: str
                        required: true
                    regional_replica_count:
                        description:
                            - The number of replicas of the Image Version to be created per region.
                            - This property would take effect for a region when regionalReplicaCount is not specified.
                            - This property is updatable.
                        type: int
                    storage_account_type:
                        description:
                            - Storage account type.
                        type: str
                    encryption:
                        description:
                            - Allows users to provide customer managed keys for encrypting the OS and data disks in the gallery artifact.
                        type: dict
                        suboptions:
                            data_disk_images:
                                description:
                                    - A list of encryption specifications for data disk images.
                                type: list
                                elements: dict
                                suboptions:
                                    disk_encryption_set_id:
                                        description:
                                            - A relative URI containing the resource ID of the disk encryption set.
                                        type: str
                                    lun:
                                        description:
                                            - This property specifies the logical unit number of the data disk.
                                            - This value is used to identify data disks within the Virtual Machine and
                                              therefore must be unique for each data disk attached to the Virtual Machine.
                                        type: int
                            os_disk_image:
                                description:
                                    - Contains encryption settings for an OS disk image.
                                type: dict
                                suboptions:
                                    disk_encryption_set_id:
                                        description:
                                            - A relative URI containing the resource ID of the disk encryption set.
                                        type: str
                                    security_profile:
                                        description:
                                            - This property specifies the security profile of an OS disk image.
                                        type: dict
                                        suboptions:
                                            confidential_vm_encryption_type:
                                                description:
                                                    - Confidential VM encryption types.
                                                type: dict
                                                suboptions:
                                                    encrypted_vm_guest_state_only_with_pmk:
                                                        description:
                                                            - VM Guest State Only with PMK.
                                                        type: str
                                                    encrypted_with_cmk:
                                                        description:
                                                            - Encrypted with CMK.
                                                        type: str
                                                    encrypted_with_pmk:
                                                        description:
                                                            - Encrypted with PMK.
                                                        type: str
                                            secure_vm_disk_encryption_set_id:
                                                description:
                                                    - Secure VM disk encryption set id.
                                                type: str
            managed_image:
                description:
                    - Managed image reference, could be resource ID, or dictionary containing I(resource_group) and I(name)
                    - Obsolete since 2.10, use storage_profile instead
                type: raw
            snapshot:
                description:
                    - Source snapshot to be used.
                    - Obsolete since 2.10, use storage_profile instead
                type: raw
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
                choices:
                    - Standard_LRS
                    - Standard_ZRS
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
      exclude_from_latest: true
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
      exclude_from_latest: true
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
      exclude_from_latest: true
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

- name: Create gallery image by using a os disk snapshot stored in Storage Account container
  azure_rm_galleryimageversion:
    resource_group: myResourceGroup
    gallery_name: myGallery
    gallery_image_name: myGalleryImage
    name: 3.4.0
    location: East  US
    publishing_profile:
      end_of_life_date: "2020-10-01t00:00:00+00:00"
      exclude_from_latest: true
      replica_count: 1
      storage_account_type: Standard_LRS
      target_regions:
        - name: East US
          regional_replica_count: 1
          storage_account_type: Standard_LRS
    storage_profile:
      os_disk:
        source:
          resource_group: myResourceGroup
          storage_account: myStorageAccount
          uri: "https://myStorageAccount.blob.core.windows.net/myContainer/myImage.vhd"
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


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMGalleryImageVersions(AzureRMModuleBaseExt):
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
            gallery_image_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            tags=dict(
                type='dict',
            ),
            location=dict(
                type='str',
            ),
            storage_profile=dict(
                type='dict',
                options=dict(
                    source_image=dict(
                        type='raw',
                    ),
                    os_disk=dict(
                        type='dict',
                        options=dict(
                            source=dict(
                                type='raw',
                            ),
                            host_caching=dict(
                                type='str',
                                default="None",
                                choices=["ReadOnly", "ReadWrite", "None"]
                            )
                        )
                    ),
                    data_disks=dict(
                        type='list',
                        elements='raw',
                        options=dict(
                            lun=dict(
                                type='int'
                            ),
                            source=dict(
                                type='raw',
                            ),
                            host_caching=dict(
                                type='str',
                                default="None",
                                choices=["ReadOnly", "ReadWrite", "None"]
                            )
                        )
                    )
                )
            ),
            publishing_profile=dict(
                type='dict',
                options=dict(
                    target_regions=dict(
                        type='list',
                        elements='raw',
                        options=dict(
                            name=dict(
                                type='str',
                                required=True,
                            ),
                            regional_replica_count=dict(
                                type='int',
                            ),
                            storage_account_type=dict(
                                type='str',
                            ),
                            encryption=dict(
                                type='dict',
                                options=dict(
                                    data_disk_images=dict(
                                        type='list',
                                        elements='dict',
                                        options=dict(
                                            disk_encryption_set_id=dict(
                                                type='str',
                                            ),
                                            lun=dict(
                                                type='int'
                                            )
                                        )
                                    ),
                                    os_disk_image=dict(
                                        type='dict',
                                        options=dict(
                                            disk_encryption_set_id=dict(
                                                type='str',
                                            ),
                                            security_profile=dict(
                                                type='dict',
                                                options=dict(
                                                    confidential_vm_encryption_type=dict(
                                                        type='dict',
                                                        options=dict(
                                                            encrypted_vm_guest_state_only_with_pmk=dict(
                                                                type='str',
                                                            ),
                                                            encrypted_with_cmk=dict(
                                                                type='str',
                                                            ),
                                                            encrypted_with_pmk=dict(
                                                                type='str',
                                                            )
                                                        )
                                                    ),
                                                    secure_vm_disk_encryption_set_id=dict(
                                                        type='str',
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    managed_image=dict(
                        type='raw',
                    ),
                    snapshot=dict(
                        type='raw',
                    ),
                    replica_count=dict(
                        type='int',
                    ),
                    exclude_from_latest=dict(
                        type='bool',
                    ),
                    end_of_life_date=dict(
                        type='str',
                    ),
                    storage_account_type=dict(
                        type='str',
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
        self.body['properties'] = {}
        self.query_parameters = {}
        self.query_parameters['api-version'] = '2022-03-03'
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
                if key == 'location':
                    self.body['location'] = kwargs[key]
                elif key == 'storage_profile':
                    self.body['properties']['storageProfile'] = {}
                    if kwargs[key].get('source_image') is not None:
                        self.body['properties']['storageProfile']['source'] = {}
                        if isinstance(kwargs[key].get('source_image'), str):
                            self.body['properties']['storageProfile']['source']['id'] = kwargs[key].get('source_image')
                        elif isinstance(kwargs[key].get('source_image'), dict):
                            if kwargs[key]['source_image'].get('id') is not None:
                                self.body['properties']['storageProfile']['source']['id'] = kwargs[key]['source_image'].get('id')
                            if kwargs[key]['source_image'].get('resource_group') is not None and kwargs[key]['source_image'].get('name') is not None:
                                self.body['properties']['storageProfile']['source']['id'] = ('/subscriptions/' +
                                                                                             self.subscription_id +
                                                                                             '/resourceGroups/' +
                                                                                             kwargs[key]['source_image'].get('resource_group') +
                                                                                             '/providers/Microsoft.Compute/images/' +
                                                                                             kwargs[key]['source_image'].get('name'))
                            elif (kwargs[key]['source_image'].get('resource_group') is not None and
                                  kwargs[key]['source_image'].get('gallery_name') is not None and
                                  kwargs[key]['source_image'].get('gallery_image_name') is not None and kwargs[key]['source_image'].get('version') is not None):
                                self.body['properties']['storageProfile']['source']['id'] = ('/subscriptions/' +
                                                                                             self.subscription_id +
                                                                                             '/resourceGroups/' +
                                                                                             kwargs[key]['source_image'].get('resource_group') +
                                                                                             '/providers/Microsoft.Compute/galleries/' +
                                                                                             kwargs[key]['source_image'].get('gallery_name') +
                                                                                             '/images/' +
                                                                                             kwargs[key]['source_image'].get('gallery_image_name') +
                                                                                             '/versions/' +
                                                                                             kwargs[key]['source_image'].get('version'))
                            else:
                                self.fail("The source_image parameters config errors")
                        else:
                            self.fail("The source_image parameters config errors")
                    if kwargs[key].get('os_disk') is not None:
                        self.body['properties']['storageProfile']['osDiskImage'] = {}
                        if kwargs[key]['os_disk'].get('host_caching') is not None:
                            self.body['properties']['storageProfile']['osDiskImage']['hostCaching'] = kwargs[key]['os_disk'].get('host_caching')
                        if kwargs[key]['os_disk'].get('source') is not None:
                            self.body['properties']['storageProfile']['osDiskImage']['source'] = {}
                            if isinstance(kwargs[key]['os_disk']['source'], str):
                                self.body['properties']['storageProfile']['osDiskImage']['source']['id'] = kwargs[key]['os_disk']['source']
                            elif isinstance(kwargs[key]['os_disk']['source'], dict):
                                if kwargs[key]['os_disk']['source'].get('id') is not None:
                                    self.body['properties']['storageProfile']['osDiskImage']['source']['id'] = kwargs[key]['os_disk']['source'].get('id')
                                elif kwargs[key]['os_disk']['source'].get('resource_group') is not None and \
                                        kwargs[key]['os_disk']['source'].get('name') is not None:
                                    resource_group = kwargs[key]['os_disk']['source'].get('resource_group')
                                    self.body['properties']['storageProfile']['osDiskImage']['source']['id'] = ('/subscriptions/' +
                                                                                                                self.subscription_id +
                                                                                                                '/resourceGroups/' +
                                                                                                                resource_group +
                                                                                                                '/providers/Microsoft.Compute/snapshots/' +
                                                                                                                kwargs[key]['os_disk']['source'].get('name'))
                                elif kwargs[key]['os_disk']['source'].get('uri') is not None and \
                                        kwargs[key]['os_disk']['source'].get('resource_group') is not None and \
                                        kwargs[key]['os_disk']['source'].get('storage_account') is not None:
                                    resource_group = kwargs[key]['os_disk']['source'].get('resource_group')
                                    storage_account = kwargs[key]['os_disk']['source'].get('storage_account')
                                    self.body['properties']['storageProfile']['osDiskImage']['source']['id'] = ('/subscriptions/' +
                                                                                                                self.subscription_id +
                                                                                                                '/resourceGroups/' +
                                                                                                                resource_group +
                                                                                                                '/providers/Microsoft.Storage' +
                                                                                                                '/storageAccounts/' +
                                                                                                                storage_account)
                                    self.body['properties']['storageProfile']['osDiskImage']['source']['uri'] = kwargs[key]['os_disk']['source'].get('uri')
                                else:
                                    self.fail("The os_disk.source parameters config errors")

                            else:
                                self.fail("The os_disk.source parameters config errors")

                    if kwargs[key].get('data_disks') is not None:
                        self.body['properties']['storageProfile']['dataDiskImages'] = []
                        data_disk = {}
                        for item in kwargs[key].get('data_disks'):
                            if item.get('lun') is not None:
                                data_disk['lun'] = item['lun']
                            if item.get('source') is not None:
                                data_disk['source'] = {}
                                if isinstance(item.get('source'), str):
                                    data_disk['source']['id'] = item.get('source')
                                elif isinstance(item.get('source'), dict):
                                    if item['source'].get('id') is not None:
                                        data_disk['source']['id'] = item['source'].get('id')
                                    elif item['source'].get('resource_group') is not None and item['source'].get('name') is not None:
                                        data_disk['source']['id'] = ('/subscriptions/' +
                                                                     self.subscription_id +
                                                                     '/resourceGroups/' +
                                                                     item['source'].get('resource_group') +
                                                                     '/providers/Microsoft.Compute/snapshots/' +
                                                                     item['source'].get('name'))
                                    else:
                                        self.fail("The data_disk.source parameters config errors")
                                else:
                                    self.fail("The data_disk.source parameters config errors")
                            if item.get('host_caching') is not None:
                                data_disk['hostCaching'] = item['host_caching']
                elif key == 'publishing_profile':
                    self.body['properties']['publishingProfile'] = {}
                    if kwargs['publishing_profile'].get('target_regions') is not None:
                        self.body['properties']['publishingProfile']['targetRegions'] = []
                        for item in kwargs['publishing_profile']['target_regions']:
                            target_regions = {}
                            for value in item.keys():
                                if value == 'name':
                                    target_regions[value] = item[value]
                                elif value == 'regional_replica_count':
                                    target_regions['regionalReplicaCount'] = item[value]
                                elif value == 'storage_account_type':
                                    target_regions['storageAccountType'] = item[value]
                                elif value == 'encryption':
                                    target_regions['encryption'] = {}
                                    if item[value].get('data_disk_images') is not None:
                                        target_regions['encryption']['dataDiskImages'] = []
                                        for tt in item[value]['data_disk_images']:
                                            disk_image = {}
                                            if tt.get('lun') is not None:
                                                disk_image['lun'] = tt['lun']
                                            if tt.get('disk_encryption_set_id') is not None:
                                                disk_image['diskEncryptionSetId'] = tt['disk_encryption_set_id']
                                            target_regions['encryption']['dataDiskImages'].append(disk_image)

                                    if item['encryption'].get('os_disk_image') is not None:
                                        target_regions['encryption']['osDiskImage'] = {}
                                        if item['encryption']['os_disk_image'].get('disk_encryption_set_id') is not None:
                                            disk_encryption_set_id = item['encryption']['os_disk_image']['disk_encryption_set_id']
                                            target_regions['encryption']['osDiskImage']['diskEncryptionSetId'] = disk_encryption_set_id
                                        if item['encryption']['os_disk_image'].get('security_profile') is not None:
                                            target_regions['encryption']['osDiskImage']['securityProfile'] = {}
                                            if item['encryption']['os_disk_image']['security_profile'].get('secure_vm_disk_encryption_set_id') is not None:
                                                secure_id = item['encryption']['os_disk_image']['security_profile']['secure_vm_disk_encryption_set_id']
                                                target_regions['encryption']['osDiskImage']['securityProfile']['secureVMDiskEncryptionSetId'] = secure_id

                                            if item['encryption']['os_disk_image']['security_profile'].get('confidential_vm_encryption_type') is not None:
                                                target_regions['encryption']['osDiskImage']['securityProfile']['confidentialVMEncryptionType'] = {}
                                                security = item['encryption']['os_disk_image']['security_profile']['confidential_vm_encryption_type']
                                                tt = target_regions['encryption']['osDiskImage']['securityProfile']['confidentialVMEncryptionType']
                                                if security.get('encrypted_vm_guest_state_only_with_pmk') is not None:
                                                    tt['EncryptedVMGuestStateOnlyWithPmk'] = security.get('encrypted_vm_guest_state_only_with_pmk')
                                                if security.get('encrypted_with_cmk') is not None:
                                                    tt['EncryptedWithCmk'] = security.get('encrypted_with_cmk')
                                                if security.get('encrypted_with_pmk') is not None:
                                                    tt['EncryptedWithPmk'] = security.get('encrypted_with_pmk')
                            self.body['properties']['publishingProfile']['targetRegions'].append(target_regions)
                    if kwargs[key].get('managed_image') is not None:
                        if isinstance(kwargs[key]['managed_image'], str):
                            self.body['properties']['publishingProfile']['managed_image'] = kwargs[key]['managed_image']
                        elif isinstance(kwargs[key]['managed_image'], dict):
                            if kwargs[key]['managed_image'].get('id') is not None:
                                self.body['properties']['publishingProfile']['managed_image'] = kwargs[key]['managed_image']['id']
                            elif kwargs[key]['managed_image'].get('resource_group') is not None and kwargs[key]['managed_image'].get('name') is not None:
                                self.body['properties']['publishingProfile']['managed_image'] = ('/subscriptions/' +
                                                                                                 self.subscription_id +
                                                                                                 '/resourceGroups/' +
                                                                                                 kwargs[key]['managed_image'].get('resource_group') +
                                                                                                 '/providers/Microsoft.Compute/images/' +
                                                                                                 kwargs[key]['managed_image'].get('name'))
                            else:
                                self.fail("The managed_image parameters config errors")
                        else:
                            self.fail("The managed_image parameters config errors")
                    if kwargs[key].get('snapshot') is not None:
                        if isinstance(kwargs[key].get('snapshot'), str):
                            self.body['properties']['publishingProfile']['snapshot'] = kwargs[key].get('snapshot')
                        elif isinstance(kwargs[key].get('snapshot'), dict):
                            if kwargs[key]['snapshot'].get('id') is not None:
                                self.body['properties']['publishingProfile']['snapshot'] = kwargs[key]['snapshot'].get('id')
                            elif kwargs[key]['snapshot'].get('resource_group') is not None and kwargs[key]['snapshot'].get('name') is not None:
                                self.body['properties']['publishingProfile']['snapshot'] = ('/subscriptions/' +
                                                                                            self.subscription_id +
                                                                                            '/resourceGroups/' +
                                                                                            kwargs[key]['snapshot'].get('resource_group') +
                                                                                            '/providers/Microsoft.Compute/snapshots/' +
                                                                                            kwargs[key]['snapshot'].get('name'))
                            else:
                                self.fail("The managed_image parameters config errors")
                        else:
                            self.fail("The managed_image parameters config errors")
                    if kwargs[key].get('replica_count') is not None:
                        self.body['properties']['publishingProfile']['replicaCount'] = kwargs[key].get('replica_count')
                    if kwargs[key].get('exclude_from_latest') is not None:
                        self.body['properties']['publishingProfile']['excludeFromLatest'] = kwargs[key].get('exclude_from_latest')
                    if kwargs[key].get('end_of_life_date') is not None:
                        self.body['properties']['publishingProfile']['endOfLifeDate'] = kwargs[key].get('end_of_life_date')
                    if kwargs[key].get('storage_account_type') is not None:
                        self.body['properties']['publishingProfile']['storageAccountType'] = kwargs[key].get('storage_account_type')

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
                update_tags, newtags = self.update_tags(old_response.get('tags', dict()))
                if update_tags:
                    self.tags = newtags
                    self.body['tags'] = self.tags
                    self.to_do = Actions.Update
                if self.body['properties'].get('publishingProfile') is not None:
                    for key in self.body['properties']['publishingProfile'].keys():
                        if key == 'targetRegions':
                            result = dict(compare=[])
                            modifies = {'/*/name': {'updatable': True, 'comparison': 'location'}}
                            if not self.default_compare(modifies, self.body['properties']['publishingProfile'][key],
                               old_response['properties']['publishingProfile'][key], '', result):
                                self.to_do = Actions.Update
                        elif key == 'endOfLifeDate':
                            if self.body['properties']['publishingProfile'][key].lower() != old_response['properties']['publishingProfile'][key].lower():
                                self.to_do = Actions.Update
                        elif self.body['properties']['publishingProfile'].get(key) != old_response['properties']['publishingProfile'].get(key):
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
        except Exception as exc:
            self.log('Error attempting to create the GalleryImageVersion instance.')
            self.fail('Error creating the GalleryImageVersion instance: {0}'.format(str(exc)))

        if hasattr(response, 'body'):
            response = json.loads(response.body())
        elif hasattr(response, 'context'):
            response = response.context['deserialized_data']
        else:
            self.fail("Create or Updating fail, no match message return, return info as {0}".format(response))

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
        except Exception as e:
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
    AzureRMGalleryImageVersions()


if __name__ == '__main__':
    main()
