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
module: azure_rm_adgroup_info
version_added: "1.3.2"
short_description: Get Azure Active Directory group info
description:
    - Get Azure Active Directory group info.
options:
    tenant:
        description:
            - The tenant ID.
        type: str
        required: True
    object_id:
        description:
            - The object id for the user.
            - returns the user who has this object ID.
        type: str
    user_principal_name:
        description:
            - The principal name of the user.
            - returns the user who has this principal name.
        type: str
    attribute_name:
        description:
            - The name of an attribute that you want to match to attribute_value.
            - If attribute_name is not a collection type it will return users where attribute_name is equal to attribute_value.
            - If attribute_name is a collection type it will return users where attribute_value is in attribute_name.
        type: str
    attribute_value:
        description:
            - The value to match attribute_name to.
            - If attribute_name is not a collection type it will return users where attribute_name is equal to attribute_value.
            - If attribute_name is a collection type it will return users where attribute_value is in attribute_name.
        type: str
    odata_filter:
        description:
            - returns users based on the the OData filter passed into this parameter.
        type: str
    all:
        description:
            - If True, will return all users in tenant.
            - If False will return no users.
            - It is recommended that you instead identify a subset of users and use filter
        type: bool
    log_path:
        description:
            - parent argument.
        type: str
    log_mode:
        description:
            - parent argument.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Cole Neubauer(@coleneubauer)
'''

EXAMPLES = '''
    - name: Using user_principal_name
      azure.azcollection.azure_rm_aduser_info:
        user_principal_name: user@contoso.com
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    - name: Using object_id
      azure.azcollection.azure_rm_aduser_info:
        object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    - name: Using attribute mailNickname - not a collection
      azure.azcollection.azure_rm_aduser_info:
        attribute_name: mailNickname
        attribute_value: users_mailNickname
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    - name: Using attribute proxyAddresses - a collection
      azure.azcollection.azure_rm_aduser_info:
        attribute_name: proxyAddresses
        attribute_value: SMTP:user@contoso.com
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    - name: Using Filter mailNickname
      azure.azcollection.azure_rm_aduser_info:
        odata_filter: mailNickname eq 'user@contoso.com'
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    - name: Using Filter proxyAddresses
      azure.azcollection.azure_rm_aduser_info:
        odata_filter: proxyAddresses/any(c:c eq 'SMTP:user@contoso.com')
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
'''

RETURN = '''
object_id:
    description:
        - The object_id for the user.
    type: str
    returned: always
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
display_name:
    description:
        - The display name of the user.
    returned: always
    type: str
    sample: John Smith
user_principal_name:
    description:
        - The principal name of the user.
    returned: always
    type: str
    sample: jsmith@contoso.com
mail_nickname:
    description:
        - The mail alias for the user.
    returned: always
    type: str
    sample: jsmith
mail:
    description:
        - The primary email address of the user.
    returned: always
    type: str
    sample: John.Smith@contoso.com
account_enabled:
    description:
        - Whether the account is enabled.
    returned: always
    type: bool
    sample: False
user_type:
    description:
        - A string value that can be used to classify user types in your directory.
    returned: always
    type: str
    sample: Member
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.graphrbac.models import GraphErrorException
    from azure.graphrbac.models import CheckGroupMembershipParameters
except ImportError:
    # This is handled in azure_rm_common
    pass

# TODO:
    # Handle checking if a member is in the group
class AzureRMADGroupInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            user_principal_name=dict(type='str'),
            object_id=dict(type='str'),
            attribute_name=dict(type='str'),
            attribute_value=dict(type='str'),
            odata_filter=dict(type='str'),
            check_membership=dict(type='str'),
            return_owners=dict(type='bool',default=False),
            return_group_members=dict(type='bool',default=False),
            return_member_groups=dict(type='bool',default=False),
            all=dict(type='bool'),
            tenant=dict(type='str', required=True),
            log_path=dict(type='str'),
            log_mode=dict(type='str'),
        )

        self.tenant = None
        self.user_principal_name = None
        self.object_id = None
        self.attribute_name = None
        self.attribute_value = None
        self.odata_filter = None
        self.check_membership = False
        self.return_owners = False
        self.return_group_members = False
        self.return_member_groups = False
        self.all = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(changed=False)

        mutually_exclusive = [['odata_filter', 'attribute_name', 'object_id', 'user_principal_name', 'all']]
        required_together = [['attribute_name', 'attribute_value']]
        required_one_of = [['odata_filter', 'attribute_name', 'object_id', 'user_principal_name', 'all']]

        super(AzureRMADGroupInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=False,
                                                supports_tags=False,
                                                mutually_exclusive=mutually_exclusive,
                                                required_together=required_together,
                                                required_one_of=required_one_of,
                                                is_ad_resource=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        ad_groups = []

        try:
            client = self.get_graphrbac_client(self.tenant)

            if self.object_id is not None:
                ad_groups = [client.groups.get(self.object_id)]
            elif self.attribute_name is not None and self.attribute_value is not None:
                ad_groups = list(client.groups.list(filter="{0} eq '{1}'".format(self.attribute_name, self.attribute_value)))
            elif self.odata_filter is not None:  # run a filter based on user input
                ad_groups = list(client.groups.list(filter=self.odata_filter))
            elif self.all:
                ad_groups = list(client.groups.list())

            self.results['ad_groups'] = [self.set_results(group, client) for group in ad_groups]

        except GraphErrorException as e:
            self.fail("failed to get ad group info {0}".format(str(e)))

        return self.results


    def group_to_dict(self, object):
        return dict(
            object_id=object.object_id,
            display_name=object.display_name,
            mail_nickname=object.mail_nickname,
            mail_enabled=object.mail_enabled,
            security_enabled=object.security_enabled,
            mail=object.mail
        )

    def user_to_dict(self, object):
        return dict(
            object_id=object.object_id,
            display_name=object.display_name,
            user_principal_name=object.user_principal_name,
            mail_nickname=object.mail_nickname,
            mail=object.mail,
            account_enabled=object.account_enabled,
            user_type=object.user_type
        )

    def set_results(self, object, client):
        results = self.group_to_dict(object)

        if results["object_id"] and self.return_owners:
            results["group_owners"] = list(client.groups.list_owners(results["object_id"]))

        if results["object_id"] and self.return_group_members:
            results["group_members"] = [self.user_to_dict(user) for user in list(client.groups.get_group_members(results["object_id"]))]

        if results["object_id"] and self.return_member_groups:
            results["member_groups"] = [self.group_to_dict(group) for group in list(client.groups.get_member_groups(results["object_id"], False))]

        if results["object_id"] and self.check_membership:
            results["is_member_of"] = client.groups.is_member_of(CheckGroupMembershipParameters(group_id=results["object_id"], member_id=self.check_membership)).value            

        return results


def main():
    AzureRMADGroupInfo()


if __name__ == '__main__':
    main()
