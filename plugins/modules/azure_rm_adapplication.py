#!/usr/bin/python
#
# Copyright (c) 2020 Guopeng Lin, <linguopeng1998@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_adapplication

version_added: "1.6.0"

short_description: Manage Azure Active Directory application

description:
    - Manage Azure Active Directory application.

options:
    tenant:
        description:
            - The tenant ID.
        type: str
        required: True

    app_id:
        description:
            - Application ID.
        type: str

    display_name:
        description:
            - The display name of the application.
        type: str

    app_roles:
        description:
            - Declare the roles you want to associate with your application.
        type: list
        elements: dict
        suboptions:
            allowed_member_types:
                description:
                    - Specifies whether this app role can be assigned to users and groups I(allowed_member_types=User).
                    - To other application's I(allowed_member_types=Application).
                    - Or both C(User) and C(Appplication).
                type: list
                elements: str
                required: True
            description:
                description:
                    - The description for the app role.
                    - This is displayed when the app role is being assigned.
                    - if the app role functions as an application permission, during consent experiences.
                type: str
            display_name:
                description:
                    - Display name for the permission that appears in the app role assignment and consent experiences.
                type: str
            is_enabled:
                description:
                    - When creating or updating an app role, this must be set to true (which is the default).
                    - To delete a role, this must first be set to false.
                    - At that point, in a subsequent call, this role may be removed.
                type: bool
            value:
                description:
                    - Specifies the value to include in the roles claim in ID tokens and access tokens authenticating an assigned user or service principal.
                    - Must not exceed 120 characters in length.
                    - Allowed characters include ! # $ % & ' ( ) * + , - . / : ; < = > ? @ [ ] ^ + _ ` { | } ~, and characters in the ranges 0-9, A-Z and a-z.
                    - Any other character, including the space character, are not allowed.
                type: str

    available_to_other_tenants:
        description:
            - The application can be used from any Azure AD tenants.
        type: bool

    credential_description:
        description:
            - The description of the password.
        type: str

    end_date:
        description:
            - Date or datetime after which credentials expire(e.g. '2017-12-31').
            - Default value is one year after current time.
        type: str

    homepage:
        description:
            - The url where users can sign in and use your app.
        type: str

    identifier_uris:
        description:
            - Space-separated unique URIs that Azure AD can use for this app.
        elements: str
        type: list

    key_type:
        description:
            - The type of the key credentials associated with the application.
        type: str
        default: AsymmetricX509Cert
        choices:
            - AsymmetricX509Cert
            - Password
            - Symmetric

    key_usage:
        description:
            - The usage of the key credentials associated with the application.
        type: str
        default: Verify
        choices:
            - Sign
            - Verify

    key_value:
        description:
            - The value for the key credentials associated with the application.
        type: str

    native_app:
        description:
            - An application which can be installed on a user's device or computer.
        type: bool

    oauth2_allow_implicit_flow:
        description:
            - Whether to allow implicit grant flow for OAuth2.
        type: bool

    optional_claims:
        description:
            - Declare the optional claims for the application.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of the optional claim.
                type: str
                required: True
            source:
                description:
                    - The source (directory object) of the claim.
                    - There are predefined claims and user-defined claims from extension properties.
                    - If the source value is null, the claim is a predefined optional claim.
                    - If the source value is user, the value in the name property is the extension property from the user object.
                type: str
            essential:
                description:
                    - If the value is true, the claim specified by the client is necessary to ensure a smooth authorization experience
                      for the specific task requested by the end user.
                    - The default value is false.
                default: false
                type: bool
            additional_properties:
                description:
                    - Additional properties of the claim.
                    - If a property exists in this collection, it modifies the behavior of the optional claim specified in the name property.
                type: str
    password:
        description:
            - App password, aka 'client secret'.
        type: str

    reply_urls:
        description:
            - Space-separated URIs to which Azure AD will redirect in response to an OAuth 2.0 request.
            - The value does not need to be a physical endpoint, but must be a valid URI.
        type: list
        elements: str

    required_resource_accesses:
        description:
            - Resource scopes and roles the application requires access to.
            - Should be in manifest json format.
        type: list
        elements: dict
        suboptions:
            resource_app_id:
                description:
                    - The unique identifier for the resource that the application requires access to.
                    - This should be equal to the appId declared on the target resource application.
                type: str
            resource_access:
                description:
                    - The description of the app role.
                type: list
                elements: dict
                suboptions:
                    id:
                        description:
                            - The unique identifier for one of the oauth2PermissionScopes or appRole instances that the resource application exposes.
                        type: str
                    type:
                        description:
                            - Specifies whether the id property references an oauth2PermissionScopes or an appRole.
                            - Possible values are Scope or Role.
                        type: str

    start_date:
        description:
            - Date or datetime at which credentials become valid, such as '2017-01-01'.
            - Default value is current time.
        type: str
    allow_guests_sign_in:
        description:
            - A property on the application to indicate if the application accepts other IDPs or not or partially accepts.
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

author:
    guopeng_lin (@guopenglin)
    haiyuan_zhang (@haiyuazhang)
    Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
  - name: Create ad application
    azure_rm_adapplication:
      tenant: "{{ tenant_id }}"
      display_name: "{{ display_name }}"

  - name: Create application with more parameter
    azure_rm_adapplication:
      tenant: "{{ tenant_id }}"
      display_name: "{{ display_name }}"
      available_to_other_tenants: False
      credential_description: "for test"
      end_date: 2021-10-01
      start_date: 2021-05-18
      identifier_uris: fredtest02.com

  - name: delete ad application
    azure_rm_adapplication:
      tenant: "{{ tenant_id }}"
      app_id: "{{ app_id }}"
      state: absent
'''

RETURN = '''
output:
    description:
        - Current state of the adapplication.
    type: complex
    returned: awalys
    contains:
        display_name:
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
        object_id:
            description:
                - Object ID of the application
            returned: always
            type: str
            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        available_to_other_tenants:
            description:
                - The application can be used from any Azure AD tenants.
            returned: always
            type: bool
            sample: false
        homepage:
            description:
                - The url where users can sign in and use your app.
            returned: always
            type: str
            sample: null
        identifier_uris:
            description:
                - Space-separated unique URIs that Azure AD can use for this app.
            returned: always
            type: list
            sample: []
        oauth2_allow_implicit_flow:
            description:
                - Whether to allow implicit grant flow for OAuth2.
            returned: always
            type: bool
            sample: false
        optional_claims:
            description:
                - The optional claims for the application.
            returned: always
            type: list
            sample: []
        reply_urls:
            description:
                - Space-separated URIs to which Azure AD will redirect in response to an OAuth 2.0 request.
            returned: always
            type: list
            sample: []
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.graphrbac.models import GraphErrorException
    import datetime
    from dateutil.relativedelta import relativedelta
    import dateutil.parser
    from azure.graphrbac.models import ApplicationCreateParameters
    import uuid
    from azure.graphrbac.models import ResourceAccess
    from azure.graphrbac.models import RequiredResourceAccess
    from azure.graphrbac.models import AppRole
    from azure.graphrbac.models import PasswordCredential, KeyCredential
    from azure.graphrbac.models import ApplicationUpdateParameters
except ImportError:
    # This is handled in azure_rm_common
    pass

app_role_spec = dict(
    allowed_member_types=dict(
        type='list',
        elements='str',
        required=True
    ),
    description=dict(
        type='str'
    ),
    display_name=dict(
        type='str'
    ),
    is_enabled=dict(
        type='bool'
    ),
    value=dict(
        type='str'
    )
)

optional_claims_spec = dict(
    name=dict(
        type='str',
        required=True
    ),
    source=dict(
        type='str'
    ),
    essential=dict(
        type='bool',
        default=False
    ),
    additional_properties=dict(
        type='str'
    )
)
required_resource_accesses_spec = dict(
    resource_app_id=dict(
        type='str'
    ),
    resource_access=dict(
        type='list',
        elements='dict',
        options=dict(
            id=dict(
                type='str'
            ),
            type=dict(
                type='str'
            )
        )
    )
)


class AzureRMADApplication(AzureRMModuleBaseExt):
    def __init__(self):

        self.module_arg_spec = dict(
            tenant=dict(type='str', required=True),
            app_id=dict(type='str'),
            display_name=dict(type='str'),
            app_roles=dict(type='list', elements='dict', options=app_role_spec),
            available_to_other_tenants=dict(type='bool'),
            credential_description=dict(type='str'),
            end_date=dict(type='str'),
            homepage=dict(type='str'),
            allow_guests_sign_in=dict(type='bool'),
            identifier_uris=dict(type='list', elements='str'),
            key_type=dict(type='str', default='AsymmetricX509Cert', choices=['AsymmetricX509Cert', 'Password', 'Symmetric']),
            key_usage=dict(type='str', default='Verify', choices=['Sign', 'Verify']),
            key_value=dict(type='str', no_log=True),
            native_app=dict(type='bool'),
            oauth2_allow_implicit_flow=dict(type='bool'),
            optional_claims=dict(type='list', elements='dict', options=optional_claims_spec),
            password=dict(type='str', no_log=True),
            reply_urls=dict(type='list', elements='str'),
            start_date=dict(type='str'),
            required_resource_accesses=dict(type='list', elements='dict', options=required_resource_accesses_spec),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.state = None
        self.tenant = None
        self.app_id = None
        self.display_name = None
        self.app_roles = None
        self.available_to_other_tenants = None
        self.credential_description = None
        self.end_date = None
        self.homepage = None
        self.identifier_uris = None
        self.key_type = None
        self.key_usage = None
        self.key_value = None
        self.native_app = None
        self.oauth2_allow_implicit_flow = None
        self.optional_claims = None
        self.password = None
        self.reply_urls = None
        self.start_date = None
        self.required_resource_accesses = None
        self.allow_guests_sign_in = None
        self.results = dict(changed=False)

        super(AzureRMADApplication, self).__init__(derived_arg_spec=self.module_arg_spec,
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
            key_creds, password_creds, required_accesses, app_roles, optional_claims = None, None, None, None, None
            if self.native_app:
                if self.identifier_uris:
                    raise self.fail("'identifier_uris' is not required for creating a native application")
            else:
                password_creds, key_creds = self.build_application_creds(self.password, self.key_value, self.key_type, self.key_usage,
                                                                         self.start_date, self.end_date, self.credential_description)
            if self.required_resource_accesses:
                required_accesses = self.build_application_accesses(self.required_resource_accesses)

            if self.app_roles:
                app_roles = self.build_app_roles(self.app_roles)

            client = self.get_graphrbac_client(self.tenant)
            app_create_param = ApplicationCreateParameters(available_to_other_tenants=self.available_to_other_tenants,
                                                           display_name=self.display_name,
                                                           identifier_uris=self.identifier_uris,
                                                           homepage=self.homepage,
                                                           reply_urls=self.reply_urls,
                                                           key_credentials=key_creds,
                                                           password_credentials=password_creds,
                                                           oauth2_allow_implicit_flow=self.oauth2_allow_implicit_flow,
                                                           required_resource_access=required_accesses,
                                                           app_roles=app_roles,
                                                           allow_guests_sign_in=self.allow_guests_sign_in,
                                                           optional_claims=self.optional_claims)
            response = client.applications.create(app_create_param)
            self.results['changed'] = True
            self.results.update(self.to_dict(response))
            return response
        except GraphErrorException as ge:
            self.fail("Error creating application, display_name {0} - {1}".format(self.display_name, str(ge)))

    def update_resource(self, old_response):
        try:
            client = self.get_graphrbac_client(self.tenant)
            key_creds, password_creds, required_accesses, app_roles, optional_claims = None, None, None, None, None
            if self.native_app:
                if self.identifier_uris:
                    raise self.fail("'identifier_uris' is not required for creating a native application")
            else:
                password_creds, key_creds = self.build_application_creds(self.password, self.key_value, self.key_type, self.key_usage,
                                                                         self.start_date, self.end_date, self.credential_description)
            if self.required_resource_accesses:
                required_accesses = self.build_application_accesses(self.required_resource_accesses)

            if self.app_roles:
                app_roles = self.build_app_roles(self.app_roles)
            app_update_param = ApplicationUpdateParameters(available_to_other_tenants=self.available_to_other_tenants,
                                                           display_name=self.display_name,
                                                           identifier_uris=self.identifier_uris,
                                                           homepage=self.homepage,
                                                           reply_urls=self.reply_urls,
                                                           key_credentials=key_creds,
                                                           password_credentials=password_creds,
                                                           oauth2_allow_implicit_flow=self.oauth2_allow_implicit_flow,
                                                           required_resource_access=required_accesses,
                                                           allow_guests_sign_in=self.allow_guests_sign_in,
                                                           app_roles=app_roles,
                                                           optional_claims=self.optional_claims)
            client.applications.patch(old_response['object_id'], app_update_param)
            self.results['changed'] = True
            self.results.update(self.get_resource())

        except GraphErrorException as ge:
            self.fail("Error updating the application app_id {0} - {1}".format(self.app_id, str(ge)))

    def delete_resource(self, response):
        try:
            client = self.get_graphrbac_client(self.tenant)
            client.applications.delete(response.get('object_id'))
            self.results['changed'] = True
            return True
        except GraphErrorException as ge:
            self.fail("Error deleting application app_id {0} display_name {1} - {2}".format(self.app_id, self.display_name, str(ge)))

    def get_resource(self):
        try:
            client = self.get_graphrbac_client(self.tenant)
            existing_apps = []
            if self.app_id:
                existing_apps = list(client.applications.list(filter="appId eq '{0}'".format(self.app_id)))
            if not existing_apps:
                return False
            result = existing_apps[0]
            return self.to_dict(result)
        except GraphErrorException as ge:
            self.log("Did not find the graph instance instance {0} - {1}".format(self.app_id, str(ge)))
            return False

    def check_update(self, response):
        for key in list(self.module_arg_spec.keys()):
            attr = getattr(self, key)
            if attr and key in response:
                if (response and attr != response[key]) or response[key] is None:
                    return True
        return False

    def to_dict(self, object):
        app_roles = [{
            'id': app_role.id,
            'display_name': app_role.display_name,
            'is_enabled': app_role.is_enabled,
            'value': app_role.value,
            "description": app_role.description
        }for app_role in object.app_roles]
        return dict(
            app_id=object.app_id,
            object_id=object.object_id,
            display_name=object.display_name,
            app_roles=app_roles,
            available_to_other_tenants=object.available_to_other_tenants,
            homepage=object.homepage,
            identifier_uris=object.identifier_uris,
            oauth2_allow_implicit_flow=object.oauth2_allow_implicit_flow,
            optional_claims=object.optional_claims,
            allow_guests_sign_in=object.allow_guests_sign_in,
            reply_urls=object.reply_urls
        )

    def build_application_creds(self, password=None, key_value=None, key_type=None, key_usage=None,
                                start_date=None, end_date=None, key_description=None):
        if password and key_value:
            raise self.fail('specify either password or key_value, but not both.')

        if not start_date:
            start_date = datetime.datetime.utcnow()
        elif isinstance(start_date, str):
            start_date = dateutil.parser.parse(start_date)

        if not end_date:
            end_date = start_date + relativedelta(years=1) - relativedelta(hours=24)
        elif isinstance(end_date, str):
            end_date = dateutil.parser.parse(end_date)

        custom_key_id = None
        if key_description and password:
            custom_key_id = self.encode_custom_key_description(key_description)

        key_type = key_type or 'AsymmetricX509Cert'
        key_usage = key_usage or 'Verify'

        password_creds = None
        key_creds = None
        if password:
            password_creds = [PasswordCredential(start_date=start_date, end_date=end_date, key_id=str(self.gen_guid()),
                                                 value=password, custom_key_identifier=custom_key_id)]
        elif key_value:
            key_creds = [
                KeyCredential(start_date=start_date, end_date=end_date, key_id=str(self.gen_guid()), value=key_value,
                              usage=key_usage, type=key_type, custom_key_identifier=custom_key_id)]

        return (password_creds, key_creds)

    def encode_custom_key_description(self, key_description):
        # utf16 is used by AAD portal. Do not change it to other random encoding
        # unless you know what you are doing.
        return key_description.encode('utf-16')

    def gen_guid(self):
        return uuid.uuid4()

    def build_application_accesses(self, required_resource_accesses):
        if not required_resource_accesses:
            return None
        required_accesses = []
        if isinstance(required_resource_accesses, dict):
            self.log('Getting "requiredResourceAccess" from a full manifest')
            required_resource_accesses = required_resource_accesses.get('required_resource_access', [])
        for x in required_resource_accesses:

            accesses = [ResourceAccess(id=y['id'], type=y['type']) for y in x['resource_access']]
            required_accesses.append(RequiredResourceAccess(resource_app_id=x['resource_app_id'],
                                                            resource_access=accesses))
        return required_accesses

    def build_app_roles(self, app_roles):
        if not app_roles:
            return None
        result = []
        if isinstance(app_roles, dict):
            self.log('Getting "appRoles" from a full manifest')
            app_roles = app_roles.get('appRoles', [])
        for x in app_roles:
            role = AppRole(id=x.get('id', None) or self.gen_guid(),
                           allowed_member_types=x.get('allowed_member_types', None),
                           description=x.get('description', None), display_name=x.get('display_name', None),
                           is_enabled=x.get('is_enabled', None), value=x.get('value', None))
            result.append(role)
        return result


def main():
    AzureRMADApplication()


if __name__ == '__main__':
    main()
