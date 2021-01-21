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
module: azure_rm_registrationdefinition_info
version_added: '2.9'
short_description: Get RegistrationDefinition info.
description:
    - Get info of RegistrationDefinition.
options:
    scope:
        description:
            - Scope of the resource.
        required: true
        type: str
    registration_definition_id:
        description:
            - Guid of the registration definition.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - GuopengLin (@t-glin)

'''

EXAMPLES = '''
    - name: Get Registration Definition
      azure_rm_registrationdefinition_info: 
        registration_definition_id: 26c128c2-fefa-4340-9bb1-6e081c90ada2
        scope: subscription/0afefe50-734e-4610-8a82-a144ahf49dea

    - name: Get Registration Definitions
      azure_rm_registrationdefinition_info: 
        scope: subscription/0afefe50-734e-4610-8a82-a144ahf49dea

'''

RETURN = '''
registration_definitions:
    description: >-
        A list of dict results where the key is the name of the
        RegistrationDefinition and the values are the facts for that
        RegistrationDefinition.
    returned: always
    type: complex
    contains:
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
                            Authorization tuple containing principal id of the user/security
                            group or service principal and id of the build-in role.
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
                                    permissions that the security group/service principal/user
                                    must have on the projected subscription. This role cannot be
                                    an owner role.
                            returned: always
                            type: str
                            sample: null
                        delegated_role_definition_ids:
                            description:
                                - >-
                                    The delegatedRoleDefinitionIds field is required when the
                                    roleDefinitionId refers to the User Access Administrator Role.
                                    It is the list of role definition ids which define all the
                                    permissions that the user in the authorization can assign to
                                    other security groups/service principals/users.
                            type: list
                            sample: null
                eligible_authorizations:
                    description:
                        - >-
                            Eligible PIM authorization tuple containing principal id of the
                            user/security group or service principal, id of the built-in role,
                            and just-in-time access policy setting
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
                                    The role definition identifier. This role will delegate all
                                    the permissions that the security group/service principal/user
                                    must have on the projected subscription. This role cannot be
                                    an owner role.
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
                                            Maximum access duration in ISO 8601 format.  The default
                                            value is "PT8H".
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
        value:
            description:
                - List of registration definitions.
            type: list
            sample: null
            contains:
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
                                    Authorization tuple containing principal id of the
                                    user/security group or service principal and id of the
                                    build-in role.
                            returned: always
                            type: list
                            sample: null
                            contains:
                                principal_id:
                                    description:
                                        - >-
                                            Principal Id of the security group/service principal/user
                                            that would be assigned permissions to the projected
                                            subscription
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
                                            The role definition identifier. This role will define all
                                            the permissions that the security group/service
                                            principal/user must have on the projected subscription.
                                            This role cannot be an owner role.
                                    returned: always
                                    type: str
                                    sample: null
                                delegated_role_definition_ids:
                                    description:
                                        - >-
                                            The delegatedRoleDefinitionIds field is required when the
                                            roleDefinitionId refers to the User Access Administrator
                                            Role. It is the list of role definition ids which define
                                            all the permissions that the user in the authorization can
                                            assign to other security groups/service principals/users.
                                    type: list
                                    sample: null
                        eligible_authorizations:
                            description:
                                - >-
                                    Eligible PIM authorization tuple containing principal id of
                                    the user/security group or service principal, id of the
                                    built-in role, and just-in-time access policy setting
                            type: list
                            sample: null
                            contains:
                                principal_id:
                                    description:
                                        - >-
                                            Principal Id of the security group/service principal/user
                                            that would be delegated permissions to the projected
                                            subscription
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
                                            The role definition identifier. This role will delegate
                                            all the permissions that the security group/service
                                            principal/user must have on the projected subscription.
                                            This role cannot be an owner role.
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
                                                    Maximum access duration in ISO 8601 format.  The
                                                    default value is "PT8H".
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
        next_link:
            description:
                - Link to next page of registration definitions.
            type: str
            sample: null

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase
try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.managedservices import ManagedServicesClient
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRegistrationDefinitionInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            scope=dict(
                type='str',
                required=True
            ),
            registration_definition_id=dict(
                type='str'
            )
        )

        self.scope = None
        self.registration_definition_id = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        self.query_parameters = {}
        self.query_parameters['api-version'] = '2020-02-01-preview'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        self.mgmt_client = None
        super(AzureRMRegistrationDefinitionInfo, self).__init__(self.module_arg_spec, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.mgmt_client = self.get_mgmt_svc_client(ManagedServicesClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2020-02-01-preview')

        if (self.scope is not None and
            self.registration_definition_id is not None):
            self.results['registration_definitions'] = self.format_item(self.get())
        elif (self.scope is not None):
            self.results['registration_definitions'] = self.format_item(self.list())
        return self.results

    def get(self):
        response = None

        try:
            response = self.mgmt_client.registration_definitions.get(scope=self.scope,
                                                                     registration_definition_id=self.registration_definition_id)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list(self):
        response = None

        try:
            response = self.mgmt_client.registration_definitions.list(scope=self.scope)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def format_item(self, item):
        if hasattr(item, 'as_dict'):
            return [item.as_dict()]
        else:
            result = []
            items = list(item)
            for tmp in items:
                result.append(tmp.as_dict())
            return result


def main():
    AzureRMRegistrationDefinitionInfo()


if __name__ == '__main__':
    main()
