#!/usr/bin/python
#
# Copyright (c) 2023 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_sshpublickey
version_added: "2.0.0"
short_description: Manage ssh public key with vm
description:
    - Create, update or delete the vm public key.
options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    location:
        description:
            - Valid Azure location. Defaults to location of the resource group.
        type: str
    name:
        description:
            - The name of the SSH public key.
        required: true
        type: str
    public_key:
        description:
            - SSH public key used to authenticate to a virtual machine through ssh.
            - If this property is not initially provided when the resource is created, the publicKey property will be populated when generateKeyPair is called.
            - If the public key is provided upon resource creation, the provided public key needs to be at least 2048-bit and in ssh-rsa format.
        type: str
    state:
        description:
            - State of the SSH Public Key. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Create a SSH Public Key
  azure_rm_sshpublickey:
    resource_group: myResourceGroup
    name: mySshPublicKey
    public_key: "ssh-rsa ****************************@test.com"
    tags:
      testing: testing
      delete: on-exit

- name: Generate a pair SSH Public Key
  azure_rm_sshpublickey:
    resource_group: myResourceGroup
    name: mySshPublicKey
    tags:
      testing: testing
      delete: on-exit

- name: Delete a SSH Public Key
  azure_rm_sshpublickey:
    resource_group: myResourceGroup
    name: mySshPublicKey
    state: absent
'''
RETURN = '''
state:
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
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMSshPublicKey(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            public_key=dict(type='str'),
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None
        self.public_key = None

        self.body = dict()

        self.results = dict(
            changed=False,
            state=dict()
        )

        super(AzureRMSshPublicKey, self).__init__(self.module_arg_spec,
                                                  supports_tags=True,
                                                  supports_check_mode=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])
            for key in ['tags', 'public_key']:
                self.body[key] = kwargs[key]

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        changed = False
        results = dict()

        old_response = self.get_by_name()

        if old_response is not None:
            if self.state == 'present':
                update_tags, self.body['tags'] = self.update_tags(old_response['tags'])
                if update_tags or self.body['public_key'] is not None and self.body['public_key'] != old_response['public_key']:
                    changed = True
                    if not self.check_mode:
                        results = self.update_ssh_public_key(self.body)
                else:
                    results = old_response
            else:
                changed = True
                if not self.check_mode:
                    results = self.delete_ssh_public_key()
        else:
            if self.state == 'present':
                changed = True
                if not self.check_mode:
                    self.body['location'] = self.location
                    results = self.create_ssh_public_key(self.body)
            else:
                changed = False
                self.log("The SSH Public Key is not exists")

        self.results['changed'] = changed
        self.results['state'] = results

        return self.results

    def get_by_name(self):
        response = None
        try:
            response = self.compute_client.ssh_public_keys.get(self.resource_group, self.name)

        except ResourceNotFoundError as exec:
            self.log("Failed to get ssh public keys, Exception as {0}".format(exec))

        return self.to_dict(response)

    def create_ssh_public_key(self, body):
        response = None
        try:
            if body.get('public_key') is None:
                response = self.to_dict(self.compute_client.ssh_public_keys.create(self.resource_group, self.name, body))
                response.update(self.to_dict(self.compute_client.ssh_public_keys.generate_key_pair(self.resource_group, self.name)))
            else:
                response = self.to_dict(self.compute_client.ssh_public_keys.create(self.resource_group, self.name, body))
        except Exception as exc:
            self.fail("Error creating SSH Public Key {0} - {1}".format(self.name, str(exc)))

        return response

    def update_ssh_public_key(self, body):
        response = None
        try:
            response = self.compute_client.ssh_public_keys.update(self.resource_group, self.name, body)
        except Exception as exc:
            self.fail("Error updating SSH Public Key {0} - {1}".format(self.name, str(exc)))
        return self.to_dict(response)

    def delete_ssh_public_key(self):
        try:
            self.compute_client.ssh_public_keys.delete(self.resource_group, self.name)
        except Exception as exc:
            self.fail("Error deleting SSH Public Key {0} - {1}".format(self.name, str(exc)))

    def to_dict(self, body):
        results = None
        if body is not None:
            if hasattr(body, 'private_key'):
                results = dict(
                    private_key=body.private_key,
                    id=body.id,
                    public_key=body.public_key
                )
            else:
                results = dict(
                    id=body.id,
                    name=body.name,
                    location=body.location,
                    tags=body.tags,
                    public_key=body.public_key
                )
        return results


def main():
    AzureRMSshPublicKey()


if __name__ == '__main__':
    main()
