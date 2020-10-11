#!/usr/bin/python
#
# Copyright (c) 2020 Paul Aiton, (@paultaiton)
# Copyright (c) 2019 Yunge Zhu, (@yungezz)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_roleassignment_info
version_added: "0.1.2"
short_description: Gets Azure Role Assignment facts
description:
    - Gets facts of Azure Role Assignment.

options:
    scope:
        description:
            - The scope to query for role assignments.
            - For example, use /subscriptions/{subscription-id}/ for a subscription.
            - /subscriptions/{subscription-id}/resourceGroups/{resourcegroup-name} for a resource group.
            - /subscriptions/{subscription-id}/resourceGroups/{resourcegroup-name}/providers/{resource-provider}/{resource-type}/{resource-name} for a resource.
            - By default will return all inhereted assignments from parent scopes, see I(strict_scope_match).
    name:
        description:
            - Name of role assignment.
            - Mutual exclusive with I(assignee).
            - Requires that I(scope) also be set.
    assignee:
        description:
            - Object id of a user, group or service principal.
            - Mutually exclusive with I(name).
    role_definition_id:
        description:
            - Resource id of role definition.
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

    - name: Get role assignments for specific scope
      azure_rm_roleassignment_info:
        scope: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
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
    from msrestazure.azure_exceptions import CloudError
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

def roleassignment_to_dict(assignment):
    return dict(
        id=assignment.id,
        name=assignment.name,
        type=assignment.type,
        principal_id=assignment.principal_id,
        role_definition_id=assignment.role_definition_id,
        scope=assignment.scope
    )


class AzureRMRoleAssignmentInfo(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str'),
            scope=dict(type='str'),
            assignee=dict(type='str'),
            role_definition_id=dict(type='str'),
            strict_scope_match=dict(type=bool, default=False)
        )

        self.name = None
        self.scope = None
        self.assignee = None
        self.role_definition_id = None
        self.strict_scope_match = None

        self.results = dict(
            changed=False,
            roleassignments=[]
        )

        mutually_exclusive = [['name', 'assignee']]

        super(AzureRMRoleAssignmentInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        if self.assignee:
            self.results['roleassignments'] = self.list_by_assignee()
        elif self.name and self.scope:
            self.results['roleassignments'] = self.get_by_name()
        elif self.scope:
            self.results['roleassignments'] = self.list_by_scope()
        elif self.name:
            self.fail("Parameter Error: Name requires a scope to also be set.")
        else:
            self.fail("Parameter Error: Please specify assignee or scope.")

        return self.results

    def get_by_name(self):
        '''
        Gets the properties of the specified role assignment by name.

        :return: deserialized role assignment dictionary
        '''
        self.log("Gets role assignment {0} by name".format(self.name))

        results = []

        try:
            response = self.authorization_client.role_assignments.get(scope=self.scope, role_assignment_name=self.name)

            if response:
                response = roleassignment_to_dict(response)

                if self.role_definition_id:
                    if self.role_definition_id == response['role_definition_id']:
                        results.append(response)
                else:
                        results.append(response)

        except CloudError as ex:
            self.log("Didn't find role assignment {0} in scope {1}".format(self.name, self.scope))

        return results

    def list_by_assignee(self):
        '''
        Gets the role assignments by assignee.

        :return: deserialized role assignment dictionary
        '''
        self.log("Gets role assignment {0} by name".format(self.name))

        results = []
        filter = "principalId eq '{0}'".format(self.assignee)
        response = self.list_assignments(filter=filter)

        return results

    def list_assignments(self, filter=None):
        '''
        Returns a list of assignments.
        '''
        results = []
        try:
            response = self.authorization_client.role_assignments.list(filter=filter)

            if response and len(response) > 0:
                response = [roleassignment_to_dict(a) for a in response]

                if self.role_definition_id:
                    for role in response:
                        if role['role_definition_id'] == self.role_definition_id:
                            results.append(r)
                else:
                    results = response

        except CloudError as ex:
            self.log("Didn't find role assignments to assignee {0}".format(self.assignee))

        return results

    def list_by_scope(self):
        '''
        Lists the role assignments by specific scope.

        :return: deserialized role assignment dictionary
        '''
        self.log("Lists role assignment by scope {0}".format(self.scope))

        results = []
        try:
            if self.strict_scope_match:
                response = list(self.authorization_client.role_assignments.list_for_scope(scope=self.scope))
            else:
                response = list(self.authorization_client.role_assignments.list_for_scope(scope=self.scope, filter='atScope()'))

            if response and len(response) > 0:
                response = [roleassignment_to_dict(a) for a in response]

                if self.role_definition_id:
                    for r in response:
                        if r['role_definition_id'] == self.role_definition_id:
                            results.append(r)
                else:
                    results = response

        except CloudError as ex:
            self.log("Didn't find role assignments to scope {0}".format(self.scope))

        return results


def main():
    """Main execution"""
    AzureRMRoleAssignmentInfo()


if __name__ == '__main__':
    main()
