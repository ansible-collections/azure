#!/usr/bin/python
#
# Copyright (c) 2018 Yunge Zhu, (@yungezz)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_roleassignment
version_added: "0.1.2"
short_description: Manage Azure Role Assignment
description:
    - Create and delete instance of Azure Role Assignment.

options:
    name:
        description:
            - Unique name of role assignment.
            - The role assignment name must be a GUID, sample as "3ce0cbb0-58c4-4e6d-a16d-99d86a78b3ca".
        required: True
    assignee_object_id:
        description:
            - The object id of assignee. This maps to the ID inside the Active Directory.
            - It can point to a user, service principal or security group.
            - Required when creating role assignment.
    role_definition_id:
        description:
            - The role definition id used in the role assignment.
            - Required when creating role assignment.
    scope:
        description:
            - The scope of the role assignment to create.
            - For example, use /subscriptions/{subscription-id}/ for subscription.
            - /subscriptions/{subscription-id}/resourceGroups/{resource-group-name} for resource group.
            - /subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/{resource-provider}/{resource-type}/{resource-name} for resource.
    state:
        description:
            - Assert the state of the role assignment.
            - Use C(present) to create or update a role assignment and C(absent) to delete it.
        default: present
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Yunge Zhu(@yungezz)

'''

EXAMPLES = '''
    - name: Create a role assignment
      azure_rm_roleassignment:
        scope: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        assignee_object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        role_definition_id:
          "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.Authorization/roleDefinitions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

    - name: Delete a role assignment
      azure_rm_roleassignment:
        name: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        scope: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        state: absent

'''

RETURN = '''
id:
    description:
        - Id of current role assignment.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.Authorization/roleAssignments/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
'''

import uuid
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError

except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRoleAssignment(AzureRMModuleBase):
    """Configuration class for an Azure RM Role Assignment"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str'),
            scope=dict(type='str'),
            assignee_object_id=dict(type='str'),
            role_definition_id=dict(type='str'),
            role_assignment_id=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent'])
        )

        self.name = None
        self.scope = None
        self.assignee_object_id = None
        self.role_definition_id = None

        self.results = dict(
            changed=False,
            id=None,
        )
        self.state = None

        mutually_exclusive = [['name', 'role_assignment_id'], ['scope', 'role_assignment_id']]

        super(AzureRMRoleAssignment, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name and not self.scope:
            self.fail("Parameter Error: setting name requires a scope to also be set.")
        if not self.scope and not self.role_assignment_id:
            self.fail("Parameter Error: either a scope or an assignment_id must be set.")

        existing_assignment = None
        response = None

        # TODO get existing assignment
        existing_assignment = self.get_roleassignment()

        if existing_assignment:
            self.results['id'] = existing_assignment.get('id')
            self.results['name'] = existing_assignment.get('name')
            self.results['principal_id'] = existing_assignment.get('principal_id')
            self.results['principal_type'] = existing_assignment.get('principal_type')
            self.results['role_definition_id'] = existing_assignment.get('role_definition_id')
            self.results['scope'] = existing_assignment.get('scope')
            self.results['type'] = existing_assignment.get('assignment')

        if self.state == 'present':
            # check if the role assignment exists
            if not existing_assignment:
                self.log("Role assignment doesn't exist in this scope")

                self.results['changed'] = True

                if self.check_mode:
                    return self.results
                response = self.create_roleassignment()
                self.results['id'] = response['id']

            else:
                self.log("Role assignment already exists, not updatable")
                self.log('Result: {0}'.format(existing_assignment))

        elif self.state == 'absent':
            if existing_assignment:
                self.log("Delete role assignment")
                self.results['changed'] = True

                if self.check_mode:
                    return self.results

                self.delete_roleassignment(existing_assignment.get('id'))

                self.log('role assignment deleted')

            else:
                self.fail("role assignment {0} not exists.".format(self.name))

        return self.results

    def create_roleassignment(self):
        '''
        Creates role assignment.

        :return: deserialized role assignment
        '''
        self.log("Creating role assignment {0}".format(self.name))

        try:
            parameters = self.assignment_models.RoleAssignmentCreateParameters(role_definition_id=self.role_definition_id, principal_id=self.assignee_object_id)
            response = self.assignment_client.role_assignments.create(scope=self.scope,
                                                                      role_assignment_name=self.name,
                                                                      parameters=parameters)

        except CloudError as exc:
            self.log('Error attempting to create role assignment.')
            self.fail("Error creating role assignment: {0}".format(str(exc)))
        return self.roleassignment_to_dict(response)

    def delete_roleassignment(self, assignment_id):
        '''
        Deletes specified role assignment.

        :return: True
        '''
        self.log("Deleting the role assignment {0}".format(self.name))
        try:
            response = self.assignment_client.role_assignments.delete_by_id(role_id=assignment_id)
        except CloudError as e:
            self.log('Error attempting to delete the role assignment.')
            self.fail("Error deleting the role assignment: {0}".format(str(e)))

        return True

    def get_roleassignment(self):
        '''
        Gets the properties of the specified role assignment.

        :return: deserialized role assignment dictionary
        '''
        self.log("Checking if the role assignment {0} is present".format(self.name))

        role_assignment = None

        try:
            response = self.authorization_client.role_assignments.list()

            if self.name:
                response = [role_assignment for role_assignment in response if role_assignment.get('name') == self.name]
            if self.scope:
                response = [role_assignment for role_assignment in response if role_assignment.get('scope') == self.scope]
            if self.assignee_object_id:
                response = [role_assignment for role_assignment in response if role_assignment.get('assignee_object_id') == self.assignee_object_id]
            if self.role_definition_id:
                response = [role_assignment for role_assignment in response if role_assignment.get('role_definition_id') == self.role_definition_id]
            if self.id:
                response = [role_assignment for role_assignment in response if role_assignment.get('id') == self.id]
            if response:
                role_assignment = self.roleassignment_to_dict(response[0])

        except CloudError as ex:
            self.log("Error when fetching state from Azure.")

        return role_assignment

    def roleassignment_to_dict(self, assignment):
        return dict(
            id=assignment.id,
            name=assignment.name,
            principal_id=assignment.principal_id,
            principal_type=assignment.principal_type,
            role_definition_id=assignment.role_definition_id,
            scope=assignment.scope,
            type=assignment.type
        )


def main():
    """Main execution"""
    AzureRMRoleAssignment()


if __name__ == '__main__':
    main()
