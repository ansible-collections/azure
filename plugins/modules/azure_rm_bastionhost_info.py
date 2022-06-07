#!/usr/bin/python
#
# Copyright (c) 2022 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_bastionhost_info

version_added: "1.13.0"

short_description: Get Azure bastion host info

description:
    - Get facts for Azure bastion host info.

options:
    name:
        description:
            - Name of the bastion host.
        type: str
    resource_group:
        description:
            - The name of the resource group.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get bastion host info by name
  azure_rm_bastionhost_info:
    name: bastion-name
    resource_group: myResourceGroup

- name: Get all bastion host by resource group
  azure_rm_bastionhost_info:
    resource_group: myResourceGroup

- name: Get all bastion hoste by subscription filter by tags
  azure_rm_bastionhost_info:
    tags:
      - key1
      - abc
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
                    type: complex
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


class AzureRMBastionHostInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type="str"),
            resource_group=dict(type="str"),
            tags=dict(type='list', elements='str')
        )

        self.name = None
        self.tags = None
        self.resource_group = None
        self.results = dict(
            changed=False,
        )

        super(AzureRMBastionHostInfo, self).__init__(self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=False,
                                                     facts_module=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name is not None and self.resource_group is not None:
            result = self.get_item()
        elif self.resource_group is not None:
            result = self.list_resourcegroup()
        else:
            result = self.list_by_subscription()

        self.results["bastion_host"] = [item for item in result if item and self.has_tags(item['tags'], self.tags)]
        return self.results

    def get_item(self):
        self.log("Get properties for {0} in {1}".format(self.name, self.resource_group))

        try:
            response = self.network_client.bastion_hosts.get(self.resource_group, self.name)
            return [self.bastion_to_dict(response)]
        except ResourceNotFoundError:
            self.log("Could not get info for {0} in {1}".format(self.name, self.resource_group))

        return []

    def list_resourcegroup(self):
        result = []
        self.log("List all in {0}".format(self.resource_group))
        try:
            response = self.network_client.bastion_hosts.list_by_resource_group(self.resource_group)
            while True:
                result.append(response.next())
        except StopIteration:
            pass
        except Exception:
            pass
        return [self.bastion_to_dict(item) for item in result]

    def list_by_subscription(self):
        result = []
        self.log("List all in by subscription")
        try:
            response = self.network_client.bastion_hosts.list()
            while True:
                result.append(response.next())
        except StopIteration:
            pass
        except Exception:
            pass
        return [self.bastion_to_dict(item) for item in result]

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
    AzureRMBastionHostInfo()


if __name__ == "__main__":
    main()
