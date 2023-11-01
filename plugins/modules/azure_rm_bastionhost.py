#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_bastionhost

version_added: "1.13.0"

short_description: Managed bastion host resource

description:
    - Create, Update or Delete bastion host resource.

options:
    name:
        description:
            - The name of the bastion host.
        type: str
        required: True
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: True
    location:
        description:
            - The resource location.
        type: str
    sku:
        description:
            - The sku of this Bastion Host.
        type: dict
        suboptions:
            name:
                description:
                    - The name of the SKU.
                type: str
                choices:
                    - Standard
                    - Basic
    enable_tunneling:
        description:
            - Enable or Disable Tunneling feature of the Bastion Host resource.
        type: bool
    enable_shareable_link:
        description:
            - Enable or Disable Shareable Link of the Bastion Host resource.
        type: bool
    enable_ip_connect:
        description:
            - Enable or Disable IP Connect feature of the Bastion Host resource.
        type: bool
    enable_file_copy:
        description:
            - Enable or Disable File Copy feature of the Bastion Host resource.
        type: bool
    scale_units:
        description:
            - The scale units for the Bastion Host resource.
        type: int
    disable_copy_paste:
        description:
            - Enable or Disable Copy or Paste feature of the Bastion Host resource.
        type: bool
    ip_configurations:
        description:
            - An array of bastion host IP configurations.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of bastion host ip configuration.
                type: str
            subnet:
                description:
                    - Reference of the subnet resource.
                type: dict
                suboptions:
                    id:
                        description:
                            - The ID of the Subnet.
                        type: str
            public_ip_address:
                description:
                    - Reference of the PublicIP resource.
                type: dict
                suboptions:
                    id:
                        description:
                            - The ID of the public IP.
                        type: str
            private_ip_allocation_method:
                description:
                    - Private IP allocation method.
                type: str
                choices:
                    - Static
                    - Dynamic
    state:
        description:
            - Assert the state of the pirvate link service.
            - Use I(state=present) to create or update the link service and I(state=absent) to delete it.
        type: str
        default: present
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Create bastion host info
  azure_rm_bastionhost:
    name: bastion-name
    resource_group: myResourceGroup
    ip_configurations:
      - name: testip_configuration
        subnet:
          id: "{{ subnet_output.state.id }}"
        public_ip_address:
          id: "{{ publicIP_output.publicipaddresses[0].id }}"
        private_ip_allocation_method: Dynamic
    sku:
      name: Standard
    enable_tunneling: false
    enable_shareable_link: false
    enable_ip_connect: false
    enable_file_copy: false
    scale_units: 6
    disable_copy_paste: false
    tags:
      key1: value1

- name: Create bastion host info
  azure_rm_bastionhost:
    name: bastion-name
    resource_group: myResourceGroup
    state: absent
'''

RETURN = '''
bastion_host:
    description:
        - List of Azure bastion host info.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID of the Azure bastion host.
            sample: "/subscriptions/xxx-xxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/bastionHosts/testbastion"
            returned: always
            type: str
        name:
            description:
                - Name of the Azure bastion host.
            returned: always
            type: str
            sample: linkservice
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: eastus
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            type: str
            returned: always
            sample: "fb0e3a90-6afa-4a01-9171-9c84d144a0f3"
        type:
            description:
                - The resource type.
            type: str
            returned: always
            sample: Microsoft.Network/bastionHosts
        tags:
            description:
                - The resource tags.
            type: list
            returned: always
            sample: { 'key1': 'value1' }
        provisioning_state:
            description:
                - The provisioning state of the bastion host resource.
            type: str
            returned: always
            sample: Succeeded
        scale_units:
            description:
                - The scale units for the Bastion Host resource.
            type: int
            returned: always
            sample: 2
        enable_tunneling:
            description:
                - Enable/Disable Tunneling feature of the Bastion Host resource.
            type: bool
            returned: always
            sample: False
        enable_shareable_link:
            description:
                - Enable/Disable Shareable Link of the Bastion Host resource.
            type: bool
            returned: always
            sample: False
        enable_ip_connect:
            description:
                - Enable/Disable IP Connect feature of the Bastion Host resource.
            type: bool
            returned: always
            sample: False
        enable_file_copy:
            description:
                - Enable/Disable File Copy feature of the Bastion Host resource.
            type: bool
            returned: always
            sample: False
        dns_name:
            description:
                - FQDN for the endpoint on which bastion host is accessible.
            type: str
            returned: always
            sample: bst-0ca1e1b6-9969-4167-be54-5972e1395c25.bastion.azure.com
        disable_copy_paste:
            description:
                - Enable/Disable Copy/Paste feature of the Bastion Host resource.
            type: bool
            returned: always
            sample: False
        sku:
            description:
                - The sku of this Bastion Host.
            type: complex
            returned: always
            contains:
                name:
                    description:
                        -  The name of this Bastion Host.
                    type: str
                    returned: always
                    sample: Standard
        ip_configurations:
            description:
                - An array of bastion host IP configurations.
            type: complex
            returned: always
            contains:
                name:
                    description:
                        - Name of the resource that is unique within a resource group.
                        - This name can be used to access the resource.
                    type: str
                    returned: always
                    sample: IpConf
                private_ip_allocation_method:
                    description:
                        - Private IP allocation method.
                    type: str
                    returned: always
                    sample: Static
                public_ip_address:
                    description:
                        - Reference of the PublicIP resource.
                    type: complex
                    returned: always
                    contains:
                        id:
                            description:
                                - The ID of the public IP address.
                            returned: always
                            type: str
                            sample: "/subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Network/publicIPAddresses/Myip"
                subnet:
                    description:
                        - The reference to the subnet resource.
                    returned: always
                    type: str
                    contains:
                        id:
                            description:
                                - The ID of the subnet..
                            returned: always
                            type: str
                            sample:  "/subscriptions/xxx-xxx/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/vnet/subnets/AzureBastionSubnet"
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass


from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


sku_spec = dict(
    name=dict(type='str', choices=['Standard', 'Basic'])
)

subnet_spec = dict(
    id=dict(type='str')
)

public_ip_address_spec = dict(
    id=dict(type='str')
)


class AzureRMBastionHost(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type="str", required=True),
            resource_group=dict(type="str", required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            ip_configurations=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(type='str'),
                    subnet=dict(type='dict', options=subnet_spec),
                    public_ip_address=dict(type='dict', options=public_ip_address_spec),
                    private_ip_allocation_method=dict(type='str', choices=['Static', 'Dynamic'])
                )
            ),
            sku=dict(type='dict', options=sku_spec),
            enable_tunneling=dict(type='bool'),
            enable_shareable_link=dict(type='bool'),
            enable_ip_connect=dict(type='bool'),
            enable_file_copy=dict(type='bool'),
            scale_units=dict(type='int'),
            disable_copy_paste=dict(type='bool')
        )

        self.name = None
        self.resource_group = None
        self.location = None
        self.tags = None
        self.state = None
        self.results = dict(
            changed=False,
        )
        self.body = {}

        super(AzureRMBastionHost, self).__init__(self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True,
                                                 facts_module=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        old_response = self.get_item()
        result = None
        changed = False

        if not self.location:
            resource_group = self.get_resource_group(self.resource_group)
            self.location = resource_group.location

        self.body['location'] = self.location
        self.body['tags'] = self.tags

        if self.state == 'present':
            if old_response:
                update_tags, tags = self.update_tags(old_response['tags'])
                if update_tags:
                    changed = True
                self.body['tags'] = tags

                if self.body.get('disable_copy_paste') is not None:
                    if bool(self.body.get('disable_copy_paste')) != bool(old_response['disable_copy_paste']):
                        changed = True
                else:
                    self.body['disable_copy_paste'] = old_response['disable_copy_paste']

                if self.body.get('enable_file_copy') is not None:
                    if bool(self.body.get('enable_file_copy')) != bool(old_response['enable_file_copy']):
                        changed = True
                else:
                    self.body['enable_file_copy'] = old_response['enable_file_copy']

                if self.body.get('enable_ip_connect') is not None:
                    if bool(self.body.get('enable_ip_connect')) != bool(old_response['enable_ip_connect']):
                        changed = True
                else:
                    self.body['enable_ip_connect'] = old_response['enable_ip_connect']

                if self.body.get('enable_shareable_link') is not None:
                    if bool(self.body.get('enable_shareable_link')) != bool(old_response['enable_shareable_link']):
                        changed = True
                else:
                    self.body['enable_shareable_link'] = old_response['enable_shareable_link']

                if self.body.get('enable_tunneling') is not None:
                    if bool(self.body.get('enable_tunneling')) != bool(old_response['enable_tunneling']):
                        changed = True
                else:
                    self.body['enable_tunneling'] = old_response['enable_tunneling']

                if self.body.get('scale_units') is not None:
                    if self.body.get('scale_units') != old_response['scale_units']:
                        changed = True
                else:
                    self.body['scale_units'] = old_response['scale_units']

                if self.body.get('sku') is not None:
                    if self.body.get('sku') != old_response['sku']:
                        changed = True
                else:
                    self.body['sku'] = old_response['sku']

                if self.body.get('ip_configurations') is not None:
                    if self.body['ip_configurations'] != old_response['ip_configurations']:
                        self.fail("Bastion Host IP configuration not support to update!")
                else:
                    self.body['ip_configurations'] = old_response['ip_configurations']
            else:
                changed = True

            if changed:
                if self.check_mode:
                    self.log("Check mode test. The bastion host is exist, will be create or updated")
                else:
                    result = self.create_or_update(self.body)
            else:
                if self.check_mode:
                    self.log("Check mode test. The Azure Bastion Host is exist, No operation in this task")
                else:
                    self.log("The Azure Bastion Host is exist, No operation in this task")
                    result = old_response
        else:
            if old_response:
                changed = True
                if self.check_mode:
                    self.log("Check mode test. The bastion host is exist, will be deleted")
                else:
                    result = self.delete_resource()
            else:
                if self.check_mode:
                    self.log("The bastion host isn't exist, no action")
                else:
                    self.log("The bastion host isn't exist, don't need to delete")

        self.results["bastion_host"] = result
        self.results['changed'] = changed
        return self.results

    def get_item(self):
        self.log("Get properties for {0} in {1}".format(self.name, self.resource_group))
        try:
            response = self.network_client.bastion_hosts.get(self.resource_group, self.name)
            return self.bastion_to_dict(response)
        except ResourceNotFoundError:
            self.log("Could not get info for {0} in {1}".format(self.name, self.resource_group))

        return []

    def create_or_update(self, parameters):
        self.log("Create or update the bastion host for {0} in {1}".format(self.name, self.resource_group))
        try:
            response = self.network_client.bastion_hosts.begin_create_or_update(self.resource_group, self.name, parameters)

            result = self.network_client.bastion_hosts.get(self.resource_group, self.name)
            return self.bastion_to_dict(result)
        except Exception as ec:
            self.fail("Create or Update {0} in {1} failed, mesage {2}".format(self.name, self.resource_group, ec))

        return []

    def delete_resource(self):
        self.log("delete the bastion host for {0} in {1}".format(self.name, self.resource_group))
        try:
            response = self.network_client.bastion_hosts.begin_delete(self.resource_group, self.name)
        except Exception as ec:
            self.fail("Delete {0} in {1} failed, message {2}".format(self.name, self.resource_group, ec))

        return []

    def bastion_to_dict(self, bastion_info):
        bastion = bastion_info.as_dict()
        result = dict(
            id=bastion.get("id"),
            name=bastion.get('name'),
            type=bastion.get('type'),
            etag=bastion.get('etag'),
            location=bastion.get('location'),
            tags=bastion.get('tags'),
            sku=dict(),
            ip_configurations=list(),
            dns_name=bastion.get('dns_name'),
            provisioning_state=bastion.get('provisioning_state'),
            scale_units=bastion.get('scale_units'),
            disable_copy_paste=bastion.get('disable_copy_paste'),
            enable_file_copy=bastion.get('enable_file_copy'),
            enable_ip_connect=bastion.get('enable_ip_connect'),
            enable_shareable_link=bastion.get('enable_tunneling'),
            enable_tunneling=bastion.get('enable_tunneling')
        )

        if bastion.get('sku'):
            result['sku']['name'] = bastion['sku']['name']

        if bastion.get('ip_configurations'):
            for items in bastion['ip_configurations']:
                result['ip_configurations'].append(
                    {
                        "name": items['name'],
                        "subnet": dict(id=items['subnet']['id']),
                        "public_ip_address": dict(id=items['public_ip_address']['id']),
                        "private_ip_allocation_method": items['private_ip_allocation_method'],
                    }
                )
        return result


def main():
    AzureRMBastionHost()


if __name__ == "__main__":
    main()
