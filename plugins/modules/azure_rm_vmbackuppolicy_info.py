#!/usr/bin/python
#
# Copyright (c) 2020 Suyeb Ansari (@suyeb786)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_vmbackuppolicy_info
version_added: '1.1.0'
short_description: Fetch Backup Policy Details
description:
    - Get Backup Policy Details.
options:
    name:
        description:
            - Policy Name.
        required: true
        type: str
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    vault_name:
        description:
            - Recovery Service Vault Name.
        required: true
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Suyeb Ansari (@suyeb786)
'''

EXAMPLES = '''
   azure_rm_backvmuppolicy_info:
     name: 'myBackupPolicy'
     vault_name: 'myVault'
     resource_group: 'myResourceGroup'
'''

RETURN = '''
response:
    description:
        - The response about the current state of the backup policy.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample:  "/subscriptions/xxxxxxx/resourceGroups/resourcegroup_name/ \
            providers/Microsoft.RecoveryServices/vaults/myVault/backupPolicies/myBackup"
        name:
            description:
                - Backup Policy Name.
            returned: always
            type: str
            sample:  "myBackup"
        properties:
            description:
                - The backup policy properties.
            returned: always
            type: dict
            sample: {
                    "backupManagementType": "AzureIaasVM",
                    "schedulePolicy": {
                      "schedulePolicyType": "SimpleSchedulePolicy",
                      "scheduleRunFrequency": "Weekly",
                      "scheduleRunDays": [
                        "Monday",
                        "Wednesday",
                        "Thursday"
                      ],
                      "scheduleRunTimes": [
                        "2018-01-24T10:00:00Z"
                      ],
                      "scheduleWeeklyFrequency": 0
                    },
                    "retentionPolicy": {
                      "retentionPolicyType": "LongTermRetentionPolicy",
                      "weeklySchedule": {
                        "daysOfTheWeek": [
                          "Monday",
                          "Wednesday",
                          "Thursday"
                        ],
                        "retentionTimes": [
                          "2018-01-24T10:00:00Z"
                        ],
                        "retentionDuration": {
                          "count": 1,
                          "durationType": "Weeks"
                        }
                      },
                      "monthlySchedule": {
                        "retentionScheduleFormatType": "Weekly",
                        "retentionScheduleWeekly": {
                          "daysOfTheWeek": [
                            "Wednesday",
                            "Thursday"
                          ],
                          "weeksOfTheMonth": [
                            "First",
                            "Third"
                          ]
                        },
                        "retentionTimes": [
                          "2018-01-24T10:00:00Z"
                        ],
                        "retentionDuration": {
                          "count": 2,
                          "durationType": "Months"
                        }
                      },
                      "yearlySchedule": {
                        "retentionScheduleFormatType": "Weekly",
                        "monthsOfYear": [
                          "February",
                          "November"
                        ],
                        "retentionScheduleWeekly": {
                          "daysOfTheWeek": [
                            "Monday",
                            "Thursday"
                          ],
                          "weeksOfTheMonth": [
                            "Fourth"
                          ]
                        },
                        "retentionTimes": [
                          "2018-01-24T10:00:00Z"
                        ],
                        "retentionDuration": {
                          "count": 4,
                          "durationType": "Years"
                        }
                      }
                    },
                    "timeZone": "Pacific Standard Time",
                    "protectedItemsCount": 0
                   }
        type:
            description:
                - Resource type.
            returned: always
            type: str
            sample:  "Microsoft.RecoveryServices/vaults/backupPolicies"
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
import json


class BackupPolicyVMInfo(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            vault_name=dict(
                type='str',
                required=True
            )
        )

        self.resource_group = None
        self.name = None
        self.vault_name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.url = None
        self.status_code = [200, 202]

        self.query_parameters = {}
        self.query_parameters['api-version'] = '2019-05-13'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(BackupPolicyVMInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True
                                                 )

    def get_url(self):
        return '/subscriptions/' \
               + self.subscription_id \
               + '/resourceGroups/' \
               + self.resource_group \
               + '/providers/Microsoft.RecoveryServices' \
               + '/vaults' + '/' \
               + self.vault_name + '/' \
               + "backupPolicies/" \
               + self.name

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        self.url = self.get_url()

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        response = self.get_resource()
        changed = False
        self.results['response'] = response
        self.results['changed'] = changed

        return self.results

    def get_resource(self):
        # self.log('Fetch Backup Policy Details {0}'.format(self.))
        try:
            response = self.mgmt_client.query(
                self.url,
                'GET',
                self.query_parameters,
                self.header_parameters,
                None,
                self.status_code,
                600,
                30,
            )
            found = True
        except Exception as e:
            self.log('Backup policy does not exist.')
            self.fail('Error in fetching VM Backup Policy {0}'.format(str(e)))
        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}

        return response


def main():
    BackupPolicyVMInfo()


if __name__ == '__main__':
    main()
