#!/usr/bin/python
#
# Copyright (c) 2020 Suyeb Ansari (@suyeb786)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_vmbackuppolicy
version_added: '1.1.0'
short_description: Create or Delete Azure VM Backup Policy
description:
    - Create or Delete Azure VM Backup Policy.
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
    time:
        description:
            - Retention times of retention policy in UTC.
        required: false
        default: '12:00'
        type: str
    weekdays:
        description:
            - List of days of the week.
        required: false
        default: ['Monday']
        type: list
        elements: str
    weeks:
        description:
            - List of weeks of month.
        required: false
        default: ['First']
        type: list
        elements: str
    months:
        description:
            - List of months of year of yearly retention policy.
        required: false
        default: ['January']
        type: list
        elements: str
    count:
        description:
            - Count of duration types. Retention duration is obtained by the counting the duration type Count times.
        required: false
        default: 1
        type: int
    state:
        description:
            - Assert the state of the protection item.
            - Use C(present) for Creating Backup Policy.
            - Use C(absent) for Deleting Backup Policy.
        default: present
        type: str
        choices:
            - present
            - absent
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Suyeb Ansari (@suyeb786)
'''

EXAMPLES = '''
- name: Create VM Backup Policy
  azure_rm_backvmuppolicy:
     name: 'myBackupPolicy'
     vault_name: 'myVault'
     resource_group: 'myResourceGroup'
     time: '18:00'
     weekdays: ['Monday', 'Thursday', 'Friday']
     weeks: ['First', 'Fourth']
     months: ['February', 'November']
     count: 4
     state: present
- name: Delete VM Backup Policy
  azure_rm_backvmuppolicy:
     name: 'myBackupPolicy'
     vault_name: 'myVault'
     resource_group: 'myResourceGroup'
     state: absent
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
import time
import json


class VMBackupPolicy(AzureRMModuleBaseExt):
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
            ),
            time=dict(
                type='str',
                default='12:00'
            ),
            weekdays=dict(
                type='list',
                elements='str',
                default=['Monday']
            ),
            weeks=dict(
                type='list',
                elements='str',
                default=['First']
            ),
            months=dict(
                type='list',
                elements='str',
                default=['January']
            ),
            count=dict(
                type='int',
                default=1
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.time = None
        self.state = None
        self.vault_name = None
        self.count = None
        self.weekdays = None
        self.weeks = None
        self.months = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.url = None
        self.status_code = [200, 201, 202, 204]

        self.body = {}
        self.query_parameters = {}
        self.query_parameters['api-version'] = '2019-05-13'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(VMBackupPolicy, self).__init__(derived_arg_spec=self.module_arg_spec,
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

    def set_schedule_run_time(self):
        return time.strftime("%Y-%m-%d", time.gmtime()) + "T" + self.time + ":00Z"

    def get_body(self):
        self.log('backup attributes {0}'.format(self.body))
        self.time = self.set_schedule_run_time()
        schedule_policy = dict()
        schedule_policy['schedulePolicyType'] = 'SimpleSchedulePolicy'
        schedule_policy['scheduleRunFrequency'] = 'Weekly'
        schedule_policy['scheduleRunTimes'] = [self.time]
        schedule_policy['scheduleRunDays'] = self.weekdays

        weekly_schedule = dict()
        weekly_schedule['daysOfTheWeek'] = ['Monday']
        weekly_schedule['retentionTimes'] = [self.time]
        weekly_schedule['retentionDuration'] = dict()
        weekly_schedule['retentionDuration']['count'] = self.count
        weekly_schedule['retentionDuration']['durationType'] = 'Weeks'

        monthly_schedule = dict()
        monthly_schedule['retentionScheduleFormatType'] = 'Weekly'
        monthly_schedule['retentionScheduleWeekly'] = dict()
        monthly_schedule['retentionScheduleWeekly']['daysOfTheWeek'] = self.weekdays
        monthly_schedule['retentionScheduleWeekly']['weeksOfTheMonth'] = self.weeks
        monthly_schedule['retentionTimes'] = [self.time]
        monthly_schedule['retentionDuration'] = dict()
        monthly_schedule['retentionDuration']['count'] = self.count
        monthly_schedule['retentionDuration']['durationType'] = 'Months'

        yearly_schedule = dict()
        yearly_schedule['retentionScheduleFormatType'] = 'Weekly'
        yearly_schedule['monthsOfYear'] = self.months
        yearly_schedule['retentionScheduleWeekly'] = dict()
        yearly_schedule['retentionScheduleWeekly']['daysOfTheWeek'] = self.weekdays
        yearly_schedule['retentionScheduleWeekly']['weeksOfTheMonth'] = self.weeks
        yearly_schedule['retentionTimes'] = [self.time]
        yearly_schedule['retentionDuration'] = dict()
        yearly_schedule['retentionDuration']['count'] = self.count
        yearly_schedule['retentionDuration']['durationType'] = 'Years'

        body = dict()
        body['properties'] = dict()
        body['properties']['backupManagementType'] = 'AzureIaasVM'
        body['properties']['timeZone'] = 'Pacific Standard Time'
        body['properties']['schedulePolicy'] = schedule_policy
        body['properties']['retentionPolicy'] = dict()
        body['properties']['retentionPolicy']['retentionPolicyType'] = 'LongTermRetentionPolicy'
        body['properties']['retentionPolicy']['weeklySchedule'] = weekly_schedule
        body['properties']['retentionPolicy']['monthlySchedule'] = monthly_schedule
        body['properties']['retentionPolicy']['yearlySchedule'] = yearly_schedule
        return body

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_parameters(self.module_arg_spec, self.body, 0)

        self.url = self.get_url()
        self.body = self.get_body()
        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_resource()

        changed = False
        if self.state == 'present':
            if old_response is False:
                response = self.create_vm_backup_policy()
                changed = True
            else:
                response = old_response
        if self.state == 'absent':
            changed = True
            response = self.delete_vm_backup_policy()
        self.results['response'] = response
        self.results['changed'] = changed

        return self.results

    def create_vm_backup_policy(self):
        # self.log('Creating VM Backup Policy {0}'.format(self.))
        try:
            response = self.mgmt_client.query(
                self.url,
                'PUT',
                self.query_parameters,
                self.header_parameters,
                self.body,
                self.status_code,
                600,
                30,
            )
        except Exception as e:
            self.log('Error in creating Backup Policy.')
            self.fail('Error in creating Backup Policy {0}'.format(str(e)))

        if hasattr(response, 'body'):
            response = json.loads(response.body())
        elif hasattr(response, 'context'):
            response = response.context['deserialized_data']
        else:
            self.fail("Create or Updating fail, no match message return, return info as {0}".format(response))

        return response

    def delete_vm_backup_policy(self):
        # self.log('Deleting Backup Policy {0}'.format(self.))
        try:
            response = self.mgmt_client.query(
                self.url,
                'DELETE',
                self.query_parameters,
                self.header_parameters,
                None,
                self.status_code,
                600,
                30,
            )
        except Exception as e:
            self.log('Error attempting to delete Azure Backup policy.')
            self.fail('Error attempting to delete Azure Backup policy: {0}'.format(str(e)))

    def get_resource(self):
        # self.log('Fetch Backup Policy Details {0}'.format(self.))
        found = False
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
        if found is True:
            response = json.loads(response.body())
            return response
        else:
            return False


def main():
    VMBackupPolicy()


if __name__ == '__main__':
    main()
