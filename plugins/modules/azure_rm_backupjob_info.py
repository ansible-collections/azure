#!/usr/bin/python
#
# Copyright (c) 2026 Zun Yang (@zunyangc)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_backupjob_info
version_added: '4.0.0'
short_description: Get Azure Backup job status
description:
    - Query the status of a single Azure Recovery Services Backup job by name,
      or list backup jobs on a Recovery Services vault.
    - Wraps the SDK operations C(RecoveryServicesBackupClient.job_details.get) and
      C(RecoveryServicesBackupClient.backup_jobs.list).
options:
    resource_group:
        description:
            - The name of the resource group containing the Recovery Services vault.
        required: true
        type: str
    recovery_vault_name:
        description:
            - The name of the Azure Recovery Services vault.
        required: true
        type: str
    name:
        description:
            - Job identifier (the job C(name) returned by the Azure Backup service).
            - When set, only that job's details are returned.
            - When not set, all backup jobs on the vault are listed.
        type: str
    filter:
        description:
            - OData filter applied when listing jobs. Ignored when I(name) is set.
            - "Example: C(status eq 'InProgress' and backupManagementType eq 'AzureIaasVM')."
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zun Yang (@zunyangc)
'''

EXAMPLES = '''
- name: Get status of a specific backup job
  azure_rm_backupjob_info:
    resource_group: my-rg
    recovery_vault_name: testVault
    name: 6c33c123-abcd-4567-89ef-000000000000

- name: List in-progress backup jobs on the vault
  azure_rm_backupjob_info:
    resource_group: my-rg
    recovery_vault_name: testVault
    filter: "status eq 'InProgress'"
'''

RETURN = '''
jobs:
    description:
        - List of backup job objects.
        - Contains a single element when I(name) is provided.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: Fully qualified resource ID of the backup job.
            returned: always
            type: str
        name:
            description: Job identifier.
            returned: always
            type: str
        type:
            description: Resource type (C(Microsoft.RecoveryServices/vaults/backupJobs)).
            returned: always
            type: str
        properties:
            description: Job properties including operation, status, start/end time, and source entity.
            returned: always
            type: dict
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # handled in azure_rm_common
    pass


class AzureRMBackupJobInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            recovery_vault_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            filter=dict(
                type='str'
            ),
        )

        self.resource_group = None
        self.recovery_vault_name = None
        self.name = None
        self.filter = None

        self.results = dict(changed=False, jobs=[])

        super(AzureRMBackupJobInfo, self).__init__(
            derived_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
            supports_tags=False,
            facts_module=True,
        )

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            job = self.get_job()
            self.results['jobs'] = [job.as_dict()] if job is not None else []
        else:
            self.results['jobs'] = [j.as_dict() for j in self.list_jobs()]

        return self.results

    def get_job(self):
        try:
            return self.recovery_services_backup_client.job_details.get(
                vault_name=self.recovery_vault_name,
                resource_group_name=self.resource_group,
                job_name=self.name,
            )
        except ResourceNotFoundError:
            self.log("Backup job {0} not found on vault {1}".format(self.name, self.recovery_vault_name))
            return None
        except Exception as exc:
            self.fail("Error fetching backup job {0}: {1}".format(self.name, str(exc)))

    def list_jobs(self):
        try:
            pager = self.recovery_services_backup_client.backup_jobs.list(
                vault_name=self.recovery_vault_name,
                resource_group_name=self.resource_group,
                filter=self.filter,
            )
            return list(pager)
        except Exception as exc:
            self.fail("Error listing backup jobs on vault {0}: {1}".format(self.recovery_vault_name, str(exc)))


def main():
    AzureRMBackupJobInfo()


if __name__ == '__main__':
    main()
