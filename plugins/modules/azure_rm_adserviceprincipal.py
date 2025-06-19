#!/usr/bin/python
#
# Copyright (c) 2020 Haiyuan Zhang, <haiyzhan@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_adserviceprincipal

version_added: "0.2.0"

short_description: Manage Azure Active Directory service principal

description:
        - Manage Azure Active Directory service principal.

options:
    account_enabled:
        description:
            - Whether the service principal is enabled.
        type: bool
        default: True
    app_id:
        description:
            - The application ID.
        type: str
        required: True
    app_role_assignment_required:
        description:
            - Whether the Role of the Service Principal is set.
        type: bool
    notes:
        description:
            - Use this field to add information that is relevant for the management of the application
        type: str
    service_principal_type:
        description:
            - The type of the service principal.
        choices:
            - application
            - managedIdentity
        type: str
        default: application
    state:
        description:
            - Assert the state of Active Dirctory service principal.
            - Use C(present) to create or update a Password and use C(absent) to delete.
        default: present
        choices:
            - absent
            - present
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    haiyuan_zhang (@haiyuazhang)
    Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: create ad sp
  azure_rm_adserviceprincipal:
    app_id: "{{ app_id }}"
    state: present
'''

RETURN = '''
app_display_name:
    description:
        - Object's display name or its prefix.
    type: str
    returned: always
    sample: fredAKSCluster
app_id:
    description:
        - The application ID.
    returned: always
    type: str
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
app_role_assignment_required:
    description:
        - Whether the Role of the Service Principal is set.
    returned: always
    type: bool
    sample: false
object_id:
    description:
        - Object ID of the associated service principal.
    returned: always
    type: str
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from msgraph.generated.models.service_principal import ServicePrincipal
except Exception:
    pass

try:
    import asyncio
    from msgraph.generated.service_principals.service_principals_request_builder import ServicePrincipalsRequestBuilder
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMADServicePrincipal(AzureRMModuleBaseExt):
    def __init__(self):

        self.module_arg_spec = dict(
            account_enabled=dict(type='bool', default=True),
            app_id=dict(type='str', required=True),
            notes=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            app_role_assignment_required=dict(type='bool'),
            service_principal_type=dict(type='str', default='application', choices=['application', 'managedIdentity'])
        )

        self.account_enabled = None
        self.state = None
        self.app_id = None
        self.app_role_assignment_required = None
        self.notes = None
        self.object_id = None
        self.service_principal_type = None
        self.results = dict(changed=False)

        super(AzureRMADServicePrincipal, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=False,
                                                        supports_tags=False,
                                                        is_ad_resource=True)

        mutually_exclusive = {}

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        self._client = self.get_msgraph_client()

        response = self.get_resource()

        if response:
            if self.state == 'present':
                if self.check_update(response):
                    self.update_resource(response)
            elif self.state == 'absent':
                self.delete_resource(response)
        else:
            if self.state == 'present':
                self.create_resource()
            elif self.state == 'absent':
                self.log("try to delete non exist resource")

        return self.results

    def create_resource(self):
        try:
            response = asyncio.get_event_loop().run_until_complete(self.create_service_principal())
            self.results['changed'] = True
            self.results.update(self.to_dict(response))
            return response
        except Exception as ge:
            self.fail("Error creating service principle, app id {0} - {1}".format(self.app_id, str(ge)))

    def update_resource(self, old_response):
        try:
            request_body = ServicePrincipal(
                app_role_assignment_required=None,
            )
            if self.app_role_assignment_required is not None:
                request_body = ServicePrincipal(
                    app_role_assignment_required=self.app_role_assignment_required
                )

            asyncio.get_event_loop().run_until_complete(self.update_service_principal(old_response, request_body))
            self.results['changed'] = True
            self.results.update(self.get_resource())

        except Exception as ge:
            self.fail("Error updating the service principal app_id {0} - {1}".format(self.app_id, str(ge)))

    def delete_resource(self, response):
        try:
            asyncio.get_event_loop().run_until_complete(self.delete_service_principal(response))
            self.results['changed'] = True
            return True
        except Exception as ge:
            self.fail("Error deleting service principal app_id {0} - {1}".format(self.app_id, str(ge)))

    def get_resource(self):
        try:
            sps = asyncio.get_event_loop().run_until_complete(self.get_service_principals())
            result = list(sps.value)
            if not result:
                return False
            result = result[0]
            return self.to_dict(result)
        except Exception as ge:
            self.log("Did not find the graph instance instance {0} - {1}".format(self.app_id, str(ge)))
            return False

    def check_update(self, response):
        app_assignment_changed = self.app_role_assignment_required is not None and \
            self.app_role_assignment_required != response.get('app_role_assignment_required', None)

        return app_assignment_changed

    def to_dict(self, object):
        return dict(
            account_enabled=object.account_enabled,
            app_id=object.app_id,
            notes=object.notes,
            object_id=object.id,
            app_display_name=object.display_name,
            app_role_assignment_required=object.app_role_assignment_required,
            service_principal_type=object.service_principal_type
        )

    async def create_service_principal(self):
        request_body = ServicePrincipal(
            app_id=self.app_id,
            account_enabled=self.account_enabled,
            notes=self.notes,
            service_principal_type=self.service_principal_type
        )
        return await self._client.service_principals.post(body=request_body)

    async def update_service_principal(self, old_response, request_body):
        return await self._client.service_principals.by_service_principal_id(old_response['object_id']).patch(
            body=request_body)

    async def delete_service_principal(self, response):
        return await self._client.service_principals.by_service_principal_id(response.get('object_id')).delete()

    async def get_service_principals(self):
        request_configuration = ServicePrincipalsRequestBuilder.ServicePrincipalsRequestBuilderGetRequestConfiguration(
            query_parameters=ServicePrincipalsRequestBuilder.ServicePrincipalsRequestBuilderGetQueryParameters(
                filter="servicePrincipalNames/any(c:c eq '{0}')".format(self.app_id),
            )
        )
        return await self._client.service_principals.get(request_configuration=request_configuration)


def main():
    AzureRMADServicePrincipal()


if __name__ == '__main__':
    main()
