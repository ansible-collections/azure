#!/usr/bin/python
#
# Copyright (c) 2021 Cole Neubauer, (@coleneubauer), xuzhang3 (@xuzhang3)
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
    object_id:
        description:
            - The object id for the ad group.
            - returns the group which has this object ID.
        type: str
    attribute_name:
        description:
            - The name of an attribute that you want to match to I(attribute_value).
            - If I(attribute_name) is not a collection type it will return groups where I(attribute_name) is equal to I(attribute_value).
            - If I(attribute_name) is a collection type it will return groups where I(attribute_value) is in I(attribute_name).
        type: str
    attribute_value:
        description:
            - The value to match attribute_name to.
            - If I(attribute_name) is not a collection type it will return groups where I(attribute_name) is equal to I(attribute_value).
            - If I(attribute_name) is a collection type it will groups users where I(attribute_value) is in I(attribute_name).
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
    - Xu Zhang(@xuzhang)
'''

EXAMPLES = '''
- name: Return a specific group using object_id
  azure_rm_adgroup_info:
    object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

- name: Return a specific group using object_id and  return the owners of the group
  azure_rm_adgroup_info:
    object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    return_owners: true

- name: Return a specific group using object_id and return the owners and members of the group
  azure_rm_adgroup_info:
    object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    return_owners: true
    return_group_members: true

- name: Return a specific group using object_id and return the groups the group is a member of
  azure_rm_adgroup_info:
    object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    return_member_groups: true

- name: Return a specific group using object_id and check an ID for membership
  azure_rm_adgroup_info:
    object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    check_membership: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

- name: Return a specific group using displayName for attribute_name
  azure_rm_adgroup_info:
    attribute_name: "displayName"
    attribute_value: "Display-Name-Of-AD-Group"

- name: Return groups matching odata_filter
  azure_rm_adgroup_info:
    odata_filter: "mailNickname eq 'Mail-Nickname-Of-AD-Group'"

- name: Return all groups
  azure_rm_adgroup_info:
    all: true
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
    import asyncio
    from msgraph.generated.groups.groups_request_builder import GroupsRequestBuilder
    from msgraph.generated.groups.item.transitive_members.transitive_members_request_builder import \
        TransitiveMembersRequestBuilder
    from msgraph.generated.groups.item.get_member_groups.get_member_groups_post_request_body import \
        GetMemberGroupsPostRequestBody
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
        )

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
        self._client = None

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
            self._client = self.get_msgraph_client()

            if self.object_id is not None:
                ad_groups = [asyncio.get_event_loop().run_until_complete(self.get_group(self.object_id))]
            elif self.attribute_name is not None and self.attribute_value is not None:
                ad_groups = asyncio.get_event_loop().run_until_complete(
                    self.get_group_list(filter="{0} eq '{1}'".format(self.attribute_name, self.attribute_value)))
            elif self.odata_filter is not None:  # run a filter based on user input
                ad_groups = asyncio.get_event_loop().run_until_complete(self.get_group_list(filter=self.odata_filter))
            elif self.all:
                ad_groups = asyncio.get_event_loop().run_until_complete(self.get_group_list())
            self.results['ad_groups'] = [self.set_results(group) for group in ad_groups]
        except Exception as e:
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
            object_id=object.id,
            app_display_name=object.display_name,
            app_role_assignment_required=object.app_role_assignment_required
        )

    def group_to_dict(self, object):
        return dict(
            object_id=object.id,
            display_name=object.display_name,
            mail_nickname=object.mail_nickname,
            mail_enabled=object.mail_enabled,
            security_enabled=object.security_enabled,
            mail=object.mail
        )

    def user_to_dict(self, object):
        return dict(
            object_id=object.id,
            display_name=object.display_name,
            user_principal_name=object.user_principal_name,
            mail_nickname=object.mail_nickname,
            mail=object.mail,
            account_enabled=object.account_enabled,
            user_type=object.user_type
        )

    def result_to_dict(self, object):
        if object.odata_type == "#microsoft.graph.group":
            return self.group_to_dict(object)
        elif object.odata_type == "#microsoft.graph.user":
            return self.user_to_dict(object)
        elif object.odata_type == "#microsoft.graph.application":
            return self.application_to_dict(object)
        elif object.odata_type == "#microsoft.graph.servicePrincipal":
            return self.serviceprincipal_to_dict(object)
        else:
            return object.odata_type

    def set_results(self, object):
        results = self.group_to_dict(object)

        if results["object_id"] and self.return_owners:
            ret = asyncio.get_event_loop().run_until_complete(self.get_group_owners(results["object_id"]))
            results["group_owners"] = [self.result_to_dict(object) for object in ret.value]

        if results["object_id"] and self.return_group_members:
            ret = asyncio.get_event_loop().run_until_complete(self.get_group_members(results["object_id"]))
            results["group_members"] = [self.result_to_dict(object) for object in ret.value]

        if results["object_id"] and self.return_member_groups:
            ret = asyncio.get_event_loop().run_until_complete(self.get_member_groups(results["object_id"]))
            results["member_groups"] = [self.result_to_dict(object) for object in list(ret.value)]

        if results["object_id"] and self.check_membership:
            filter = "id eq '{0}' ".format(self.check_membership)
            ret = asyncio.get_event_loop().run_until_complete(self.get_group_members(results["object_id"], filter))
            results["is_member_of"] = True if ret.value and len(ret.value) != 0 else False

        return results

    async def get_group(self, group_id):
        return await self._client.groups.by_group_id(group_id).get()

    async def get_group_list(self, filter=None):
        if filter:
            request_configuration = GroupsRequestBuilder.GroupsRequestBuilderGetRequestConfiguration(
                query_parameters=GroupsRequestBuilder.GroupsRequestBuilderGetQueryParameters(
                    count=True,
                    filter=filter,
                ),
            )
            groups = await self._client.groups.get(request_configuration=request_configuration)
        else:
            groups = await self._client.groups.get()

        if groups and groups.value:
            return groups.value

        return []

    async def get_group_owners(self, group_id):
        request_configuration = GroupsRequestBuilder.GroupsRequestBuilderGetRequestConfiguration(
            query_parameters=GroupsRequestBuilder.GroupsRequestBuilderGetQueryParameters(
                count=True,
                select=['id', 'displayName', 'userPrincipalName', 'mailNickname', 'mail', 'accountEnabled', 'userType',
                        'appId', 'appRoleAssignmentRequired']

            ),
        )
        return await self._client.groups.by_group_id(group_id).owners.get(request_configuration=request_configuration)

    async def get_group_members(self, group_id, filters=None):
        request_configuration = TransitiveMembersRequestBuilder.TransitiveMembersRequestBuilderGetRequestConfiguration(
            query_parameters=TransitiveMembersRequestBuilder.TransitiveMembersRequestBuilderGetQueryParameters(
                count=True,
                select=['id', 'displayName', 'userPrincipalName', 'mailNickname', 'mail', 'accountEnabled', 'userType',
                        'appId', 'appRoleAssignmentRequired']

            ),
        )
        if filters:
            request_configuration.query_parameters.filter = filters
        return await self._client.groups.by_group_id(group_id).transitive_members.get(
            request_configuration=request_configuration)

    async def get_member_groups(self, obj_id):
        request_body = GetMemberGroupsPostRequestBody(security_enabled_only=False)
        return await self._client.groups.by_group_id(obj_id).get_member_groups.post(body=request_body)


def main():
    AzureRMADGroupInfo()


if __name__ == '__main__':
    main()
