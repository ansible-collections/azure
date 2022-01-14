#!/usr/bin/python
#
# Copyright (c) 2021 Praveen Ghuge (@praveenghuge), Karl Dasan (@ikarldasan)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_ddosprotectionplan_info
version_added: "1.7.0"
short_description: Get Azure DDoS protection plan
description:
    - Get facts of Azure DDoS protection plan.
options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
    name:
        description:
            - The name of the DDoS protection plan.
        type: str
extends_documentation_fragment:
- azure.azcollection.azure
author:
    - Praveen Ghuge (@praveenghuge)
    - Karl Dasan (@ikarldasan)
'''


EXAMPLES = '''
  - name: Get facts of specific DDoS protection plan
    azure_rm_ddosprotectionplan_info:
      resource_group: myResourceGroup
      name: myDDoSProtectionPlan
'''

RETURN = '''
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureDDoSProtectionPlanInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False)
        self.resource_group = None
        self.name = None
        self.tags = None

        super(AzureDDoSProtectionPlanInfo, self).__init__(
            self.module_arg_spec, supports_check_mode=True, supports_tags=False)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name is not None:
            results = self.get()
        elif self.resource_group:
            # all the DDoS protection plan listed in that specific resource group
            results = self.list_resource_group()
        else:
            # all the DDoS protection plan listed in the subscription
            results = self.list_subscription()

        self.results['ddosprotectionplan'] = [
            self.ddos_protection_plan_to_dict(x) for x in results]
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.network_client.ddos_protection_plans.get(
                self.resource_group, self.name)
            self.log("Response : {0}".format(response))
        except ResourceNotFoundError as e:
            self.fail('Could not get info for DDoS protection plan. {0}'.format(str(e)))

        if response and self.has_tags(response.tags, self.tags):
            results = [response]
        return results

    def list_resource_group(self):
        self.log('List items for resource group')
        try:
            response = self.network_client.ddos_protection_plans.list_by_resource_group(
                self.resource_group)

        except ResourceNotFoundError as exc:
            self.fail(
                "Failed to list for resource group {0} - {1}".format(self.resource_group, str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def list_subscription(self):
        self.log('List items for subscription')
        try:
            response = self.network_client.ddos_protection_plans.list()

        except ResourceNotFoundError as exc:
            self.fail(
                "Failed to list DDoS protection plan in the subscription - {0}".format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(item)
        return results

    def ddos_protection_plan_to_dict(self, item):
        # turn DDoS protection plan object into a dictionary (serialization)
        ddos_protection_plan = item.as_dict()

        result = dict(
            additional_properties=ddos_protection_plan.get('additional_properties', None),
            id=ddos_protection_plan.get('id', None),
            name=ddos_protection_plan.get('name', None),
            type=ddos_protection_plan.get('type', None),
            location=ddos_protection_plan.get('location', None),
            tags=ddos_protection_plan.get('tags', None),
            etag=ddos_protection_plan.get('etag', None),
            resource_guid=ddos_protection_plan.get('resource_guid', None),
            provisioning_state=ddos_protection_plan.get('provisioning_state', None),
            virtual_networks=ddos_protection_plan.get('virtual_networks', None)
        )
        return result


def main():
    AzureDDoSProtectionPlanInfo()


if __name__ == '__main__':
    main()
