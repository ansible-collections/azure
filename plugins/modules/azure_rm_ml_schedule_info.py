#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_schedule_info
version_added: "3.19.0"
short_description: List ML Schedule resources
description:
    - List ML Schedule resources.
options:
    name:
        description:
            - Name of the Azure ML schedule.
        type: str
        required: false
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    ml_workspace:
        description:
            - Name of the Azure ML workspace.
        required: true
        type: str
    list_type:
        description:
            - Specify if you want enabled, disabled or all schedules.
        type: str
        choices:
            - enabled
            - disabled
            - all

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: List ML Schedule by name
  azure.azcollection.azure_rm_ml_schedule_info:
    name: MySchedule
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace

- name: List Disabled ML Schedules
  azure.azcollection.azure_rm_ml_schedule_info:
    resource_group: myResourceGroup
    ml_workspace: myMLWorkspace
    list_type: disabled
'''

RETURN = '''
ml_schedules:
    description:
        - Schedules that match the query.
    returned: always
    type: dict
    sample: [
      {
        "create_job": {
            "compute": "azureml:cpu-cluster",
            "display_name": "hello_pipeline_abc",
            "experiment_name": "Default",
            "inputs": {
                "hello_string_top_level_input": "hello world"
            },
            "jobs": {
                "a": {
                    "component": "azureml:/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-schedule/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/components/azureml_anonymous/versions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                    "inputs": {
                        "hello_string": {
                            "path": "${{ '{{' }}parent.inputs.hello_string_top_level_input{{ '}}' }}"
                        }
                    },
                    "type": "command"
                },
                "b": {
                    "component": "azureml:/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-schedule/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/components/azureml_anonymous/versions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                    "type": "command"
                },
                "c": {
                    "component": "azureml:/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/xxxxx-ml-schedule/providers/Microsoft.MachineLearningServices/workspaces/workspace-xxxxxxxxxx/components/azureml_anonymous/versions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                    "inputs": {
                        "world_input": {
                            "path": "${{ '{{' }}parent.jobs.b.outputs.world_output{{ '}}' }}"
                        }
                    },
                    "type": "command"
                }
            },
            "status": "NotStarted",
            "type": "pipeline"
        },
        "creation_context": {
            "created_at": "2026-05-14T16:46:52.141013+00:00",
            "created_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "created_by_type": "User",
            "last_modified_at": "2026-05-14T16:47:49.168130+00:00",
            "last_modified_by": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "last_modified_by_type": "User"
        },
        "description": "a simple hourly cron job schedule",
        "display_name": "Simple cron job schedule",
        "is_enabled": false,
        "name": "schedulexxxxxxxxxx",
        "provisioning_state": "Succeeded",
        "trigger": {
            "expression": "1 * * * *",
            "start_time": "2022-07-10 10:00:00",
            "time_zone": "Pacific Standard Time",
            "type": "cron"
        }
      }
    ]
'''  # NOQA


try:
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLScheduleInfo(MLClientCommon):
    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=False,
            ),
            resource_group=dict(
                type='str',
                required=True,
            ),
            ml_workspace=dict(
                type='str',
                required=True,
            ),
            list_type=dict(
                type='str',
                choices=['disabled', 'enabled', 'all'],
            ),
        )

        self._client = None
        self.ml_registry = None

        self.results = dict(
            ml_schedules=[]
        )

        mutually_exclusive = [('name', 'list_type')]

        super(AzureRMMLScheduleInfo, self).__init__(
            self.module_arg_spec,
            supports_tags=False,
            supports_check_mode=True,
            facts_module=True,
            mutually_exclusive=mutually_exclusive,
        )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name:
            try:
                result = self.client.schedules.get(name=self.name)
                ml_schedules = [self.entity_to_dict(result)]
            except ResourceNotFoundError:
                ml_schedules = []
        else:
            list_view_type = self.get_schedule_list_view_type(self.list_type)
            results = self.client.schedules.list(
                list_view_type=list_view_type
            )
            ml_schedules = [self.entity_to_dict(self.client.schedules.get(x.name)) for x in results]

        self.results['ml_schedules'] = ml_schedules
        return self.results


def main():
    AzureRMMLScheduleInfo()


if __name__ == '__main__':
    main()
