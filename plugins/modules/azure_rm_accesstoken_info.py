#!/usr/bin/python
#
# Copyright (c) 2023 Patrick Uiterwijk <@puiterwijk>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_accesstoken_info

version_added: "1.19.0"

short_description: Get Azure API access token

description:
    - Get an access token for Azure APIs.

options:
    scopes:
        description:
            - The scopes to request.
        type: list
        elements: str
        required: True
    claims:
        description:
            - Additional claims required in the token.
        type: list
        elements: str
    token_tenant_id:
        description:
            - Tenant to include in the token request.
        type: str
    enable_cae:
        description:
            - Whether to enable Continuous Access Evaluation (CAE) for the requested token.
        default: false
        type: bool

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Patrick Uiterwijk (@puiterwijk)
'''

EXAMPLES = '''
- name: Get access token for Microsoft Graph
  azure.azcollection.azure_rm_accesstoken_info:
    scopes:
      - https://graph.microsoft.com/.default
'''

RETURN = '''
access_token:
    description:
        - API access token.
    returned: success
    type: str
    sample: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiaWF0IjoxNTE2MjM5MDIyfQ.L8i6g3PfcHlioHCCPURC9pmXT7gdJpx3kOoyAfNUwCc
expires_on:
    description:
        - Timestamp the token expires on.
    returned: success
    type: int
    sample: 1699337824
'''


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMAccessToken(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            scopes=dict(type='list', elements='str', required=True),
            claims=dict(type='list', elements='str'),
            token_tenant_id=dict(type='str'),
            enable_cae=dict(type='bool', default=False),
        )

        self.scopes = None
        self.claims = None
        self.token_tenant_id = None
        self.enable_cae = False

        self.results = dict(changed=False)

        super(AzureRMAccessToken, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=False,
                                                 is_ad_resource=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        claims = None
        if self.claims is not None:
            claims = ' '.join(self.claims)

        cred = self.azure_auth.azure_credential_track2
        token = cred.get_token(
            *self.scopes,
            claims=claims,
            tenant_id=self.token_tenant_id,
            enable_cae=self.enable_cae,
        )

        self.results['access_token'] = token.token
        self.results['expires_on'] = token.expires_on
        return self.results


def main():
    AzureRMAccessToken()


if __name__ == '__main__':
    main()
