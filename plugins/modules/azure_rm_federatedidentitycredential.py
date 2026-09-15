#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_federatedidentitycredential

version_added: "4.1.0"

short_description: Manage a federated identity credential on a user-assigned managed identity

description:
    - Create, update and delete a federated identity credential (Microsoft.ManagedIdentity/userAssignedIdentities/federatedIdentityCredentials).

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
        required: true
        type: str
    issuer:
        description:
            - The URL of the issuer to be trusted.
            - Required when I(state=present).
        type: str
    subject:
        description:
            - The identifier of the external identity.
            - Required when I(state=present).
        type: str
    audiences:
        description:
            - The list of audiences that can appear in the issued token.
            - Required when I(state=present).
        type: list
        elements: str
    state:
        description:
            - Assert the state of the federated identity credential. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Create a federated identity credential
  azure_rm_federatedidentitycredential:
    resource_group: myResourceGroup
    identity_name: myIdentity
    name: myCredential
    issuer: https://token.actions.githubusercontent.com
    subject: "repo:myOrg/myRepo:environment:production"
    audiences:
      - api://AzureADTokenExchange
    state: present

- name: Update a federated identity credential's subject
  azure_rm_federatedidentitycredential:
    resource_group: myResourceGroup
    identity_name: myIdentity
    name: myCredential
    issuer: https://token.actions.githubusercontent.com
    subject: "repo:myOrg/myRepo:environment:staging"
    audiences:
      - api://AzureADTokenExchange
    state: present

- name: Delete a federated identity credential
  azure_rm_federatedidentitycredential:
    resource_group: myResourceGroup
    identity_name: myIdentity
    name: myCredential
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the federated identity credential.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The federated identity credential resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/
                     Microsoft.ManagedIdentity/userAssignedIdentities/myIdentity/federatedIdentityCredentials/myCredential"
        name:
            description:
                - The federated identity credential name.
            returned: always
            type: str
            sample: myCredential
        issuer:
            description:
                - The URL of the issuer to be trusted.
            returned: always
            type: str
            sample: https://token.actions.githubusercontent.com
        subject:
            description:
                - The identifier of the external identity.
            returned: always
            type: str
            sample: "repo:myOrg/myRepo:environment:production"
        audiences:
            description:
                - The list of audiences that can appear in the issued token.
            returned: always
            type: list
            sample: ["api://AzureADTokenExchange"]
        system_data:
            description:
                - Metadata pertaining to creation and last modification of the resource.
                - Not always populated immediately after creation.
            returned: success
            type: dict
            sample: {
                "created_at": "2026-08-31T03:12:08.743499Z",
                "created_by": "72f98888-8666-4144-9199-2d7cd0444444",
                "created_by_type": "User",
                "last_modified_at": "2026-08-31T03:12:08.743499Z",
                "last_modified_by": "72f98888-8666-4144-9199-2d7cd0444444",
                "last_modified_by_type": "User"
            }
        type:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: "Microsoft.ManagedIdentity/userAssignedIdentities/federatedIdentityCredentials"
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.serialization import as_attribute_dict
    from azure.mgmt.msi.models import FederatedIdentityCredential
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMFederatedIdentityCredential(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            identity_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            issuer=dict(type='str'),
            subject=dict(type='str'),
            audiences=dict(type='list', elements='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.module_required_if = [
            ('state', 'present', ['issuer', 'subject', 'audiences']),
        ]

        self.resource_group = None
        self.identity_name = None
        self.name = None
        self.issuer = None
        self.subject = None
        self.audiences = None
        self.state = None

        self.results = dict(
            changed=False,
            state=dict(),
        )

        super(AzureRMFederatedIdentityCredential, self).__init__(self.module_arg_spec,
                                                                 required_if=self.module_required_if,
                                                                 supports_check_mode=True,
                                                                 supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec.keys():
            setattr(self, key, kwargs[key])

        changed = False
        old_response = self.get_credential()
        response = old_response

        if self.state == 'present':
            if not old_response:
                changed = True
            else:
                if self.issuer != old_response.get('issuer') or \
                        self.subject != old_response.get('subject') or \
                        self.audiences != old_response.get('audiences'):
                    changed = True
                    old_response['issuer'] = self.issuer
                    old_response['subject'] = self.subject
                    old_response['audiences'] = self.audiences

            if changed and not self.check_mode:
                response = self.create_or_update_credential()

        elif self.state == 'absent':
            if old_response:
                changed = True
                if not self.check_mode:
                    self.delete_credential()
                    response = None

        self.results['changed'] = changed
        self.results['state'] = response if response else dict()

        return self.results

    def get_credential(self):
        try:
            response = self.msi_client.federated_identity_credentials.get(
                resource_group_name=self.resource_group,
                resource_name=self.identity_name,
                federated_identity_credential_resource_name=self.name,
            )
            return as_attribute_dict(response, exclude_readonly=False)
        except ResourceNotFoundError:
            return None

    def create_or_update_credential(self):
        parameters = FederatedIdentityCredential(issuer=self.issuer, subject=self.subject, audiences=self.audiences)
        try:
            response = self.msi_client.federated_identity_credentials.create_or_update(
                resource_group_name=self.resource_group,
                resource_name=self.identity_name,
                federated_identity_credential_resource_name=self.name,
                parameters=parameters,
            )
        except Exception as exc:
            self.fail("Error creating or updating federated identity credential {0} - {1}".format(self.name, str(exc)))
        return as_attribute_dict(response, exclude_readonly=False)

    def delete_credential(self):
        try:
            self.msi_client.federated_identity_credentials.delete(
                resource_group_name=self.resource_group,
                resource_name=self.identity_name,
                federated_identity_credential_resource_name=self.name,
            )
        except Exception as exc:
            self.fail("Error deleting federated identity credential {0} - {1}".format(self.name, str(exc)))
        return True


def main():
    AzureRMFederatedIdentityCredential()


if __name__ == '__main__':
    main()
