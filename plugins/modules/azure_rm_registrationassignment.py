#!/usr/bin/python
#
# Copyright (c) 2020 Fred-Sun, (@Fred-Sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_registrationassignment
version_added: '1.3.0'
short_description: Manage Azure RegistrationAssignment instance
description:
    - Create and delete instance of Azure RegistrationAssignment.
options:
    scope:
        description:
            - Scope of the registration assignment. Can be in subscription or group level.
        required: true
        type: str
    registration_assignment_id:
        description:
            - ID of the registration assignment.
            - If is not specified, an UUID will be generated for it.
        type: str
    properties:
        description:
            - Properties of a registration assignment.
        type: dict
        suboptions:
            registration_definition_id:
                description:
                  - Fully qualified path of the registration definition.
                required: true
                type: str
    state:
        description:
            - Assert the state of the RegistrationAssignment.
            - Use C(present) to create or update an RegistrationAssignment and C(absent) to delete it.
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
    - name: Delete Registration Assignment
      azure_rm_registrationassignment:
        scope: subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        registration_assignment_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        state: absent


    - name: Create Registration Assignment in subscription level
      azure_rm_registrationassignment:
        scope: subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        registration_assignment_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        properties:
          registration_definition_id: /subscriptions/xxx-xxx/providers/Microsoft.ManagedServices/registrationDefinitions/xxx-xxx


    - name: Create Registration Assignment in resourcegroup level with randomly generating registration_assignment_id
      azure_rm_registrationassignment:
        scope: subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup
        properties:
          registration_definition_id: /subscriptions/xxx-xxx/providers/Microsoft.ManagedServices/registrationDefinitions/xxx-xxx

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
                - Properties of a registration assignment.
            returned: always
            type: complex
            contains:
                registration_definition_id:
                    description:
                        - Fully qualified path of the registration definition.
                    returned: always
                    type: str
                    sample: null
        id:
            description:
                - The fully qualified path of the registration assignment.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxx/providers/Microsoft.ManagedServices/registrationAssignments/xxx-xxx
        type:
            description:
                - Type of the resource.
            returned: always
            type: str
            sample: Microsoft.ManagedServices/registrationAssignments
        name:
            description:
                - Name of the registration assignment.
            returned: always
            type: str
            sample: 9b2895ec-fb1e-4a1e-a978-abd9933d6b20

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


class AzureRMRegistrationAssignment(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            scope=dict(
                type='str',
                required=True
            ),
            registration_assignment_id=dict(
                type='str',
            ),
            properties=dict(
                type='dict',
                disposition='/properties',
                options=dict(
                    registration_definition_id=dict(
                        type='str',
                        disposition='registration_definition_id',
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
        self.registration_assignment_id = None
        self.expand_registration_definition = False
        self.body = {}

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRegistrationAssignment, self).__init__(derived_arg_spec=self.module_arg_spec,
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
        if self.registration_assignment_id is None:
            self.registration_assignment_id = str(uuid.uuid4())

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
            self.results['state'] = response

        if self.state == 'present':
            if self.results['state'].get('properties', None) is not None:
                registration_definition_id = self.results['state']['properties']['registration_definition_id']
                self.results['state']['properties'].clear()
                self.results['state']['properties']['registration_definition_id'] = registration_definition_id

        return self.results

    def create_update_resource(self):
        try:
            response = self.mgmt_client.registration_assignments.create_or_update(scope=self.scope,
                                                                                  registration_assignment_id=self.registration_assignment_id,
                                                                                  properties=self.body.get('properties', None),
                                                                                  request_body=self.body)
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the RegistrationAssignment instance.')
            self.fail('Error creating the RegistrationAssignment instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.mgmt_client.registration_assignments.delete(scope=self.scope,
                                                                        registration_assignment_id=self.registration_assignment_id)
        except CloudError as e:
            self.log('Error attempting to delete the RegistrationAssignment instance.')
            self.fail('Error deleting the RegistrationAssignment instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.mgmt_client.registration_assignments.get(scope=self.scope,
                                                                     registration_assignment_id=self.registration_assignment_id,
                                                                     expand_registration_definition=self.expand_registration_definition)
        except Exception as e:
            return False
        return response.as_dict()


def main():
    AzureRMRegistrationAssignment()


if __name__ == '__main__':
    main()
