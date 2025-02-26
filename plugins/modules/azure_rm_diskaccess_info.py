#!/usr/bin/python
#
# Copyright (c) 2025 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_diskaccess_info
version_added: '3.3.0'
short_description: Show the details for the disk access
description:
    - Get or list the details for the disk access.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
    name:
        description:
            - The disk access name.
        type: str
    tags:
        description:
            - The tags of the disk access.
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get disk access by name
  azure_rm_diskaccess_info:
    resource_group: myRG
    name: testaccess

- name: List disk access by resource group
  azure_rm_diskaccess_info:
    resource_group: myRG

- name: List disk access in same subscription and filter by tags
  azure_rm_diskaccess_info:
    resource_group: myRG
    tags:
      - key1
      - key2
'''

RETURN = '''
disk_accesses:
    description:
        - Details for the disk access.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            type: str
            returned: always
            sample: "/subscriptions/xxxx/resourceGroups/myRG/providers/Microsoft.Compute/diskAccesses/diskacc"
        resource_group:
            description:
                - Resource group name.
            type: str
            returned: always
            sample: myRG
        name:
            description:
                - Resource name.
            type: str
            returned: always
            sample: testaccess
        type:
            description:
                - Resource Type.
            type: str
            returned: always
            sample: "Microsoft.Compute/diskAccesses"
        tags:
            description:
                - The tags of the disk access.
            type: dict
            returned: always
            sample: {key1: value1, key2: value2}
        provisioning_state:
            description:
                - The disk access resource provisioning state.
            type: str
            returned: always
            sample: Successed
        extended_location:
            description:
                - The extended location where the disk access will be created.
            type: dict
            returned: always
            sample: {"name": "portland", "type": "EdgeZone"}
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass


class AzureRMDiskAccessInfo(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
            ),
            name=dict(
                type='str'
            ),
            tags=dict(
                type='list',
                elements='str',
            )
        )
        # store the results of the module operation
        self.results = dict()
        self.resource_group = None
        self.name = None
        self.tags = None

        super(AzureRMDiskAccessInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec):
            setattr(self, key, kwargs[key])

        if self.name is not None:
            if self.resource_group is not None:
                disk_accesses = self.get_diskaccess()
            else:
                self.fail("Missing configuration, When configure the nae, you must configure the resource group name")
        elif self.resource_group is not None:
            disk_accesses = self.list_by_resourcegroup()
        else:
            disk_accesses = self.list_all()

        self.results['disk_accesses'] = [self.to_dict(x) for x in disk_accesses if self.has_tags(x.tags, self.tags)]
        return self.results

    def get_diskaccess(self):
        try:
            return [self.disk_client.disk_accesses.get(self.resource_group, self.name)]
        except ResourceNotFoundError:
            return []

    def list_by_resourcegroup(self):
        try:
            return self.disk_client.disk_accesses.list_by_resource_group(self.resource_group)
        except Exception:
            pass

    def list_all(self):
        result = []
        try:
            return self.disk_client.disk_accesses.list()
        except Exception as ec:
            pass

    def to_dict(self, item):
        if item is None:
            return None
        disk_access = dict(
            resource_group=item.id.split('/')[4],
            name=item.name,
            id=item.id,
            type=item.type,
            location=item.location,
            provisioning_state=item.provisioning_state,
            extended_location=dict(),
            tags=item.tags
        )
        if item.extended_location is not None:
            disk_access['extended_location']['name'] = item.extended_location.name
            disk_access['extended_location']['type'] = item.extended_location.type
        return disk_access


def main():
    AzureRMDiskAccessInfo()


if __name__ == '__main__':
    main()
