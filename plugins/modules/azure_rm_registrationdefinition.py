#!/usr/bin/python
#
# Copyright (c) 2020 GuopengLin, (@t-glin)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_registrationdefinition
version_added: '2.9'
short_description: Manage Azure RegistrationDefinition instance.
description:
    - 'Create, update and delete instance of Azure RegistrationDefinition.'
options:
    scope:
        description:
            - Scope of the resource.
        required: true
        type: str
    registration_definition_id:
        description:
            - Guid of the registration definition.
        required: true
        type: str
    properties:
        description:
            - Properties of a registration definition.
        type: dict
        suboptions:
            description:
                description:
                    - Description of the registration definition.
                type: str
            authorizations:
                description:
                    - >-
                        Authorization tuple containing principal id of the user/security
                        group or service principal and id of the build-in role.
                required: true
                type: list
                suboptions:
                    principal_id:
                        description:
                            - >-
                                Principal Id of the security group/service principal/user that
                                would be assigned permissions to the projected subscription
                        required: true
                        type: str
                    principal_id_display_name:
                        description:
                            - Display name of the principal Id.
                        type: str
                    role_definition_id:
                        description:
                            - >-
                                The role definition identifier. This role will define all the
                                permissions that the security group/service principal/user must
                                have on the projected subscription. This role cannot be an owner
                                role.
                        required: true
                        type: str
                    delegated_role_definition_ids:
                        description:
                            - >-
                                The delegatedRoleDefinitionIds field is required when the
                                roleDefinitionId refers to the User Access Administrator Role.
                                It is the list of role definition ids which define all the
                                permissions that the user in the authorization can assign to
                                other security groups/service principals/users.
                        type: list
            eligible_authorizations:
                description:
                    - >-
                        Eligible PIM authorization tuple containing principal id of the
                        user/security group or service principal, id of the built-in role,
                        and just-in-time access policy setting
                type: list
                suboptions:
                    principal_id:
                        description:
                            - >-
                                Principal Id of the security group/service principal/user that
                                would be delegated permissions to the projected subscription
                        required: true
                        type: str
                    principal_id_display_name:
                        description:
                            - Display name of the principal Id.
                        type: str
                    role_definition_id:
                        description:
                            - >-
                                The role definition identifier. This role will delegate all the
                                permissions that the security group/service principal/user must
                                have on the projected subscription. This role cannot be an owner
                                role.
                        required: true
                        type: str
                    just_in_time_access_policy:
                        description:
                            - Just-in-time access policy setting.
                        type: dict
                        suboptions:
                            multi_factor_auth_provider:
                                description:
                                    - MFA provider.
                                required: true
                                type: str
                                choices:
                                    - Azure
                                    - None
                            maximum_activation_duration:
                                description:
                                    - >-
                                        Maximum access duration in ISO 8601 format.  The default
                                        value is "PT8H".
                                type: str
            name:
                description:
                    - Name of the registration definition.
                type: str
            managed_by_tenant_id:
                description:
                    - Id of the managedBy tenant.
                required: true
                type: str
    plan:
        description:
            - Plan details for the managed services.
        type: dict
        suboptions:
            name:
                description:
                    - The plan name.
                required: true
                type: str
            publisher:
                description:
                    - The publisher ID.
                required: true
                type: str
            product:
                description:
                    - The product code.
                required: true
                type: str
            version:
                description:
                    - The plan's version.
                required: true
                type: str
    state:
        description:
            - Assert the state of the RegistrationDefinition.
            - >-
                Use C(present) to create or update an RegistrationDefinition and
                C(absent) to delete it.
        default: present
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - GuopengLin (@t-glin)

'''

EXAMPLES = '''
    - name: Delete Registration Definition
      azure_rm_registrationdefinition: 
        registration_definition_id: 26c128c2-fefa-4340-9bb1-6e081c90ada2
        scope: subscription/0afefe50-734e-4610-8a82-a144ahf49dea

    - name: Put Registration Definition
      azure_rm_registrationdefinition: 
        registration_definition_id: 26c128c2-fefa-4340-9bb1-6e081c90ada2
        scope: subscription/0afefe50-734e-4610-8a82-a144ahf49dea

'''

RETURN = '''
properties:
    description:
        - Properties of a registration definition.
    type: dict
    sample: null
    contains:
        description:
            description:
                - Description of the registration definition.
            type: str
            sample: null
        authorizations:
            description:
                - >-
                    Authorization tuple containing principal id of the user/security group
                    or service principal and id of the build-in role.
            returned: always
            type: list
            sample: null
            contains:
                principal_id:
                    description:
                        - >-
                            Principal Id of the security group/service principal/user that
                            would be assigned permissions to the projected subscription
                    returned: always
                    type: str
                    sample: null
                principal_id_display_name:
                    description:
                        - Display name of the principal Id.
                    type: str
                    sample: null
                role_definition_id:
                    description:
                        - >-
                            The role definition identifier. This role will define all the
                            permissions that the security group/service principal/user must
                            have on the projected subscription. This role cannot be an owner
                            role.
                    returned: always
                    type: str
                    sample: null
                delegated_role_definition_ids:
                    description:
                        - >-
                            The delegatedRoleDefinitionIds field is required when the
                            roleDefinitionId refers to the User Access Administrator Role. It
                            is the list of role definition ids which define all the
                            permissions that the user in the authorization can assign to other
                            security groups/service principals/users.
                    type: list
                    sample: null
        eligible_authorizations:
            description:
                - >-
                    Eligible PIM authorization tuple containing principal id of the
                    user/security group or service principal, id of the built-in role, and
                    just-in-time access policy setting
            type: list
            sample: null
            contains:
                principal_id:
                    description:
                        - >-
                            Principal Id of the security group/service principal/user that
                            would be delegated permissions to the projected subscription
                    returned: always
                    type: str
                    sample: null
                principal_id_display_name:
                    description:
                        - Display name of the principal Id.
                    type: str
                    sample: null
                role_definition_id:
                    description:
                        - >-
                            The role definition identifier. This role will delegate all the
                            permissions that the security group/service principal/user must
                            have on the projected subscription. This role cannot be an owner
                            role.
                    returned: always
                    type: str
                    sample: null
                just_in_time_access_policy:
                    description:
                        - Just-in-time access policy setting.
                    type: dict
                    sample: null
                    contains:
                        multi_factor_auth_provider:
                            description:
                                - MFA provider.
                            returned: always
                            type: str
                            sample: null
                        maximum_activation_duration:
                            description:
                                - >-
                                    Maximum access duration in ISO 8601 format.  The default value
                                    is "PT8H".
                            type: str
                            sample: null
        name:
            description:
                - Name of the registration definition.
            type: str
            sample: null
        managed_by_tenant_id:
            description:
                - Id of the managedBy tenant.
            returned: always
            type: str
            sample: null
plan:
    description:
        - Plan details for the managed services.
    type: dict
    sample: null
    contains:
        name:
            description:
                - The plan name.
            returned: always
            type: str
            sample: null
        publisher:
            description:
                - The publisher ID.
            returned: always
            type: str
            sample: null
        product:
            description:
                - The product code.
            returned: always
            type: str
            sample: null
        version:
            description:
                - The plan's version.
            returned: always
            type: str
            sample: null
id:
    description:
        - Fully qualified path of the registration definition.
    type: str
    sample: null
type:
    description:
        - Type of the resource.
    type: str
    sample: null
name:
    description:
        - Name of the registration definition.
    type: str
    sample: null

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.managedservices import ManagedServicesClient
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRegistrationDefinition(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            scope=dict(
                type='str',
                required=True
            ),
            registration_definition_id=dict(
                type='str',
                required=True
            ),
            properties=dict(
                type='dict',
                disposition='/properties',
                options=dict(
                    description=dict(
                        type='str',
                        disposition='description'
                    ),
                    authorizations=dict(
                        type='list',
                        disposition='authorizations',
                        required=True,
                        elements='dict',
                        options=dict(
                            principal_id=dict(
                                type='str',
                                disposition='principal_id',
                                required=True
                            ),
                            principal_id_display_name=dict(
                                type='str',
                                disposition='principal_id_display_name'
                            ),
                            role_definition_id=dict(
                                type='str',
                                disposition='role_definition_id',
                                required=True
                            ),
                            delegated_role_definition_ids=dict(
                                type='list',
                                disposition='delegated_role_definition_ids',
                                elements='uuid'
                            )
                        )
                    ),
                    eligible_authorizations=dict(
                        type='list',
                        disposition='eligible_authorizations',
                        elements='dict',
                        options=dict(
                            principal_id=dict(
                                type='str',
                                disposition='principal_id',
                                required=True
                            ),
                            principal_id_display_name=dict(
                                type='str',
                                disposition='principal_id_display_name'
                            ),
                            role_definition_id=dict(
                                type='str',
                                disposition='role_definition_id',
                                required=True
                            ),
                            just_in_time_access_policy=dict(
                                type='dict',
                                disposition='just_in_time_access_policy',
                                options=dict(
                                    multi_factor_auth_provider=dict(
                                        type='str',
                                        disposition='multi_factor_auth_provider',
                                        choices=['Azure',
                                                 'None'],
                                        required=True
                                    ),
                                    maximum_activation_duration=dict(
                                        type='str',
                                        disposition='maximum_activation_duration'
                                    )
                                )
                            )
                        )
                    ),
                    name=dict(
                        type='str',
                        disposition='registration_definition_name'
                    ),
                    managed_by_tenant_id=dict(
                        type='str',
                        disposition='managed_by_tenant_id',
                        required=True
                    )
                )
            ),
            plan=dict(
                type='dict',
                disposition='/plan',
                options=dict(
                    name=dict(
                        type='str',
                        disposition='name',
                        required=True
                    ),
                    publisher=dict(
                        type='str',
                        disposition='publisher',
                        required=True
                    ),
                    product=dict(
                        type='str',
                        disposition='product',
                        required=True
                    ),
                    version=dict(
                        type='str',
                        disposition='version',
                        required=True
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.scope = None
        self.registration_definition_id = None
        self.body = {}

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRegistrationDefinition, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                            supports_check_mode=True,
                                                            supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_parameters(self.module_arg_spec, self.body, 0)

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ManagedServicesClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    suppress_subscription_id=True,
                                                    api_version='2020-02-01-preview')


        old_response = self.get_resource()

        if not old_response:
            if self.state == 'present':
                self.to_do = Actions.Create
        else:
            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                modifiers = {}
                self.create_compare_modifiers(self.module_arg_spec, '', modifiers)
                self.results['modifiers'] = modifiers
                self.results['compare'] = []
                if not self.default_compare(modifiers, self.body, old_response, '', self.results):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.create_update_resource()
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            self.delete_resource()
        else:
            self.results['changed'] = False
            response = old_response
            self.result['state'] = response

        return self.results

    def create_update_resource(self):
        try:
            response = self.mgmt_client.registration_definitions.create_or_update(registration_definition_id=self.registration_definition_id,
                                                                                  scope=self.scope,
                                                                                  plan=self.body.get('plan', None),
                                                                                  properties=self.body.get('properties', None),
                                                                                  request_body=self.body)
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the RegistrationDefinition instance.')
            self.fail('Error creating the RegistrationDefinition instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.mgmt_client.registration_definitions.delete(registration_definition_id=self.registration_definition_id,
                                                                        scope=self.scope)
        except CloudError as e:
            self.log('Error attempting to delete the RegistrationDefinition instance.')
            self.fail('Error deleting the RegistrationDefinition instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.mgmt_client.registration_definitions.get(scope=self.scope,
                                                                     registration_definition_id=self.registration_definition_id)
        except Exception as e:
            return False
        return response.as_dict()


def main():
    AzureRMRegistrationDefinition()


if __name__ == '__main__':
    main()
