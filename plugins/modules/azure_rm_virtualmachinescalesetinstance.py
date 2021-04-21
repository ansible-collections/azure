#!/usr/bin/python
#
# Copyright (c) 2019 Zim Kalinowski, (@zikalino)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_virtualmachinescalesetinstance
version_added: "0.1.2"
short_description: Get Azure Virtual Machine Scale Set Instance facts
description:
    - Get facts of Azure Virtual Machine Scale Set VMs.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    vmss_name:
        description:
            - The name of the VM scale set.
        required: True
    instance_id:
        description:
            - The instance ID of the virtual machine.
        required: True
    latest_model:
        type: bool
        description:
            - Set to C(yes) to upgrade to the latest model.
    power_state:
        description:
            - Use this option to change power state of the instance.
        choices:
            - 'running'
            - 'stopped'
            - 'deallocated'
    protect_from_scale_in:
        type: bool
        description:
            - turn on/off instance protection from scale in
    protect_from_scale_set_actions:
        type: bool
        description:
            - tun on/off instance protection from scale set actions
    state:
        description:
            - State of the VMSS instance. Use C(present) to update an instance and C(absent) to delete an instance.
        default: present
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zim Kalinowski (@zikalino)

'''

EXAMPLES = '''
  - name: Upgrade instance to the latest image
    azure_rm_virtualmachinescalesetinstance:
      resource_group: myResourceGroup
      vmss_name: myVMSS
      instance_id: "2"
      latest_model: yes

  - name: Turn on protect from scale in
    azure_rm_virtualmachinescalesetinstance:
        resource_group: myResourceGroup
        vmss_name: myVMSS
        instance_id: "2"
        protect_from_scale_in: true
'''

RETURN = '''
instances:
    description:
        - A list of instances.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Instance resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/TestGroup/providers/Microsoft.Compute/scalesets/myscaleset/vms/myvm
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.compute import ComputeManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVirtualMachineScaleSetInstance(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            vmss_name=dict(
                type='str',
                required=True
            ),
            instance_id=dict(
                type='str'
            ),
            latest_model=dict(
                type='bool'
            ),
            power_state=dict(
                type='str',
                choices=['running', 'stopped', 'deallocated']
            ),
            protect_from_scale_in=dict(
                type='bool'
            ),
            protect_from_scale_set_actions=dict(
                type='bool'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.vmss_name = None
        self.instance_id = None
        self.latest_model = None
        self.power_state = None
        self.state = None
        self.protect_from_scale_in = None
        self.protect_from_scale_set_actions = None
        super(AzureRMVirtualMachineScaleSetInstance, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2019-07-01')

        instances = self.get()

        if self.state == 'absent':
            for item in instances:
                if not self.check_mode:
                    self.delete(item['instance_id'])
                self.results['changed'] = True
            self.results['instances'] = []
        else:
            if self.latest_model is not None:
                for item in instances:
                    if not item.get('latest_model', None):
                        if not self.check_mode:
                            self.apply_latest_model(item['instance_id'])
                        item['latest_model'] = True
                        self.results['changed'] = True

            if self.power_state is not None:
                for item in instances:
                    if self.power_state == 'stopped' and item['power_state'] not in ['stopped', 'stopping']:
                        if not self.check_mode:
                            self.stop(item['instance_id'])
                        self.results['changed'] = True
                    elif self.power_state == 'deallocated' and item['power_state'] not in ['deallocated']:
                        if not self.check_mode:
                            self.deallocate(item['instance_id'])
                        self.results['changed'] = True
                    elif self.power_state == 'running' and item['power_state'] not in ['running']:
                        if not self.check_mode:
                            self.start(item['instance_id'])
                        self.results['changed'] = True
            if self.protect_from_scale_in is not None or self.protect_from_scale_set_actions is not None:
                for item in instances:
                    protection_policy = item['protection_policy']
                    if protection_policy is None or self.protect_from_scale_in != protection_policy['protect_from_scale_in'] or \
                            self.protect_from_scale_set_actions != protection_policy['protect_from_scale_set_actions']:
                        if not self.check_mode:
                            self.update_protection_policy(self.instance_id, self.protect_from_scale_in, self.protect_from_scale_set_actions)
                        self.results['changed'] = True

        self.results['instances'] = [{'id': item['id']} for item in instances]
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.virtual_machine_scale_set_vms.get(resource_group_name=self.resource_group,
                                                                          vm_scale_set_name=self.vmss_name,
                                                                          instance_id=self.instance_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Virtual Machine Scale Set VM.')

        if response:
            results.append(self.format_response(response))

        return results

    def apply_latest_model(self, instance_id):
        try:
            poller = self.compute_client.virtual_machine_scale_sets.update_instances(resource_group_name=self.resource_group,
                                                                                     vm_scale_set_name=self.vmss_name,
                                                                                     instance_ids=[instance_id])
            self.get_poller_result(poller)
        except CloudError as exc:
            self.log("Error applying latest model {0} - {1}".format(self.vmss_name, str(exc)))
            self.fail("Error applying latest model {0} - {1}".format(self.vmss_name, str(exc)))

    def delete(self, instance_id):
        try:
            self.mgmt_client.virtual_machine_scale_set_vms.delete(resource_group_name=self.resource_group,
                                                                  vm_scale_set_name=self.vmss_name,
                                                                  instance_id=instance_id)
        except CloudError as e:
            self.log('Could not delete instance of Virtual Machine Scale Set VM.')
            self.fail('Could not delete instance of Virtual Machine Scale Set VM.')

    def start(self, instance_id):
        try:
            self.mgmt_client.virtual_machine_scale_set_vms.start(resource_group_name=self.resource_group,
                                                                 vm_scale_set_name=self.vmss_name,
                                                                 instance_id=instance_id)
        except CloudError as e:
            self.log('Could not start instance of Virtual Machine Scale Set VM.')
            self.fail('Could not start instance of Virtual Machine Scale Set VM.')

    def stop(self, instance_id):
        try:
            self.mgmt_client.virtual_machine_scale_set_vms.power_off(resource_group_name=self.resource_group,
                                                                     vm_scale_set_name=self.vmss_name,
                                                                     instance_id=instance_id)
        except CloudError as e:
            self.log('Could not stop instance of Virtual Machine Scale Set VM.')
            self.fail('Could not stop instance of Virtual Machine Scale Set VM.')

    def deallocate(self, instance_id):
        try:
            self.mgmt_client.virtual_machine_scale_set_vms.deallocate(resource_group_name=self.resource_group,
                                                                      vm_scale_set_name=self.vmss_name,
                                                                      instance_id=instance_id)
        except CloudError as e:
            self.log('Could not deallocate instance of Virtual Machine Scale Set VM.')
            self.fail('Could not deallocate instance of Virtual Machine Scale Set VM.')

    def update_protection_policy(self, instance_id, protect_from_scale_in, protect_from_scale_set_actions):
        try:
            d = {}
            if protect_from_scale_in is not None:
                d['protect_from_scale_in'] = protect_from_scale_in
            if protect_from_scale_set_actions is not None:
                d['protect_from_scale_set_actions'] = protect_from_scale_set_actions
            protection_policy = self.compute_models.VirtualMachineScaleSetVMProtectionPolicy(**d)
            instance = self.mgmt_client.virtual_machine_scale_set_vms.get(resource_group_name=self.resource_group,
                                                                          vm_scale_set_name=self.vmss_name,
                                                                          instance_id=instance_id)
            instance.protection_policy = protection_policy
            poller = self.mgmt_client.virtual_machine_scale_set_vms.update(resource_group_name=self.resource_group,
                                                                           vm_scale_set_name=self.vmss_name,
                                                                           instance_id=instance_id,
                                                                           parameters=instance)
            self.get_poller_result(poller)
        except CloudError as e:
            self.log('Could not update instance protection policy.')
            self.fail('Could not update instance protection policy.')

    def format_response(self, item):
        d = item.as_dict()
        iv = self.mgmt_client.virtual_machine_scale_set_vms.get_instance_view(resource_group_name=self.resource_group,
                                                                              vm_scale_set_name=self.vmss_name,
                                                                              instance_id=d.get('instance_id', None)).as_dict()
        power_state = ""
        for index in range(len(iv['statuses'])):
            code = iv['statuses'][index]['code'].split('/')
            if code[0] == 'PowerState':
                power_state = code[1]
                break
        d = {
            'id': d.get('id'),
            'tags': d.get('tags'),
            'instance_id': d.get('instance_id'),
            'latest_model': d.get('latest_model_applied'),
            'power_state': power_state,
            'protection_policy': d.get('protection_policy')
        }
        return d


def main():
    AzureRMVirtualMachineScaleSetInstance()


if __name__ == '__main__':
    main()
