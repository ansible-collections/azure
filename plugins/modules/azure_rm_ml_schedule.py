#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_ml_schedule
version_added: "3.19.0"
short_description: Create, Disable, Enable or Delete an Azure Machine Learning Schedule
description:
    - Create, Disable, Enable or Delete an Azure Machine Learning Schedule.
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
    resource_definition:
        description:
            - "Azure ML schedule specification. The YAML reference docs
              for schedule can be found at:
              https://aka.ms/ml-cli-v2-schedule-yaml-reference."
        type: str
        required: false
    state:
        description:
            - State of the Schedule. Use C(present) to create
              or update. C(disabled) to disable, C(enabled) to
              enable.
        default: present
        type: str
        choices:
            - present
            - disabled
            - enabled
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Bill Peck (@p3ck)
'''

EXAMPLES = '''
- name: Create ML Schedule
  azure.azcollection.azure_rm_ml_schedule:
    name: schedulexxxxxxxxxx
    resource_group: xxxxx-ml-schedule
    ml_workspace: workspace-xxxxxxxxxx
    resource_definition: |
      $schema: https://azuremlschemas.azureedge.net/latest/schedule.schema.json
      name: simple_cron_job_schedule
      display_name: Simple cron job schedule
      description: a simple hourly cron job schedule

      trigger:
        type: cron
        expression: "1 * * * *"
        start_time: "2022-07-10T10:00:00" # optional
        time_zone: "Pacific Standard Time" # optional

      # create_job: azureml:simple-pipeline-job
      create_job: ./targets/azure_rm_ml_schedule/files/simple-pipeline-job.yml
'''

RETURN = '''
changed:
    description:
        - Whether the resource is changed.
    returned: always
    type: bool
    sample: false
ml_schedule:
    description:
        - Schedule that was just created or updated.
    returned: always
    type: dict
    sample: {
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
'''  # NOQA


try:
    import io
    from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ml import MLClientCommon
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.ml.entities._load_functions import load_schedule
    from azure.ai.ml.entities._load_functions import _try_load_yaml_dict
    from azure.ai.ml.exceptions import ValidationException
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMLSchedule(MLClientCommon):

    PARAM_OVERRIDES = ['name',
                       'tags',
                       ]

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=False,
            ),
            resource_definition=dict(
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
            state=dict(
                type='str',
                default='present',
                choices=['present', 'disabled', 'enabled', 'absent'],
            ),
        )

        self._client = None
        self.ml_registry = None
        self.state = None

        self.results = dict(
            changed=False,
            compare=[],
            ml_schedule={}
        )

        required_if = [
            ('state', 'present', ['resource_definition']),
            ('resource_definition', None, ['name'])
        ]

        super(AzureRMMLSchedule, self).__init__(self.module_arg_spec,
                                                supports_check_mode=False,
                                                required_if=required_if,
                                                )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False

        # Process resource_file yaml and passed in parameters
        try:
            resource_definition = io.StringIO(self.resource_definition)
            yaml_dict = _try_load_yaml_dict(resource_definition)
        except ValidationException:
            yaml_dict = dict()
        schedule_name = self.name or yaml_dict.get('name', None)

        ml_schedule_info = self.get(name=schedule_name)

        if self.state == 'present':
            params_override = self.update_params(kwargs, self.PARAM_OVERRIDES)

            resource_definition = io.StringIO(self.resource_definition)
            ml_schedule = load_schedule(source=resource_definition,
                                        params_override=params_override)

            if ml_schedule_info:
                # Update
                orig_schedule_info = self.entity_to_dict(ml_schedule_info)

                response = self.client.begin_create_or_update(ml_schedule)
                ml_schedule_object = self.get_poller_result(response)
                ml_schedule_info = self.entity_to_dict(ml_schedule_object)

                changed = not self.default_compare(
                    {},
                    ml_schedule_info,
                    orig_schedule_info,
                    '',
                    self.results
                )
            else:
                # Create
                changed = True
                response = self.client.begin_create_or_update(ml_schedule)
                ml_schedule_object = self.get_poller_result(response)
                ml_schedule_info = self.entity_to_dict(ml_schedule_object)
        elif self.state == 'absent':
            # Delete
            if ml_schedule_info:
                changed = True
                response = self.client.schedules.begin_delete(name=schedule_name)
                result = self.get_poller_result(response)
                ml_schedule_info = self.get(schedule_name, as_dict=True)
        elif self.state == 'enabled':
            # Enable
            list_view_type = self.get_schedule_list_view_type('disabled')
            results = self.client.schedules.list(list_view_type=list_view_type)
            ml_schedules = [x.name for x in results]

            if schedule_name in ml_schedules:
                changed = True
                self.enable(name=schedule_name)
            ml_schedule_info = self.get(name=schedule_name,
                                        as_dict=True)
        elif self.state == 'disabled':
            # Disable
            list_view_type = self.get_schedule_list_view_type('enabled')
            results = self.client.schedules.list(list_view_type=list_view_type)
            ml_schedules = [x.name for x in results]

            if schedule_name in ml_schedules:
                changed = True
                self.disable(name=schedule_name)
            ml_schedule_info = self.get(name=schedule_name,
                                        as_dict=True)

        self.results['ml_schedule'] = ml_schedule_info
        self.results['changed'] = changed
        return self.results

    def update_params(self, kwargs, param_overrides, ml_schedule=None):
        params_override = []

        # If ml_schedule is defined use those values as a base.
        # Update can't change some of these values but we need
        # to keep the same values as before the update.
        if ml_schedule:
            items = self.entity_to_dict(ml_schedule).items()
            params_override = [{k: v} for k, v in items]

        # Update values based on what param_overrides says we can update.
        for key in list(self.module_arg_spec.keys()):
            if kwargs[key] is not None and key in param_overrides:
                params_override.append({key: kwargs[key]})
        return params_override

    def get(self, name, as_dict=False):
        try:
            # Attempt to retrieve ml_schedule based on name
            ml_schedule_info = self.client.schedules.get(name=name)
            if as_dict:
                ml_schedule_info = self.entity_to_dict(ml_schedule_info)
        except ResourceNotFoundError:
            ml_schedule_info = None
        return ml_schedule_info

    def enable(self, name=None):
        try:
            response = self.client.schedules.begin_enable(name=name)
            ml_schedule_object = self.get_poller_result(response)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error enabling the schedule instance: {0}".format(str(e)))

    def disable(self, name=None):
        try:
            response = self.client.schedules.begin_disable(name=name)
            ml_schedule_object = self.get_poller_result(response)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail("Error disabling the schedule instance: {0}".format(str(e)))


def main():
    AzureRMMLSchedule()


if __name__ == '__main__':
    main()
