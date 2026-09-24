#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_federatedidentitycredential_info

version_added: "4.1.0"

short_description: Get federated identity credential facts

description:
    - Get facts for a specified federated identity credential or all federated identity credentials on a user-assigned identity.

options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    identity_name:
        description:
            - The name of the parent user-assigned identity.
        required: true
        type: str
    name:
        description:
            - The name of the federated identity credential.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Get facts for one federated identity credential
  azure_rm_federatedidentitycredential_info:
    resource_group: myResourceGroup
    identity_name: myIdentity
    name: myCredential

- name: Get facts for all federated identity credentials on an identity
  azure_rm_federatedidentitycredential_info:
    resource_group: myResourceGroup
    identity_name: myIdentity
'''

RETURN = '''
federatedidentitycredentials:
    description:
        - Gets a list of federated identity credentials.
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/
                   Microsoft.ManagedIdentity/userAssignedIdentities/myIdentity/federatedIdentityCredentials/myCredential",
            "name": "myCredential",
            "issuer": "https://token.actions.githubusercontent.com",
            "subject": "repo:myOrg/myRepo:environment:production",
            "audiences": ["api://AzureADTokenExchange"],
            "system_data": {
                "created_at": "2026-08-31T03:12:08.743499Z",
                "created_by": "72f98888-8666-4144-9199-2d7cd0444444",
                "created_by_type": "User",
                "last_modified_at": "2026-08-31T03:12:08.743499Z",
                "last_modified_by": "72f98888-8666-4144-9199-2d7cd0444444",
                "last_modified_by_type": "User"
            },
            "type": "Microsoft.ManagedIdentity/userAssignedIdentities/federatedIdentityCredentials"
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMFederatedIdentityCredentialInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            identity_name=dict(type='str', required=True),
            name=dict(type='str'),
        )

        self.resource_group = None
        self.identity_name = None
        self.name = None

        self.results = dict(changed=False)

        super(AzureRMFederatedIdentityCredentialInfo, self).__init__(self.module_arg_spec,
                                                                     supports_check_mode=True,
                                                                     supports_tags=False,
                                                                     facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            results = self.get_item()
        else:
            results = self.list_items()

        self.results['federatedidentitycredentials'] = results

        return self.results

    def get_item(self):
        try:
            item = self.msi_client.federated_identity_credentials.get(
                resource_group_name=self.resource_group,
                resource_name=self.identity_name,
                federated_identity_credential_resource_name=self.name,
            )
            return [as_attribute_dict(item, exclude_readonly=False)]
        except ResourceNotFoundError:
            return []

    def list_items(self):
        try:
            response = self.msi_client.federated_identity_credentials.list(
                resource_group_name=self.resource_group,
                resource_name=self.identity_name,
            )
            return [as_attribute_dict(item, exclude_readonly=False) for item in response]
        except ResourceNotFoundError as exc:
            self.fail("Failed to list federated identity credentials for identity {0} - {1}".format(self.identity_name, str(exc)))


def main():
    AzureRMFederatedIdentityCredentialInfo()


if __name__ == '__main__':
    main()
