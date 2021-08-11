#!/usr/bin/python
#
# Copyright (c) 2021 Praveen Ghuge(@praveenghuge) Karl Dasan(@karldas30) Saurabh Malpani (@saurabh3796)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_eventhub_info
version_added: "1.6.0"
short_description: Get Azure Event Hub
description:
    - Get facts of Azure Event Hub.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
        type: str
    namespace_name:
        description:
            - The name of the namspace.
        required: False
        type: str
    name:
        description:
            - The name of the Event hub.
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure
author:
    - Saurabh Malpani (@saurabh3796)
'''


EXAMPLES = '''
  - name: Get facts of specific Event hub
    community.azure.azure_rm_eventhub_info:
      resource_group: myResourceGroup
      name: myEventHub
'''

RETURN = '''
state:
    description:
        - Current state of the Event Hub namesapce or Event Hub.
    returned: always
    type: dict
    sample: {
            "additional_properties": {},
            "created_at": "2021-04-19T12:49:46.597Z",
            "critical": null,
            "data_center": null,
            "status": "Active",
            "location": "eastus",
            "metric_id": "149f0952-6f3d-48ba-9e98-57011575cbbd:eventhubtestns1753",
            "name": "eventhubtestns1753",
            "namespace_type": null,
            "provisioning_state": "Succeeded",
            "region": null,
            "scale_unit": null,
            "service_bus_endpoint": "https://eventhubtestns1753.servicebus.windows.net:443/",
            "sku": "Basic",
            "tags": {},
            "type": "Microsoft.EventHub/Namespaces",
            "updated_at": "2021-04-19T12:54:33.397Z"
    }
'''

try:
    from msrestazure.azure_exceptions import CloudError
except ImportError:
    # This is handled in azure_rm_common
    pass
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMEventHubInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            namespace_name=dict(
                type='str',
                required=False
            ),
            name=dict(
                type='str',
                required=False
            )
        )

        # store the results of the module operation
        self.results = dict(
            changed=False)
        self.resource_group = None
        self.namespace_name = None
        self.name = None
        self.tags = None

        super(AzureRMEventHubInfo, self).__init__(
            self.module_arg_spec, supports_check_mode=True, supports_tags=False)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name and self.namespace_name and self.resource_group:
            results = self.get_event_hub()
            self.results['eventhub'] = [
                self.event_hub_to_dict(x) for x in results]
        elif self.namespace_name:
            results = self.get_namespace()
            self.results['namespace'] = [
                self.namespace_to_dict(x) for x in results]
        elif self.name is None and self.namespace_name is None:
            results = self.list_all_namespace()
            self.results['namespaces'] = [
                self.namespace_to_dict(x) for x in results]
        return self.results

    def get_namespace(self):
        '''
        Get the namespace using resource group and namespace name
        '''
        response = None
        results = []
        try:
            response = self.event_hub_client.namespaces.get(
                self.resource_group, self.namespace_name)
            self.log("Response : {0}".format(response))

        except CloudError as e:
            self.fail('Could not get info for namespace. {0}').format(
                str(e))

        if response:
            results = [response]
        return results

    def get_event_hub(self):
        '''
        get event hub using resource_group, namespace_name and name.
        '''
        response = None
        results = []

        try:
            response = self.event_hub_client.event_hubs.get(
                self.resource_group, self.namespace_name, self.name)

        except CloudError as e:
            self.fail('Could not get info for event hub. {0}').format(
                str(e))

        if response:
            results = [response]
        return results

    def list_all_namespace(self):
        '''
        List all namespaces in particular resource_group
        '''
        self.log('List items for resource group')
        try:
            response = self.event_hub_client.namespaces.list_by_resource_group(
                self.resource_group)

        except CloudError as exc:
            self.fail(
                "Failed to list for resource group {0} - {1}".format(self.resource_group, str(exc)))

        results = []
        for item in response:
            results.append(item)
        return results

    def namespace_to_dict(self, item):
        # turn event hub object into a dictionary (serialization)
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

    def event_hub_to_dict(self, item):
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


def main():
    AzureRMEventHubInfo()


if __name__ == '__main__':
    main()
