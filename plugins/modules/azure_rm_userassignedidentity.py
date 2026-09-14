#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_userassignedidentity

version_added: "4.1.0"

short_description: Manage a user-assigned managed identity

description:
    - Create, update and delete a user-assigned managed identity (Microsoft.ManagedIdentity/userAssignedIdentities).

options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    name:
        description:
            - The name of the user-assigned identity.
        required: true
        type: str
    location:
        description:
            - Valid Azure location for the identity. Defaults to location of the resource group.
        type: str
    isolation_scope:
        description:
            - Enum to configure regional restrictions on identity assignment.
        type: str
        choices:
            - None
            - Regional
    state:
        description:
            - Assert the state of the user-assigned identity. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Create a user-assigned identity
  azure_rm_userassignedidentity:
    resource_group: myResourceGroup
    name: myIdentity
    location: eastus
    state: present

- name: Update a user-assigned identity's tags
  azure_rm_userassignedidentity:
    resource_group: myResourceGroup
    name: myIdentity
    tags:
      env: production
    state: present

- name: Delete a user-assigned identity
  azure_rm_userassignedidentity:
    resource_group: myResourceGroup
    name: myIdentity
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the user-assigned identity.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The user-assigned identity resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/
                     Microsoft.ManagedIdentity/userAssignedIdentities/myIdentity"
        name:
            description:
                - The user-assigned identity name.
            returned: always
            type: str
            sample: myIdentity
        location:
            description:
                - The Azure Region where the resource lives.
            returned: always
            type: str
            sample: eastus
        tenant_id:
            description:
                - The id of the tenant which the identity belongs to.
            returned: always
            type: str
            sample: "72f98888-8666-4144-9199-2d7cd0111111"
        principal_id:
            description:
                - The id of the service principal object associated with the identity.
            returned: always
            type: str
            sample: "72f98888-8666-4144-9199-2d7cd0222222"
        client_id:
            description:
                - The id of the app associated with the identity.
            returned: always
            type: str
            sample: "72f98888-8666-4144-9199-2d7cd0333333"
        isolation_scope:
            description:
                - Regional restriction configured on the identity.
            returned: always
            type: str
            sample: "None"
        system_data:
            description:
                - Metadata pertaining to creation and last modification of the resource.
                - Not always populated immediately after creation.
            returned: success
            type: dict
            sample: {
                "created_at": "2026-08-31T03:12:08.743499Z",
                "created_by": "72f98888-8666-4144-9199-2d7cd0444444",
                "created_by_type": "User",
                "last_modified_at": "2026-08-31T03:12:08.743499Z",
                "last_modified_by": "72f98888-8666-4144-9199-2d7cd0444444",
                "last_modified_by_type": "User"
            }
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: {"key1": "value1"}
        type:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: "Microsoft.ManagedIdentity/userAssignedIdentities"
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.msi.models import Identity, IdentityUpdate
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMUserAssignedIdentity(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            isolation_scope=dict(type='str', choices=['None', 'Regional']),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.isolation_scope = None
        self.state = None
        self.tags = None

        self.results = dict(
            changed=False,
            state=dict(),
        )

        super(AzureRMUserAssignedIdentity, self).__init__(self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        changed = False
        old_response = self.get_identity()
        response = old_response

        if self.state == 'present':
            if not old_response:
                changed = True
            else:
                if self.isolation_scope is not None and self.isolation_scope != old_response.get('isolation_scope'):
                    changed = True
                    old_response['isolation_scope'] = self.isolation_scope
                update_tags, self.tags = self.update_tags(old_response.get('tags'))
                if update_tags:
                    changed = True
                    old_response['tags'] = self.tags

            if changed and not self.check_mode:
                response = self.create_or_update_identity(old_response)

        elif self.state == 'absent':
            if old_response:
                changed = True
                if not self.check_mode:
                    self.delete_identity()
                    response = None

        self.results['changed'] = changed
        self.results['state'] = response if response else dict()

        return self.results

    def get_identity(self):
        try:
            response = self.msi_client.user_assigned_identities.get(
                resource_group_name=self.resource_group,
                resource_name=self.name,
            )
            return as_attribute_dict(response, exclude_readonly=False)
        except ResourceNotFoundError:
            return None

    def create_or_update_identity(self, old_response):
        # location is immutable and omitted from IdentityUpdate; fall back to the existing
        # isolation_scope so a tags-only update never resets a value the user didn't touch.
        isolation_scope = self.isolation_scope
        if isolation_scope is None and old_response:
            isolation_scope = old_response.get('isolation_scope')

        try:
            if old_response:
                parameters = IdentityUpdate(tags=self.tags, isolation_scope=isolation_scope)
                response = self.msi_client.user_assigned_identities.update(
                    resource_group_name=self.resource_group,
                    resource_name=self.name,
                    parameters=parameters,
                )
            else:
                parameters = Identity(location=self.location, tags=self.tags, isolation_scope=isolation_scope)
                response = self.msi_client.user_assigned_identities.create_or_update(
                    resource_group_name=self.resource_group,
                    resource_name=self.name,
                    parameters=parameters,
                )
        except Exception as exc:
            self.fail("Error creating or updating user-assigned identity {0} - {1}".format(self.name, str(exc)))
        return as_attribute_dict(response, exclude_readonly=False)

    def delete_identity(self):
        try:
            self.msi_client.user_assigned_identities.delete(
                resource_group_name=self.resource_group,
                resource_name=self.name,
            )
        except Exception as exc:
            self.fail("Error deleting user-assigned identity {0} - {1}".format(self.name, str(exc)))
        return True


def main():
    AzureRMUserAssignedIdentity()


if __name__ == '__main__':
    main()
