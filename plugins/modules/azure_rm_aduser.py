#!/usr/bin/python
#
# Copyright (c) 2020 Cole Neubauer, (@coleneubauer)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: azure_rm_aduser

version_added: "1.5.0"

short_description: Modify an Azure Active Directory user

description:
    - Create, delete, and update an Azure Active Directory user.

options:
    tenant:
        description:
            - The tenant ID.
        type: str
        required: True
    state:
        description:
            - State of the ad user. Use C(present) to create or update an ad user and C(absent) to delete an ad user.
        type: str
        default: present
        choices:
            - absent
            - present
    object_id:
        description:
            - The object id for the user.
            - Updates or deletes the user who has this object ID.
            - Mutually exclusive with I(user_principal_name), I(attribute_name), and I(odata_filter).
        type: str
    account_enabled:
        description:
            - A boolean determing whether or not the user account is enabled.
            - Used when either creating or updating a user account.
        type: bool
    display_name:
        description:
            - The display name of the user.
            - Used when either creating or updating a user account.
        type: str
    given_name:
        description:
            - The given name for the user.
            - Used when either creating or updating a user account.
        type: str
    surname:
        description:
            - The surname for the user.
            - Used when either creating or updating a user account.
        type: str
    immutable_id:
        description:
            - The immutable_id of the user.
            - Used when either creating or updating a user account.
        type: str
    mail:
        description:
            - The primary email address of the user.
            - Used when either creating or updating a user account.
        type: str
    mail_nickname:
        description:
            - The mail alias for the user.
            - Used when either creating or updating a user account.
        type: str
    password_profile:
        description:
            - The password for the user.
            - Used when either creating or updating a user account.
        type: str
    usage_location:
        description:
            - A two letter country code, ISO standard 3166.
            - Required for a user that will be assigned licenses due to legal requirement to check for availability of services in countries.
            - Used when either creating or updating a user account.
        type: str
    user_type:
        description:
            - A string value that can be used to classify user types in your directory, such as Member and Guest.
            - Used when either creating or updating a user account.
        type: str
    user_principal_name:
        description:
            - The principal name of the user.
            - Creates, updates, or deletes the user who has this principal name.
            - Mutually exclusive with I(object_id), I(attribute_name), and I(odata_filter).
        type: str
    attribute_name:
        description:
            - The name of an attribute that you want to match to attribute_value.
            - If attribute_name is not a collection type it will update or delete the user where attribute_name is equal to attribute_value.
            - If attribute_name is a collection type it will update or delete the user where attribute_value is in attribute_name.
            - Mutually exclusive with I(object_id), I(user_principal_name), and I(odata_filter).
            - Required together with I(attribute_value).
        type: str
    attribute_value:
        description:
            - The value to match attribute_name to.
            - If attribute_name is not a collection type it will update or delete the user where attribute_name is equal to attribute_value.
            - If attribute_name is a collection type it will update or delete the user where attribute_value is in attribute_name.
            - Required together with I(attribute_name).
        type: str
    odata_filter:
        description:
            - Filter that can be used to specify a user to update or delete.
            - Mutually exclusive with I(object_id), I(attribute_name), and I(user_principal_name).
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Cole Neubauer(@coleneubauer)

'''

EXAMPLES = '''
- name: Create user
  azure_rm_aduser:
    user_principal_name: "{{ user_id }}"
    tenant: "{{ tenant_id }}"
    state: "present"
    account_enabled: "True"
    display_name: "Test_{{ user_principal_name }}_Display_Name"
    password_profile: "password"
    mail_nickname: "Test_{{ user_principal_name }}_mail_nickname"
    immutable_id: "{{ object_id }}"
    given_name: "First"
    surname: "Last"
    user_type: "Member"
    usage_location: "US"
    mail: "{{ user_principal_name }}@contoso.com"

- name: Update user with new value for account_enabled
  azure_rm_aduser:
    user_principal_name: "{{ user_id }}"
    tenant: "{{ tenant_id }}"
    state: "present"
    account_enabled: "False"

- name: Delete user
  azure_rm_aduser:
    user_principal_name: "{{ user_id }}"
    tenant: "{{ tenant_id }}"
    state: "absent"

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
    from azure.graphrbac.models import UserUpdateParameters
    from azure.graphrbac.models import UserCreateParameters
    from azure.graphrbac.models import PasswordProfile
    from azure.graphrbac.models import GraphErrorException
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMADUser(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            user_principal_name=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            object_id=dict(type='str'),
            attribute_name=dict(type='str'),
            attribute_value=dict(type='str'),
            odata_filter=dict(type='str'),
            account_enabled=dict(type='bool'),
            display_name=dict(type='str'),
            password_profile=dict(type='str', no_log=True),
            mail_nickname=dict(type='str'),
            immutable_id=dict(type='str'),
            usage_location=dict(type='str'),
            given_name=dict(type='str'),
            surname=dict(type='str'),
            user_type=dict(type='str'),
            mail=dict(type='str'),
            tenant=dict(type='str', required=True),
        )

        self.tenant = None
        self.user_principal_name = None
        self.state = None
        self.object_id = None
        self.attribute_name = None
        self.attribute_value = None
        self.odata_filter = None
        self.account_enabled = None
        self.display_name = None
        self.password_profile = None
        self.mail_nickname = None
        self.immutable_id = None
        self.usage_location = None
        self.given_name = None
        self.surname = None
        self.user_type = None
        self.mail = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(changed=False)

        mutually_exclusive = [['odata_filter', 'attribute_name', 'object_id', 'user_principal_name']]
        required_together = [['attribute_name', 'attribute_value']]
        required_one_of = [['odata_filter', 'attribute_name', 'object_id', 'user_principal_name']]

        super(AzureRMADUser, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=False,
                                            supports_tags=False,
                                            mutually_exclusive=mutually_exclusive,
                                            required_together=required_together,
                                            required_one_of=required_one_of,
                                            is_ad_resource=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        try:
            client = self.get_graphrbac_client(self.tenant)

            ad_user = self.get_exisiting_user(client)

            if self.state == 'present':

                if ad_user:  # Update, changed

                    password = None

                    if self.password_profile:
                        password = PasswordProfile(password=self.password_profile)

                    should_update = False

                    if self.immutable_id and ad_user.immutable_id != self.immutable_id:
                        should_update = True
                    if should_update or self.usage_location and ad_user.usage_location != self.usage_location:
                        should_update = True
                    if should_update or self.given_name and ad_user.given_name != self.given_name:
                        should_update = True
                    if should_update or self.surname and ad_user.surname != self.surname:
                        should_update = True
                    if should_update or self.user_type and ad_user.user_type != self.user_type:
                        should_update = True
                    if should_update or self.account_enabled is not None and ad_user.account_enabled != self.account_enabled:
                        should_update = True
                    if should_update or self.display_name and ad_user.display_name != self.display_name:
                        should_update = True
                    if should_update or password:
                        should_update = True
                    if should_update or self.user_principal_name and ad_user.user_principal_name != self.user_principal_name:
                        should_update = True
                    if should_update or self.mail_nickname and ad_user.mail_nickname != self.mail_nickname:
                        should_update = True

                    if should_update:
                        parameters = UserUpdateParameters(immutable_id=self.immutable_id,
                                                          usage_location=self.usage_location,
                                                          given_name=self.given_name,
                                                          surname=self.surname,
                                                          user_type=self.user_type,
                                                          account_enabled=self.account_enabled,
                                                          display_name=self.display_name,
                                                          password_profile=password,
                                                          user_principal_name=self.user_principal_name,
                                                          mail_nickname=self.mail_nickname)

                        client.users.update(upn_or_object_id=ad_user.object_id, parameters=parameters)

                        self.results['changed'] = True

                        # Get the updated versions of the users to return
                        # the update method, has no return value so it needs to be explicitely returned in a call
                        ad_user = self.get_exisiting_user(client)

                    else:
                        self.results['changed'] = False

                else:  # Create, changed
                    password = PasswordProfile(password=self.password_profile)
                    parameters = UserCreateParameters(account_enabled=self.account_enabled,
                                                      display_name=self.display_name,
                                                      password_profile=password,
                                                      user_principal_name=self.user_principal_name,
                                                      mail_nickname=self.mail_nickname,
                                                      immutable_id=self.immutable_id,
                                                      usage_location=self.usage_location,
                                                      given_name=self.given_name,
                                                      surname=self.surname,
                                                      user_type=self.user_type,
                                                      mail=self.mail)
                    ad_user = client.users.create(parameters=parameters)
                    self.results['changed'] = True

                self.results['ad_user'] = self.to_dict(ad_user)

            elif self.state == 'absent':
                if ad_user:  # Delete, changed
                    client.users.delete(ad_user.object_id)
                    self.results['changed'] = True
                else:  # Do nothing unchanged
                    self.results['changed'] = False

        except GraphErrorException as e:
            self.fail("failed to get ad user info {0}".format(str(e)))

        return self.results

    def get_exisiting_user(self, client):
        ad_user = None

        try:
            if self.user_principal_name is not None:
                ad_user = client.users.get(self.user_principal_name)
            elif self.object_id is not None:
                ad_user = client.users.get(self.object_id)
            elif self.attribute_name is not None and self.attribute_value is not None:
                try:
                    ad_user = list(client.users.list(filter="{0} eq '{1}'".format(self.attribute_name, self.attribute_value)))[0]
                except GraphErrorException as e:
                    # the type doesn't get more specific. Could check the error message but no guarantees that message doesn't change in the future
                    # more stable to try again assuming the first error came from the attribute being a list
                    try:
                        ad_user = list(client.users.list(filter="{0}/any(c:c eq '{1}')".format(self.attribute_name, self.attribute_value)))[0]
                    except GraphErrorException as sub_e:
                        raise
            elif self.odata_filter is not None:  # run a filter based on user input to return based on any given attribute/query
                ad_user = list(client.users.list(filter=self.odata_filter))[0]
        except GraphErrorException as e:
            # User was not found
            err_msg = str(e)
            if err_msg == "Resource '{0}' does not exist or one of its queried reference-property objects are not present.".format(self.user_principal_name):
                ad_user = None
            else:
                raise
        return ad_user

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
    AzureRMADUser()


if __name__ == '__main__':
    main()
