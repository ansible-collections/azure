#!/usr/bin/python
#
# Copyright (c) 2025 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_diskaccess
version_added: '3.3.0'
short_description: Show the details for the disk access
description:
    - Get or list the details for the disk access.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: true
    name:
        description:
            - The disk access name.
        required: true
        type: str
    location:
        description:
            - Resource location.
        type: str
    extended_location:
        description:
            - The extended location where the disk access will be created.
        type: dict
        suboptions:
            name:
                description:
                    - The name of the extended location.
                type: str
                required: true
            type:
                description:
                    - The type of the extended location.
                type: str
                default: EdgeZone
                choices:
                    - EdgeZone
    state:
        description:
            - State of the disk access.
            - Use C(present) to create or update a disk access and use C(absent) to delete.
        type: str
        default: present
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Create a new disk access
  azure_rm_diskaccess:
    resource_group: myRG
    name: testaccess
    location: westus2

- name: Create a new disk access
  azure_rm_diskaccess:
    resource_group: myRG
    name: testaccess
    location: westus
    extended_location:
      name: losangeles
      type: EdgeZone
    tags:
      key1: value1

- name: Delete the disk access
  azure_rm_diskaccess:
    resource_group: myRG
    name: testaccess
    state: absent
'''

RETURN = '''
state:
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
            sample:
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
    from azure.core.polling import LROPoller
except ImportError:
    pass


class AzureRMDiskAccess(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
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
            extended_location=dict(
                type='dict',
                options=dict(
                    name=dict(type='str', required=True),
                    type=dict(type='str', default='EdgeZone', choices=['EdgeZone']),
                )
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                default='present'
            )
        )
        # store the results of the module operation
        self.results = dict()
        self.resource_group = None
        self.name = None
        self.location = None
        self.extended_location = None
        self.state = None

        super(AzureRMDiskAccess, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True, facts_module=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec) + ['tags']:
            setattr(self, key, kwargs[key])

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        changed = False
        response = self.get_diskaccess()

        if self.state == 'present':
            if response is not None:
                if self.extended_location is not None and self.extended_location.get('name') != response['extended_location'].get('name'):
                    self.fail("Extended location cannot be changed")

                update_tags, self.tags = self.update_tags(response.get('tags'))
                if update_tags:
                    changed = True
                    if not self.check_mode:
                        response = self.update_diskaccess()
            else:
                changed = True
                if not self.check_mode:
                    response = self.create_or_update()
        else:
            if not self.check_mode:
                if response is not None:
                    response = self.delete_diskaccess()
                    changed = True
                else:
                    changed = False
            else:
                changed = True

        self.results['changed'] = changed
        self.results['state'] = response

        return self.results

    def get_diskaccess(self):
        try:
            return self.to_dict(self.disk_client.disk_accesses.get(self.resource_group, self.name))
        except ResourceNotFoundError:
            pass

    def create_or_update(self):
        try:
            poller = self.disk_client.disk_accesses.begin_create_or_update(self.resource_group, self.name, dict(tags=self.tags,
                                                                                                                location=self.location,
                                                                                                                extended_location=self.extended_location))
            if isinstance(poller, LROPoller):
                response = self.get_poller_result(poller)
                return self.to_dict(response)

        except Exception as ec:
            self.fail('Error when create disk access {0}: {1}'.format(self.name, ec))

    def update_diskaccess(self):
        try:
            poller = self.disk_client.disk_accesses.begin_update(self.resource_group, self.name, dict(tags=self.tags))
            if isinstance(poller, LROPoller):
                response = self.get_poller_result(poller)
                return self.to_dict(response)
        except Exception as ec:
            self.fail('Error when update disk access {0}: {1}'.format(self.name, ec))

    def delete_diskaccess(self):
        try:
            self.disk_client.disk_accesses.begin_delete(self.resource_group, self.name)
        except Exception as ec:
            self.fail('Error when delete disk access {0}: {1}'.format(self.name, ec))

    def get_diskaccess(self):
        try:
            return self.to_dict(self.disk_client.disk_accesses.get(self.resource_group, self.name))
        except ResourceNotFoundError:
            pass

    def to_dict(self, item):
        if item is None:
            return None
        disk_access = dict(
            resource_group=self.resource_group,
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
    AzureRMDiskAccess()


if __name__ == '__main__':
    main()
