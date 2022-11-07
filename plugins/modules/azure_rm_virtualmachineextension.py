#!/usr/bin/python
#
# Copyright (c) 2017 Sertac Ozercan <seozerca@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_virtualmachineextension

version_added: "0.1.2"

short_description: Managed Azure Virtual Machine extension

description:
    - Create, update and delete Azure Virtual Machine Extension.
    - Note that this module was called M(azure.azcollection.azure_rm_virtualmachine_extension) before Ansible 2.8. The usage did not change.

options:
    resource_group:
        description:
            - Name of a resource group where the vm extension exists or will be created.
        required: true
        type: str
    name:
        description:
            - Name of the vm extension.
        required: true
        type: str
    state:
        description:
            - State of the vm extension. Use C(present) to create or update a vm extension and C(absent) to delete a vm extension.
        default: present
        type: str
        choices:
            - absent
            - present
    location:
        description:
            - Valid Azure location. Defaults to location of the resource group.
        type: str
    virtual_machine_name:
        description:
            - The name of the virtual machine where the extension should be create or updated.
        required: true
        type: str
    publisher:
        description:
            - The name of the extension handler publisher.
        type: str
    virtual_machine_extension_type:
        description:
            - The type of the extension handler.
        type: str
    type_handler_version:
        description:
            - The type version of the extension handler.
        type: str
    settings:
        description:
            - JSON formatted public settings for the extension.
        type: dict
    protected_settings:
        description:
            - JSON formatted protected settings for the extension.
            - >-
                Previously configured settings are not available, so the parameter is not used for idempotency checks.
                If changes to this parameter need to be applied, use in conjunction with I(force_update_tag).
        type: dict
    auto_upgrade_minor_version:
        description:
            - Whether the extension handler should be automatically upgraded across minor versions.
        type: bool
    force_update_tag:
        description:
            - Whether the extension should be updated or re-run even if no changes can be detected from what is currently configured.
            - Helpful when applying changes to I(protected_settings).
        type: bool
        default: false
        version_added: '1.10.0'

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Sertac Ozercan (@sozercan)
    - Julien Stroheker (@julienstroheker)
'''

EXAMPLES = '''
- name: Create VM Extension
  azure_rm_virtualmachineextension:
    name: myvmextension
    location: eastus
    resource_group: myResourceGroup
    virtual_machine_name: myvm
    publisher: Microsoft.Azure.Extensions
    virtual_machine_extension_type: CustomScript
    type_handler_version: 2.0
    settings: '{"commandToExecute": "hostname"}'
    auto_upgrade_minor_version: true

- name: Delete VM Extension
  azure_rm_virtualmachineextension:
    name: myvmextension
    resource_group: myResourceGroup
    virtual_machine_name: myvm
    state: absent
'''

RETURN = '''
state:
    description:
        - Current state of the vm extension.
    returned: always
    type: dict
    sample: { "state":"Deleted" }

changed:
    description:
        - Whether or not the resource has changed.
    returned: always
    type: bool
    sample: true
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


def vmextension_to_dict(extension):
    '''
    Serializing the VM Extension from the API to Dict
    :return: dict
    '''
    return dict(
        id=extension.id,
        name=extension.name,
        location=extension.location,
        publisher=extension.publisher,
        virtual_machine_extension_type=extension.type_properties_type,
        type_handler_version=extension.type_handler_version,
        auto_upgrade_minor_version=extension.auto_upgrade_minor_version,
        settings=extension.settings,
        protected_settings=extension.protected_settings,
    )


class AzureRMVMExtension(AzureRMModuleBase):
    """Configuration class for an Azure RM VM Extension resource"""

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
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            location=dict(
                type='str'
            ),
            virtual_machine_name=dict(
                type='str',
                required=True
            ),
            publisher=dict(
                type='str'
            ),
            virtual_machine_extension_type=dict(
                type='str'
            ),
            type_handler_version=dict(
                type='str'
            ),
            auto_upgrade_minor_version=dict(
                type='bool'
            ),
            settings=dict(
                type='dict'
            ),
            protected_settings=dict(
                type='dict', no_log=True
            ),
            force_update_tag=dict(
                type='bool',
                default=False
            ),
        )

        self.resource_group = None
        self.name = None
        self.virtual_machine_name = None
        self.location = None
        self.publisher = None
        self.virtual_machine_extension_type = None
        self.type_handler_version = None
        self.auto_upgrade_minor_version = None
        self.settings = None
        self.protected_settings = None
        self.state = None
        self.force_update_tag = False

        required_if = [
            ('state', 'present', ['publisher', 'virtual_machine_extension_type', 'type_handler_version']),
        ]

        self.results = dict(changed=False, state=dict())

        super(AzureRMVMExtension, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=False,
                                                 supports_tags=False,
                                                 required_if=required_if)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.module._name == 'azure_rm_virtualmachine_extension':
            self.module.deprecate("The 'azure_rm_virtualmachine_extension' module has been renamed to 'azure_rm_virtualmachineextension'", version=(2, 9))

        resource_group = None
        to_be_updated = False

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        response = self.get_vmextension()

        if self.state == 'present':
            if not response:
                to_be_updated = True
            else:
                if self.force_update_tag:
                    to_be_updated = True

                if self.settings is not None:
                    if response['settings'] != self.settings:
                        response['settings'] = self.settings
                        to_be_updated = True
                else:
                    self.settings = response['settings']

                if response['location'] != self.location:
                    self.location = response['location']
                    self.module.warn("Property 'location' cannot be changed")

                if response['publisher'] != self.publisher:
                    self.publisher = response['publisher']
                    self.module.warn("Property 'publisher' cannot be changed")

                if response['virtual_machine_extension_type'] != self.virtual_machine_extension_type:
                    self.virtual_machine_extension_type = response['virtual_machine_extension_type']
                    self.module.warn("Property 'virtual_machine_extension_type' cannot be changed")

                if response['type_handler_version'] != self.type_handler_version:
                    response['type_handler_version'] = self.type_handler_version
                    to_be_updated = True

                if self.auto_upgrade_minor_version is not None:
                    if response['auto_upgrade_minor_version'] != self.auto_upgrade_minor_version:
                        response['auto_upgrade_minor_version'] = self.auto_upgrade_minor_version
                        to_be_updated = True
                else:
                    self.auto_upgrade_minor_version = response['auto_upgrade_minor_version']

            if to_be_updated:
                self.results['changed'] = True
                self.results['state'] = self.create_or_update_vmextension()
        elif self.state == 'absent':
            if response:
                self.delete_vmextension()
                self.results['changed'] = True

        return self.results

    def create_or_update_vmextension(self):
        '''
        Method calling the Azure SDK to create or update the VM extension.
        :return: void
        '''
        self.log("Creating VM extension {0}".format(self.name))
        try:
            params = self.compute_models.VirtualMachineExtension(
                location=self.location,
                publisher=self.publisher,
                type_properties_type=self.virtual_machine_extension_type,
                type_handler_version=self.type_handler_version,
                auto_upgrade_minor_version=self.auto_upgrade_minor_version,
                settings=self.settings,
                protected_settings=self.protected_settings,
                force_update_tag=self.force_update_tag,
            )
            poller = self.compute_client.virtual_machine_extensions.begin_create_or_update(self.resource_group, self.virtual_machine_name, self.name, params)
            response = self.get_poller_result(poller)
            return vmextension_to_dict(response)

        except Exception as e:
            self.log('Error attempting to create the VM extension.')
            self.fail("Error creating the VM extension: {0}".format(str(e)))

    def delete_vmextension(self):
        '''
        Method calling the Azure SDK to delete the VM Extension.
        :return: void
        '''
        self.log("Deleting vmextension {0}".format(self.name))
        try:
            poller = self.compute_client.virtual_machine_extensions.begin_delete(self.resource_group, self.virtual_machine_name, self.name)
            self.get_poller_result(poller)
        except Exception as e:
            self.log('Error attempting to delete the vmextension.')
            self.fail("Error deleting the vmextension: {0}".format(str(e)))

    def get_vmextension(self):
        '''
        Method calling the Azure SDK to get a VM Extension.
        :return: void
        '''
        self.log("Checking if the vm extension {0} is present".format(self.name))
        found = False
        try:
            response = self.compute_client.virtual_machine_extensions.get(self.resource_group, self.virtual_machine_name, self.name)
            found = True
        except ResourceNotFoundError as e:
            self.log('Did not find vm extension')
        if found:
            return vmextension_to_dict(response)
        else:
            return False


def main():
    """Main execution"""
    AzureRMVMExtension()


if __name__ == '__main__':
    main()
