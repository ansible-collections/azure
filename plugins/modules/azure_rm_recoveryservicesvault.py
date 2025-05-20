#!/usr/bin/python
#
# Copyright (c) 2020 Suyeb Ansari (@suyeb786)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = \
    '''
---
module: azure_rm_recoveryservicesvault
version_added: '1.1.0'
short_description: Create and Delete Azure Recovery Services vault
description:
    - Create or Delete Azure Recovery Services vault.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - The name of the Azure Recovery Service Vault.
        required: true
        type: str
    location:
        description:
            - Azure Resource location.
        required: true
        type: str
    state:
        description:
            - Assert the state of the protection item.
            - Use C(present) for Creating Azure Recovery Service Vault.
            - Use C(absent) for Deleting Azure Recovery Service Vault.
        default: present
        type: str
        choices:
            - present
            - absent
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
    - azure.azcollection.azure_identity_multiple
author:
    - Suyeb Ansari (@suyeb786)
'''

EXAMPLES = '''
- name: Create/Update Azure Recovery Service vault
  azure_rm_recoveryservicesvault:
    resource_group: 'myResourceGroup'
    name: 'testVault'
    location: 'westeurope'
    state: 'present'
- name: Delete Recovery Service Vault
  azure_rm_recoveryservicesvault:
    resource_group: 'myResourceGroup'
    name: 'testVault'
    location: 'westeurope'
    state: 'absent'
'''

RETURN = '''
response:
    description:
        - The response about the current state of the recovery services vault.
    returned: always
    type: complex
    contains:
        etag:
            description:
                - A unique read-only string that changes whenever the resource create.
            returned: always
            type: str
            sample: "datetime'2020-09-16T02%3A44%3A27.834293Z'"
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample:  "/subscriptions/xxxxxxx/resourceGroups/resourcegroup_name/ \
            providers/Microsoft.RecoveryServices/vaults/rev_name"
        location:
            description:
                - The location of the resource.
            returned: always
            type: str
            sample: "eastus"
        name:
            description:
                - Name of the recovery services vault name.
            returned: always
            type: str
            sample: revault_name
        properties:
            description:
                - The recovery service vault properties.
            returned: always
            type: dict
            sample: {
                    "privateEndpointStateForBackup": "None",
                    "privateEndpointStateForSiteRecovery": "None",
                    "provisioningState": "Succeeded"
                    }
        sku:
            description:
                - The sku type of the recovery service vault.
            returned: always
            type: str
            sample: Standard
        type:
            description:
                - The type of the recovery service vault.
            returned: always
            type: str
            sample: "Microsoft.RecoveryServices/vaults"
        tags:
            description:
                - The resource tags.
            returned: when-used
            type: dict
            sample: {'key1': 'value'}
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
import json
import time

try:
    from azure.mgmt.recoveryservices.models import (IdentityData, UserIdentity)
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRecoveryServicesVault(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
                required=True
            ),
            identity=dict(
                type='dict',
                options=self.managed_identity_multiple_spec
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.state = None
        self.identity = None
        self.tags = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.url = None
        self.status_code = [200, 201, 202, 204]

        self.body = {}
        self.query_parameters = {}
        self.query_parameters['api-version'] = None
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        self._managed_identity = None

        super(AzureRMRecoveryServicesVault, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                           supports_check_mode=True,
                                                           supports_tags=True
                                                           )

    @property
    def managed_identity(self):
        if not self._managed_identity:
            self._managed_identity = {"identity": IdentityData,
                                      "user_assigned": UserIdentity
                                      }
        return self._managed_identity

    def get_api_version(self):
        return '2020-02-02'

    def get_url(self):
        if self.state == 'present' or self.state == 'absent':
            return '/subscriptions/' \
                   + self.subscription_id \
                   + '/resourceGroups/' \
                   + self.resource_group \
                   + '/providers/Microsoft.RecoveryServices' \
                   + '/vaults' + '/' \
                   + self.name

    def get_body(self):
        if self.state == 'present':
            return {
                "properties": {},
                "sku": {
                    "name": "Standard"
                },
                "identity": self.identity,
                "location": self.location,
                'tags': self.tags
            }
        else:
            return {}

    def format_for_body(self, identity):
        if identity:
            identity = identity.as_dict()
            if identity.get("user_assigned_identities", None):
                identity["userAssignedIdentities"] = identity.pop("user_assigned_identities")
        return identity

    def format_for_helper(self, identity):
        if identity and identity.get("userAssignedIdentities"):
            identity["user_assigned_identities"] = identity.pop("userAssignedIdentities")
        return identity

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_parameters(self.module_arg_spec, self.body, 0)

        self.query_parameters['api-version'] = self.get_api_version()
        self.url = self.get_url()
        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_resource()

        update_identity = False
        if self.identity:
            old_identity = old_response and old_response.get('identity', None)
            old_identity = self.format_for_helper(old_identity)
            update_identity, identity = self.update_managed_identity(curr_identity=old_identity,
                                                                     new_identity=self.identity)
            self.identity = self.format_for_body(identity)
        else:
            if old_response is not False:
                self.identity = old_response.get('identity')

        update_tags = False
        if old_response is not False:
            update_tags, self.tags = self.update_tags(old_response.get('tags'))
        self.body = self.get_body()

        changed = False
        if self.state == 'present':
            if old_response is False:
                changed = True
                self.create_recovery_service_vault()
            elif update_identity is True or update_tags is True:
                changed = True
                self.create_recovery_service_vault()
            else:
                changed = False
            response = self.get_resource()
        if self.state == 'absent':
            changed = True
            response = self.delete_recovery_service_vault()

        self.results['response'] = response
        self.results['changed'] = changed

        return self.results

    def create_recovery_service_vault(self):
        # self.log('Creating Recovery Service Vault Name {0}'.format(self.))
        try:
            response = self.mgmt_client.query(
                self.url,
                'PUT',
                self.query_parameters,
                self.header_parameters,
                self.body,
                self.status_code,
                600,
                30,
            )
        except Exception as e:
            self.log('Error in creating Azure Recovery Service Vault.')
            self.fail('Error in creating Azure Recovery Service Vault {0}'.format(str(e)))

        if hasattr(response, 'body'):
            response = json.loads(response.body())
        elif hasattr(response, 'context'):
            response = response.context['deserialized_data']
        else:
            self.fail("Create or Updating fail, no match message return, return info as {0}".format(response))

        return response

    def delete_recovery_service_vault(self):
        # self.log('Deleting Recovery Service Vault {0}'.format(self.))
        try:
            response = self.mgmt_client.query(
                self.url,
                'DELETE',
                self.query_parameters,
                self.header_parameters,
                None,
                self.status_code,
                600,
                30,
            )
        except Exception as e:
            self.log('Error attempting to delete Azure Recovery Service Vault.')
            self.fail('Error while deleting Azure Recovery Service Vault: {0}'.format(str(e)))

    def get_resource(self):
        # self.log('Get Recovery Service Vault Name {0}'.format(self.))
        found = False
        retries = 0
        retry_limit = 60
        sleep_time = 2
        try:
            # Some operations of Recovery Service Vault can take a while to
            #  Provision.  Check that the resource has provisioned and warn
            #  if we timeout waiting for it.
            provisioning = True
            while provisioning is True and retries < retry_limit:
                response = self.mgmt_client.query(
                    self.url,
                    'GET',
                    self.query_parameters,
                    self.header_parameters,
                    None,
                    self.status_code,
                    600,
                    30,
                )
                response = json.loads(response.body())
                provisioning_status = response['properties']['provisioningState']
                provisioning = provisioning_status != 'Succeeded' and True or False
                retries += 1
                time.sleep(sleep_time)
            found = True
            if retries >= retry_limit:
                self.module.warn(
                    'Retry limit {0} exceeded while waiting for resource to provision'.format(retry_limit)
                )
        except Exception as e:
            self.log('Recovery Service Vault Does not exist.')
        if found is True:
            return response
        else:
            return False


def main():
    AzureRMRecoveryServicesVault()


if __name__ == '__main__':
    main()
