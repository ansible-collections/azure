#!/usr/bin/python
#
# Copyright (c) 2019 Zim Kalinowski, (@zikalino)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_snapshot
version_added: "0.1.2"
short_description: Manage Azure Snapshot instance
description:
    - Create, update and delete instance of Azure Snapshot.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - Resource name.
        required: true
        type: str
    location:
        description:
            - Resource location.
        type: str
    incremental:
        description:
            - Whether a snapshot is incremental.
            - Incremental snapshots on the same disk occupy less space than full snapshots and can be diffed.
        type: bool
        default: False
    sku:
        description:
            - The snapshots SKU.
        type: dict
        suboptions:
            name:
                description:
                    - The sku name.
                type: str
                choices:
                    - Standard_LRS
                    - Premium_LRS
                    - Standard_ZRS
            tier:
                description:
                    - The sku tier.
                type: str
    os_type:
        description:
            - The Operating System type.
        type: str
        choices:
            - Linux
            - Windows
            - linux
            - windows
    creation_data:
        description:
            - Disk source information.
            - CreationData information cannot be changed after the disk has been created.
        type: dict
        suboptions:
            create_option:
                description:
                    - This enumerates the possible sources of a disk's creation.
                type: str
                choices:
                    - Import
                    - Copy
            source_uri:
                description:
                    - If I(create_option=Import), this is the URI of a blob to be imported into a managed disk.
                type: str
            source_id:
                description:
                    - If I(create_option=Copy), this is the resource ID of a managed disk to be copied from.
                type: str
    state:
        description:
            - Assert the state of the Snapshot.
            - Use C(present) to create or update an Snapshot and C(absent) to delete it.
        default: present
        type: str
        choices:
          - absent
          - present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Zim Kalinowski (@zikalino)

'''

EXAMPLES = '''
- name: Create a snapshot by importing an unmanaged blob from the same subscription.
  azure_rm_snapshot:
    resource_group: myResourceGroup
    name: mySnapshot
    location: eastus
    creation_data:
      create_option: Import
      source_uri: 'https://mystorageaccount.blob.core.windows.net/osimages/osimage.vhd'

- name: Create a snapshot by copying an existing managed disk.
  azure_rm_snapshot:
    resource_group: myResourceGroup
    name: mySnapshot
    location: eastus
    creation_data:
      create_option: Copy
      source_id: '/subscriptions/sub123/resourceGroups/group123/providers/Microsoft.Compute/disks/disk123'
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Compute/snapshots/mySnapshot
'''

import time
import json
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMSnapshots(AzureRMModuleBaseExt):
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
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str',
                        choices=['Standard_LRS',
                                 'Premium_LRS',
                                 'Standard_ZRS']
                    ),
                    tier=dict(
                        type='str'
                    )
                )
            ),
            os_type=dict(
                type='str',
                choices=['Windows', 'linux',
                         'Linux', 'windows']
            ),
            incremental=dict(type='bool', default=False),
            creation_data=dict(
                type='dict',
                options=dict(
                    create_option=dict(
                        type='str',
                        choices=['Import', 'Copy'],
                    ),
                    source_uri=dict(
                        type='str'
                    ),
                    source_id=dict(
                        type='str'
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.id = None
        self.name = None
        self.type = None
        self.managed_by = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200, 201, 202]
        self.to_do = Actions.NoAction

        self.body = {}
        self.body['properties'] = dict()
        self.query_parameters = {}
        self.query_parameters['api-version'] = '2022-03-02'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(AzureRMSnapshots, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == 'incremental':
                    self.body['properties']['incremental'] = kwargs[key]
                elif key == 'os_type':
                    self.body['properties']['osType'] = kwargs[key]
                elif key == 'creation_data':
                    self.body['properties']['creationData'] = dict()
                    if kwargs[key].get('create_option') is not None:
                        self.body['properties']['creationData']['createOption'] = kwargs[key].get('create_option')
                        self.body['properties']['creationData']['sourceUri'] = kwargs[key].get('source_uri')
                        self.body['properties']['creationData']['sourceResourceId'] = kwargs[key].get('source_id')
                        if kwargs[key].get('source_uri') is not None:
                            self.query_parameters['api-version'] = '2019-03-01'
                else:
                    self.body[key] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if 'location' not in self.body:
            self.body['location'] = resource_group.location

        self.url = ('/subscriptions' +
                    '/{{ subscription_id }}' +
                    '/resourceGroups' +
                    '/{{ resource_group }}' +
                    '/providers' +
                    '/Microsoft.Compute' +
                    '/snapshots' +
                    '/{{ snapshot_name }}')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)
        self.url = self.url.replace('{{ resource_group }}', self.resource_group)
        self.url = self.url.replace('{{ snapshot_name }}', self.name)

        old_response = self.get_resource()

        if not old_response:
            self.log("Snapshot instance doesn't exist")

            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log('Snapshot instance already exists')

            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                if self.body.get('sku') is not None and \
                   not all(self.body['sku'][item] == old_response['sku'].get(item) for item in self.body['sku'].keys()):
                    self.to_do = Actions.Update
                if self.body['properties'].get('incremental') is not None and \
                   self.body['properties']['incremental'] != old_response['properties']['incremental']:
                    self.to_do = Actions.Update
                if self.body['properties'].get('osType') is not None and \
                   self.body['properties']['osType'] != old_response['properties'].get('osType'):
                    self.to_do = Actions.Update
                if self.body['properties'].get('creationData') is not None and \
                   not all(self.body['properties']['creationData'][item] == old_response['properties']['creationData'].get(item)
                   for item in self.body['properties']['creationData'].keys()):
                    self.to_do = Actions.Update

                update_tags, self.body['tags'] = self.update_tags(old_response.get('tags'))
                if update_tags:
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log('Need to Create / Update the Snapshot instance')

            if self.check_mode:
                self.results['changed'] = True
                return self.results
            response = self.create_update_resource()
            self.results['changed'] = True
            self.log('Creation / Update done')
        elif self.to_do == Actions.Delete:
            self.log('Snapshot instance deleted')
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_resource()

            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_resource():
                time.sleep(20)
        else:
            self.log('Snapshot instance unchanged')
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]

        return self.results

    def create_update_resource(self):
        # self.log('Creating / Updating the Snapshot instance {0}'.format(self.))
        response = None
        try:
            response = self.mgmt_client.query(url=self.url,
                                              method='PUT',
                                              query_parameters=self.query_parameters,
                                              header_parameters=self.header_parameters,
                                              body=self.body,
                                              expected_status_codes=self.status_code,
                                              polling_timeout=600,
                                              polling_interval=30)
        except Exception as exc:
            self.log('Error attempting to create the Snapshot instance.')
            self.fail('Error creating the Snapshot instance: {0}'.format(str(exc)))

        if hasattr(response, 'body'):
            response = json.loads(response.body())
        elif hasattr(response, 'context'):
            response = response.context['deserialized_data']
        else:
            self.fail("Create or Updating fail, no match message return, return info as {0}".format(response))

        return response

    def delete_resource(self):
        # self.log('Deleting the Snapshot instance {0}'.format(self.))
        try:
            response = self.mgmt_client.query(url=self.url,
                                              method='DELETE',
                                              query_parameters=self.query_parameters,
                                              header_parameters=self.header_parameters,
                                              body=None,
                                              expected_status_codes=self.status_code,
                                              polling_timeout=600,
                                              polling_interval=30)
        except Exception as e:
            self.log('Error attempting to delete the Snapshot instance.')
            self.fail('Error deleting the Snapshot instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        # self.log('Checking if the Snapshot instance {0} is present'.format(self.))
        found = False
        try:
            response = self.mgmt_client.query(url=self.url,
                                              method='GET',
                                              query_parameters=self.query_parameters,
                                              header_parameters=self.header_parameters,
                                              body=None,
                                              expected_status_codes=self.status_code,
                                              polling_timeout=600,
                                              polling_interval=30)
            response = json.loads(response.body())
            found = True
            self.log("Response : {0}".format(response))
            # self.log("Snapshot instance : {0} found".format(response.name))
        except Exception as e:
            self.log('Did not find the Snapshot instance.')
        if found is True:
            return response

        return False


def main():
    AzureRMSnapshots()


if __name__ == '__main__':
    main()
