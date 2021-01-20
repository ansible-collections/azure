#!/usr/bin/python
#
# Copyright (c) 2020 Cole Neubauer, (@coleneubauer)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
module: azure_rm_aduser_info

version_added: "1.3.2"

short_description: Get Azure Active Directory user info

description:
    - Get Azure Active Directory user info.

options:
    tenant:
        description:
            - The tenant ID.
        type: str
        required: True
    object_id:
        description:
            - It's service principal's object ID.
        type: str
    app_id:
        description:
            - The application ID.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Cole Neubauer(@coleneubauer)

'''

EXAMPLES = '''
  - name: get ad user info
    azure_rm_adserviceprincipal_info:
      app_id: "{{ app_id }}"
      tenant: "{{ tenant_id }}"

'''

RETURN = '''
app_role_assignment_required:
    description:
        - Whether the Role of the Service Principal is set.
    type: bool
    returned: always
    sample: false
object_id:
    description:
        - It's service principal's object ID.
    returned: always
    type: str
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx


'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.graphrbac.models import GraphErrorException
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMADUserInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            user_principle_name=dict(type='str'),
            object_id=dict(type='str'),
            filter_parameter_name=dict(type='str'),
            filter_parameter_value=dict(type='str'),
            tenant=dict(type='str', required=True),
        )

        self.tenant = None
        self.user_principle_name = None
        self.object_id = None
        self.filter_parameter_name = None
        self.filter_parameter_value = None
        self.results = dict(changed=False)

        # TODO: limit object id, user_principle_name, and filter params
        # TODO: add tests
        # TODO: documentation
        # TODO: cleanup
        # TODO: consider adding a "filter" parameter for more complex limits.
        # Would probably be easier for most to do the query directly

        super(AzureRMADUserInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                            supports_check_mode=False,
                                                            supports_tags=False,
                                                            is_ad_resource=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        ad_users = []

        try:
            client = self.get_graphrbac_client(self.tenant)

            if self.user_principle_name is not None:
                ad_users = [client.users.get(self.user_principle_name)]
            elif self.object_id is not None:
                ad_users = [client.users.get(self.object_id)]
            else: # run a filter based on user input to return based on any given var
                try:
                    ad_users = list(client.users.list(filter="{0} eq '{1}'".format(self.filter_parameter_name, self.filter_parameter_value)))
                except GraphErrorException as e:
                    # the type doesn't get more specific. Could check the error message but no guarantees that message doesn't change in the future
                    # more stable to try again assuming the first error came from the parameter being a list and try again
                    try:
                        ad_users = list(client.users.list(filter="{0}/any(c:c eq '{1}')".format(self.filter_parameter_name, self.filter_parameter_value)))
                    except GraphErrorException as sub_e:
                        raise #TODO add previous failure message as well before raising

            self.results['ad_users'] = [self.to_dict(user) for user in ad_users]
        except GraphErrorException as e:
            self.fail("failed to get ad user info {0}".format(str(e)))

        return self.results

    def to_dict(self, object):
        return dict(
            object_id=object.object_id,
            display_name=object.display_name,
            user_principal_name=object.user_principal_name,
            mail_nickname=object.mail_nickname,
            mail=object.mail,
            account_enabled=object.account_enabled,
            user_type=object.user_type
        )

def main():
    AzureRMADUserInfo()


if __name__ == '__main__':
    main()
