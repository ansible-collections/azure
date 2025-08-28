#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_dedicatedhost

version_added: "3.8.0"

short_description: Create, delete and update a dedicated host

description:
    - Creates, deletes, and updates a dedicated host.

options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    host_group_name:
        description:
            - The name of the host group.
        type: str
        required: true
    name:
        description:
            - The name of the dedicated host.
        required: true
        type: str
    location:
        description:
            - Valid Azure location for dedicated host. Defaults to location of resource group.
        type: str
    platform_fault_domain:
        description:
            - Fault domain of the dedicated host within a dedicated host group.
        type: int
        choices:
            - 0
    sku:
        description:
            - SKU of the dedicated host for Hardware Generation and VM family.
            - Only C(name) is required to be set
        type: dict
        suboptions:
            name:
                description:
                    - The sku name.
                type: str
    auto_replace_on_failure:
        description:
            - Specifies whether the dedicated host should be replaced automatically in case of a failure.
            - The value is defaulted to C(true) when not provided.
        default: true
        type: bool
    license_type:
        description:
            - Specifies the software license type that will be applied to the VMs deployed on the dedicated host.
        type: str
        choices:
            - 'None'
            - 'Windows_Server_Hybrid'
            - 'Windows_Server_Perpetual'
    is_restart:
        description:
            - Wether to restart the dedicated host.
        type: bool
        default: false
    state:
        description:
            - Assert the state of the host group. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - magodo (@magodo)
    - xuzhang3 (@xuzhang3)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Create a dedicated host
  azure_rm_dedicatedhost:
    resource_group: myAzureResourceGroup
    name: mydedicatedhost
    location: eastus
    platform_fault_domain: 1
    sku:
      name: DSv3-Type1
    state: present

- name: Delete a dedicated host
  azure_rm_dedicatedhost:
    resource_group: myAzureResourceGroup
    host_group_name: myhostgroup
    name: mydedicatedhost
    state: absent
'''

RETURN = '''
state:
    description:
        - Gets a list of dedicated host.
    returned: always
    type: complex
    contains:
        host_group_name:
            description:
                - The name of the host group.
            type: str
            returned: always
            sample: myDedicatedHostGroup
        resource_group:
            description:
                - The name of the resource group.
            type: str
            returned: always
            sample: myResourceGroup
        name:
            description:
                - The dedicate hsot name.
            type: str
            returned: always
            sample: myHost
        id:
            description:
                - The dedicate host ID.
            type: str
            returned: always
            sample: "/subscriptions/{subscription-id}/resourceGroups/myResourceGroup/providers/Microsoft.Compute/HostGroups/myDedicatedHostGroup/hosts/myHost"
        location:
            description:
                - Resource location.
            type: str
            returned: always
            sample: eastus
        tags:
            description:
                - Resource tags.
            type: dict
            returned: always
            sample: {'key1': 'value1'}
        sku:
            description:
                - SKU of the dedicated host for Hardware Generation and VM family.
            type: dict
            returned: always
            sample: {'name': 'DSv3-Type4'}
        auto_replace_on_failure:
            description:
                - Specifies whether the dedicated host should be replaced automatically in case of a failure.
            type: bool
            returned: always
            sample: true
        license_type:
            description:
                - Specifies the software license type that will be applied to the VMs deployed on the dedicated host.
            type: str
            returned: always
            sample: Windows_Server_Hybrid
        provisioning_state:
            description:
                - The provisioning state, which only appears in the response.
            type: str
            returned: always
            sample: Succeeded
        platform_fault_domain:
            description:
                - Fault domain of the dedicated host within a dedicated host.
            type: str
            returned: always
            sample: 1
        virtual_machines:
            description:
                - A list of references to all virtual machines in the Dedicated Host.
            type: str
            returned: always
            sample: [{"id": "/subscriptions/subId/resourceGroups/myResourceGroup/providers/Microsoft.Compute/virtualMachines/vm1"}]
'''

from ansible.module_utils.basic import _load_params
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase, \
    normalize_location_name

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDedicatedHost(AzureRMModuleBase):

    def __init__(self):

        _load_params()
        # define user inputs from playbook
        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            host_group_name=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str'),
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(type='str')
                )
            ),
            platform_fault_domain=dict(type='int', choices=[0]),
            auto_replace_on_failure=dict(type='bool', default=True),
            license_type=dict(type='str', choices=['None', 'Windows_Server_Hybrid', 'Windows_Server_Perpetual']),
            state=dict(choices=['present', 'absent'], default='present', type='str'),
            is_restart=dict(type='bool', default=False)
        )

        self.results = dict(
            changed=False,
            state=dict()
        )

        self.resource_group = None
        self.host_group_name = None
        self.name = None
        self.state = None
        self.location = None
        self.tags = None
        self.sku = None
        self.platform_fault_domain = None
        self.auto_replace_on_failure = None
        self.license_type = None
        self.is_restart = None

        super(AzureRMDedicatedHost, self).__init__(self.module_arg_spec,
                                                   supports_tags=True,
                                                   supports_check_mode=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        changed = False

        # retrieve resource group to make sure it exists
        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        self.location = normalize_location_name(self.location)
        results = self.get_resource()

        if results is not None:
            if self.state == 'present':
                update_tags, self.tags = self.update_tags(results['tags'])
                if update_tags:
                    changed = True
                elif self.auto_replace_on_failure is not None and bool(self.auto_replace_on_failure) != bool(results['auto_replace_on_failure']):
                    changed = True
                elif self.platform_fault_domain and self.platform_fault_domain != results['platform_fault_domain']:
                    changed = True
                elif self.sku and self.sku['name'] != results['sku']['name']:
                    changed = True
                elif self.license_type and self.license_type != results['license_type']:
                    changed = True
                if not self.check_mode and changed:
                    results = self.update_dedicatedhost()
            else:
                changed = True
                if not self.check_mode:
                    results = self.delete_dedicatedhost()
        else:
            if self.state == 'present':
                changed = True
                if not self.check_mode:
                    results = self.create_dedicatedhost()
            else:
                self.log("The dedecated host not exist")
                changed = False

        if results is not None and self.is_restart:
            self.log("Restart the dedicated host. The operation will complete successfully once the dedicated host has restarted and is running.")
            changed = True
            if not self.check_mode:
                self.restart_dedicatedhost()

        self.results['changed'] = changed
        self.results['state'] = results
        return self.results

    def get_resource(self):
        self.log('Get host facts for {0}'.format(self.name))
        # get specific host group
        try:
            response = self.compute_client.dedicated_hosts.get(self.resource_group, self.host_group_name, self.name)
        except ResourceNotFoundError:
            return None

        return self.host_to_dict(response)

    def create_dedicatedhost(self):
        try:
            # create the dedicated host
            response = self.compute_client.dedicated_hosts.begin_create_or_update(resource_group_name=self.resource_group,
                                                                                  host_group_name=self.host_group_name,
                                                                                  host_name=self.name,
                                                                                  parameters=dict(location=self.location,
                                                                                                  sku=self.sku,
                                                                                                  tags=self.tags,
                                                                                                  platform_fault_domain=self.platform_fault_domain,
                                                                                                  auto_replace_on_failure=self.auto_replace_on_failure,
                                                                                                  license_type=self.license_type))
            if isinstance(response, LROPoller):
                return self.host_to_dict(self.get_poller_result(response))
        except Exception as exc:
            self.fail("Error creating or updating host {0} - {1}".format(self.name, str(exc)))

    def update_dedicatedhost(self):
        try:
            # update the dedicated host
            response = self.compute_client.dedicated_hosts.begin_update(resource_group_name=self.resource_group,
                                                                        host_group_name=self.host_group_name,
                                                                        host_name=self.name,
                                                                        parameters=dict(sku=self.sku,
                                                                                        tags=self.tags,
                                                                                        platform_fault_domain=self.platform_fault_domain,
                                                                                        auto_replace_on_failure=self.auto_replace_on_failure,
                                                                                        license_type=self.license_type))
            if isinstance(response, LROPoller):
                return self.host_to_dict(self.get_poller_result(response))
        except Exception as exc:
            self.fail("Error creating or updating host {0} - {1}".format(self.name, str(exc)))

    def restart_dedicatedhost(self):
        try:
            # restart the dedicate host
            response = self.compute_client.dedicated_hosts.begin_restart(resource_group_name=self.resource_group,
                                                                         host_group_name=self.host_group_name,
                                                                         host_name=self.name)
            if isinstance(response, LROPoller):
                return self.get_poller_result(response)
        except Exception as exc:
            self.fail("Error restarting host {0} - {1}".format(self.name, str(exc)))

    def delete_dedicatedhost(self):
        try:
            # delete the dedicated host
            response = self.compute_client.dedicated_hosts.begin_delete(resource_group_name=self.resource_group,
                                                                        host_group_name=self.host_group_name,
                                                                        host_name=self.name)
            if isinstance(response, LROPoller):
                return self.get_poller_result(response)

        except Exception as exc:
            self.fail("Error deleting host {0} - {1}".format(self.name, str(exc)))

    def host_to_dict(self, host):
        result = dict(
            resource_group=self.resource_group,
            host_group_name=self.host_group_name,
            id=host.id,
            name=host.name,
            location=host.location,
            tags=host.tags,
            sku=dict(),
            auto_replace_on_failure=host.auto_replace_on_failure,
            license_type=host.license_type,
            provisioning_state=host.provisioning_state,
            platform_fault_domain=host.platform_fault_domain,
            virtual_machines=[]
        )
        if host.virtual_machines:
            result['virtual_machines'] = [dict(id=item.id) for item in host.virtual_machines]

        if host.sku:
            result['sku']['name'] = host.sku.name
        return result


def main():
    AzureRMDedicatedHost()


if __name__ == '__main__':
    main()
