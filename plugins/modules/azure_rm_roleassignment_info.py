#!/usr/bin/python
#
# Copyright (c) 2020 Paul Aiton, (@paultaiton)
# Copyright (c) 2019 Yunge Zhu, (@yungezz)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_roleassignment_info
version_added: "0.1.2"
short_description: Gets Azure Role Assignment facts
description:
    - Gets facts of Azure Role Assignment.

options:
    assignee:
        description:
            - Object id of a user, group or service principal.
            - Mutually exclusive with I(name) and I(id).
        aliases:
          - assignee_object_id
    id:
        description:
            - Fqid of role assignment to look up.
            - If set, I(role_definition_id) and I(scope) will be silently ignored.
            - Mutually exclusive with I(assignee) and I(name).
    name:
        description:
            - Name of role assignment.
            - Requires that I(scope) also be set.
            - Mutual exclusive with I(assignee) and I(id).
    role_definition_id:
        description:
            - Resource id of role definition.
    scope:
        description:
            - The scope to query for role assignments.
            - For example, use /subscriptions/{subscription-id}/ for a subscription.
            - /subscriptions/{subscription-id}/resourceGroups/{resourcegroup-name} for a resource group.
            - /subscriptions/{subscription-id}/resourceGroups/{resourcegroup-name}/providers/{resource-provider}/{resource-type}/{resource-name} for a resource.
            - By default will return all inhereted assignments from parent scopes, see I(strict_scope_match).
    strict_scope_match:
        description:
            - If strict_scope_match is True, role assignments will only be returned for the exact scope defined.
            - Inherited role assignments will be excluded from results.
            - Option will be silently ignored if no scope is provided.
        type: bool
        default: False

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Yunge Zhu(@yungezz)
    - Paul Aiton(@paultaiton)

'''

EXAMPLES = '''
    - name: Get role assignments for specific service principal
      azure_rm_roleassignment_info:
        assignee: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Get role assignments for specific scope that matches specific role definition
      azure_rm_roleassignment_info:
        scope: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        role_definition_id: /subscriptions/xxx-sub-guid-xxx/providers/Microsoft.Authorization/roleDefinitions/xxx-role-guid-xxxx

    - name: Get role assignments for specific scope with no inherited assignments
      azure_rm_roleassignment_info:
        scope: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        strict_scope_match: True

    - name: Get role assignments by name
      azure_rm_roleassignment_info:
        scope: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        name: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Get role assignments by id
      azure_rm_roleassignment_info:
        id: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.Authorization/roleAssignments/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
'''

RETURN = '''
roleassignments:
    description:
        - List of role assignments.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Id of role assignment.
            type: str
            returned: always
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/providers/Microsoft.Authorization/roleAssignments/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        name:
            description:
                - Name of role assignment.
            type: str
            returned: always
            sample: myRoleAssignment
        type:
            description:
                - Type of role assignment.
            type: str
            returned: always
            sample: custom
        principal_id:
            description:
                - Principal Id of the role assigned to.
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
            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        scope:
            description:
                - The role assignment scope.
            type: str
            returned: always
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
'''

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRoleAssignmentInfo(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            assignee=dict(type='str', aliases=['assignee_object_id']),
            id=dict(type='str'),
            name=dict(type='str'),
            role_definition_id=dict(type='str'),
            scope=dict(type='str'),
            strict_scope_match=dict(type='bool', default=False)
        )

        self.assignee = None
        self.id = None
        self.name = None
        self.role_definition_id = None
        self.scope = None
        self.strict_scope_match = None

        self.results = dict(
            changed=False,
            roleassignments=[]
        )

        mutually_exclusive = [['name', 'assignee', 'id']]

        super(AzureRMRoleAssignmentInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=False,
                                                        facts_module=True,
                                                        mutually_exclusive=mutually_exclusive)

    def exec_module(self, **kwargs):
        """Main module execution method"""
        is_old_facts = self.module._name == 'azure_rm_roleassignment_facts'
        if is_old_facts:
            self.module.deprecate("The 'azure_rm_roleassignment_facts' module has been renamed to 'azure_rm_roleassignment_info'", version=(2.9, ))

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.id:
            self.results['roleassignments'] = self.get_by_id()
        elif self.name and self.scope:
            self.results['roleassignments'] = self.get_by_name()
        elif self.name and not self.scope:
            self.fail("Parameter Error: Name requires a scope to also be set.")
        elif self.scope:
            self.results['roleassignments'] = self.list_by_scope()
        elif self.assignee:
            self.results['roleassignments'] = self.list_by_assignee()
        else:
            self.results['roleassignments'] = self.list_assignments()

        return self.results

    def get_by_id(self):
        '''
        Gets the role assignments by specific assignment id.

        :return: deserialized role assignment dictionary
        '''
        self.log("Lists role assignment by id {0}".format(self.id))

        results = []
        try:
            response = [self.authorization_client.role_assignments.get_by_id(role_id=self.id)]
            response = [self.roleassignment_to_dict(a) for a in response]
            results = response

        except Exception as ex:
            self.log("Didn't find role assignments id {0}".format(self.scope))

        return results

    def get_by_name(self):
        '''
        Gets the properties of the specified role assignment by name.

        :return: deserialized role assignment dictionary
        '''
        self.log("Gets role assignment {0} by name".format(self.name))

        results = []

        try:
            response = [self.authorization_client.role_assignments.get(scope=self.scope, role_assignment_name=self.name)]
            response = [self.roleassignment_to_dict(a) for a in response]

            # If role_definition_id is set, we only want results matching that id.
            if self.role_definition_id:
                response = [role_assignment for role_assignment in response if (role_assignment.get('role_definition_id').split('/')[-1].lower()
                                                                                == self.role_definition_id.split('/')[-1].lower())]

            results = response

        except Exception as ex:
            self.log("Didn't find role assignment {0} in scope {1}".format(self.name, self.scope))

        return results

    def list_by_assignee(self):
        '''
        Gets the role assignments by assignee.

        :return: deserialized role assignment dictionary
        '''
        self.log("Gets role assignment {0} by name".format(self.name))

        filter = "principalId eq '{0}'".format(self.assignee)
        return self.list_assignments(filter=filter)

    def list_assignments(self, filter=None):
        '''
        Returns a list of assignments.
        '''
        results = []

        try:
            response = list(self.authorization_client.role_assignments.list(filter=filter))
            response = [self.roleassignment_to_dict(a) for a in response]

            # If role_definition_id is set, we only want results matching that id.
            if self.role_definition_id:
                response = [role_assignment for role_assignment in response if (role_assignment.get('role_definition_id').split('/')[-1].lower()
                                                                                == self.role_definition_id.split('/')[-1].lower())]

            results = response

        except Exception as ex:
            self.log("Didn't find role assignments in subscription {0}.".format(self.subscription_id))

        return results

    def list_by_scope(self):
        '''
        Lists the role assignments by specific scope.

        :return: deserialized role assignment dictionary
        '''
        self.log("Lists role assignment by scope {0}".format(self.scope))

        results = []
        try:
            # atScope filter limits to exact scope plus parent scopes. Without it will return all children too.
            response = list(self.authorization_client.role_assignments.list_for_scope(scope=self.scope, filter='atScope()'))

            response = [self.roleassignment_to_dict(role_assignment) for role_assignment in response]

            # If assignee is set we only want results matching that assignee.
            if self.assignee:
                response = [role_assignment for role_assignment in response if role_assignment.get('principal_id').lower() == self.assignee.lower()]

            # If strict_scope_match is true we only want results matching exact scope.
            if self.strict_scope_match:
                response = [role_assignment for role_assignment in response if role_assignment.get('scope').lower() == self.scope.lower()]

            # If role_definition_id is set, we only want results matching that id.
            if self.role_definition_id:
                response = [role_assignment for role_assignment in response if (role_assignment.get('role_definition_id').split('/')[-1].lower()
                                                                                == self.role_definition_id.split('/')[-1].lower())]

            results = response

        except Exception as ex:
            self.log("Didn't find role assignments at scope {0}".format(self.scope))

        return results

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
    AzureRMRoleAssignmentInfo()


if __name__ == '__main__':
    main()
