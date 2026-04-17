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

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'hybridcomputemachineextensions'

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
            state=dict(type='str', choices=['present', 'absent'], default='present')
        )

        self.name = None
        self.resource_group = None
        self.machine_name = None
        self.location = None
        self.tags = None
        self.properties = None
        self.state = None
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
                    arc_machine_extension_update['location'] = resource_group.location
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

        return self.results

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
