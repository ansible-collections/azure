#!/usr/bin/python
#
# Copyright (c) 2020 Fred-Sun, (@Fred-Sun)
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
version_added: '1.3.0'
short_description: Manage Azure RegistrationDefinition instance
description:
    - Create, update and delete instance of Azure RegistrationDefinition.
options:
    registration_definition_id:
        description:
            - ID of the registration definition.
            - If is not specified, an UUID will be generated for it.
        type: str
    scope:
        description:
            - The subscription ID defines the subscription in which the registration definition will be created.
            - If not specified, will use the subscription derived from AzureRMAuth.
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
                    - Authorization tuple containing principal ID of the user/security group or service principal and ID of the build-in role.
                required: true
                type: list
                suboptions:
                    principal_id:
                        description:
                            - Principal ID of the security group/service principal/user that would be assigned permissions to the projected subscription.
                        required: true
                        type: str
                    role_definition_id:
                        description:
                            - The role definition identifier.
                            - This role will define all the permissions that the security group/service principal/user must have on the projected subscription.
                            - This role cannot be an owner role.
                        required: true
                        type: str
            registration_definition_name:
                description:
                    - Name of the registration definition.
                type: str
            managed_by_tenant_id:
                description:
                    - ID of the managedBy tenant.
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
            - Use C(present) to create or update an RegistrationDefinition and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Fred-Sun (@Fred-Sun)

'''

EXAMPLES = '''
    - name: Create Registration Definition without scope
      azure_rm_registrationdefinition:
        registration_definition_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        properties:
          description: test
          authorizations:
            - principal_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
              role_definition_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
          managed_by_tenant_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
          registration_definition_name: def4

    - name: Create Registration Definition with scope
      azure_rm_registrationdefinition:
        scope: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        registration_definition_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        properties:
          description: test
          authorizations:
            - principal_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
              role_definition_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
          managed_by_tenant_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
          registration_definition_name: def5

    - name: Delete Registration Definition
      azure_rm_registrationdefinition:
        registration_definition_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        state: absent

'''

RETURN = '''
state:
    description:
        - The state info of the registration assignment.
    type: complex
    returned: always
    contains:
        properties:
            description:
                - Properties of a registration definition.
            returned: always
            type: complex
            contains:
                description:
                    description:
                        - Description of the registration definition.
                    returned: always
                    type: str
                    sample: test
                authorizations:
                    description:
                        - Authorization tuple containing principal ID of the user/security group or service principal and ID of the build-in role.
                    returned: always
                    type: complex
                    contains:
                        principal_id:
                            description:
                                - Principal ID of the security group/service principal/user that would be assigned permissions to the projected subscription
                            returned: always
                            type: str
                            sample: 99e3227f-8701-4099-869f-bc3efc7f1e64
                        role_definition_id:
                            description:
                                - The role definition identifier.
                                - This role will define all the permissions that the security group/service principal/user must have on the subscription.
                                - This role cannot be an owner role.
                            returned: always
                            type: str
                            sample: b24988ac-6180-42a0-ab88-20f7382dd24c
                registration_definition_name:
                    description:
                        - Name of the registration definition.
                    returned: always
                    type: str
                    sample: null
                managed_by_tenant_id:
                    description:
                        - ID of the managedBy tenant.
                    returned: always
                    type: str
                    sample: null
        plan:
            description:
                - Plan details for the managed services.
            returned: always
            type: complex
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
            returned: always
            type: str
            sample: null
        type:
            description:
                - Type of the resource.
            returned: always
            type: str
            sample: Microsoft.ManagedServices/registrationDefinitions
        name:
            description:
                - Name of the registration definition.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/providers/Microsoft.ManagedServices/registrationDefinitions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

'''
import uuid
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
                type='str'
            ),
            registration_definition_id=dict(
                type='str',
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
                            role_definition_id=dict(
                                type='str',
                                disposition='role_definition_id',
                                required=True
                            )
                        )
                    ),
                    registration_definition_name=dict(
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

        if self.registration_definition_id is None:
            self.registration_definition_id = str(uuid.uuid4())

        if not self.scope:
            self.scope = "/subscriptions/" + self.subscription_id
        else:
            self.scope = "/subscriptions/" + self.scope

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ManagedServicesClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2019-09-01',
                                                    suppress_subscription_id=True)

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
            self.results['state'] = response
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            self.delete_resource()
        else:
            self.results['changed'] = False
            response = old_response

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
