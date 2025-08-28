#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_dedicatedhost_info

version_added: "3.8.0"

short_description: Retrieves information abount dedicated host

description:
    - Retrieves information about a dedicated host.
    - Lists all of the dedicated hosts in the specified dedicated host group.

options:
    resource_group:
        description:
            - Name of the resource group.
        type: str
        required: True
    host_group_name:
        description:
            - The name of the dedicated host group.
        type: str
        required: True
    name:
        description:
            - Name of the dedicate host.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - xuzhang3 (@xuzhang3)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: List facts for one dedicate host
  azure_rm_dedicatedhost_info:
    resource_group: myAzureResourceGroup
    host_group_name: myhostgroup

- name: Get facts for dedicate host
  azure_rm_dedicatedhost_info:
    resource_group: myAzureResourceGroup
    host_group_name: myhostgroup
    name: mydedicatehost
'''

RETURN = '''
dedicate_hosts:
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
            sample: None
        provisioning_state:
            description:
                - The provisioning state, which only appears in the response.
            type: str
            returned: always
            sample: Succeeded
        platform_fault_domain:
            description:
                - Fault domain of the dedicated host within a dedicated host group.
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

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'DedicateHostInfo'


class AzureRMDedicateHostInfo(AzureRMModuleBase):

    def __init__(self):

        # define user inputs into argument
        self.module_arg_spec = dict(
            name=dict(type='str'),
            host_group_name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            tags=dict(type='list', elements='str')
        )

        # store the results of the module operation
        self.results = dict(
            changed=False
        )

        self.name = None
        self.resource_group = None
        self.host_group_name = None
        self.tags = None

        super(AzureRMDedicateHostInfo, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=False, facts_module=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        results = []
        if self.name is not None:
            # if there is a host name provided, return facts about that dedicated host
            results = self.get_item()
        else:
            # all the host listed in specific host group
            results = self.list_by_host_group()

        self.results['dedicated_hosts'] = [self.host_to_dict(item) for item in results] if results else []

        return self.results

    def get_item(self):
        self.log('Get host facts for {0}'.format(self.name))
        results = []
        # get specific host group
        try:
            item = self.compute_client.dedicated_hosts.get(self.resource_group, self.host_group_name, self.name)
        except ResourceNotFoundError:
            return []

        # serialize result
        if item and self.has_tags(item.tags, self.tags):
            results = [item]
        return results

    def list_by_host_group(self):
        self.log('List all host for host group - {0}'.format(self.host_group_name))
        try:
            response = self.compute_client.dedicated_hosts.list_by_host_group(self.resource_group, self.host_group_name)
        except Exception:
            return []

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

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
    AzureRMDedicateHostInfo()


if __name__ == '__main__':
    main()
