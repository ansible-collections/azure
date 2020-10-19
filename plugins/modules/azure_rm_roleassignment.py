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

        old_response = None
        response = None

        # TODO get existing assignment
        old_response = self.get_roleassignment()

        if old_response:
            self.results['id'] = old_response['id']

        if self.state == 'present':
            # check if the role assignment exists
            if not old_response:
                self.log("Role assignment doesn't exist in this scope")

                self.results['changed'] = True

                if self.check_mode:
                    return self.results
                response = self.create_roleassignment()
                self.results['id'] = response['id']

            else:
                self.log("Role assignment already exists, not updatable")
                self.log('Result: {0}'.format(old_response))

        elif self.state == 'absent':
            if old_response:
                self.log("Delete role assignment")
                self.results['changed'] = True

                if self.check_mode:
                    return self.results

                self.delete_roleassignment(old_response['id'])

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
            # pylint: disable=missing-kwoa
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
        if not self.scope:
            scope = '/subscriptions/' + self.subscription_id
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

        response = None

        if self.role_assignment_id:
            response = [self.authorization_client.role_assignments.get_by_id(role_id=self.role_assignment_id)]
        elif self.name and self.scope:
            response = [self.authorization_client.role_assignments.get(scope=self.scope, role_assignment_name=self.name)]

        try:
            response = list(self.assignment_client.role_assignments.list())
            if response:
                for assignment in response:
                    if assignment.name == self.name and assignment.scope == self.scope:
                        return self.roleassignment_to_dict(assignment)

        except CloudError as ex:
            self.log("Didn't find role assignment {0} in scope {1}".format(self.name, self.scope))

        return False

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
