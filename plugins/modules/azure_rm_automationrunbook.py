#!/usr/bin/python
#
# Copyright (c) 2017 Fred Sun, <xiuxi.sun@qq.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_automationrunbook
version_added: '1.12.0'
short_description: Mange automation runbook
description:
    - Create, update, delete or publish automation runbook.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: True
    name:
        description:
            - The name of the automation runbook.
        type: str
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        type: str
        required: True
    location:
        description:
            - The location of the automation runbook.
        type: str
    description:
        description:
            - Sets the description.
        type: str
    runbook_type:
        description:
            - Sets the type of the runbook.
        type: str
        choices:
            - Script
            - Graph
            - PowerShellWorkflow
            - PowerShell
            - GraphPowerShellWorkflow
            - GraphPowerShell
    log_activity_trace:
        description:
            - Sets the option to log activity trace of the runbook.
        type: int
    log_progress:
        description:
            - Sets progress log option.
        type: bool
    log_verbose:
        description:
            - Sets verbose log option.
        type: bool
    publish:
        description:
            - Whether to publish the runbook.
        type: bool
    state:
        description:
            - State of the automation runbook. Use C(present) to create or update a automation runbook and use C(absent) to delete.
        type: str
        default: present
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Fred Sun (@Fred-sun)

'''

EXAMPLES = '''
- name: create automation runbook with default parameters
  azure_rm_automationrunbook:
    resource_group: "{{ resource_group }}"
    automation_account_name: "{{ account-name }}"
    name: "{{ runbook-name }}"
    runbook_type: "Script"
    description: "Fred test"

- name: create automation runbook with more parameters
  azure_rm_automationrunbook:
    resource_group: "{{ resource_group }}"
    automation_account_name: "{{ account-name }}"
    name: "{{ runbook-name }}"
    runbook_type: "Script"
    description: "Fred test"
    log_activity_trace: 3
    log_progress: true
    log_verbose: false
    tags:
      key1: value1

- name: Publish automation runbook
  azure_rm_automationrunbook:
    resource_group: "{{ resource_group }}"
    automation_account_name: "{{ account-name }}"
    name: "{{ runbook-name }}"
    publish: true

- name: Delete automation runbook
  azure_rm_automationrunbook:
    resource_group: "{{ resource_group }}"
    automation_account_name: "{{ account-name }}"
    name: "{{ runbook-name }}"
    state: absent
'''

RETURN = '''
state:
    description:
        - List of automation runbook dicts.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            type: str
            returned: always
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups
                     /myResourceGroup/providers/Microsoft.Automation/automationAccounts/test/runbooks/runbook_name"
        resource_group:
            description:
                - Resource group name.
            type: str
            returned: always
            sample: myResourceGroup
        name:
            description:
                - Resource name.
            type: str
            returned: always
            sample: Testing
        location:
            description:
                - Resource location.
            type: str
            returned: always
            sample: eastus
        creation_time:
            description:
                - The resource creation date time.
            type: str
            returned: always
            sample: "2022-03-24T06:30:54.116666+00:00"
        job_count:
            description:
                - The job count of the runbook.
            type: int
            returned: always
            sample: 3
        last_modified_by:
            description:
                - The resource last modifier.
            type: str
            returned: always
            sample: Fred-sun
        last_modified_time:
            description:
                - The last person to update the resource.
            type: str
            returned: always
            sample: "2022-03-25T06:30:54.116666+00:00"
        log_activity_trace:
            description:
                - The option to log activity trace of the runbook.
            type: int
            returned: always
            sample: 3
        log_progress:
            description:
                - Whether show progress log option.
            type: bool
            returned: always
            sample: True
        log_verbose:
            description:
                - Whether show verbose log option.
            type: bool
            returned: always
            sample: True
        output_types:
            description:
                - The runbook output type.
            type: list
            returned: always
            sample: []
        runbook_content_link:
            description:
                - The publish runbook content link.
            type: str
            returned: always
            sample: null
        state:
            description:
                - The resource state.
            type: str
            returned: always
            sample: Published
        tags:
            description:
                - The resource tags.
            type: dict
            returned: always
            sample: { 'key1': 'value1' }
        type:
            description:
                - The resource automation runbook type.
            type: str
            returned: always
            sample: "Microsoft.Automation/AutomationAccounts/Runbooks"
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass


class AzureRMAutomationRunbook(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            automation_account_name=dict(
                type='str',
                required=True
            ),
            runbook_type=dict(
                type='str',
                choices=['Script', 'Graph', 'PowerShellWorkflow', 'PowerShell', 'GraphPowerShellWorkflow', 'GraphPowerShell']
            ),
            description=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            log_activity_trace=dict(
                type='int'
            ),
            log_progress=dict(
                type='bool'
            ),
            publish=dict(
                type='bool'
            ),
            log_verbose=dict(
                type='bool'
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                default='present'
            )
        )
        # store the results of the module operation
        self.results = dict()
        self.resource_group = None
        self.name = None
        self.automation_account_name = None
        self.runbook_type = None
        self.description = None
        self.log_activity_trace = None
        self.log_progress = None
        self.log_verbose = None
        self.location = None
        self.publish = None

        super(AzureRMAutomationRunbook, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec) + ['tags']:
            setattr(self, key, kwargs[key])

        if not self.location:
            resource_group = self.get_resource_group(self.resource_group)
            self.location = resource_group.location

        runbook = self.get()
        changed = False

        if self.state == 'present':
            if runbook:
                update_parameter = dict()
                if self.tags is not None:
                    update_tags, tags = self.update_tags(runbook['tags'])
                    if update_tags:
                        changed = True
                        update_parameter['tags'] = tags
                if self.description is not None and self.description != runbook['description']:
                    changed = True
                    update_parameter['description'] = self.description
                if self.log_activity_trace is not None and self.log_activity_trace != runbook['log_activity_trace']:
                    changed = True
                    update_parameter['log_activity_trace'] = self.log_activity_trace
                if self.log_progress is not None and self.log_progress != runbook['log_progress']:
                    changed = True
                    update_parameter['log_progress'] = self.log_progress
                if self.log_verbose is not None and self.log_verbose != runbook['log_verbose']:
                    changed = True
                    update_parameter['log_verbose'] = self.log_verbose
                if self.location is not None and self.location != runbook['location']:
                    changed = True
                    self.fail("Parameter error (location): The parameters {0} cannot be update".format(self.location))
                if self.runbook_type is not None and self.runbook_type != runbook['runbook_type']:
                    changed = True
                    self.fail("Parameter error (runbook_type): The parameters {0} cannot be update".format(self.runbook_type))

                if changed:
                    if not self.check_mode:
                        if update_parameter.get('log_activity_trace'):
                            runbook['log_activity_trace'] = update_parameter.get('log_activity_trace')

                        paramters = self.automation_models.RunbookCreateOrUpdateParameters(
                            location=runbook['location'] if update_parameter.get('location') else update_parameter.get('location'),
                            log_verbose=runbook['log_verbose'] if update_parameter.get('log_verbose') else update_parameter.get('log_verbose'),
                            runbook_type=runbook['runbook_type'] if update_parameter.get('runbook_type') else update_parameter.get('runbook_type'),
                            description=runbook['description'] if update_parameter.get('description') else update_parameter.get('description'),
                            log_activity_trace=runbook['log_activity_trace'],
                            tags=runbook['tags'] if update_parameter.get('tags') else update_parameter.get('tags'),
                            log_progress=runbook['log_progress'] if update_parameter.get('log_progress') else update_parameter.get('log_progress')
                        )

                        runbook = self.update_runbook(update_parameter)

            else:
                paramters = self.automation_models.RunbookCreateOrUpdateParameters(
                    location=self.location,
                    log_verbose=self.log_verbose,
                    runbook_type=self.runbook_type,
                    description=self.description,
                    log_activity_trace=self.log_activity_trace,
                    tags=self.tags,
                    log_progress=self.log_progress
                )
                changed = True
                if not self.check_mode:
                    runbook = self.create_or_update(paramters)

            if not self.check_mode:
                if self.publish and runbook['state'] != 'Published':
                    changed = True
                    self.publish_runbook()
        else:
            changed = True
            if not self.check_mode:
                runbook = self.delete_automation_runbook()

        self.results['changed'] = changed
        self.results['state'] = runbook
        return self.results

    def get(self):
        try:
            response = self.automation_client.runbook.get(self.resource_group, self.automation_account_name, self.name)
            return self.to_dict(response)
        except ResourceNotFoundError:
            pass

    def publish_runbook(self):
        response = None
        try:
            response = self.automation_client.runbook.begin_publish(self.resource_group, self.automation_account_name, self.name)
        except Exception as exc:
            self.fail('Error when updating automation account {0}: {1}'.format(self.name, exc.message))

    def update_runbook(self, parameters):
        try:
            response = self.automation_client.runbook.update(self.resource_group, self.automation_account_name, self.name, parameters)
            return self.to_dict(response)
        except Exception as exc:
            self.fail('Error when updating automation account {0}: {1}'.format(self.name, exc.message))

    def create_or_update(self, parameters):
        try:
            response = self.automation_client.runbook.create_or_update(self.resource_group, self.automation_account_name, self.name, parameters)
            return self.to_dict(response)
        except Exception as exc:
            self.fail('Error when creating automation account {0}: {1}'.format(self.name, exc.message))

    def delete_automation_runbook(self):
        try:
            return self.automation_client.runbook.delete(self.resource_group, self.automation_account_name, self.name)
        except Exception as exc:
            self.fail('Error when deleting automation account {0}: {1}'.format(self.name, exc.message))

    def to_dict(self, runbook):
        if not runbook:
            return None
        runbook_dict = dict(
            id=runbook.id,
            type=runbook.type,
            name=runbook.name,
            tags=runbook.tags,
            location=runbook.location,
            runbook_type=runbook.runbook_type,
            runbook_content_link=runbook.publish_content_link,
            state=runbook.state,
            log_verbose=runbook.log_verbose,
            log_progress=runbook.log_progress,
            log_activity_trace=runbook.log_activity_trace,
            job_count=runbook.job_count,
            output_types=runbook.output_types,
            last_modified_by=runbook.last_modified_by,
            last_modified_time=runbook.last_modified_time,
            creation_time=runbook.creation_time,
            description=runbook.description
        )
        return runbook_dict


def main():
    AzureRMAutomationRunbook()


if __name__ == '__main__':
    main()
