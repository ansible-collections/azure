#!/usr/bin/python
#
# Copyright (c) 2021 Cole Neubauer, (@coleneubauer)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
module: azure_rm_adgroup
version_added: "1.6.0"
short_description: Manage Azure Active Directory group
description:
    - Create, update or delete Azure Active Directory group.
options:
    state:
        description:
            - Assert the state of the resource group. Use C(present) to create or update and C(absent) to delete.
        default: present
        choices:
            - absent
            - present
        type: str
    object_id:
        description:
            - The object id for the ad group.
            - Can be used to reference when updating an existing group.
            - Ignored when attempting to create a group.
        type: str
    display_name:
        description:
            - The display name of the ad group.
            - Can be used with I(mail_nickname) instead of I(object_id) to reference existing group.
            - Required when creating a new ad group.
        type: str
    mail_nickname:
        description:
            - The mail nickname of the ad group.
            - Can be used with I(display_name) instead of I(object_id) to reference existing group.
            - Required when creating a new ad group.
        type: str
    present_members:
        description:
            - The azure ad objects asserted to be members of the group.
            - This list does not need to be all inclusive. Objects that are members and not on this list remain members.
        type: list
        elements: str
    absent_members:
        description:
            - The azure ad objects asserted to not be members of the group.
        type: list
        elements: str
    present_owners:
        description:
            - The azure ad objects asserted to be owners of the group.
            - This list does not need to be all inclusive. Objects that are owners and not on this list remain members.
        type: list
        elements: str
    absent_owners:
        description:
            - The azure ad objects asserted to not be owners of the group.
        type: list
        elements: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Cole Neubauer(@coleneubauer)
'''

EXAMPLES = '''
- name: Create Group
  azure_rm_adgroup:
    display_name: "Group-Name"
    mail_nickname: "Group-Mail-Nickname"
    state: 'present'

- name: Delete Group using display_name and mail_nickname
  azure_rm_adgroup:
    display_name: "Group-Name"
    mail_nickname: "Group-Mail-Nickname"
    state: 'absent'

- name: Delete Group using object_id
  azure_rm_adgroup:
    object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    state: 'absent'

- name: Ensure Users are Members of a Group using display_name and mail_nickname
  azure_rm_adgroup:
    display_name: "Group-Name"
    mail_nickname: "Group-Mail-Nickname"
    state: 'present'
    present_members:
      - "https://graph.windows.net/{{ tenant_id }}/directoryObjects/{{ ad_object_1_object_id }}"
      - "https://graph.windows.net/{{ tenant_id }}/directoryObjects/{{ ad_object_2_object_id }}"

- name: Ensure Users are Members of a Group using object_id
  azure_rm_adgroup:
    object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    state: 'present'
    present_members:
      - "https://graph.windows.net/{{ ad_object_1_tenant_id }}/directoryObjects/{{ ad_object_1_object_id }}"
      - "https://graph.windows.net/{{ ad_object_2_tenant_id }}/directoryObjects/{{ ad_object_2_object_id }}"

- name: Ensure Users are not Members of a Group using display_name and mail_nickname
  azure_rm_adgroup:
    display_name: "Group-Name"
    mail_nickname: "Group-Mail-Nickname"
    state: 'present'
    absent_members:
      - "{{ ad_object_1_object_id }}"

- name: Ensure Users are Members of a Group using object_id
  azure_rm_adgroup:
    object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    state: 'present'
    absent_members:
      - "{{ ad_object_1_object_id }}"

- name: Ensure Users are Owners of a Group using display_name and mail_nickname
  azure_rm_adgroup:
    display_name: "Group-Name"
    mail_nickname: "Group-Mail-Nickname"
    state: 'present'
    present_owners:
      - "https://graph.windows.net/{{ tenant_id }}/directoryObjects/{{ ad_object_1_object_id }}"
      - "https://graph.windows.net/{{ tenant_id }}/directoryObjects/{{ ad_object_2_object_id }}"

- name: Ensure Users are Owners of a Group using object_id
  azure_rm_adgroup:
    object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    state: 'present'
    present_owners:
      - "https://graph.windows.net/{{ ad_object_1_tenant_id }}/directoryObjects/{{ ad_object_1_object_id }}"
      - "https://graph.windows.net/{{ ad_object_2_tenant_id }}/directoryObjects/{{ ad_object_2_object_id }}"

- name: Ensure Users are not Owners of a Group using display_name and mail_nickname
  azure_rm_adgroup:
    display_name: "Group-Name"
    mail_nickname: "Group-Mail-Nickname"
    state: 'present'
    absent_owners:
      - "{{ ad_object_1_object_id }}"
      - "{{ ad_object_2_object_id }}"

- name: Ensure Users are Owners of a Group using object_id
  azure_rm_adgroup:
    object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    state: 'present'
    absent_owners:
      - "{{ ad_object_1_object_id }}"
      - "{{ ad_object_2_object_id }}"
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
    from msgraph.generated.models.group import Group
    from msgraph.generated.groups.item.transitive_members.transitive_members_request_builder import \
        TransitiveMembersRequestBuilder
    from msgraph.generated.models.reference_create import ReferenceCreate
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMADGroup(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            object_id=dict(type='str'),
            display_name=dict(type='str'),
            mail_nickname=dict(type='str'),
            present_members=dict(type='list', elements='str'),
            present_owners=dict(type='list', elements='str'),
            absent_members=dict(type='list', elements='str'),
            absent_owners=dict(type='list', elements='str'),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
        )

        self.display_name = None
        self.mail_nickname = None
        self.object_id = None
        self.present_members = []
        self.present_owners = []
        self.absent_members = []
        self.absent_owners = []
        self.state = None
        self.results = dict(changed=False)
        self._client = None

        super(AzureRMADGroup, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=False,
                                             supports_tags=False,
                                             is_ad_resource=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        # TODO remove ad_groups return. Returns as one object always
        ad_groups = []

        try:
            self._client = self.get_msgraph_client()
            ad_groups = []

            if self.display_name and self.mail_nickname:
                filter = "displayName eq '{0}' and mailNickname eq '{1}'".format(self.display_name, self.mail_nickname)
                ad_groups = asyncio.get_event_loop().run_until_complete(self.get_group_list(filter))
                if ad_groups:
                    self.object_id = ad_groups[0].id

            elif self.object_id:
                ad_groups = [asyncio.get_event_loop().run_until_complete(self.get_group(self.object_id))]

            if ad_groups:
                if self.state == "present":
                    self.results["changed"] = False
                elif self.state == "absent":
                    asyncio.get_event_loop().run_until_complete(self.delete_group(self.object_id))
                    ad_groups = []
                    self.results["changed"] = True
            else:
                if self.state == "present":
                    if self.display_name and self.mail_nickname:
                        group = Group(
                            mail_enabled=False,
                            security_enabled=True,
                            group_types=[],
                            display_name=self.display_name,
                            mail_nickname=self.mail_nickname,
                        )

                        ad_groups = [asyncio.get_event_loop().run_until_complete(self.create_group(group))]
                        self.results["changed"] = True
                    else:
                        raise ValueError(
                            'The group does not exist. Both display_name : {0} and mail_nickname : {1} must be passed to create a new group'
                            .format(self.display_name, self.mail_nickname))
                elif self.state == "absent":
                    self.results["changed"] = False

            if ad_groups and ad_groups[0] is not None:
                self.update_members(ad_groups[0].id)
                self.update_owners(ad_groups[0].id)
                self.results.update(self.set_results(ad_groups[0]))

        except Exception as e:
            self.fail(e)
        return self.results

    def update_members(self, group_id):
        current_members = []

        if self.present_members or self.absent_members:
            ret = asyncio.get_event_loop().run_until_complete(self.get_group_members(group_id))
            current_members = [object.id for object in ret.value]

        if self.present_members:
            present_members_by_object_id = self.dictionary_from_object_urls(self.present_members)

            members_to_add = list(set(present_members_by_object_id.keys()) - set(current_members))

            if members_to_add:
                for member_object_id in members_to_add:
                    asyncio.get_event_loop().run_until_complete(
                        self.add_group_member(group_id, present_members_by_object_id[member_object_id]))
                self.results["changed"] = True

        if self.absent_members:
            members_to_remove = list(set(self.absent_members).intersection(set(current_members)))

            if members_to_remove:
                for member in members_to_remove:
                    asyncio.get_event_loop().run_until_complete(self.delete_group_member(group_id, member))
                self.results["changed"] = True

    def update_owners(self, group_id):
        current_owners = []

        if self.present_owners or self.absent_owners:
            ret = asyncio.get_event_loop().run_until_complete(self.get_group_owners(group_id))
            current_owners = [object.id for object in ret.value]

        if self.present_owners:

            present_owners_by_object_id = self.dictionary_from_object_urls(self.present_owners)
            owners_to_add = list(set(present_owners_by_object_id.keys()) - set(current_owners))

            if owners_to_add:
                for owner_object_id in owners_to_add:
                    asyncio.get_event_loop().run_until_complete(
                        self.add_gropup_owner(group_id, present_owners_by_object_id[owner_object_id]))
                self.results["changed"] = True

        if self.absent_owners:
            owners_to_remove = list(set(self.absent_owners).intersection(set(current_owners)))

            if owners_to_remove:
                for owner in owners_to_remove:
                    asyncio.get_event_loop().run_until_complete(self.remove_gropup_owner(group_id, owner))
                self.results["changed"] = True

    def dictionary_from_object_urls(self, object_urls):
        objects_by_object_id = {}

        for urls in object_urls:
            object_id = urls.split("/")[-1]
            objects_by_object_id[object_id] = urls

        return objects_by_object_id

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

        if results["object_id"] and (self.present_owners or self.absent_owners):
            ret = asyncio.get_event_loop().run_until_complete(self.get_group_owners(results["object_id"]))
            results["group_owners"] = [self.result_to_dict(object) for object in ret.value]

        if results["object_id"] and (self.present_members or self.absent_members):
            ret = asyncio.get_event_loop().run_until_complete(self.get_group_members(results["object_id"]))
            results["group_members"] = [self.result_to_dict(object) for object in ret.value]

        return results

    async def create_group(self, create_group):
        return await self._client.groups.post(body=create_group)

    async def delete_group(self, group_id):
        await self._client.groups.by_group_id(group_id).delete()

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

    async def get_group_members(self, group_id, filters=None):
        request_configuration = TransitiveMembersRequestBuilder.TransitiveMembersRequestBuilderGetRequestConfiguration(
            query_parameters=TransitiveMembersRequestBuilder.TransitiveMembersRequestBuilderGetQueryParameters(
                count=True,
            ),
        )
        if filters:
            request_configuration.query_parameters.filter = filters
        return await self._client.groups.by_group_id(group_id).transitive_members.get(
            request_configuration=request_configuration)

    async def add_group_member(self, group_id, obj_id):
        request_body = ReferenceCreate(
            odata_id="https://graph.microsoft.com/v1.0/directoryObjects/{0}".format(obj_id),
        )
        await self._client.groups.by_group_id(group_id).members.ref.post(body=request_body)

    async def delete_group_member(self, group_id, member_id):
        await self._client.groups.by_group_id(group_id).members.by_directory_object_id(member_id).ref.delete()

    async def get_group_owners(self, group_id):
        request_configuration = GroupsRequestBuilder.GroupsRequestBuilderGetRequestConfiguration(
            query_parameters=GroupsRequestBuilder.GroupsRequestBuilderGetQueryParameters(
                count=True,
            ),
            headers={'ConsistencyLevel': "eventual", }
        )
        return await self._client.groups.by_group_id(group_id).owners.get(request_configuration=request_configuration)

    async def add_gropup_owner(self, group_id, obj_id):
        request_body = ReferenceCreate(
            odata_id="https://graph.microsoft.com/v1.0/users/{0}".format(obj_id),
        )
        await self._client.groups.by_group_id(group_id).owners.ref.post(body=request_body)

    async def remove_gropup_owner(self, group_id, obj_id):
        await self._client.groups.by_group_id(group_id).owners.by_directory_object_id(obj_id).ref.delete()


def main():
    AzureRMADGroup()


if __name__ == '__main__':
    main()
