#!/usr/bin/python
#
# Copyright (c) 2020 Haiyuan Zhang, <haiyzhan@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: azure_rm_adserviceprincipal

version_added: "0.2.0"

short_description: Manage Azure Active Directory service principal

description:
        - Manage Azure Active Directory service principal.

options:
    app_id:
        description:
            - The application ID.
        type: str
        required: True
    tenant:
        description:
            - The tenant ID.
        type: str
        required: True
    app_role_assignment_required:
        description:
            - Whether the Role of the Service Principal is set.
        type: bool
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
    - azure.azcollection.azure_tags

author:
    haiyuan_zhang (@haiyuazhang)
    Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
  - name: create ad sp
    azure_ad_serviceprincipal:
      app_id: "{{ app_id }}"
      state: present
      tenant: "{{ tenant_id }}"
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
    from azure.graphrbac.models import ServicePrincipalCreateParameters
    from azure.graphrbac.models import ServicePrincipalUpdateParameters
except Exception:
    pass

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.graphrbac.models import GraphErrorException
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMADServicePrincipal(AzureRMModuleBaseExt):
    def __init__(self):

        self.module_arg_spec = dict(
            app_id=dict(type='str', required=True),
            tenant=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            app_role_assignment_required=dict(type='bool')
        )

        self.state = None
        self.tenant = None
        self.app_id = None
        self.app_role_assignment_required = None
        self.object_id = None
        self.results = dict(changed=False)

        super(AzureRMADServicePrincipal, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=False,
                                                        supports_tags=False,
                                                        is_ad_resource=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

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
            client = self.get_graphrbac_client(self.tenant)
            response = client.service_principals.create(ServicePrincipalCreateParameters(app_id=self.app_id, account_enabled=True))
            self.results['changed'] = True
            self.results.update(self.to_dict(response))
            return response
        except GraphErrorException as ge:
            self.fail("Error creating service principle, app id {0} - {1}".format(self.app_id, str(ge)))

    def update_resource(self, old_response):
        try:
            client = self.get_graphrbac_client(self.tenant)
            to_update = {}
            if self.app_role_assignment_required is not None:
                to_update['app_role_assignment_required'] = self.app_role_assignment_required

            client.service_principals.update(old_response['object_id'], to_update)
            self.results['changed'] = True
            self.results.update(self.get_resource())

        except GraphErrorException as ge:
            self.fail("Error updating the service principal app_id {0} - {1}".format(self.app_id, str(ge)))

    def delete_resource(self, response):
        try:
            client = self.get_graphrbac_client(self.tenant)
            client.service_principals.delete(response.get('object_id'))
            self.results['changed'] = True
            return True
        except GraphErrorException as ge:
            self.fail("Error deleting service principal app_id {0} - {1}".format(self.app_id, str(ge)))

    def get_resource(self):
        try:
            client = self.get_graphrbac_client(self.tenant)
            result = list(client.service_principals.list(filter="servicePrincipalNames/any(c:c eq '{0}')".format(self.app_id)))
            if not result:
                return False
            result = result[0]
            return self.to_dict(result)
        except GraphErrorException as ge:
            self.log("Did not find the graph instance instance {0} - {1}".format(self.app_id, str(ge)))
            return False

    def check_update(self, response):
        app_assignment_changed = self.app_role_assignment_required is not None and \
            self.app_role_assignment_required != response.get('app_role_assignment_required', None)

        return app_assignment_changed

    def to_dict(self, object):
        return dict(
            app_id=object.app_id,
            object_id=object.object_id,
            app_display_name=object.display_name,
            app_role_assignment_required=object.app_role_assignment_required
        )


def main():
    AzureRMADServicePrincipal()


if __name__ == '__main__':
    main()
