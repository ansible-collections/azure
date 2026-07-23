#!/usr/bin/python
#
# Copyright (c) 2026 Bill Peck (@p3ck)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_powerplatform_customerinsights
version_added: "3.21.0"
short_description: Manage Dynamics 365 Customer Insights instances
description:
    - Create, update, or delete Dynamics 365 Customer Insights instances.
    - Uses the Customer Insights REST API (not Azure Resource Manager).
    - Authenticates via Entra ID service principal with the
      C(Dynamics 365 AI for Customer Insights) API permission.
    - The service principal must have admin consent granted for the API permission.
options:
    name:
        description:
            - Display name of the Customer Insights instance.
            - Used to identify the instance for idempotency when I(instance_id) is not provided.
        type: str
        required: true
    instance_id:
        description:
            - UUID of an existing Customer Insights instance.
            - If omitted, the module discovers the instance by I(name).
            - Required for update operations where multiple instances share the same name.
        type: str
    region:
        description:
            - Customer Insights region for the instance.
            - Required when I(state=present).
            - "Valid values include: C(unitedstates), C(europe), C(asiapacific),
              C(australia), C(unitedkingdom), C(india), C(japan), C(canada),
              C(southamerica), C(france), C(switzerlandnorth), C(germany),
              C(unitedarabemirates), C(southafrica)."
        type: str
    instance_type:
        description:
            - Type of Customer Insights instance to create.
        type: str
        choices:
            - trial
            - sandbox
            - production
        default: trial
    bap_provisioning_type:
        description:
            - Controls how the Power Platform environment is handled during instance creation.
            - C(create) provisions a new Power Platform environment automatically.
            - C(skip) skips Power Platform environment provisioning.
            - C(attach) attaches to an existing Power Platform environment.
        type: str
        choices:
            - create
            - skip
            - attach
        default: create
    state:
        description:
            - State of the Customer Insights instance.
            - Use C(present) to create or update an instance.
            - Use C(absent) to delete an instance.
        type: str
        choices:
            - present
            - absent
        default: present
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create a trial Customer Insights instance
  azure.azcollection.azure_powerplatform_customerinsights:
    name: my-ci-instance
    region: unitedstates
    instance_type: trial
    bap_provisioning_type: create
    state: present

- name: Create a production Customer Insights instance
  azure.azcollection.azure_powerplatform_customerinsights:
    name: prod-ci-instance
    region: europe
    instance_type: production
    state: present

- name: Delete a Customer Insights instance by name
  azure.azcollection.azure_powerplatform_customerinsights:
    name: my-ci-instance
    state: absent

- name: Delete a Customer Insights instance by ID
  azure.azcollection.azure_powerplatform_customerinsights:
    name: my-ci-instance
    instance_id: "12345678-1234-1234-1234-123456789012"
    state: absent
'''

RETURN = '''
instance:
    description:
        - Customer Insights instance details.
    returned: when state is present and not check mode
    type: dict
    contains:
        instance_id:
            description: UUID of the instance.
            type: str
            returned: always
            sample: "12345678-1234-1234-1234-123456789012"
        name:
            description: Display name of the instance.
            type: str
            returned: always
            sample: "my-ci-instance"
        region:
            description: Customer Insights region.
            type: str
            returned: always
            sample: "unitedstates"
        instance_type:
            description: Instance type.
            type: str
            returned: always
            sample: "trial"
        provisioning_state:
            description: Current provisioning state of the instance.
            type: str
            returned: always
            sample: "active"
        azure_region:
            description: Azure region where the scale unit resides.
            type: str
            returned: when available
            sample: "westus"
        created_utc:
            description: UTC timestamp when the instance was created.
            type: str
            returned: when available
            sample: "2026-01-15T10:30:00Z"
        updated_utc:
            description: UTC timestamp when the instance was last updated.
            type: str
            returned: when available
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


class AzureRMPowerPlatformCustomerInsights(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            instance_id=dict(type='str'),
            region=dict(type='str'),
            instance_type=dict(
                type='str',
                choices=['trial', 'sandbox', 'production'],
                default='trial',
            ),
            bap_provisioning_type=dict(
                type='str',
                choices=['create', 'skip', 'attach'],
                default='create',
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                default='present',
            ),
        )

        self.name = None
        self.instance_id = None
        self.region = None
        self.instance_type = None
        self.bap_provisioning_type = None
        self.state = None

        self.results = dict(changed=False)

        super(AzureRMPowerPlatformCustomerInsights, self).__init__(
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

        if self.state == 'present' and not self.region:
            self.fail("Parameter 'region' is required when state is 'present'.")

        existing = self._get_instance()

        if self.state == 'present':
            if existing is None:
                if not self.check_mode:
                    instance = self._create_instance()
                    self.results['instance'] = instance
                self.results['changed'] = True
            else:
                update_needed = self._check_update_needed(existing)
                if update_needed:
                    if not self.check_mode:
                        instance = self._update_instance(existing['instance_id'])
                        self.results['instance'] = instance
                    self.results['changed'] = True
                else:
                    self.results['instance'] = existing
        else:
            if existing is not None:
                if not self.check_mode:
                    self._delete_instance(existing['instance_id'])
                self.results['changed'] = True

        return self.results

    def _get_auth_headers(self):
        cred = self.azure_auth.azure_credential_track2
        token = cred.get_token(CI_TOKEN_SCOPE)
        return {
            'Authorization': 'Bearer {0}'.format(token.token),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def _get_instance(self):
        if self.instance_id:
            return self._get_instance_by_id(self.instance_id)
        return self._find_instance_by_name(self.name)

    def _get_instance_by_id(self, instance_id):
        url = '{0}/instances/{1}'.format(CI_API_BASE, instance_id)
        headers = self._get_auth_headers()
        response = requests.get(url, headers=headers, timeout=60)
        if response.status_code == 404:
            return None
        if response.status_code == 401 or response.status_code == 403:
            self.fail(
                "Authentication failed (HTTP {0}). Ensure your service principal has "
                "'Dynamics 365 AI for Customer Insights' API permission with admin consent. "
                "Response: {1}".format(response.status_code, response.text)
            )
        if response.status_code != 200:
            self.fail("Failed to get instance {0}: HTTP {1} - {2}".format(
                instance_id, response.status_code, response.text))
        return self._parse_instance(response.json())

    def _find_instance_by_name(self, name):
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
        instances = response.json()
        if not isinstance(instances, list):
            return None
        for inst in instances:
            inst_name = inst.get('name') or inst.get('friendlyName', '')
            if inst_name.lower() == name.lower():
                return self._parse_instance(inst)
        return None

    def _check_update_needed(self, existing):
        if self.region and existing.get('region') and \
                self.region.lower() != existing['region'].lower():
            return True
        if self.instance_type and existing.get('instance_type') and \
                self.instance_type.lower() != existing['instance_type'].lower():
            return True
        return False

    def _create_instance(self):
        url = '{0}/instances/V2'.format(CI_API_BASE)
        headers = self._get_auth_headers()
        body = {
            'instanceMetadata': {
                'name': self.name,
                'region': self.region,
                'instanceType': self.instance_type,
            },
            'bapProvisioningType': self.bap_provisioning_type,
        }
        response = requests.post(url, headers=headers, json=body, timeout=300)
        if response.status_code == 401 or response.status_code == 403:
            self.fail(
                "Authentication failed (HTTP {0}). Ensure your service principal has "
                "'Dynamics 365 AI for Customer Insights' API permission with admin consent. "
                "Response: {1}".format(response.status_code, response.text)
            )
        if response.status_code == 409:
            self.fail("Instance creation conflict: {0}".format(response.text))
        if response.status_code not in (200, 201, 202):
            self.fail("Failed to create instance: HTTP {0} - {1}".format(
                response.status_code, response.text))
        return self._parse_instance(response.json())

    def _update_instance(self, instance_id):
        url = '{0}/instances/{1}/V2'.format(CI_API_BASE, instance_id)
        headers = self._get_auth_headers()
        body = {
            'instanceMetadata': {
                'name': self.name,
                'region': self.region,
                'instanceType': self.instance_type,
            },
        }
        response = requests.patch(url, headers=headers, json=body, timeout=300)
        if response.status_code == 401 or response.status_code == 403:
            self.fail(
                "Authentication failed (HTTP {0}). Response: {1}".format(
                    response.status_code, response.text)
            )
        if response.status_code not in (200, 201, 202):
            self.fail("Failed to update instance {0}: HTTP {1} - {2}".format(
                instance_id, response.status_code, response.text))
        return self._parse_instance(response.json())

    def _delete_instance(self, instance_id):
        url = '{0}/instances/{1}'.format(CI_API_BASE, instance_id)
        headers = self._get_auth_headers()
        response = requests.delete(url, headers=headers, timeout=300)
        if response.status_code == 404:
            return
        if response.status_code == 401 or response.status_code == 403:
            self.fail(
                "Authentication failed (HTTP {0}). Response: {1}".format(
                    response.status_code, response.text)
            )
        if response.status_code not in (200, 202, 204):
            self.fail("Failed to delete instance {0}: HTTP {1} - {2}".format(
                instance_id, response.status_code, response.text))

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
    AzureRMPowerPlatformCustomerInsights()


if __name__ == '__main__':
    main()
