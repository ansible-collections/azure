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
    app_id:
        description:
            - Application ID.
        type: str

    display_name:
        description:
            - The display name of the application.
        required: true
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

    sign_in_audience:
        description:
            - The application can be used from any Azure AD tenants.
            - Microsoft Graph SDK deprecate I(available_to_other_tenants), replace by I(sign_in_audience).
            - Refer to link U(https://learn.microsoft.com/en-us/graph/migrate-azure-ad-graph-property-differences#application-property-differences)
        type: str
        choices:
            - AzureADMyOrg
            - AzureADMultipleOrgs
            - AzureADandPersonalMicrosoftAccount
            - PersonalMicrosoftAccount

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

    notes:
        description:
            - Notes relevant for the management of the application.
        type: str

    oauth2_allow_implicit_flow:
        description:
            - Whether to allow implicit grant flow for OAuth2.
        type: bool

    optional_claims:
        description:
            - Declare the optional claims for the application.
        type: dict
        suboptions:
            access_token_claims :
                description:
                    - The optional claims returned in the JWT access token
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
                            - If the value is true, the claim specified by the client is necessary to ensure a smooth authorization experience\
                               for the specific task requested by the end user.
                            - The default value is false.
                        default: false
                        type: bool
                    additional_properties:
                        description:
                            - Additional properties of the claim.
                            - If a property exists in this collection, it modifies the behavior of the optional claim specified in the name property.
                        type: list
                        elements: str
            id_token_claims:
                description:
                    - The optional claims returned in the JWT ID token
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
                            - If the value is true, the claim specified by the client is necessary to ensure a smooth authorization experience\
                               for the specific task requested by the end user.
                            - The default value is false.
                        default: false
                        type: bool
                    additional_properties:
                        description:
                            - Additional properties of the claim.
                            - If a property exists in this collection, it modifies the behavior of the optional claim specified in the name property.
                        type: list
                        elements: str
            saml2_token_claims:
                description:
                    - The optional claims returned in the SAML token
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
                            - If the source value is user, the value in the name property is the extension property rom the user object.
                        type: str
                    essential:
                        description:
                            - If the value is true, the claim specified by the client is necessary to ensure a smooth authorization experience\
                               for the specific task requested by the end user.
                            - The default value is false.
                        default: false
                        type: bool
                    additional_properties:
                        description:
                            - Additional properties of the claim.
                            - If a property exists in this collection, it modifies the behavior of the optional claim specified in the name property.
                        type: list
                        elements: str
    password:
        description:
            - App password, aka 'client secret'.
        type: str

    web_reply_urls:
        description:
            - The web redirect urls.
            - Space-separated URIs to which Azure AD will redirect in response to an OAuth 2.0 request.
            - The value does not need to be a physical endpoint, but must be a valid URI.
        type: list
        elements: str
        aliases:
            - reply_urls

    spa_reply_urls:
        description:
            - The spa redirect urls.
            - Space-separated URIs to which Azure AD will redirect in response to an OAuth 2.0 request.
            - The value does not need to be a physical endpoint, but must be a valid URI.
        type: list
        elements: str

    public_client_reply_urls:
        description:
            - The public client redirect urls.
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
    display_name: "{{ display_name }}"

- name: Create ad application with multi redirect urls
  azure_rm_adapplication:
    display_name: "{{ display_name }}"
    web_reply_urls:
      - https://web01.com
    spa_reply_urls:
      - https://spa01.com
      - https://spa02.com
    public_client_reply_urls:
      - https://public01.com
      - https://public02.com

- name: Create application with more parameter
  azure_rm_adapplication:
    display_name: "{{ display_name }}"
    sign_in_audience: AzureADandPersonalMicrosoftAccount
    credential_description: "for test"
    end_date: 2021-10-01
    start_date: 2021-05-18
    identifier_uris: fredtest02.com

- name: delete ad application
  azure_rm_adapplication:
    app_id: "{{ app_id }}"
    state: absent
'''

RETURN = '''
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
sign_in_audience:
    description:
        - The application can be used from any Azure AD tenants.
    returned: always
    type: str
    sample: AzureADandPersonalMicrosoftAccount
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
public_client_reply_urls:
    description:
        - The public client redirect urls.
        - Space-separated URIs to which Azure AD will redirect in response to an OAuth 2.0 request.
    returned: always
    type: list
    sample: []
web_reply_urls:
    description:
        - The web redirect urls.
        - Space-separated URIs to which Azure AD will redirect in response to an OAuth 2.0 request.
    returned: always
    type: list
    sample: []
spa_reply_urls:
    description:
        - The spa redirect urls.
        - Space-separated URIs to which Azure AD will redirect in response to an OAuth 2.0 request.
    returned: always
    type: list
    sample: []
optional_claims:
    description:
        - Declare the optional claims for the application.
    type: complex
    returned: always
    contains:
        access_token_claims :
            description:
                - The optional claims returned in the JWT access token
            type: list
            returned: always
            sample: ['name': 'aud', 'source': null, 'essential': false, 'additional_properties': []]
        id_token_claims:
            description:
                - The optional claims returned in the JWT ID token
            type: list
            returned: always
            sample: ['name': 'acct', 'source': null, 'essential': false, 'additional_properties': []]
        saml2_token_claims:
            description:
                - The optional claims returned in the SAML token
            type: list
            returned: always
            sample: ['name': 'acct', 'source': null, 'essential': false, 'additional_properties': []]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    import datetime
    import dateutil.parser
    import uuid
    import asyncio
    from dateutil.relativedelta import relativedelta
    from msgraph.generated.applications.applications_request_builder import ApplicationsRequestBuilder
    from msgraph.generated.models.application import Application
    from msgraph.generated.models.password_credential import PasswordCredential
    from msgraph.generated.models.key_credential import KeyCredential
    from msgraph.generated.models.required_resource_access import RequiredResourceAccess
    from msgraph.generated.models.resource_access import ResourceAccess
    from msgraph.generated.models.app_role import AppRole
    from msgraph.generated.models.web_application import WebApplication
    from msgraph.generated.models.spa_application import SpaApplication
    from msgraph.generated.models.public_client_application import PublicClientApplication
    from msgraph.generated.models.implicit_grant_settings import ImplicitGrantSettings
    from msgraph.generated.models.optional_claim import OptionalClaim
    from msgraph.generated.models.optional_claims import OptionalClaims
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

claims_spec = dict(
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
        type='list',
        elements='str'
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
            app_id=dict(type='str'),
            display_name=dict(type='str', required=True),
            app_roles=dict(type='list', elements='dict', options=app_role_spec),
            sign_in_audience=dict(
                type='str',
                choices=['AzureADMyOrg', 'AzureADMultipleOrgs', 'AzureADandPersonalMicrosoftAccount', 'PersonalMicrosoftAccount']
            ),
            credential_description=dict(type='str'),
            end_date=dict(type='str'),
            homepage=dict(type='str'),
            allow_guests_sign_in=dict(type='bool'),
            identifier_uris=dict(type='list', elements='str'),
            key_type=dict(type='str', default='AsymmetricX509Cert',
                          choices=['AsymmetricX509Cert', 'Password', 'Symmetric']),
            key_usage=dict(type='str', default='Verify', choices=['Sign', 'Verify']),
            key_value=dict(type='str', no_log=True),
            native_app=dict(type='bool'),
            notes=dict(type='str'),
            oauth2_allow_implicit_flow=dict(type='bool'),
            optional_claims=dict(
                type='dict',
                options=dict(
                    access_token_claims=dict(type='list', elements='dict', no_log=True, options=claims_spec),
                    id_token_claims=dict(type='list', elements='dict', no_log=True, options=claims_spec),
                    saml2_token_claims=dict(type='list', elements='dict', no_log=True, options=claims_spec),
                )
            ),
            password=dict(type='str', no_log=True),
            public_client_reply_urls=dict(type='list', elements='str'),
            web_reply_urls=dict(type='list', elements='str', aliases=['reply_urls']),
            spa_reply_urls=dict(type='list', elements='str'),
            start_date=dict(type='str'),
            required_resource_accesses=dict(type='list', elements='dict', options=required_resource_accesses_spec),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )

        self.state = None
        self.app_id = None
        self.display_name = None
        self.app_roles = None
        self.credential_description = None
        self.end_date = None
        self.homepage = None
        self.identifier_uris = None
        self.key_type = None
        self.key_usage = None
        self.key_value = None
        self.native_app = None
        self.notes = None
        self.oauth2_allow_implicit_flow = None
        self.optional_claims = None
        self.password = None
        self.public_client_reply_urls = None
        self.spa_reply_urls = None
        self.web_reply_urls = None
        self.start_date = None
        self.required_resource_accesses = None
        self.allow_guests_sign_in = None
        self.results = dict(changed=False)
        self._client = None
        self.sign_in_audience = None

        super(AzureRMADApplication, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=False,
                                                   supports_tags=False,
                                                   is_ad_resource=True)

    def exec_module(self, **kwargs):
        self._client = self.get_msgraph_client()
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
                    self.fail("'identifier_uris' is not required for creating a native application")
            else:
                password_creds, key_creds = self.build_application_creds(self.password, self.key_value, self.key_type,
                                                                         self.key_usage,
                                                                         self.start_date, self.end_date,
                                                                         self.credential_description)
            if self.required_resource_accesses:
                required_accesses = self.build_application_accesses(self.required_resource_accesses)

            if self.app_roles:
                app_roles = self.build_app_roles(self.app_roles)

            if self.optional_claims:
                optional_claims = self.build_optional_claims(self.optional_claims)

            create_app = Application(
                sign_in_audience=self.sign_in_audience,
                web=WebApplication(
                    home_page_url=self.homepage,
                    redirect_uris=self.web_reply_urls,
                    implicit_grant_settings=ImplicitGrantSettings(
                        enable_access_token_issuance=self.oauth2_allow_implicit_flow,
                    ),
                ),
                spa=SpaApplication(redirect_uris=self.spa_reply_urls),
                public_client=PublicClientApplication(redirect_uris=self.public_client_reply_urls),
                display_name=self.display_name,
                identifier_uris=self.identifier_uris,
                key_credentials=key_creds,
                notes=self.notes,
                password_credentials=password_creds,
                required_resource_access=required_accesses,
                app_roles=app_roles,
                optional_claims=optional_claims
                # allow_guests_sign_in=self.allow_guests_sign_in,
            )
            response = asyncio.get_event_loop().run_until_complete(self.create_application(create_app))
            self.results['changed'] = True
            self.results.update(self.to_dict(response))
            return response
        except Exception as ge:
            self.fail("Error creating application, display_name: {0} - {1}".format(self.display_name, str(ge)))

    def update_resource(self, old_response):
        try:
            key_creds, password_creds, required_accesses, app_roles, optional_claims = None, None, None, None, None
            if self.native_app:
                if self.identifier_uris:
                    self.fail("'identifier_uris' is not required for creating a native application")
            else:
                password_creds, key_creds = self.build_application_creds(self.password, self.key_value, self.key_type,
                                                                         self.key_usage,
                                                                         self.start_date, self.end_date,
                                                                         self.credential_description)
            if self.required_resource_accesses:
                required_accesses = self.build_application_accesses(self.required_resource_accesses)

            if self.app_roles:
                app_roles = self.build_app_roles(self.app_roles)

            if self.optional_claims:
                optional_claims = self.build_optional_claims(self.optional_claims)

            app_update_param = Application(
                sign_in_audience=self.sign_in_audience,
                web=WebApplication(
                    home_page_url=self.homepage,
                    redirect_uris=self.web_reply_urls,
                    implicit_grant_settings=ImplicitGrantSettings(
                        enable_access_token_issuance=self.oauth2_allow_implicit_flow,
                    ),
                ),
                spa=SpaApplication(redirect_uris=self.spa_reply_urls),
                public_client=PublicClientApplication(redirect_uris=self.public_client_reply_urls),
                display_name=self.display_name,
                identifier_uris=self.identifier_uris,
                key_credentials=key_creds,
                notes=self.notes,
                password_credentials=password_creds,
                required_resource_access=required_accesses,
                # allow_guests_sign_in=self.allow_guests_sign_in,
                app_roles=app_roles,
                optional_claims=optional_claims)
            asyncio.get_event_loop().run_until_complete(self.update_application(
                obj_id=old_response['object_id'], update_app=app_update_param))

            self.results['changed'] = True
            self.results.update(self.get_resource())

        except Exception as ge:
            self.fail("Error updating the application app_id {0} - {1}".format(self.app_id, str(ge)))

    def delete_resource(self, response):
        try:
            asyncio.get_event_loop().run_until_complete(self.delete_application(response.get('object_id')))
            self.results['changed'] = True
            return True
        except Exception as ge:
            self.fail(
                "Error deleting application app_id {0} display_name {1} - {2}".format(self.app_id, self.display_name,
                                                                                      str(ge)))

    def get_resource(self):
        try:
            existing_apps = []
            if self.app_id:
                ret = asyncio.get_event_loop().run_until_complete(self.get_application_by_app_id(self.app_id))
                existing_apps = ret.value

            if not existing_apps:
                return False
            result = existing_apps[0]
            return self.to_dict(result)
        except Exception as ge:
            self.fail(ge)
            # self.log("Did not find the graph instance instance {0} - {1}".format(self.app_id, str(ge)))
            # return False

    def check_update(self, response):
        for key in list(self.module_arg_spec.keys()):
            attr = getattr(self, key)
            if attr and key in response:
                if (response and attr != response[key]) or response[key] is None:
                    return True
        return False

    def serialize_claims(self, claims):
        if claims is None:
            return None
        return [{
            "additional_properties": claim.additional_properties,
            "essential": claim.essential,
            "name": claim.name,
            "source": claim.source} for claim in claims]

    def to_dict(self, object):
        app_roles = [{
            'id': app_role.id,
            'display_name': app_role.display_name,
            'is_enabled': app_role.is_enabled,
            'value': app_role.value,
            "description": app_role.description
        } for app_role in object.app_roles]
        optional_claims = {
            "access_token": self.serialize_claims(object.optional_claims.access_token),
            "id_token": self.serialize_claims(object.optional_claims.id_token),
            "saml2_token": self.serialize_claims(object.optional_claims.saml2_token)
        } if object.optional_claims is not None else object.optional_claims
        return dict(
            app_id=object.app_id,
            object_id=object.id,
            display_name=object.display_name,
            app_roles=app_roles,
            sign_in_audience=object.sign_in_audience,
            homepage=object.web.home_page_url,
            identifier_uris=object.identifier_uris,
            notes=object.notes,
            oauth2_allow_implicit_flow=object.web.implicit_grant_settings.enable_access_token_issuance,
            optional_claims=optional_claims,
            # allow_guests_sign_in=object.allow_guests_sign_in,
            web_reply_urls=object.web.redirect_uris,
            spa_reply_urls=object.spa.redirect_uris,
            public_client_reply_urls=object.public_client.redirect_uris
        )

    def build_application_creds(self, password=None, key_value=None, key_type=None, key_usage=None,
                                start_date=None, end_date=None, key_description=None):
        if password and key_value:
            self.fail('specify either password or key_value, but not both.')

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
            password_creds = [PasswordCredential(start_date_time=start_date, end_date_time=end_date,
                                                 key_id=self.gen_guid(), secret_text=password,
                                                 custom_key_identifier=custom_key_id)]  # value ? secret_text
        elif key_value:
            key_creds = [
                KeyCredential(start_date_time=start_date, end_date_time=end_date, key_id=self.gen_guid(), key=key_value,
                              # value ? key
                              usage=key_usage, type=key_type, custom_key_identifier=custom_key_id)]

        return password_creds, key_creds

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
                           is_enabled=x.get('is_enabled', None), value=x.get('value', None))  # value ? additional_data
            result.append(role)
        return result

    def build_optional_claims(self, optional_claims):

        def build_claims(claims_dict):
            if claims_dict is None:
                return None
            return [OptionalClaim(
                essential=claim.get("essential"),
                name=claim.get("name"),
                source=claim.get("source"),
                additional_properties=claim.get("additional_properties")
            ) for claim in claims_dict]

        claims = OptionalClaims(
            access_token=build_claims(optional_claims.get("access_token_claims")),
            id_token=build_claims(optional_claims.get("id_token_claims")),
            saml2_token=build_claims(optional_claims.get("saml2_token_claims"))
        )
        return claims

    async def create_application(self, creat_app):
        return await self._client.applications.post(body=creat_app)

    async def update_application(self, obj_id, update_app):
        return await self._client.applications.by_application_id(obj_id).patch(body=update_app)

    async def get_application_by_app_id(self, app_id):
        request_configuration = ApplicationsRequestBuilder.ApplicationsRequestBuilderGetRequestConfiguration(
            query_parameters=ApplicationsRequestBuilder.ApplicationsRequestBuilderGetQueryParameters(
                filter=(" appId eq '{0}'".format(app_id)), ),
        )

        return await self._client.applications.get(request_configuration=request_configuration)

    async def delete_application(self, obj_id):
        await self._client.applications.by_application_id(obj_id).delete()

    async def get_applications(self, filters):
        request_configuration = ApplicationsRequestBuilder.ApplicationsRequestBuilderGetRequestConfiguration(
            query_parameters=ApplicationsRequestBuilder.ApplicationsRequestBuilderGetQueryParameters(
                filter=(' and '.join(filters))
            ))
        return await self._client.applications.get(request_configuration=request_configuration)


def main():
    AzureRMADApplication()


if __name__ == '__main__':
    main()
