#!/usr/bin/python
#
# Copyright (c) 2023 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_sshpublickey_info

version_added: "2.0.0"

short_description: Get Ssh Public Key with VM facts

description:
    - Get Ssh Public Key with VM facts

options:
    resource_group:
        description:
            - Name of the resource group.
        type: str
    name:
        description:
            - Name of the SSH Public Key.
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
- name: Get facts of the VM's ssh public key by name
  azure_rm_sshpublickey_info:
    resource_group: myResourceGroup
    name: mysshpublickey

- name: Get facts of the VM's ssh public key by resource group
  azure_rm_sshpublickey_info:
    resource_group: myResourceGroup

- name: Get facts by tags
  azure_rm_sshpublickey_info:
    resource_group: myResourceGroup
    tags:
      - testing
      - foo:bar
'''

RETURN = '''
ssh_keys:
    description:
        - Current state of the SSH Public Key.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/xxxx/resourceGroups/xxx/providers/Microsoft.Compute/sshPublicKeys/mySshPublicKeyName
        location:
            description:
                - The Geo-location where the resource lives.
            returned: always
            type: str
            sample: eastus
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: mySshPublicKey
        tags:
            description:
                - Resource tags, such as { 'tags1':'value1' }.
            returned: always
            type: dict
            sample: { 'key1':'value1' }
        public_key:
            description:
                - SSH public key used to authenticate to a virtual machine through ssh.
            returned: always
            type: str
            sample: "ssh-rsa **************@test.com"
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMSshPublicKeyInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.results = dict(
            changed=False,
            ssh_keys=[]
        )

        self.resource_group = None
        self.name = None
        self.tags = None

        super(AzureRMSshPublicKeyInfo, self).__init__(self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False,
                                                      facts_module=True)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name and self.resource_group:
            response = [self.get_by_name()]
        elif self.resource_group:
            response = self.list_by_resourcegroup()
        else:
            response = self.list_all()

        self.results['ssh_keys'] = [self.to_dict(item) for item in response if response is not None]

        return self.results

    def get_by_name(self):
        response = None
        try:
            response = self.compute_client.ssh_public_keys.get(self.resource_group, self.name)

        except ResourceNotFoundError as exec:
            self.log("Failed to get ssh public keys, Exception as {0}".format(exec))

        return response

    def list_by_resourcegroup(self):
        response = None
        try:
            response = self.compute_client.ssh_public_keys.list_by_resource_group(self.resource_group)
        except Exception as exec:
            self.log("Faild to list ssh public keys by resource group, exception as {0}".format(exec))
        return response

    def list_all(self):
        response = None
        try:
            response = self.compute_client.ssh_public_keys.list_by_subscription()
        except Exception as exc:
            self.fail("Failed to list all items - {0}".format(str(exc)))

        return response

    def to_dict(self, body):
        results = dict()
        if body is not None and self.has_tags(body.tags, self.tags):
            results = dict(
                id=body.id,
                name=body.name,
                location=body.location,
                tags=body.tags,
                public_key=body.public_key
            )
        return results


def main():
    AzureRMSshPublicKeyInfo()


if __name__ == '__main__':
    main()
