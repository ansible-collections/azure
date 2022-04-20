#!/usr/bin/python
#
# Copyright (c) 2017 Fred-sun, <xiuxi.sun@qq.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_automationrunbook_info
version_added: '1.12.0'
short_description: Get Azure automation runbook facts
description:
    - Get facts of automation runbook.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        type: str
        required: True
    name:
        description:
            - The name of the automation runbook.
        type: str
    show_content:
        description:
            - Wether retrieve the content of runbook identified by runbook name.
        type: bool
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Fred Sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Get details of an automation account
  azure_rm_automationrunbook_info:
    resource_group: "{{ resource_group }}"
    automation_account_name: "{{ account-name }}"
    name: "{{ runbook-name }}"

- name: List automation runbook in the account
  azure_rm_automationrunbook_info:
    resource_group: "{{ resource_group }}"
    automation_account_name: "{{ account-name }}"

- name: Get details of an automation account
  azure_rm_automationrunbook_info:
    resource_group: "{{ resource_group }}"
    automation_account_name: "{{ account-name }}"
    name: "{{ runbook-name }}"
    show_content: True

'''

RETURN = '''
automation_runbook:
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
            type: list
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


class AzureRMAutomationRunbookInfo(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            automation_account_name=dict(
                type='str',
                required=True
            ),
            show_content=dict(
                type='bool'
            ),
            tags=dict(
                type='list',
                elements='str'
            )
        )
        # store the results of the module operation
        self.results = dict()
        self.resource_group = None
        self.name = None
        self.tags = None
        self.automation_account_name = None
        self.show_content = None

        super(AzureRMAutomationRunbookInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec) + ['tags']:
            setattr(self, key, kwargs[key])

        if self.name and self.show_content:
            runbooks = [self.get_content()]
        elif self.name:
            runbooks = [self.get()]
        else:
            runbooks = self.list_by_automaiton_account()
        self.results['automation_runbook'] = [self.to_dict(x) for x in runbooks if x and self.has_tags(x.tags, self.tags)]
        return self.results

    def get_content(self):
        try:
            return self.automation_client.runbook.get(self.resource_group, self.automation_account_name, self.name)
        except ResourceNotFoundError as exc:
            pass

    def get(self):
        try:
            return self.automation_client.runbook.get(self.resource_group, self.automation_account_name, self.name)
        except ResourceNotFoundError as exc:
            pass

    def list_by_automaiton_account(self):
        result = []
        try:
            resp = self.automation_client.runbook.list_by_automation_account(self.resource_group, self.automation_account_name)
            while True:
                result.append(resp.next())
        except StopIteration:
            pass
        except Exception as exc:
            pass
        return result

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
    AzureRMAutomationRunbookInfo()


if __name__ == '__main__':
    main()
