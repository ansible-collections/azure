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
module: azure_rm_registrationassignment
version_added: '2.9'
short_description: Manage Azure RegistrationAssignment instance.
description:
    - 'Create, update and delete instance of Azure RegistrationAssignment.'
options:
    scope:
        description:
            - Scope of the resource.
        required: true
        type: str
    registration_assignment_id:
        description:
            - Guid of the registration assignment.
        required: true
        type: str
    expand_registration_definition:
        description:
            - >-
                Tells whether to return registration definition details also along with
                registration assignment details.
        type: bool
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
            registration_definition:
                description:
                    - Registration definition inside registration assignment.
                type: dict
                suboptions:
                    properties:
                        description:
                            - >-
                                Properties of registration definition inside registration
                                assignment.
                        type: dict
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
            - Assert the state of the RegistrationAssignment.
            - >-
                Use C(present) to create or update an RegistrationAssignment and
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
    - name: Delete Registration Assignment
      azure_rm_registrationassignment: 
        registration_assignment_id: 26c128c2-fefa-4340-9bb1-6e081c90ada2
        scope: subscription/0afefe50-734e-4610-8a82-a144ahf49dea

    - name: Put Registration Assignment
      azure_rm_registrationassignment: 
        registration_assignment_id: 26c128c2-fefa-4340-9bb1-6e081c90ada2
        scope: subscription/0afefe50-734e-4610-8a82-a144ahf49dea

'''

RETURN = '''
properties:
    description:
        - Properties of a registration assignment.
    type: dict
    sample: null
    contains:
        registration_definition_id:
            description:
                - Fully qualified path of the registration definition.
            returned: always
            type: str
            sample: null
        registration_definition:
            description:
                - Registration definition inside registration assignment.
            type: dict
            sample: null
            contains:
                properties:
                    description:
                        - >-
                            Properties of registration definition inside registration
                            assignment.
                    type: dict
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
        - The fully qualified path of the registration assignment.
    type: str
    sample: null
type:
    description:
        - Type of the resource.
    type: str
    sample: null
name:
    description:
        - Name of the registration assignment.
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


class AzureRMRegistrationAssignment(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            scope=dict(
                type='str',
                required=True
            ),
            registration_assignment_id=dict(
                type='str',
                required=True
            ),
            expand_registration_definition=dict(
                type='bool'
            ),
            properties=dict(
                type='dict',
                disposition='/properties',
                options=dict(
                    registration_definition_id=dict(
                        type='str',
                        disposition='registration_definition_id',
                        required=True
                    ),
                    registration_definition=dict(
                        type='dict',
                        updatable=False,
                        disposition='registration_definition',
                        options=dict(
                            properties=dict(
                                type='dict',
                                disposition='properties'
                            ),
                            plan=dict(
                                type='dict',
                                disposition='plan',
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
                            )
                        )
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
        self.expand_registration_definition = None
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
            self.results['state'] = response

        return self.results

    def create_update_resource(self):
        try:
            response = self.mgmt_client.registration_assignments.create_or_update(scope=self.scope,
                                                                                  registration_assignment_id=self.registration_assignment_id,
                                                                                  properties=self.body.get('properties', None),
                                                                                  request_body=self.body)
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.log('Error attempting to create the RegistrationAssignment instance.')
            self.fail('Error creating the RegistrationAssignment instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.mgmt_client.registration_assignments.delete(scope=self.scope,
                                                                        registration_assignment_id=self.registration_assignment_id)
        except Exception as e:
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
