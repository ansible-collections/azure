#!/usr/bin/python
#
# Copyright (c) 2019 Liu Qingyi, (@smile37773)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_galleryimageversion_info
version_added: "0.1.2"
short_description: Get Azure SIG Image Version info
description:
    - Get info of Azure SIG Image Version.
options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: true
    gallery_name:
        description:
            - The name of the Shared Image Gallery in which the Image Definition resides.
        type: str
        required: true
    gallery_image_name:
        description:
            - The name of the gallery Image Definition in which the Image Version resides.
        type: str
        required: true
    name:
        description:
            - Resource name.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Liu Qingyi (@smile37773)

'''

EXAMPLES = '''
- name: List gallery image versions in a gallery image definition.
  azure_rm_galleryimageversion_info:
    resource_group: myResourceGroup
    gallery_name: myGallery
    gallery_image_name: myImage
- name: Get a gallery image version.
  azure_rm_galleryimageversion_info:
    resource_group: myResourceGroup
    gallery_name: myGallery
    gallery_image_name: myImage
    name: myVersion
'''

RETURN = '''
versions:
    description:
        A list of dict results where the key is the name of the version and the values are the info for that version.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups
      /myResourceGroup/providers/Microsoft.Compute/galleries/myGallery/images/myImage/versions/myVersion"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: "myVersion"
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: "eastus"
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: { "tag": "value" }
        publishing_profile:
            description:
                - The publishing profile of a gallery image version.
            type: dict
        provisioning_state:
            description:
                - The current state of the gallery.
            type: str
            sample: "Succeeded"
        storage_profile:
            description:
                - This is the storage profile of a Gallery Image Version.
            type: dict
            sample: {
                    "data_disk_images": [{"host_caching": "None", "lun": 0, "size_in_gb": 128}],
                    "os_disk_image": {"host_caching": "ReadOnly", "size_in_gb": 30, "source": {}},
                    "source": {"id": "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.Compute/images/testimagea"},
                    "type": "Microsoft.Compute/galleries/images/versions"
            }
        safety_profile:
            description:
                - This is the safety profile of the Gallery Image Version.
            type: dict
            sample: {
                    "allow_deletion_of_replicated_locations": false,
                    "reported_for_policy_violation": false
                }
'''

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass


class AzureRMGalleryImageVersionsInfo(AzureRMModuleBase):
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
                type='str'
            ),
        )

        self.resource_group = None
        self.gallery_name = None
        self.gallery_image_name = None
        self.name = None

        self.results = dict(changed=False)
        super(AzureRMGalleryImageVersionsInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            self.results['versions'] = self.get()
        else:
            self.results['versions'] = self.listbygalleryimage()
        return self.results

    def get(self):
        """ Get a single gallery image version"""
        response = None

        try:
            response = self.image_version_client.gallery_image_versions.get(self.resource_group, self.gallery_name, self.gallery_image_name, self.name)
        except ResourceNotFoundError:
            self.log('Could not get the gallery image verison')

        return self.format_item(response)

    def listbygalleryimage(self):
        response = None
        try:
            response = self.image_version_client.gallery_image_versions.list_by_gallery_image(self.resource_group, self.gallery_name, self.gallery_image_name)
        except Exception:
            self.log('Could not list the gallery image versions')

        return [self.format_item(x) for x in response] if response else []

    def format_item(self, item):
        if item is None:
            return None
        else:
            return item.as_dict()


def main():
    AzureRMGalleryImageVersionsInfo()


if __name__ == '__main__':
    main()
