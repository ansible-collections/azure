#!/usr/bin/python
#
# Copyright (c) 2020 Cole Neubauer, (@coleneubauer)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
module: azure_rm_aduser_info

version_added: "1.4.0"

short_description: Get Azure Active Directory user info

description:
    - Get Azure Active Directory user info.

options:
    object_id:
        description:
            - The object id for the user.
            - returns the user who has this object ID.
            - Mutually exclusive with I(user_principal_name), I(attribute_name), I(odata_filter) and I(all).
        type: str
    user_principal_name:
        description:
            - The principal name of the user.
            - returns the user who has this principal name.
            - Mutually exclusive with I(object_id), I(attribute_name), I(odata_filter) and I(all).
        type: str
    attribute_name:
        description:
            - The name of an attribute that you want to match to attribute_value.
            - If I(attribute_name) is not a collection type it will return users where I(attribute_name) is equal to I(attribute_value).
            - If I(attribute_name) is a collection type it will return users where I(attribute_value) is in I(attribute_name).
            - Mutually exclusive with I(object_id), I(user_principal_name), I(odata_filter) and I(all).
            - Required together with I(attribute_value).
        type: str
    attribute_value:
        description:
            - The value to match attribute_name to.
            - If I(attribute_name) is not a collection type it will return users where I(attribute_name) is equal to I(attribute_value).
            - If I(attribute_name) is a collection type it will return users where I(attribute_value) is in I(attribute_name).
            - Required together with I(attribute_name).
        type: str
    odata_filter:
        description:
            - Returns users based on the the OData filter passed into this parameter.
            - Mutually exclusive with I(object_id), I(attribute_name), I(user_principal_name) and I(all).
        type: str
    all:
        description:
            - If C(True), will return all users in tenant.
            - If C(False) will return no users.
            - It is recommended that you instead identify a subset of users and use filter.
            - Mutually exclusive with I(object_id), I(attribute_name), I(odata_filter) and I(user_principal_name).
        type: bool
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Cole Neubauer(@coleneubauer)

'''

EXAMPLES = '''
- name: Using user_principal_name
  azure.azcollection.azure_rm_aduser_info:
    user_principal_name: user@contoso.com

- name: Using object_id
  azure.azcollection.azure_rm_aduser_info:
    object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

- name: Using attribute mailNickname - not a collection
  azure.azcollection.azure_rm_aduser_info:
    attribute_name: mailNickname
    attribute_value: users_mailNickname

- name: Using attribute proxyAddresses - a collection
  azure.azcollection.azure_rm_aduser_info:
    attribute_name: proxyAddresses
    attribute_value: SMTP:user@contoso.com

- name: Using Filter mailNickname
  azure.azcollection.azure_rm_aduser_info:
    odata_filter: mailNickname eq 'user@contoso.com'

- name: Using Filter proxyAddresses
  azure.azcollection.azure_rm_aduser_info:
    odata_filter: proxyAddresses/any(c:c eq 'SMTP:user@contoso.com')
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
given_name:
    description:
        - The given name of the user.
    returned: always
    type: str
    sample: John
surname:
    description:
        - The surname of the user.
    returned: always
    type: str
    sample: Smith
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
mobile_phone:
    description:
        - The mobile phone number of the user.
    type: str
    returned: always
    sample: '+1234567890123'
company_name:
    description:
        - The name of the company that the user is associated with.
    type: str
    returned: always
    sample: "Test Company"
on_premises_extension_attributes:
    description:
        - Contains extensionAttributes1-15 for the user.
        - These extension attributes are also known as Exchange custom attributes 1-15.
        - For an onPremisesSyncEnabled user, the source of authority for this set of properties is the on-premises and is read-only.
        - For a cloud-only user (where onPremisesSyncEnabled is false), these properties can be set during the creation or update of a user object.
        - For a cloud-only user previously synced from on-premises Active Directory, these properties are read-only in Microsoft Graph/
          but can be fully managed through the Exchange Admin Center or the Exchange Online V2 module in PowerShell.
    type: dict
    returned: always
    sample: {}
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase

try:
    import asyncio
    from msgraph.generated.users.users_request_builder import UsersRequestBuilder
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMADUserInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            user_principal_name=dict(type='str'),
            object_id=dict(type='str'),
            attribute_name=dict(type='str'),
            attribute_value=dict(type='str'),
            odata_filter=dict(type='str'),
            all=dict(type='bool'),
        )

        self.user_principal_name = None
        self.object_id = None
        self.attribute_name = None
        self.attribute_value = None
        self.odata_filter = None
        self.all = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(changed=False)

        mutually_exclusive = [['odata_filter', 'attribute_name', 'object_id', 'user_principal_name', 'all']]
        required_together = [['attribute_name', 'attribute_value']]
        required_one_of = [['odata_filter', 'attribute_name', 'object_id', 'user_principal_name', 'all']]

        super(AzureRMADUserInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False,
                                                mutually_exclusive=mutually_exclusive,
                                                required_together=required_together,
                                                required_one_of=required_one_of,
                                                is_ad_resource=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        ad_users = []

        try:
            self._client = self.get_msgraph_client()

            if self.user_principal_name is not None:
                ad_users = [asyncio.get_event_loop().run_until_complete(self.get_user(self.user_principal_name))]
            elif self.object_id is not None:
                ad_users = [asyncio.get_event_loop().run_until_complete(self.get_user(self.object_id))]
            elif self.attribute_name is not None and self.attribute_value is not None:
                try:
                    users = asyncio.get_event_loop().run_until_complete(
                        self.get_users_by_filter("{0} eq '{1}'".format(self.attribute_name, self.attribute_value)))
                    ad_users = list(users.value)
                except Exception as e:
                    # the type doesn't get more specific. Could check the error message but no guarantees that message doesn't change in the future
                    # more stable to try again assuming the first error came from the attribute being a list
                    try:
                        users = asyncio.get_event_loop().run_until_complete(self.get_users_by_filter(
                            "{0}/any(c:c eq '{1}')".format(self.attribute_name, self.attribute_value)))
                        ad_users = list(users.value)
                    except Exception as sub_e:
                        raise
            elif self.odata_filter is not None:  # run a filter based on user input to return based on any given attribute/query
                users = asyncio.get_event_loop().run_until_complete(self.get_users_by_filter(self.odata_filter))
                ad_users = list(users.value)
            elif self.all:
                # this returns as a list, since we parse multiple pages
                ad_users = asyncio.get_event_loop().run_until_complete(self.get_users())
            self.results['ad_users'] = [self.to_dict(user) for user in ad_users]

        except Exception as e:
            self.fail("failed to get ad user info {0}".format(str(e)))

        return self.results

    def on_premises_extension_attributes_to_dict(self, on_premises_extension_attributes):
        extension_attributes = {}
        for index in range(1, 16 + 1):
            attribute_name = f'extension_attribute{index}'
            if hasattr(on_premises_extension_attributes, attribute_name):
                attr_value = getattr(on_premises_extension_attributes, attribute_name)
                if attr_value is not None:
                    extension_attributes[attribute_name] = attr_value
        return extension_attributes

    def to_dict(self, object):
        return dict(
            object_id=object.id,
            display_name=object.display_name,
            user_principal_name=object.user_principal_name,
            mail_nickname=object.mail_nickname,
            mail=object.mail,
            account_enabled=object.account_enabled,
            user_type=object.user_type,
            company_name=object.company_name,
            mobile_phone=object.mobile_phone,
            surname=object.surname,
            given_name=object.given_name,
            on_premises_extension_attributes=self.on_premises_extension_attributes_to_dict(object.on_premises_extension_attributes)
        )

    async def get_user(self, object):
        request_configuration = UsersRequestBuilder.UsersRequestBuilderGetRequestConfiguration(
            query_parameters=UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
                select=["accountEnabled", "displayName", "mail", "mailNickname", "id", "userPrincipalName",
                        "userType", "companyName", "mobilePhone", "onPremisesExtensionAttributes", "surname",
                        "givenName"]
            ),
        )
        return await self._client.users.by_user_id(object).get(request_configuration=request_configuration)

    async def get_users(self):
        request_configuration = UsersRequestBuilder.UsersRequestBuilderGetRequestConfiguration(
            query_parameters=UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
                select=["accountEnabled", "displayName", "mail", "mailNickname", "id", "userPrincipalName",
                        "userType", "companyName", "mobilePhone", "onPremisesExtensionAttributes", "surname",
                        "givenName"]
            ),
        )
        users = []
        # paginated response can be quite large
        response = await self._client.users.get(request_configuration=request_configuration)
        if response:
            users += response.value
        while response is not None and response.odata_next_link is not None:
            response = await self._client.users.with_url(response.odata_next_link).get(request_configuration=request_configuration)
            if response:
                users += response.value

        return users

    async def get_users_by_filter(self, filter):
        return await self._client.users.get(
            request_configuration=UsersRequestBuilder.UsersRequestBuilderGetRequestConfiguration(
                query_parameters=UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
                    filter=filter,
                    select=["accountEnabled", "displayName", "mail", "mailNickname", "id", "userPrincipalName",
                            "userType", "companyName", "onPremisesExtensionAttributes", "surname", "givenName"],
                    count=True
                ),
            ))


def main():
    AzureRMADUserInfo()


if __name__ == '__main__':
    main()
