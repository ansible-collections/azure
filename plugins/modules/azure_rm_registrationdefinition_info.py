#!/usr/bin/python
#
# Copyright (c) 2020 Fred-Sun, (@Fred-Sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_registrationdefinition_info
version_added: '1.3.0'
short_description: Get RegistrationDefinition info
description:
    - Get info of RegistrationDefinition.
options:
    scope:
        description:
            - The subscription ID defines the subscription in which the registration definition will be retrieved.
            - If not specified, will use the subscription derived from AzureRMAuth.
        type: str
    registration_definition_id:
        description:
            - ID of the registration definition.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Fred-Sun (@Fred-Sun)
'''

EXAMPLES = '''
    - name: Get Registration Definition
      azure_rm_registrationdefinition_info:
        registration_definition_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Get All Registration Definitions from AzureRMAuth's subscription
      azure_rm_registrationdefinition_info:

    - name: Get All Registration Definitions in the subscription levle
      azure_rm_registrationdefinition_info:
          scope: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

'''

RETURN = '''
registration_definitions:
    description:
        - A list of dict results where the key is the name of the RegistrationDefinition and the values are the facts for that RegistrationDefinition.
    returned: always
    type: complex
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
                    sample: null
                authorizations:
                    description:
                        - Authorization tuple containing principal ID of the user/security group or service principal and id of the build-in role.
                    returned: always
                    type: complex
                    contains:
                        principal_id:
                            description:
                                - Principal ID of the security group/service principal/user that would be assigned permissions to the projected subscription.
                            returned: always
                            type: str
                            sample: null
                        role_definition_id:
                            description:
                                - The role definition identifier.
                                - The role will define all the permissions that the security group/service principal/user must have on the subscription.
                                - The role cannot be an owner role.
                            returned: always
                            type: str
                            sample: null
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
            sample: null
        name:
            description:
                - Name of the registration definition.
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


class AzureRMRegistrationDefinitionInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            scope=dict(
                type='str'
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

        self.mgmt_client = None
        super(AzureRMRegistrationDefinitionInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if not self.scope:
            self.scope = "/subscriptions/" + self.subscription_id
        else:
            self.scope = "/subscriptions/" + self.scope

        self.mgmt_client = self.get_mgmt_svc_client(ManagedServicesClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2019-09-01',
                                                    suppress_subscription_id=True)

        if self.registration_definition_id is not None:
            self.results['registration_definitions'] = self.format_item(self.get())
        else:
            self.results['registration_definitions'] = self.format_item(self.list())
        return self.results

    def get(self):
        response = None

        try:
            response = self.mgmt_client.registration_definitions.get(scope=self.scope,
                                                                     registration_definition_id=self.registration_definition_id)
        except Exception as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list(self):
        response = None

        try:
            response = self.mgmt_client.registration_definitions.list(scope=self.scope)
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
    AzureRMRegistrationDefinitionInfo()


if __name__ == '__main__':
    main()
