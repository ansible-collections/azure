#!/usr/bin/python
#
# Copyright (c) 2021 Cole Neubauer, (@coleneubauer)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: azure_rm_adgroup_info
version_added: "1.6.0"
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
            - The object id for the ad group.
            - returns the group which has this object ID.
        type: str
    attribute_name:
        description:
            - The name of an attribute that you want to match to attribute_value.
            - If attribute_name is not a collection type it will return groups where attribute_name is equal to attribute_value.
            - If attribute_name is a collection type it will return groups where attribute_value is in attribute_name.
        type: str
    attribute_value:
        description:
            - The value to match attribute_name to.
            - If attribute_name is not a collection type it will return groups where attribute_name is equal to attribute_value.
            - If attribute_name is a collection type it will groups users where attribute_value is in attribute_name.
        type: str
    odata_filter:
        description:
            - returns groups based on the the OData filter passed into this parameter.
        type: str
    check_membership:
        description:
            - The object ID of the contact, group, user, or service principal to check for membership against returned groups.
        type: str
    return_owners:
        description:
            - Indicate whether the owners of a group should be returned with the returned groups.
        default: False
        type: bool
    return_group_members:
        description:
            - Indicate whether the members of a group should be returned with the returned groups.
        default: False
        type: bool
    return_member_groups:
        description:
            - Indicate whether the groups in which a groups is a member should be returned with the returned groups.
        default: False
        type: bool
    all:
        description:
            - If True, will return all groups in tenant.
            - If False will return no users.
            - It is recommended that you instead identify a subset of groups and use filter.
        default: False
        type: bool
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Cole Neubauer(@coleneubauer)
'''

EXAMPLES = '''
    - name: Return a specific group using object_id
      azure_rm_adgroup_info:
        object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Return a specific group using object_id and  return the owners of the group
      azure_rm_adgroup_info:
        object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        return_owners: True
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Return a specific group using object_id and return the owners and members of the group
      azure_rm_adgroup_info:
        object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        return_owners: True
        return_group_members: True
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Return a specific group using object_id and return the groups the group is a member of
      azure_rm_adgroup_info:
        object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        return_member_groups: True
        tenant: "{{ tenant_id }}"

    - name: Return a specific group using object_id and check an ID for membership
      azure_rm_adgroup_info:
        object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        check_membership: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Return a specific group using displayName for attribute_name
      azure_rm_adgroup_info:
        attribute_name: "displayName"
        attribute_value: "Display-Name-Of-AD-Group"
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Return groups matching odata_filter
      azure_rm_adgroup_info:
        odata_filter: "mailNickname eq 'Mail-Nickname-Of-AD-Group'"
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Return all groups
      azure_rm_adgroup_info:
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        all: True

'''

RETURN = '''
object_id:
    description:
        - The object_id for the group.
    type: str
    returned: always
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
display_name:
    description:
        - The display name of the group.
    returned: always
    type: str
    sample: GroupName
mail_nickname:
    description:
        - The mail alias for the group.
    returned: always
    type: str
    sample: groupname
mail_enabled:
    description:
        - Whether the group is mail-enabled. Must be false. This is because only pure security groups can be created using the Graph API.
    returned: always
    type: bool
    sample: False
security_enabled:
    description:
        - Whether the group is security-enable.
    returned: always
    type: bool
    sample: False
mail:
    description:
        - The primary email address of the group.
    returned: always
    type: str
    sample: group@contoso.com
group_owners:
    description:
        - The owners of the group.
    returned: always
    type: list
group_members:
    description:
        - The members of the group.
    returned: always
    type: list
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.graphrbac.models import GraphErrorException
    from azure.graphrbac.models import CheckGroupMembershipParameters
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMADGroupInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            object_id=dict(type='str'),
            attribute_name=dict(type='str'),
            attribute_value=dict(type='str'),
            odata_filter=dict(type='str'),
            check_membership=dict(type='str'),
            return_owners=dict(type='bool', default=False),
            return_group_members=dict(type='bool', default=False),
            return_member_groups=dict(type='bool', default=False),
            all=dict(type='bool', default=False),
            tenant=dict(type='str', required=True),
        )

        self.tenant = None
        self.object_id = None
        self.attribute_name = None
        self.attribute_value = None
        self.odata_filter = None
        self.check_membership = None
        self.return_owners = False
        self.return_group_members = False
        self.return_member_groups = False
        self.all = False

        self.results = dict(changed=False)

        mutually_exclusive = [['odata_filter', 'attribute_name', 'object_id', 'all']]
        required_together = [['attribute_name', 'attribute_value']]
        required_one_of = [['odata_filter', 'attribute_name', 'object_id', 'all']]

        super(AzureRMADGroupInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
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

    def application_to_dict(self, object):
        return dict(
            app_id=object.app_id,
            object_id=object.object_id,
            display_name=object.display_name,
        )

    def serviceprincipal_to_dict(self, object):
        return dict(
            app_id=object.app_id,
            object_id=object.object_id,
            app_display_name=object.display_name,
            app_role_assignment_required=object.app_role_assignment_required
        )

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

    def result_to_dict(self, object):
        if object.object_type == "Group":
            return self.group_to_dict(object)
        elif object.object_type == "User":
            return self.user_to_dict(object)
        elif object.object_type == "Application":
            return self.application_to_dict(object)
        elif object.object_type == "ServicePrincipal":
            return self.serviceprincipal_to_dict(object)
        else:
            return object.object_type

    def set_results(self, object, client):
        results = self.group_to_dict(object)

        if results["object_id"] and self.return_owners:
            results["group_owners"] = [self.result_to_dict(object) for object in list(client.groups.list_owners(results["object_id"]))]

        if results["object_id"] and self.return_group_members:
            results["group_members"] = [self.result_to_dict(object) for object in list(client.groups.get_group_members(results["object_id"]))]

        if results["object_id"] and self.return_member_groups:
            results["member_groups"] = [self.result_to_dict(object) for object in list(client.groups.get_member_groups(results["object_id"], False))]

        if results["object_id"] and self.check_membership:
            results["is_member_of"] = client.groups.is_member_of(
                CheckGroupMembershipParameters(group_id=results["object_id"], member_id=self.check_membership)).value

        return results


def main():
    AzureRMADGroupInfo()


if __name__ == '__main__':
    main()
