#!/usr/bin/python
#
# Copyright (c) 2021 Praveen Ghuge(@praveenghuge) Karl Dasan(@karldas30) Saurabh Malpani (@saurabh3796)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_eventhub
version_added: "1.6.0"
short_description: Manage Event Hub
description:
    - Create, update and delete instance of Event Hub.
options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
        type: str
    namespace_name:
        description:
            - Name of the namespace in which to create event hub.
        required: True
        type: str
    name:
        description:
            - Unique name of the Event Hub.
        required: False
        type: str
    message_retention_in_days:
        description:
            - Number of days to retain the events for this Event Hub.
        required: False
        type: int
    partition_count:
        description:
            - Number of partitions created for the Event Hub.
            - Range from 1 to 32.
        required: False
        type: int
    status:
        description:
            - Enumerates the possible values for the status of the Event hub.
        default: Active
        required: False
        type: str
        choices:
            - Active
            - Disabled
            - Restoring
            - SendDisabled
            - ReceiveDisabled
            - Creating
            - Deleting
            - Renaming
            - Unknown
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
        required: False
        type: str
    sku:
        description:
            - The name of the SKU.
            - Please see L(https://azure.microsoft.com/en-in/pricing/details/event-hubs/,).
        default: Basic
        choices:
            - Basic
            - Standard
        type: str
    state:
      description:
          - Assert the state of the Event Hub.
          - Use C(present) to create or update an event hub and C(absent) to delete it.
      default: present
      choices:
          - absent
          - present
      type: str

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Praveen Ghuge (@praveenghuge)
    - Karl Dasan (@karldas30)
    - Saurabh Malpani(@saurabh3796)
'''
EXAMPLES = '''

- name: "Create Event Hub"
  azure_rm_eventhub:
    resource_group: testgroupans
    location: eastus
    namespace_name: myNamespace
    name: myhub
    tags:
       - a: b
    sku: free

- name: Delete Event Hub
  azure_rm_eventhub:
    resource_group: testgroupans
    name: myNamespace
    state: absent

- name: "Create Event Hub Namespace"
  azure_rm_eventhub:
    resource_group: testgroupans
    location: eastus
    namespace_name: myNamespace
    tags:
      a: b
    sku: free

- name: Delete Event Hub Namespace
  azure_rm_eventhub:
    resource_group: testgroupans
    namespace_name: myNamespace
    state: absent

'''

RETURN = '''
state:
    description:
        - Current state of the Event Hub namesapce or Event Hub.
    returned: always
    type: dict
    sample: {
        "additional_properties": {"location": "East US"},
        "critical": false,
        "enabled": true,
        "metric_id": null,
        "name": "testnaedd3d22d3w",
        "namespace_type": "eventHub",
        "status": "Active",
        "region": null,
        "scale_unit": null,
        "service_bus_endpoint": "https://testnaedd3d22d3w.servicebus.windows.net:443/",
        "sku": "Basic",
        "tags": {
            "a": "b"
        },
        "message_retention_in_days": 7,
        "partition_count": 4,
        "partition_ids": ["0", "1", "2", "3"],
        "updated_at": "2021-04-29T10:05:24.000Z",
        "created_at": "2021-04-29T10:05:20.377Z",
        "type": "Microsoft.eventHubs/namespaces"
    }

'''

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.eventhub.models import Eventhub, EHNamespace
    from azure.mgmt.eventhub.models.sku import Sku
except ImportError:
    # This is handled in azure_rm_common
    pass
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
import time


class AzureRMEventHub(AzureRMModuleBase):

    def __init__(self):
        # define user inputs from playbook

        self.authorizations_spec = dict(
            name=dict(type='str', required=True)
        )

        self.module_arg_spec = dict(
            message_retention_in_days=dict(type='int'),
            name=dict(type='str'),
            namespace_name=dict(type='str', required=True),
            partition_count=dict(type='int'),
            resource_group=dict(type='str', required=True),
            sku=dict(type='str', choices=[
                'Basic', 'Standard'], default='Basic'),
            status=dict(choices=["Active", "Disabled", "Restoring", "SendDisabled", "ReceiveDisabled", "Creating", "Deleting", "Renaming", "Unknown"],
                        default='Active', type='str'),
            state=dict(choices=['present', 'absent'],
                       default='present', type='str'),
            location=dict(type='str')
        )
        required_if = [
            ('state', 'present', [
             'partition_count', 'message_retention_in_days'])
        ]
        self.sku = None
        self.resource_group = None
        self.namespace_name = None
        self.message_retention_in_days = None
        self.name = None
        self.location = None
        self.authorizations = None
        self.tags = None
        self.status = None
        self.partition_count = None
        self.results = dict(
            changed=False,
            state=dict()
        )
        self.state = None

        super(AzureRMEventHub, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        # retrieve resource group to make sure it exists
        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        results = dict()
        changed = False

        try:
            self.log(
                'Fetching Event Hub Namespace {0}'.format(self.name))
            namespace = self.event_hub_client.namespaces.get(
                self.resource_group, self.namespace_name)

            results = namespace_to_dict(namespace)
            event_hub_results = None
            if self.name:
                self.log('Fetching event Hub {0}'.format(self.name))
                event_hub = self.event_hub_client.event_hubs.get(
                    self.resource_group, self.namespace_name, self.name)
                event_hub_results = event_hub_to_dict(
                    event_hub)
            # don't change anything if creating an existing namespace, but change if deleting it
            if self.state == 'present':
                changed = False

                update_tags, results['tags'] = self.update_tags(
                    results['tags'])

                if update_tags:
                    changed = True
                elif self.namespace_name and not self.name:
                    if self.sku != results['sku']:
                        changed = True
                elif self.namespace_name and self.name and event_hub_results:
                    if results['sku'] != 'Basic' and self.message_retention_in_days != event_hub_results['message_retention_in_days']:
                        self.sku = results['sku']
                        changed = True
            elif self.state == 'absent':
                changed = True

        except Exception:
            # the event hub does not exist so create it
            if self.state == 'present':
                changed = True
            else:
                # you can't delete what is not there
                changed = False

        self.results['changed'] = changed

        if self.name and not changed:
            self.results['state'] = event_hub_results
        else:
            self.results['state'] = results

        # return the results if your only gathering information
        if self.check_mode:
            return self.results

        if changed:
            if self.state == "present":
                if self.name is None:
                    self.results['state'] = self.create_or_update_namespaces()
                elif self.namespace_name and self.name:
                    self.results['state'] = self.create_or_update_event_hub()
            elif self.state == "absent":
                # delete Event Hub
                if self.name is None:
                    self.delete_namespace()
                elif self.namespace_name and self.name:
                    self.delete_event_hub()
                self.results['state']['status'] = 'Deleted'
        return self.results

    def create_or_update_namespaces(self):
        '''
        create or update namespaces
        '''
        try:
            namespace_params = EHNamespace(
                location=self.location,
                sku=Sku(name=self.sku),
                tags=self.tags
            )
            result = self.event_hub_client.namespaces.create_or_update(
                self.resource_group,
                self.namespace_name,
                namespace_params)

            namespace = self.event_hub_client.namespaces.get(
                self.resource_group,
                self.namespace_name)
            while namespace.provisioning_state == "Created":
                time.sleep(30)
                namespace = self.event_hub_client.namespaces.get(
                    self.resource_group,
                    self.namespace_name,
                )
        except CloudError as ex:
            self.fail("Failed to create namespace {0} in resource group {1}: {2}".format(
                self.namespace_name, self.resource_group, str(ex)))
        return namespace_to_dict(namespace)

    def create_or_update_event_hub(self):
        '''
        Create or update Event Hub.
        :return: create or update Event Hub instance state dictionary
        '''
        try:
            if self.sku == 'Basic':
                self.message_retention_in_days = 1
            params = Eventhub(
                message_retention_in_days=self.message_retention_in_days,
                partition_count=self.partition_count,
                status=self.status
            )
            result = self.event_hub_client.event_hubs.create_or_update(
                self.resource_group,
                self.namespace_name,
                self.name,
                params)

            self.log("Response : {0}".format(result))
        except Exception as ex:
            self.fail("Failed to create event hub {0} in resource group {1}: {2}".format(
                self.name, self.resource_group, str(ex)))
        return event_hub_to_dict(result)

    def delete_event_hub(self):
        '''
        Deletes specified event hub
        :return True
        '''
        self.log("Deleting the event hub {0}".format(self.name))
        try:
            result = self.event_hub_client.event_hubs.delete(
                self.resource_group, self.namespace_name, self.name)
        except CloudError as e:
            self.log('Error attempting to delete event hub.')
            self.fail(
                "Error deleting the event hub : {0}".format(str(e)))
        return True

    def delete_namespace(self):
        '''
        Deletes specified namespace
        :return True
        '''
        self.log("Deleting the namespace {0}".format(self.namespace_name))
        try:
            result = self.event_hub_client.namespaces.delete(
                self.resource_group, self.namespace_name)
        except CloudError as e:
            self.log('Error attempting to delete namespace.')
            self.fail(
                "Error deleting the namespace : {0}".format(str(e)))
        return True


def event_hub_to_dict(item):
    # turn event hub object into a dictionary (serialization)
    event_hub = item.as_dict()
    result = dict()
    if item.additional_properties:
        result['additional_properties'] = item.additional_properties
    result['name'] = event_hub.get('name', None)
    result['partition_ids'] = event_hub.get('partition_ids', None)
    result['created_at'] = event_hub.get('created_at', None)
    result['updated_at'] = event_hub.get('updated_at', None)
    result['message_retention_in_days'] = event_hub.get(
        'message_retention_in_days', None)
    result['partition_count'] = event_hub.get('partition_count', None)
    result['status'] = event_hub.get('status', None)
    result['tags'] = event_hub.get('tags', None)
    return result


def namespace_to_dict(item):
    # turn event hub namespace object into a dictionary (serialization)
    namespace = item.as_dict()
    result = dict(
        additional_properties=namespace.get(
            'additional_properties', {}),
        name=namespace.get('name', None),
        type=namespace.get('type', None),
        location=namespace.get(
            'location', '').replace(' ', '').lower(),
        sku=namespace.get("sku").get("name"),
        tags=namespace.get('tags', None),
        provisioning_state=namespace.get(
            'provisioning_state', None),
        region=namespace.get('region', None),
        metric_id=namespace.get('metric_id', None),
        service_bus_endpoint=namespace.get(
            'service_bus_endpoint', None),
        scale_unit=namespace.get('scale_unit', None),
        enabled=namespace.get('enabled', None),
        critical=namespace.get('critical', None),
        data_center=namespace.get('data_center', None),
        namespace_type=namespace.get('namespace_type', None),
        updated_at=namespace.get('updated_at', None),
        created_at=namespace.get('created_at', None),
        is_auto_inflate_enabled=namespace.get(
            'is_auto_inflate_enabled', None),
        maximum_throughput_units=namespace.get(
            'maximum_throughput_units', None)
    )
    return result


def main():
    AzureRMEventHub()


if __name__ == '__main__':
    main()
