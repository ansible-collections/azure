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
module: azure_rm_registrationassignment_info
version_added: '2.0.0'
short_description: Get RegistrationAssignment info
description:
    - Get info of RegistrationAssignment.
options:
    scope:
        description:
             - Scope of the resource.
        required: true
        type: str
    registration_assignment_id:
        description:
            - Guid of the registration assignment.
        type: str
    expand_registration_definition:
        description:
            - Tells whether to return registration definition details also along with registration assignment details.
        required: true
        type: bool
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - GuopengLin (@t-glin)
    - Fred-Sun (@Fred-Sun)
    - Haiyuan Zhang (@haiyuazhang)

'''

EXAMPLES = '''
    - name: Get Registration Assignment
      azure_rm_registrationassignment_info: 
        registration_assignment_id: 26c128c2-fefa-4340-9bb1-6e081c90ada2
        scope: subscription/0afefe50-734e-4610-8a82-a144ahf49dea


    - name: Get Registration Assignments
      azure_rm_registrationassignment_info: 
        scope: subscription/0afefe50-734e-4610-8a82-a144ahf49dea


'''

RETURN = '''
registration_assignments:
    description:
        - A list of dict results where the key is the name of the RegistrationAssignment.
        - The values are the facts for that RegistrationAssignment.
    returned: always
    type: complex
    contains:
        properties:
            description:
                - Properties of a registration assignment.
            returned: always
            type: complex
            contains:
                id:
                    description:
                      - Fully qualified path of the registration definition.
                    returned: always
                    type: str
                    sample: /subscriptions/xxx-xxx/providers/Microsoft.ManagedServices/registrationDefinitions/xxx-xxx
                registration_definition:
                    description:
                        - Registration definition inside registration assignment.
                    returned: always
                    type: complex
                    contains:
                        properties:
                            description:
                                - Properties of registration definition inside registration assignment.
                            returned: always
                            type: dict
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
                - The fully qualified path of the registration assignment.
            returned: always
            type: str
            sample: /subscriptions/xxx-xxxf/providers/Microsoft.ManagedServices/registrationAssignments/xxx-xxx
        type:
            description:
                - Type of the resource.
            returned: always
            type: str
            sample: Microsoft.ManagedServices/registrationAssignment
        name:
            description:
                - Name of the registration assignment.
            returned: always
            type: str
            sample: 9b2895ec-fb1e-4a1e-a978-abd9933d6b20
        value:
            description:
                - List of registration assignments.
            returned: always
            type: complex
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
                        registration_definition:
                            description:
                                - Registration definition inside registration assignment.
                            returned: always
                            type: complex
                            contains:
                                properties:
                                    description:
                                        - Properties of registration definition inside registration assignment.
                                    returned: always
                                    type: dict
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
        next_link:
            description:
                - Link to next page of registration assignments.
            returned: always
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


class AzureRMRegistrationAssignmentInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            scope=dict(
                type='str',
                required=True
            ),
            registration_assignment_id=dict(
                type='str'
            ),
            expand_registration_definition=dict(
                type='bool',
                required=True
            )
        )

        self.scope = None
        self.registration_assignment_id = None
        self.expand_registration_definition = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        self.mgmt_client = None
        super(AzureRMRegistrationAssignmentInfo, self).__init__(self.module_arg_spec, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.mgmt_client = self.get_mgmt_svc_client(ManagedServicesClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2020-02-01-preview')

        if (self.scope is not None and self.registration_assignment_id is not None):
            self.results['registration_assignments'] = self.format_item(self.get())
        elif (self.scope is not None):
            self.results['registration_assignments'] = self.format_item(self.list())
        return self.results

    def get(self):
        response = None

        try:
            response = self.mgmt_client.registration_assignments.get(scope=self.scope,
                                                                     registration_assignment_id=self.registration_assignment_id,
                                                                     expand_registration_definition=self.expand_registration_definition)
        except Exception as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list(self):
        response = None

        try:
            response = self.mgmt_client.registration_assignments.list(scope=self.scope,
                                                                      expand_registration_definition=self.expand_registration_definition)
        except Exception as e:
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
    AzureRMRegistrationAssignmentInfo()


if __name__ == '__main__':
    main()
