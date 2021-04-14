#!/usr/bin/python
#
# Copyright (c) 2020 Paul Aiton, (@paultaiton)
# Copyright (c) 2018 Yunge Zhu, (@yungezz)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_roleassignment
version_added: "0.1.2"
short_description: Manage Azure Role Assignment
description:
    - Create and delete instance of Azure Role Assignment.

options:
    assignee_object_id:
        description:
            - The object id of assignee. This maps to the ID inside the Active Directory.
            - It can point to a user, service principal or security group.
            - Required when creating role assignment.
        aliases:
          - assignee
    id:
        description:
            - Fully qualified id of assignment to delete or create.
            - Mutually Exclusive with I(scope) and I(name)
    name:
        description:
            - Unique name of role assignment.
            - The role assignment name must be a GUID, sample as "3ce0cbb0-58c4-4e6d-a16d-99d86a78b3ca".
            - Mutually Exclusive with I(id)
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
            - Mutually Exclusive with I(id)
    state:
        description:
            - Assert the state of the role assignment.
            - Use C(present) to create or update a role assignment and C(absent) to delete it.
            - If C(present), then I(role_definition_id) and I(assignee_object_id) are both required
        default: present
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Yunge Zhu(@yungezz)
    - Paul Aiton(@paultaiton)

'''

EXAMPLES = '''
    - name: Create a role assignment
      azure_rm_roleassignment:
        scope: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        assignee_object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        role_definition_id:
          "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.Authorization/roleDefinitions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

    - name: Create a role assignment
      azure_rm_roleassignment:
        name: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        scope: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        assignee_object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        role_definition_id:
          "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.Authorization/roleDefinitions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

    - name: Delete a role assignment
      azure_rm_roleassignment:
        name: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        scope: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        state: absent

    - name: Delete a role assignment
      azure_rm_roleassignment:
        id: /subscriptions/xxx-sub-guid-xxx/resourceGroups/rgname/providers/Microsoft.Authorization/roleAssignments/xxx-assign-guid-xxx"

    - name: Delete a role assignment
      azure_rm_roleassignment:
        scope: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        assignee_object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        role_definition_id:
          "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.Authorization/roleDefinitions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
'''

RETURN = '''
id:
    description:
        - Id of current role assignment.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.Authorization/roleAssignments/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
name:
    description:
        - Name of role assignment.
    type: str
    returned: always
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
type:
    description:
        - Type of role assignment.
    type: str
    returned: always
    sample: Microsoft.Authorization/roleAssignments
assignee_object_id:
    description:
        - Principal Id of the role assignee.
    type: str
    returned: always
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
principal_type:
    description:
        - Principal type of the role assigned to.
    type: str
    returned: always
    sample: ServicePrincipal
role_definition_id:
    description:
        - Role definition id that was assigned to principal_id.
    type: str
    returned: always
    sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.Authorization/roleDefinitions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
scope:
    description:
        - The role assignment scope.
    type: str
    returned: always
    sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
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
            assignee_object_id=dict(type='str', aliases=['assignee']),
            id=dict(type='str'),
            name=dict(type='str'),
            role_definition_id=dict(type='str'),
            scope=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent'])
        )

        self.assignee_object_id = None
        self.id = None
        self.name = None
        self.role_definition_id = None
        self.scope = None
        self.state = None

        self.results = dict(
            changed=False,
            id=None,
        )

        mutually_exclusive = [['name', 'id'], ['scope', 'id']]
        required_one_of = [['scope', 'id']]
        required_if = [
            ["state", "present", ["assignee_object_id", "role_definition_id"]]
        ]

        super(AzureRMRoleAssignment, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False,
                                                    required_one_of=required_one_of,
                                                    required_if=required_if,
                                                    mutually_exclusive=mutually_exclusive)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name and not self.scope:
            self.fail("Parameter Error: setting name requires a scope to also be set.")

        existing_assignment = None
        response = None

        existing_assignment = self.get_roleassignment()

        if existing_assignment:
            self.set_results(existing_assignment)

        if self.state == 'present':
            # check if the role assignment exists
            if not existing_assignment:
                self.log("Role assignment doesn't exist in this scope")

                self.results['changed'] = True

                if self.check_mode:
                    return self.results
                response = self.create_roleassignment()
                self.set_results(response)

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
                # If assignment doesn't exist, that's the desired state.
                self.log("role assignment {0} does not exist.".format(self.name))

        return self.results

    def create_roleassignment(self):
        '''
        Creates role assignment.

        :return: deserialized role assignment
        '''
        self.log("Creating role assignment {0}".format(self.name))

        response = None
        try:
            # pylint: disable=missing-kwoa
            parameters = self.authorization_models.RoleAssignmentCreateParameters(role_definition_id=self.role_definition_id,
                                                                                  principal_id=self.assignee_object_id)
            if self.id:
                response = self.authorization_client.role_assignments.create_by_id(role_id=self.id,
                                                                                   parameters=parameters)
            elif self.scope:
                if not self.name:
                    self.name = str(uuid.uuid4())
                response = self.authorization_client.role_assignments.create(scope=self.scope,
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
            response = self.authorization_client.role_assignments.delete_by_id(role_id=assignment_id)
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

        if self.id:
            try:
                response = self.authorization_client.role_assignments.get_by_id(role_id=self.id)
                role_assignment = self.roleassignment_to_dict(response)
                if role_assignment and self.assignee_object_id and role_assignment.get('assignee_object_id') != self.assignee_object_id:
                    self.fail('State Mismatch Error: The assignment ID exists, but does not match the provided assignee.')

                if role_assignment and self.role_definition_id and (role_assignment.get('role_definition_id').split('/')[-1].lower()
                                                                    != self.role_definition_id[-1].lower()):
                    self.fail('State Mismatch Error: The assignment ID exists, but does not match the provided role.')

            except CloudError as ex:
                self.log("Didn't find role assignments id {0}".format(self.id))

        elif self.name and self.scope:
            try:
                response = self.authorization_client.role_assignments.get(scope=self.scope, role_assignment_name=self.name)
                role_assignment = self.roleassignment_to_dict(response)
                if role_assignment and self.assignee_object_id and role_assignment.get('assignee_object_id') != self.assignee_object_id:
                    self.fail('State Mismatch Error: The assignment name exists, but does not match the provided assignee.')

                if role_assignment and self.role_definition_id and (role_assignment.get('role_definition_id').split('/')[-1].lower()
                                                                    != self.role_definition_id[-1].lower()):
                    self.fail('State Mismatch Error: The assignment name exists, but does not match the provided role.')

            except CloudError as ex:
                self.log("Didn't find role assignment by name {0} at scope {1}".format(self.name, self.scope))

        else:
            try:
                if self.scope and self.assignee_object_id and self.role_definition_id:
                    response = list(self.authorization_client.role_assignments.list())
                    response = [self.roleassignment_to_dict(role_assignment) for role_assignment in response]
                    response = [role_assignment for role_assignment in response if role_assignment.get('scope') == self.scope]
                    response = [role_assignment for role_assignment in response if role_assignment.get('assignee_object_id') == self.assignee_object_id]
                    response = [role_assignment for role_assignment in response if (role_assignment.get('role_definition_id').split('/')[-1].lower()
                                                                                    == self.role_definition_id.split('/')[-1].lower())]
                else:
                    self.fail('If id or name are not supplied, then assignee_object_id and role_definition_id are required.')
                if response:
                    role_assignment = response[0]
            except CloudError as ex:
                self.log("Didn't find role assignments for subscription {0}".format(self.subscription_id))

        return role_assignment

    def set_results(self, assignment):
        self.results['id'] = assignment.get('id')
        self.results['name'] = assignment.get('name')
        self.results['type'] = assignment.get('type')
        self.results['assignee_object_id'] = assignment.get('assignee_object_id')
        self.results['principal_type'] = assignment.get('principal_type')
        self.results['role_definition_id'] = assignment.get('role_definition_id')
        self.results['scope'] = assignment.get('scope')

    def roleassignment_to_dict(self, assignment):
        return dict(
            assignee_object_id=assignment.principal_id,
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
