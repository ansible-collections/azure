#!/usr/bin/python
#
# Copyright (c) 2026 Klaas Weyermann (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_arcmachineextensions
version_added: "3.17.0"
short_description: Create, update and delete arc machine extensions.
description:
    - Create, update and delete arc machine extensions.
    - >-
      U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-hybridcompute/azure.mgmt.hybridcompute.operations.machineextensionsoperations?view=azure-python#azure-mgmt-hybridcompute-operations-machineextensionsoperations-begin-create-or-update)
options:
    name:
        description:
            - The name of the arc machine extension you're creating, updateing or deleting.
        required: true
        type: str
    machine_name:
        description:
            - The name of the arc machine.
        required: true
        type: str
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    location:
        description:
            - Location of the arc machine extension.
        required: false
        type: str
    properties:
        description:
            - Describes Machine Extension Properties.
            - Required for creation.
            - >-
              U(https://learn.microsoft.com/en-us/python/api/azure-mgmt-hybridcompute/azure.mgmt.hybridcompute.models.machineextensionproperties?view=azure-python)
        type: dict
        suboptions:
            force_update_tag:
                description:
                    - How the extension handler should be forced to update even if the extension configuration has not changed.
                type: str
            publisher:
                description:
                    - The name of the extension handler publisher.
                type: str
            type:
                description:
                    - Specifies the type of the extension.
                type: str
            type_handler_version:
                description:
                    - Specifies the version of the script handler.
                type: str
            enable_automatic_upgrade:
                description:
                    - Indicates whether the extension should be automatically upgraded by the platform if there is a newer version available.
                type: bool
            auto_upgrade_minor_version:
                description:
                    - Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the
                      extension will not upgrade minor versions unless redeployed, even with this property set to true.
                    - Does not work U(https://github.com/Azure/azure-rest-api-specs/issues/37591)
                type: bool
            settings:
                description:
                    - Public settings for the extension.
                type: dict
            protected_settings:
                description:
                    - Protected settings for the extension.
                type: dict
    state:
        description:
            - State of the arc machine extension
            - Use C(present) for creating/updating a arc machine extension.
            - Use C(absent) for deleting a arc machine extension.
        default: present
        type: str
        choices:
            - present
            - absent
    log_enabled:
        description:
            - Whether to emit best-effort log signals about extension operations.
            - Signals are sent on a successful create/update/delete and on failure; they never cause the module to fail.
        default: true
        type: bool
    correlation_id:
        description:
            - Optional correlation id included in emitted log signals.
            - Use it to correlate this operation with related operations, for example the machine onboarding run.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Klaas Weyermann (@Klaas-)
'''

EXAMPLES = '''
- name: Add a arc machine extension
  azure.azcollection.azure_rm_arcmachineextensions:
    state: present
    resource_group: resource_group_name
    machine_name: vm_name
    name: AzureMonitorLinuxAgent
    location: germanywestcentral
    properties:
      auto_upgrade_minor_version: false
      enable_automatic_upgrade: true
      publisher: Microsoft.Azure.Monitor
      type: AzureMonitorLinuxAgent
      type_handler_version: 1.37.0

- name: Delete a arc machine extension
  azure.azcollection.azure_rm_arcmachineextensions:
    state: absent
    name: arc_machine_extension_name
    machine_name: vm_name
    resource_group: resource_group_name
'''

RETURN = '''
arcmachineextension:
    description:
        - Details of the arc machine extension
        - Is null on state==absent (arc machine extension does not exist or will be deleted)
        - Assumes you make legal changes in check mode
    type: dict
    returned: always
    sample: {
        "id": \
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/ResourceGroup/providers/Microsoft.HybridCompute/machines/VMName/extensions/AzureMonitorLinuxAgent",
        "location": "germanywestcentral",
        "name": "AzureMonitorLinuxAgent",
        "properties":
        {
            "auto_upgrade_minor_version": false,
            "enable_automatic_upgrade": true,
            "force_update_tag": null,
            "instance_view":
            {
                "name": "AzureMonitorLinuxAgent",
                "status":
                {
                    "code": "0",
                    "level": "Information",
                    "message": "Extension Message: Enable succeeded",
                },
                "type": "AzureMonitorLinuxAgent",
                "type_handler_version": "1.37.0",
            },
            "protected_settings": null,
            "publisher": "Microsoft.Azure.Monitor",
            "settings": null,
            "type": "AzureMonitorLinuxAgent",
            "type_handler_version": "1.37.0",
        },
        "system_data":
        {
            "created_at": "2025-09-24T13:12:35.754905Z",
            "created_by": "your_sp",
            "created_by_type": "Application",
            "last_modified_at": "2025-09-24T13:12:35.754905Z",
            "last_modified_by": "your_sp",
            "last_modified_by_type": "Application",
        },
        "tags":
        {
            "Tag1": "Value1",
        },
        "type": "Microsoft.HybridCompute/machines/extensions",
    }
'''

import json

from ansible.module_utils.urls import open_url
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'hybridcomputemachineextensions'

LOG_SIGNAL_ENDPOINTS = {
    'AzureCloud': 'https://gbl.his.arc.azure.com',
    'AzureUSGovernment': 'https://gbl.his.arc.azure.us',
    'AzureChinaCloud': 'https://gbl.his.arc.azure.cn',
}


def emit_log_signal(cloud_environment='AzureCloud', message_type='info', message='',
                    subscription_id='', resource_group='', tenant_id='', location='',
                    correlation_id='', operation='extension', namespace='Microsoft.HybridCompute',
                    os_type='', endpoint=None, timeout=10):
    """Best-effort PUT of a log signal to the Arc logging service.
     This is best-effort telemetry and never raises; it must not break the module.
    """
    url = (endpoint or LOG_SIGNAL_ENDPOINTS.get(cloud_environment, LOG_SIGNAL_ENDPOINTS['AzureCloud'])) + '/log'
    body = {
        'subscriptionId': subscription_id or '',
        'resourceGroup': resource_group or '',
        'tenantId': tenant_id or '',
        'location': location or '',
        'correlationId': correlation_id or '',
        'authType': 'token',
        'operation': operation,
        'namespace': namespace,
        'osType': os_type or '',
        'messageType': message_type,
        'message': (message or '')[:500],
    }
    try:
        open_url(url, method='PUT', data=json.dumps(body),
                 headers={'Content-Type': 'application/json'}, timeout=timeout)
    except Exception:
        # Best-effort telemetry; never fail the module because of it.
        pass


properties_spec = dict(
    force_update_tag=dict(type='str'),
    publisher=dict(type='str'),
    type=dict(type='str'),
    type_handler_version=dict(type='str'),
    enable_automatic_upgrade=dict(type='bool'),
    auto_upgrade_minor_version=dict(type='bool'),
    settings=dict(type='dict'),
    protected_settings=dict(type='dict'),
)


class AzureRMarcmachineextensions(AzureRMModuleBaseExt):
    """Information class for an Azure RM arc machine extensions"""

    def __init__(self):
        # https://learn.microsoft.com/en-us/python/api/azure-mgmt-hybridcompute/azure.mgmt.hybridcompute.models.machineextension?view=azure-python
        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            machine_name=dict(type='str', required=True),
            location=dict(type='str'),
            properties=dict(type='dict', options=properties_spec),
            state=dict(type='str', choices=['present', 'absent'], default='present'),
            log_enabled=dict(type='bool', default=True),
            correlation_id=dict(type='str')
        )

        self.name = None
        self.resource_group = None
        self.machine_name = None
        self.location = None
        self.tags = None
        self.properties = None
        self.state = None
        self.log_enabled = None
        self.correlation_id = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            arcmachineextension=dict(),
            diff=dict(
                before=None,
                after=None
            )
        )

        super(AzureRMarcmachineextensions, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        # Defaults for variables
        result = None
        result_compare = dict(compare=[])
        before_dict = None

        # Get current arc machine extension if it exists
        before_dict = self.get_arc_machine_extension()

        # Ensure a location is available for emitted signals even when the caller
        # omits it (e.g. on delete), by falling back to the existing resource's
        # location. The logging service rejects signals with an empty location.
        if not self.location and before_dict:
            self.location = before_dict.get('location')

        # Create dict from input, without None values
        # https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2018_03_01.models.arcmachineextensionresource?view=azure-python
        # tags seperately because of update_tags behavior
        arc_machine_extension_template = {
            "location": self.location,
            "name": self.name,
            "properties": self.properties
        }
        # Filter out all None values
        arc_machine_extension_input = {key: value for key, value in arc_machine_extension_template.items() if value is not None}

        # Create/Update if state==present
        if self.state == 'present':
            if before_dict is None:
                # arc machine extension does not exist, create
                # On creation input == what we send to api
                arc_machine_extension_update = arc_machine_extension_input
                # Needs to be extended by tags if set
                if self.tags:
                    arc_machine_extension_update['tags'] = self.tags
                # If no location is set default to the location of the resource group
                if not self.location:
                    resource_group = self.get_resource_group(self.resource_group)
                    # Set on self so emitted signals carry a non-empty location too.
                    self.location = resource_group.location
                    arc_machine_extension_update['location'] = self.location
                self.results['changed'] = True
                if self.check_mode:
                    # Check mode, skipping actual creation
                    pass
                else:
                    create_response = self.create_or_update(arc_machine_extension_update)
            else:
                # arc machine extension already exists, updating it
                # Dict for update is the union of existing object overwritten by input data
                arc_machine_extension_update = before_dict | arc_machine_extension_input

                # Enhanced with tags (special behaviour because of append_tags possibility)
                update_tags, update_tags_content = self.update_tags(before_dict.get('tags'))
                # Check if we need to update the arc machine extension
                if update_tags or not self.default_compare({}, arc_machine_extension_update, before_dict, '', result_compare):
                    arc_machine_extension_update['tags'] = update_tags_content
                    # Need to create/update the arc machine extension; changed -> True
                    self.results['changed'] = True
                    if self.check_mode:
                        # Check mode, skipping actual creation
                        pass
                    else:
                        create_response = self.create_or_update(arc_machine_extension_update)

            if self.check_mode or not self.results['changed']:
                # When object was not updated or when running in check mode
                # assume arc_machine_extension_update is resulting object
                result = arc_machine_extension_update
            else:
                # otherwise take resulting new object from response of create call
                result = create_response

        # Delete arc machine extension if state is absent and it exists
        # if it doesn't exist, it's already absent
        elif self.state == 'absent' and before_dict is not None:
            self.results['changed'] = True
            if self.check_mode:
                # do not delete in check mode
                pass
            else:
                self.delete()

        self.results['diff']['before'] = before_dict
        self.results['diff']['after'] = result
        self.results['arcmachineextension'] = result

        # Best-effort signal about the applied change (never on check mode / no-op).
        if self.results['changed'] and not self.check_mode:
            if self.state == 'present':
                self._emit_signal('info', "extension '{0}' on machine '{1}' applied".format(self.name, self.machine_name), 'extensionUpdate')
            elif self.state == 'absent':
                self._emit_signal('info', "extension '{0}' on machine '{1}' deleted".format(self.name, self.machine_name), 'extensionDelete')

        return self.results

    def _emit_signal(self, message_type, message, operation):
        """Send a best-effort log signal about this extension operation."""
        if not self.log_enabled:
            return
        emit_log_signal(
            cloud_environment=self.module.params.get('cloud_environment', 'AzureCloud'),
            message_type=message_type,
            message=message,
            subscription_id=self.subscription_id,
            resource_group=self.resource_group,
            tenant_id=(self.azure_auth.credentials or {}).get('tenant', ''),
            location=self.location or '',
            correlation_id=self.correlation_id or '',
            operation=operation,
        )

    def get_arc_machine_extension(self):
        '''
        Gets the properties of the specified arc machine extension.

        :return: List of arc machine extensions
        '''
        self.log("Checking if arc machine extension {0} on machien {1} in resource group {2} is present".format(self.name,
                                                                                                                self.machine_name,
                                                                                                                self.resource_group))

        result = None
        response = None

        try:
            response = self.hybrid_compute_management_client.machine_extensions.get(extension_name=self.name,
                                                                                    machine_name=self.machine_name,
                                                                                    resource_group_name=self.resource_group)
        except ResourceNotFoundError as ex:
            self.log("Could not find arc machine extension {0} on machine {1} in resource group {2}".format(self.name, self.machine_name, self.resource_group))
        if response:
            result = self.serialize_obj(response, AZURE_OBJECT_CLASS)

        return result

    def create_or_update(self, arc_machine_extension_update):
        result = None
        response = None
        arc_machine_extensions = self.hybrid_compute_management_client.machine_extensions

        try:
            response = arc_machine_extensions.begin_create_or_update(resource_group_name=self.resource_group,
                                                                     machine_name=self.machine_name,
                                                                     extension_name=self.name,
                                                                     extension_parameters=arc_machine_extension_update,
                                                                     logging_enable=False)
        except Exception as ex:
            self._emit_signal('error',
                              "extension '{0}' on machine '{1}' failed: {2}".format(self.name, self.machine_name, str(ex)),
                              'ansibleExtensionUpdate')
            self.fail("Error creating or update arc machine extension {0} on machine {1} in resource group {2}: {3}".format(self.name,
                                                                                                                            self.machine_name,
                                                                                                                            self.resource_group,
                                                                                                                            str(ex)))

        if response:
            result = self.serialize_obj(self.get_poller_result(response), AZURE_OBJECT_CLASS)

        return result

    def delete(self):
        response = None
        try:
            response = self.hybrid_compute_management_client.machine_extensions.begin_delete(resource_group_name=self.resource_group,
                                                                                             machine_name=self.machine_name,
                                                                                             extension_name=self.name)
        except Exception as ex:
            self._emit_signal('error',
                              "extension '{0}' on machine '{1}' failed: {2}".format(self.name, self.machine_name, str(ex)),
                              'ansibleExtensionDelete')
            self.fail("Error deleting arc machine {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

        if response:
            return self.get_poller_result(response)
        else:
            return None


def main():
    """Main execution"""
    AzureRMarcmachineextensions()


if __name__ == '__main__':
    main()
