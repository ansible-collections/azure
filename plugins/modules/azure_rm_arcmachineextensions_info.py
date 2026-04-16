#!/usr/bin/python
#
# Copyright (c) 2026 Klaas Weyermann (@Klaas-)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_arcmachineextensions_info
version_added: "3.17.0"
short_description: Get arc machine extensions
description:
    - Get arc machine extensions

options:
    name:
        description:
            - The name of the arc machine extension you're trying to get details about.
        type: str
    machine_name:
        description:
            - The name of the arc machine
        required: true
        type: str
    resource_group:
        description:
            - The name of the resource group in which the arc machine is
        required: true
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Klaas Weyermann (@Klaas-)
'''

EXAMPLES = '''
- name: Get arc machine extension details
  azure.azcollection.azure_rm_arcmachineextensions_info:
    name: extension_name
    machine_name: arc_machine_name
    resource_group: resource_group_name

- name: Get all arc machine extensions of specific arc machine
  azure.azcollection.azure_rm_arcmachineextensions_info:
    machine_name: arc_machine_name
    resource_group: resource_group_name
'''

RETURN = '''
arcmachineextensions:
    description:
        - List of arc machine extensions
        - Can be empty if listing arc machine extensions or arc machine extension does not exist
    type: list
    returned: always
    sample: [
        {
            "id": \
"/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/Resource_Group/providers/Microsoft.HybridCompute/machines/VMName/extensions/AzureMonitorLinuxAgent",
            "location": "germanywestcentral",
            "name": "AzureMonitorLinuxAgent",
            "properties": {
                "auto_upgrade_minor_version": false,
                "enable_automatic_upgrade": true,
                "instance_view": {
                    "name": "AzureMonitorLinuxAgent",
                    "status": {
                        "code": "0",
                        "level": "Information",
                        "message": "Extension Message: Enable succeeded"
                    },
                    "type": "AzureMonitorLinuxAgent",
                    "type_handler_version": "1.37.0"
                },
                "provisioning_state": "Succeeded",
                "publisher": "Microsoft.Azure.Monitor",
                "settings": {},
                "type": "AzureMonitorLinuxAgent",
                "type_handler_version": "1.37.0"
            },
            "tags": {
                "TagKey": "TagValue"
            },
            "type": "Microsoft.HybridCompute/machines/extensions"
        }
    ]
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'hybridcomputemachineextensions'


class AzureRMarcmachineextensionsInfo(AzureRMModuleBase):
    """Information class for an Azure RM arc machine extensions"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str', required=False),
            machine_name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True)
        )

        self.name = None
        self.machine_name = None
        self.resource_group = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            arcmachineextensions=[]
        )

        super(AzureRMarcmachineextensionsInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                              supports_check_mode=True,
                                                              supports_tags=False,
                                                              facts_module=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            result = self.get_arc_machine_extension()
        else:
            result = self.list_arc_machine_extensions()

        self.results['arcmachineextensions'] = result

        return self.results

    def get_arc_machine_extension(self):
        '''
        Gets the properties of the specified arc machine extension.

        :return: List of arc machine extensions
        '''
        self.log("Checking if arc machine extension {0} in resource group {1} is present".format(self.name,
                                                                                                 self.resource_group))

        result = []
        arc_machine_extension = None

        try:
            arc_machine_extension = self.hybrid_compute_management_client.machine_extensions.get(machine_name=self.machine_name,
                                                                                                 resource_group_name=self.resource_group,
                                                                                                 extension_name=self.name)
        except ResourceNotFoundError as ex:
            self.log("Could not find arc machine extension {0} in resource group {1}".format(self.name, self.resource_group))
            return []
        except HttpResponseError as ex:
            if ex.error.code == 'InvalidSubscriptionId':
                self.log("Could not find subscription id")
                return []
            else:
                raise Exception(ex)
        if arc_machine_extension:
            result = [self.serialize_obj(arc_machine_extension, AZURE_OBJECT_CLASS)]

        return result

    def list_arc_machine_extensions(self):
        '''
        Gets the properties of the specified arc machine extensions in resource group or subscription.

        :return: List of arc machine extensions
        '''

        result = []
        arc_machine_extensions = None

        self.log("Checking if the arc machine extensions in resource group {0} and machine name {1} are present".format(self.resource_group,
                                                                                                                        self.machine_name))
        arc_machine_extensions_mgmt_client = self.hybrid_compute_management_client.machine_extensions
        arc_machine_extensions = arc_machine_extensions_mgmt_client.list(resource_group_name=self.resource_group,
                                                                         machine_name=self.machine_name)
        if arc_machine_extensions:
            # it seems the exception is thrown when iterating through arc_machine_extensions, not when setting arc_machine_extensions
            try:
                for item in arc_machine_extensions:
                    result.append(self.serialize_obj(item, AZURE_OBJECT_CLASS))
            except ResourceNotFoundError as ex:
                self.log("Could not find resource group {0}".format(self.resource_group))
            except HttpResponseError as ex:
                if ex.error.code == 'InvalidSubscriptionId':
                    self.log("Could not find subscription id")
                else:
                    raise Exception(ex)

        return result


def main():
    """Main execution"""
    AzureRMarcmachineextensionsInfo()


if __name__ == '__main__':
    main()
