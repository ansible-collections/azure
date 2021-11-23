#!/usr/bin/python
#
# Copyright (c) 2021 Praveen Ghuge (@praveenghuge), Karl Dasan (@karldas30)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_notificationhub
version_added: "1.7.0"
short_description: Manage Notification Hub
description:
    - Create, update and delete instance of Notification Hub.
options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
        type: str
    namespace_name:
        description:
            - Name of the namespace in which to create notification hub.
        required: True
        type: str
    name:
        description:
            - Unique name of the Notification Hub.
        type: str
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
        type: str
    sku:
        description:
            - The name of the SKU.
            - Please see L(https://azure.microsoft.com/en-in/pricing/details/notification-hubs/,).
        default: free
        choices:
            - free
            - basic
            - standard
        type: str
    state:
        description:
            - Assert the state of the Notification Hub.
            - Use C(present) to create or update an notification hub and C(absent) to delete it.
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
'''
EXAMPLES = '''

- name: "Create Notification Hub"
  azure_rm_notificationhub:
    resource_group: testgroupans
    location: eastus
    namespace_name: myNamespace
    name: myhub
    tags:
       - a: b
    sku: free

- name: Delete Notification Hub
  azure_rm_notificationhub:
    resource_group: testgroupans
    name: myNamespace
    state: absent

- name: "Create Notification Hub Namespace"
  azure_rm_notificationhub:
    resource_group: testgroupans
    location: eastus
    namespace_name: myNamespace
    tags:
       - a: b
    sku: free

- name: Delete Notification Hub Namespace
  azure_rm_notificationhub:
    resource_group: testgroupans
    namespace_name: myNamespace
    state: absent

'''

RETURN = '''
state:
    description:
        - Current state of the Notification Hub namesapce or Notification Hub.
    returned: always
    type: dict
    sample: {
        "additional_properties": {},
        "critical": false,
        "data_center": null,
        "enabled": true,
        "location": "eastus2",
        "metric_id": null,
        "name": "testnaedd3d22d3w",
        "namespace_type": "NotificationHub",
        "provisioning_state": "Succeeded",
        "region": null,
        "scale_unit": null,
        "service_bus_endpoint": "https://testnaedd3d22d3w.servicebus.windows.net:443/",
        "sku": "Free",
        "tags": {
            "a": "b"
        },
        "type": "Microsoft.NotificationHubs/namespaces"
    }
'''

import time
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.notificationhubs.models import NotificationHubCreateOrUpdateParameters, NamespaceCreateOrUpdateParameters
    from azure.mgmt.notificationhubs.models.sku import Sku
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureNotificationHub(AzureRMModuleBase):

    def __init__(self):
        # define user inputs from playbook

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            namespace_name=dict(type='str', required=True),
            name=dict(type='str'),
            location=dict(type='str'),
            sku=dict(type='str', choices=[
                     'free', 'basic', 'standard'], default='free'),
            state=dict(choices=['present', 'absent'],
                       default='present', type='str'),
        )

        self.resource_group = None
        self.namespace_name = None
        self.name = None
        self.sku = None
        self.location = None
        self.authorizations = None
        self.tags = None
        self.state = None
        self.results = dict(
            changed=False,
            state=dict()
        )

        super(AzureNotificationHub, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        self.results['check_mode'] = self.check_mode

        # retrieve resource group to make sure it exists
        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            # Set default location
            self.location = resource_group.location

        results = dict()
        changed = False

        try:
            self.log(
                'Fetching Notification Hub Namespace {0}'.format(self.name))
            namespace = self.notification_hub_client.namespaces.get(
                self.resource_group, self.namespace_name)

            results = namespace_to_dict(namespace)
            if self.name:
                self.log('Fetching Notification Hub {0}'.format(self.name))
                notification_hub = self.notification_hub_client.notification_hubs.get(
                    self.resource_group, self.namespace_name, self.name)
                results = notification_hub_to_dict(
                    notification_hub)
            # don't change anything if creating an existing namespace, but change if deleting it
            if self.state == 'present':
                changed = False

                update_tags, results['tags'] = self.update_tags(
                    results['tags'])

                if update_tags:
                    changed = True
                elif self.namespace_name and not self.name:
                    if self.sku != results['sku'].lower():
                        changed = True

            elif self.state == 'absent':
                changed = True

        except CloudError:
            # the notification hub does not exist so create it
            if self.state == 'present':
                changed = True
            else:
                # you can't delete what is not there
                changed = False

        self.results['changed'] = changed
        if self.name and not changed:
            self.results['state'] = results

        # return the results if your only gathering information
        if self.check_mode:
            return self.results

        if changed:
            if self.state == "present":
                if self.name is None:
                    self.results['state'] = self.create_or_update_namespaces()
                elif self.namespace_name and self.name:
                    self.results['state'] = self.create_or_update_notification_hub()
            elif self.state == "absent":
                # delete Notification Hub
                if self.name is None:
                    self.delete_namespace()
                elif self.namespace_name and self.name:
                    self.delete_notification_hub()
                self.results['state']['status'] = 'Deleted'

        return self.results

    def create_or_update_namespaces(self):
        '''
        create or update namespaces
        '''
        try:
            namespace_params = NamespaceCreateOrUpdateParameters(
                location=self.location,
                namespace_type="NotificationHub",
                sku=Sku(name=self.sku),
                tags=self.tags
            )
            result = self.notification_hub_client.namespaces.create_or_update(
                self.resource_group,
                self.namespace_name,
                namespace_params)

            namespace = self.notification_hub_client.namespaces.get(
                self.resource_group,
                self.namespace_name)

            while namespace.status == "Created":
                time.sleep(30)
                namespace = self.notification_hub_client.namespaces.get(
                    self.resource_group,
                    self.namespace_name,
                )
        except CloudError as ex:
            self.fail("Failed to create namespace {0} in resource group {1}: {2}".format(
                self.namespace_name, self.resource_group, str(ex)))
        return namespace_to_dict(result)

    def create_or_update_notification_hub(self):
        '''
        Create or update Notification Hub.
        :return: create or update Notification Hub instance state dictionary
        '''
        try:
            response = self.create_or_update_namespaces()
            params = NotificationHubCreateOrUpdateParameters(
                location=self.location,
                sku=Sku(name=self.sku),
                tags=self.tags
            )
            result = self.notification_hub_client.notification_hubs.create_or_update(
                self.resource_group,
                self.namespace_name,
                self.name,
                params)
            self.log("Response : {0}".format(result))
        except CloudError as ex:
            self.fail("Failed to create notification hub {0} in resource group {1}: {2}".format(
                self.name, self.resource_group, str(ex)))
        return notification_hub_to_dict(result)

    def delete_notification_hub(self):
        '''
        Deletes specified notication hub
        :return True
        '''
        self.log("Deleting the notification hub {0}".format(self.name))
        try:
            result = self.notification_hub_client.notification_hubs.delete(
                self.resource_group, self.namespace_name, self.name)
        except CloudError as e:
            self.log('Error attempting to delete notification hub.')
            self.fail(
                "Error deleting the notification hub : {0}".format(str(e)))
        return True

    def delete_namespace(self):
        '''
        Deletes specified namespace
        :return True
        '''
        self.log("Deleting the namespace {0}".format(self.namespace_name))
        try:
            result = self.notification_hub_client.namespaces.delete(
                self.resource_group, self.namespace_name)
        except CloudError as e:
            self.log('Error attempting to delete namespace.')
            self.fail(
                "Error deleting the namespace : {0}".format(str(e)))
        return True


def notification_hub_to_dict(item):
    # turn notification hub object into a dictionary (serialization)
    notification_hub = item.as_dict()
    result = dict(
        additional_properties=notification_hub.get(
            'additional_properties', {}),
        id=notification_hub.get('id', None),
        name=notification_hub.get('name', None),
        type=notification_hub.get('type', None),
        location=notification_hub.get(
            'location', '').replace(' ', '').lower(),
        tags=notification_hub.get('tags', None),
        provisioning_state=notification_hub.get(
            'provisioning_state', None),
        region=notification_hub.get('region', None),
        metric_id=notification_hub.get('metric_id', None),
        service_bus_endpoint=notification_hub.get(
            'service_bus_endpoint', None),
        scale_unit=notification_hub.get('scale_unit', None),
        enabled=notification_hub.get('enabled', None),
        critical=notification_hub.get('critical', None),
        data_center=notification_hub.get('data_center', None),
        namespace_type=notification_hub.get('namespace_type', None)
    )
    return result


def namespace_to_dict(item):
    # turn notification hub namespace object into a dictionary (serialization)
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
        namespace_type=namespace.get('namespace_type', None)
    )
    return result


def main():
    AzureNotificationHub()


if __name__ == '__main__':
    main()
