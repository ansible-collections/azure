#!/usr/bin/python
#
# Copyright (c) 2017 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_containerinstance_info
version_added: "0.1.2"
short_description: Get Azure Container Instance facts
description:
    - Get facts of Container Instance.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: True
    name:
        description:
            - The name of the container instance.
        type: str
    tags:
        description:
            - Limit results by providing of tags. Format tags 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Zim Kalinowski (@zikalino)

'''

EXAMPLES = '''
  - name: Get specific Container Instance facts
    azure_rm_containerinstance_info:
      resource_group: myResourceGroup
      name: myContainer

  - name: List Container Instances in a specified resource group name
    azure_rm_containerinstance_info:
      resource_group: myResourceGroup
      tags:
        - key
        - key:value
'''

RETURN = '''
container_groups:
    description: A list of Container Instance dictionaries.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource id.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.ContainerInstance/contain
                     erGroups/myContainer"
        resource_group:
            description:
                - Resource group where the container exists.
            returned: always
            type: str
            sample: testrg
        name:
            description:
                - The resource name.
            returned: always
            type: str
            sample: mycontainers
        location:
            description:
                - The resource location.
            returned: always
            type: str
            sample: westus
        os_type:
            description:
                - The OS type of containers.
            returned: always
            type: str
            sample: linux
        ip_address:
            description:
                - IP address of the container instance.
            returned: always
            type: str
            sample: 173.15.18.1
        dns_name_label:
            description:
                - The Dns name label for the IP.
            returned: always
            type: str
            sample: mydomain
        ports:
            description:
                - List of ports exposed by the container instance.
            returned: always
            type: list
            sample: [ 80, 81 ]
        containers:
            description:
                - The containers within the container group.
            returned: always
            type: complex
            sample: containers
            contains:
                name:
                    description:
                        - The name of the container instance.
                    returned: always
                    type: str
                    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.ContainerInstance
                             /containerGroups/myContainer"
                image:
                    description:
                        - The container image name.
                    returned: always
                    type: str
                    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.ContainerInstance
                             /containerGroups/myContainer"
                memory:
                    description:
                        - The required memory of the containers in GB.
                    returned: always
                    type: float
                    sample: 1.5
                cpu:
                    description:
                        - The required number of CPU cores of the containers.
                    returned: always
                    type: int
                    sample: 1
                ports:
                    description:
                        - List of ports exposed within the container group.
                    returned: always
                    type: list
                    sample: [ 80, 81 ]
                commands:
                    description:
                        - List of commands to execute within the container instance in exec form.
                    returned: always
                    type: list
                    sample: [ "pip install abc" ]
                volume_mounts:
                    description:
                        - The list of volumes mounted in container instance
                    returned: If volumes mounted in container instance
                    type: list
                    sample: [
                        {
                            "mount_path": "/mnt/repo",
                            "name": "myvolume1"
                        }
                    ]
                environment_variables:
                    description:
                        - List of container environment variables.
                    type: complex
                    contains:
                        name:
                            description:
                                - Environment variable name.
                            type: str
                        value:
                            description:
                                - Environment variable value.
                            type: str
        volumes:
            description: The list of Volumes that can be mounted by container instances
            returned: If container group has volumes
            type: list
            sample: [
                {
                    "git_repo": {
                        "repository": "https://github.com/Azure-Samples/aci-helloworld.git"
                    },
                    "name": "myvolume1"
                }
            ]
        tags:
            description: Tags assigned to the resource. Dictionary of string:string pairs.
            type: dict
            sample: { "tag1": "abc" }
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _camel_to_snake

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMContainerInstanceInfo(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            tags=dict(
                type='list',
                elements='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
        )
        self.resource_group = None
        self.name = None
        self.tags = None

        super(AzureRMContainerInstanceInfo, self).__init__(self.module_arg_spec,
                                                           supports_check_mode=True,
                                                           supports_tags=False,
                                                           facts_module=True)

    def exec_module(self, **kwargs):

        is_old_facts = self.module._name == 'azure_rm_containerinstance_facts'
        if is_old_facts:
            self.module.deprecate("The 'azure_rm_containerinstance_facts' module has been renamed to 'azure_rm_containerinstance_info'", version=(2.9, ))

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if (self.name is not None):
            self.results['containerinstances'] = self.get()
        elif (self.resource_group is not None):
            self.results['containerinstances'] = self.list_by_resource_group()
        else:
            self.results['containerinstances'] = self.list_all()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.containerinstance_client.container_groups.get(resource_group_name=self.resource_group,
                                                                          container_group_name=self.name)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError as e:
            self.log('Could not get facts for Container Instances.')

        if response is not None and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.containerinstance_client.container_groups.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.fail('Could not list facts for Container Instances.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_all(self):
        response = None
        results = []
        try:
            response = self.containerinstance_client.container_groups.list()
            self.log("Response : {0}".format(response))
        except Exception as e:
            self.fail('Could not list facts for Container Instances.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        containers = d['containers']
        ports = d['ip_address']['ports'] if 'ip_address' in d else []
        resource_group = d['id'].split('resourceGroups/')[1].split('/')[0]

        for port_index in range(len(ports)):
            ports[port_index] = ports[port_index]['port']

        for container_index in range(len(containers)):
            old_container = containers[container_index]
            new_container = {
                'name': old_container['name'],
                'image': old_container['image'],
                'memory': old_container['resources']['requests']['memory_in_gb'],
                'cpu': old_container['resources']['requests']['cpu'],
                'ports': [],
                'commands': old_container.get('command'),
                'environment_variables': old_container.get('environment_variables'),
                'volume_mounts': []
            }
            for port_index in range(len(old_container['ports'])):
                new_container['ports'].append(old_container['ports'][port_index]['port'])
            if 'volume_mounts' in old_container:
                for volume_mount_index in range(len(old_container['volume_mounts'])):
                    new_container['volume_mounts'].append(old_container['volume_mounts'][volume_mount_index])
            containers[container_index] = new_container

        d = {
            'id': d['id'],
            'resource_group': resource_group,
            'name': d['name'],
            'os_type': d['os_type'],
            'dns_name_label': d['ip_address'].get('dns_name_label'),
            'ip_address': d['ip_address']['ip'] if 'ip_address' in d else '',
            'ports': ports,
            'location': d['location'],
            'containers': containers,
            'restart_policy': _camel_to_snake(d.get('restart_policy')) if d.get('restart_policy') else None,
            'tags': d.get('tags', None),
            'volumes': d['volumes'] if 'volumes' in d else []
        }
        return d


def main():
    AzureRMContainerInstanceInfo()


if __name__ == '__main__':
    main()
