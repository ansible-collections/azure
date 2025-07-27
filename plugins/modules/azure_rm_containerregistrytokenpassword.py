#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_containerregistrytokenpassword
version_added: "3.7.0"
short_description: Generate or  renegenerate the Azure Container Registry Token Password
description:
    - Generate or  renegenerate the Azure Container Registry Token Password.
    - Note that the generated password cannot be retrieved. Please store your credentials safely after generation.

options:
    resource_group:
        description:
            - The name of the resource group to which the container registry belongs.
        type: str
        required: true
    registry_name:
        description:
            - The name of the container registry.
        type: str
        required: true
    token_id:
        description:
            - The ID of the container registry token.
        type: str
        required: true
    expiry:
        description:
            - The expiry datetime of the password.
            - Sample as 2025/07/25.
            - If not configured, it will never expire.
        type: str
    name:
        description:
            - The name of the password.
            - If not configured, both passwords will be regenerated.
        type: str
        choices:
            - password1
            - password2

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Generate a new password for container registry token
  azure_rm_containerregistrytokenpassword:
    resource_group: myResourceGroup
    registry_name: myRegistry
    name: mytoken
    expiry: 2025/08/01
    token_id: token_id
'''

RETURN = '''
passwords:
    description:
        - A list of dictionaries containing facts for token passwords facts.
    returned: always
    type: list
    sample: [
       {
            "creation_time": "2025-07-24T08:28:50.569062Z",
            "expiry": "2025-08-01T00:00:00.000Z",
            "name": "password1"
        },
        {
            "creation_time": "2025-07-24T08:29:19.12587Z",
            "expiry": "2025-08-01T00:00:00.000Z",
            "name": "password2",
            "value": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        }
    ]
'''

try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
    from azure.core.polling import LROPoller
    from datetime import datetime
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMContainerRegistryTokenPassword(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True,
            ),
            registry_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                choices=['password1', 'password2']
            ),
            token_id=dict(
                type='str',
                required=True
            ),
            expiry=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
            passwords=None,
        )
        self.resource_group = None
        self.registry_name = None
        self.name = None
        self.expiry = None
        self.token_id = None

        super(AzureRMContainerRegistryTokenPassword, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=False)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec):
            setattr(self, key, kwargs[key])

        # Create dict form input, without None value
        password_template = dict(name=self.name,
                                 token_id=self.token_id,
                                 expiry=datetime.strptime(self.expiry, "%Y/%m/%d") if self.expiry else None)
        try:
            response = self.containerregistrytoken_client.registries.begin_generate_credentials(resource_group_name=self.resource_group,
                                                                                                registry_name=self.registry_name,
                                                                                                generate_credentials_parameters=password_template)

        except Exception as ec:
            self.fail("Generate token password occur exception, Exception as {0}".format(str(ec)))

        if isinstance(response, LROPoller):
            response = self.get_poller_result(response)

        self.results = response.as_dict()
        self.results['changed'] = True
        return self.results


def main():
    AzureRMContainerRegistryTokenPassword()


if __name__ == '__main__':
    main()
