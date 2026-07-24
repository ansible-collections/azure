#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_powerplatform_customerinsights_info
version_added: "3.21.0"
short_description: Get Dynamics 365 Customer Insights instance facts
description:
    - Get facts for one or all Dynamics 365 Customer Insights instances.
    - Uses the Customer Insights REST API (not Azure Resource Manager).
    - Authenticates via Entra ID service principal with the
      C(Dynamics 365 AI for Customer Insights) API permission.
options:
    name:
        description:
            - Display name of a specific Customer Insights instance.
            - If specified, returns only the matching instance.
            - If omitted, returns all instances visible to the authenticated principal.
        type: str
    instance_id:
        description:
            - UUID of a specific Customer Insights instance.
            - Takes precedence over I(name) when both are provided.
        type: str
    subscription_key:
        description:
            - The API subscription key for the Customer Insights environment.
            - Found in Customer Insights under Settings > Permissions > APIs.
            - Required for all API calls; the Customer Insights API is fronted
              by Azure API Management and requires this key in addition to the
              Bearer token.
        type: str
        required: true
        no_log: true
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Get all Customer Insights instances
  azure.azcollection.azure_powerplatform_customerinsights_info:
    subscription_key: "{{ ci_subscription_key }}"
  register: ci_info

- name: Get a specific Customer Insights instance by name
  azure.azcollection.azure_powerplatform_customerinsights_info:
    name: my-ci-instance
    subscription_key: "{{ ci_subscription_key }}"
  register: ci_info

- name: Get a specific Customer Insights instance by ID
  azure.azcollection.azure_powerplatform_customerinsights_info:
    instance_id: "12345678-1234-1234-1234-123456789012"
    subscription_key: "{{ ci_subscription_key }}"
  register: ci_info
'''

RETURN = '''
instances:
    description:
        - List of Customer Insights instances.
    returned: always
    type: list
    elements: dict
    contains:
        instance_id:
            description: UUID of the instance.
            type: str
            sample: "12345678-1234-1234-1234-123456789012"
        name:
            description: Display name of the instance.
            type: str
            sample: "my-ci-instance"
        region:
            description: Customer Insights region.
            type: str
            sample: "unitedstates"
        instance_type:
            description: Instance type.
            type: str
            sample: "trial"
        provisioning_state:
            description: Current provisioning state.
            type: str
            sample: "active"
        azure_region:
            description: Azure region where the scale unit resides.
            type: str
            sample: "westus"
        created_utc:
            description: UTC timestamp when the instance was created.
            type: str
            sample: "2026-01-15T10:30:00Z"
        updated_utc:
            description: UTC timestamp when the instance was last updated.
            type: str
            sample: "2026-01-15T10:30:00Z"
'''  # NOQA

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


CI_API_BASE = 'https://api.ci.ai.dynamics.com/v1'
CI_TOKEN_SCOPE = 'https://api.ci.ai.dynamics.com/.default'


class AzureRMPowerPlatformCustomerInsightsInfo(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str'),
            instance_id=dict(type='str'),
            subscription_key=dict(type='str', required=True, no_log=True),
        )

        self.name = None
        self.instance_id = None
        self.subscription_key = None

        self.results = dict(changed=False, instances=[])

        super(AzureRMPowerPlatformCustomerInsightsInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            is_ad_resource=True,
        )

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if not HAS_REQUESTS:
            self.fail("The Python 'requests' library is required. pip install requests")

        if self.instance_id:
            self.results['instances'] = self._get_by_id(self.instance_id)
        elif self.name:
            self.results['instances'] = self._get_by_name(self.name)
        else:
            self.results['instances'] = self._list_all()

        return self.results

    def _get_auth_headers(self):
        cred = self.azure_auth.azure_credential_track2
        token = cred.get_token(CI_TOKEN_SCOPE)
        return {
            'Authorization': 'Bearer {0}'.format(token.token),
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Accept': 'application/json',
        }

    def _get_by_id(self, instance_id):
        url = '{0}/instances/{1}'.format(CI_API_BASE, instance_id)
        headers = self._get_auth_headers()
        response = requests.get(url, headers=headers, timeout=60)
        if response.status_code == 404:
            return []
        if response.status_code == 401 or response.status_code == 403:
            self.fail(
                "Authentication failed (HTTP {0}). Ensure your service principal has "
                "'Dynamics 365 AI for Customer Insights' API permission with admin consent. "
                "Response: {1}".format(response.status_code, response.text)
            )
        if response.status_code != 200:
            self.fail("Failed to get instance {0}: HTTP {1} - {2}".format(
                instance_id, response.status_code, response.text))
        return [self._parse_instance(response.json())]

    def _get_by_name(self, name):
        all_instances = self._list_all()
        return [i for i in all_instances if i['name'].lower() == name.lower()]

    def _list_all(self):
        url = '{0}/instances'.format(CI_API_BASE)
        headers = self._get_auth_headers()
        response = requests.get(url, headers=headers, timeout=60)
        if response.status_code == 401 or response.status_code == 403:
            self.fail(
                "Authentication failed (HTTP {0}). Ensure your service principal has "
                "'Dynamics 365 AI for Customer Insights' API permission with admin consent. "
                "Response: {1}".format(response.status_code, response.text)
            )
        if response.status_code != 200:
            self.fail("Failed to list instances: HTTP {0} - {1}".format(
                response.status_code, response.text))
        data = response.json()
        if not isinstance(data, list):
            return []
        return [self._parse_instance(inst) for inst in data]

    def _parse_instance(self, raw):
        return dict(
            instance_id=raw.get('instanceId', ''),
            name=raw.get('name', raw.get('friendlyName', '')),
            region=raw.get('region', ''),
            instance_type=raw.get('instanceType', ''),
            provisioning_state=raw.get('provisioningState', ''),
            azure_region=raw.get('azureRegion', ''),
            created_utc=str(raw.get('createdUtc', '')) if raw.get('createdUtc') else '',
            updated_utc=str(raw.get('updatedUtc', '')) if raw.get('updatedUtc') else '',
        )


def main():
    AzureRMPowerPlatformCustomerInsightsInfo()


if __name__ == '__main__':
    main()
